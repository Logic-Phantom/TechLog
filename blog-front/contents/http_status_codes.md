---
date: '2025-06-13'
title: 'HTTP 상태 코드 완벽 정리'
categories: ['web']
summary: '응답 코드에 대하여'
thumbnail: './images/web/httpStatus.png'
comments: true
---
# 🌐 HTTP 상태 코드 완벽 정리

HTTP 상태 코드는 클라이언트가 서버에 요청(Request)을 보냈을 때, 서버가 그 요청에 대해 어떤 상태(Status)인지를 숫자로 알려주는 응답 코드(Response Code)입니다. 이 코드는 **3자리 숫자**로 구성되며, 각 자릿수에 따라 의미가 달라집니다.

---

## 🔢 상태 코드 범주

| 범위 | 의미 | 예시 | 설명 |
|------|------|------|------|
| **1xx** | 정보 (Informational) | 100, 101 | 요청을 받았고, 계속 처리 중 |
| **2xx** | 성공 (Success) | 200, 201 | 요청이 성공적으로 처리됨 |
| **3xx** | 리다이렉션 (Redirection) | 301, 302 | 요청 완료를 위해 추가 동작 필요 |
| **4xx** | 클라이언트 오류 (Client Error) | 400, 404 | 클라이언트 요청에 오류 발생 |
| **5xx** | 서버 오류 (Server Error) | 500, 503 | 서버가 요청 처리 실패 |

---

## ✅ 2xx: 성공 응답

- **200 OK**  
  요청이 정상적으로 처리되었음을 의미.

- **201 Created**  
  POST 요청을 통해 리소스가 성공적으로 생성됨.

- **204 No Content**  
  요청은 성공했지만 반환할 데이터가 없음.

---

## 🔁 3xx: 리다이렉션

- **301 Moved Permanently**  
  요청한 리소스가 영구적으로 다른 URL로 이동함.

- **302 Found**  
  일시적으로 다른 URL로 이동됨.

- **304 Not Modified**  
  리소스가 수정되지 않았으므로 클라이언트는 로컬 캐시를 사용할 수 있음.

---

## ⚠️ 4xx: 클라이언트 오류

- **400 Bad Request**  
  잘못된 문법 또는 유효하지 않은 요청.

- **401 Unauthorized**  
  인증이 필요함.

- **403 Forbidden**  
  서버가 요청을 이해했지만, 권한이 없어 접근 거부됨.

- **404 Not Found**  
  요청한 리소스를 찾을 수 없음.

- **405 Method Not Allowed**  
  요청에서 사용한 HTTP 메서드가 허용되지 않음.

- **429 Too Many Requests**  
  너무 많은 요청을 보냄.

---

## 💥 5xx: 서버 오류

- **500 Internal Server Error**  
  서버 내부 오류.

- **502 Bad Gateway**  
  프록시 서버가 잘못된 응답을 받음.

- **503 Service Unavailable**  
  서버가 일시적으로 요청을 처리할 수 없음.

- **504 Gateway Timeout**  
  응답을 기다리다 시간 초과됨.

---

## 🛠️ 개발 실무 팁

- 2xx 응답에는 데이터 or 성공 메시지를 포함
- 4xx는 사용자 입력 오류 등 사용자에게 안내
- 5xx는 서버 로그 필수 확인 + 클라이언트에 상세 노출은 지양
- RESTful API를 위해 상태 코드에 맞는 응답 처리 필요

---

## 📝 결론

HTTP 상태 코드는 단순한 숫자 이상의 의미를 지닙니다. 각각의 코드가 갖는 의미를 명확히 알고 있다면, API 설계, 디버깅, 보안 처리에 있어서 큰 도움이 됩니다.

---

## ✨ 참고용 표

| 상태 코드 | 의미 | 설명 |
|-----------|------|------|
| 200 | OK | 요청 성공 |
| 201 | Created | 리소스 생성 |
| 204 | No Content | 응답 본문 없음 |
| 301 | Moved Permanently | 영구 이동 |
| 302 | Found | 일시 이동 |
| 400 | Bad Request | 잘못된 요청 |
| 401 | Unauthorized | 인증 필요 |
| 403 | Forbidden | 접근 거부 |
| 404 | Not Found | 찾을 수 없음 |
| 500 | Internal Server Error | 서버 오류 |
| 503 | Service Unavailable | 서비스 불가 |
