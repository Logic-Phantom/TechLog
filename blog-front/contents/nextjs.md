---
date: '2025-05-20'
title: 'Next.js란 무엇인가? 개요와 특징 정리'
categories: [JavaScript, Next.js, react]
summary: 'Next.. 다음은..?'
thumbnail: './images/next/next2.png'
comments: true
---
> **Next.js**는 React 기반의 프레임워크로, 서버 사이드 렌더링(SSR)과 정적 사이트 생성(SSG)을 손쉽게 지원하며, 개발자 경험을 극대화해주는 도구입니다.

## 🔍 Next.js란?

Next.js는 Vercel에서 만든 **React 프레임워크**로, 기존 React 프로젝트에서 직접 구현해야 했던 다양한 기능들을 내장하고 있어 빠르게 웹 애플리케이션을 구축할 수 있도록 도와줍니다.

- 파일 기반 라우팅 (pages 디렉토리)
- 서버 사이드 렌더링 (SSR)
- 정적 사이트 생성 (SSG)
- API 라우트 지원 (Express 없이도 API 구현 가능)
- 이미지 최적화, 코드 분할, 빠른 페이지 로딩 등

## 🚀 Next.js의 주요 기능

### 1. 파일 기반 라우팅

`pages` 폴더 안에 `.js`, `.ts`, `.jsx` 파일을 만들면 URL 라우트가 자동 생성됩니다.

예: `pages/about.js` → `/about` URL

### 2. 서버 사이드 렌더링 (SSR)

페이지를 서버에서 HTML로 렌더링하여 초기 로딩 속도가 빠르고 SEO에 유리합니다.

```js
export async function getServerSideProps() {
  return { props: { message: "Hello SSR" } };
}
```

### 3. 정적 사이트 생성 (SSG)

빌드 시점에 HTML 파일을 생성하므로 빠르고 안정적인 페이지 제공이 가능합니다.

```js
export async function getStaticProps() {
  return { props: { message: "Hello SSG" } };
}
```

### 4. API 라우트

`pages/api` 폴더에 서버 코드 작성 가능 → 별도의 백엔드 없이도 간단한 API 제공

```js
// pages/api/hello.js
export default function handler(req, res) {
  res.status(200).json({ message: "Hello API" });
}
```

## 📦 Next.js vs React vs Node.js

| 항목 | 설명 |
|------|------|
| **React** | UI를 구성하는 라이브러리 |
| **Next.js** | React 기반 웹 프레임워크 |
| **Node.js** | 자바스크립트를 브라우저 밖에서 실행할 수 있는 런타임 환경 |

Next.js는 React로 개발된 페이지를 Node.js 위에서 실행해 SSR/SSG 기능을 제공하며, 클라이언트와 서버 사이의 다리를 연결해주는 역할도 합니다.

## 🛠️ 개발 및 배포

- 개발 서버 실행: `npm run dev`
- 정적 빌드: `npm run build`
- 배포: Vercel, Netlify, 또는 직접 서버에 배포 가능

## ✅ 마무리

Next.js는 빠르고 최적화된 웹사이트를 쉽게 만들 수 있게 해주는 도구입니다.  
React를 사용하고 있다면, Next.js를 도입해보는 것도 매우 좋은 선택입니다.

---

> 참고: [공식 문서 바로가기](https://nextjs.org/docs)
