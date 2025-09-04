---
date: '2025-09-04'
title: '🌐 개발자가 알면 좋은 웹 상식 모음집'
categories: ['Web','ETC']
summary: '알면 쓸만한 것들에 대하여'
thumbnail: './images/web/etcDef.png'
comments: true
---
# 🌐 개발자가 알면 좋은 웹 상식 모음집

웹 개발을 하다 보면 교과서에는 잘 나오지 않지만 **알고 있으면 유용한 상식(짜투리 지식)**들이 많습니다.  
이 글에서는 초보자부터 전문가까지 도움이 될 수 있는 **웹 개발 상식**을 정리했습니다.

---

## 1. 기본적인 웹 상식

### 1.1 HTTP와 HTTPS
- **HTTP (HyperText Transfer Protocol)**: 웹에서 데이터를 주고받는 기본 프로토콜.
- **HTTPS**: 보안이 강화된 HTTP. SSL/TLS 암호화를 통해 안전한 통신 보장.
- **알아두면 좋은 점**: HTTPS는 단순히 보안뿐 아니라, SEO(검색 엔진 최적화)에도 유리하다.

### 1.2 URL 구조
```
https://example.com:443/path/page?query=value#fragment
```
- `https` → 프로토콜
- `example.com` → 도메인
- `443` → 포트
- `/path/page` → 경로
- `?query=value` → 쿼리스트링
- `#fragment` → 페이지 내 특정 위치

### 1.3 브라우저 캐시
- 정적 자원(CSS, JS, 이미지)은 브라우저에 캐시된다.
- 캐시 전략:
  - **Cache-Control**: 캐시 유효 기간 지정
  - **ETag**: 파일 버전 비교
- **Tip**: 리소스가 업데이트되면 파일명에 해시값을 붙여 캐시 무효화 처리.

---

## 2. 중급 개발자가 알면 좋은 상식

### 2.1 쿠키, 세션, 로컬스토리지
- **쿠키**: 서버와 클라이언트 간에 전달되는 작은 데이터 조각.
- **세션**: 서버에서 관리하는 사용자 상태.
- **로컬스토리지 / 세션스토리지**: 브라우저에 영구적(또는 일시적)으로 저장되는 데이터.
- **Tip**: 민감한 정보는 절대 로컬스토리지에 저장하지 말고, 반드시 보안 검토할 것.

### 2.2 CORS (Cross-Origin Resource Sharing)
- 다른 도메인 간 요청을 허용할지 설정하는 정책.
- 기본적으로 브라우저는 보안을 위해 차단한다.
- 서버에서 `Access-Control-Allow-Origin` 헤더를 설정해야 한다.
- **심화 포인트**: 단순 요청(Simple Request)과 Preflight 요청(OPTIONS)을 구분할 것.

### 2.3 DOM과 Virtual DOM
- **DOM(Document Object Model)**: 브라우저가 HTML을 구조화한 객체.
- **Virtual DOM**: React, Vue 등에서 사용하는 가상 DOM. 변경 사항만 효율적으로 반영.
- **Tip**: Virtual DOM이 무조건 빠른 건 아니며, 적절한 상황에서만 성능 최적화에 도움 된다.

---

## 3. 전문가 수준의 심화 상식

### 3.1 브라우저 렌더링 과정
1. HTML 파싱 → DOM 트리 생성
2. CSS 파싱 → CSSOM 트리 생성
3. DOM + CSSOM → Render Tree 생성
4. Layout(배치), Paint(그리기), Composite(합성)

- **Tip**: Reflow(Layout)는 성능에 큰 영향을 미치므로, CSS 애니메이션은 `transform`, `opacity`를 활용하면 좋다.

### 3.2 HTTP/2와 HTTP/3
- **HTTP/2**
  - 멀티플렉싱 지원 → 한 연결에서 여러 요청 동시 처리
  - 서버 푸시(Server Push)
- **HTTP/3**
  - QUIC 프로토콜 기반
  - TCP가 아닌 UDP를 활용 → 속도와 안정성 개선
- **실무 팁**: 최신 브라우저 환경에서는 HTTP/3 지원 여부를 확인하고 적용하면 성능 향상에 도움 된다.

### 3.3 보안 상식
- **XSS (Cross-Site Scripting)**: 입력값 검증 및 이스케이프 처리 필요
- **CSRF (Cross-Site Request Forgery)**: CSRF 토큰 사용
- **CSP (Content Security Policy)**: 외부 스크립트/리소스 로딩 제어
- **HTTPS 적용**: 기본 중의 기본

---

## 4. 실전에서 유용한 웹 상식

### 4.1 SEO와 퍼포먼스
- **SEO 최적화**
  - `<title>`, `<meta>` 태그 잘 설정
  - 사이트맵 제출
- **퍼포먼스 최적화**
  - 이미지 최적화(WebP 등 사용)
  - 코드 스플리팅 및 Lazy Loading
  - Lighthouse 도구로 측정 및 개선

### 4.2 네트워크 최적화
- CDN(Content Delivery Network) 활용
- 정적 자원 압축(Gzip, Brotli)
- 캐시 정책 수립

### 4.3 배포와 운영 상식
- 블루/그린 배포, 롤링 업데이트 전략 이해
- 모니터링 툴 (예: Sentry, Datadog, Grafana) 사용
- 로그 수집 및 에러 추적 자동화

---

## 5. 결론

웹 개발은 단순히 코드 작성이 아니라,  
**브라우저, 네트워크, 보안, 운영까지** 아우르는 폭넓은 이해가 필요합니다.  

작은 상식 하나가 프로젝트 성능이나 보안 안정성을 크게 바꿀 수 있습니다.  
꾸준히 이런 **짜투리 지식**을 쌓아두면 분명히 큰 차이를 만들어낼 것입니다.

---
