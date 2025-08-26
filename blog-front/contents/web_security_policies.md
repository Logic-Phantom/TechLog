---
date: '2025-08-26'
title: '🌐 웹 보안 정책 심층 가이드 '
categories: ['Web','Polices']
summary: '알쓸웹보(알면 쓸만한 웹 보안정책)'
thumbnail: './images/web/Polices.png'
comments: true
---

# 🌐 웹 보안 정책 심층 가이드  
CSRF, XSS, SSRF, CORS, CSP 완전 정복

웹 애플리케이션은 점점 더 복잡해지고 있으며, 그만큼 보안 위협도 교묘해지고 있습니다.  
이번 글에서는 **웹 보안 정책에서 반드시 알아야 할 핵심 개념**인 CSRF, XSS, SSRF, CORS, CSP를  
기본 원리부터 실무 적용, 그리고 전문가 레벨의 심화 내용까지 단계적으로 정리합니다.  

---

## 1️⃣ CSRF (Cross-Site Request Forgery)

### 🧩 기본 개념
- **정의**: 사용자가 의도하지 않은 요청을 특정 웹 애플리케이션에 강제로 보내는 공격 기법.
- **비유**: 은행 사이트에 로그인한 사용자가 공격자가 심어둔 링크를 클릭 → 모르는 사이에 송금 요청 발생.

### ⚙️ 동작 원리
1. 사용자가 신뢰할 수 있는 사이트(`bank.com`)에 로그인 → 세션 쿠키 저장됨.
2. 공격자가 악성 페이지(`evil.com`)를 열도록 유도.
3. 그 페이지가 `bank.com/transfer?to=attacker&amount=1000` 요청 자동 전송.
4. 세션 쿠키가 자동으로 첨부되어 정상적인 요청처럼 처리됨.

### 🛡️ 방어 기법
- **CSRF Token (Anti-CSRF Token)**: 요청마다 고유 난수 토큰 포함.
- **SameSite Cookie**: `Strict` 또는 `Lax` 속성으로 크로스 도메인 쿠키 전송 차단.
- **Double Submit Cookie**: 쿠키와 파라미터에 같은 토큰 전달 후 서버에서 비교.

### 🎯 전문가 관점
- OAuth, JWT 기반 시스템에서도 **state 파라미터**와 **nonce 값**으로 CSRF를 방어.
- Single Page Application(SPA)에서는 CSRF보다 XSS가 더 위협적 → CSRF 대비책을 적용해도 XSS로 토큰 유출 시 무력화 가능.

---

## 2️⃣ XSS (Cross-Site Scripting)

### 🧩 기본 개념
- **정의**: 악성 스크립트(JS 등)를 삽입하여 사용자 브라우저에서 실행시키는 공격.
- **종류**:
  - **Stored XSS**: 서버 DB에 저장 → 모든 사용자에게 전파.
  - **Reflected XSS**: URL 파라미터 등에 포함 → 즉시 반사되어 실행.
  - **DOM-based XSS**: 클라이언트 JS 코드의 불안전한 DOM 조작에서 발생.

### ⚙️ 동작 원리
```html
<input value="<script>alert('XSS')</script>">
```
→ 필터링 없이 렌더링되면 사용자 브라우저에서 실행됨.

### 🛡️ 방어 기법
- **입력 검증(Input Validation)**: 허용된 값만 처리(화이트리스트 기반).
- **출력 인코딩(Output Encoding)**: HTML, JS, URL 컨텍스트별로 적절한 인코딩 적용.
- **CSP(Content Security Policy)** 활용: 임의 스크립트 차단, 특정 도메인 스크립트만 허용.

### 🎯 전문가 관점
- XSS는 단순 알림창 공격이 아니라 **세션 탈취, 키로깅, 피싱, 크립토마이닝**까지 확장됨.
- **Trusted Types API**(최신 브라우저)로 DOM 삽입 시 정책 기반 방어 가능.
- React, Vue 같은 프레임워크도 **XSS 방어 내장**하지만 `v-html`/`dangerouslySetInnerHTML` 사용 시 여전히 취약.

---

## 3️⃣ SSRF (Server-Side Request Forgery)

### 🧩 기본 개념
- **정의**: 공격자가 서버가 대신 외부 요청을 보내도록 속이는 공격.
- **비유**: 사용자가 도서관에 "이 책 찾아줘"라고 했는데, 공격자는 "직원 전용 금고 열어봐"라고 시키는 꼴.

