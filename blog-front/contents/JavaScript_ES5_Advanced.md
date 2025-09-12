---
date: '2025-09-12'
title: 'JavaScript ES5 고급 문법, 스킬, 아키텍처 총정리'
categories: ['Web']
summary: 'JavaScript 이해'
thumbnail: './images/javascript/jsRead.png'
comments: true
---
# JavaScript ES5 고급 문법, 스킬, 아키텍처 총정리

JavaScript는 웹 개발의 핵심 언어로, ES5(ECMAScript 5) 기준에서도 고급 문법과 스킬, 아키텍처 설계 원칙을 이해하는 것이 중요합니다. 이 글에서는 ES5 기반 JavaScript의 **기본부터 심화**, **전문가 레벨의 활용**까지 정리합니다.

---

## 1. ES5 JavaScript 기본

### 1.1 변수 선언
ES5에서는 `var`만 존재하며, 함수 레벨 스코프(function scope)를 갖습니다.

```javascript
var name = "ChatGPT";
function greet() {
    var name = "User";
    console.log(name); // "User"
}
console.log(name); // "ChatGPT"
```

### 1.2 데이터 타입과 타입 변환
- 기본형: `String`, `Number`, `Boolean`, `Null`, `Undefined`
- 객체형: `Object`, `Array`, `Function`, `Date`, `RegExp`

```javascript
var num = "123";
var converted = Number(num); // 123
var bool = Boolean(0); // false
```

### 1.3 함수
ES5에서는 함수 선언식, 함수 표현식, 익명 함수, 즉시 실행 함수(IIFE)를 사용할 수 있습니다.

```javascript
// 함수 선언식
function sum(a, b) {
    return a + b;
}

// 함수 표현식
var multiply = function(a, b) {
    return a * b;
};

// IIFE
(function(){
    console.log("즉시 실행 함수");
})();
```

---

## 2. 객체와 프로토타입 기반 상속

### 2.1 객체 생성
```javascript
var person = {
    name: "Alice",
    greet: function() {
        console.log("Hello, " + this.name);
    }
};
person.greet();
```

### 2.2 생성자 함수와 프로토타입
ES5에서는 클래스가 없으므로, 생성자 함수와 프로토타입을 사용하여 상속과 메서드 공유를 합니다.

```javascript
function Person(name, age) {
    this.name = name;
    this.age = age;
}

Person.prototype.greet = function() {
    console.log("Hi, I'm " + this.name);
};

var alice = new Person("Alice", 30);
alice.greet(); // Hi, I'm Alice
```

### 2.3 상속 구현
```javascript
function Employee(name, age, role) {
    Person.call(this, name, age); // 부모 생성자 호출
    this.role = role;
}

Employee.prototype = Object.create(Person.prototype);
Employee.prototype.constructor = Employee;

var bob = new Employee("Bob", 25, "Developer");
bob.greet(); // Hi, I'm Bob
```

---

## 3. 고급 ES5 문법

### 3.1 클로저(Closure)
함수와 그 함수가 선언된 렉시컬 환경을 기억하는 패턴입니다.

```javascript
function makeCounter() {
    var count = 0;
    return function() {
        count++;
        return count;
    };
}

var counter = makeCounter();
console.log(counter()); // 1
console.log(counter()); // 2
```

### 3.2 즉시 실행 함수 패턴(IIFE)
모듈화, 변수 은닉화에 사용됩니다.

```javascript
var module = (function() {
    var privateVar = "비공개";
    return {
        getPrivate: function() {
            return privateVar;
        }
    };
})();
console.log(module.getPrivate()); // 비공개
```

### 3.3 함수형 패턴
- `map`, `filter`, `reduce` 등의 고차함수 활용
- ES5는 `Array.prototype`에 존재

```javascript
var numbers = [1,2,3,4,5];
var doubled = numbers.map(function(n){ return n*2; });
var evens = numbers.filter(function(n){ return n%2===0; });
var sum = numbers.reduce(function(acc, n){ return acc+n; }, 0);
```

### 3.4 this와 바인딩
- `call`, `apply`, `bind`로 함수의 `this` 컨텍스트 제어

```javascript
function say(greeting) {
    console.log(greeting + ", " + this.name);
}
var obj = {name: "Alice"};
say.call(obj, "Hello"); // Hello, Alice
say.apply(obj, ["Hi"]); // Hi, Alice
var bound = say.bind(obj);
bound("Hey"); // Hey, Alice
```

