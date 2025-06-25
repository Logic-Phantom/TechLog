---
date: '2025-06-25'
title: 'CLEOPATRA XML 구조와 코드 자동화 도구 구축기'
categories: ['ETC']
summary: 'Figma → XML 자동 변환 → 정합성 검증 → 배포 자동화'
thumbnail: './images/etc/etc.png'
comments: true
---

# CLEOPATRA XML 구조와 코드 자동화 도구 구축기

## 📌 시작하며

Figma 디자인을 CLEOPATRA XML(.clx)로 자동 변환하는 프로젝트를 진행하며,
단순한 태그 매핑을 넘어, XML 정합성 검사, 자동화 배포, 라벨링 자동화까지 이어지는
엔드-투-엔드 개발 워크플로를 구축하게 되었습니다.

이 글에서는 그 과정에서 마주한 문제, CLEOPATRA의 XML 구조와 자주 쓰는 태그/속성,
그리고 GitHub Actions를 이용한 자동화 도구 구축 사례까지 자세히 소개합니다.

---

## 1. CLEOPATRA `.clx` XML 구조 분석

CLEOPATRA는 `.clx` 확장자의 XML 기반 UI 마크업을 사용합니다. 처음엔 단순한 XML로 보였지만, 다음과 같은 구조적 특성과 규칙이 존재합니다.

### 🎯 자주 사용하는 CLEOPATRA 태그

| 태그 | 설명 |
|------|------|
| `<cl:button>` | 버튼 컴포넌트, `id`, `label`, `x`, `y`, `width`, `height` 속성 필수 |
| `<cl:inputbox>` | 입력창 컴포넌트, `id`, `x`, `y`, `type` 필수 |
| `<cl:grid>` | 테이블 형태의 그리드. 하위에 `<cl:gridcolumn>`, `<cl:gridheader>`, `<cl:griddetail>` 존재 |
| `<cl:image>` | 이미지 삽입용. `src`, `x`, `y`, `width`, `height` |
| `<cl:appspec>` | 전체 앱 설정 메타정보 포함 |
| `<cl:model>` | 데이터 모델 정의 영역. `std:sid` 사용 |

```xml
<cl:button id="btnSubmit" label="저장" x="100" y="50" width="120" height="30"/>
```

---

## 2. XML 정합성 검사 자동화

초기에는 사람이 직접 `.clx` 파일을 열고 태그 오류를 일일이 확인했습니다. 그러나 자동 변환이 많아지면서, **자동 XML 정합성 검사기**를 제작하게 되었습니다.

### ✅ 예외 케이스 예시

- `<cl:button>` 태그에 `id` 누락 → XML 파서 오류
- `<cl:model>` 내 `std:sid` 중복 → CLEOPATRA 실행 시 충돌
- `<cl:grid>` 내부 구조 누락 → 화면 비정상 렌더링

### 🔧 해결 방법

```java
// Java DOM 파서를 통한 XML 유효성 검사 예시
DocumentBuilder builder = DocumentBuilderFactory.newInstance().newDocumentBuilder();
Document doc = builder.parse(new File("test.clx"));

NodeList buttons = doc.getElementsByTagName("cl:button");
for (int i = 0; i < buttons.getLength(); i++) {
    Element btn = (Element) buttons.item(i);
    if (!btn.hasAttribute("id")) {
        throw new RuntimeException("button 태그에 id 누락됨");
    }
}
```

---

## 3. 자동화된 .clx 파일 생성

클래스명 기반으로 디자인 요소를 분류하고, 이를 XML 구조로 자동 변환하기 위해
**Labeler 자동화 스크립트**를 제작했습니다.

### 🛠 라벨러 예시 구조

- 입력: Figma JSON
- 처리: 클래스 추출 → CLEOPATRA XML 매핑
- 출력: `.clx`, `.js` 자동 생성 + `label.txt` 생성

```bash
src/
 ├─ figma/
 │   └─ parser.js
 ├─ generator/
 │   ├─ ClxWriter.java
 │   └─ LabelFileWriter.java
 └─ output/
     ├─ result.clx
     └─ label.txt
```

---

## 4. GitHub Actions 기반 자동화 배포

변환기 코드를 커밋하거나 Pull Request 시, 자동으로 다음 작업을 하도록 설정했습니다.

- `.clx` 정합성 검사
- Java 빌드 및 테스트
- 변환 결과물 `.zip` 생성
- Slack 또는 Discord 알림 (선택)

### 📦 GitHub Actions 예시 (`.github/workflows/build.yml`)

```yaml
name: Build and Validate CLEOPATRA XML

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate-xml:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Java
        uses: actions/setup-java@v3
        with:
          java-version: '17'

      - name: Build and Validate
        run: |
          ./gradlew build
          java -jar validator.jar output/result.clx

      - name: Archive result
        uses: actions/upload-artifact@v3
        with:
          name: clx-outputs
          path: output/
```

---

## ✅ 마무리하며

CLEOPATRA XML을 다루는 것은 단순한 UI 마크업 이상의 작업이었습니다.
Figma → XML 자동 변환 → 정합성 검증 → 배포 자동화까지,
전체 흐름을 스크립트와 워크플로로 통합하면서 생산성과 안정성을 크게 높일 수 있었습니다.

이 글이 자동화 도구를 도입하려는 분들께 도움이 되길 바랍니다.
