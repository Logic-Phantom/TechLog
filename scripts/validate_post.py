"""게시글 품질·SEO 검증 (auto_post.py 가 새 글 저장 직후 호출, 단독 실행도 가능).

  python3 scripts/validate_post.py blog-front/contents/<슬러그>.md   # 엄격 모드: 오류가 있으면 종료 코드 1
  python3 scripts/validate_post.py --all                               # 기존 글 전체 보고 (항상 종료 코드 0)
  LINK_CHECK=0 ...                                                     # 외부 링크 접속 확인 생략

판정 기준
  오류(ERROR)  — 저장소 안에서 확정할 수 있는 문제: 프론트매터 누락·형식, 썸네일/본문 이미지 파일 없음,
                 없는 내부 게시글 링크, 슬러그 형식, 제목 불일치, 닫히지 않은 코드 블록, 형식이 깨진 URL, 동일 제목
  경고(WARN)   — 외부 사정이나 판단이 섞인 문제: 외부 링크 응답 실패(일시 오류·차단 가능), 요약 길이,
                 기존 글과의 유사도, 언어 태그 없는 코드 블록, 용어 표기 불일치, 이미지 alt 누락
기술적 정확성(설명과 코드의 의미 일치, API 동작)은 자동으로 보장할 수 없으므로 경고 수준의 휴리스틱만 둔다.
"""
import difflib
import glob
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENTS = os.path.join(ROOT, 'blog-front', 'contents')
SITE_HOST = 'logic-phantom.github.io'
SITE_PAGES = {'/', '/stats/', '/rss.xml', '/sitemap-index.xml', '/robots.txt'}
REQUIRED = ['date', 'title', 'categories', 'summary', 'thumbnail', 'comments']
MAX_LINK_CHECKS = 40


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def split_front(text):
    m = re.match(r'\A---\r?\n(.*?)\r?\n---\r?\n', text, re.S)
    if not m:
        return None, text
    front = {}
    for line in m.group(1).splitlines():
        km = re.match(r'^([A-Za-z_]+):\s*(.*)$', line)
        if km:
            front[km.group(1)] = km.group(2).strip()
    return front, text[m.end():]


def unquote(v):
    return v[1:-1] if len(v) >= 2 and v[0] == v[-1] and v[0] in '\'"' else v


def strip_emoji(s):
    return re.sub(r'[^\w\s가-힣.+#/-]', '', s).strip()


def strip_code(body):
    """코드 블록·인라인 코드를 지운 본문 (링크·용어 검사용)."""
    body = re.sub(r'^(```|~~~).*?^\1\s*$', '', body, flags=re.S | re.M)
    return re.sub(r'`[^`\n]*`', '', body)


def slug_of(path):
    return '/' + os.path.basename(path)[:-3] + '/'


def post_index(exclude=None):
    posts = {}
    for p in glob.glob(os.path.join(CONTENTS, '*.md')):
        if exclude and os.path.abspath(p) == os.path.abspath(exclude):
            continue
        front, body = split_front(read(p))
        posts[slug_of(p)] = {'title': unquote((front or {}).get('title', '')), 'body': body}
    return posts


def words(text):
    return set(w for w in re.findall(r'[0-9A-Za-z가-힣]{2,}', text.lower()))


def check_url(url):
    """외부 URL 접속 확인. (상태, 설명) — 실패해도 경고로만 쓴다."""
    headers = {'User-Agent': 'Mozilla/5.0 (compatible; logic-phantom-link-check)'}
    last = ''
    for method in ('HEAD', 'GET'):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, 'ok'
        except urllib.error.HTTPError as e:
            last = f'HTTP {e.code}'
            if e.code in (404, 410) and method == 'GET':
                return e.code, '페이지 없음 (주소 확인 필요)'
            if e.code in (405, 403, 404, 410, 429, 500, 501, 502, 503):
                continue  # HEAD 미지원·봇 차단·일시 오류 → GET 으로 한 번 더
            return e.code, last
        except (OSError, ValueError) as e:
            last = f'{type(e).__name__}'
    return None, f'접속 실패 ({last}, 일시 오류·차단일 수 있음)'


