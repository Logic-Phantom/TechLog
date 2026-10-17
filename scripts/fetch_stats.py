"""GoatCounter 통계 API → 공개용 조회수 JSON (배포 빌드 직전에 실행).

토큰은 이 스크립트(서버 측, GitHub Actions)에서만 쓰고, 결과 JSON 에는 경로와 숫자만 남긴다.
API·토큰이 없거나 실패해도 종료 코드는 0 — 블로그는 통계 없이 정상 빌드된다 (가짜 수치를 만들지 않음).

환경 변수
  GOATCOUNTER_API_TOKEN        필수. GoatCounter → Settings → API 에서 "통계 읽기" 권한만 준 토큰 (GitHub Secrets)
  GATSBY_GOATCOUNTER_ENDPOINT  https://코드.goatcounter.com/count — 여기서 API 주소를 계산
  GOATCOUNTER_API_URL          (선택) API 주소 직접 지정, 예: https://코드.goatcounter.com/api/v0
  GOATCOUNTER_STATS_START      (선택) 누적 집계 시작일 YYYY-MM-DD (기본 2026-10-01, 측정 도입 시점)
  STATS_OUTPUT                 (선택) 출력 경로 (기본 blog-front/static/data/popular-posts.json)

API (https://www.goatcounter.com/help/api, /api.json OpenAPI 스펙 기준)
  GET /api/v0/stats/total  → {"total": 정수, ...}
  GET /api/v0/stats/hits   → {"hits": [{"path_id", "path", "count", "event", ...}], "more": bool}
                             limit 최대 100, 다음 페이지는 exclude_paths 에 받은 path_id 를 넘긴다
  인증: Authorization: Bearer <token>, 요청 한도 초당 4회
"""
import datetime
import glob
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENTS = os.path.join(ROOT, 'blog-front', 'contents')
OUTPUT = os.environ.get('STATS_OUTPUT') or os.path.join(ROOT, 'blog-front', 'static', 'data', 'popular-posts.json')
DEFAULT_START = '2026-10-01'
MAX_PAGES = 50


def log(msg):
    print(f'[stats] {msg}', flush=True)


def normalize_path(raw):
    """src/utils/analytics.ts 의 normalizePath 와 같은 규칙: 쿼리·해시 제거, 디코딩, 앞뒤 슬래시."""
    path = re.split(r'[?#]', raw or '/')[0]
    path = urllib.parse.unquote(path)
    if not path.startswith('/'):
        path = '/' + path
    last = path.rsplit('/', 1)[-1]
    if not path.endswith('/') and '.' not in last:
        path += '/'
    return re.sub(r'/{2,}', '/', path)


def post_slugs():
    """gatsby-node 의 createFilePath 와 같은 규칙: contents/<이름>.md → /<이름>/"""
    return {normalize_path('/' + os.path.basename(p)[:-3] + '/') for p in glob.glob(os.path.join(CONTENTS, '*.md'))}


def api_base():
    url = (os.environ.get('GOATCOUNTER_API_URL') or '').strip().rstrip('/')
    if not url:
        endpoint = (os.environ.get('GATSBY_GOATCOUNTER_ENDPOINT') or '').strip()
        if re.fullmatch(r'https://[^/\s]+/count/?', endpoint):
            url = re.sub(r'/count/?$', '', endpoint) + '/api/v0'
    if not re.fullmatch(r'https://[^\s]+/api/v0', url or ''):
        return None
    return url


def request(base, token, path, params):
    """GET 요청. 429·5xx·네트워크 오류는 최대 3회 재시도. 토큰은 절대 출력하지 않는다."""
    url = f'{base}{path}?{urllib.parse.urlencode(params)}'
    for attempt in range(3):
        req = urllib.request.Request(url, headers={
            'Authorization': f'Bearer {token}', 'Content-Type': 'application/json',
            'User-Agent': 'logic-phantom-techlog-stats'})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code in (401, 403):
                raise RuntimeError(f'인증 실패 HTTP {e.code} — 토큰 값이나 "통계 읽기" 권한을 확인하세요') from None
            if e.code == 429 or e.code >= 500:
                wait = int(e.headers.get('X-Rate-Limit-Reset') or 0) + 1 if e.code == 429 else 5 * (attempt + 1)
                log(f'{path} HTTP {e.code}, {wait}초 후 재시도')
                time.sleep(min(wait, 30))
                continue
            raise RuntimeError(f'{path} HTTP {e.code}') from None
        except (OSError, ValueError) as e:
            log(f'{path} 네트워크/응답 오류 {type(e).__name__}, 재시도')
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f'{path} 요청 실패 (재시도 초과)')


def collect(base, token, start, end):
    window = {'start': start, 'end': end}
    total = request(base, token, '/stats/total', window).get('total')

    counts, seen = {}, []
    for _ in range(MAX_PAGES):
        params = dict(window, limit=100)
        if seen:
            params['exclude_paths'] = ','.join(str(i) for i in seen)
        data = request(base, token, '/stats/hits', params)
        hits = data.get('hits') or []
        new_ids = [h.get('path_id') for h in hits if isinstance(h.get('path_id'), int) and h['path_id'] not in seen]
        for h in hits:
            if h.get('event') or not isinstance(h.get('path'), str) or not isinstance(h.get('count'), int):
                continue
            key = normalize_path(h['path'])
            counts[key] = counts.get(key, 0) + max(h['count'], 0)
        seen.extend(new_ids)
        if not data.get('more') or not new_ids:
            break
        time.sleep(0.3)  # 초당 4회 제한
    return (total if isinstance(total, int) else None), counts


def main():
    token = (os.environ.get('GOATCOUNTER_API_TOKEN') or '').strip()
    base = api_base()
    if not token or not base:
        log('GOATCOUNTER_API_TOKEN 또는 GATSBY_GOATCOUNTER_ENDPOINT(GOATCOUNTER_API_URL) 미설정 → 통계 없이 빌드합니다')
        return 0

    start_day = (os.environ.get('GOATCOUNTER_STATS_START') or DEFAULT_START).strip()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', start_day):
        log(f'GOATCOUNTER_STATS_START 형식 오류({start_day}) → 기본값 {DEFAULT_START} 사용')
        start_day = DEFAULT_START
    now = datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)
    start = f'{start_day}T00:00:00Z'
    end = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    try:
        total, counts = collect(base, token, start, end)
    except RuntimeError as e:
        log(f'통계 수집 실패: {e} → 통계 없이 빌드합니다')
        return 0

    slugs = post_slugs()
    posts = sorted(({'path': p, 'views': v} for p, v in counts.items() if p in slugs and v > 0),
                   key=lambda x: (-x['views'], x['path']))
    result = {
        'generatedAt': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'source': 'goatcounter',
        'metric': 'visitors',
        'rangeStart': start,
        'rangeEnd': end,
        'totalViews': total,
        'posts': posts,
    }
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    tmp = OUTPUT + '.tmp'
    with open(tmp, 'w', encoding='utf-8', newline='\n') as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
        f.write('\n')
    os.replace(tmp, OUTPUT)
    log(f'저장: {os.path.relpath(OUTPUT, ROOT)} (전체 {total}, 게시글 {len(posts)}편 / API 경로 {len(counts)}개)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
