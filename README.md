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
- 댓글 시스템 (Utterances) 통합

### 3. 성능 최적화
- Gatsby의 정적 사이트 생성으로 빠른 로딩
- 이미지 최적화 및 지연 로딩
- SEO 최적화
- 캐싱 전략 구현

### 4. 사용자 경험
- 카테고리 기반 글 분류
- 깔끔한 타이포그래피
- 부드러운 페이지 전환

### 5. 검색 노출·분석·성장 (설정 방법은 아래 [📈 검색·분석·통계 운영](#-검색분석통계-운영))
- Google Search Console 대응: `sitemap-index.xml`, `robots.txt`, 게시글별 title·description·canonical·Open Graph·Twitter 카드, `BlogPosting` 구조화 데이터
- GA4 방문자 분석 (측정 ID가 있을 때만 로드, SPA 이동 포함 페이지뷰 1회씩)
- GoatCounter 공개 조회수: 게시글 상세 `👁 조회수`, 목록 카드·인기 글 TOP 5·`/stats/` 통계 페이지 (실제 집계값만 표시)
- 게시글 공유(Web Share API)·링크 복사, 관련 글 자동 추천(`함께 읽으면 좋은 글`)
- RSS 피드 `/rss.xml` (최신 50편, 자동 발견 `<link rel="alternate">` 포함)
- 자동 발행 글 품질·SEO 검증 (`scripts/validate_post.py`)

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
| 자동 발행 | Gemini API (무료 등급), Python + Pillow |

---

## 📁 프로젝트 구조

```bash
TechLog/
├── blog-front/              # 블로그 프론트엔드
│   ├── contents/           # 블로그 포스트 (Markdown)
│   │   └── images/        # 포스트별 썸네일·다이어그램 (주제 폴더로 분류)
│   ├── src/
│   │   ├── components/    # 리액트 컴포넌트 (Post/ViewCounter·PostShare·RelatedPosts, Main/PopularPosts 등)
│   │   ├── pages/        # 페이지 컴포넌트 (index, stats = /stats/ 통계 페이지)
│   │   ├── templates/    # 포스트 템플릿
│   │   └── utils/        # analytics.ts (GA4·GoatCounter), stats.ts (조회수 매핑·정렬)
│   ├── static/           # 정적 파일 (robots.txt, 빌드 때 생성되는 data/popular-posts.json)
│   ├── gatsby-config.js  # Gatsby 설정 (sitemap·RSS·canonical·PWA)
│   ├── gatsby-node.js    # Gatsby Node API (slug, 관련 글 계산, 통계 노드)
│   ├── gatsby-ssr.js     # lang="ko", 분석 스크립트 삽입 (운영 빌드 + 환경 변수 있을 때만)
│   └── gatsby-browser.js # 페이지 이동마다 페이지뷰 전송
├── scripts/
│   ├── auto_post.py      # 매일 자동 게시글 생성 (Gemini API 호출 → 본문·이미지·검증·README 반영)
│   ├── validate_post.py  # 게시글 품질·SEO 검증 (auto_post.py가 호출, 단독 실행 가능)
│   ├── fetch_stats.py    # GoatCounter 통계 API(실패 시 공개 카운터) → 공개 조회수 JSON (deploy.yml이 빌드 전에 실행)
│   └── draw_kit.py       # 썸네일·다이어그램 렌더링 헬퍼 (Pillow, 공통 팔레트)
└── .github/
    ├── workflows/
    │   ├── deploy.yml     # main 푸시 시 Gatsby 빌드 → Logic-Phantom.github.io 배포
    │   └── daily-post.yml # 매일 12:00(KST) 자동 게시글 작성 → 푸시 → 배포 호출
    └── triggers/
        └── daily-post     # 이 파일을 수정해 푸시하면 자동 발행을 즉시 실행
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
- GitHub Actions를 통한 자동 배포 (`deploy.yml`, `main` 푸시 또는 수동 호출)
- **매일 한국시간 12:00 자동 게시글 발행** (`daily-post.yml`)

```text
cron 03:17 / 07:17 / 11:17 UTC (= 12:17 / 16:17 / 20:17 KST, GitHub 사정으로 수 시간 지연 가능)
 → 오늘 날짜 글이 이미 있으면 건너뜀 (그래서 뒤 두 번은 앞 실행이 실패한 날만 동작하는 재시도)
 → scripts/auto_post.py
     ① 아래 "작성 가이드" + 기존 글 목록을 Gemini에 1회 전송 → 본문 + 이미지 명세(JSON) 수신
        503·연결 끊김·잘린 JSON이면 다음 모델로, 전 모델 실패 시 2분·5분 쉬고 최대 3라운드 재시도
     ② 본문이 15KB 미만이면 보강 요청 1회 추가
     ③ 썸네일·다이어그램 렌더링(draw_kit.py) → 본문 자리표시자에 이미지 삽입
     ④ 프론트매터 생성 → scripts/validate_post.py 품질·SEO 검증 (오류면 여기서 실패, 아래 표 참고)
     ⑤ README 4절 주제 표·후보 목록 갱신
 → 검증: 새 .md 1개, 프론트매터 7개 필드, 썸네일·본문 이미지 존재, 분량
 → main에 rebase 후 푸시 → deploy.yml 호출 (GITHUB_TOKEN 푸시는 push 트리거가 안 걸리므로 직접 호출)
