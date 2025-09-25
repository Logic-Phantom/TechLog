---
date: '2025-09-25'
title: '자바스크립트 window 객체 완벽 가이드'
categories: ['Web']
summary: 'Window 객체 를 알아보자자'
thumbnail: './images/javascript/jsWin.png'
comments: true
---

# 자바스크립트 `window` 객체 완벽 가이드

웹 브라우저 환경에서 자바스크립트를 실행할 때 가장 기본이 되는 전역
객체가 바로 **`window` 객체**입니다.\
브라우저에서 실행되는 모든 전역 변수와 함수는 사실상 `window` 객체의
속성으로 등록되며,\
DOM 조작, 브라우저 제어, 이벤트 처리 등 다양한 기능을 제공합니다.

------------------------------------------------------------------------

## 1. `window` 객체란?

-   **브라우저 환경에서의 전역 객체**
    -   Node.js에서는 `global` 객체가 전역이지만, 브라우저에서는
        `window`가 전역 객체 역할을 합니다.
    -   전역으로 선언된 변수/함수는 자동으로 `window` 객체의 속성으로
        등록됩니다.

``` javascript
var globalVar = "Hello";
console.log(window.globalVar); // "Hello"
```

-   **최상위 컨텍스트**
    -   `this` 키워드가 전역에서 참조될 경우 `window`를 가리킵니다.
    -   ES 모듈(`type="module"`)에서는 `undefined`가 되므로 차이가
        있습니다.

------------------------------------------------------------------------

## 2. 주요 속성과 메서드

### 2.1 브라우저 제어 관련

-   **`window.location`**
    -   현재 문서의 URL 정보를 담고 있으며, 페이지 이동/리다이렉트를
        제어합니다.

    ``` javascript
    console.log(window.location.href); // 현재 페이지의 전체 URL
    window.location.href = "https://example.com"; // 페이지 이동
    ```
-   **`window.history`**
    -   사용자의 브라우저 히스토리를 다루는 객체입니다.
    -   `back()`, `forward()`, `go(n)` 같은 메서드를 제공합니다.

    ``` javascript
    history.back();     // 뒤로가기
    history.forward();  // 앞으로가기
    history.go(-2);     // 2단계 뒤로 이동
    ```
-   **`window.navigator`**
    -   브라우저와 운영체제의 정보를 제공합니다.

    ``` javascript
    console.log(navigator.userAgent); // 브라우저/OS 정보
    console.log(navigator.language);  // 언어 설정
    ```

------------------------------------------------------------------------

### 2.2 화면 및 문서 관련

-   **`window.document`**
    -   현재 로드된 DOM(Document Object Model) 객체를 나타냅니다.
    -   DOM 조작의 진입점.

    ``` javascript
    document.title = "새 제목";
    document.body.style.background = "lightgray";
    ```
-   **`window.screen`**
    -   사용자의 화면 해상도와 컬러 정보 제공.

    ``` javascript
    console.log(screen.width, screen.height); // 화면 해상도
    ```

------------------------------------------------------------------------

### 2.3 팝업 및 UI 관련

-   **`alert()`, `confirm()`, `prompt()`**
    -   기본 대화 상자 제공.

    ``` javascript
    alert("Hello, World!");
    if (confirm("삭제하시겠습니까?")) {
      console.log("삭제 실행");
    }
    let name = prompt("이름을 입력하세요:");
    ```
-   **`open()`**
    -   새로운 브라우저 창 또는 탭을 엽니다.

    ``` javascript
    let newWin = window.open("https://example.com", "_blank", "width=500,height=400");
    ```

------------------------------------------------------------------------

### 2.4 타이머 관련

-   **`setTimeout` / `clearTimeout`**

    ``` javascript
    let timer = setTimeout(() => console.log("3초 후 실행"), 3000);
    clearTimeout(timer);
    ```

-   **`setInterval` / `clearInterval`**

    ``` javascript
    let interval = setInterval(() => console.log("1초마다 실행"), 1000);
    clearInterval(interval);
    ```

------------------------------------------------------------------------

## 3. 고급 활용

### 3.1 SPA(싱글 페이지 애플리케이션)와 History API

-   `pushState()`와 `replaceState()`를 사용하면 브라우저 주소 표시줄을
    바꾸면서도 페이지 전체 새로고침 없이 화면을 전환할 수 있습니다.

``` javascript
history.pushState({ page: 1 }, "title 1", "?page=1");
history.replaceState({ page: 2 }, "title 2", "?page=2");

window.onpopstate = function(event) {
  console.log("뒤로가기/앞으로가기 이벤트", event.state);
};
```

### 3.2 메시지 전달 (`postMessage`)

-   다른 창/iframe 간 안전한 데이터 전달 가능.

``` javascript
// 부모 창
let child = window.open("child.html");
child.postMessage("Hello Child", "*");

// 자식 창 (child.html)
window.addEventListener("message", (event) => {
  console.log("부모에서 받은 메시지:", event.data);
});
```

### 3.3 브라우저 스토리지

-   `window.localStorage`, `window.sessionStorage`를 통해 키-값 저장소
    활용 가능.

``` javascript
localStorage.setItem("user", "Alice");
console.log(localStorage.getItem("user")); // "Alice"
```

------------------------------------------------------------------------

## 4. 보안 및 주의사항

1.  **팝업 차단**: `window.open()`은 사용자 액션(클릭 등) 없이 호출하면
    대부분 브라우저에서 차단됩니다.
2.  **CORS 제한**: 다른 도메인의 `window` 객체 접근은 제한됩니다.
3.  **전역 오염 방지**: 변수를 `window`에 직접 올리는 대신 `let`,
    `const` 사용으로 스코프를 제한하는 것이 바람직합니다.
4.  **모듈 환경 차이**: ES 모듈이나 `strict mode`에서 `this`는
    `window`를 가리키지 않을 수 있습니다.

------------------------------------------------------------------------

## 5. 요약

-   `window`는 브라우저 환경의 전역 객체이며, DOM, 네비게이션, 타이머,
    팝업, 저장소 등 다양한 기능을 제공.
-   `history.pushState` 같은 API는 SPA 라우팅 구현에 핵심적.
-   보안, 호환성, 사용자 경험을 고려해 적절히 사용하는 것이 중요.

------------------------------------------------------------------------
