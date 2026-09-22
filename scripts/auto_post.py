"""매일 자동 게시글 생성 (Gemini 무료 API, 요청 1회).

Gemini CLI 같은 에이전트는 도구 호출마다 API 요청을 쓰므로 무료 한도(모델당 하루 20회 내외)를 금방 넘긴다.
그래서 README 작성 가이드와 기존 글 목록을 한 번에 넘기고, 글 본문 + 이미지 명세를 JSON 한 덩어리로 받는다.
파일 저장·이미지 렌더링·README 갱신은 이 스크립트가 결정적으로 처리한다.

환경 변수
  GEMINI_API_KEY  필수
  GEMINI_MODELS   쉼표 구분 모델 목록. 앞에서부터 시도하고 404/429면 다음 모델로 넘어간다.
  TODAY           YYYY-MM-DD (기본: 오늘)
  DRY_RUN_JSON    지정 시 API 대신 이 JSON 파일을 사용 (로컬 테스트용)
"""
import datetime
import glob
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'scripts'))
from draw_kit import thumbnail_base, thumbnail_devices, thumbnail_panel, flow_diagram, compare_diagram  # noqa: E402

CONTENTS = os.path.join(ROOT, 'blog-front', 'contents')
README = os.path.join(ROOT, 'README.md')
DEFAULT_MODELS = 'gemini-3.8-flash,gemini-3.7-flash,gemini-3.6-flash,gemini-3.5-flash,gemini-3.5-flash-lite'

CATEGORIES = ['Web', 'AI', 'HTTP', 'CI/CD', 'ETC', 'Server', 'React', 'Mobile', 'JavaScript', 'UI', 'Java',
              'Python', 'Html', 'Css', 'Error', 'Developer Tool', 'Language', 'Polices']
FOLDERS = ['web', 'AI', 'javascript', 'html', 'http', 'css', 'next', 'pwa', 'server', 'mcp', 'mob', 'vercel',
           'vibe', 'gatsby', 'markup', 'error', 'spa-mpa', 'etc']

STEP = {'type': 'OBJECT', 'properties': {'label': {'type': 'STRING'}, 'sub': {'type': 'STRING'},
                                         'note': {'type': 'STRING'}}, 'required': ['label']}
SIDE = {'type': 'OBJECT', 'properties': {'title': {'type': 'STRING'},
                                         'rows': {'type': 'ARRAY', 'items': {'type': 'STRING'}},
                                         'result': {'type': 'STRING'}}, 'required': ['title', 'rows', 'result']}
SCHEMA = {
    'type': 'OBJECT',
    'properties': {
        'slug': {'type': 'STRING'},
        'emoji': {'type': 'STRING'},
        'title': {'type': 'STRING'},
        'summary': {'type': 'STRING'},
        'categories': {'type': 'ARRAY', 'items': {'type': 'STRING'}},
        'image_folder': {'type': 'STRING'},
        'readme_area': {'type': 'STRING'},
        'readme_topic': {'type': 'STRING'},
        'used_candidate': {'type': 'STRING'},
        'thumbnail': {'type': 'OBJECT', 'properties': {
            'keyword_lines': {'type': 'ARRAY', 'items': {'type': 'STRING'}},
            'badge': {'type': 'STRING'}, 'caption': {'type': 'STRING'}},
            'required': ['keyword_lines', 'badge', 'caption']},
        'diagrams': {'type': 'ARRAY', 'items': {'type': 'OBJECT', 'properties': {
            'kind': {'type': 'STRING', 'enum': ['flow', 'compare']},
            'title': {'type': 'STRING'}, 'caption': {'type': 'STRING'}, 'alt': {'type': 'STRING'},
            'steps': {'type': 'ARRAY', 'items': STEP}, 'left': SIDE, 'right': SIDE},
            'required': ['kind', 'title', 'caption', 'alt']}},
        'body': {'type': 'STRING'},
    },
    'required': ['slug', 'emoji', 'title', 'summary', 'categories', 'image_folder', 'readme_area',
                 'readme_topic', 'thumbnail', 'diagrams', 'body'],
}


def read(p):
    with open(p, encoding='utf-8') as f:
        return f.read()


def write(p, s):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, 'w', encoding='utf-8', newline='\n') as f:
        f.write(s)


def guide_section(readme):
    """README의 작성 가이드 1~6절 (7절 이미지 생성 방법은 스크립트가 대신하므로 제외)."""
    start = readme.index('## 📝 블로그 포스트 작성 가이드')
    end = readme.index('### 7.', start)
    return readme[start:end]


