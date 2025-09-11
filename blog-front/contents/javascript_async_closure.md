---
date: '2025-09-11'
title: '자바스크립트 비동기 처리와 클로저 완전 정복'
categories: ['Web']
summary: '자바스크립트 두번째 이야기'
thumbnail: './images/javascript/jsRule2.png'
comments: true
---
# 자바스크립트 비동기 처리와 클로저 완전 정복

## 1. 비동기 처리의 배경

자바스크립트는 **싱글 스레드 언어**로, 한 번에 하나의 작업만 실행할 수
있습니다.\
하지만 네트워크 요청, 파일 읽기, 타이머 같은 작업을 모두 동기적으로
처리하면 브라우저가 멈추게 됩니다.\
이를 해결하기 위해 **비동기 처리(Asynchronous)** 개념이 도입되었습니다.

------------------------------------------------------------------------

## 2. Promise

### 기본 개념

`Promise`는 비동기 작업의 완료/실패를 나타내는 객체입니다.

``` js
const promise = new Promise((resolve, reject) => {
  setTimeout(() => {
    resolve("완료!");
    // reject("에러 발생");
  }, 1000);
});

promise
  .then(result => console.log(result)) // 완료!
  .catch(error => console.error(error))
  .finally(() => console.log("항상 실행"));
```

### 상태

-   `pending`: 대기 중
-   `fulfilled`: 성공
-   `rejected`: 실패

### 실무 예제

``` js
function fetchData(url){
  return new Promise((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onload = () => resolve(xhr.responseText);
    xhr.onerror = () => reject("에러 발생");
    xhr.send();
  });
}

fetchData("/api/data")
  .then(data => console.log(data))
  .catch(err => console.error(err));
```

------------------------------------------------------------------------

## 3. async / await

### 기본 개념

`async/await`는 Promise 기반 코드를 **동기식처럼 작성**할 수 있게
해줍니다.

``` js
async function getUser(){
  try {
    const res = await fetch("/api/user");
    const user = await res.json();
    console.log(user);
  } catch(e) {
    console.error("에러 발생", e);
  }
}
getUser();
```

### 특징

-   `async` 함수는 항상 Promise 반환
-   `await`는 Promise가 처리될 때까지 기다림
-   `try...catch`로 에러 처리 가능

### 실무 예제

``` js
async function getPosts(){
  const urls = ["/api/post/1", "/api/post/2"];
  const results = [];
  for(const url of urls){
    const res = await fetch(url);
    results.push(await res.json());
  }
  return results;
}

getPosts().then(posts => console.log(posts));
```

⚡ **Tip**: 독립적인 요청은 `Promise.all`을 활용하면 성능 향상

``` js
async function getPostsParallel(){
  const urls = ["/api/post/1", "/api/post/2"];
  const results = await Promise.all(urls.map(url => fetch(url).then(r=>r.json())));
  return results;
}
```

------------------------------------------------------------------------

## 4. 클로저 (Closure)

### 기본 개념

클로저는 **함수가 선언될 당시의 스코프(환경)를 기억하는 함수**입니다.

``` js
function outer(){
  let count = 0;
  return function inner(){
    count++;
    return count;
  }
}

const counter = outer();
console.log(counter()); // 1
console.log(counter()); // 2
```

### 활용 예시

-   **데이터 은닉**: 외부에서 직접 접근 불가능한 private 변수 생성
-   **상태 유지**: 함수 호출 간 데이터 보존
-   **콜백/이벤트 핸들러**: 상태를 기억하는 핸들러 작성

### 실무 예제

``` js
function createUserManager(){
  let users = [];
  return {
    add: function(user){ users.push(user); },
    list: function(){ return users.slice(); }
  };
}

const manager = createUserManager();
manager.add("Alice");
manager.add("Bob");
console.log(manager.list()); // ["Alice", "Bob"]
```

------------------------------------------------------------------------

## 5. 고급 활용 (전문가용)

### 5.1. Promise 고급 패턴

-   **Promise.all**: 모든 Promise 완료 대기
-   **Promise.race**: 가장 빠른 Promise 결과 반환
-   **Promise.allSettled**: 모든 결과(성공/실패)를 배열로 반환

``` js
Promise.race([
  fetch("/api/slow"),
  fetch("/api/fast")
]).then(res => console.log("가장 빠른 응답", res));
```

### 5.2. async/await 최적화

-   병렬 처리 시 `Promise.all` 적극 활용
-   반복문 안에서는 `for...of` + await보다 **map + Promise.all** 선호

``` js
async function loadData(ids){
  return await Promise.all(ids.map(id => fetch(`/api/${id}`).then(r=>r.json())));
}
```

### 5.3. 클로저와 메모리 관리

클로저는 **참조를 유지**하기 때문에 메모리 누수(leak)가 발생할 수 있음.\
→ 불필요한 참조는 `null`로 해제하거나, 클로저 사용 범위를 최소화해야 함.

``` js
function heavy(){
  let bigData = new Array(1000000).fill("data");
  return function(){
    console.log(bigData[0]);
  };
}
const h = heavy();
// bigData는 해제되지 않음 → 메모리 사용 주의
```

------------------------------------------------------------------------

## 6. 정리

-   **Promise**: 비동기 작업의 성공/실패를 다루는 객체
-   **async/await**: Promise를 더 읽기 쉽게 작성하는 문법
-   **클로저**: 스코프를 기억하는 함수, 상태 유지 및 데이터 은닉 가능

👉 초급 단계에서는 콜백 → Promise → async/await 순으로 이해\
👉 심화 단계에서는 병렬 처리 최적화, 클로저 메모리 관리까지 고려해야
합니다.

------------------------------------------------------------------------

# 마무리

자바스크립트에서 **비동기 처리**와 **클로저**는 단순한 문법 지식이
아니라,\
실무에서 성능, 유지보수, 보안까지 영향을 미치는 핵심 개념입니다.\
이 두 가지를 제대로 이해하면 **안정적이고 효율적인 코드**를 작성할 수
있습니다.
