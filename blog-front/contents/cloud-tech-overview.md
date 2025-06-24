---
date: '2024-11-20'
title: '클라우드 기술 개요'
categories: ['ETC']
summary: '클라우드 컴퓨팅의 기본 개념과 주요 서비스'
thumbnail: './images/web/cloud.png'
comments: true
---
# 🌥️ 클라우드 컴퓨팅 완전 정복: 개발자를 위한 클라우드 기술 개요

> 개발자라면 반드시 이해해야 할 현대 소프트웨어 인프라의 핵심, 클라우드 컴퓨팅을 깊이 있게 파헤쳐 봅니다.

---

## 📌 클라우드 컴퓨팅이란?

**클라우드 컴퓨팅(Cloud Computing)**은 인터넷을 통해 서버, 스토리지, 데이터베이스, 네트워크, 소프트웨어 등 IT 자원을 **온디맨드 방식**으로 제공하는 기술입니다. 사용자는 물리적 장비를 직접 구축하지 않아도 되고, 필요한 만큼만 자원을 사용하고 비용을 지불할 수 있습니다.

간단히 말해, "내 서버실을 만들지 않아도 되는 IT 인프라의 혁신"이라 할 수 있습니다.

---

## 🕰️ 클라우드의 역사

- **1960년대**: 개념적 뿌리 (John McCarthy가 "컴퓨팅이 공공 유틸리티가 될 것"이라 예언)
- **1999년**: Salesforce.com, SaaS 비즈니스 모델을 최초로 상용화
- **2006년**: 아마존, AWS(Amazon Web Services) 출시 → IaaS 시장 본격 개화
- **2010년대**: Microsoft Azure, Google Cloud Platform 등 클라우드 시장 본격 경쟁 시작
- **2020년 이후**: 멀티 클라우드, 하이브리드 클라우드, 서버리스 컴퓨팅, AI 클라우드 등 급속 확장

---

## 🧩 클라우드 서비스 모델

### 1. ☁️ IaaS (Infrastructure as a Service)

> 가상 머신, 스토리지, 네트워크 등 인프라 자원을 서비스로 제공  
**대표 서비스**: AWS EC2, Azure Virtual Machines, Google Compute Engine

### 2. 🧱 PaaS (Platform as a Service)

> 애플리케이션을 구축/실행할 수 있는 플랫폼을 제공  
**대표 서비스**: Heroku, Google App Engine, AWS Elastic Beanstalk

### 3. 💻 SaaS (Software as a Service)

> 소프트웨어를 서비스 형태로 제공 (사용자는 설치 불필요)  
**대표 서비스**: Google Workspace, Microsoft 365, Notion, Figma

---

## 🏗️ 클라우드 아키텍처 구성 요소

- **Compute**: EC2, Lambda, Cloud Functions
- **Storage**: S3, Azure Blob, Google Cloud Storage
- **Database**: RDS, DynamoDB, Firestore, Cloud SQL
- **Networking**: VPC, Cloud Load Balancer, CDN
- **Monitoring & Logging**: CloudWatch, Stackdriver, Azure Monitor
- **DevOps**: CodePipeline, GitHub Actions, Terraform, Helm

---

## 🏆 주요 클라우드 플랫폼 비교

| 제공업체       | 장점                                                         | 대표 서비스                          |
|----------------|--------------------------------------------------------------|---------------------------------------|
| **AWS**        | 시장 점유율 1위, 서비스 종류 가장 다양, 커뮤니티 방대       | EC2, S3, Lambda, RDS, CloudFront      |
| **Azure**      | 마이크로소프트 생태계와의 강력한 연동                      | Virtual Machines, Azure Functions     |
| **Google Cloud** | 데이터 분석/AI 서비스에 강점, Kubernetes의 원조             | BigQuery, GKE, Firebase               |
| **Oracle Cloud**| 엔터프라이즈 데이터베이스에 최적화                         | Autonomous DB, OCI Compute            |
| **Naver Cloud / KT Cloud** | 국내 서비스 안정성, 한국어 지원 강력                 | AI 서비스, 클라우드 VPC, 서버리스 등 |

---

## ✅ 클라우드의 장점

- **확장성**: 수요에 따라 자원을 자동으로 조절 (Auto Scaling)
- **유연성**: 전 세계 리전에 배포 가능
- **비용 효율성**: 사용한 만큼 지불 (Pay-as-you-go)
- **빠른 개발**: 인프라에 대한 고민 없이 앱 개발에 집중 가능
- **보안 강화**: IAM, 보안 그룹, 키 관리 시스템 등 다양한 보안 서비스

---

## ⚠️ 클라우드의 단점

- **비용 예측 어려움**: 사용량이 많아질수록 비용 폭증 가능
- **벤더 락인(Vendor Lock-In)**: 특정 클라우드 플랫폼에 종속될 수 있음
- **데이터 주권 문제**: 리전 선택이 중요한 이유
- **학습 곡선**: 서비스가 많아 처음 진입 장벽이 높음

---

## 🔥 최근 클라우드 트렌드

### 1. 멀티 클라우드 & 하이브리드 클라우드
> 하나의 벤더에 종속되지 않고 AWS + Azure + GCP를 조합하거나, 온프레미스와 클라우드를 혼합 운영

### 2. 서버리스(Serverless)
> 인프라를 전혀 신경 쓰지 않고 함수 단위로 실행되는 클라우드 방식  
→ AWS Lambda, Cloud Functions

### 3. 컨테이너 & 쿠버네티스(Kubernetes)
> 컨테이너 기반 마이크로서비스 아키텍처를 통해 유연한 배포 및 스케일링 구현  
→ EKS, GKE, AKS

### 4. AI 클라우드
> AI 모델 훈련, 서빙, 추론까지 클라우드에서 처리 (Vertex AI, SageMaker 등)

### 5. 인프라 코드화 (IaC)
> 인프라를 코드로 관리하여 자동화, 버전관리 가능  
→ Terraform, Pulumi, AWS CDK

---

## 🧠 클라우드 입문자를 위한 학습 팁

- **공식 튜토리얼 따라 하기**: AWS, Azure, GCP 모두 체험 계정 제공
- **무료 강의 활용**: YouTube, Udemy 무료 강의 풍부
- **자격증 도전**:  
  - AWS Certified Cloud Practitioner  
  - Google Associate Cloud Engineer  
  - Microsoft Azure Fundamentals

---

## 📝 마치며

클라우드는 단순한 "서버 대여 서비스"가 아닙니다. 현대의 소프트웨어 인프라 설계, 운영, 보안을 아우르는 핵심 기술입니다. 개발자에게 클라우드는 더 이상 선택이 아닌 **필수 역량**입니다.

지금 이 순간에도 전 세계 수많은 앱과 서비스가 클라우드 위에서 돌아가고 있습니다. 클라우드를 이해하는 것은, **소프트웨어의 미래를 이해하는 것**입니다.

---
