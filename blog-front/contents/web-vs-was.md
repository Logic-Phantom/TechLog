---
date: '2025-06-12'
title: 'Web vs WebAssembly: 언제 무엇을 사용할까?'
categories: ['Web']
summary: '웹 기술과 WebAssembly의 비교 및 적절한 사용 시나리오'
thumbnail: './images/web/webWas.png'
comments: true
---

# Web과 WAS의 차이점과 용도

## 1. Web Server란?
Web 서버는 클라이언트(브라우저)로부터 요청을 받아 HTML, CSS, JS, 이미지 등의 **정적 리소스**를 전달해주는 서버입니다.

### 대표적인 Web 서버
- Apache HTTP Server
- Nginx
- IIS

### 주요 기능
- 정적 리소스 제공 (HTML, 이미지, JS, CSS 등)
- 요청 라우팅
- 로드 밸런싱 (WAS 앞단에서)
- SSL 처리

---

## 2. WAS란?
WAS(Web Application Server)는 클라이언트의 요청을 처리하기 위해 동적인 로직을 수행하고 DB와 연동하는 **애플리케이션 실행 환경**입니다.

### 대표적인 WAS
- Apache Tomcat (Java 서블릿 기반)
- JBoss / WildFly
- WebLogic
- WebSphere

### 주요 기능
- 동적 웹 콘텐츠 처리 (JSP, Servlet 등)
- 비즈니스 로직 수행
- 데이터베이스 연동
- 세션 관리, 트랜잭션 처리

---

## 3. Web Server와 WAS의 차이

| 구분 | Web Server | WAS |
|------|------------|-----|
| 주 역할 | 정적 리소스 제공 | 동적 로직 처리 |
| 처리 방식 | 요청된 파일을 그대로 응답 | 요청을 로직에 따라 가공 후 응답 |
| 예시 | HTML, CSS, JS, 이미지 | JSP, Servlet, Spring, 데이터 조회 |
| 리소스 사용 | 적음 | 많음 |
| 확장성 | Nginx는 뛰어남 | WAS는 부하가 큼 |
| 구조 | 클라이언트 ←→ Web | 클라이언트 ←→ Web ←→ WAS |

---

## 4. 실제 배포 환경의 구성도

```
[Client (Browser)]
        ↓
   [Web Server (Nginx)]
        ↓
  [WAS (Tomcat, Spring)]
        ↓
     [Database]
```

---

## 5. 톰캣은 Web 서버인가 WAS인가?

- Tomcat은 기본적으로 WAS (서블릿 컨테이너)
- 하지만 HTML/CSS 같은 정적 파일도 서빙할 수 있어서 Web 서버 역할도 가능
- 즉, **개발/테스트용으로는 Tomcat 하나로 Web + WAS 겸용 가능**

---

## 6. 로컬 개발 환경과 운영 환경의 차이

| 환경 | Web 서버 | WAS | 분리 여부 |
|------|----------|-----|----------|
| 로컬 (톰캣만 사용) | 톰캣 내장 기능 | 톰캣 서블릿 컨테이너 | ❌ 통합 |
| 운영 | Nginx, Apache | Tomcat, JBoss 등 | ✅ 분리 |

---

## 7. 클라이언트 → WAS 직접 요청 구조의 이해

현대 웹 애플리케이션에서는 다음과 같은 흐름이 일반적입니다:

```
[클라이언트 브라우저]
     ↓
[Web 서버] ← 정적 파일(HTML, JS, CSS 등)
     ↓
[클라이언트 브라우저에서 실행된 JS 코드]
     ↓
[WAS] ← REST API 요청 (동적 데이터)
```

즉 Web 서버는 정적 파일만 제공하고, 클라이언트는 JS로 WAS의 API를 직접 호출합니다.

### 대표 사례
- React, Vue, Angular 등 SPA 앱
- 정적 자산은 Nginx에서 제공
- API는 WAS(Spring, Node 등)에서 제공

---

## 8. 서버 사이드 렌더링 예외

SSR(서버사이드 렌더링) 구조에서는 다음 흐름도 가능합니다:

```
[브라우저]
   ↓ 요청
[WAS에서 HTML 생성 (JSP, Thymeleaf 등)]
   ↓ 응답
[브라우저]
```

- Next.js, Nuxt.js, JSP 기반 프로젝트에서 많이 사용
- 이 경우 Web 서버는 WAS와 프록시 연결만 하고, HTML은 WAS에서 생성

---

## ✅ 결론 요약

- Web 서버: 정적 파일 제공 (HTML, JS, CSS)
- WAS: 동적 로직, DB처리, JSON 등 API 응답
- 로컬에선 통합, 운영에선 분리
- 대부분의 SPA 구조에선 클라이언트 → WAS 구조가 자연스럽다