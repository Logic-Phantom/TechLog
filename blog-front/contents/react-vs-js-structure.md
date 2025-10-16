---
date: '2025-10-16'
title: 'React 스크립트 구조 vs 순수 JavaScript 스크립트 구조 완벽 비교'
categories: ['web']
summary: '구조 파악해보기'
thumbnail: './images/javascript/ReactScr.png'
comments: true
---
# React 스크립트 구조 vs 순수 JavaScript 스크립트 구조 완벽 비교

## 🧭 들어가며
React는 자바스크립트 기반 라이브러리이지만, 그 **스크립트 구조와 개발 패러다임**은 순수 JavaScript(이하 “Vanilla JS”)와 다릅니다.  
이 글에서는 JavaScript만 사용해온 개발자도 **React의 구조를 한눈에 이해**할 수 있도록,  
**기본 → 심화 → 전문가 수준** 순으로 정리합니다.

---

## 1️⃣ 기본 개념 차이

| 구분 | Vanilla JavaScript | React |
|------|--------------------|--------|
| 목적 | DOM 직접 조작 | UI 상태(state)에 따른 렌더링 |
| 구조 | HTML + JS 분리 | JSX(JS + XML) 통합 구조 |
| 데이터 흐름 | 수동 업데이트 | 단방향 데이터 흐름 (state → UI) |
| 렌더링 방식 | DOM API를 직접 호출 | 가상 DOM(Virtual DOM) 사용 |
| 재사용성 | 낮음 (함수 중심) | 높음 (컴포넌트 중심) |

### 💡 핵심 요약
Vanilla JS는 **명령형(Imperative)** 방식이고,  
React는 **선언형(Declarative)** 방식입니다.

> 명령형: “무엇을 어떻게 할지” 직접 지시  
> 선언형: “무엇이 되어야 하는지” 선언

---

## 2️⃣ 스크립트 구조 비교 (Hello World 예제)

### ✅ Vanilla JavaScript 버전
```html
<!DOCTYPE html>
<html>
  <body>
    <div id="app"></div>
    <script>
      const app = document.getElementById('app');
      const message = document.createElement('h1');
      message.textContent = 'Hello World!';
      app.appendChild(message);
    </script>
  </body>
</html>
```

**설명**
- DOM 요소를 직접 생성하고 `appendChild()`로 붙입니다.
- 코드 흐름이 “명령형”입니다.
- HTML, CSS, JS가 명확히 분리되어 있습니다.

---

### ✅ React 버전
```jsx
import React from 'react';
import ReactDOM from 'react-dom/client';

function App() {
  return <h1>Hello World!</h1>;
}

const root = ReactDOM.createRoot(document.getElementById('app'));
root.render(<App />);
```

**설명**
- JSX 문법을 통해 **HTML과 JS를 결합**.
- DOM을 직접 조작하지 않고 **ReactDOM이 자동 렌더링**.
- 구조적으로는 `컴포넌트 단위`로 설계됩니다.

---

## 3️⃣ 이벤트 처리 구조 비교

### 🔹 Vanilla JS
```html
<button id="btn">Click</button>
<script>
  document.getElementById('btn').addEventListener('click', function() {
    alert('Button clicked!');
  });
</script>
```

### 🔹 React
```jsx
function App() {
  function handleClick() {
    alert('Button clicked!');
  }

  return <button onClick={handleClick}>Click</button>;
}
```

**차이점**
| 구분 | Vanilla JS | React |
|------|-------------|--------|
| 이벤트 등록 | DOM API 직접 사용 | JSX 속성으로 정의 |
| 스코프 | 전역 또는 외부 함수 | 컴포넌트 내부 함수 |
| 구조적 재사용 | 불가능 | 가능 (컴포넌트 단위) |

---

## 4️⃣ 상태 관리 (State) 개념

Vanilla JS에서는 데이터가 바뀌면 직접 DOM을 수정해야 합니다.

```html
<div id="counter">0</div>
<button id="btn">+1</button>
<script>
  let count = 0;
  document.getElementById('btn').addEventListener('click', () => {
    count++;
    document.getElementById('counter').textContent = count;
  });
</script>
```

React에서는 `state`로 관리합니다.

```jsx
import { useState } from 'react';

function Counter() {
  const [count, setCount] = useState(0);

  return (
    <>
      <div>{count}</div>
      <button onClick={() => setCount(count + 1)}>+1</button>
    </>
  );
}
```

