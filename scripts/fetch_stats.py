"""GoatCounter 통계 → 공개용 조회수 JSON (배포 빌드 직전에 실행).

토큰은 이 스크립트(서버 측, GitHub Actions)에서만 쓰고, 결과 JSON 에는 경로와 숫자만 남긴다.
API 가 안 되면(토큰 없음·401/403/404 등) 토큰이 필요 없는 공개 방문자 카운터로 게시글마다 조회한다.
둘 다 실패해도 종료 코드는 0 — 블로그는 통계 없이 정상 빌드된다 (가짜 수치를 만들지 않음).

환경 변수
  GATSBY_GOATCOUNTER_ENDPOINT  필수. https://코드.goatcounter.com/count — 여기서 API·카운터 주소를 계산
  GOATCOUNTER_API_TOKEN        (선택) GoatCounter → Settings → API 에서 "통계 읽기" 권한만 준 토큰 (GitHub Secrets)
  GOATCOUNTER_API_URL          (선택) API 주소 직접 지정, 예: https://코드.goatcounter.com/api/v0
  GOATCOUNTER_STATS_START      (선택) 누적 집계 시작일 YYYY-MM-DD (기본 2026-10-01, 측정 도입 시점)
  STATS_OUTPUT                 (선택) 출력 경로 (기본 blog-front/static/data/popular-posts.json)

API (https://www.goatcounter.com/help/api, /api.json OpenAPI 스펙 기준)
  GET /api/v0/stats/total  → {"total": 정수, ...}
  GET /api/v0/stats/hits   → {"hits": [{"path_id", "path", "count", "event", ...}], "more": bool}
                             limit 최대 100, 다음 페이지는 exclude_paths 에 받은 path_id 를 넘긴다
  GET /api/v0/me           → 토큰 확인용 (404 진단에만 사용, 응답 내용은 출력하지 않음)
  인증: Authorization: Bearer <token>, 요청 한도 초당 4회
  404 는 "데이터 없음"이 아니라 토큰은 맞는데 서버 DB 조회가 빈 결과일 때 나온다 (zhttp: sql.ErrNoRows → 404)

공개 카운터 (토큰 불필요, Settings → "Allow adding visitor counts" 필요)
  GET /counter/<인코딩된 경로>.json → {"count": "1,234", ...}  기록 없는 경로는 404 + count 0
  GET /counter/TOTAL.json          → 사이트 전체. 기간 지정 없이 전체 누적, 응답은 최대 4시간 캐시
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


class StatsError(RuntimeError):
    def __init__(self, msg, code=None):
        super().__init__(msg)
        self.code = code


def site_base():
    """GATSBY_GOATCOUNTER_ENDPOINT(https://코드.goatcounter.com/count) → https://코드.goatcounter.com"""
    endpoint = (os.environ.get('GATSBY_GOATCOUNTER_ENDPOINT') or '').strip()
    if not re.fullmatch(r'https://[^/\s]+/count/?', endpoint):
        return None
    return re.sub(r'/count/?$', '', endpoint)


def api_base():
    url = (os.environ.get('GOATCOUNTER_API_URL') or '').strip().rstrip('/')
    if not url and site_base():
        url = site_base() + '/api/v0'
    if not re.fullmatch(r'https://[^\s]+/api/v0', url or ''):
        return None
    return url


def fetch_json(url, headers, label):
    """GET 요청. 429·5xx·네트워크 오류는 최대 3회 재시도, 그 밖의 HTTP 오류는 StatsError(code)."""
    for attempt in range(3):
        req = urllib.request.Request(url, headers={'User-Agent': 'logic-phantom-techlog-stats', **headers})
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code == 429 or e.code >= 500:
                wait = int(e.headers.get('X-Rate-Limit-Reset') or 0) + 1 if e.code == 429 else 5 * (attempt + 1)
                log(f'{label} HTTP {e.code}, {wait}초 후 재시도')
                time.sleep(min(wait, 30))
                continue
            raise StatsError(f'{label} HTTP {e.code}', e.code) from None
        except (OSError, ValueError) as e:
            log(f'{label} 네트워크/응답 오류 {type(e).__name__}, 재시도')
            time.sleep(5 * (attempt + 1))
    raise StatsError(f'{label} 요청 실패 (재시도 초과)')


def request(base, token, path, params):
    """API 요청. 토큰은 절대 출력하지 않는다."""
    url = f'{base}{path}?{urllib.parse.urlencode(params)}'
    try:
        return fetch_json(url, {'Authorization': f'Bearer {token}'}, path)
    except StatsError as e:
        if e.code in (401, 403):
            raise StatsError(f'인증 실패 HTTP {e.code} — 토큰 값이나 "통계 읽기" 권한을 확인하세요', e.code) from None
        raise


def diagnose_404(base, token):
    """/stats/total 404 원인 구분: /me 도 404 면 토큰에 연결된 사용자를 서버가 못 찾는 상태."""
    try:
        request(base, token, '/me', {})
        log('진단: /me 는 정상 → 토큰은 유효하지만 통계 조회가 404. GoatCounter 쪽 문제일 수 있음')
    except StatsError as e:
        if e.code == 404:
            log('진단: /me 도 404 → 토큰의 사용자를 찾지 못함. GoatCounter에서 토큰을 새로 발급해 Secrets를 교체하세요')
        else:
            log(f'진단: /me 실패 ({e})')


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


def counter(site, path):
    """공개 카운터 한 경로의 누적 수. 기록이 없는 경로는 404(count 0)라 0으로 본다."""
    name = 'TOTAL' if path == 'TOTAL' else urllib.parse.quote(path, safe="!*'()")
    try:
        data = fetch_json(f'{site}/counter/{name}.json', {}, f'/counter/{name}.json')
    except StatsError as e:
        if e.code == 404:
            return 0
        raise
    digits = re.sub(r'[^0-9]', '', str(data.get('count', '')))  # "1,234" 처럼 구분자가 들어 있음
    if not digits:
        raise StatsError(f'/counter/{name}.json 응답에 count 없음')
    return int(digits)


def collect_public(site, slugs):
    """API 대신 공개 카운터로 게시글마다 조회 (게시글 수만큼 요청, 초당 4회 이하)."""
    try:
        total = counter(site, 'TOTAL')
    except StatsError as e:
        raise StatsError(f'공개 카운터 사용 불가: {e} — GoatCounter Settings의 "Allow adding visitor counts" 확인', e.code) from None
    counts = {}
    for slug in sorted(slugs):
        time.sleep(0.3)
        counts[slug] = counter(site, slug)
    return total, counts


def main():
    site = site_base()
    if not site:
        log('GATSBY_GOATCOUNTER_ENDPOINT 미설정 → 통계 없이 빌드합니다')
        return 0
    token = (os.environ.get('GOATCOUNTER_API_TOKEN') or '').strip()
    base = api_base()

    start_day = (os.environ.get('GOATCOUNTER_STATS_START') or DEFAULT_START).strip()
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', start_day):
        log(f'GOATCOUNTER_STATS_START 형식 오류({start_day}) → 기본값 {DEFAULT_START} 사용')
        start_day = DEFAULT_START
    now = datetime.datetime.now(datetime.timezone.utc).replace(minute=0, second=0, microsecond=0)
    # 게시글 날짜가 KST 라서 시작일도 KST 자정(= 전날 15:00 UTC)부터 센다. 저장은 UTC, 표시는 /stats/ 에서 KST 로 변환
    kst_midnight = datetime.datetime.strptime(start_day, '%Y-%m-%d') - datetime.timedelta(hours=9)
    start = kst_midnight.strftime('%Y-%m-%dT%H:%M:%SZ')
    end = now.strftime('%Y-%m-%dT%H:%M:%SZ')

    slugs = post_slugs()
    total = counts = None
    source = 'goatcounter'
    if token and base:
        try:
            total, counts = collect(base, token, start, end)
        except StatsError as e:
            log(f'API 통계 수집 실패: {e} → 공개 카운터로 대체합니다')
            if e.code == 404:
                diagnose_404(base, token)
    else:
        log('GOATCOUNTER_API_TOKEN 미설정 → 공개 카운터로 수집합니다')

    if counts is None:
        try:
            total, counts = collect_public(site, slugs)
        except StatsError as e:
            log(f'통계 수집 실패: {e} → 통계 없이 빌드합니다')
            return 0
        source, start = 'goatcounter-counter', None  # 공개 카운터는 기간 지정 없이 전체 누적

    posts = sorted(({'path': p, 'views': v} for p, v in counts.items() if p in slugs and v > 0),
                   key=lambda x: (-x['views'], x['path']))
    result = {
        'generatedAt': datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'source': source,
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
    log(f'저장: {os.path.relpath(OUTPUT, ROOT)} ({source}, 전체 {total}, 게시글 {len(posts)}편 / 조회 경로 {len(counts)}개)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