```

| 항목 | 내용 |
|------|------|
| 필요 시크릿 | `GEMINI_API_KEY` (Google AI Studio 발급) |
| 모델 | 최신 Flash부터 순서대로 시도, 한도 초과·미지원이면 다음 모델. 변경은 Variables `GEMINI_MODELS` (쉼표 구분) |
| 즉시 실행 | Actions 탭 → Daily Auto Post → Run workflow (`force` 체크) 또는 `.github/triggers/daily-post` 수정 후 푸시 |
| 놓친 날 채우기 | Run workflow의 `date`에 `YYYY-MM-DD` 입력, 또는 트리거 파일에 `date=YYYY-MM-DD` 한 줄을 넣고 푸시 (그 날짜 글이 이미 있으면 건너뜀) |
| 실패 확인 | 실행 결과 화면의 annotation에 로그 끝부분이 남음. 실패하면 푸시하지 않고 같은 날 다음 cron에서 재시도 |
| 로컬 테스트 | `DRY_RUN_JSON=샘플.json python3 scripts/auto_post.py` (API 호출 없이 렌더링만) |
| 중지 | Actions 탭 → Daily Auto Post → `...` → Disable workflow |

> 💡 무료 등급은 모델당 하루 요청 수가 매우 적어(약 20회) 도구를 반복 호출하는 CLI 에이전트(Gemini CLI 등)는 한도를 초과합니다.
> 그래서 요청 1~2회로 끝나도록 **생성은 Gemini, 저장·이미지·검증은 스크립트**로 역할을 나눴습니다.

- 이미지 최적화 자동화
- SEO 메타데이터 자동 생성

#### 자동 검증 항목 (`scripts/validate_post.py`)

Gemini를 추가로 호출하지 않고, 새 글을 저장한 직후 스크립트가 검사합니다. **오류**가 하나라도 있으면 README를 고치기 전에 실패하고, 워크플로우는 푸시하지 않은 채 같은 날 다음 cron에서 다시 시도합니다.

| 구분 | 항목 |
|------|------|
| 오류 (실패) | 프론트매터 블록·7개 필드 누락, `date` 형식(`'YYYY-MM-DD'`), `categories` 형식, 파일명 kebab-case, 본문 첫 `#` 제목 = `title`, 썸네일·본문 이미지 파일 없음, 없는 내부 게시글 링크(`/slug/`, `https://logic-phantom.github.io/...`), 깨진 URL 형식, 닫히지 않은 코드 블록, 기존 글과 **같은 제목**, UTF-8 BOM |
| 경고 (통과) | 외부 링크 접속 실패(일시 오류·봇 차단일 수 있어 HEAD→GET 재시도 후 경고만), `summary` 길이(10~25자)·제목과 동일, 제목 70자 초과, 기존 글과 제목 유사(80%↑)·본문 어휘 중복(50%↑), 언어 태그 없는 코드 블록, 용어 표기 혼용(`JavaScript`/`Javascript`), 이미지 alt 누락, 참고 자료에 외부 링크 없음 |

- 단독 실행: `python3 scripts/validate_post.py blog-front/contents/<슬러그>.md` (오류면 종료 코드 1)
- 기존 글 전체 보고: `python3 scripts/validate_post.py --all --no-network` (항상 종료 코드 0, 기존 글은 수정하지 않음)
- 외부 링크 확인 생략: `LINK_CHECK=0`
- ⚠️ 분량·형식 검사가 **기술적 정확성**(설명과 코드의 의미 일치, API·버전 사실 관계)을 보장하지는 않습니다. 용어 표기 혼용 같은 휴리스틱 경고만 있으니 발행 후 사람이 확인해야 합니다.

