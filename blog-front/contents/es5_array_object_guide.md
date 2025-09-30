---
date: '2025-09-30'
title: 'JavaScript ES5 배열 & 객체 메서드 총정리'
categories: ['Web']
summary: '객체와 배열'
thumbnail: './images/javascript/jsAry.png'
comments: true
---
# JavaScript ES5 배열 & 객체 메서드 총정리

## 1. 들어가며
ECMAScript 5(ES5)는 2009년에 표준화된 자바스크립트 버전으로, 오늘날 대부분의 브라우저와 환경에서 완벽히 지원됩니다.  
ES5에서 새롭게 추가된 배열 메서드들과 기존 객체 메서드들은 실무에서 매우 자주 쓰이며, 이후 버전(ES6+)의 토대가 됩니다.  

---

## 2. 배열(Array)

### 2.1 기본 문법
```js
var arr = [1, 2, 3, 4];
console.log(arr.length); // 4
console.log(arr[0]);     // 1
```

---

### 2.2 반복 메서드

#### (1) forEach
- 배열을 순회하며 각 요소에 대해 콜백 실행
```js
arr.forEach(function(num, idx) {
  console.log(idx, num);
});
```

#### (2) map
- 각 요소를 변환하여 **새 배열** 반환
```js
var squared = arr.map(function(x) {
  return x * x;
});
// [1, 4, 9, 16]
```

#### (3) filter
- 조건을 만족하는 요소만 남겨 **새 배열** 반환
```js
var even = arr.filter(function(x) {
  return x % 2 === 0;
});
// [2, 4]
```

---

### 2.3 조건 검사 메서드

#### (1) some
- 하나라도 조건을 만족하면 `true`
```js
arr.some(function(x) {
  return x > 3;
}); // true
```

#### (2) every
- 모두 조건을 만족해야 `true`
```js
arr.every(function(x) {
  return x > 0;
}); // true
```

---

### 2.4 탐색 메서드

#### (1) indexOf / lastIndexOf
```js
[1, 2, 3, 2].indexOf(2);     // 1
[1, 2, 3, 2].lastIndexOf(2); // 3
```

#### (2) join
```js
[1,2,3].join("-"); // "1-2-3"
```

---

### 2.5 축약 & 누적 메서드

#### (1) reduce
- 누적 계산 처리
```js
var sum = arr.reduce(function(acc, cur) {
  return acc + cur;
}, 0);
// 10
```

#### (2) reduceRight
- 오른쪽에서 왼쪽으로 계산
```js
var str = ["a","b","c"].reduceRight(function(acc, cur) {
  return acc + cur;
}, "");
// "cba"
```

---

### 2.6 배열 조작 메서드
```js
var a = [1,2,3];
a.push(4);    // [1,2,3,4]
a.pop();      // [1,2,3]
a.shift();    // [2,3]
a.unshift(0); // [0,2,3]
a.slice(1,2); // [2]
a.splice(1,1,"X"); // [2] 반환, 원본: [0,"X",3]
a.concat([4,5]);  // [0,"X",3,4,5]
a.reverse();      // ["X",0,3]
a.sort();         // 사전순 정렬
```

---

## 3. 객체(Object)

### 3.1 기본 문법
```js
var user = { name: "Alice", age: 25 };
console.log(user.name);   // "Alice"
console.log(user["age"]); // 25
```

---

### 3.2 주요 메서드 (ES5 추가)

#### (1) Object.keys
- 객체의 키 배열 반환
```js
Object.keys(user); // ["name", "age"]
```

#### (2) Object.create
- 지정한 프로토타입을 가진 새 객체 생성
```js
var proto = { greet: function() { return "hi"; } };
var obj = Object.create(proto);
obj.greet(); // "hi"
```

#### (3) Object.defineProperty
- 프로퍼티 정의(접근자/속성 제어)
```js
var obj = {};
Object.defineProperty(obj, "x", {
  value: 10,
  writable: false,
  enumerable: true
});
console.log(obj.x); // 10
obj.x = 20;         // 무시됨
```

#### (4) Object.defineProperties
- 여러 프로퍼티 한번에 정의
```js
var person = {};
Object.defineProperties(person, {
  name: { value: "Bob", writable: true },
  age: { value: 30, writable: false }
});
```

#### (5) Object.getOwnPropertyDescriptor
```js
Object.getOwnPropertyDescriptor(person, "age");
// { value:30, writable:false, enumerable:false, configurable:false }
```

#### (6) Object.freeze / Object.seal
```js
var obj2 = { a: 1 };
Object.freeze(obj2);
// obj2.a = 2; // 무시됨

var obj3 = { b: 2 };
Object.seal(obj3);
// obj3.c = 3; // 추가 불가
obj3.b = 5;  // 수정 가능
```

---

## 4. 실무 활용 예제

### 4.1 객체 배열 필터링
```js
var users = [
  { name: "Kim", age: 20 },
  { name: "Lee", age: 30 }
];
var adults = users.filter(function(u) {
  return u.age >= 25;
});
// [{ name:"Lee", age:30 }]
```

### 4.2 그룹핑 (reduce)
```js
var grouped = users.reduce(function(acc, u) {
  if (!acc[u.age]) acc[u.age] = [];
  acc[u.age].push(u);
  return acc;
}, {});
// {20:[{...}], 30:[{...}]}
```

### 4.3 중복 제거
```js
function unique(arr) {
  var result = [];
  arr.forEach(function(item) {
    if (result.indexOf(item) === -1) {
      result.push(item);
    }
  });
  return result;
}
unique([1,2,2,3]); // [1,2,3]
```

---

## 5. 마치며
ES5에서 배열과 객체를 다루는 메서드는 지금까지도 실무에서 기본 중의 기본입니다.  
특히 `forEach`, `map`, `filter`, `reduce`, `Object.keys`, `Object.defineProperty` 등은  
코드의 **가독성**, **재사용성**, **안정성**을 크게 높여줍니다.
