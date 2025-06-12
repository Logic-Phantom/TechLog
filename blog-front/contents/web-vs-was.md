---
date: '2025-06-12'
title: 'Web과 WAS의 차이점과 용도 정리'
categories: ['web']
summary: '웹 서비스의 핵심 구성 요소'
thumbnail: './images/web/webWas.png'
comments: true
---

# Web과 WAS의 차이점과 용도 정리

웹 애플리케이션을 개발하다 보면 **Web 서버**와 **WAS(Web Application Server)**라는 용어를 자주 접하게 됩니다. 처음에는 비슷하게 느껴질 수 있지만, 두 서버는 명확하게 다른 목적과 역할을 가지고 있으며, 이를 정확히 이해하는 것은 시스템 설계나 아키텍처 구성 시 매우 중요합니다.

이 글에서는 **Web과 WAS의 차이**, **각자의 역할**, 그리고 **실제 사용 사례**까지 정리해보겠습니다.

---

## 1. Web 서버란?

### 📌 정의
Web 서버는 **HTTP 프로토콜을 기반으로 정적인 콘텐츠(HTML, CSS, JS, 이미지 등)**를 클라이언트(브라우저)에 제공하는 서버입니다.

### 📦 주요 기능
- 정적 파일 제공 (HTML, CSS, JS, PNG 등)
- 클라이언트로부터 요청을 받고 응답(Http Response)을 반환
- 요청을 WAS나 리버스 프록시 서버로 전달(역할 분리 가능)

### 🌐 대표적인 Web 서버
- Apache HTTP Server
- Nginx
- Microsoft IIS

### 🧩 예시
브라우저에서 `index.html`을 요청하면 Web 서버는 해당 파일을 읽어 그대로 클라이언트에 전달합니다.

```plaintext
[Client] → HTTP Request → [Web Server] → HTML 파일 전달 → [Client]
```

---

## 2. WAS(Web Application Server)란?

### 📌 정의
WAS는 **웹 어플리케이션의 비즈니스 로직이 실행되는 서버**로, 동적인 요청을 처리합니다. 즉, Web 서버가 단순한 정적 리소스 제공이라면, WAS는 DB와 연동된 **동적 처리**를 담당합니다.

### ⚙️ 주요 기능
- 동적 컨텐츠 처리 (JSP, Servlet, Spring, Django 등)
- DB 연결 및 트랜잭션 처리
- 로그인, 게시판, 주문 등 사용자 요청에 따른 동적 응답 생성
- 세션 관리, 보안 처리, 로깅 등

### ☕ 대표적인 WAS
- Apache Tomcat
- JBoss / WildFly
- WebLogic
- Jetty

### 🧩 예시
사용자가 로그인 양식을 제출하면 WAS는 사용자 정보를 DB에서 확인 후 로그인 처리 및 응답을 생성합니다.

```plaintext
[Client] → 로그인 요청 → [Web Server] → [WAS] → DB → 로그인 처리 결과 → [Client]
```

---

## 3. Web 서버와 WAS의 차이점 정리

| 구분 | Web 서버 | WAS |
|------|----------|-----|
| 역할 | 정적 컨텐츠 처리 | 동적 로직 처리 |
| 예시 | HTML, 이미지 전송 | 로그인, 게시글 처리 등 |
| 실행 환경 | 단순 파일 전송 | 코드 실행 (Servlet, JSP, Java 등) |
| 부담 | 가볍고 빠름 | 무겁고 복잡 |
| 대표 제품 | Nginx, Apache | Tomcat, JBoss |

---

## 4. 함께 사용하는 이유: 분리의 이점

현대의 웹 시스템에서는 Web 서버와 WAS를 **역할에 따라 분리**하여 구성하는 것이 일반적입니다.

### 🎯 이유
- **성능 향상**: 정적 파일 처리는 Web 서버가 빠르게 수행
- **보안성 강화**: WAS는 외부에 노출되지 않고 Web 서버만 공개
- **부하 분산**: Web 서버가 요청을 필터링하여 필요한 요청만 WAS로 전달

### 🔧 구성 예시

```plaintext
[Client]
   ↓
[Web Server]  ← 정적 파일 처리 (HTML/CSS/JS)
   ↓
[WAS]         ← 동적 처리 (로그인, 게시판 등)
   ↓
[DB]          ← 데이터 저장/조회
```

---

## 5. 마무리: 언제 어떤 서버를 써야 할까?

| 목적 | 적합한 서버 |
|------|--------------|
| 정적인 콘텐츠만 제공 | Web 서버만으로 충분 |
| 사용자 요청에 따른 동적 처리 필요 | WAS 필요 (Spring, JSP 등) |
| 성능과 보안을 고려한 아키텍처 | Web + WAS 분리 구조 권장 |

---

## 🔚 결론

Web 서버와 WAS는 **웹 서비스의 핵심 구성 요소**입니다. 각자의 역할을 명확히 이해하고 적절히 분리함으로써, **성능**, **보안**, **확장성**을 갖춘 안정적인 시스템을 설계할 수 있습니다.

> 💡 웹 개발을 막 시작한 개발자라면 Web 서버와 WAS의 차이를 이해하는 것만으로도 프로젝트 구조와 운영 방식에 대한 안목이 생깁니다.

---

**참고 자료**
- [Nginx 공식 문서](https://nginx.org/)
- [Apache Tomcat 공식 문서](https://tomcat.apache.org/)
- [HTTP 개념 정리 - MDN](https://developer.mozilla.org/ko/docs/Web/HTTP)