---
date: '2025-10-01'
title: '자바스크립트에서 꼭 알아야 할 개념과 기술들'
categories: ['Web']
summary: '(ES5 & ES6 기준)'
thumbnail: './images/javascript/jsMust.png'
comments: true
---
# 자바스크립트에서 꼭 알아야 할 개념과 기술들 (ES5 & ES6 기준)

자바스크립트(JavaScript)는 웹 개발의 핵심 언어로, ES5(ECMAScript 5)와
ES6(ECMAScript 2015) 이후부터는 문법적·기능적 발전이 크게
이루어졌습니다.\
이 글에서는 **기본부터 전문가 수준까지** 꼭 알아야 할 자바스크립트의
핵심 개념과 테크닉을 정리합니다.

------------------------------------------------------------------------

## 1. 기본 개념 (ES5 중심)

### 1.1 변수 선언 방식

-   **`var`**\
    ES5까지 사용되던 변수 선언 키워드. 함수 스코프(function scope)를
    가짐.

    ``` js
    var x = 10;
    function test() {
      var y = 20;
      console.log(x, y); // 10, 20
    }
    ```

-   **호이스팅(Hoisting)**: `var`로 선언된 변수는 선언부가 함수 맨 위로
    끌어올려지는 것처럼 동작.

------------------------------------------------------------------------

### 1.2 데이터 타입

-   원시 타입 (Primitive): `string`, `number`, `boolean`, `null`,
    `undefined`
-   참조 타입 (Reference): `object`, `array`, `function`

``` js
var str = "Hello";   // string
var num = 42;        // number
var arr = [1,2,3];   // array (object)
var fn = function() { return "함수"; };
```

------------------------------------------------------------------------

### 1.3 함수와 스코프

-   **함수 선언식**과 **함수 표현식**

    ``` js
    // 선언식 (호이스팅 O)
    function add(a, b) {
      return a + b;
    }

    // 표현식 (호이스팅 X)
    var multiply = function(a, b) {
      return a * b;
    };
    ```

-   **this** 키워드 (ES5)

    -   전역: `window` (브라우저) 또는 `global` (Node.js)
    -   함수 내부: 호출 방식에 따라 달라짐

    ``` js
    var obj = {
      name: "JS",
      getName: function() {
        return this.name;
      }
    };
    console.log(obj.getName()); // "JS"
    ```

------------------------------------------------------------------------

### 1.4 배열(Array) 메서드 (ES5)

-   `forEach`, `map`, `filter`, `reduce`

``` js
var nums = [1,2,3,4];
var doubled = nums.map(function(n){ return n*2; }); // [2,4,6,8]
var sum = nums.reduce(function(acc, cur){ return acc+cur; }, 0); // 10
```

------------------------------------------------------------------------

## 2. ES6 이후 핵심 개념

### 2.1 let과 const

-   **`let`**: 블록 스코프(block scope), 재할당 가능
-   **`const`**: 상수, 재할당 불가 (참조형은 값 변경 가능)

``` js
let a = 1;
const b = {x:1};
b.x = 2; // 가능
```

------------------------------------------------------------------------

### 2.2 화살표 함수 (Arrow Function)

-   `this` 바인딩이 정적(lexical scope)으로 결정됨

``` js
const add = (a, b) => a + b;
```

------------------------------------------------------------------------

### 2.3 구조 분해 할당 (Destructuring)

``` js
const arr = [1,2];
const [x,y] = arr; // x=1, y=2

const obj = {name:"JS", age:10};
const {name, age} = obj;
```

------------------------------------------------------------------------

### 2.4 템플릿 리터럴

``` js
let name = "JS";
console.log(`Hello, ${name}!`); // "Hello, JS!"
```

------------------------------------------------------------------------

### 2.5 클래스(Class) 문법

``` js
class Person {
  constructor(name) {
    this.name = name;
  }
  greet() {
    return `Hello, I'm ${this.name}`;
  }
}
```

------------------------------------------------------------------------

### 2.6 모듈 (Module)

-   **export / import**

``` js
// util.js
export function sum(a,b){ return a+b; }

