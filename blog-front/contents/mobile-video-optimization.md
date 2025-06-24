---
date: '2025-06-23'
title: '모바일 비디오 최적화 가이드'
categories: ['Mobile']
summary: '모바일 환경에서의 비디오 성능 최적화 기법'
thumbnail: './images/vercel/Mobile.png'
comments: true
---

# 📌 Mobile Video 성능 최적화: 모바일 청첩장 프로젝트 사례로 보는 실전 가이드

## 개요

모바일 청첩장을 제작하며, 모바일 기기에서 배경 영상(`.mp4`, `.webm`)이 느리게 로딩되거나 끊기는 현상이 발견되었다. 특히 3G 또는 저속 네트워크 환경에서의 경험이 현저히 나빠지는 문제가 발생했다. 이를 해결하기 위해 다양한 테스트와 성능 최적화를 시도하였고, 그 과정을 기록으로 남긴다.

---

## 1. 문제 발생 배경

### 💬 문제 현상
- **영상 로딩 지연**: 첫 진입 시 영상이 늦게 시작되거나, 정지된 채 멈춤
- **모바일 기기 이슈**: iOS Safari 또는 저사양 Android에서 끊김 발생
- **모바일 네트워크**: LTE, 5G에서는 괜찮지만, 3G/저속에서는 거의 영상 미출력

### 🔍 사용 중인 기술 스택
- Front: Next.js
- 배포: Vercel
- 영상 포맷: `wedding-bg.mp4`, `wedding-bg.webm`
- 백그라운드 방식: `<video autoplay muted loop playsinline>`

---

## 2. 원인 분석

### 원인 1. **모바일 네트워크 속도 불안정**
- 3G 기준 다운로드 속도: 평균 0.5 ~ 1.5 Mbps
- 초기 영상 로딩에만 수 MB 소요되어 UX 손실

### 원인 2. **브라우저별 autoplay 정책**
- iOS Safari는 muted 속성이 있어야 autoplay 가능
- playsinline이 없으면 전체화면 강제됨 → UX 파괴

### 원인 3. **영상 포맷 및 해상도**
- `.mp4` + `.webm` 모두 제공 중이나 1080p 해상도였음
- 모바일에 과한 해상도

---

## 3. 해결을 위한 최적화 전략

### ✅ 전략 1. **영상 인코딩 최적화**
- 해상도: 1080p → 720p 또는 480p로 낮춤
- Bitrate: 2~4Mbps → 0.8~1.2Mbps로 줄임
- GOP 설정: Keyframe 간격 최적화로 seeking 성능 향상

```bash
ffmpeg -i input.mp4 -vf scale=854:480 -b:v 1000k -bufsize 1000k -c:a aac -movflags +faststart output.mp4
```

### ✅ 전략 2. **`<video>` 태그 속성 정비**
```html
<video autoplay muted playsinline loop preload="auto">
  <source src="/videos/wedding-bg.webm" type="video/webm" />
  <source src="/videos/wedding-bg.mp4" type="video/mp4" />
</video>
```

### ✅ 전략 3. **LCP 관점에서 이미지 fallback 도입**
```html
<video ... poster="/images/video-fallback.jpg">...</video>
```

### ✅ 전략 4. **Lazy Load + IntersectionObserver 도입**
```js
const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.play();
    } else {
      entry.target.pause();
    }
  });
});
observer.observe(document.querySelector("video"));
```

### ✅ 전략 5. **CDN 최적화 및 Vercel 헤더 설정**
```json
{
  "headers": [
    {
      "source": "/videos/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    }
  ]
}
```

---

## 4. 네트워크 별 성능 테스트

| 네트워크 환경 | 영상 로딩 시간 (초) | UX 체감 |
|---------------|----------------------|----------|
| 5G            | 0.5~1.0              | 매우 쾌적 |
| LTE           | 1.5~2.5              | 쾌적     |
| 3G (시뮬레이션) | 4.5~6.0              | 로딩지연, UX 저하 |
| Wi-Fi (10Mbps) | 0.3~0.6              | 매우 쾌적 |

> ✅ 영상 fallback 적용 + 해상도 최적화 이후, 3G에서도 3초 내 진입 가능

---

## 5. 모바일 영상 퍼포먼스 체크리스트

| 항목 | 체크 |
|------|------|
| 해상도 480p/720p 제공 여부 | ✅ |
| `.webm` + `.mp4` 포맷 동시 지원 | ✅ |
| `<video>` autoplay, muted, playsinline | ✅ |
| `poster` 이미지 fallback 제공 | ✅ |
| Lazy loading 및 JS 최적화 | ✅ |
| CDN 캐싱 및 헤더 설정 | ✅ |
| 실제 저속 네트워크 환경 테스트 | ✅ |

---

## 6. 결론 및 회고

모바일 웹에서 영상은 "리스크 높은 자산"이다. 청첩장과 같은 감성 기반 UX를 위해 영상이 필수였지만, 오히려 사용자 경험을 해치는 요소가 될 수 있음을 깨달았다.

> **"퍼포먼스 최적화는 기능이 아닌 기본"**  
> 영상의 존재 자체보다, 그것을 어떻게 전달하느냐가 핵심이다.

---

## 💡 참고 자료

- [Google: Media Loading Best Practices](https://web.dev/video-optimization/)
- [Vercel Caching Guide](https://vercel.com/docs/edge-network/caching)