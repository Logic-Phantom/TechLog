---
date: '2026-10-29'
title: '🖍️ CSS Custom Highlight API 완벽 가이드: DOM 변형 없는 초고성능 텍스트 하이라이팅'
categories: ['Web']
summary: 'DOM 수정 없는 초고성능 텍스트 하이라이팅'
thumbnail: './images/css/css-custom-highlight-api-guide.png'
comments: true
---
# 🖍️ CSS Custom Highlight API 완벽 가이드: DOM 변형 없는 초고성능 텍스트 하이라이팅

> DOM 트리 노드를 쪼개거나 `<mark>` 태그로 감싸지 않고도 텍스트를 스타일링할 수 있을까?
> CSS Custom Highlight API를 활용해 레이아웃 리플로우(Reflow) 없이 60fps로 작동하는 차세대 웹 텍스트 하이라이팅 기법을 완벽히 정복합니다.

---

## 📌 목차
1. 🧭 1. DOM 조작 하이라이트의 비극: 왜 Custom Highlight API인가?
2. 💡 2. CSS Custom Highlight API의 작동 원리와 핵심 개념
3. 🛠️ 3. 기본 사용법: Range, Highlight, 그리고 CSS.highlights
4. 🎨 4. CSS ::highlight() 의사 요소 스타일링과 적용 가능한 속성
5. 🔍 5. 실전 예제 1: 초고성능 문서 검색어 실시간 하이라이팅
6. 📊 6. 기존 DOM 방식 vs Custom Highlight API 심층 비교
7. 🔄 7. 실전 예제 2: 다중 하이라이트 레이어와 우선순위(Priority) 관리
8. 🧩 8. Virtual Scrolling 및 대용량 문서 대응 전략
9. ⚠️ 9. 실무 함정과 주의사항 (Text Normalization & Boundary Drift)
10. ⛔ 10. 이 기술을 사용하면 안 되는 경우와 한계점
11. 🧾 11. 정리
12. 📚 참고 자료

---

## 🧭 1. DOM 조작 하이라이트의 비극: 왜 Custom Highlight API인가?

웹 애플리케이션에서 키워드 검색, 문서 내 단어 강조, 코드 에디터 문법 하이라이팅, AI 답변 텍스트 드래그 강조 등을 구현할 때 전통적으로 사용해 온 방법은 **DOM 노드를 분할하고 `<mark>`나 `<span class="highlight">` 태그로 텍스트를 감싸는 것**이었습니다.

그러나 수천 줄이 넘는 전자책 뷰어, 대용량 PDF 미리보기, 또는 실시간 에디터에서 이러한 방식을 사용할 경우 다음과 같은 중대한 문제점이 발생합니다.

1. **극심한 레이아웃 리플로우(Reflow)와 재페인트(Repaint)**: 단어 하나를 감쌀 때마다 텍스트 노드가 분할되어 DOM 트리가 재구성되고, 브라우저는 레이아웃을 다시 계산합니다.
2. **State & DOM 훼손**: 기존 React/Vue 등의 가상 DOM(Virtual DOM) 프레임워크 기반 앱에서 외부 스크립트가 DOM 텍스트 노드를 분할하면 상태 동기화가 깨지거나 Render Mismatch 오류가 발생합니다.
3. **복원 및 제거의 번거로움**: 하이라이팅을 해제하려면 분할된 텍스트 노드를 다시 찾아서 `normalize()`를 호출하거나 parentNode를 복원해야 합니다.

CSS Custom Highlight API는 **DOM 구조를 단 1Bit도 변경하지 않고** 오직 JavaScript의 `Range` 객체와 CSS 레지스트리를 사용해 페인트 레이어 상에서만 스타일을 입히는 혁신적인 W3C 웹 표준 기술입니다.

![DOM 분할 방식과 Custom Highlight API 방식의 처리 방식 비교 도식](./images/css/css-custom-highlight-api-guide-1.png)

---

## 💡 2. CSS Custom Highlight API의 작동 원리와 핵심 개념

Custom Highlight API는 크게 3가지 요소의 협력으로 동작합니다.

1. **`Range` 객체**: 하이라이트할 문서 내 텍스트의 시작점(`startContainer`, `startOffset`)과 끝점(`endContainer`, `endOffset`)을 정의합니다.
2. **`Highlight` 객체**: 하나 이상의 `Range` 객체 모음을 담는 JS 객체입니다. 그룹화된 텍스트 세트에 동일한 스타일 역할을 부여합니다.
3. **`CSS.highlights` 레지스트리**: 전역 Map 형태로, 지정한 이름(Custom Highlight Name)으로 `Highlight` 객체를 등록합니다.
4. **`::highlight(name)` CSS pseudo-element**: CSS에서 등록된 레지스트리 키값을 타겟팅하여 배경색, 글자색, 밑줄 등을 선언적으로 적용합니다.

