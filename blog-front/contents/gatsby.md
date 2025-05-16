---
date: '2024-11-14'
title: 'Gatsby로 정적 사이트 만들기'
categories: ['Gatsby', 'React', 'JAMStack']
summary: 'Gatsby와 JAMStack 아키텍처의 이해와 활용'
thumbnail: './images/gatsby/gatsby4.png'
comments: true
---

## 들어가며
개인 기술 블로그를 만들기 위해 여러 도구를 검토하던 중, Gatsby를 선택하게 되었습니다. 이 글에서는 Gatsby의 특징과 장점, 그리고 JAMStack 아키텍처에 대해 자세히 알아보겠습니다.

## Gatsby 소개
Gatsby는 JAMStack을 기반으로 한 강력한 정적 사이트 생성기(Static Site Generator)입니다. GraphQL을 통해 데이터를 관리하고, 빌드 시점에 정적 페이지를 생성하는 특징을 가지고 있습니다.

주요 특징:
- GraphQL 기반 데이터 관리
- 플러그인 시스템을 통한 확장성
- React 컴포넌트 기반 개발
- 빠른 페이지 로딩 속도

## JAMStack 아키텍처
JAMStack은 JavaScript, API, Markup의 조합을 의미하며, 현대적인 웹 개발 아키텍처입니다.

### 전통적 웹사이트와의 차이점
![JAMStack vs 전통적 웹사이트](./images/gatsby/gatsby1.png)

#### 전통적 웹사이트
- 서버와 데이터베이스 의존
- 복잡한 아키텍처
- 느린 로딩 속도

#### JAMStack
- 정적 파일 기반
- CDN 활용
- 단순한 구조

### JAMStack의 장점
1. **빠른 성능**
   - Pre-rendered 페이지
   - CDN 통한 빠른 전송
   - 초기 로딩 시간 단축

2. **향상된 보안**
   - 공격 표면 감소
   - API 추상화
   - 서버리스 아키텍처

3. **쉬운 확장성**
   - CDN 기반 확장
   - 글로벌 배포 용이
   - 효율적인 리소스 관리

## Gatsby vs Next.js

### 사용 목적의 차이
1. **Next.js**
   - 서버 사이드 렌더링 중심
   - 동적 웹사이트 생성
   - 실시간 데이터 처리

2. **Gatsby**
   - 순수 정적 사이트 생성
   - 블로그, 포트폴리오에 최적화
   - 빌드 타임 데이터 처리

## Gatsby의 동작 방식
![Gatsby 구조](./images/gatsby/gatsby2.png)

### 1. Data Sources
- 다양한 데이터 소스 지원
  - CMS (WordPress 등)
  - Markdown 파일
  - 외부 API
  - 데이터베이스

### 2. Build Process
- GraphQL 데이터 레이어
- React 컴포넌트 구성
- 플러그인 시스템 활용
- 자동 최적화

### 3. Deploy
- 정적 파일 생성
- CDN 배포
- 서버리스 운영
- 높은 성능 보장

## 결론
Gatsby는 현대적인 웹 개발 트렌드인 JAMStack을 완벽하게 구현하면서, 개발자 경험과 사용자 경험을 모두 개선한 프레임워크입니다. 특히 기술 블로그나 문서화 사이트 같은 정적 콘텐츠 중심의 웹사이트 구축에 탁월한 선택이 될 수 있습니다.

---