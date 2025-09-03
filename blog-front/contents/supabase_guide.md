---
date: '2025-09-03'
title: 'Supabase 심층 가이드'
categories: ['Web','Server']
summary: '트랜드의 트랜드'
thumbnail: './images/web/Supabase.png'
comments: true
---
# Supabase 심층 가이드: 기초부터 전문가 활용까지

## 1. Supabase란?
Supabase는 오픈소스 기반의 **Firebase 대체 서비스**로, 빠르게 백엔드를 구축하고자 하는 개발자를 위한 **BaaS(Backend as a Service)**입니다.
주요 특징은 다음과 같습니다:

- **PostgreSQL 기반**: 관계형 데이터베이스를 사용하며 SQL과 호환
- **실시간 데이터베이스**: `Realtime` 기능으로 DB 변경을 클라이언트에 실시간 반영
- **인증(Authentication)**: OAuth, 이메일/비밀번호, 마법 링크 등 지원
- **스토리지(Storage)**: 파일 업로드 및 관리
- **Edge Functions**: 서버리스 함수로 백엔드 로직 구현 가능
- **오픈소스 & 호스팅**: 자체 호스팅 가능, 클라우드 호스팅도 제공

> Firebase와 달리 SQL 기반이라는 점에서 기존 RDB 설계를 그대로 활용 가능하고, 복잡한 쿼리도 자유롭게 작성할 수 있음.

## 2. Supabase의 핵심 구성 요소
### 2.1 Database
- PostgreSQL 기반
- 실시간 변경 감지 기능
- Row-level security(RLS)로 세밀한 접근 제어 가능

### 2.2 Auth
- 이메일/비밀번호, OAuth(Google, GitHub 등)
- JWT 기반 인증
- 세션 관리 및 비밀번호 재설정 기능

### 2.3 Storage
- 파일 업로드, 이미지, 문서 관리
- 공개/비공개 접근 제어
- URL 서명으로 제한된 접근 가능

### 2.4 Realtime
- DB 테이블, 채널 단위 실시간 구독
- WebSocket 기반
- 실시간 채팅, 알림 시스템 등에 활용 가능

### 2.5 Functions (Edge Functions)
- 서버리스 함수 구현
- HTTP 엔드포인트 제공
- JWT 인증, DB 트리거 등 활용 가능

## 3. Supabase 시작하기 (기초)
### 3.1 프로젝트 생성
1. [Supabase 홈페이지](https://supabase.com/) 접속
2. 계정 생성 후 새 프로젝트 생성
3. Database password 설정 및 프로젝트 생성

### 3.2 테이블 생성
예시: `users` 테이블
```sql
create table users (
    id uuid primary key default gen_random_uuid(),
    email text unique not null,
    username text,
    created_at timestamp default now()
);
```

### 3.3 인증 설정
- 이메일/비밀번호 로그인 활성화
- OAuth 제공자 설정

### 3.4 클라이언트 초기화
JavaScript 예시:
```javascript
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = 'https://xyzcompany.supabase.co';
const supabaseKey = 'public-anon-key';
const supabase = createClient(supabaseUrl, supabaseKey);
```

## 4. 기본 CRUD 예제
### 4.1 데이터 삽입
```javascript
const { data, error } = await supabase
  .from('users')
  .insert([{ email: 'example@test.com', username: 'example' }]);
```

### 4.2 데이터 조회
```javascript
const { data, error } = await supabase
  .from('users')
  .select('*')
  .eq('username', 'example');
```

### 4.3 데이터 업데이트
```javascript
const { data, error } = await supabase
  .from('users')
  .update({ username: 'newname' })
  .eq('email', 'example@test.com');
```

### 4.4 데이터 삭제
```javascript
const { data, error } = await supabase
  .from('users')
  .delete()
  .eq('email', 'example@test.com');
```

## 5. 심화 활용
### 5.1 Realtime 구독
```javascript
supabase
  .from('users')
  .on('INSERT', payload => {
    console.log('New user added!', payload);
  })
  .subscribe();
```

### 5.2 Row-Level Security (RLS)
```sql
alter table users enable row level security;

create policy "user can view own data"
  on users
  for select
  using (auth.uid() = id);
```

### 5.3 스토리지 활용
```javascript
const { data, error } = await supabase.storage
  .from('avatars')
  .upload('public/avatar1.png', file);
```

### 5.4 서버리스 함수
```javascript
// functions/sendWelcomeEmail/index.js
export async function handler(req, res) {
  const { email } = await req.json();
  // 이메일 전송 로직
  res.status(200).json({ message: 'Email sent' });
}
```

## 6. 프로젝트 적용 방법
### 6.1 웹 애플리케이션
- Next.js, React 등과 통합
- 예: 로그인, 회원가입, 실시간 채팅 구현

### 6.2 모바일 애플리케이션
- React Native, Flutter와 연동
- Supabase SDK 제공으로 인증, DB, 스토리지 쉽게 사용 가능

### 6.3 백엔드 대체
- 기존 Node.js 서버 일부 기능을 Supabase Functions와 DB로 대체 가능
- Firebase를 사용하던 프로젝트를 SQL 기반으로 마이그레이션 가능

## 7. 최적화 및 전문가 팁
1. **SQL 쿼리 최적화**
   - 인덱스 생성
   - 복잡한 조인은 View나 Materialized View 활용

2. **보안**
   - RLS 적극 활용
   - 민감 데이터는 Storage 암호화 옵션 사용

3. **실시간 기능**
   - 필요한 테이블에만 구독
   - 클라이언트 부하 최소화

4. **프로젝트 관리**
   - 스테이징/프로덕션 분리
   - Supabase CLI로 마이그레이션 관리

## 8. 참고 자료
- [Supabase 공식 문서](https://supabase.com/docs)
- [Supabase GitHub](https://github.com/supabase/supabase)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
