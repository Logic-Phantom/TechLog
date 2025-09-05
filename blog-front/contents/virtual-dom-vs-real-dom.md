---
date: '2025-09-05'
title: '⚡ Virtual DOM vs Real DOM 조작 성능 비교'
categories: ['Web']
summary: '가상과 현실의 차이'
thumbnail: './images/web/VirtualDOM.png'
comments: true
---
# ⚡ Virtual DOM vs Real DOM 조작 성능 비교

## 1. 들어가며
웹 개발을 하다 보면 **DOM(Document Object Model)** 조작은 필수적입니다.  
특히 프론트엔드 라이브러리(React, Vue, Svelte 등)가 등장하면서, 기존 브라우저의 **Real DOM** 조작과 이를 개선하기 위한 **Virtual DOM** 개념의 차이가 중요한 논의 주제가 되었습니다.  

이번 글에서는 **기초적인 DOM 개념부터 시작해서, Virtual DOM이 등장한 이유, 성능 비교, 실제 상황에서의 적용 전략**까지 단계적으로 살펴보겠습니다.

---

## 2. Real DOM이란?
**Real DOM**은 브라우저가 HTML 문서를 해석해 생성하는 **트리 구조의 객체 모델**입니다.  
즉, HTML 태그와 구조를 메모리 상에서 트리 형태로 표현한 것으로, JavaScript를 통해 조작할 수 있습니다.

### ✨ 특징
- **트리 구조**: `document` → `html` → `body` → `div` → `span` …
- **상호작용**: JS에서 `document.querySelector()` 같은 메서드로 접근/수정 가능
- **렌더링**: DOM 변경 → Reflow(레이아웃 계산) & Repaint(화면 갱신) 발생

### ⚠️ 한계
- 작은 변경도 전체 트리의 일부를 다시 렌더링해야 할 수 있음
- 대규모 UI 업데이트 시 성능 저하 발생
- DOM API 자체가 무겁고, 브라우저 엔진과의 상호작용 비용이 큼

---

## 3. Virtual DOM이란?
**Virtual DOM**은 브라우저의 DOM을 직접 건드리지 않고, **메모리 상에서 가상의 DOM 트리를 만들어 두고 비교(diffing)한 후 필요한 부분만 Real DOM에 반영하는 방식**입니다.

### ✨ 특징
- **메모리 상의 가상 객체**: Real DOM을 추상화한 JS 객체 트리
- **Diff 알고리즘**: 이전 Virtual DOM과 새로운 Virtual DOM을 비교하여 최소 변경 사항만 Real DOM에 반영
- **Batching**: 여러 변경을 모아 한 번에 Real DOM에 적용

---

## 4. 도식: Virtual DOM Diff 과정

```
초기 상태:
Real DOM      Virtual DOM
  <ul>           <ul>
   <li>A</li>     <li>A</li>
   <li>B</li>     <li>B</li>
   <li>C</li>     <li>C</li>
  </ul>          </ul>

업데이트 (C → D):
New Virtual DOM
  <ul>
   <li>A</li>
   <li>B</li>
   <li>D</li>
  </ul>

Diff 알고리즘 동작:
- A 동일
- B 동일
- C → D 변경

최종 Real DOM 반영:
  <ul>
   <li>A</li>
   <li>B</li>
   <li>D</li>
  </ul>
```

➡️ Virtual DOM은 전체를 다시 렌더링하지 않고, 변경된 `C → D`만 Real DOM에 반영합니다.

---

## 5. 성능 비교

### (1) Real DOM 조작
- **장점**: 단순 구조에서는 직접 조작이 빠를 수 있음
- **단점**: 많은 엘리먼트 변경 시 불필요한 Reflow/Repaint 반복 발생

> 예시: 리스트 1만 개 중 하나를 업데이트해도, 브라우저는 렌더 트리 전체를 다시 계산해야 할 수 있음

### (2) Virtual DOM 조작
- **장점**:
  - 변경 감지(diff) 후 최소 변경만 적용
  - 대규모 UI 업데이트에서 효율적
  - React/Vue 같은 프레임워크 최적화 기술과 결합