// main.js
import {sum} from './util.js';
```

------------------------------------------------------------------------

## 3. 꼭 알아야 할 고급 개념과 테크닉

### 3.1 클로저(Closure)

함수가 선언될 때의 환경(스코프)을 기억하여 외부 함수의 변수를 참조.

``` js
function counter() {
  var count = 0;
  return function() {
    count++;
    return count;
  }
}
var c = counter();
console.log(c()); // 1
console.log(c()); // 2
```

------------------------------------------------------------------------

### 3.2 프로토타입(Prototype)과 상속

``` js
function Animal(name) {
  this.name = name;
}
Animal.prototype.say = function() {
  console.log("Hi, I'm " + this.name);
};
var dog = new Animal("Dog");
dog.say(); // Hi, I'm Dog
```

------------------------------------------------------------------------

### 3.3 비동기 처리 (ES5 vs ES6)

-   **ES5: 콜백(callback)**

``` js
setTimeout(function() {
  console.log("done");
}, 1000);
```

-   **ES6: Promise**

``` js
new Promise((resolve) => {
  setTimeout(()=> resolve("done"), 1000);
}).then(console.log);
```

-   **ES8 이후: async/await** (참고)

``` js
async function run() {
  let result = await new Promise(r => setTimeout(()=>r("done"),1000));
  console.log(result);
}
```

------------------------------------------------------------------------

### 3.4 변수 네이밍 관례와 언더스코프(\_)

-   `_`(언더스코어) 활용 예시:
    -   **프라이빗 변수 표기**: `_count`
    -   **사용하지 않는 변수 자리 표시자**: `(value, _index) => { ... }`
    -   **라이브러리 전용 네임스페이스**: `_` (예: Lodash)

------------------------------------------------------------------------

### 3.5 주석(Comment) 패턴

-   단일 라인 주석: `//`
-   블록 주석: `/* ... */`
-   JSDoc 스타일 (전문가용)

``` js
/**
 * 두 수를 더합니다.
 * @param {number} a 
 * @param {number} b 
 * @returns {number}
 */
function add(a, b){ return a+b; }
```

------------------------------------------------------------------------

### 3.6 함수형 프로그래밍 기법

-   순수 함수, 불변성 유지, 고차 함수

``` js
const arr = [1,2,3];
const doubled = arr.map(x=>x*2); // 순수 함수
```

------------------------------------------------------------------------

### 3.7 모듈 패턴과 싱글톤

``` js
var Singleton = (function(){
  var instance;
  function createInstance(){
    return {name:"single"};
  }
  return {
    getInstance: function(){
      if(!instance) instance = createInstance();
      return instance;
    }
  };
})();
```

------------------------------------------------------------------------

## 4. 전문가 관점에서 꼭 알아야 할 것들

-   **실행 컨텍스트(Execution Context)**\
    자바스크립트 코드가 실행될 때 생성되는 환경 (Variable Object, Scope
    Chain, this)
-   **이벤트 루프(Event Loop)**\
    JS의 비동기 실행 메커니즘 (Call Stack, Callback Queue, Microtask
    Queue)
-   **메모리 관리와 가비지 컬렉션(GC)**
-   **Immutable 패턴과 상태 관리 기법 (Redux 등과 연계)**
-   **성능 최적화 테크닉**
    -   Debounce, Throttle
    -   Lazy Loading, Tree Shaking

------------------------------------------------------------------------

## 결론

자바스크립트는 **ES5의 기초 개념**을 잘 이해하는 것이 중요하며, 이후
**ES6 이상의 최신 문법**과 **심화 개념(클로저, 프로토타입, 이벤트 루프
등)**을 이해해야 실무에서 진정한 전문가로 성장할 수 있습니다.\
이번 글에서 다룬 개념들을 기반으로 프로젝트에 직접 적용해보며 자신만의
테크닉으로 발전시키는 것을 권장합니다.

------------------------------------------------------------------------
