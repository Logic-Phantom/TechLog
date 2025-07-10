---
date: '2025-07-10'
title: '🖥️ HTML이 브라우저에 그려지는 여정'
categories: ['Web','Html']
summary: 'HTML의 기나긴 여정'
thumbnail: './images/web/HtmlStory.png'
comments: true
---

# 🖥️ HTML이 브라우저에 그려지는 여정

> 브라우저는 HTML을 어떻게 화면에 그릴까?  
> 단순한 HTML 파일이 어떻게 웹페이지가 되는지, 우리가 매일 보는 화면이 만들어지는 모든 과정을 이야기로 풀어보자.

---

## 1. 📡 브라우저, 서버에 문을 두드리다

브라우저가 열리자마자 사용자가 주소창에 URL을 입력한다.  
예를 들어 `https://www.example.com`이라고 치면, 브라우저는 다음과 같은 일을 한다.

- **DNS 조회:** 이 도메인을 실제 IP 주소로 변환한다. (`A record`)
- **TCP 연결:** 서버와 연결을 맺기 위해 3-way 핸드셰이크를 진행한다.
- **HTTPS라면 TLS 핸드셰이크도 진행된다.**
- **HTTP 요청 전송:** `GET / HTTP/1.1` 요청과 함께 브라우저의 User-Agent 등을 포함한 헤더도 같이 전송한다.

---

## 2. 📄 HTML, 응답으로 돌아오다

서버는 브라우저의 요청을 받고 HTML 파일을 응답한다.

```http
HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
  <head>
    <title>Example</title>
  </head>
  <body>
    <h1>Hello World</h1>
    <img src="banner.png" />
  </body>
</html>
```

이제부터 브라우저는 이 텍스트 데이터를 가지고 본격적인 **그리기 작업(rendering)** 에 들어간다.

---

## 3. 🔍 Parsing — HTML을 DOM으로 변환

브라우저는 HTML 텍스트를 한 줄씩 읽으며 **토큰(token)** 을 만든다.  
그리고 이를 **DOM(Document Object Model)** 이라는 **트리 구조**로 바꾼다.

- `<html>` → DOM 노드 생성
- `<head>`, `<body>` 등 자식 노드 생성
- `<h1>Hello</h1>` → 텍스트 노드까지 포함한 구조로

> 이때 DOM은 메모리에 존재하는 **자바스크립트 객체 트리**다.

---

## 4. 🎨 CSSOM — 스타일도 트리로

HTML에는 `<style>`이나 `<link rel="stylesheet">` 같은 스타일 정의도 포함된다.

- 브라우저는 CSS 파일도 비동기로 다운로드한다.
- 그 후 CSS 텍스트를 해석하여 CSSOM(CSS Object Model)을 만든다.

```css
h1 {
  color: blue;
  font-size: 24px;
}
```

CSSOM도 DOM처럼 트리 구조이며, 어떤 노드에 어떤 스타일이 적용되는지 정의한다.

---

## 5. 🧩 Render Tree 구성

이제 DOM과 CSSOM을 조합하여 **Render Tree**를 만든다.

- DOM은 구조 정보
- CSSOM은 스타일 정보
- Render Tree는 실제로 **화면에 표시할 요소만 포함한 구조**

예시:
- `<head>`는 화면에 표시되지 않으므로 Render Tree에서 제외
- `<h1>Hello</h1>`는 Render Tree에 포함되고, 색상, 폰트 등의 스타일도 함께 적용된다.

---

## 6. 📐 Layout — 위치 계산

Render Tree를 만들었다면 이제 각 요소가 **어디에 위치할지**를 계산한다.  
이 단계는 "레이아웃(Layout)" 또는 "Reflow"라고도 부른다.

- 요소의 `width`, `height`, `padding`, `margin`, `position` 등 CSS 정보를 바탕으로 위치를 결정
- 부모 요소의 위치, 스크롤, 뷰포트 크기까지 고려함

> 이 단계는 **비용이 크기 때문에 최소화**하는 것이 성능에 중요하다.

---

## 7. 🖌️ Painting — 화면에 색칠하기

이제 계산된 각 요소를 실제 **픽셀 단위로 그리는 작업**이 시작된다.

- 각 박스에 배경색을 칠하고
- 텍스트를 렌더링하고
- 이미지를 삽입하고
- 보더나 그림자도 그린다

브라우저는 이 정보를 **레이어** 단위로 나누어 GPU에 전달한다.

---

## 8. 🚀 Compositing — 최종 합성

마지막 단계는 여러 레이어를 GPU에서 **합성(compositing)** 하는 것이다.

- 예를 들어:
  - 배경 레이어
  - 텍스트 레이어
  - 이미지 레이어
- 이들을 순서대로 겹쳐서 한 화면으로 보여준다.

---

## 9. 💫 자바스크립트의 개입

자바스크립트는 DOM을 동적으로 바꾸거나 스타일을 바꿀 수 있다.

- `element.style.color = "red"`
- `document.body.appendChild(newDiv)`
- 애니메이션, 이벤트, Ajax 등으로 DOM이 변하면 **다시 Layout → Paint → Composite** 단계를 거친다.

> 따라서 DOM을 자주 바꾸는 코드는 성능 이슈를 유발할 수 있다.

---

## 🧠 정리 — 브라우저의 렌더링 파이프라인

```
[HTML 응답]
    ↓
[Parsing → DOM 생성]
    ↓
[CSSOM 생성]
    ↓
[Render Tree 생성]
    ↓
[Layout]
    ↓
[Paint]
    ↓
[Composite → 화면 출력]
```

이 과정을 **렌더링 파이프라인(Rendering Pipeline)** 이라고 부르며, 브라우저마다 최적화 방식은 조금씩 다르지만 기본 원리는 같다.

---

## ✨ 마치며

HTML은 그저 텍스트일 뿐이지만, 브라우저는 이를 **구조화하고**, **스타일링하고**, **위치와 모양을 계산한 뒤**, 결국 우리가 보는 아름다운 웹페이지로 완성한다.

이 과정을 이해하는 건 단순한 이론 공부가 아니다.  
**성능 최적화**, **애니메이션 처리**, **DOM 조작** 등 실제 프론트엔드 개발에 큰 도움이 된다.

---

🛠️ **다음 편 예고:**  
"브라우저 렌더링 성능 최적화 — Layout Thrashing과 그 해결법"