def existing_posts():
    rows = []
    for p in sorted(glob.glob(os.path.join(CONTENTS, '*.md'))):
        m = re.search(r"^title:\s*'(.*)'", read(p), re.M)
        rows.append(f"- {os.path.basename(p)[:-3]} : {m.group(1) if m else ''}")
    return '\n'.join(rows)


def build_prompt(today, readme):
    return f"""너는 Logic-Phantom 기술 블로그의 필자다. 오늘({today})자 새 게시글 1편을 작성해 JSON으로 반환한다.

# 작성 규약 (README 발췌 — 반드시 따를 것)
{guide_section(readme)}

# 이미 존재하는 게시글 (슬러그 : 제목) — 이 주제들과 겹치면 안 된다
{existing_posts()}

# 출력 규칙
- 주제: 위 "아직 비어 있는 후보"에서 하나를 고르고 `used_candidate`에 후보 문자열을 **그대로** 적는다. 후보가 없으면 겹치지 않는 새 주제를 정하고 빈 문자열.
- slug: kebab-case 영문, 기존 슬러그와 달라야 함.
- emoji: 이모지 1개. title: 이모지를 **뺀** 제목.
- summary: 10~25자 후킹 카피.
- categories: {CATEGORIES} 중 1~2개. 대부분 ["Web"].
- image_folder: {FOLDERS} 중 하나.
- readme_area: README 4절 표의 "분야" 값 중 하나(없으면 새 분야명), readme_topic: 표에 추가할 짧은 주제명.
- thumbnail.keyword_lines: 영문 대문자 키워드 1~2줄(한 줄 10자 이내). badge: 영문 대문자 부제(16자 이내). caption: 한글 카피 한 줄(18자 이내).
- diagrams: 1~2개. kind="flow"면 steps 3~5개(label 12자 이내, sub 18자 이내, note는 선택·12자 이내).
  kind="compare"면 left(기존 방식)/right(새 방식) 각각 rows 3개(20자 이내)와 result(12자 이내). title은 30자 이내 한글+영문, caption은 45자 이내 한 문장.
- body: 프론트매터 없이 `# (이모지) (제목)` 으로 시작하는 마크다운 본문. README 5절 구조(인용구, 목차, 10~14개 이모지 번호 섹션, 비교표, 언어 태그가 있는 코드 블록, 실무 함정, 쓰면 안 되는 경우, 정리 + 한 줄 요약, 참고 자료)를 지킨다.
  분량은 한국어 기준 충실하게(15~25KB). 다이어그램이 들어갈 위치에 `{{{{DIAGRAM_1}}}}`, `{{{{DIAGRAM_2}}}}` 자리표시자를 한 줄로 단독 배치한다.
- 확실하지 않은 API·함수명은 지어내지 말고, 널리 알려진 공식 API와 라이브러리만 사용한다. 참고 자료 링크는 공식 문서 위주.
"""


def call_gemini(prompt):
    key = os.environ['GEMINI_API_KEY']
    models = [m.strip() for m in os.environ.get('GEMINI_MODELS', DEFAULT_MODELS).split(',') if m.strip()]
    body = json.dumps({
        'contents': [{'role': 'user', 'parts': [{'text': prompt}]}],
        'generationConfig': {'responseMimeType': 'application/json', 'responseSchema': SCHEMA,
                             'temperature': 0.9, 'maxOutputTokens': 32768},
    }).encode()
    for model in models:
        url = f'https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent'
        for attempt in range(2):
            req = urllib.request.Request(url, data=body, method='POST', headers={
                'Content-Type': 'application/json', 'x-goog-api-key': key})
            try:
                with urllib.request.urlopen(req, timeout=600) as r:
                    data = json.load(r)
            except urllib.error.HTTPError as e:
                msg = e.read().decode(errors='replace')[:300]
                print(f'[{model}] HTTP {e.code}: {msg}')
                if e.code >= 500 and attempt == 0:
                    time.sleep(20)
                    continue
                break  # 404(모델 없음)·429(한도)·4xx → 다음 모델
            except (urllib.error.URLError, TimeoutError) as e:
                print(f'[{model}] 네트워크 오류: {e}')
                break
            cand = (data.get('candidates') or [{}])[0]
            parts = cand.get('content', {}).get('parts', [])
            text = ''.join(p.get('text', '') for p in parts if not p.get('thought'))
            if not text:
                print(f'[{model}] 빈 응답 (finishReason={cand.get("finishReason")})')
                break
            print(f'[{model}] 응답 {len(text)}자, usage={data.get("usageMetadata")}')
            return json.loads(text)
    sys.exit('모든 모델 호출 실패')


