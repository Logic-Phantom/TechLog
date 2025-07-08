---
date: '2025-07-08'
title: '🚀 Zig란..?'
categories: ['Web']
summary: '지그 재그를 알아보자~'
thumbnail: './images/web/Zig.png'
comments: true
---

# 🚀 Zig란 무엇인가요?

Zig는 C를 대체할 수 있도록 설계된 **현대적 시스템 프로그래밍 언어**입니다.  
Andrew Kelley가 2015년에 개발을 시작했고, 안전성과 성능, 이식성을 동시에 잡기 위해 탄생했습니다.

> C처럼 빠르지만, 더 안전하고, 읽기 쉬우며, 고성능을 위한 기능을 갖춘 언어입니다.

---

# 🧠 Zig의 핵심 특징

## ✅ 1. 메모리 안전성

- Null 포인터나 버퍼 오버플로우를 명시적으로 방지
- `error`, `defer`, `comptime` 등 C에는 없는 안전한 기능 제공

## ✅ 2. 가비지 컬렉션 없음

- 직접 메모리 제어 가능
- GC 없이도 명시적으로 자원 해제 가능

## ✅ 3. C와의 완벽한 호환성

- C 헤더 파일 직접 import
- libc 없이도 동작 가능하며, 자체 빌드 시스템 보유

## ✅ 4. Cross Compilation의 강점

- `zig build-exe hello.zig -target x86_64-windows` 와 같은 방식으로 다양한 플랫폼 타깃 지원

## ✅ 5. 간결한 문법

```zig
const std = @import("std");

pub fn main() void {
    std.debug.print("Hello, Zig!\n", .{});
}
```

---

# ⚖️ Zig의 장점과 단점

| 장점 | 단점 |
|------|------|
| C보다 안전하고 직관적인 문법 | 아직 안정 버전(v1.0) 미출시 |
| 뛰어난 컴파일 속도와 빌드 시스템 | Rust 대비 생태계 규모 작음 |
| 다양한 플랫폼 지원 (cross-compiling) | 복잡한 프로젝트에는 성숙도가 부족할 수 있음 |

---

# 🔧 실제 사용 사례

- **Bun.js** 런타임 (JavaScript 런타임)
- **TigerBeetle** 고성능 금융 데이터베이스
- **Ghostty** GPU 기반 터미널
- **Uber**, **Valve** 등에서도 내부 빌드 도구 등에 도입

---

# 🔮 앞으로의 전망

- Zig는 빠르게 성장 중인 언어이며, C 개발자들이 넘어올 수 있는 **이식성과 생산성의 균형**을 잡은 언어입니다.
- 공식 v1.0이 출시되면 더 널리 쓰일 것으로 보이며, 임베디드, OS 개발, 게임, 툴체인 등 다양한 분야에서 활용될 것입니다.

> "Zig는 단순한 대안이 아니라, 새로운 세대의 시스템 언어입니다."

---

📌 추천 링크:
- 공식 사이트: [https://ziglang.org](https://ziglang.org)
- 문서: [https://ziglang.org/documentation/master/](https://ziglang.org/documentation/master/)
- 커뮤니티: Zig Discord, GitHub

