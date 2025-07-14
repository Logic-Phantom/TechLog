---
date: '2025-07-14'
title: '🖥️ 브라우저가 HTML을 불러온 뒤, JavaScript는 무슨 일을 할까?'
categories: ['Web','Html','JavaScript']
summary: 'JavaScript의 기나긴 여정'
thumbnail: './images/web/JavaScriptStory.png'
comments: true
---
# 브라우저가 HTML을 불러온 뒤, JavaScript는 무슨 일을 할까?

---

## 🧭 어느 날의 웹페이지 탐험

"클릭 한 번 했을 뿐인데, 이 많은 일이 벌어진다고?"  
프론트엔드 개발을 막 시작한 나는, 이런 의문이 들었다.  

HTML은 구조이고, CSS는 스타일이고, JavaScript는 동작이라고 배웠다.  
그런데 사용자가 웹사이트에 접속하고, **DOM이 만들어지고, JavaScript가 실행되고, 렌더링이 완료되는 그 순간까지의 흐름**은 과연 어떤 원리일까?

---

## 📦 HTML의 도착: 브라우저의 시작

웹사이트 주소를 치고 엔터를 누르면  
브라우저는 해당 URL로 HTTP 요청을 보낸다. 그리고 응답으로 돌아온 것이 바로 **HTML 파일**이다.

이때부터 브라우저는 **렌더링 엔진**을 통해 다음 작업을 한다:

1. HTML을 위에서부터 차례대로 읽기 시작
2. 태그들을 만나면 DOM(Document Object Model) 트리를 구성
3. `<link>`나 `<script>` 같은 외부 리소스를 만나면 병렬로 다운로드

> 이 과정에서 스크립트가 `<head>`에 `<script src="...">` 형식으로 들어있다면, HTML 파싱은 멈추고 해당 JS를 먼저 처리한다.

---

## 🌳 DOM Tree + CSSOM Tree = Render Tree

HTML을 다 읽고 나면 **DOM 트리**가 완성된다.  
CSS는 따로 **CSSOM**(CSS Object Model) 트리로 변환된다.

이 둘을 합쳐 **렌더 트리(Render Tree)**를 만든 후,  
브라우저는 이것을 바탕으로 **Layout → Paint → Composite** 과정을 거쳐  
**사용자에게 보이는 화면**을 그려낸다.

---

## 🤖 이제 JavaScript의 무대

### ✔️ `DOMContentLoaded` vs `load`

브라우저는 렌더링 완료 시점을 기준으로 이벤트를 두 가지 발생시킨다:

- `DOMContentLoaded`: DOM 트리만 완성되었을 때
- `load`: 모든 리소스 (이미지, 스타일시트 등) 까지 모두 로딩이 끝났을 때

보통 JS는 이 시점을 기준으로 **동적인 행동**을 시작한다:

```js
document.addEventListener("DOMContentLoaded", function () {
  document.querySelector("button").addEventListener("click", () => {
    alert("버튼 클릭됨!");
  });
});
```

---

## 🧠 JavaScript 런타임의 작동 방식

HTML이 다 로드되고 나면, 브라우저는 **자바스크립트 엔진(V8, SpiderMonkey 등)**을 통해 JS를 실행한다.  
이 엔진은 다음과 같은 **이벤트 루프(event loop)** 메커니즘으로 작동한다:

1. **Call Stack**: 현재 실행 중인 함수들을 담는 공간  
2. **Web APIs**: 타이머, DOM, AJAX 등 브라우저에서 제공하는 비동기 작업
3. **Callback Queue**: 완료된 비동기 작업의 콜백 함수들이 대기하는 곳
4. **Event Loop**: 콜스택이 비면, 큐에서 콜백을 꺼내 실행

이 덕분에 JS는 **싱글 쓰레드지만 비동기 처리**가 가능하다.

---

## 🎬 실제 예제: 버튼을 누르면 이미지가 바뀌는 페이지

```html
<body>
  <img id="image" src="default.png" />
  <button id="change">이미지 바꾸기</button>

  <script>
    document.addEventListener("DOMContentLoaded", () => {
      document.getElementById("change").addEventListener("click", () => {
        document.getElementById("image").src = "changed.png";
      });
    });
  </script>
</body>
```

이 단순한 예제에도 다음과 같은 일이 벌어진다:

- HTML 파싱 → DOM 생성
- `DOMContentLoaded` 이벤트 → JS 실행
- 사용자 클릭 → 이벤트 리스너 발동 → 이미지 src 변경
- 브라우저는 변경된 src를 인식하고 다시 이미지 요청 → 화면 갱신

---

## 🔍 마무리: 정적에서 동적으로

HTML은 정적인 구조를 만드는 언어지만,  
**JavaScript는 그 구조를 시간에 따라 변화시킬 수 있는 언어**다.

사용자의 액션, 비동기 데이터, 애니메이션 등  
모든 **동적인 변화의 중심에는 JavaScript의 동작 원리와 이벤트 루프**가 존재한다.

웹페이지는 단순히 '불러오는 것'만으로 끝나지 않는다.  
그 뒤엔 수많은 로직과 이벤트, 렌더링 사이클이 무대 뒤에서 조용히 움직이고 있다.

---

## 🔗 참고자료

- [MDN Web Docs - Event Loop](https://developer.mozilla.org/ko/docs/Web/JavaScript/EventLoop)
- [Google Developers - Critical Rendering Path](https://developer.chrome.com/docs/devtools/rendering/)
