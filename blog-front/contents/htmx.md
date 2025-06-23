---
date: '2024-11-20'
title: 'HTMX: 현대적인 웹 개발 접근법'
categories: ['Web']
summary: 'HTMX를 활용한 서버 사이드 렌더링과 동적 웹 애플리케이션'
thumbnail: './images/html/html.png'
comments: true
---

# 🚀 HTMX: HTML의 반격이 시작된다

> "HTML을 다시 주인공으로 만들 시간이다."

프론트엔드 세계는 React, Vue, Angular 같은 프레임워크가 지배해 왔습니다. 하지만 무거운 빌드, 러닝 커브, 점점 증가하는 복잡도에 지친 개발자들이 새로운 대안을 찾기 시작했습니다.

바로 그 대안, **HTMX**.

---

## 💡 HTMX란 무엇인가?

**htmx**는 HTML의 확장이며, 서버와의 상호작용을 **AJAX, CSS Transitions, WebSockets, Server-Sent Events**와 같은 기술로 간단하게 HTML 태그 안에서 처리할 수 있게 해줍니다.

### 요약하자면:

- ✅ **JavaScript 없이도 동적인 UI 가능**
- ✅ **서버 중심 개발에 최적화**
- ✅ **기존 HTML에 속성만 추가하면 끝**
- ✅ **초경량 - gzipped 기준 10KB 이하**

---

## 🧠 철학: HTML을 Hypermedia로

htmx는 HTML을 단순한 마크업 이상의 **Hypermedia**로 활용하자는 철학을 가지고 있습니다. "서버가 HTML을 반환하는 것이 구시대적"이라는 인식을 뒤집습니다.

```html
<!-- htmx가 없었다면 복잡한 JS로 처리했을 코드 -->
<button hx-get="/like" hx-swap="outerHTML">
  👍 좋아요
</button>
```

> 클릭하면 `/like` 엔드포인트에 GET 요청을 보내고, 해당 버튼 자체를 서버의 응답으로 교체합니다.

---

## ⚙️ 주요 속성들

| 속성 | 설명 |
|------|------|
| `hx-get`, `hx-post` | AJAX 요청을 보낼 HTTP 메서드 |
| `hx-target` | 응답을 삽입할 대상 |
| `hx-swap` | 응답을 삽입하는 방식 (innerHTML, outerHTML 등) |
| `hx-trigger` | 이벤트 트리거 설정 (클릭, 변경, 지연 등) |

---

## 📦 설치 방법

```html
<script src="https://unpkg.com/htmx.org@1.9.2"></script>
```

혹은 CDN 없이 직접 호스팅할 수도 있습니다.

---

## 🧪 실전 예제: 댓글 리스트에 새로운 댓글 추가하기

```html
<form hx-post="/comments" hx-target="#comment-list" hx-swap="beforeend">
  <input type="text" name="comment" placeholder="댓글 입력..." />
  <button type="submit">작성</button>
</form>

<ul id="comment-list">
  <li>첫 번째 댓글</li>
</ul>
```

서버가 새로운 `<li>`를 반환하면, 자동으로 `<ul>`의 마지막에 추가됩니다.

---

## ⚔️ HTMX vs Modern JS 프레임워크

| 항목 | htmx | React / Vue |
|------|------|-------------|
| 학습 곡선 | 낮음 | 중~고 |
| 초기 설정 | 거의 없음 | 복잡함 |
| 성능 | 빠름 (서버 중심) | 클라이언트 중심 |
| 확장성 | REST/HATEOAS 기반 | 상태관리 필요 |
| JavaScript 의존도 | 낮음 | 높음 |

---

## 🌐 어디에 쓰면 좋은가?

- 빠르게 만드는 **관리자 페이지, CRUD 웹앱**
- HTML 중심의 **마케팅 페이지**
- 서버 중심의 **Django, Flask, Spring** 앱
- 무거운 프레임워크 도입이 과한 프로젝트

---

## 🎯 결론: 웹 개발의 미니멀리즘

htmx는 **HTML만으로도 충분히 동적인 웹앱**을 만들 수 있다는 것을 보여줍니다. 단순함과 명료함, 그리고 서버 중심의 개발 방식으로 다시 돌아가고 싶다면, htmx는 최고의 선택이 될 수 있습니다.

> "더 적은 코드로 더 많은 기능을."

---

## 🔗 참고자료

- 공식 홈페이지: [https://htmx.org](https://htmx.org)
- 깃허브 저장소: [https://github.com/bigskysoftware/htmx](https://github.com/bigskysoftware/htmx)
- HATEOAS 개념 설명: [REST의 Hypermedia](https://restfulapi.net/hateoas/)

---

