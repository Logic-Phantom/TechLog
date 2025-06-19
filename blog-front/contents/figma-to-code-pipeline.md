---
date: '2025-06-19'
title: '코드 파이프라인 자동화 구축기'
categories: ['Figma','design']
summary: 'JSON -> XML 변환'
thumbnail: './images/css/Figma.png'
comments: true
---

# 🚀 Figma → 코드 파이프라인 자동화 구축기

## 🧩 프로젝트 개요
- **프로젝트명**: Converter‑Figma  
- **목표**: Figma에서 바로 JSON/XML로 디자인 데이터를 추출한 뒤, CI/CD 파이프라인을 통해 자동 배포까지 연결하는 **엔드 투 엔드 자동화 시스템**  
- **사용 기술**:
  - Figma API + Node.js 스크립트
  - 구조화된 JSON → `.clx` / `.xml` 변환기 (CLEOPATRA 플랫폼용)
  - GitHub Actions 기반 CI/CD
  - 코드 정렬/포맷터 (Prettier / custom script)

---

## 1️⃣ Figma 데이터 추출 자동화
- **Figma API** 활용 스크립트 작성  
  - export 대상은 특정 Frame 및 컴포넌트  
  - JSON 형식으로 저장 → 이후 XML 변환 모듈로 파이프라인 연결  
- **난관**:
  - 디자인 스펙 누락 → 개발 중 예기치 않은 파싱 에러 발생  
  - **해결**: API 호출 전 스펙 유효성 검사 로직 추가, 누락 항목 감지 시 Slack/Webhook으로 알림

---

## 2️⃣ 중간 표현 (IR: Intermediate Representation)
- Figma에서 추출된 JSON을 어떻게 변환해야 할까?
  - 커스텀 구조(`AltNode`) 설계 → 부모-자식 구조 재구성  
  - **레이아웃 최적화**:
    - auto-layout, 고정폭·반응형 처리가 핵심
    - JSON 내 레이아웃 키 재배치 및 중복 속성 제거 스크립트 적용

---

## 3️⃣ JSON → XML(`.clx`) 변환기 구성
- **JSON → `.clx/.xml`**로 변환 담당 모듈 구현  
- **난관**:
  - 속성 누락 및 순서 불일치 → CLEOPATRA 파싱 실패  
  - **결실**: 변환 후 자동 검사(Validator) 도입 + CI 워크플로에 통합 → 불일치 시 PR 실패 처리

```js
// 예시: 자동 검사 스니펫
const xmlStr = generateCLX(altNodes);
if (!validateXML(xmlStr)) {
  throw new Error('⛔ CLX validation failed — 자동 배포 중단');
}
```

---

## 4️⃣ CI/CD 워크플로
- GitHub Actions 설정:

```yaml
on:
  push:
    paths:
      - 'figma/**'
jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Figma 데이터 fetch & 변환
        run: npm run fetch-and-convert
      - name: XML 검사
        run: npm run validate-xml
      - name: 배포
        run: npm run deploy-to-cleopatra
```

- **Auto-rollback**: 변환 실패 시 워크플로 중단 + Slack/Email Notification

---

## 5️⃣ 코드 정렬 / 스타일 일관성
- `Prettier` 기반 XML 포맷 터 → 정렬 이슈 최소화  
- **문제 해결**:
  - 포맷팅 규칙 미흡으로 발생하는 `XML diff` 과도 → CI 검사에 `git diff --exit-code` 추가

---

## 6️⃣ 🎯 실전 적용 피드백
- **효과**:
  - Figma 디자인 → 코드 반영까지 걸리는 시간 10분 → 1분으로 단축  
  - 수동 누락 실수 ↓, 린트 에러 및 형식 문제 사전 차단  
- **아쉬움 & 개선점**:
  - 복잡한 design token/variable 관리까지 확대 예정  
  - Workflow 안정성 보강 위한 테스트 케이스 추가 예정

---

## 📝 코드·스크린샷·CI 예시 준비 방법
| 항목 | 설명 |
|------|------|
| 코드 스니펫 | 주요 파이프라인, CLI 스크립트, XML 변환 코드 |
| CI 설정 | GitHub Actions 워크플로 전체 YAML |
| 스크린샷 | Figma 발췌 예시, CI 실행 로그 캡처 |
| 결과물 | 생성된 `.clx` 파일 비교(전/후 diff) |

---

## ✍️ 마무리 코멘트
이 프로젝트는 **디자인 → 코드 배포까지 한 줄 자동화**라는 꿈을 실제로 구현한 경험입니다.  
“자동화할 수 있는 단계는 모두 코드로” 라는 원칙 아래, **적중한 스펙 검증·포맷 자동화·CI 차단 로직**이 핵심입니다.  
이제는 **디자인 한 번 바뀌면 코드가 바로 적용되는 시대** 입니다. 😉
