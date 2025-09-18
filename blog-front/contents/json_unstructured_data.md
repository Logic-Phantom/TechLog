---
date: '2025-09-18'
title: 'JSON 데이터와 비정형 데이터'
categories: ['Web']
summary: '한단계 앞으로'
thumbnail: './images/javascript/jsonData.png'
comments: true
---
# JSON 데이터와 비정형 데이터: 기초부터 전문가 관점까지

## 1. 들어가며
데이터 시대에서 가장 중요한 키워드는 **형식(Structured)**과 **비형식(Unstructured)**입니다.  
JSON은 그 중에서도 표준화된 데이터 교환 형식으로 널리 사용되고 있으며, 동시에 다양한 비정형 데이터와 함께 활용되고 있습니다.  
이 글에서는 JSON과 비정형 데이터의 기본 개념부터 심화적 응용, 그리고 전문가적 시각에서의 활용 방안까지 다룹니다.

---

## 2. JSON 데이터 기본 개념
### 2.1 JSON이란?
- **정의**: JavaScript Object Notation의 약자
- **특징**
  - 키-값 쌍 구조 (key-value)
  - 경량 데이터 교환 포맷
  - 언어 독립적
- **예시**
```json
{
  "name": "홍길동",
  "age": 30,
  "skills": ["Java", "Spring", "JavaScript"]
}
```

### 2.2 장점
- 사람과 기계 모두 읽기 쉬움
- 다양한 언어에서 파싱/생성 지원
- REST API, GraphQL, NoSQL(MongoDB 등)에서 표준 포맷

---

## 3. 비정형 데이터란?
### 3.1 정의
- 사전에 정의된 스키마가 없는 데이터
- 예: 텍스트, 이미지, 동영상, 음성, 센서 로그 등

### 3.2 특징
- 구조적 제약 없음
- 방대한 크기 (Big Data의 주요 원천)
- 저장·처리 복잡성 증가

### 3.3 예시
- **텍스트 데이터**: 고객 리뷰, 소셜 미디어 게시글
- **멀티미디어 데이터**: 사진, 영상, 오디오
- **로그 데이터**: 서버 로그, IoT 센서 데이터

---

## 4. JSON과 비정형 데이터의 연결점
- 비정형 데이터를 **메타데이터**와 함께 JSON으로 표현 가능
- 예시: 이미지 데이터에 대한 JSON 메타데이터
```json
{
  "file_name": "cat.png",
  "size": "2MB",
  "resolution": "1920x1080",
  "labels": ["cat", "animal", "cute"]
}
```

- 로그 수집 시스템(예: ELK 스택, Splunk)에서 JSON을 사용하여 비정형 데이터를 구조화

---

## 5. 실무 활용
### 5.1 REST API 응답
- JSON은 웹 API의 사실상 표준
- 클라이언트-서버 간 데이터 교환에 필수

### 5.2 빅데이터 & 분석
- Hadoop, Spark에서 JSON 로그 처리
- 머신러닝 학습용 라벨링 데이터(JSON 포맷으로 저장)

### 5.3 데이터베이스
- MongoDB, CouchDB 등은 JSON 기반 문서형 DB
- 관계형 DB에서도 JSON 컬럼 타입 지원 (예: PostgreSQL, MySQL 5.7+)

---

## 6. 심화 주제
### 6.1 JSON Schema
- JSON 데이터의 구조를 정의하는 표준
- 예:
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "사용자 정보",
  "type": "object",
  "properties": {
    "name": { "type": "string" },
    "age": { "type": "integer" },
    "skills": { "type": "array", "items": { "type": "string" } }
  },
  "required": ["name", "age"]
}
```

### 6.2 성능 및 최적화
- JSON 직렬화/역직렬화 속도 이슈
- 대규모 데이터 전송 시 압축(Gzip 등) 활용
- BSON(Binary JSON) → MongoDB 내부 포맷

### 6.3 보안 이슈
- JSON 인젝션 공격 가능성
- 민감 데이터 마스킹 필요

---

## 7. 전문가 관점에서의 JSON & 비정형 데이터
- **데이터 레이크(Data Lake)**: 다양한 비정형 데이터를 JSON 메타데이터와 함께 저장
- **ETL 파이프라인**: JSON 기반 데이터 변환 및 적재 자동화
- **AI/ML 학습 데이터셋**: 이미지/텍스트/음성 등 비정형 데이터를 JSON 라벨과 결합
- **클라우드 네이티브 아키텍처**: AWS S3, GCP BigQuery, Azure Data Lake에서 JSON 지원 강화

---

## 8. 결론
- JSON은 단순히 "데이터 교환 포맷"을 넘어 **비정형 데이터를 구조화하고 활용하는 핵심 기술**
- 앞으로는 데이터 레이크, AI/ML 학습, 클라우드 네이티브 환경에서 JSON과 비정형 데이터의 결합이 더욱 중요해질 것

---

## 참고 자료
- [JSON 공식 문서](https://www.json.org/json-ko.html)
- [JSON Schema](https://json-schema.org/)
- [MongoDB Documentation](https://www.mongodb.com/docs/)
- [Apache Spark JSON Guide](https://spark.apache.org/docs/latest/sql-data-sources-json.html)