---

## 4. ES5 스킬 & 디자인 패턴

### 4.1 모듈 패턴(Module Pattern)
전역 변수 오염 방지, 캡슐화

```javascript
var myModule = (function(){
    var privateVar = 0;
    function privateFunc() { return ++privateVar; }
    return {
        increment: privateFunc
    };
})();
console.log(myModule.increment()); // 1
```

### 4.2 싱글톤 패턴(Singleton Pattern)
전역 상태 관리에 사용

```javascript
var singleton = (function(){
    var instance;
    function create() {
        return { id: Math.random() };
    }
    return {
        getInstance: function() {
            if(!instance) instance = create();
            return instance;
        }
    };
})();
console.log(singleton.getInstance());
console.log(singleton.getInstance()); // 동일한 인스턴스
```

### 4.3 관찰자 패턴(Observer Pattern)
데이터 변화 감지, 이벤트 기반 아키텍처

```javascript
function Subject() {
    this.observers = [];
}
Subject.prototype.subscribe = function(fn) {
    this.observers.push(fn);
};
Subject.prototype.notify = function(data) {
    this.observers.forEach(function(fn){ fn(data); });
};

var subject = new Subject();
subject.subscribe(function(data){ console.log("Observer1:", data); });
subject.notify("Hello Observers"); // Observer1: Hello Observers
```

### 4.4 커링(Currying)
함수 분할로 재사용성을 높임

```javascript
function multiply(a) {
    return function(b) {
        return a * b;
    };
}
var double = multiply(2);
console.log(double(5)); // 10
```

---

## 5. ES5 아키텍처 & 고급 설계

### 5.1 모듈화 전략
- IIFE, Revealing Module Pattern, AMD, CommonJS
- 전역 변수 최소화, 책임 분리

### 5.2 MVC / MV* 구조
- JavaScript만으로도 간단한 MVC 구현 가능
- View와 Model 간 이벤트 바인딩

```javascript
// Model
var model = {
    data: 0,
    increment: function(){ this.data++; }
};

// View
function render(){
    console.log("Value:", model.data);
}

// Controller
function update(){
    model.increment();
    render();
}

update(); // Value: 1
update(); // Value: 2
```

### 5.3 이벤트 중심 아키텍처
- Pub/Sub 패턴
- 모듈 간 결합도 감소

### 5.4 메모리 관리 & 성능 팁
- 클로저 남용 주의 (메모리 누수 위험)
- 이벤트 리스너 제거
- DOM 조작 최소화
- 반복문 최적화 (`for` vs `forEach` vs `while`)

---

## 6. 전문가용 트릭과 패턴

### 6.1 함수 데코레이터
- 기존 함수 확장

```javascript
function logDecorator(fn) {
    return function(){
        console.log("Before function");
        var result = fn.apply(this, arguments);
        console.log("After function");
        return result;
    };
}

function greet(name){ console.log("Hello " + name); }
var decorated = logDecorator(greet);
decorated("Alice");
```

### 6.2 메서드 체이닝
```javascript
function Chain(){
    this.value = 0;
}
Chain.prototype.add = function(x){ this.value+=x; return this; };
Chain.prototype.multiply = function(x){ this.value*=x; return this; };
var result = new Chain().add(5).multiply(2).value; // 10
```

### 6.3 ES5 기반 유틸리티 함수
- `extend`, `clone`, `merge` 등 재사용 함수
```javascript
function extend(target, source){
    for(var key in source){
        if(source.hasOwnProperty(key)){
            target[key] = source[key];
        }
    }
    return target;
}
```

---

## 7. 마무리

ES5 기준에서도 **클로저, IIFE, 프로토타입 상속, 디자인 패턴** 등을 활용하면 구조적이고 유지보수 가능한 JavaScript 코드를 작성할 수 있습니다.  
심화적으로는 **모듈화, 이벤트 중심 아키텍처, 퍼포먼스 최적화**까지 고려해야 합니다.

---

> ✅ **핵심 요약**
> - ES5는 `var`, 함수, 프로토타입 기반
> - 클로저와 IIFE는 캡슐화와 모듈화 핵심
> - 디자인 패턴: 싱글톤, 모듈, Observer, 커링
> - 아키텍처: MVC, 이벤트 중심, 메모리 최적화
> - ES6+ 기능이 없는 환경에서도 충분히 고급 구조 구현 가능
