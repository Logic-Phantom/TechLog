---
date: '2025-09-10'
title: '자바스크립트 기본 문법부터 실무 활용까지 총정리'
categories: ['Web']
summary: '기본 부터 단단히'
thumbnail: './images/javascript/jsRule.png'
comments: true
---
# 자바스크립트 기본 문법부터 실무 활용까지 총정리

## 1. 변수와 상수

-   **var**: 함수 스코프, 호이스팅 발생 → 사용 지양
-   **let**: 블록 스코프, 재할당 가능
-   **const**: 블록 스코프, 재할당 불가 (불변 아님, 객체 내부 수정 가능)

``` js
let count = 1;
const PI = 3.14;
```

------------------------------------------------------------------------

## 2. 자료형

-   기본형(Primitive): string, number, boolean, null, undefined, symbol,
    bigint
-   참조형(Object): object, array, function, date, regexp

``` js
typeof "hello"; // string
typeof 123;     // number
typeof null;    // object (JS의 오래된 버그)
```

------------------------------------------------------------------------

## 3. 배열 다루기

### 요소 추가/삭제

``` js
const arr = [1,2,3];
arr.push(4);   // [1,2,3,4]
arr.pop();     // [1,2,3]
arr.shift();   // [2,3]
arr.unshift(0);// [0,2,3]
```

### 특정 요소 제거 (filter)

``` js
const arr = [1,2,3,4];
const result = arr.filter(x => x !== 2); // [1,3,4]
```

💡 **실무 예제**\
사용자 권한 목록에서 특정 권한 제거하기

``` js
const permissions = ["READ", "WRITE", "DELETE"];
const safePermissions = permissions.filter(p => p !== "DELETE");
// ["READ", "WRITE"]
```

### 중복 제거 (Set 활용)

``` js
const arr = [1,1,2,2,3];
const unique = [...new Set(arr)]; // [1,2,3]
```

### 배열 합치기

``` js
const a = [1,2];
const b = [3,4];
const merged = [...a, ...b]; // [1,2,3,4]
```

### 고급 활용: reduce

``` js
const sum = [1,2,3,4].reduce((acc,cur) => acc+cur, 0); // 10
```

⚡ **성능 비교**\
큰 배열에서 합을 구할 때 for문이 reduce보다 빠르다.

``` js
const bigArr = Array(1e6).fill(1);

// reduce
console.time("reduce");
bigArr.reduce((a,b)=>a+b,0);
console.timeEnd("reduce");

// for loop
console.time("for");
let total = 0;
for(let i=0;i<bigArr.length;i++) total+=bigArr[i];
console.timeEnd("for");
```

실무에서는 **가독성** → reduce, **성능 최적화 필요 시** → for.

------------------------------------------------------------------------

## 4. 문자열 다루기

### 검색 및 대체

``` js
"hello world".indexOf("world"); // 6
"hello world".includes("hello"); // true
"hello world".replace("world", "JS"); // hello JS
```

💡 **실무 예제**\
사용자 입력에서 불필요한 공백 제거 후 금칙어 필터링

``` js
let input = "  bad word ";
input = input.trim().replace("bad","***"); // "*** word"
```

### 자르기

``` js
"apple,banana,cherry".split(","); // ["apple","banana","cherry"]
"javascript".slice(0,4); // "java"
```

⚡ **성능 비교**\
정규식 replace vs split+join

``` js
const text = "a-b-c-d";

console.time("replace");
for(let i=0;i<1e6;i++) text.replace(/-/g,"");
console.timeEnd("replace");

console.time("splitjoin");
for(let i=0;i<1e6;i++) text.split("-").join("");
console.timeEnd("splitjoin");
```

대체로 **split+join이 빠르다**.

------------------------------------------------------------------------

## 5. 함수

### 선언식 vs 표현식

``` js
function add(a,b){ return a+b; }
const sub = function(a,b){ return a-b; };
```

💡 **실무 예제**\
콜백 함수 전달

