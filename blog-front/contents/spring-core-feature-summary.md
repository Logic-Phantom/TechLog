---
date: '2025-07-04'
title: '스프링 프레임워크의 핵심 기능'
categories: ['Web']
summary: '봄이 왔구나...'
thumbnail: './images/web/SpringFun.png'
comments: true
---
# 🌿 Spring Framework 핵심 기능 정리  
> 실무에서 자주 사용되는 기능과 설정 방법을 한눈에!

---

## 🧼 Filter (javax.servlet.Filter)

### 📌 개요
- 서블릿 컨테이너 수준에서 HTTP 요청/응답을 가로채 처리하는 기능
- 인증, 인코딩, 로깅 등에 사용

### 🛠️ 설정 방법 (Spring Boot 기준)

```java
@Component
public class LoggingFilter implements Filter {
    @Override
    public void doFilter(ServletRequest request, ServletResponse response, FilterChain chain)
        throws IOException, ServletException {
        HttpServletRequest req = (HttpServletRequest) request;
        System.out.println("Request URI: " + req.getRequestURI());
        chain.doFilter(request, response);
    }
}
```

### ✅ 특징
- DispatcherServlet 이전에 실행
- 전역 필터로 작동

---

## 🧭 Interceptor (HandlerInterceptor)

### 📌 개요
- Spring MVC에서 DispatcherServlet 이후 Controller 실행 전/후에 동작
- 인증/권한 처리, 로깅, 사용자 행위 추적 등에 적합

### 🛠️ 설정 방법

```java
public class AuthInterceptor implements HandlerInterceptor {
    @Override
    public boolean preHandle(HttpServletRequest request, HttpServletResponse response, Object handler)
        throws Exception {
        System.out.println("Interceptor 실행: " + request.getRequestURI());
        return true;
    }
}
```

```java
@Configuration
public class WebConfig implements WebMvcConfigurer {
    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(new AuthInterceptor()).addPathPatterns("/api/**");
    }
}
```

### ✅ 특징
- 특정 URL 패턴 지정 가능
- Controller와 밀접하게 동작

---

## ⚙️ AOP (Aspect-Oriented Programming)

### 📌 개요
- 핵심 비즈니스 로직 외에 반복적으로 발생하는 **공통 관심사(Cross-Cutting Concern)** 를 모듈화
- 로깅, 트랜잭션, 보안 등의 공통 처리에 사용

### 🛠️ 의존성 추가 (Spring Boot)

```xml
<dependency>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-aop</artifactId>
</dependency>
```

### ✏️ 예제 코드

```java
@Aspect
@Component
public class LoggingAspect {
    @Before("execution(* com.example.service.*.*(..))")
    public void logBefore(JoinPoint joinPoint) {
        System.out.println("호출 전: " + joinPoint.getSignature().getName());
    }
}
```

### ✅ 특징
- `@Aspect` 어노테이션 사용
- JoinPoint, Pointcut 등 AOP 용어 이해 필요

---

## 🧷 @RestController

### 📌 개요
- `@Controller + @ResponseBody`의 축약형
- JSON 기반 REST API 개발에 사용

### 🛠️ 사용 예

```java
@RestController
@RequestMapping("/api")
public class ApiController {

    @GetMapping("/hello")
    public String hello() {
        return "Hello, World!";
    }
}
```

### ✅ 특징
- 템플릿(View) 없이 JSON 응답
- API 서버 구현에 필수

---

## 🔖 사용자 정의 어노테이션 (Custom Annotation)

### 📌 개요
- 반복되는 설정/검사를 직접 어노테이션으로 선언해 처리
- 보통 AOP와 함께 사용

### ✏️ 어노테이션 정의

```java
@Target(ElementType.METHOD)
@Retention(RetentionPolicy.RUNTIME)
public @interface CheckAuth {
}
```

### ✏️ Aspect 처리

```java
@Aspect
@Component
public class AuthAspect {
    @Before("@annotation(CheckAuth)")
    public void check() {
        // 인증 처리
        System.out.println("인증 검사 수행");
    }
}
```

---

## 📎 @Component vs @Service vs @Repository

| 어노테이션   | 설명                             |
|--------------|----------------------------------|
| `@Component` | 모든 스프링 Bean의 기본 어노테이션 |
| `@Service`   | 비즈니스 로직을 담는 클래스에 사용 |
| `@Repository`| DAO 클래스에 사용 (예외 변환 포함)  |

---

## ✅ 핵심 요약

| 기능          | 동작 위치                  | 주 사용 목적               |
|---------------|----------------------------|----------------------------|
| Filter        | 서블릿 컨테이너 수준        | 보안, 인코딩, 로깅         |
| Interceptor   | DispatcherServlet 이후      | 인증, 권한, 요청 검사      |
| AOP           | 메서드 호출 전후            | 공통 로직 분리(로깅, 트랜잭션 등) |
| RestController| REST API 처리               | JSON 응답 제공             |
| Custom Annotation | 선언형 개발               | 코드 가독성 및 재사용성 향상 |

---

_🔍 이 문서는 Spring/Spring Boot 개발에서 자주 사용되는 핵심 기능들을 중심으로 정리되었습니다. 실무/학습/기능 비교 시 참고하시기 바랍니다._