![Highlight API 작동 단계 다이어그램](./images/css/css-custom-highlight-api-guide-2.png)

이 구조 덕분에 하이라이트 범위를 새로 계산하거나 변경할 때 브라우저는 DOM 트리 re-parsing을 거치지 않고 오직 텍스트 페인팅 단계에서만 스타일을 고속 업데이트합니다.

---

## 🛠️ 3. 기본 사용법: Range, Highlight, 그리고 CSS.highlights

기본적인 자바스크립트 및 CSS 작성 패턴은 매우 단순하며 명확합니다.

### Step 1: HTML 및 DOM 준비
```html
<p id="article">CSS Custom Highlight API는 정말 강력한 차세대 브라우저 기능입니다.</p>
```

### Step 2: Range 지정 및 Highlight 등록 (JavaScript)
```js
// 1. 하이라이팅할 텍스트 노드 참조
const paragraph = document.getElementById('article');
const textNode = paragraph.firstChild;

// 2. 'Custom Highlight' 단어 위치 범위 지정 (index 4 ~ 26)
const range1 = new Range();
range1.setStart(textNode, 4);
range1.setEnd(textNode, 26);

// 3. Highlight 객체 생성 (여러 range 전달 가능)
const myHighlight = new Highlight(range1);

// 4. CSS.highlights 레지스트리에 등록
CSS.highlights.set('search-result', myHighlight);
```

### Step 3: CSS 가상 요소로 스타일 적용 (CSS)
```css
/* CSS 레지스트리에 등록한 이름 'search-result' 타겟팅 */
::highlight(search-result) {
  background-color: #fef08a;
  color: #854d0e;
  text-decoration: underline wavy #ca8a04;
}
```

단 세 단계만으로 DOM 분할 없이 지정된 단어가 화려하게 강조됩니다!

---

## 🎨 4. CSS ::highlight() 의사 요소 스타일링과 적용 가능한 속성

`::highlight()`는 보안 및 브라우저 성능 최적화를 위해 **일부 CSS 속성만 제한적으로 허용**합니다. 텍스트의 레이아웃 박스 크기를 변경시키는 속성(예: `font-size`, `margin`, `padding`, `display`)은 적용되지 않습니다.

| 구분 | 지원되는 속성 목록 | 비고 |
| :--- | :--- | :--- |
| **색상 및 배경** | `color`, `background-color` | 가장 기본적인 하이라이팅 속성 |
| **텍스트 장식** | `text-decoration`, `text-shadow` | 밑줄, 취소선, 물결선, 그림자 효과 |
| **텍스트 강조** | `text-emphasis-color`, `-webkit-text-fill-color` | 텍스트 강조 점 및 채우기 색상 |
| **커스텀 변수** | `var(--custom-color)` | CSS 변수를 통한 다이내믹 컬러 바인딩 가능 |
| **미지원 속성** | `font-size`, `width`, `margin`, `transform` 등 | **레이아웃 변형 속성 전면 불허** |

```css
/* 복합 하이라이트 스타일 예시 */
::highlight(user-selection) {
  background-color: rgba(59, 130, 246, 0.2);
  color: #1d4ed8;
  text-decoration: underline 2px #2563eb;
  text-shadow: 0 0 2px rgba(37, 99, 235, 0.3);
}
```

---

## 🔍 5. 실전 예제 1: 초고성능 문서 검색어 실시간 하이라이팅

사용자가 검색창에 입력할 때마다 대용량 문서 안에서 키워드를 찾아 실시간으로 하이라이팅하는 완벽한 실무 코드를 구현해보겠습니다.

```js
/**
 * 특정 컨테이너 내부의 모든 텍스트 노드에서 검색어를 찾아 Highlight 범위 배열을 반환합니다.
 */
function createSearchRanges(container, query) {
  if (!query) return [];
  
  const ranges = [];
  const treeWalker = document.createTreeWalker(
    container,
    NodeFilter.SHOW_TEXT,
    null
  );

  let currentNode = treeWalker.nextNode();
  const lowerQuery = query.toLowerCase();

  while (currentNode) {
    const text = currentNode.textContent.toLowerCase();
    let startOffset = 0;

    while ((startOffset = text.indexOf(lowerQuery, startOffset)) !== -1) {
      const range = new Range();
      range.setStart(currentNode, startOffset);
      range.setEnd(currentNode, startOffset + query.length);
      ranges.push(range);
      startOffset += query.length;
    }

    currentNode = treeWalker.nextNode();
  }

  return ranges;
}

// 검색창 input 이벤트 바인딩
const searchInput = document.getElementById('search-input');
const contentArea = document.getElementById('content-area');

searchInput.addEventListener('input', (e) => {
  const query = e.target.value.trim();

  if (!query) {
    // 검색어가 없으면 레지스트리에서 제거
    CSS.highlights.delete('find-keyword');
    return;
  }

  const matchedRanges = createSearchRanges(contentArea, query);
  
  // 생성된 Range 목록으로 Highlight 객체 생성 후 등록
  const searchHighlight = new Highlight(...matchedRanges);
  CSS.highlights.set('find-keyword', searchHighlight);
});
```

