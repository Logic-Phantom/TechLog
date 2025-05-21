---
date: '2025-05-21'
title: 'Vercel: 현대적인 프론트엔드 개발을 위한 클라우드 플랫폼'
categories: ['Vercel', 'CI/CD']
summary: '배포의 현대화 ... 편의성'
thumbnail: './images/vercel/vercel.png'
comments: true
---

# Vercel : 현대적인 프론트엔드 개발을 위한 클라우드 플랫폼

> “Git push로 글로벌 인프라를 가진 배포를 마친다.” — 이 말이 가능한 시대를 만든 것이 바로 Vercel이다.

---

## 🧭 Vercel이란?

**Vercel**은 정적/동적 웹 애플리케이션의 **자동화된 빌드 및 배포 파이프라인을 제공하는 프론트엔드 중심의 클라우드 플랫폼**입니다. 특히 **Next.js의 공식 개발사**이기도 하며, 프론트엔드 생태계와 완벽한 궁합을 자랑합니다.

---

## 🏗️ Vercel 아키텍처 개요

Vercel의 구조는 크게 3단계로 나눌 수 있습니다:

```
[ Git 연동 ] → [ 빌드 및 배포 (Build & Deploy Infra) ] → [ 글로벌 엣지 네트워크 ]
```

### 1. Git 기반 배포 트리거
GitHub, GitLab, Bitbucket에 연결하여, push/pull request 시 자동으로 배포가 트리거됩니다.

### 2. Build & Deploy Infra
Vercel의 인프라가 자동으로 프로젝트를 감지하고 적절한 빌드 명령어를 실행합니다 (예: `next build`, `npm run build`).

- **Serverless Function 빌드**
- **Edge Middleware 컴파일**
- **ISR(Incremental Static Regeneration)** 지원

### 3. 글로벌 엣지 네트워크
배포된 결과는 Vercel의 Edge CDN을 통해 전 세계로 퍼집니다. Cloudflare Workers와 유사한 방식으로 동작하는 **Edge Function**도 함께 배포됩니다.

---

## ⚙️ 배포 프로세스 (CI/CD Pipeline)

1. **Git Push**
2. Vercel이 자동으로 변경 사항을 감지
3. 프로젝트 빌드 시작
4. 각 빌드 아티팩트 및 함수가 서버리스 환경에 배포
5. Edge Network를 통해 글로벌 배포 완료
6. `Preview URL` 자동 생성 → 팀 피드백 가능

---

## 🧪 Preview Deployment

PR(Pull Request)을 생성하면 Vercel은 해당 브랜치만의 **미리보기 배포 URL**을 자동 생성합니다.

- 피그마처럼 실시간 피드백 가능
- 디자이너, QA, 기획자 누구나 접근 가능
- “마치 staging 환경이 무한한 느낌”

---

## 🧬 고급 기능

### ▪ Serverless Functions
- `/api/hello.js` → 자동으로 클라우드 함수로 배포
- Node.js, Go, Python 등 지원

### ▪ Edge Functions
- 사용자의 위치에 따라 더 빠른 응답
- 쿠키, 헤더에 기반한 서버사이드 로직 처리

### ▪ ISR (Incremental Static Regeneration)
- SSG와 SSR의 장점만 가져온 Vercel 특화 기능
- 빌드 이후에도 실시간 페이지 갱신 가능

---

## 🛠️ 사용 예시

| 프로젝트 | 활용 방식 |
|----------|----------|
| Next.js 블로그 | 정적 사이트 배포 + ISR |
| 포트폴리오 사이트 | Serverless + Edge CDN |
| e-Commerce | Preview URL + Edge Function 활용 |

---

## 👍 장점 요약

- 깃 커밋만으로 글로벌 배포
- Next.js 최적화 (기본 빌드 시스템)
- 무제한 Preview 환경
- Team collaboration 극대화
- 무료 요금제로도 충분한 기능 제공

---

## 👎 단점 요약

- 복잡한 백엔드 구현은 어려움
- 빌드 시간 및 요청 제한 (Free Tier)
- 데이터베이스 직접 호스팅 불가

---

## 🧭 언제 쓰면 좋은가?

✅ 빠르게 배포 가능한 SaaS, 스타트업
✅ 디자이너와 협업이 많은 프론트엔드 중심 프로젝트
✅ 글로벌 사용자 대상의 정적/동적 웹사이트

---

## 🔗 참고 링크

- [Vercel 공식 웹사이트](https://vercel.com)
- [Vercel Docs](https://vercel.com/docs)
- [Next.js 공식 문서](https://nextjs.org/docs)

---

_작성자: [Forest_LIM]_
