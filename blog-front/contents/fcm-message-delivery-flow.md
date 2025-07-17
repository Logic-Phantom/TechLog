---
date: '2025-07-17'
title: '🔔 FCM 메시지가 사용자에게 도달하기까지'
categories: ['Web']
summary: 'Firebase Cloud Messaging(Firebase Server → 브라우저/디바이스까지)의 작동'
thumbnail: './images/web/FcmAlert.png'
comments: true
---

> 사용자의 디바이스에 "띵!"하고 알림이 도착하기까지, 그 이면에서는 어떤 일이 벌어지고 있을까?

---

## 🧩 서론: 그날의 푸시 알림

2025년 어느 날, 회사 서비스에서 이벤트 알림을 푸시로 날리기로 결정했다.  
우리 백엔드 팀의 역할은 단순했다.

- "사용자에게 메시지를 보내라!"

하지만, 메시지는 '어떻게' 사용자에게 전달되는 걸까?  
Firebase Cloud Messaging(이하 FCM)을 사용하고 있었지만,  
그 흐름을 제대로 이해한 건 이번이 처음이었다.

---

## 🌐 1. 전체 아키텍처 개요

```plaintext
[내 서버] ──▶ [FCM Server] ──▶ [사용자 디바이스 (웹/앱)] ──▶ [알림 표시]
                 ▲                          ▲
                 │                          │
           인증/토큰 관리               Service Worker
```

---

## 2️⃣ Step-by-Step 흐름: 알림이 만들어지고 전달되기까지

### 1단계: 클라이언트가 Firebase와 연결하고 등록 토큰을 발급받다

웹 또는 앱에서 다음 과정을 거친다:

1. Firebase SDK 초기화 (firebase-messaging.js)
2. 사용자에게 알림 권한 요청
3. 권한 허용 시, FCM은 "registration token"을 발급
4. 이 토큰을 **내 서버에 저장**해둠

```js
// Web 예시
const messaging = firebase.messaging();

const token = await messaging.getToken({
  vapidKey: 'YOUR_PUBLIC_VAPID_KEY',
});
```

👉 이 `token`은 사용자의 디바이스를 식별하는 유일한 키다.

---

### 2단계: 서버에서 메시지를 만들고 FCM에 전달

서버 측에서는 REST API를 통해 메시지를 전송한다.

```http
POST https://fcm.googleapis.com/v1/projects/{project-id}/messages:send
Authorization: Bearer {access_token}
Content-Type: application/json
```

요청 바디 예시:

```json
{
  "message": {
    "token": "user_device_token",
    "notification": {
      "title": "새 소식!",
      "body": "당신을 위한 새로운 이벤트가 도착했어요."
    },
    "data": {
      "url": "/event/detail"
    }
  }
}
```

✅ `notification`은 브라우저에서 자동 알림 생성  
✅ `data`는 개발자가 수동 처리 가능

---

### 3단계: Firebase가 사용자 디바이스로 푸시 전달

- Firebase는 등록된 `token`을 통해 디바이스와 연결
- 메시지를 Web Push 프로토콜 또는 Android/iOS 전용 채널을 통해 전송

🧠 이때까지의 흐름:
```plaintext
[Server] → [FCM] → [Push Service] → [사용자 브라우저]
```

---

### 4단계: 브라우저 백그라운드에서 Service Worker가 메시지 수신

브라우저가 꺼지지 않고 백그라운드에서 살아있다면,  
`firebase-messaging-sw.js` 또는 custom `service-worker.js`가 메시지를 받는다.

```js
// firebase-messaging-sw.js
self.addEventListener('push', function (event) {
  const payload = event.data.json();
  self.registration.showNotification(payload.notification.title, {
    body: payload.notification.body,
    icon: '/icon.png',
    data: payload.data,
  });
});
```

🧩 알림 표시 후 클릭 시, 특정 URL로 이동하거나 액션 처리 가능

---

## 🎯 흐름 요약 다이어그램

```plaintext
(1) 클라이언트가 FCM 토큰 발급
        ↓
(2) 서버가 메시지를 생성
        ↓
(3) FCM 서버로 메시지 전송
        ↓
(4) FCM이 대상 디바이스로 Push
        ↓
(5) Service Worker가 수신 후 알림 표시
        ↓
(6) 사용자가 알림 클릭 (→ 웹 페이지 이동 등)
```

---

## ❗️주의할 점

- **알림 권한은 수동 허용이 필요** (특히 브라우저에서)
- **브라우저가 꺼져 있으면 수신 불가**
  - 크롬의 경우 브라우저 프로세스가 종료되면 푸시 수신 실패
  - 반면, Edge 또는 PWA 설치 시 OS 백그라운드 유지로 수신 가능
- **token 유효성 관리** 중요
  - 오래된 token은 유효하지 않으므로 주기적 재발급 필요

---

## 🔍 실제 활용 팁

- 모바일 웹 앱이라면 PWA로 설치 유도 → 푸시 수신 안정성 증가
- 사용자 그룹에 따라 topic 메시지 사용 가능 (`/topics/news`)
- 사용자 액션에 따라 알림 전송: 예약, 뉴스, 댓글, 좋아요 등

---

## 🧠 마무리하며

"그냥 알림 보내는 거잖아."  
그렇게 생각했지만, 실제로는 꽤 섬세한 흐름과 관리가 필요한 영역이었다.

Firebase 덕분에 푸시는 쉬워졌지만,  
**어디서 누가 어떤 흐름으로 받는지를 파악**해야  
실제로 **사용자 경험을 개선하는 알림**을 만들 수 있다.

---

> 푸시는 기술이 아니라 연결이다.  
> 알림 하나에도 수많은 기술자들의 고민과 흐름이 숨어 있다.
