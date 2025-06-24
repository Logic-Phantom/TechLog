---
date: '2025-06-24'
title: 'Next.js + Vercel에서 ISR 업데이트 지연 문제 해결기'
categories: ['Next.js', 'Vercel']
summary: 'ISR의 캐싱 구조와 업데이트 반영 딜레이 문제, 그리고 Edge 함수와 캐싱 전략으로 개선한 과정'
thumbnail: './images/vercel/Next2.png'
comments: true
---

# 📌 Next.js + Vercel에서 ISR 업데이트 지연 문제 해결기

최근에 **모바일 청첩장**을 Vercel에 배포하는 프로젝트를 진행했습니다. 디자인이 자주 바뀌고, 업데이트된 내용이 즉시 반영되어야 하는 환경에서 **ISR(Incremental Static Regeneration)**를 선택했는데, 예상 외의 문제가 있었습니다.  

## ⚙️ 프로젝트 구성

- **프레임워크**: Next.js 14
- **배포 플랫폼**: Vercel
- **렌더링 전략**: `getStaticProps + revalidate`
- **주요 페이지**: `/invitation/[id]`, `/event/[slug]` 등 동적 경로 다수
- **요구사항**: 페이지 데이터 업데이트 시, 최소한 수 분 이내로 반영 필요

## ❗️문제 상황: ISR 반영 지연

초기에는 `getStaticProps`에 `revalidate: 60`을 설정해, 최대 1분 주기로 콘텐츠를 갱신하도록 했습니다.

```ts
export const getStaticProps = async () => {
  const data = await fetchData();
  return {
    props: { data },
    revalidate: 60,
  };
};
```

그런데 문제는 **배포 직후, 또는 데이터가 변경된 직후에도 반영이 수 분 이상 지연**된다는 것이었습니다. 특히 모바일에서 캐시된 페이지가 유지되어 **이전 정보가 계속 노출되는 현상**이 발생했습니다.

## 🔍 원인 분석

1. **ISR은 백그라운드에서 regenerate** 하므로 첫 번째 사용자는 여전히 구버전을 볼 수 있음
2. **Vercel CDN 캐시**가 Edge에서 유지되며, 실제 regenerate된 버전이 반영되지 않음
3. 특히 **동적 경로**에서는 캐시 무효화 타이밍이 예측하기 어려움

## 💡 해결 방안: Edge Middleware + Cache-Control

### ✅ 방법 1. `Cache-Control` 직접 제어

```ts
export const getServerSideProps = async ({ res }) => {
  res.setHeader(
    'Cache-Control',
    'public, max-age=0, s-maxage=60, stale-while-revalidate=30'
  );
  const data = await fetchData();
  return { props: { data } };
};
```

문제는 **ISR이 아닌 SSR**을 사용하는 방식이 되어, **정적 페이지의 장점을 잃는다는 점**이었습니다.

---

### ✅ 방법 2. Edge Middleware에서 캐시 우회

```ts
// middleware.ts
import { NextResponse } from 'next/server';

export function middleware(req) {
  const res = NextResponse.next();

  // 특정 경로에 대해 캐시 무효화 헤더 적용
  if (req.nextUrl.pathname.startsWith('/invitation')) {
    res.headers.set('Cache-Control', 'no-cache, no-store');
  }

  return res;
}
```

이를 통해 **CDN의 캐시를 강제로 무효화하거나, 경로 단위로 더 정밀하게 캐시 정책을 설정**할 수 있었습니다.

---

## ⚖️ 적용 후 변화와 느낀 점

| 항목 | 개선 전 | 개선 후 |
|------|----------|----------|
| 데이터 변경 반영 속도 | 최대 수 분 | 수 초 ~ 1분 이내 |
| 모바일 캐시 문제 | 자주 발생 | 거의 없음 |
| 초기 페이지 로딩 속도 | 빠름 | 약간 느림 (SSR fallback 시) |

### 👍 장점

- 캐시 정책을 **세분화하여 예측 가능한 상태로 제어** 가능
- Edge Function을 이용하면 **사용자 위치 기반 대응이나 조건부 캐싱**도 가능

### 👎 단점

- 구성 복잡도 상승
- ISR의 정적 퍼포먼스를 부분 포기하는 구조
- Edge 함수 호출은 **요금제와 호출 수**에 민감

---

## 🧩 결론

> Next.js의 ISR은 분명 강력하지만, **즉시성 또는 실시간 반영이 중요한 서비스**에는 단독으로 쓰기엔 부족한 점이 있습니다.

실시간 반영이 필요한 경우엔 `ISR + Edge Function`, 또는 `SSR + 캐시 정책 조절`이 현실적인 선택이었습니다.

> **정적 빌드의 퍼포먼스를 원하면서도, 실시간성도 잡고 싶다면 "캐시 전략"이 핵심**입니다.

---

## 📎 참고 자료

- [Next.js ISR 공식 문서](https://nextjs.org/docs/pages/building-your-application/data-fetching/incremental-static-regeneration)
- [Vercel Edge Middleware 문서](https://vercel.com/docs/middleware)