def validate(path, strict=True, network=True):
    """(errors, warnings) 리스트 반환."""
    errors, warns = [], []
    err = errors.append if strict else warns.append
    text = read(path)
    if text.startswith('﻿'):
        err('UTF-8 BOM 이 있습니다 (BOM 없이 저장)')
        text = text[1:]
    front, body = split_front(text)
    name = os.path.basename(path)

    # 1) 파일명 = 슬러그
    if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*\.md', name):
        err(f'파일명(슬러그)이 kebab-case 영문이 아닙니다: {name}')

    # 2) 프론트매터
    if front is None:
        errors.append('프론트매터(--- ... ---) 블록이 없습니다')
        return errors, warns
    for k in REQUIRED:
        if not front.get(k):
            errors.append(f'프론트매터 {k} 누락')
    date = front.get('date', '')
    if date and not re.fullmatch(r"'\d{4}-\d{2}-\d{2}'", date):
        err(f"date 형식 오류: {date} (작은따옴표 'YYYY-MM-DD')")
    if front.get('categories') and not re.fullmatch(r'\[\s*[\'"][^\]]+\]', front['categories']):
        err(f'categories 형식 오류: {front["categories"]}')
    if front.get('comments') and front['comments'] != 'true':
        warns.append(f'comments 가 true 가 아닙니다: {front["comments"]}')

    title = unquote(front.get('title', ''))
    summary = unquote(front.get('summary', ''))
    if title and len(title) > 70:
        warns.append(f'제목이 깁니다({len(title)}자) — 검색 결과에서 잘릴 수 있음')
    if summary:
        if not 10 <= len(summary) <= 25:
            warns.append(f'summary 길이 {len(summary)}자 (가이드 10~25자)')
        if strip_emoji(summary) == strip_emoji(title):
            warns.append('summary 가 제목과 같습니다 (meta description 으로 쓰임)')

    # 3) 썸네일
    thumb = unquote(front.get('thumbnail', ''))
    if thumb:
        if not thumb.startswith('./images/'):
            warns.append(f'thumbnail 이 ./images/ 아래가 아닙니다: {thumb}')
        if not os.path.isfile(os.path.normpath(os.path.join(CONTENTS, thumb))):
            errors.append(f'썸네일 파일 없음: {thumb}')

    # 4) 본문 첫 제목 = 프론트매터 title
    first = next((l for l in body.splitlines() if l.strip()), '')
    if not first.startswith('# '):
        err('본문이 `# 제목` 으로 시작하지 않습니다')
    elif title and first[2:].strip() != title:
        err(f'본문 제목과 프론트매터 title 이 다릅니다: "{first[2:].strip()}" ≠ "{title}"')

    # 5) 코드 블록
    fences = re.findall(r'^(```|~~~)(.*)$', body, re.M)
    if len(fences) % 2:
        errors.append('닫히지 않은 코드 블록이 있습니다')
    no_lang = sum(1 for i, (_, lang) in enumerate(fences) if i % 2 == 0 and not lang.strip())
    if no_lang:
        warns.append(f'언어 태그 없는 코드 블록 {no_lang}개')

    prose = strip_code(body)

    # 6) 이미지
    for alt, src in re.findall(r'!\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)', prose):
        if not alt.strip():
            warns.append(f'이미지 alt 텍스트 없음: {src}')
        if re.match(r'https?://', src):
            continue
        if not os.path.isfile(os.path.normpath(os.path.join(CONTENTS, urllib.parse.unquote(src)))):
            errors.append(f'본문 이미지 없음: {src}')

    # 7) 링크 (내부 게시글 / 외부 URL)
    known = set(post_index().keys()) | SITE_PAGES
    external = []
    for label, href in re.findall(r'(?<!!)\[([^\]]*)\]\(([^)\s]+)(?:\s+"[^"]*")?\)', prose):
        href = href.strip('<>')
        if href.startswith('#') or href.startswith('mailto:'):
            continue
        parsed = urllib.parse.urlparse(href)
        if parsed.scheme in ('http', 'https'):
            if not parsed.netloc or ' ' in href:
                errors.append(f'URL 형식 오류: {href}')
            elif parsed.netloc.lower() == SITE_HOST:
                internal = urllib.parse.unquote(parsed.path or '/')
                internal = internal if internal.endswith('/') or '.' in internal.rsplit('/', 1)[-1] else internal + '/'
                if internal not in known:
                    errors.append(f'존재하지 않는 내부 링크: {href}')
            else:
                external.append(href)
        elif parsed.scheme:
            warns.append(f'http(s) 가 아닌 링크: {href}')
        elif href.startswith('/'):
            internal = urllib.parse.unquote(parsed.path)
            internal = internal if internal.endswith('/') or '.' in internal.rsplit('/', 1)[-1] else internal + '/'
            if internal not in known:
                errors.append(f'존재하지 않는 내부 링크: {href}')
        elif href.endswith('.md') or href.startswith('./') or href.startswith('../'):
            target = os.path.normpath(os.path.join(CONTENTS, urllib.parse.unquote(parsed.path)))
            if not os.path.exists(target):
                errors.append(f'존재하지 않는 상대 링크: {href}')
    if '참고 자료' in body and not external:
        warns.append('참고 자료 절에 외부 링크가 없습니다')
    if network:
        for url in list(dict.fromkeys(external))[:MAX_LINK_CHECKS]:
            status, note = check_url(url)
            if status is None or status >= 400:
                warns.append(f'외부 링크 확인 실패: {url} — {note}')

    # 8) 기존 글과의 중복 가능성
    others = post_index(exclude=path)
    norm_title = strip_emoji(title).lower()
    mine = words(prose)
    for slug, other in others.items():
        other_title = strip_emoji(other['title']).lower()
        if norm_title and other_title == norm_title:
            err(f'기존 글과 제목이 같습니다: {slug}')
            continue
        ratio = difflib.SequenceMatcher(None, norm_title, other_title).ratio() if norm_title else 0
        if ratio >= 0.8:
            warns.append(f'기존 글과 제목이 비슷합니다({ratio:.0%}): {slug} "{other["title"]}"')
        theirs = words(strip_code(other['body']))
        if mine and theirs:
            jac = len(mine & theirs) / len(mine | theirs)
            if jac >= 0.5:
                warns.append(f'기존 글과 본문 어휘가 많이 겹칩니다({jac:.0%}): {slug}')

    # 9) 기술 용어 표기 일관성 (예: JavaScript / Javascript, WebSocket / Websocket)
    variants = {}
    # 한글 조사가 바로 붙는 경우(JavaScript에서)도 잡도록 경계는 ASCII 문자로만 판단
    for tok in re.findall(r'(?<![A-Za-z0-9_./-])[A-Za-z][A-Za-z0-9]*(?:\.[A-Za-z]+)?(?![A-Za-z0-9_/-])', prose):
        if len(tok) >= 4:
            variants.setdefault(tok.lower(), {}).setdefault(tok, 0)
            variants[tok.lower()][tok] += 1
    for forms in variants.values():
        if len(forms) > 1 and any(re.search(r'[a-z][A-Z]', f) for f in forms):
            listed = ', '.join(f'{f}({n})' for f, n in sorted(forms.items(), key=lambda x: -x[1]))
            warns.append(f'용어 표기가 섞여 있습니다: {listed}')

    return errors, warns


def report(path, errors, warns):
    rel = os.path.relpath(path, ROOT)
    for e in errors:
        print(f'ERROR {rel}: {e}', flush=True)
    for w in warns:
        print(f'WARN  {rel}: {w}', flush=True)


def main(argv):
    network = os.environ.get('LINK_CHECK', '1') != '0' and '--no-network' not in argv
    args = [a for a in argv if not a.startswith('--')]
    if '--all' in argv:
        files = sorted(glob.glob(os.path.join(CONTENTS, '*.md')))
        n_err = n_warn = 0
        for p in files:
            errors, warns = validate(p, strict=False, network=network)
            report(p, errors, warns)
            n_err += bool(errors)
            n_warn += bool(warns)
        print(f'검사 {len(files)}편: 오류 있는 글 {n_err}편, 경고 있는 글 {n_warn}편 (보고 모드, 종료 코드 0)')
        return 0
    if not args:
        print(__doc__)
        return 2
    failed = False
    for p in args:
        errors, warns = validate(p, strict=True, network=network)
        report(p, errors, warns)
        failed = failed or bool(errors)
        print(f'{os.path.relpath(p, ROOT)}: 오류 {len(errors)}건, 경고 {len(warns)}건')
    return 1 if failed else 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
