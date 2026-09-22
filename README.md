# 🚀 Logic-Phantom 기술 블로그

개발의 흔적을 기록하고 지식을 나누는 공간,  
**Logic-Phantom의 개인 기술 블로그**입니다.

[Gatsby](https://www.gatsbyjs.com/) 기반으로 구축되었으며, GitHub Pages를 통해 배포되고 있습니다.

> 📍 블로그 주소: [https://logic-phantom.github.io](https://logic-phantom.github.io)

---

## ✨ 블로그 특징

### 1. 최신 웹 기술 적용
- PWA(Progressive Web App) 지원으로 앱처럼 설치 가능
- 오프라인 지원으로 네트워크 없이도 접근 가능
- 모바일 최적화 및 반응형 디자인

### 2. 개발자 친화적 기능
- 마크다운 기반의 간편한 글 작성
- 코드 하이라이팅 지원
- 다크모드 지원
- 댓글 시스템 (Utterances) 통합

### 3. 성능 최적화
- Gatsby의 정적 사이트 생성으로 빠른 로딩
- 이미지 최적화 및 지연 로딩
- SEO 최적화
- 캐싱 전략 구현

### 4. 사용자 경험
- 카테고리/태그 기반 글 분류
- 검색 기능
- 깔끔한 타이포그래피
- 부드러운 페이지 전환

---

## 🛠 기술 스택

| 영역 | 기술 스택 |
|------|------------|
| 프레임워크 | React, Gatsby |
| 스타일링 | Styled Components, Emotion |
| 마크다운 | Remark, Prism.js |
| 배포 | GitHub Pages |
| CI/CD | GitHub Actions |
| PWA | Workbox, Service Workers |
| 댓글 | Utterances |

---

## 📁 프로젝트 구조

```bash
TechLog/
├── blog-front/              # 블로그 프론트엔드
│   ├── contents/           # 블로그 포스트 (Markdown)
│   │   └── images/        # 포스트별 썸네일·다이어그램 (주제 폴더로 분류)
│   ├── src/
│   │   ├── components/    # 리액트 컴포넌트
│   │   ├── pages/        # 페이지 컴포넌트
│   │   └── templates/    # 포스트 템플릿
│   ├── static/           # 정적 파일
│   ├── gatsby-config.js  # Gatsby 설정
│   └── gatsby-node.js    # Gatsby Node API
└── .github/
    └── workflows/        # GitHub Actions 워크플로우
```

---

## 🔧 주요 기능 구현

### PWA 구현
- Web App Manifest 설정
- Service Worker 구현
- 오프라인 지원
- 앱 설치 기능

### 블로그 기능
- 마크다운 포스트 작성
- 코드 블록 하이라이팅
- 이미지 최적화
- 반응형 레이아웃

### 자동화
- GitHub Actions를 통한 자동 배포
- **매일 한국시간 12:00 자동 게시글 발행** (`.github/workflows/daily-post.yml`)
  - `scripts/auto_post.py`가 아래 작성 가이드 + 기존 글 목록을 Gemini 무료 API에 **1회** 보내 본문·이미지 명세(JSON)를 받음
    → 썸네일·다이어그램 렌더링(`scripts/draw_kit.py`) → README 4절 갱신 → 검증 → `main` 푸시 → `deploy.yml` 호출
  - 필요 시크릿: `GEMINI_API_KEY` (Google AI Studio 발급) / 모델 순서 변경: 저장소 Variables `GEMINI_MODELS` (쉼표 구분)
  - 무료 등급은 모델당 하루 요청 수가 매우 적어(약 20회) 도구를 반복 호출하는 CLI 에이전트 방식은 쓰지 않음
  - 로컬 테스트: `DRY_RUN_JSON=샘플.json python3 scripts/auto_post.py` (API 호출 없이 렌더링만)
  - 즉시 실행: `.github/triggers/daily-post` 파일을 수정해 푸시하거나 Actions 탭 → Run workflow (force)
  - 그날 날짜의 글이 이미 있으면 건너뜀. Actions 탭에서 수동 실행 가능
- 이미지 최적화 자동화
- SEO 메타데이터 자동 생성

---

## 📝 블로그 포스트 작성 가이드

> 🤖 **AI 에이전트에게 "리드미 읽고 게시글 작성해줘" 라고만 요청해도 되도록** 이 절에 모든 규약을 적어 둡니다.
> 별도 지시가 없으면 **아직 다루지 않은 새 주제**를 골라 아래 규칙대로 본문과 이미지를 함께 생성합니다.

### 1. 파일 위치와 이름

```bash
blog-front/contents/<슬러그>.md          # 본문
blog-front/contents/images/<주제폴더>/   # 썸네일 + 본문 다이어그램
```

- 파일명은 **kebab-case 영문**(예: `local-first-crdt-guide.md`)
- `gatsby-node.js`가 `createFilePath`로 **파일명을 그대로 URL 슬러그**로 씁니다 → `/local-first-crdt-guide/`
- 인코딩은 **UTF-8 (BOM 없음)**

### 2. 프론트매터

```markdown
---
date: '2026-09-20'
title: '🔄 로컬 퍼스트(Local-First) 웹과 CRDT 완벽 가이드'
categories: ['Web']
summary: '서버가 아니라 내 기기가 원본이다'
thumbnail: './images/web/localFirst.png'
comments: true
---
```

| 필드 | 규칙 |
|------|------|
| `date` | `'YYYY-MM-DD'` 작은따옴표 필수. 목록은 **date DESC, title ASC** 로 정렬 |
| `title` | 앞에 이모지 1개 + 제목. 본문 첫 줄의 `#` 제목과 동일하게 |
| `categories` | **아래 3절의 기존 값 재사용** (새 값 남발 금지) |
| `summary` | 카드에 노출되는 **짧은 한 줄 카피** (10~25자). 문장 설명이 아니라 후킹 문구 |
| `thumbnail` | `contents` 기준 상대경로. 반드시 실제 파일을 함께 생성 |
| `comments` | 항상 `true` |

### 3. 카테고리 (실제 사용 중인 값)

`Web` · `AI` · `HTTP` · `CI/CD` · `ETC` · `Server` · `React` · `Mobile` · `JavaScript` · `UI` · `Java` · `Python` · `Html` · `Css` · `Error` · `Developer Tool` · `Language` · `Polices`

- 대부분의 글은 `['Web']` 단독을 씁니다. 필요할 때만 `['Web','AI']`처럼 2개까지 조합
- 기존 표기를 확인하려면: `grep -h "^categories:" blog-front/contents/*.md | sort | uniq -c | sort -rn`

### 4. 주제 선정 — 중복 피하기

**이미 다룬 영역** (새 글은 이 범위를 벗어나야 함)

| 분야 | 기존 주제 |
|------|-----------|
| JavaScript | ES5/ES6 핵심, 비동기·클로저, 에러 처리, 내장/외부 유틸 라이브러리, JS vs TS, window 객체 |
| 프레임워크 | React 구조, Next.js, Gatsby, Svelte, htmx, Flutter, 마이크로 프론트엔드, SPA vs MPA, Virtual DOM |
| 브라우저·표준 | HTML 렌더링 과정, 웹 표준, 웹 접근성, Web Worker, WebAssembly, WebGPU, 자동재생 정책, 3D 인터랙티브 웹, View Transitions API |
| 네트워크 | HTTP/1~3, 상태 코드, WebSocket·STOMP, FCM 푸시 |
| 성능 | Web Vitals, 모바일 비디오 최적화, ISR·엣지 캐싱, 캐시 vs 세션 |
| 서버 | Spring / Spring Boot, JVM, VO·DTO, 모놀리스, 백엔드 API 비교, Supabase, Web vs WAS |
| 인프라 | Jamstack, Vercel, 배포 아키텍처, 클라우드, PWA, WebView vs PWA |
| AI | LLM 개요, Web LLM, 브라우저 Transformer, MCP, 에이전틱 웹, AI 코딩 도구, AI 거버넌스, 바이브 코딩, YOLOv5, agno |
| 보안 | 웹 보안 정책, 웹 취약점 대응, 패스키·WebAuthn |
| 데이터·협업 | 로컬 퍼스트 & CRDT |

**아직 비어 있는 후보** (바로 골라 쓸 수 있는 목록)

`WebRTC 실시간 미디어` · `CSS Container Queries & :has()` · `Web Components / Shadow DOM` · `Service Worker 캐싱 전략 심화` · `WebTransport & HTTP/3 스트리밍` · `프론트엔드 관측성(OpenTelemetry·RUM)` · `Signals 기반 반응성` · `아일랜드 아키텍처(Astro)` · `Origin Private File System` · `WebCodecs` · `국제화(i18n)와 Intl API` · `SQLite in the Browser (WASM)` · `Feature Flag & 점진 배포`

> 새 글을 쓴 뒤에는 위 표에 주제를 한 줄 추가하고, 후보 목록에서 해당 항목을 제거합니다.

### 5. 본문 구조

기존 글들이 공유하는 뼈대입니다.

```markdown
# (프론트매터 title과 동일)

> 핵심을 찌르는 인용구 한두 줄
> 이 글에서 무엇을 다루는지

---

## 📌 목차
1. ...  (10~14개 섹션)

---

## 🧭 1. 첫 섹션
본문 — 개념 → 코드 → 표 → 함정 순으로 전개

![다이어그램 설명](./images/web/xxx.png)

---

## 🧾 N. 정리
- 불릿 5~6개로 핵심 회수

> ✨ **한 줄 요약**
> 기억에 남을 한 문장

---

## 📚 참고 자료
- [공식 문서](https://...)
```

작성 원칙:
- 섹션 제목마다 **이모지 1개**, 번호 부여
- **비교는 반드시 표**로 (`| 구분 | A | B |`)
- 코드 블록에는 언어 태그(`js`, `jsx`, `bash`, `text`) 명시
- 단순 소개에서 끝내지 말고 **실무 함정 / 쓰면 안 되는 경우**를 한 섹션 이상 포함
- 분량은 **15~25KB** 수준 (기존 글 평균 대비 충실한 편)

### 6. 이미지 규칙

| 용도 | 크기 | 배경 | 저장 위치 |
|------|------|------|-----------|
| 썸네일 | **1536 × 1024** (3:2) | 연하늘 `#D6E8FB` 플랫 일러스트 | `images/<주제>/<이름>.png` |
| 본문 다이어그램 | **1280 × 600~700** | 흰색, 설명용 도식 | 동일 폴더 |

주제 폴더: `web` · `AI` · `javascript` · `html` · `http` · `css` · `next` · `pwa` · `server` · `mcp` · `mob` · `vercel` · `vibe` · `gatsby` · `markup` · `error` · `spa-mpa` · `etc`

**공통 팔레트** (기존 썸네일과 톤을 맞추기 위해 그대로 사용)

```text
배경 #D6E8FB   네이비 #1E3A5F   블루 #5B8FD4   연블루 #A8C9EF
페일 #C6DEF8   그린 #279866    레드 #CE4747   그레이 #788A9E   페이퍼 #F9FBFE
```

썸네일 구성: 연하늘 배경 + 구름/플러스 장식 → 가운데 흰 라운드 패널에 **영문 대문자 키워드**(네이비 굵게) → 하단 네이비 알약 배지에 부제 → 좌우에 기기·아이콘 → 맨 아래 한글 카피 한 줄.

### 7. 이미지 생성 방법

**macOS / Linux / CI (권장)**: Python + Pillow 로 그립니다. 팔레트·썸네일 레이아웃 헬퍼가 `scripts/draw_kit.py`에 있습니다.

```bash
python3 -m venv .venv && .venv/bin/pip install pillow   # 최초 1회 (.venv는 커밋하지 않음)
```

```python
import sys; sys.path.insert(0, 'scripts')
from draw_kit import *

img, d = thumbnail_base()                                  # 연하늘 배경 + 구름/플러스
thumbnail_panel(d, ['PASS', 'KEYS'], 'WEBAUTHN', '비밀번호 없는 로그인')
img.save('blog-front/contents/images/web/passkey.png')

img, d = canvas(1280, 680, 'white')                        # 본문 다이어그램
rrect(d, (40, 110, 310, 200), 18, fill='pale', outline='navy', width=5)
text_c(d, 175, 155, '브라우저', 28, bold=True)
arrow(d, (320, 155), (480, 155), color='blue', dashed=True)
```

한글 폰트는 macOS `AppleSDGothicNeo`, Ubuntu `fonts-noto-cjk`, Windows `Malgun Gothic` 순으로 자동 탐색합니다.

**Windows (Node·Python 없는 환경)**: 아래처럼 PowerShell + System.Drawing 으로 그립니다.

이 저장소의 작업 환경에는 `node`/`python`이 없습니다. **Windows PowerShell + System.Drawing**으로 PNG를 직접 그립니다.

> ⚠️ 스크립트 파일은 반드시 **UTF-8 with BOM** 으로 저장해야 합니다.
> BOM이 없으면 Windows PowerShell 5.1이 ANSI로 읽어 한글이 깨지고 파서 에러가 납니다.
>
> ```powershell
> $t = [IO.File]::ReadAllText($p, [Text.Encoding]::UTF8)
> [IO.File]::WriteAllText($p, $t, (New-Object Text.UTF8Encoding $true))
> ```

최소 뼈대:

```powershell
Add-Type -AssemblyName System.Drawing
function Hex($h) { [System.Drawing.ColorTranslator]::FromHtml($h) }

function RR($x, $y, $w, $h, $r) {          # 라운드 사각형 경로
  $p = New-Object System.Drawing.Drawing2D.GraphicsPath; $d = $r * 2
  $p.AddArc($x, $y, $d, $d, 180, 90);            $p.AddArc($x + $w - $d, $y, $d, $d, 270, 90)
  $p.AddArc($x + $w - $d, $y + $h - $d, $d, $d, 0, 90); $p.AddArc($x, $y + $h - $d, $d, $d, 90, 90)
  $p.CloseFigure(); $p
}

function NewFont($size, $bold) {           # 한글은 Malgun Gothic, 단위는 Pixel
  $st = if ($bold) { [System.Drawing.FontStyle]::Bold } else { [System.Drawing.FontStyle]::Regular }
  New-Object System.Drawing.Font('Malgun Gothic', $size, $st, [System.Drawing.GraphicsUnit]::Pixel)
}

$bmp = New-Object System.Drawing.Bitmap(1536, 1024)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$g.TextRenderingHint = [System.Drawing.Text.TextRenderingHint]::AntiAliasGridFit
$g.Clear((Hex '#D6E8FB'))

# ... FillPath / DrawString / FillPolygon(화살촉) 으로 구성 ...

$bmp.Save('blog-front/contents/images/web/example.png', [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $bmp.Dispose()
```

레이아웃 주의점:
- **텍스트는 `RectangleF` + `StringFormat(Center, Center)`** 로 중앙 정렬 — 폭이 부족하면 조용히 잘리므로 한글 1자당 폰트 크기만큼 폭을 확보
- 화살표는 패널보다 **나중에** 그려야 가려지지 않음
- 좌우 요소는 캔버스 중심(768px) 기준으로 대칭 배치

### 8. 작성 체크리스트

- [ ] 기존 글과 겹치지 않는 주제인가 (4절 표 확인)
- [ ] 파일명 = 슬러그, kebab-case
- [ ] 프론트매터 7개 필드 + `date`에 작은따옴표
- [ ] `thumbnail` 경로의 PNG를 **실제로 생성**했는가
- [ ] 본문 다이어그램 1~2장 삽입 및 경로 확인
- [ ] 목차 / 비교표 / 코드 블록 / 함정 섹션 / 한 줄 요약 / 참고 자료 포함
- [ ] 4절 "이미 다룬 영역" 표에 새 주제 추가

---

## 🚀 시작하기

1. 저장소 클론
```bash
git clone https://github.com/Logic-Phantom/TechLog.git
```

2. 의존성 설치
```bash
cd blog-front
npm install
```

3. 개발 서버 실행
```bash
gatsby develop
```

4. 빌드
```bash
gatsby build
```

---

## 📘 Documentation

자세한 문서는 다음 포스트들을 참고하세요:
- [Gatsby로 기술 블로그 만들기](https://logic-phantom.github.io/gatsby)
- [PWA 적용하기](https://logic-phantom.github.io/pwa-implementation)
- [GitHub Pages 배포하기](https://logic-phantom.github.io/github-pages)

---

## 🔄 최근 업데이트

- PWA 기능 추가 (2024.03)
- 댓글 시스템 Utterances 적용
- 다크모드 지원
- 이미지 최적화 개선
- SEO 최적화

---

## 📬 Contact

- GitHub: [@Logic-Phantom](https://github.com/Logic-Phantom)
- Blog: [https://logic-phantom.github.io](https://logic-phantom.github.io)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