- **단점**:
  - Virtual DOM 자체를 구성하고 비교하는 비용이 존재
  - 아주 작은 변경에서는 Real DOM보다 느릴 수 있음

---

## 6. 간단한 코드 예제: 성능 비교

### ✅ Real DOM 직접 조작
```html
<button id="realBtn">Real DOM 업데이트</button>
<ul id="realList"></ul>

<script>
const realList = document.getElementById('realList');
for (let i = 0; i < 10000; i++) {
  const li = document.createElement('li');
  li.textContent = `Item ${i}`;
  realList.appendChild(li);
}

document.getElementById('realBtn').addEventListener('click', () => {
  console.time('Real DOM');
  for (let i = 0; i < 10000; i++) {
    realList.children[i].textContent = `Updated ${i}`;
  }
  console.timeEnd('Real DOM');
});
</script>
```

### ✅ Virtual DOM 방식 (간단 구현)
```html
<button id="virtualBtn">Virtual DOM 업데이트</button>
<ul id="virtualList"></ul>

<script>
let vdom = Array.from({ length: 10000 }, (_, i) => `Item ${i}`);

function renderVDOM(vdom) {
  const list = document.getElementById('virtualList');
  list.innerHTML = vdom.map(item => `<li>${item}</li>`).join('');
}

renderVDOM(vdom);

document.getElementById('virtualBtn').addEventListener('click', () => {
  console.time('Virtual DOM');
  // 새로운 Virtual DOM 생성
  const newVdom = vdom.map((_, i) => `Updated ${i}`);
  
  // Diff & Patch (간단히 모든 항목 비교)
  newVdom.forEach((val, i) => {
    if (val !== vdom[i]) {
      document.getElementById('virtualList').children[i].textContent = val;
    }
  });

  vdom = newVdom;
  console.timeEnd('Virtual DOM');
});
</script>
```

---

## 7. 전문가 관점 심화 분석

### (1) Virtual DOM의 핵심 최적화
- **O(n) Diff 알고리즘**: key 기반 비교로 성능 최적화
- **Batch Update**: 이벤트 루프 단위로 업데이트 모아 처리
- **Fiber 구조 (React 16+)**: 렌더링 작업을 분할·중단·재개 가능

### (2) Real DOM 최적화 방법
- **DocumentFragment** 사용
- **requestAnimationFrame** 활용
- **Canvas/WebGL**로 직접 렌더링

### (3) 새로운 대안: Signals & Fine-grained reactivity
- SolidJS, Svelte → Virtual DOM 자체를 생략
- 상태 변경이 일어난 지점만 직접 업데이트

---

## 8. 언제 어떤 방식을 선택할까?

| 상황 | 권장 방식 |
|------|-----------|
| 간단한 DOM 조작 (Vanilla JS, jQuery 스타일) | Real DOM 직접 조작 |
| 대규모 SPA (React, Vue 등) | Virtual DOM 기반 |
| 고성능 그래픽/UI (게임, 시각화 등) | Canvas, WebGL, 혹은 Fine-grained reactivity 프레임워크 |
| 마이크로 인터랙션 위주 | Real DOM + 최적화 기법 |

---

## 9. 결론
- **Real DOM**은 단순하지만 대규모 변경에 비효율적이다.
- **Virtual DOM**은 대규모 업데이트를 효율적으로 처리하기 위해 도입된 추상화 계층이다.
- 하지만 Virtual DOM도 만능은 아니며, 최근에는 **Fine-grained reactivity**와 같은 대체 기술이 주목받고 있다.
- 따라서, **프로젝트의 규모, 성능 요구사항, 팀의 기술 스택**에 따라 올바른 방식을 선택하는 것이 중요하다.

---

## 10. 참고 자료
- [React 공식 문서: Virtual DOM](https://react.dev/learn/keeping-components-pure)
- [MDN Web Docs: DOM](https://developer.mozilla.org/ko/docs/Web/API/Document_Object_Model)
- [Vue.js Guide: Virtual DOM](https://vuejs.org/guide/extras/rendering-mechanism.html)
