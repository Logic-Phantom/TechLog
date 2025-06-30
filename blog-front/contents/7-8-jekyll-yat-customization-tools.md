---
date: '2025-06-30'
title: 'Jekyll Theme YAT 커스터마이징 경험기'
categories: ['Css']
summary: '동적 경험 못지않은 UX'
thumbnail: './images/css/Jekyll.png'
comments: true
---

# 📌 7. Jekyll Theme YAT 커스터마이징 경험기
## 📁 테마 구조 파악부터 시작

처음 `jekyll-theme-yat` 테마를 접했을 때 느낀 건 **"정갈하지만 꽤 제한적인 구조다"**였습니다.  
하지만 이를 커스터마이징하려면 우선 전체 폴더 구조를 정확히 이해할 필요가 있었죠.

```bash
.
├── _layouts/
├── _includes/
├── _sass/
├── assets/
├── _config.yml
├── index.md
```

Jekyll 테마는 기본적으로 `_layouts`, `_includes`, `_sass` 세 축을 중심으로 작동합니다.  
공통 레이아웃은 `_layouts/default.html`, 섹션별 분할은 `_includes`, 그리고 스타일은 `_sass` 아래에 정리되어 있었죠.

## 🎨 원하는 UI/UX를 위한 구조적 변경

단순 블로그라기보단 "도구 기록 아카이브"로 만들고 싶었습니다.  
그래서 다음 요소들을 중심으로 UI를 커스터마이징했죠:

- **다크모드 토글 (Pure JS / 플러그인 없이)**  
  `localStorage`를 사용하여 다크모드 상태를 저장하고, 클래스 토글로 적용했습니다.

```js
// assets/js/theme-toggle.js
const toggle = document.getElementById('darkmode-toggle');
toggle.addEventListener('click', () => {
  const html = document.documentElement;
  html.classList.toggle('dark');
  localStorage.setItem('theme', html.classList.contains('dark') ? 'dark' : 'light');
});
```

- **스크롤 이동 애니메이션**  
  CSS `scroll-behavior: smooth;`와 `<a href="#section">` anchor를 적극 활용하여 부드러운 이동감을 주었습니다.

- **코드 하이라이팅 커스터마이징**  
  기존 Rouge + markdown 기반이 너무 무거워서, `highlight.js`를 직접 CDN으로 삽입해 단순화했습니다.

```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/github-dark.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
<script>hljs.highlightAll();</script>
```

## 🔧 실전에서 마주친 문제와 해결

- Jekyll 플러그인은 GitHub Pages에서 일부 제한되기 때문에, 외부 스크립트를 커스터마이징하여 우회했습니다.
- 테마가 CSS 전처리기(SASS) 기반이므로 작은 스타일 수정도 `_sass/_variables.scss`나 `_sass/_base.scss`에서 정리하면 전체 일관성을 유지할 수 있었습니다.

---

# 📌 8. Tool 철학 & 개발방식 – npm 없는 개발, 가능한가?

## 🧠 도구 선택의 철학

npm은 확실히 강력합니다. 하지만 **과도한 추상화**와 **의존성 지옥**에 빠지는 경험을 여러 번 하면서  
"정말 필요한가?"라는 의문이 생겼습니다.

그래서 이 프로젝트는 다음 기준을 따랐습니다:

- 가능한 **바닐라 JS + HTML/CSS**
- 모듈은 CDN 기반으로 로드
- 빌드는 셸 스크립트나 GitHub Actions로 자동화

## 🔄 Webpack 없이도 빌드 파이프라인 가능?

정적 사이트라면 충분히 가능합니다. 예를 들면:

- `sass` CLI로 SCSS → CSS 변환
- `minify-html` 유틸리티로 HTML 최소화
- 커밋/PR 시 GitHub Actions에서 자동 빌드 & 배포

## ✅ GitHub Actions 자동화 설정

### 📂 `.github/workflows/deploy.yml`

```yaml
name: Deploy to GitHub Pages

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Ruby for Jekyll
        uses: ruby/setup-ruby@v1
        with:
          ruby-version: '3.1'
      - name: Install dependencies
        run: bundle install
      - name: Build site
        run: bundle exec jekyll build
      - name: Deploy
        uses: peaceiris/actions-gh-pages@v3
        with:
          github_token: ${{ secrets.GITHUB_TOKEN }}
          publish_dir: ./_site
```

## 🤯 겪었던 문제들

- `public/` 디렉토리만 별도 gh-pages에 push할 때 퍼미션 에러 → 워크플로에서 token 스코프 수정
- Windows 환경에서 `jekyll serve` 호환 이슈 → GitHub Actions 기반으로 로컬 빌드는 최소화

---

## ✨ 마치며

"Jekyll은 정적이다"라는 말은 틀렸습니다.  
구조를 이해하고 커스터마이징하면 **동적 경험 못지않은 UX**를 구현할 수 있었습니다.  
그리고 도구는 **"가볍고, 내가 통제 가능한 수준"**이 가장 좋습니다.

이 프로젝트를 통해:
- 직접 구성한 빌드 파이프라인
- 철학 중심의 도구 선택
- 플러그인 없이도 가능한 UX 개선

을 경험했고, 앞으로도 이 원칙은 유지할 예정입니다.