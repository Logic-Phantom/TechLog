---
date: '2025-09-23'
title: 'STOMP 기반 WebSocket 메시징 완벽 가이드'
categories: ['Web']
summary: 'Web에서 메시징 처리하는 방법'
thumbnail: './images/web/webMsgSoket.png'
comments: true
---
# STOMP 기반 WebSocket 메시징 완벽 가이드

## 1. 들어가며
웹 애플리케이션이 실시간성을 요구하는 경우(예: 채팅, 알림, 주식 시세, 협업 도구 등) **WebSocket**은 HTTP 기반 요청/응답 모델을 넘어 양방향 통신을 가능하게 합니다.  
그러나 기본 WebSocket은 단순히 **바이너리/텍스트 프레임**을 전송하는 수준이므로, 메시지 구조나 라우팅, 구독 관리 등을 개발자가 직접 구현해야 하는 부담이 있습니다.  

이를 보완하기 위해 등장한 프로토콜이 **STOMP (Simple Text Oriented Messaging Protocol)** 입니다. STOMP는 메시지를 **프레임 단위로 정의**하고, **Publish/Subscribe** 기반의 라우팅과 사용자별 메시지 전달까지 쉽게 구현할 수 있도록 도와줍니다.

---

## 2. 기본 WebSocket vs STOMP 비교

| 구분 | 기본 WebSocket | STOMP 기반 WebSocket |
|------|----------------|----------------------|
| 메시지 포맷 | 텍스트/바이너리 프레임 | 명령어 기반 프레임 구조 (SEND, SUBSCRIBE, MESSAGE 등) |
| 통신 방식 | 주로 1:1 통신 | Pub/Sub (브로드캐스트 및 특정 사용자 대상) |
| 라우팅 | 직접 구현 필요 | 메시지 브로커 자동 라우팅 |
| 구독 관리 | 직접 구현 필요 | /topic, /queue 기반 구독 지원 |
| 확장성 | 낮음 | 높음 (분산 환경에 적합) |
| 호환성 | WebSocket 미지원 환경 불가 | SockJS로 폴백 지원 (XHR, Streaming 등) |

---

## 3. STOMP 메시지 프레임 구조

STOMP는 HTTP와 유사한 텍스트 기반 프로토콜로, 명령어(Command) + 헤더(Header) + 바디(Body) 구조를 가집니다.

예시:  
```
SEND
destination:/topic/news
content-type:text/plain

Breaking News: WebSocket with STOMP is awesome!
```

### 주요 명령어
- **CONNECT / DISCONNECT** : 클라이언트 연결/종료
- **SEND** : 특정 대상(주제/큐/사용자)으로 메시지 전송
- **SUBSCRIBE / UNSUBSCRIBE** : 주제(topic) 구독/해제
- **MESSAGE** : 서버 → 클라이언트 전달 메시지
- **ERROR** : 오류 프레임

---

## 4. 서버 사이드 구성 (Spring 기반 예시)

### 4.1 WebSocket 엔드포인트 설정
```java
@Configuration
@EnableWebSocketMessageBroker
public class WebSocketConfig implements WebSocketMessageBrokerConfigurer {

    @Override
    public void configureMessageBroker(MessageBrokerRegistry config) {
        // 클라이언트가 구독하는 prefix: /topic, /queue
        config.enableSimpleBroker("/topic", "/queue");

        // 클라이언트가 메시지 보낼 때 붙이는 prefix
        config.setApplicationDestinationPrefixes("/app");

        // 특정 사용자에게 보낼 prefix
        config.setUserDestinationPrefix("/user");
    }

    @Override
    public void registerStompEndpoints(StompEndpointRegistry registry) {
        // 클라이언트가 연결할 엔드포인트
        registry.addEndpoint("/ws-stomp")
                .setAllowedOrigins("*")
                .withSockJS(); // WebSocket 미지원 브라우저 대응
    }
}
```

