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
- 이미지 최적화 자동화
- SEO 메타데이터 자동 생성

---

## 📝 블로그 포스트 작성

마크다운 파일의 기본 구조:
```markdown
---
date: 'YYYY-MM-DD'
title: '포스트 제목'
categories: ['카테고리1', '카테고리2']
summary: '포스트 요약'
thumbnail: './images/thumbnail.png'
comments: true
---

포스트 내용...
```

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
