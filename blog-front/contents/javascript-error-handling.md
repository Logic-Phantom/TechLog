---
date: '2025-09-19'
title: '자바스크립트에서 `try...catch`와 예외 처리 기법 총정리'
categories: ['Web']
summary: '예외 처리하는 방안'
thumbnail: './images/javascript/jsError.png'
comments: true
---
# 자바스크립트에서 `try...catch`와 예외 처리 기법 총정리

## 1. 기본 개념

### `try...catch`란?

-   자바스크립트에서 **예외 처리(Error Handling)**를 위한 구문.
-   `try` 블록에서 실행 중 오류가 발생하면, `catch` 블록이 호출됨.
-   오류가 없으면 `catch`는 실행되지 않음.

``` js
try {
  console.log(abc); // ReferenceError: abc is not defined
} catch (error) {
  console.error("에러 발생:", error.message);
}
```

### 실행 흐름

1.  `try` 블록 실행
2.  에러 발생 시 → 제어 흐름이 `catch`로 이동
3.  에러 없으면 → `catch`는 건너뜀
4.  `finally` 블록이 있다면 무조건 실행됨 (성공/실패 상관없이)

``` js
try {
  console.log("실행 시작");
  throw new Error("강제 에러");
} catch (e) {
  console.log("에러 잡음:", e.message);
} finally {
  console.log("무조건 실행됨");
}
```

------------------------------------------------------------------------

## 2. `catch`가 실행되는 조건

-   **런타임 에러**: 정의되지 않은 변수 참조, 타입 에러, 잘못된 함수
    호출 등.
-   **명시적 throw**: `throw new Error()` 등.
-   **`await` 구문에서 Promise reject**: async 함수 내 `try...catch`에서
    잡힘.

``` js
async function test() {
  try {
    await Promise.reject(new Error("실패!"));
  } catch (e) {
    console.log("catch 실행:", e.message);
  }
}
test();
```

------------------------------------------------------------------------

## 3. `catch`가 실행되지 않는 경우

-   **문법 오류 (파싱 단계에서 발생)**: 코드 자체가 실행 전에 막히므로
    `try...catch`로 못 잡음.
-   **비동기 콜백에서 발생한 에러**: 외부 `try...catch`로는 잡히지 않음.
-   **Promise reject (await 없이)**: 단순히 `Promise.reject()`만 하면
    `catch`에서 잡히지 않음.

``` js
try {
  setTimeout(() => {
    throw new Error("이건 바깥 try로 못 잡음");
  }, 100);
} catch (e) {
  console.log("여기엔 도달하지 않음");
}
```

------------------------------------------------------------------------

## 4. `try...catch`처럼 사용할 수 있는 문법 및 기술

### 4.1 `Promise.prototype.catch`

-   비동기 에러 처리를 위한 체인 방식.

``` js
fetch("/api/data")
  .then(res => res.json())
  .catch(err => console.error("에러 발생:", err));
```

### 4.2 `async/await` + `try...catch`

-   비동기 코드를 동기처럼 작성 가능.

``` js
async function loadData() {
  try {
    const res = await fetch("/api/data");
    const data = await res.json();
    console.log(data);
  } catch (e) {
    console.error("에러 처리:", e);
  }
}
```

### 4.3 전역 예외 처리

-   **브라우저**: `window.onerror`, `window.addEventListener("error")`
-   **Node.js**: `process.on("uncaughtException")`,
    `process.on("unhandledRejection")`

``` js
window.addEventListener("error", (event) => {
  console.error("전역 에러 잡힘:", event.message);
});

process.on("unhandledRejection", (reason, promise) => {
  console.error("처리되지 않은 Promise 거부:", reason);
});
```

### 4.4 옵셔널 체이닝(Optional Chaining)

-   예외를 던지지 않고 `undefined`를 반환 → 런타임 에러를 예방.

``` js
const user = {};
console.log(user.profile?.name); // undefined (에러 X)
```

### 4.5 Nullish Coalescing 연산자

-   `null` 또는 `undefined`일 때 기본값 대체.

``` js
const name = user.name ?? "Guest";
```

### 4.6 타입스크립트 (TypeScript)

-   정적 타입 체크를 통해 런타임 예외를 사전에 예방.

``` ts
function greet(name: string) {
  console.log("Hello", name);
}
greet("JS"); // 정상
// greet(123); // 컴파일 단계에서 오류
```

------------------------------------------------------------------------

## 5. 전문가용 심화: 에러 처리 아키텍처

### 5.1 커스텀 에러 클래스 정의

``` js
class ValidationError extends Error {
  constructor(message) {
    super(message);
    this.name = "ValidationError";
  }
}

try {
  throw new ValidationError("유효하지 않은 입력");
} catch (e) {
  if (e instanceof ValidationError) {
    console.error("검증 오류:", e.message);
  }
}
```

### 5.2 중앙집중식 에러 처리 (Middleware)

-   Express 같은 서버 프레임워크에서는 **에러 미들웨어**를 두어 일괄
    처리.

``` js
app.use((err, req, res, next) => {
  console.error(err.stack);
  res.status(500).send("Something broke!");
});
```

### 5.3 로깅 & 모니터링

-   `try...catch`로 잡은 에러를 단순 출력하는 게 아니라, Sentry, Datadog
    같은 APM에 기록해 추적 가능.

### 5.4 재시도 패턴 (Retry Pattern)

-   네트워크 에러 시 단순 실패하지 않고 일정 횟수 재시도.

``` js
async function fetchWithRetry(url, retries = 3) {
  for (let i = 0; i < retries; i++) {
    try {
      const res = await fetch(url);
      if (!res.ok) throw new Error("Request failed");
      return await res.json();
    } catch (e) {
      if (i === retries - 1) throw e; // 마지막 시도 실패
    }
  }
}
```

------------------------------------------------------------------------

## 6. 결론

-   `try...catch`는 **런타임 예외 처리**의 핵심.
-   하지만 **비동기 코드, 전역 예외, 타입 체크, 안전한 연산자** 등
    다양한 보완 기술을 함께 써야 안정적인 애플리케이션을 구축할 수 있음.
-   초급 단계에서는 `try...catch`를 올바르게 쓰는 법을 익히고, 고급
    단계에서는 **아키텍처 차원에서 에러를 어떻게 관리할지** 고민하는
    것이 중요하다.