**React의 핵심:**
- UI는 `state`의 결과물입니다.  
- `setState` 호출 시 React가 자동으로 Virtual DOM을 비교(diffing)하고 필요한 부분만 다시 렌더링합니다.

---

## 5️⃣ 컴포넌트 기반 아키텍처

React는 **UI를 작은 단위로 분리(컴포넌트화)** 합니다.

### Vanilla JS 구조
```
index.html
 └── script.js
```

### React 구조
```
src/
 ├── App.jsx
 ├── components/
 │   ├── Header.jsx
 │   ├── Button.jsx
 │   └── Footer.jsx
 └── index.js
```

**장점**
- 각 기능 단위로 나뉜 모듈형 구조
- 재사용성 ↑, 유지보수성 ↑, 테스트 용이

---

## 6️⃣ JSX와 DOM의 차이

| 항목 | JSX | DOM |
|------|------|------|
| 작성 방식 | HTML과 유사하지만 JS 안에서 작성 | 브라우저가 렌더링하는 실제 노드 |
| 렌더링 주체 | ReactDOM | 브라우저 |
| 데이터 바인딩 | {변수} 사용 | innerText, innerHTML 직접 수정 |
| 속성명 | `className`, `onClick` | `class`, `onclick` |

**예시**
```jsx
<div className="box" onClick={handleClick}>
  {title}
</div>
```

---

## 7️⃣ React의 렌더링 사이클 (전문가 영역)

React는 단순히 화면을 그리는 것이 아니라, 다음 단계를 거칩니다.

1. **렌더 단계(Render Phase)**  
   - 컴포넌트를 호출해 Virtual DOM 트리를 생성
2. **커밋 단계(Commit Phase)**  
   - 변경된 부분만 실제 DOM에 반영 (Reconciliation)
3. **리렌더 조건**  
   - props 변경, state 변경, 부모 리렌더 시

React 18 이후부터는 **Concurrent Rendering(동시 렌더링)**이 도입되어,  
UI 응답성을 유지하면서 비동기적으로 렌더링을 처리할 수 있습니다.

---

## 8️⃣ React vs JavaScript 아키텍처 비교 정리

| 구분 | Vanilla JS | React |
|------|-------------|--------|
| 개발 철학 | 명령형 | 선언형 |
| 구조 | HTML, CSS, JS 분리 | 컴포넌트 단위 통합 |
| 렌더링 | DOM 직접 조작 | Virtual DOM 자동 반영 |
| 상태 관리 | 변수 기반 | useState, Redux, Context 등 |
| 재사용성 | 낮음 | 높음 |
| 유지보수 | 어려움 | 쉬움 (컴포넌트 단위) |
| 성능 최적화 | 직접 처리 | 자동 diffing & memoization 가능 |

---

## 9️⃣ 심화: React 내부 구조 이해

React는 **Fiber Architecture**를 사용합니다.  
이는 Virtual DOM을 효율적으로 업데이트하기 위한 **비동기 스케줄링 엔진**입니다.

- **Fiber Node**: 각 컴포넌트의 렌더 정보를 담은 객체  
- **Reconciliation**: 이전 Fiber와 새 Fiber 비교  
- **Commit**: 실제 DOM 반영

이 덕분에 React는 대규모 애플리케이션에서도 **부분 업데이트**만 수행하며,  
렌더링 성능을 크게 개선할 수 있습니다.

---

## 🧩 결론

| 요약 포인트 | 설명 |
|--------------|--------|
| React는 JS 기반이지만, 구조는 전혀 다르다 | 명령형 → 선언형 전환 |
| DOM 조작 대신 상태(state) 중심 | 데이터 흐름이 명확 |
| 컴포넌트 단위로 설계 | 재사용성과 확장성 확보 |
| Virtual DOM, Fiber 아키텍처 등 내부 구조가 존재 | 고성능 렌더링 가능 |

---

## 🚀 마무리

Vanilla JS에서 React로 전환할 때 가장 중요한 것은  
“**DOM을 직접 조작하지 않는다**”는 사고 전환입니다.

React는 단순한 UI 라이브러리가 아니라,  
**UI 상태(State)를 기반으로 선언형 구조를 제공하는 렌더링 엔진**입니다.  

React의 핵심을 이해했다면,  
당신의 자바스크립트 코드는 한 단계 더 진화할 것입니다. ✨

---

**📘 참고 자료**
- [React 공식 문서](https://react.dev/)
- [MDN Web Docs - DOM](https://developer.mozilla.org/ko/docs/Web/API/Document_Object_Model)
- [React Fiber Architecture Explained](https://github.com/acdlite/react-fiber-architecture)