---

## 📈 검색·분석·통계 운영

### 구성 요약

```text
[브라우저]  gatsby-ssr.js 가 넣은 gtag.js / GoatCounter count.js
              └ gatsby-browser.js onRouteUpdate → 페이지 이동마다 page_view 1회 (GA4·GoatCounter)
            게시글 상세 👁 조회수 ← GoatCounter 공개 카운터 /counter/<경로>.json (토큰 불필요)

[배포 빌드] deploy.yml
              ① scripts/fetch_stats.py  (GOATCOUNTER_API_TOKEN 사용, 서버 측에서만)
                   GoatCounter API /stats/total, /stats/hits → blog-front/static/data/popular-posts.json
                   API 실패·토큰 없음 → 공개 카운터 /counter/<경로>.json 을 게시글마다 조회 (전체 누적)
                   (경로·숫자만 저장, 실제 게시글이 아닌 경로는 제외, 커밋하지 않음)
              ② gatsby build → 인기 글 TOP 5 · 카드 조회수 · /stats/ 페이지에 반영
```

- 모든 외부 연동은 **선택**입니다. 값이 없으면 해당 스크립트·UI만 빠지고 블로그는 그대로 빌드·동작합니다.
- 조회수가 없을 때 0·임의 숫자·최신 글을 대신 보여 주지 않습니다 (인기 글 섹션 자체를 숨김).
- 경로 규칙: 쿼리·해시 제거 → 퍼센트 인코딩 해제 → `/slug/` 형태. 집계(`analytics.ts normalizePath`)와 통계 매핑(`fetch_stats.py normalize_path`)이 같은 규칙을 씁니다.

### 환경 변수 · GitHub 설정

| 이름 | 어디에 | 용도 | 비밀? | 없으면 |
|------|--------|------|-------|--------|
| `GATSBY_GA_MEASUREMENT_ID` | GitHub **Variables**(또는 Secrets) → 빌드 단계, 로컬은 `blog-front/.env.production` | GA4 측정 ID `G-XXXXXXXXXX`. 브라우저 코드에 포함됨 | 아니오 (공개 값) | GA4 스크립트 미삽입 |
| `GATSBY_GOATCOUNTER_ENDPOINT` | GitHub **Variables**(또는 Secrets) → 통계 수집·빌드 단계, 로컬은 `.env.production` | `https://<코드>.goatcounter.com/count`. 집계·공개 카운터·API 주소 계산 | 아니오 (공개 값) | 조회수 수집·표시 전부 꺼짐 |
| `GOATCOUNTER_API_TOKEN` | GitHub **Secrets** → 통계 수집 단계에서만 | GoatCounter API 토큰 (통계 읽기 권한만) | **예** — `GATSBY_` 접두사 금지, 브라우저·JSON·로그에 남기지 않음 | 공개 카운터로 대체 수집 (기간 지정 없이 전체 누적, 게시글 수만큼 요청) |
| `GOATCOUNTER_STATS_START` | GitHub Variables (선택) | 누적 집계 시작일 `YYYY-MM-DD` (기본 `2026-10-01`) | 아니오 | 기본값 사용 |
| `GOATCOUNTER_API_URL` | 로컬/Actions (선택) | API 주소 직접 지정 `https://<코드>.goatcounter.com/api/v0` | 아니오 | 엔드포인트에서 계산 |

> 실제 값은 이 문서나 코드에 적지 않습니다. 로컬 `.env*` 파일은 `blog-front/.gitignore`에 포함되어 있습니다.
> 분석 스크립트는 **운영 빌드(`gatsby build`)에서만** 삽입됩니다. `gatsby develop`에서는 수집하지 않습니다.

### 외부 서비스 초기 설정 (사용자가 직접 해야 하는 일)

