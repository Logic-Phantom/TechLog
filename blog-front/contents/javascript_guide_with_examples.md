---
date: '2025-09-10'
title: '자바스크립트 기본 문법부터 실무 활용까지 총정리'
categories: ['Web']
summary: '기본 부터 단단히'
thumbnail: './images/javascript/jsRule.png'
comments: true
---
# 자바스크립트 기본 문법부터 실무 활용까지 총정리 (ES5 버전)

## 1. 변수와 상수

-   **var**: 함수 스코프, 호이스팅 발생 → 주로 사용됨 (ES5에서는
    let/const 없음)

``` js
var count = 1;
var PI = 3.14;
```

------------------------------------------------------------------------

## 2. 자료형

-   기본형(Primitive): string, number, boolean, null, undefined
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
var arr = [1,2,3];
arr.push(4);   // [1,2,3,4]
arr.pop();     // [1,2,3]
arr.shift();   // [2,3]
arr.unshift(0);// [0,2,3]
```

### 특정 요소 제거 (filter)

``` js
var arr = [1,2,3,4];
var result = arr.filter(function(x){ return x !== 2; }); // [1,3,4]
```

💡 **실무 예제** 사용자 권한 목록에서 특정 권한 제거하기

``` js
var permissions = ["READ", "WRITE", "DELETE"];
var safePermissions = permissions.filter(function(p){ return p !== "DELETE"; });
// ["READ", "WRITE"]
```

### 중복 제거 (ES5에서는 직접 구현 필요)

``` js
var arr = [1,1,2,2,3];
var unique = [];
for(var i=0;i<arr.length;i++){
  if(unique.indexOf(arr[i]) === -1){
    unique.push(arr[i]);
  }
}
// [1,2,3]
```

### 배열 합치기

``` js
var a = [1,2];
var b = [3,4];
var merged = a.concat(b); // [1,2,3,4]
```

### 고급 활용: reduce

``` js
var sum = [1,2,3,4].reduce(function(acc,cur){ return acc+cur; }, 0); // 10
```

------------------------------------------------------------------------

## 4. 문자열 다루기

### 검색 및 대체

``` js
"hello world".indexOf("world"); // 6
"hello world".indexOf("hello") !== -1; // true
"hello world".replace("world", "JS"); // hello JS
```

💡 **실무 예제** 사용자 입력에서 불필요한 공백 제거 후 금칙어 필터링

``` js
var input = "  bad word ";
input = input.replace(/^\s+|\s+$/g,"").replace("bad","***"); // "*** word"
```

### 자르기

``` js
"apple,banana,cherry".split(","); // ["apple","banana","cherry"]
"javascript".slice(0,4); // "java"
```

------------------------------------------------------------------------

## 5. 함수

### 선언식 vs 표현식

``` js
function add(a,b){ return a+b; }
var sub = function(a,b){ return a-b; };
```

💡 **실무 예제** 콜백 함수 전달

``` js
var arr = [1,2,3];
arr.forEach(function(x){ console.log(x*2); });
```

### 화살표 함수 (ES5에서는 일반 함수 사용)

``` js
var mul = function(a,b){ return a*b; };
```

------------------------------------------------------------------------

## 6. 객체

### 선언 및 접근

``` js
var user = {name:"Tom", age:20};
user.name; // Tom
user["age"]; // 20
```

💡 **실무 예제** API 응답 데이터 파싱

``` js
var response = {id:1, profile:{name:"Alice"}};
var name = (response.profile && response.profile.name) ? response.profile.name : "Guest";
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
for(var i=0;i<5;i++) console.log(i);
for(var i=0;i<[1,2,3].length;i++) console.log([1,2,3][i]);
[1,2,3].forEach(function(x){ console.log(x); });
```

------------------------------------------------------------------------

## 8. 비동기 처리

### 콜백

``` js
setTimeout(function(){ console.log("done"); }, 1000);
```

### Promise/async는 ES6 이후 기능 → ES5에서는 콜백 패턴 주로 사용

``` js
function getUser(callback){
  var xhr = new XMLHttpRequest();
  xhr.open("GET","/api/user",true);
  xhr.onreadystatechange = function(){
    if(xhr.readyState===4){
      if(xhr.status===200){
        callback(null, JSON.parse(xhr.responseText));
      }else{
        callback("에러 발생");
      }
    }
  };
  xhr.send();
}
getUser(function(err,user){
  if(err) console.error(err);
  else console.log(user);
});
```

------------------------------------------------------------------------

## 9. 고급 활용

### 배열 메서드 체이닝

``` js
var result = [1,2,3,4,5]
  .filter(function(x){ return x%2===0; })
  .map(function(x){ return x*x; })
  .reduce(function(a,b){ return a+b; },0); // 20
```

------------------------------------------------------------------------

# 마무리

ES5에서는 최신 문법이 없으므로 가독성은 다소 떨어지지만, 콜백 패턴과
기본 배열/문자열 메서드만으로도 충분히 실무 개발이 가능합니다.
