---
date: '2025-07-03'
title: '스프링 프레임워크 vs 스프링 부트'
categories: ['Web']
summary: '나라도 스프링부트 쓴다'
thumbnail: './images/web/Spring.png'
comments: true
---
# ☕ 스프링 프레임워크 vs 스프링 부트: 왜 부트를 쓰게 되었을까?

기술 블로그를 운영하면서 나는 종종 과거 프로젝트를 되돌아본다.  
특히 Java 백엔드 개발을 처음 시작했을 때 **Spring Framework**와 **Spring Boot**의 차이를 몰라 많이 헤맸던 기억이 있다.

이번 글에서는 "왜 우리는 스프링 부트를 쓰게 되었는가?"를 나의 경험과 함께 정리해보려고 한다.

---

## 🏗️ 그때 그 시절: XML의 숲을 헤치며

처음 맡았던 프로젝트는 구식(?) 스프링 프레임워크 기반이었다.  
그땐 모든 설정을 **XML로 작성**했었다.

```xml
<!-- applicationContext.xml -->
<bean id="userService" class="com.example.service.UserServiceImpl">
    <property name="userRepository" ref="userRepository"/>
</bean>
```

Bean 정의, 트랜잭션 설정, AOP, 데이터소스 설정까지…  
**10개가 넘는 XML 파일**이 존재했고, 설정만 하다가 하루가 지나갔다.

당시엔 몰랐다. 이게 얼마나 비효율적인지를.

---

## 🧪 테스트 코드? 설정하다 지친다…

단위 테스트 하나 돌리려고 하면 최소한 5개 설정 파일을 로딩해야 했고,  
컨트롤러를 만들고도 **서버 구동만 2~3분씩 걸렸다**.

Spring 자체는 잘 만들었지만, **입문자에게는 너무 친절하지 않았다.**

---

## 🚀 스프링 부트를 만나다: “진짜 이게 다예요?”

이후 새로운 프로젝트에서 드디어 `Spring Boot`를 접하게 된다.

```java
@SpringBootApplication
public class MyApp {
    public static void main(String[] args) {
        SpringApplication.run(MyApp.class, args);
    }
}
```

나는 놀랐다.  
“**application.properties** 하나로 설정이 끝났다고?”  
“**임베디드 톰캣이 내장**되어 있다고?”

게다가 `@RestController`, `@Service`, `@Repository` 등 어노테이션 기반의 자동 설정은 신세계였다.

---

## 📦 스프링 부트가 가져온 변화

| 항목 | 스프링 프레임워크 | 스프링 부트 |
|------|------------------|--------------|
| 설정 방식 | 수동 (XML, Java Config) | 자동 (Auto Configuration) |
| 서버 | 외부 톰캣 필요 | 내장 톰캣 제공 |
| 의존성 관리 | 직접 설정 | 스타터 패키지 제공 |
| 실행 방법 | WAR 빌드 후 배포 | `java -jar`로 실행 |
| 학습 곡선 | 가파름 | 상대적으로 완만 |

---

## 🔍 왜 스프링 부트를 선택하게 되었을까?

- **생산성**: 바로 개발 시작 가능. `starter-web`, `starter-jpa` 등 스타터 패키지로 복잡도 감소.
- **간결성**: 설정이 간단. YAML 또는 properties 하나로 대부분 해결.
- **유지보수**: 팀원이 바뀌어도 빠르게 적응 가능.
- **테스트 용이성**: `@SpringBootTest` 하나로 거의 모든 테스트 환경 구성.

---

## 🧠 정리하며: 프레임워크 그 이상의 프레임워크

사실 `Spring Boot`는 **Spring Framework 위에 구축된 것**이다.  
그래서 “Spring Boot는 Spring의 하위 개념인가요?”라는 질문은 반은 맞고 반은 틀렸다.

정확히 말하면,  
> 스프링 부트는 스프링 프레임워크를 **더 쉽게 사용하기 위한 ‘런처’이자 ‘편의 도구’**이다.

---

## 📌 참고로 알아두면 좋은 정보들

- `@SpringBootApplication`은 사실 `@Configuration + @EnableAutoConfiguration + @ComponentScan`의 조합이다.
- Spring Boot는 정해진 **디렉토리 구조**와 **의존성 버전 조율 BOM(Bill of Materials)**을 갖고 있어 협업에 유리하다.
- 3.0 이후부터는 **Spring Boot + Virtual Threads** 조합도 주목받고 있다.

---

## 🪄 나의 선택은?

만약 지금 새로운 프로젝트를 시작한다면?  
**Spring Boot**를 선택할 것이다.  
그건 내가 게을러서가 아니라, **효율적이고 싶기 때문**이다.

물론, Spring Framework의 동작 원리를 이해하는 것은 여전히 중요하다.  
Spring Boot를 다루더라도 결국 그 기반은 순수한 Spring이기 때문이다.

---

## 🙋‍♂️ 당신은 지금 어떤 선택을 하고 있는가?