1. **GA4**: [analytics.google.com](https://analytics.google.com) → 속성 만들기 → 웹 데이터 스트림(`https://logic-phantom.github.io`) → 측정 ID 복사
   - 데이터 스트림 → 향상된 측정 → 페이지 조회 → 고급 설정 → **"브라우저 기록 이벤트 기반 페이지 변경" 해제** (사이트가 이동마다 page_view를 직접 보내므로, 켜 두면 중복 집계)
2. **GoatCounter**: [goatcounter.com](https://www.goatcounter.com) 에서 사이트 생성(코드 = `<코드>.goatcounter.com`)
   - Settings → **"Allow adding visitor counts on your website"** 켜기 (상세 페이지 실시간 조회수용, 기본 꺼짐)
3. **GoatCounter API 토큰**: 사용자 메뉴 → API → 새 토큰, **통계 읽기(read statistics) 권한만** 선택
4. **GitHub 저장소(TechLog) → Settings → Secrets and variables → Actions**
   - Variables: `GATSBY_GA_MEASUREMENT_ID`, `GATSBY_GOATCOUNTER_ENDPOINT` (선택: `GOATCOUNTER_STATS_START`)
   - Secrets: `GOATCOUNTER_API_TOKEN`
5. **Google Search Console**: [search.google.com/search-console](https://search.google.com/search-console) → URL 접두어 `https://logic-phantom.github.io/` 추가 → 소유권 확인 (HTML 파일 방식이면 받은 파일을 `blog-front/static/`에 넣어 배포, 또는 GA4 연결 방식)
6. Search Console → Sitemaps → `sitemap-index.xml` 제출
7. 변수·시크릿을 등록해도 배포는 자동으로 다시 돌지 않습니다. **Actions → Build and Deploy to io Repo → Run workflow** 로 수동 실행하거나 다음 정기 배포(매일 09:00 KST)를 기다립니다
8. 배포 후 확인: GA4 실시간 보고서, GoatCounter 대시보드, 게시글 상세의 `👁 조회수`, Actions 로그의 `[stats] 저장: ...` 줄, `/stats/` 페이지

### 생성되는 공개 파일

| 경로 | 내용 |
|------|------|
| `/sitemap-index.xml` → `/sitemap-0.xml` | 게시글·공개 페이지 (`/info/`·404 제외, 게시일을 수정일로 쓰지 않도록 `lastmod` 없음) |
| `/robots.txt` | 전체 허용 + 사이트맵 위치 (`blog-front/static/robots.txt`) |
| `/rss.xml` | 최신 50편: 제목·URL·summary·게시일·카테고리·썸네일(enclosure) |
| `/stats/` | 전체 조회수·갱신 시각·집계 기간·TOP 5·게시글별 누적 조회수 (데이터 없으면 미설정 안내) |
| `/data/popular-posts.json` | 빌드 때 생성된 경우에만. `generatedAt`·`metric`·기간·`totalViews`·`posts[{path, views}]` |

게시글 프론트매터 선택 필드: `tags: ['a', 'b']`(관련 글 추천 보조), `updatedAt: 'YYYY-MM-DD'`(실제로 내용을 고쳤을 때만 → 구조화 데이터 `dateModified`). 기존 글에 없어도 빌드됩니다.

### 장애 대응

| 증상 | 확인할 것 |
|------|-----------|
| 조회수·인기 글이 안 보임 | ① Actions 로그 `Fetch view stats` 단계의 `[stats]` 메시지 ② 변수·시크릿 이름 ③ GoatCounter에 아직 데이터가 없으면 정상(숨김) ④ 상세 페이지 카운터는 GoatCounter 설정의 visitor counts 허용 여부, 응답은 최대 4시간 캐시 |
| `[stats] API 통계 수집 실패: 인증 실패 HTTP 401/403` | 토큰 값 오타·만료, 통계 읽기 권한 누락. 공개 카운터로 대체 수집되므로 배포·통계는 계속됨 |
| `[stats] ... 미설정` | `GATSBY_GOATCOUNTER_ENDPOINT` 미등록이면 통계 없음, `GOATCOUNTER_API_TOKEN`만 없으면 공개 카운터 사용 (의도한 상태면 무시) |
| `[stats] API 통계 수집 실패: /stats/total HTTP 404` | 방문 기록 유무와 무관 (기록이 없어도 API는 `total: 0`을 돌려줌). GoatCounter는 토큰 인증 뒤 서버 DB 조회가 빈 결과일 때 404를 줌. 바로 다음 `[stats] 진단:` 줄 확인 — `/me 도 404`면 GoatCounter에서 토큰을 새로 발급해 `GOATCOUNTER_API_TOKEN` 교체. 그동안은 공개 카운터로 대체 수집됨 |
| `[stats] 통계 수집 실패: 공개 카운터 사용 불가` | GoatCounter Settings → "Allow adding visitor counts" 꺼짐. 이때만 통계 없이 빌드 |
| 배포는 성공했는데 사이트가 예전 화면 | `gatsby-plugin-offline` 서비스 워커 캐시. 시크릿 창으로 확인하거나 개발자 도구 → Application → Storage → **Clear site data**. 기존 방문자는 탭을 모두 닫은 뒤 다음 방문부터 새 버전이 보임 |
| GA4에 데이터가 없음 | 측정 ID 형식(`G-`), 빌드 로그의 `[analytics] ... 끕니다` 경고, 광고 차단기, 실시간 보고서는 수 분·일반 보고서는 24~48시간 지연 |
| GA4 페이지뷰가 2배 | 위 1번의 "브라우저 기록 이벤트 기반 페이지 변경" 해제 여부 |
| 검색에 안 나옴 | Search Console 소유권·사이트맵 제출 여부, URL 검사로 색인 요청. 신규 사이트는 수일~수주 소요 |
| RSS가 없음 | `blog-front/public/rss.xml` 생성 여부(로컬 `npm run build`), `gatsby-plugin-feed` 설치 여부(`npm install`) |
| 배포 빌드 실패 | 통계 단계는 `continue-on-error`라 원인이 아님. `Build the project` 로그에서 GraphQL·이미지 경로 오류 확인, 로컬 `npm run build` 재현 |

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
| JavaScript | ES5/ES6 핵심, 비동기·클로저, 에러 처리, 내장/외부 유틸 라이브러리, JS vs TS, window 객체, 국제화(i18n)와 Intl API |
| 프레임워크 | React 구조, Next.js, Gatsby, Svelte, htmx, Flutter, 마이크로 프론트엔드, SPA vs MPA, Virtual DOM, Signals 기반 반응성, 아일랜드 아키텍처 & Astro |
| 브라우저·표준 | HTML 렌더링 과정, 웹 표준, 웹 접근성, Web Worker, WebAssembly, WebGPU, 자동재생 정책, 3D 인터랙티브 웹, View Transitions API, CSS Container Queries & :has(), Web Components / Shadow DOM, WebCodecs 영상/음성 저수준 제어, CSS Anchor Positioning, Navigation API와 차세대 SPA 라우팅, Web Bluetooth API, Web Audio API, Popover API와 Top Layer, CSS Scroll-driven Animations와 60fps 선언적 스크롤, Web Bluetooth & Web HID API, Compute Pressure API와 적응형 워크로드 최적화, Credential Management API, Web Share Target API와 네이티브 공유 연동, Async Clipboard API와 시스템 클립보드 보안 제어, Compression Streams API와 네이티브 데이터 압축, File System Access API와 사용자 로컬 파일 직접 I/O, Background Fetch API와 대용량 파일 백그라운드 I/O, CSS Custom Highlight API와 Highlight Registry, Page Lifecycle API와 브라우저 생명주기 관리 |
| 네트워크 | HTTP/1~3, 상태 코드, WebSocket·STOMP, FCM 푸시, WebTransport & HTTP/3 스트리밍, WebRTC 실시간 미디어 |
| 성능 | Web Vitals, 모바일 비디오 최적화, ISR·엣지 캐싱, 캐시 vs 세션, Service Worker 캐싱 전략 심화, 프론트엔드 관측성(RUM & OpenTelemetry), Speculation Rules API와 브라우저 사전 렌더링, Prioritized Task Scheduling API와 메인 스레드 스케줄링 |
| 서버 | Spring / Spring Boot, JVM, VO·DTO, 모놀리스, 백엔드 API 비교, Supabase, Web vs WAS |
| 인프라 | Jamstack, Vercel, 배포 아키텍처, 클라우드, PWA, WebView vs PWA, Feature Flag & 점진 배포 |
| AI | LLM 개요, Web LLM, 브라우저 Transformer, MCP, 에이전틱 웹, AI 코딩 도구, AI 거버넌스, 바이브 코딩, YOLOv5, agno |
| 보안 | 웹 보안 정책, 웹 취약점 대응, 패스키·WebAuthn, FedCM API와 개인정보 보호 기반 통합 인증 |
| 데이터·협업 | 로컬 퍼스트 & CRDT |
| 데이터·브라우저 | Origin Private File System, SQLite in the Browser (WASM), Broadcast Channel API와 Multi-Tab Communication, Web Locks API와 다중 탭 동시성 제어 |

**아직 비어 있는 후보** (바로 골라 쓸 수 있는 목록)



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
| 썸네일 | **1536 × 1024** (3:2) | 테마별 파스텔/다크 플랫 일러스트 | `images/<주제>/<이름>.png` |
| 본문 다이어그램 | **1280 × 600~700** | 흰색, 설명용 도식 | 동일 폴더 |

주제 폴더: `web` · `AI` · `javascript` · `html` · `http` · `css` · `next` · `pwa` · `server` · `mcp` · `mob` · `vercel` · `vibe` · `gatsby` · `markup` · `error` · `spa-mpa` · `etc`

**다이어그램 팔레트** (본문 도식은 이 톤으로 통일)

```text
배경 #D6E8FB   네이비 #1E3A5F   블루 #5B8FD4   연블루 #A8C9EF
페일 #C6DEF8   그린 #279866    레드 #CE4747   그레이 #788A9E   페이퍼 #F9FBFE
```

**썸네일은 글마다 달라 보이도록** 레이아웃 × 테마 × 아이콘을 조합합니다. 텍스트 재료는 항상 같습니다: **영문 대문자 키워드 1~2줄** + **영문 배지(부제)** + **한글 카피 한 줄** + **주제 아이콘 1개**.

| 레이아웃 | 구성 |
|----------|------|
| `classic` | 가운데 흰 패널에 키워드 + 좌우 아이콘과 점선 화살표 + 하단 카피 (기존 스타일) |
| `split` | 왼쪽 큰 타이포(배지 → 키워드 → 강조선 → 카피) + 오른쪽 원형 일러스트 |
| `editor` | 다크 코드 에디터 창 안에 `// 배지`, 키워드, `$ 카피` + 모서리 아이콘 |
| `poster` | 대각선 띠 + 거대한 키워드 + 하단 캡션 바 |
| `emblem` | 가운데 원형 엠블럼 아이콘 + 아래 키워드·배지·카피 |

- 테마: `sky` · `night` · `mint` · `peach` · `lavender` · `ocean`
- 아이콘: `devices` · `browser` · `phone` · `code` · `server` · `database` · `cloud` · `shield` · `chip` · `network` · `gear` · `chat` · `bolt` · `chart` · `globe` · `layers`
- 자동 발행은 **기존 글 수로 레이아웃·테마를 순환**(5 × 6, 서로소라 30편 동안 조합이 반복되지 않음)시키고, 아이콘은 Gemini가 주제에 맞게 고릅니다.

### 7. 이미지 생성 방법

**macOS / Linux / CI (권장)**: Python + Pillow 로 그립니다. 팔레트·썸네일 레이아웃 헬퍼가 `scripts/draw_kit.py`에 있습니다.

```bash
python3 -m venv .venv && .venv/bin/pip install pillow   # 최초 1회 (.venv는 커밋하지 않음)
```

```python
import sys; sys.path.insert(0, 'scripts')
from draw_kit import *

thumbnail('blog-front/contents/images/web/passkey.png',   # 썸네일 (레이아웃·테마·아이콘 지정)
          ['PASS', 'KEYS'], 'WEBAUTHN', '비밀번호 없는 로그인', 'shield', 'split', 'mint')
layout, theme = pick_style(42)                             # 또는 숫자로 순환 선택

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
- [ ] `python3 scripts/validate_post.py blog-front/contents/<슬러그>.md` 오류 0건

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

- 성장 기반: sitemap·robots·OG·canonical·구조화 데이터, GA4, GoatCounter 조회수·인기 글·`/stats/`, 공유·관련 글, RSS, 자동 발행 품질 검증 (2026.10)
- 자동 발행 안정화: Gemini 503·연결 끊김·잘린 응답 재시도, 하루 3회 스케줄로 실패 시 당일 재시도 (2026.10)
- 썸네일 다양화: 레이아웃 5종 × 테마 6종 × 아이콘 16종 조합, 글마다 자동 순환 (2026.09)
- **매일 12:00(KST) 자동 게시글 발행** — Gemini 무료 API + GitHub Actions (2026.09)
- 썸네일·다이어그램 생성 도구를 Python(Pillow)으로 이식, 글자 자동 맞춤·줄바꿈 지원 (2026.09)
- README에 AI 에이전트용 게시글 작성 가이드 정리 (2026.09)
- PWA 기능 추가 (2024.03)
- 댓글 시스템 Utterances 적용
- 이미지 최적화 개선
- SEO 최적화

---

## 📬 Contact

- GitHub: [@Logic-Phantom](https://github.com/Logic-Phantom)
- Blog: [https://logic-phantom.github.io](https://logic-phantom.github.io)

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.
