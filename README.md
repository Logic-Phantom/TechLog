## 🧑‍💻 logic-phantom.github.io

개발자의 생각과 배움을 기록하는 **개인 기술 블로그**입니다.  
[Gatsby](https://www.gatsbyjs.com/) 기반으로 구축되었으며, GitHub Actions를 이용한 CI/CD 파이프라인을 통해 **GitHub Pages**에 자동 배포됩니다.

> 📍 블로그 주소: [https://logic-phantom.github.io](https://logic-phantom.github.io)

---

## 🛠 기술 스택

- **Framework**: [Gatsby](https://www.gatsbyjs.com/)
- **Deploy**: GitHub Pages + GitHub Actions
- **CI/CD**: `main` 브랜치에 커밋 시 자동 빌드 및 배포
- **Content**: Markdown 기반의 포스트 관리
- **기타**: SEO 및 퍼포먼스를 고려한 최적화 구조

---

## 📁 프로젝트 구조

```
codemasterli.github.io/
├── content/ # 블로그 글 (Markdown)
├── src/ # Gatsby 소스 코드
│    ├── components/ # 공통 컴포넌트
│    ├── pages/ # 라우트 페이지
│    └── templates/ # 마크다운 포스트 템플릿
├── static/ # 정적 파일 (이미지 등)
├── gatsby-config.js # Gatsby 설정
├── package.json
└── README.md
```

---

## ⚙️ 자동 배포 시스템 (CI/CD)

GitHub Actions를 통해 다음 조건에 따라 블로그가 자동 배포됩니다:

- `main` 브랜치에 커밋이 푸시될 때
- 매일 자정 (UTC 기준) 스케줄에 따라

### 배포 흐름

1. Gatsby 프로젝트(`blog-front`)를 빌드
2. 결과물(`public/`)을 GitHub Pages용 저장소 (`Logic-Phantom/Logic-Phantom.github.io`)로 복사
3. 변경 사항이 있을 경우 자동 커밋 및 푸시

> 배포 설정은 `.github/workflows/deploy.yml`에서 확인할 수 있습니다.

---

## 🚀 로컬 실행 방법

```bash
# Gatsby 프로젝트 디렉토리로 이동
cd blog-front

# 패키지 설치
npm install

# 개발 서버 실행
npm run develop

# 브라우저에서 http://localhost:8000 확인
