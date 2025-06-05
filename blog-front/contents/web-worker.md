---
date: '2025-06-05'
title: ' 웹 워커(Web Worker) 완벽 가이드'
categories: ['web']
summary: '브라우저의 메인 스레드가 숨통이 트이는 순간'
thumbnail: './images/web/web-worker.png'
comments: true
---

# 웹 워커(Web Worker) 완벽 가이드

> 브라우저의 메인 스레드가 숨통이 트이는 순간

## 🔍 웹 워커란?

웹 워커(Web Worker)는 **웹 애플리케이션에서 스레드를 백그라운드로 분리하여 실행**할 수 있게 해주는 브라우저 API입니다. 자바스크립트는 기본적으로 싱글 스레드이기 때문에 무거운 연산이 메인 스레드를 막아 UI가 멈추거나 렌더링이 지연되는 문제가 발생할 수 있습니다. 이런 상황에서 웹 워커를 활용하면 **메인 스레드와 별개로 비동기 처리를 수행**할 수 있습니다.

## 🧠 웹 워커의 구조

웹 워커는 기본적으로 다음과 같은 구조로 동작합니다:

1. **메인 스레드에서 워커 생성**
2. **워커 파일은 별도의 JS 파일**로 존재해야 함
3. **`postMessage`를 통해 데이터 전송 및 수신**
4. **워커는 `onmessage` 핸들러로 메시지 수신**

```javascript
// main.js
const worker = new Worker("worker.js");
worker.postMessage({ value: 100 });
worker.onmessage = (e) => {
  console.log("워커 결과:", e.data);
};

// worker.js
onmessage = function (e) {
  const result = e.data.value * 2;
  postMessage(result);
};
```

## ⚙️ 종류

### 1. Dedicated Worker
- 단일 스레드와 1:1 연결 (한 페이지 전용)

### 2. Shared Worker
- 여러 브라우저 탭에서 공유 가능

### 3. Service Worker
- 네트워크 요청 캐싱, 오프라인 지원 등에 활용 (PWA 등)

## 🛠️ 활용 사례

### 🎨 1. 이미지/비디오 프로세싱
- 필터, 썸네일 생성 등 무거운 연산을 백그라운드에서 처리

### 🔍 2. 대용량 데이터 처리
- 예: CSV 파싱, 대규모 JSON 가공

### 🧬 3. 머신러닝 / WebAssembly 연동
- TensorFlow.js나 WASM과 함께 사용하면 성능을 극대화할 수 있음

### 📊 4. 실시간 데이터 분석
- 주식, IoT 센서 등 실시간으로 들어오는 데이터를 웹 워커가 분석

## ✅ 장점

- 🧵 UI 스레드와 분리되어 렌더링 끊김 최소화
- ⚡ CPU 집중 작업을 백그라운드에서 처리 가능
- 🔄 데이터 전송은 직렬화되어 안정적

## ⚠️ 단점 및 주의사항

- 📁 워커는 별도 파일로 존재해야 하며 **DOM 접근 불가**
- 🚫 LocalStorage, Window, Document 등의 객체 사용 불가
- 🧪 디버깅이 어렵고, 네트워크 로깅 등에서도 제외될 수 있음
- 📦 번들러 설정이 까다로울 수 있음 (Webpack, Vite 등)

## 🧪 팁: 웹 워커 성능 최적화

- 워커가 너무 많이 생성되면 오히려 브라우저 성능 저하
- 데이터 전송량은 최소화 (postMessage는 복사됨)
- `transferable objects`를 활용해 복사 대신 메모리 이동 가능

```javascript
const buffer = new ArrayBuffer(1024);
worker.postMessage(buffer, [buffer]); // 복사 대신 참조 이전
```

## 🚀 결론

웹 워커는 브라우저 환경에서도 멀티스레드처럼 병렬 처리를 가능하게 해주는 강력한 기능입니다. UI와 별도로 처리해야 할 무거운 연산이 있다면 적극적으로 활용해보세요. 사용자 경험을 개선하는 동시에 성능도 확보할 수 있습니다.

---

## 📚 참고 자료
- [MDN Web Docs - Web Workers](https://developer.mozilla.org/ko/docs/Web/API/Web_Workers_API)
- [Google Developers - Using Web Workers](https://developers.google.com/web/updates/2018/10/audio-worklet)

---