### CSS 정의
```css
::highlight(find-keyword) {
  background-color: #5b8fd4;
  color: #ffffff;
  border-radius: 2px;
}
```

이 코드는 10만 단어 규모의 문서에서도 input 이벤트 발생 시 16ms(60fps) 이내로 지연 없는 실시간 검색어 강조를 수행합니다.

---

## 📊 6. 기존 DOM 방식 vs Custom Highlight API 심층 비교

두 방식의 기술적 스펙과 실무적 성능 차이를 아래 표로 비교합니다.

| 비교 항목 | 기존 DOM 분할 방식 (`<mark>`) | CSS Custom Highlight API |
| :--- | :--- | :--- |
| **DOM 트리 변경** | 텍스트 노드가 잘리고 여러 노드로 분할됨 | **DOM 변화 없음 (Zero Mutation)** |
| **렌더링 성능** | Reflow + Re-layout 발생 (대용량 시 병목) | **Paint 단계만 수행 (초고성능 60fps)** |
| **React/Vue 호환성** | Virtual DOM과 mismatch 위험 매우 높음 | **완벽한 상호 운용성 (DOM 미선댐)** |
| **이벤트 바인딩** | `<mark onclick="...">` 직접 요소 클릭 가능 | **텍스트 범위 기준 좌표 계산 필요** |
| **제거 비용** | 노드 병합 및 `normalize()` 연산 필요 | **`CSS.highlights.delete()` 끝** |
| **브라우저 지원율** | 100% (오래된 표준) | **Chrome 105+, Safari 17.2+, Firefox 117+ (최신 모던 브라우저 완료)** |

---

## 🔄 7. 실전 예제 2: 다중 하이라이트 레이어와 우선순위(Priority) 관리

문서에서 **검색어 하이라이트**와 **사용자 문장 형광펜(Bookmark)**, 그리고 **AI 추천 단어**가 한 단어 위에서 서로 겹칠 때는 어떻게 될까요?

`Highlight` 객체의 `priority` 속성을 사용하면 스타일 충돌 시 어떤 레이어가 위에 올지 명확하게 제어할 수 있습니다.

```js
// 1. 사용자 문장 형광펜 (우선순위 100 - 최상위)
const userBookmarkRange = new Range();
userBookmarkRange.setStart(textNode, 10);
userBookmarkRange.setEnd(textNode, 30);

const bookmarkHighlight = new Highlight(userBookmarkRange);
bookmarkHighlight.priority = 100; // 높을수록 위에 그려짐
CSS.highlights.set('user-bookmark', bookmarkHighlight);

// 2. 실시간 검색어 (우선순위 10)
const searchRange = new Range();
searchRange.setStart(textNode, 20);
searchRange.setEnd(textNode, 40);

const searchHighlight = new Highlight(searchRange);
searchHighlight.priority = 10;
CSS.highlights.set('search-query', searchHighlight);
```

```css
/* 사용자 형광펜: 노란색 */
::highlight(user-bookmark) {
  background-color: #fef08a;
  color: #000;
}

/* 검색어: 빨간 밑줄 */
::highlight(search-query) {
  background-color: #bbf7d0;
  text-decoration: underline red 2px;
}
```

`index 20 ~ 30` 지점은 두 하이라이트가 겹치게 됩니다. 이때 `priority: 100`인 `user-bookmark` 배경색이 우세하게 적용되며, overlap 속성 중 중복되지 않는 `text-decoration` 등은 함께 렌더링됩니다.

---

## 🧩 8. Virtual Scrolling 및 대용량 문서 대응 전략

만약 무한 스크롤이나 가상 스크롤(Virtual List)이 적용된 수십만 줄의 뷰어라면 어떻게 최적화해야 할까요?

1. **화면에 보이는 DOM 노드만 탐색**: 전체 데이터베이스 문서를 다 찾지 않고, 현재 Viewport에 마운트된 텍스트 노드에 대해서만 Range를 생성합니다.
2. **Range Reuse**: 스크롤이 움직여 DOM 노드가 언마운트되면, 해당 DOM을 가리키던 Range를 `CSS.highlights`에서 제거하여 메모리 누수를 방지합니다.