### ⚙️ 동작 원리
1. 애플리케이션이 URL 입력을 받아 외부 리소스를 가져옴.
2. 공격자가 내부망 주소(`http://127.0.0.1:8080/admin`)를 전달.
3. 서버가 내부 자원에 직접 접근하여 정보 유출.

### 🛡️ 방어 기법
- **Allowlist 기반 접근 제한**: 허용된 도메인만 요청.
- **내부망 접근 차단**: `localhost`, `169.254.*`, `10.*` 등 사설망 요청 필터링.
- **Proxy 사용**: 모든 요청을 프록시로 보내어 로깅 및 제어.

### 🎯 전문가 관점
- SSRF는 단순 정보 유출을 넘어서 → **클라우드 메타데이터 API 탈취(AWS EC2 IAM Role 크리덴셜 등)**로 이어짐.
- 최신 보안 가이드라인에서는 SSRF를 OWASP Top 10 (2021) 주요 취약점으로 포함.

---

## 4️⃣ CORS (Cross-Origin Resource Sharing)

### 🧩 기본 개념
- **정의**: 브라우저 보안 정책(Same-Origin Policy)을 완화해 다른 출처(origin)의 자원에 접근할 수 있게 하는 메커니즘.
- **문제 상황**: `frontend.com` → `api.com` 요청 시 기본적으로 차단됨.

### ⚙️ 동작 원리
1. 브라우저가 Preflight Request(`OPTIONS`) 전송.
2. 서버가 `Access-Control-Allow-Origin` 헤더로 허용 여부 응답.
3. 조건이 맞을 경우 실제 요청 진행.

### 🛡️ 방어 기법
- **정확한 Origin 설정**: `*` 대신 필요한 도메인만 허용.
- **인증 정보 포함 시 (`withCredentials: true`)** → `*` 불가, 반드시 명시된 도메인 사용.
- **최소 권한 정책 적용**: 불필요한 메서드(`PUT`, `DELETE`) 허용하지 않기.

### 🎯 전문가 관점
- 잘못된 CORS 설정은 **CSRF보다 더 위험** → 다른 도메인에서 API를 악용 가능.
- 일부 개발자는 편의를 위해 `Access-Control-Allow-Origin: *`로 설정 → 보안 취약점 유발.
- 내부망 API를 외부에 노출할 때 특히 주의 필요.

---

## 5️⃣ CSP (Content Security Policy)

### 🧩 기본 개념
- **정의**: 웹 애플리케이션에서 로드할 수 있는 리소스를 제어하는 보안 정책.
- **목적**: XSS, 데이터 인젝션 등 스크립트 실행을 방지.

### ⚙️ 동작 원리
- 서버가 응답 헤더에 `Content-Security-Policy` 설정:
```http
Content-Security-Policy: default-src 'self'; script-src 'self' https://apis.google.com
```
→ 오직 같은 출처와 `apis.google.com`에서만 JS 로드 가능.

### 🛡️ 방어 기법
- **기본 정책(default-src)**을 좁게 설정 후 필요한 경우만 개별 허용.
- **Nonce/Hash 기반 실행 허용**: 인라인 스크립트 차단 후 특정 해시/난수만 허용.
- **Report-Only 모드** 활용: 실제 차단 전 정책 테스트 가능.

### 🎯 전문가 관점
- CSP는 XSS 완벽 차단 수단이 아님 → 개발자의 설정 방식에 따라 우회 가능.
- 현대 브라우저에서는 CSP + Subresource Integrity(SRI) 조합으로 보안 강화.
- 대규모 서비스에서는 **CSP violation 리포트**를 로그로 수집해 공격 탐지 가능.

---

## 🚀 결론: 보안 정책은 '레이어드(다층) 접근'이 핵심

- **CSRF**: 토큰 + SameSite 쿠키  
- **XSS**: 인코딩 + CSP + 프레임워크 안전 API  
- **SSRF**: Allowlist + 내부망 차단  
- **CORS**: 최소 권한 설정  
- **CSP**: 기본 정책 + Nonce/Hash 기반 허용  

👉 단일 정책만 믿으면 안 되고, **여러 방어 기법을 조합한 Defense in Depth 전략**이 필수입니다.  
👉 또한 개발 단계에서 보안을 고려하는 **Security by Design**이 장기적으로 비용 절감과 서비스 신뢰도 확보에 기여합니다.

---

📌 **참고 자료**
- [OWASP Top 10 (2021)](https://owasp.org/Top10/)
- [MDN Web Docs - Web Security](https://developer.mozilla.org/en-US/docs/Web/Security)
- [Google Web Fundamentals - CSP](https://developers.google.com/web/fundamentals/security/csp)