### 4.2 메시지 컨트롤러
```java
@Controller
public class ChatController {

    // /app/chat.sendMessage 로 들어온 메시지를 /topic/public 으로 브로드캐스트
    @MessageMapping("/chat.sendMessage")
    @SendTo("/topic/public")
    public ChatMessage sendMessage(ChatMessage message) {
        return message;
    }

    // 특정 사용자에게만 전달
    @MessageMapping("/chat.private")
    public void sendPrivate(ChatMessage message, Principal user) {
        messagingTemplate.convertAndSendToUser(
            message.getReceiver(), "/queue/private", message
        );
    }

    @Autowired
    private SimpMessagingTemplate messagingTemplate;
}
```

---

## 5. 클라이언트 구성

### 5.1 SockJS + Stomp.js 연결
```javascript
import SockJS from "sockjs-client";
import Stomp from "stompjs";

const socket = new SockJS("/ws-stomp");
const stompClient = Stomp.over(socket);

stompClient.connect({}, (frame) => {
    console.log("Connected: " + frame);

    // 구독
    stompClient.subscribe("/topic/public", (message) => {
        console.log("Received:", JSON.parse(message.body));
    });

    // 메시지 발행
    stompClient.send("/app/chat.sendMessage", {}, JSON.stringify({
        sender: "user1",
        content: "Hello STOMP!"
    }));
});
```

---

## 6. 심화: 커스터마이징 포인트

### 6.1 인바운드/아웃바운드 채널 인터셉터
```java
@Component
public class StompChannelInterceptor implements ChannelInterceptor {

    @Override
    public Message<?> preSend(Message<?> message, MessageChannel channel) {
        StompHeaderAccessor accessor =
            MessageHeaderAccessor.getAccessor(message, StompHeaderAccessor.class);

        if (StompCommand.CONNECT.equals(accessor.getCommand())) {
            String token = accessor.getFirstNativeHeader("Authorization");
            // 토큰 검증 로직
        }
        return message;
    }
}
```

→ 인증/인가, 메시지 로깅, 필터링, 멀티 테넌시 구현에 활용 가능

---

### 6.2 메시지 브로커 확장
- **SimpleBroker**: 메모리 기반, 단일 서버 환경 적합
- **RabbitMQ / Kafka**와 연동: 대규모 분산 메시징 지원

```java
@Override
public void configureMessageBroker(MessageBrokerRegistry config) {
    config.enableStompBrokerRelay("/topic", "/queue")
          .setRelayHost("localhost")
          .setRelayPort(61613)
          .setClientLogin("guest")
          .setClientPasscode("guest");
}
```

---

## 7. 장단점 정리

### 장점
- 명확한 프로토콜 → 개발/유지보수 용이
- Pub/Sub 기반 → 브로드캐스트, 그룹 메시징 자연스럽게 지원
- 사용자 prefix → 특정 사용자 타깃 메시징 가능
- 확장성 → 메시지 브로커(RabbitMQ, Kafka) 연계로 분산 환경 지원
- SockJS 폴백 → WebSocket 미지원 브라우저에서도 동작

### 단점
- WebSocket 단순 프레임보다 오버헤드 존재
- 브로커 확장 시 추가 인프라 필요
- 대용량 메시징 시 성능 튜닝 필수 (큐 설정, 세션 관리 등)

---

## 8. 결론
STOMP는 WebSocket의 단순 프레임 전송을 **메시징 프로토콜**로 확장하여,  
**라우팅, 구독, 사용자별 메시징, 확장성**을 모두 갖춘 강력한 실시간 통신 아키텍처를 제공합니다.  

실시간 협업 서비스, 대규모 알림 시스템, IoT 센서 데이터 처리 등 **실시간성과 확장성**이 필요한 분야에서 사실상 표준으로 자리 잡고 있습니다.  

---

## 9. 참고 자료
- [STOMP 공식 문서](https://stomp.github.io/stomp-specification-1.2.html)
- [Spring WebSocket Messaging](https://docs.spring.io/spring-framework/reference/web/websocket.html)
- [SockJS Protocol](https://github.com/sockjs/sockjs-protocol)
