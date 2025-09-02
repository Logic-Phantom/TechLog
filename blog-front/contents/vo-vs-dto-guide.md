---
date: '2025-09-02'
title: 'VO와 DTO 개념 심층 가이드'
categories: ['Web','Server']
summary: '데이터 구조 정의 및 전달 방식'
thumbnail: './images/web/voDto.png'
comments: true
---
# VO와 DTO 개념 심층 가이드

## 1. 들어가며

백엔드 개발에서 데이터 구조를 정의하고 전달하는 방식은 매우 중요합니다.
특히 **VO(Value Object)** 와 **DTO(Data Transfer Object)** 는 자주
사용되는 개념으로, 소프트웨어 아키텍처의 품질과 유지보수성에 큰 영향을
줍니다.

이 문서에서는 VO와 DTO의 기초 개념부터 실무 적용 사례, 그리고 전문가적
관점에서의 활용 방안까지 단계적으로 설명합니다.

------------------------------------------------------------------------

## 2. VO(Value Object)

### 2.1 개념

-   **정의**: VO는 *값을 표현하기 위한 객체*로, 특정 도메인의 속성을
    불변(Immutable)하게 표현합니다.
-   **특징**
    -   동일성(Identity)이 아닌 **동등성(Equality)** 로 비교합니다.
    -   값이 같으면 같은 객체로 취급합니다.
    -   변경 불가능(Immutable)한 성격을 가집니다.

### 2.2 예시 (Java)

``` java
public class Money {
    private final int amount;
    private final String currency;

    public Money(int amount, String currency) {
        this.amount = amount;
        this.currency = currency;
    }

    public int getAmount() { return amount; }
    public String getCurrency() { return currency; }

    @Override
    public boolean equals(Object o) {
        if (this == o) return true;
        if (!(o instanceof Money)) return false;
        Money money = (Money) o;
        return amount == money.amount && currency.equals(money.currency);
    }

    @Override
    public int hashCode() {
        return Objects.hash(amount, currency);
    }
}
```

여기서 `Money` 객체는 금액과 통화를 나타내는 **VO**이며, 값이 동일하면
같은 객체로 취급합니다.

### 2.3 장점

-   불변성을 통한 안정성 확보
-   도메인 개념을 코드로 명확하게 표현
-   값 기반 비교로 직관적인 동등성 판단 가능

------------------------------------------------------------------------

## 3. DTO(Data Transfer Object)

### 3.1 개념

-   **정의**: DTO는 *데이터 전송을 위한 객체*로, 계층 간 데이터 교환에
    사용됩니다.
-   **특징**
    -   보통 **getter/setter** 를 가짐
    -   직렬화/역직렬화에 용이
    -   비즈니스 로직을 포함하지 않음

### 3.2 예시 (Java)

``` java
public class UserDTO {
    private String name;
    private String email;

    public UserDTO() {}

    public UserDTO(String name, String email) {
        this.name = name;
        this.email = email;
    }

    public String getName() { return name; }
    public void setName(String name) { this.name = name; }

    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
}
```

`UserDTO`는 컨트롤러와 서비스 계층, 혹은 API 통신에서 데이터를 담아
전달하는 용도로 사용됩니다.

### 3.3 장점

-   계층 간 데이터 교환 단순화
-   네트워크 전송 최적화 (필요한 데이터만 포함 가능)
-   보안 강화 (민감한 엔티티 정보 노출 방지)

------------------------------------------------------------------------

## 4. VO vs DTO 비교

  구분             VO (Value Object)       DTO (Data Transfer Object)
  ---------------- ----------------------- ----------------------------
  목적             도메인 모델의 값 표현   계층 간 데이터 전달
  불변성           불변 (Immutable)        가변 (Mutable)
  로직 포함 여부   도메인 규칙 포함 가능   로직 없음
  비교 기준        값 동등성               주로 참조 비교
  사용 위치        도메인 계층             프레젠테이션, API 계층

------------------------------------------------------------------------

## 5. 실무 적용 전략

### 5.1 언제 VO를 사용할까?

-   금액, 좌표, 이메일, 전화번호 등 **도메인에서 불변성이 필요한 값**을
    표현할 때
-   비즈니스 규칙을 캡슐화해야 할 때

### 5.2 언제 DTO를 사용할까?

-   API 요청/응답에서 데이터 전달 시
-   외부 시스템 간 데이터 교환 시
-   DB에서 조회한 데이터를 가공하여 반환할 때

### 5.3 함께 쓰는 방식

-   **Entity → VO → DTO** 변환 패턴
    -   Entity: 데이터베이스의 영속 객체
    -   VO: 도메인 로직을 가진 불변 객체
    -   DTO: 외부와 데이터를 주고받기 위한 객체

``` java
// Entity → VO 변환
User user = userRepository.findById(1L);
Email email = new Email(user.getEmail());

// VO → DTO 변환
UserDTO dto = new UserDTO(user.getName(), email.getValue());
```

------------------------------------------------------------------------

## 6. 전문가 관점에서의 심화 내용

### 6.1 VO의 활용 심화

-   **DDD(Domain-Driven Design)** 에서 핵심 개념
-   값 객체를 활용해 **풍부한 도메인 모델(Rich Domain Model)** 을 설계
    가능
-   예: `Address`, `Money`, `Period` 등 복합 값 표현

### 6.2 DTO의 활용 심화

-   **API 최적화**: 필요한 데이터만 담아 전송 → 성능 개선
-   **MapStruct, ModelMapper** 와 같은 매퍼 라이브러리로 자동 변환 가능
-   CQRS(Command Query Responsibility Segregation) 패턴에서 **Query
    DTO** 로 자주 사용

### 6.3 잘못된 사용 시 문제점

-   VO를 단순 데이터 홀더처럼 사용 → 엔티티와 차이 없어짐
-   DTO에 비즈니스 로직 포함 → 유지보수 어려움
-   계층 간 경계 모호 → 코드 품질 저하

------------------------------------------------------------------------

## 7. 결론

-   **VO**는 도메인 모델을 풍부하게 하고, 불변성을 보장하며 안정성을
    높입니다.
-   **DTO**는 계층 간 데이터 교환을 단순화하고 보안을 강화합니다.
-   둘을 적절히 구분하고 조합하여 사용하는 것이 유지보수성과 확장성을
    모두 잡는 핵심 전략입니다.

------------------------------------------------------------------------

## 참고 자료

-   Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart
    of Software*
-   Martin Fowler, *Patterns of Enterprise Application Architecture*
-   Spring Framework 공식 문서