def update_readme(readme, area, topic, candidate):
    lines = readme.split('\n')
    start = next(i for i, l in enumerate(lines) if l.startswith('| 분야 | 기존 주제 |'))
    i = start + 2
    done = False
    while i < len(lines) and lines[i].startswith('|'):
        cells = [c.strip() for c in lines[i].strip('|').split('|')]
        if cells[0] == area:
            lines[i] = f'| {cells[0]} | {cells[1]}, {topic} |'
            done = True
            break
        i += 1
    if not done:
        lines.insert(i, f'| {area} | {topic} |')
    s = '\n'.join(lines)
    if candidate:
        tok = f'`{candidate}`'
        s = s.replace(f'{tok} · ', '').replace(f' · {tok}', '').replace(tok, '')
    return s


def main():
    today = os.environ.get('TODAY') or datetime.date.today().isoformat()
    readme = read(README)

    if os.environ.get('DRY_RUN_JSON'):
        post = json.loads(read(os.environ['DRY_RUN_JSON']))
    else:
        post = call_gemini(build_prompt(today, readme))

    slug = re.sub(r'[^a-z0-9-]', '-', post['slug'].lower()).strip('-')
    slug = re.sub(r'-{2,}', '-', slug)
    if os.path.exists(os.path.join(CONTENTS, slug + '.md')):
        slug = f'{slug}-{today.replace("-", "")}'
    folder = post['image_folder'] if post['image_folder'] in FOLDERS else 'web'
    cats = [c for c in post['categories'] if c in CATEGORIES][:2] or ['Web']
    emoji = post['emoji'].strip()[:2] or '📝'
    title = post['title'].strip().replace("'", '’')
    summary = post['summary'].strip().replace("'", '’')
    img_dir = os.path.join(CONTENTS, 'images', folder)
    os.makedirs(img_dir, exist_ok=True)

    # 썸네일
    t = post['thumbnail']
    img, d = thumbnail_base()
    thumbnail_devices(d)
    thumbnail_panel(d, [k.upper() for k in t['keyword_lines'][:2]] or ['TECH'], t['badge'].upper(), t['caption'])
    img.save(os.path.join(img_dir, f'{slug}.png'))

    # 다이어그램
    body = post['body'].strip()
    for n, dg in enumerate(post['diagrams'][:2], 1):
        fname = f'{slug}-{n}.png'
        path = os.path.join(img_dir, fname)
        if dg['kind'] == 'compare' and dg.get('left') and dg.get('right'):
            compare_diagram(path, dg['title'], dg['left'], dg['right'], dg['caption'])
        else:
            flow_diagram(path, dg['title'], dg.get('steps') or [{'label': dg['title']}], dg['caption'])
        tag = f'![{dg["alt"]}](./images/{folder}/{fname})'
        ph = '{{DIAGRAM_%d}}' % n
        if ph in body:
            body = body.replace(ph, tag)
        else:  # 자리표시자를 빠뜨렸으면 두 번째 섹션 구분선 뒤에 삽입
            parts = body.split('\n---\n')
            idx = min(len(parts) - 1, 2 + n)
            parts[idx] = parts[idx].rstrip() + '\n\n' + tag + '\n'
            body = '\n---\n'.join(parts)
    body = re.sub(r'\{\{DIAGRAM_\d\}\}\n?', '', body)

    # 본문 첫 줄 제목을 프론트매터와 일치시킴
    heading = f'# {emoji} {title}'
    body = re.sub(r'\A#\s+.*', heading, body) if body.startswith('#') else heading + '\n\n' + body

    front = (f"---\ndate: '{today}'\ntitle: '{emoji} {title}'\ncategories: [{', '.join(repr(c) for c in cats)}]\n"
             f"summary: '{summary}'\nthumbnail: './images/{folder}/{slug}.png'\ncomments: true\n---\n")
    write(os.path.join(CONTENTS, slug + '.md'), front + body + '\n')
    write(README, update_readme(readme, post['readme_area'].strip(), post['readme_topic'].strip(),
                                (post.get('used_candidate') or '').strip()))
    print(f'작성 완료: blog-front/contents/{slug}.md ({len((front + body).encode())} bytes)')


if __name__ == '__main__':
    main()
