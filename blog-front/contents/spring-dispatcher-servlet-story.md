---
date: '2025-07-07'
title: '🧵 Spring MVC 이야기'
categories: ['Web']
summary: 'DispatcherServlet이 들려주는 웹 요청 여정'
thumbnail: './images/web/SpringMVC.png'
comments: true
---
# 🧵 Spring MVC 이야기: DispatcherServlet이 들려주는 웹 요청 여정

> "어떤 요청이든 나를 거치지 않고는 지나갈 수 없지."  
> – DispatcherServlet

---

## 🌐 1. 사용자의 요청, 문을 두드리다

웹 브라우저에서 사용자가 주소창에 `/members/list`를 입력하고 엔터를 친다.  
이 요청은 웹 서버(Tomcat)에 도달하고, 톰캣은 설정된 `web.xml`이나 어노테이션을 통해 알아낸다.

> "이 요청은 스프링에게 맡기면 돼!"

그렇게 요청은 **`DispatcherServlet`**에게 전달된다.  
Spring MVC의 **프론트 컨트롤러**로, 모든 요청을 받아들여 분기 처리하는 핵심이다.

---

## 🧭 2. 길잡이를 찾아라: HandlerMapping

DispatcherServlet은 고민한다.

> "누가 이 요청을 처리할 수 있을까?"

그래서 먼저 **`HandlerMapping`**을 찾아간다.  
HandlerMapping은 요청 URL과 매핑된 **Controller 메서드(핸들러)** 를 찾아준다.

예를 들어, `/members/list` 요청에 대해 `MemberController.list()` 메서드가 매핑되어 있다고 알려준다.

> "요청에 맞는 컨트롤러 핸들러는 여기 있어요!"

---

## 🛠 3. 실행 도우미: HandlerAdapter

DispatcherServlet은 이제 실행만 하면 된다.  
하지만 직접 실행하지는 않고, 실행을 도와주는 **`HandlerAdapter`**에게 요청한다.

HandlerAdapter는 다양한 형태의 핸들러(예: `@Controller`, `@RestController`, `HttpRequestHandler` 등)를 처리할 수 있는 실행 전략을 알고 있다.

> "걱정 마, 내가 대신 핸들러 메서드를 실행해줄게."

그리고 드디어 사용자가 기대하던 **Controller의 메서드**가 실행된다!

---

## 🧪 4. 비즈니스 로직 실행과 Model 반환

`MemberController.list()`는 회원 목록을 조회하고  
Model에 담아 View 이름과 함께 반환한다:

```java
@RequestMapping("/members/list")
public String list(Model model) {
    List<Member> members = memberService.findAll();
    model.addAttribute("members", members);
    return "memberList";
}
```

반환값 `"memberList"`는 JSP나 Thymeleaf 같은 **뷰 이름**이다.  
하지만 아직 실제 화면은 아니다.

---

## 🧙‍♂️ 5. 화면 마법사: ViewResolver

DispatcherServlet은 "memberList"가 무슨 뜻인지 모른다.  
그래서 **`ViewResolver`**를 찾아간다.

ViewResolver는 설정을 바탕으로 View 이름을 **실제 파일 경로로 변환**한다.

> `"memberList"` → `/WEB-INF/views/memberList.jsp`

---

## 🖼 6. 마지막 무대: View 렌더링

이제 남은 건 최종 화면을 사용자에게 보여주는 일.  
DispatcherServlet은 View 객체에게 요청한다:

> "여기 모델 데이터와 함께 화면 좀 만들어줘!"

View는 모델 데이터를 바탕으로 HTML을 렌더링하고,  
그 결과를 사용자 브라우저로 전송한다.

---

## 🧩 전체 흐름 요약

```text
[1] 클라이언트 요청
     ↓
[2] DispatcherServlet 수신
     ↓
[3] HandlerMapping → 핸들러 탐색
     ↓
[4] HandlerAdapter → 핸들러 실행
     ↓
[5] Controller → Model & View 이름 반환
     ↓
[6] ViewResolver → View 객체 생성
     ↓
[7] View 렌더링 → 응답 전송
```

---

## 📌 마무리: DispatcherServlet의 말

> "내가 있기에 Spring MVC는 깔끔하게 흘러간다.  
> 모든 요청은 나를 통하고, 모든 응답도 내가 책임진다."

Spring의 설계는 복잡한 요청 처리를 명확한 체계로 나누어, 유지보수와 확장성까지 고려한 구조로 되어 있다.  
Spring MVC의 요청 흐름을 이해한다면, **스프링의 세계를 제대로 이해한 것**과 같다.

---

## 📚 참고 키워드 정리

| 개념              | 역할 설명 |
|------------------|-----------------------------|
| DispatcherServlet | 요청을 받아 처리 흐름을 제어하는 프론트 컨트롤러 |
| HandlerMapping    | 요청 URL에 대응되는 컨트롤러(핸들러)를 찾음 |
| HandlerAdapter    | 핸들러 실행을 담당하는 어댑터 |
| Controller        | 비즈니스 로직 수행 및 모델 데이터 반환 |
| ViewResolver      | 논리적 뷰 이름을 실제 뷰(JSP 등)로 변환 |
| View              | 모델 데이터를 HTML로 렌더링하는 객체 |