```js
// 가상 스크롤 컴포넌트의 unmount 시 정리 코드
function cleanupUnmountedNodeHighlights(highlightName, targetNode) {
  const highlight = CSS.highlights.get(highlightName);
  if (!highlight) return;

  for (const range of highlight) {
    if (range.intersectsNode(targetNode)) {
      highlight.delete(range);
    }
  }
}
```

---

## ⚠️ 9. 실무 함정과 주의사항 (Text Normalization & Boundary Drift)

Custom Highlight API를 실무에 도입할 때 반드시 마주치는 2가지 함정이 있습니다.

### 함정 1: 동적 DOM 변경 시 위치 어긋남 (Boundary Drift)
JavaScript가 `Range`를 등록한 후, 사용자 입력이나 API 응답으로 텍스트 노드의 내용이 중간에 수정되면 기존 `Range`의 `startOffset`과 `endOffset`이 고정되어 하이라이트 위치가 어긋나는 현상이 발생합니다.

- **해결책**: DOM 텍스트가 변경되는 시점에 MutationObserver를 활용하거나, 입력 이벤트 핸들러에서 해당 노드의 Range offset을 즉시 재계산하여 업데이트해야 합니다.

### 함정 2: `Text.splitText()` 또는 `node.normalize()` 호출 금지
기존 레거시 라이브러리가 DOM 조작을 수행하며 텍스트 노드를 쪼개버리면, 미리 쥐고 있던 `Range` 참조가 깨지거나 불합리한 오프셋을 가리키게 됩니다.

- **해결책**: Custom Highlight API를 도입했다면 기존의 DOM 분할 방식 텍스트 하이라이팅 라이브러리(예: mark.js 등)와 혼용하지 말고 완전히 이관해야 합니다.

---

## ⛔ 10. 이 기술을 사용하면 안 되는 경우와 한계점

모든 상황에 Custom Highlight API가 정답은 아닙니다.

1. **하이라이트된 텍스트 요소에 직접 클릭/마우스 호버 이벤트를 달아야 하는 경우**
   - `::highlight()` 가상 요소는 실제 DOM 노드가 아니므로 `.addEventListener('click')`을 할 수 없습니다.
   - *대안*: 하이라이트된 영역에 마우스 이벤트를 바인딩하려면 `document.caretRangeFromPoint()`나 `Range.getBoundingClientRect()`로 좌표를 역산해야 하므로, 개별 단어 단위의 복잡한 툴팁 클릭이 필수라면 전통적인 `<mark>` 노드 방식이 더 유리할 수 있습니다.
2. **구형 브라우저 및 특정 WebView 지원 필수 서비스**
   - IE 지원이나 아주 구형 모바일 WebView(iOS 16 미만, Android 구형 WebView)를 타겟팅해야 하는 환경이라면 폴리필(Polyfill) 또는 fallback 처리가 필요합니다.

--- 

## 🧾 11. 정리

- **CSS Custom Highlight API**는 DOM 트리를 수정하지 않고 `Range`와 CSS 가상 요소를 결합해 텍스트에 고성능 스타일을 입히는 현대적 웹 표준입니다.
- 기존 `<mark>` 태그 분할 방식 대비 **Reflow 발생 제로, 메모리 절감, React/Vue 호환성 완벽 보장**이라는 강력한 이점을 지닙니다.
- `Highlight.priority`로 다중 레이어 우선순위를 쉽게 관리할 수 있으며, 검색어 강조, 에디터 선택 영역, AI 텍스트 피드백 표시에 가장 최적화되어 있습니다.
- 하이라이트 영역에 직접 클릭 이벤트를 붙이는 특수 목적을 제외하면, 모던 웹 프론트엔드의 모든 텍스트 강조 기능은 Custom Highlight API로 대체하는 것이 확실한 모범 답안입니다.

> ✨ **한 줄 요약**
> DOM을 쪼개는 비효율적인 하이라이팅은 끝났다. `Range`와 `CSS.highlights`로 60fps 스무스 텍스트 스타일링을 구현하자!

---

## 📚 참고 자료
- [MDN Web Docs: CSS Custom Highlight API](https://developer.mozilla.org/en-US/docs/Web/API/CSS_Custom_Highlight_API)
- [W3C CSS Custom Highlight API Module Level 1 Spec](https://www.w3.org/TR/css-highlight-api-1/)
- [Chrome Developers: CSS Custom Highlight API](https://developer.chrome.com/blog/css-custom-highlight-api/)