``` js
const arr = [1,2,3];
arr.forEach(function(x){ console.log(x*2); });
```

### 화살표 함수

``` js
const mul = (a,b) => a*b;
```

⚡ **성능 비교**\
화살표 함수와 일반 함수의 성능은 거의 동일 → 가독성과 this 바인딩 차이가
중요.

------------------------------------------------------------------------

## 6. 객체

### 선언 및 접근

``` js
const user = {name:"Tom", age:20};
user.name; // Tom
user["age"]; // 20
```

💡 **실무 예제**\
API 응답 데이터 파싱

``` js
const response = {id:1, profile:{name:"Alice"}};
const name = response.profile?.name ?? "Guest";
```

------------------------------------------------------------------------

## 7. 조건문과 반복문

### 조건문

``` js
if(x > 10) {...} else {...}
x > 10 ? "크다" : "작다";
```

### 반복문

``` js
for(let i=0;i<5;i++) console.log(i);
for(const x of [1,2,3]) console.log(x);
[1,2,3].forEach(x => console.log(x));
```

⚡ **성능 비교**\
for vs forEach

``` js
const arr = Array(1e6).fill(1);

console.time("for");
let sum1 = 0;
for(let i=0;i<arr.length;i++) sum1+=arr[i];
console.timeEnd("for");

console.time("forEach");
let sum2 = 0;
arr.forEach(x => sum2+=x);
console.timeEnd("forEach");
```

`for`가 더 빠름 → **대용량 데이터** 처리 시 권장.

------------------------------------------------------------------------

## 8. 비동기 처리

### 콜백

``` js
setTimeout(() => console.log("done"), 1000);
```

### Promise

``` js
new Promise(resolve => resolve(1)).then(x => console.log(x));
```

### async/await

``` js
async function fetchData(){
  const res = await fetch("url");
  return res.json();
}
```

💡 **실무 예제**

``` js
async function getUser(){
  try{
    const res = await fetch("/api/user");
    const user = await res.json();
    console.log(user);
  }catch(e){
    console.error("에러 발생", e);
  }
}
```

------------------------------------------------------------------------

## 9. 고급 활용

### 배열 메서드 체이닝

``` js
const result = [1,2,3,4,5]
  .filter(x => x%2===0)
  .map(x => x*x)
  .reduce((a,b)=>a+b,0); // 20
```

⚡ **성능 비교**

``` js
const bigArr = Array(1e6).fill(1).map((_,i)=>i);

// 체이닝
console.time("chaining");
const result1 = bigArr.filter(x=>x%2===0).map(x=>x*2).reduce((a,b)=>a+b,0);
console.timeEnd("chaining");

// for
console.time("for");
let result2=0;
for(let i=0;i<bigArr.length;i++){
  if(bigArr[i]%2===0) result2 += bigArr[i]*2;
}
console.timeEnd("for");
```

**가독성**: 체이닝, **속도**: for.

------------------------------------------------------------------------

## 10. 전문가용 팁

-   **불변성 유지**: 직접 값 수정 대신 새로운 객체/배열 생성하기
    (리액트, 리덕스에서 중요)
-   **깊은 복사**: `JSON.parse(JSON.stringify(obj))` 또는
    `structuredClone(obj)`
-   **성능 최적화**: 반복문보단 map/filter/reduce 활용, 하지만 대규모
    데이터에서는 for문이 더 빠름
-   **에러 핸들링**: `try...catch`와 `Promise.catch` 적극 활용
-   **모듈화**: ES6 `import/export`로 코드 분리

------------------------------------------------------------------------

# 마무리

자바스크립트는 단순 문법만 아는 것과, 실제 상황에서 활용하는 것은 큰
차이가 있습니다.\
기본기(배열, 문자열, 객체 조작)를 충분히 익히고, **비동기 처리 / ES6
문법 / 함수형 패턴**을 활용하면 더욱 생산적인 코드를 작성할 수 있습니다.
