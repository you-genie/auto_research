# CI/CD 완전 정복: 러너(Runner)부터 배포 전략까지 — 개발자를 위한 친절한 입문서

> 이 글은 개발 경험은 있지만 DevOps/CI/CD는 처음 접하는 분들을 위해 썼어요. LLM 같은 AI 기술은 훤히 아는데 "CI/CD 파이프라인이 뭐예요?"라는 질문에 막힌다면, 딱 맞는 글이에요.

---

## 목차

1. [CI/CD, 그래서 왜 필요한 건데요?](#1-cicd-그래서-왜-필요한-건데요)
2. [CI vs CD: 헷갈리는 개념 한 번에 정리](#2-ci-vs-cd-헷갈리는-개념-한-번에-정리)
3. [파이프라인이란 무엇인가](#3-파이프라인이란-무엇인가)
4. [러너(Runner) 완전 해부 — 이 글의 핵심](#4-러너runner-완전-해부--이-글의-핵심)
5. [주요 CI/CD 도구 비교 (2025~2026)](#5-주요-cicd-도구-비교-20252026)
6. [GitHub Actions YAML 워크플로 예제](#6-github-actions-yaml-워크플로-예제)
7. [모범 사례 — 실전에서 바로 쓰는 팁](#7-모범-사례--실전에서-바로-쓰는-팁)
8. [최신 트렌드 (2025~2026)](#8-최신-트렌드-20252026)
9. [참고 문헌](#9-참고-문헌)

---

## 1. CI/CD, 그래서 왜 필요한 건데요?

솔직히 말하면, CI/CD 없이 코드를 운영해본 사람이라면 그 고통을 압니다. "내 로컬에서는 됐는데 서버에서 왜 안 되지?"가 반복되고, 배포 날이면 팀 전체가 긴장하는 그 느낌이요.

[Octopus Deploy의 CI/CD 가이드](https://octopus.com/devops/ci-cd/)에 따르면, CI/CD는 소프트웨어 개발 생명주기를 자동화하고 간소화해서 팀이 고품질 애플리케이션을 더 빠르고 안정적으로 제공할 수 있도록 한다고 설명해요.

핵심 이점 세 가지만 꼽자면:

- **빠른 피드백**: 코드를 올리면 수 분 내로 "이 코드 문제있어" 알람이 옴
- **배포 공포 제거**: 자동화된 프로세스로 "오늘 배포하는 날이다..." 긴장 없어짐
- **팀 협업 품질 향상**: 모든 사람이 같은 기준으로 코드를 합침

[JetBrains 개발자 생태계 보고서 2025](https://blog.jetbrains.com/teamcity/2026/03/best-ci-tools/)를 보면 **전체 개발자의 55%가 CI/CD 도구를 정기적으로 사용**하고 있어요. 반대로 말하면, 아직 45%는 도입 전이라는 뜻이기도 하고요.

---

## 2. CI vs CD: 헷갈리는 개념 한 번에 정리

"CI/CD"가 한 단어처럼 쓰이는데, 사실 안에 세 가지 개념이 들어있어요.

### 2-1. CI (Continuous Integration, 지속적 통합)

> "CI means that any changes developers make to their code are immediately integrated into the master branch." — Octopus Deploy

그러니까, 개발자들이 코드를 자주(하루에도 여러 번) 공유 저장소에 올리고, 올릴 때마다 자동으로 빌드·테스트를 돌리는 거예요.

**CI가 없으면 어떻게 돼요?** A 개발자가 2주 동안 기능 브랜치에서 작업하고, B 개발자도 2주 동안 다른 기능을 짜요. 두 주 뒤에 합치려고 보면... 충돌 지옥이 기다리고 있죠. 이걸 "통합 지옥(Integration Hell)"이라고 불러요. CI는 이걸 막아주는 거예요.

### 2-2. CD (Continuous Delivery, 지속적 전달)

CI 다음 단계예요. 코드가 테스트를 통과하면, **언제든 배포 가능한 상태**로 패키징까지 해놓는 거예요. 실제 프로덕션 배포는 사람이 버튼 한 번 눌러서 하는 방식이죠.

> "package software and deploy it to production environments with the push of a button." — Octopus Deploy

### 2-3. CD (Continuous Deployment, 지속적 배포)

지속적 전달에서 "버튼 누르기"도 자동화한 버전이에요. 테스트 통과 → 자동으로 프로덕션까지 배포. 사람이 개입할 여지가 없어요. 아주 성숙한 팀, 아주 촘촘한 테스트 커버리지가 있어야 가능해요.

| 개념 | 자동화 범위 | 프로덕션 배포 |
|------|------------|--------------|
| CI (지속적 통합) | 빌드 + 테스트 | 수동 |
| CD (지속적 전달) | 빌드 + 테스트 + 패키징 | **수동** (버튼 누름) |
| CD (지속적 배포) | 빌드 + 테스트 + 패키징 + 배포 | **자동** |

대부분의 팀은 CI + 지속적 전달(Continuous Delivery) 조합으로 운영해요. 지속적 배포는 Netflix, Amazon 같은 곳들이 하는 고급 단계거든요.

---

## 3. 파이프라인이란 무엇인가

파이프라인(Pipeline)은 코드가 "개발자 손"에서 "실제 서비스"로 가는 여정을 단계별로 자동화한 흐름이에요. 물이 파이프를 따라 흐르듯, 코드가 각 단계를 거쳐 흘러가는 거죠.

[Octopus Deploy](https://octopus.com/devops/ci-cd/)는 CI/CD 파이프라인의 기본 4단계를 이렇게 정의해요:

```
[소스] → [빌드] → [테스트] → [배포]
  ↑          ↑        ↑         ↑
git push   컴파일   자동화 테스트   프로덕션
```

### 각 단계 설명

**1단계 — 소스 (Source)**
개발자가 `git push`나 Pull Request를 올리면 파이프라인이 시작돼요. GitHub, GitLab 같은 버전 관리 시스템이 트리거 역할을 해요.

**2단계 — 빌드 (Build)**
코드를 실행 가능한 형태로 만드는 단계예요. Python이라면 의존성 설치(`pip install`), Java라면 컴파일, Docker를 쓴다면 컨테이너 이미지 생성 등이 여기 해당해요.

**3단계 — 테스트 (Test)**
단위 테스트, 통합 테스트, 성능 테스트 등 자동화된 테스트들이 돌아가요. 여기서 하나라도 실패하면 파이프라인이 멈추고 개발자에게 알림이 가요.

**4단계 — 배포 (Deploy)**
테스트를 모두 통과한 코드를 스테이징(staging) 환경이나 프로덕션에 올리는 단계예요.

---

## 4. 러너(Runner) 완전 해부 — 이 글의 핵심

자, 이제 진짜 중요한 얘기를 해볼게요. "러너가 뭐예요?"라는 질문, CI/CD를 처음 접할 때 제일 먼저 막히는 부분이거든요.

### 4-1. 러너란 무엇인가 — 한 줄 정의

**러너(Runner)는 CI/CD 파이프라인의 각 작업(Job)을 실제로 실행하는 에이전트(프로그램)예요.**

쉽게 비유하면, GitHub/GitLab 서버는 "여기에 할 일이 생겼어요!"라고 알리는 사무실이고, 러너는 그 할 일을 받아서 실제로 처리하는 직원이에요. 직원은 회사 PC(GitHub 호스팅 서버)에 있을 수도 있고, 내 집 컴퓨터(셀프 호스팅)에 있을 수도 있어요.

### 4-2. 러너의 동작 원리 — 어떻게 잡(Job)을 가져가나

[Depot의 GitHub Actions 러너 아키텍처 분석](https://depot.dev/blog/github-actions-runner-architecture-part-1-the-listener)에 따르면, 러너는 다음과 같은 방식으로 동작해요:

```
[GitHub 서버]  ←——— 롱폴링(Long Polling) ———→  [Runner 에이전트]
      |                                                |
  Job 대기열에                                    "잡 있어요?"
  새 Job 추가됨                                   계속 물어봄
      |                                                |
  Job Available                                   Job 받아서 실행
  메시지 전송 ———————————————————————————————→ 실행 완료 후 다시 대기
```

**구체적인 프로세스:**

1. **연결 확립**: 러너가 시작되면 GitHub Actions 서비스에 인증하고, HTTPS 롱폴링(Long Polling) 연결을 맺어요.

2. **잡 대기**: 서버는 최대 50초 동안 연결을 열어둬요. 새 잡이 없으면 HTTP 202로 빈 응답을 돌려주고, 러너는 다시 폴링을 시작해요.

3. **잡 수신**: 새 잡이 생기면 서버가 `RunnerJobRequest` 메시지를 보내요. 러너는 약 2분 안에 잡을 "획득(acquire)"해야 해요.

4. **Lock 갱신**: 잡을 획득한 뒤, 60초마다 하트비트(Heartbeat)를 보내서 "나 아직 살아있어, 잡 진행 중이야"라고 알려줘요.

5. **Worker 실행**: 마지막으로 Worker 프로세스를 생성해서 실제 워크플로 명령어들을 실행해요.

> "The server will hold the request open for up to 50 seconds waiting for a new job to run." — Depot, GitHub Actions Runner Architecture

> 즉, 러너는 끊임없이 GitHub 서버에 "새 잡 있어요?"라고 물어보는 에이전트예요. 이 방식을 롱폴링(Long Polling)이라고 해요.

### 4-3. GitLab Runner의 경우

[GitLab Runner 가이드 (Baeldung)](https://www.baeldung.com/ops/gitlab-runner-guide)에 따르면, GitLab Runner도 비슷한 방식으로 동작해요. 기본 설정으로 **3초마다** GitLab 서버에 새 잡이 있는지 폴링해요.

최근에는 **롱폴링(Long Polling)** 방식도 도입됐어요. GitLab Workhorse가 Redis PubSub 채널을 구독하고, 새 잡이 생기면 즉시 알림을 받는 방식이죠. 이렇게 하면 3초마다 폴링하는 것보다 훨씬 빠르게 잡을 받아 실행할 수 있어요.

### 4-4. GitHub-Hosted Runner vs Self-Hosted Runner

이게 실무에서 제일 많이 고민하는 부분이에요.

#### GitHub-Hosted Runner (깃허브 호스팅 러너)

GitHub이 직접 관리하는 가상머신이에요. 잡이 시작되면 깨끗한 VM이 생성되고, 잡이 끝나면 VM이 사라져요.

**장점:**
- 설정 없이 바로 사용 가능
- OS/소프트웨어 업데이트를 GitHub이 자동으로 해줌
- 보안 격리 완벽 (잡마다 새 VM)
- ubuntu-latest, windows-latest, macos-latest 등 다양한 환경 제공

**단점:**
- 월 무료 시간 제한 (Free 플랜: 2,000분/월)
- 내부 네트워크 접근 불가 (회사 내부 DB 등)
- 특수 하드웨어(GPU, 특정 ARM 칩) 사용 불가
- 비용이 올라갈 수 있음 (큰 팀 또는 많은 빌드 시)

#### Self-Hosted Runner (셀프 호스팅 러너)

내 서버, 내 PC, 내 클라우드 VM에 직접 러너 에이전트를 설치해서 운영하는 방식이에요.

[GitHub Docs - Self-hosted runners](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners)에 따르면:

**장점:**
- 빌드 시간 무제한 (GitHub 분 제한 없음)
- 회사 내부 네트워크 접근 가능
- GPU, 특수 하드웨어 활용 가능
- 장기적 비용 절감 (빌드 양이 많을 때)
- 코드/시크릿이 내 인프라에만 있음

**단점:**
- 직접 유지관리 필요 (OS 패치, 보안 업데이트 등)
- 셋업 복잡도 있음
- 잡 간 환경 오염 주의 (이전 잡의 파일이 남을 수 있음)
- 퍼블릭 저장소에 셀프 호스팅 러너 사용 시 보안 위험 (외부인의 PR이 내 서버에서 실행될 수 있음!)

| 비교 항목 | GitHub-Hosted | Self-Hosted |
|---------|--------------|-------------|
| 초기 설정 | 즉시 사용 | 직접 설치/설정 |
| 유지관리 | GitHub 담당 | 직접 담당 |
| 비용 구조 | 분당 과금 | 서버 비용 (고정) |
| 내부망 접근 | 불가 | 가능 |
| 특수 하드웨어 | 제한적 | 자유롭게 가능 |
| 보안 격리 | 완벽 (잡마다 새 VM) | 직접 관리 필요 |
| 빌드 병렬성 | 요금제에 따라 제한 | 머신 수에 따라 제한 |

#### 어떤 걸 선택해야 하나요?

- **개인 프로젝트, 스타트업 초기**: GitHub-Hosted로 시작. 설정 없이 바로 씀.
- **빌드 양이 많아지고 비용 걱정될 때**: Self-Hosted 검토
- **내부 DB/시스템에 접근해야 하는 통합 테스트**: Self-Hosted 필수
- **GPU 빌드, ML 모델 테스트**: Self-Hosted (자체 GPU 서버 활용)

[GitHub Blog](https://github.blog/enterprise-software/ci-cd/when-to-choose-github-hosted-runners-or-self-hosted-runners-with-github-actions/)에서도 "예측 가능한 정기적 빌드 볼륨에서는 셀프 호스팅이 경제적"이라고 언급해요.

### 4-5. Actions Runner Controller (ARC) — 쿠버네티스에서 자동 확장

팀 규모가 커지면 러너 관리도 복잡해져요. 이때 등장하는 게 [Actions Runner Controller(ARC)](https://docs.github.com/en/actions/concepts/runners/actions-runner-controller)예요. 쿠버네티스 위에서 러너를 자동으로 스케일링하는 오퍼레이터(Operator)예요.

**동작 방식:**
1. ARC가 GitHub에 롱폴링 연결 유지
2. 새 잡 발생 → ARC가 쿠버네티스 API를 통해 새 Runner Pod 생성
3. 잡 완료 → Runner Pod 자동 삭제
4. 잡이 없을 때는 러너가 0개로 스케일 다운

잡마다 깨끗한 컨테이너 환경이 생성되므로, 환경 오염 문제가 없고 비용 효율도 좋아요.

### 4-6. Buildkite Agent — 하이브리드 모델의 대표주자

[Buildkite](https://buildkite.com/docs/agent)는 독특한 하이브리드 모델을 써요. **SaaS 컨트롤 플레인 + 셀프 호스팅 에이전트** 조합이에요.

> 클라우드 기반 컨트롤 플레인이 파이프라인 조율과 UI를 담당하고, 오픈소스 에이전트가 여러분의 인프라에서 실제 빌드를 실행해요. — Buildkite Documentation

이 방식은 코드와 시크릿이 절대 Buildkite 서버로 나가지 않는 게 장점이에요. 대규모 조직(50인 이상)이나 보안이 중요한 환경에서 선호해요.

---

## 5. 주요 CI/CD 도구 비교 (2025~2026)

[JetBrains 2025 개발자 생태계 보고서](https://blog.jetbrains.com/teamcity/2026/03/best-ci-tools/)와 [Northflank 가이드](https://northflank.com/blog/best-ci-cd-tools)를 종합해서 주요 도구들을 비교해볼게요.

### 시장 점유율 (2025 기준)

| 도구 | 기업 도입률 | 개인 프로젝트 |
|------|-----------|-------------|
| **GitHub Actions** | 33% | 39% |
| **Jenkins** | 28% | 13% |
| **GitLab CI** | 19% | 10% |
| 기타 (CircleCI, Buildkite 등) | ~20% | ~38% |

### 도구별 특징 비교

#### GitHub Actions
- **한 줄 요약**: GitHub 쓰는 팀의 기본 선택
- GitHub 생태계와 완벽 통합, 10,000개 이상의 마켓플레이스 액션 활용 가능
- YAML 기반, 직관적인 문법
- GitHub 외 저장소는 사용 불가 (이게 가장 큰 단점)
- **적합한 팀**: GitHub으로 코드 관리하는 모든 팀

#### GitLab CI/CD
- **한 줄 요약**: 올인원 DevOps 플랫폼을 원한다면
- 저장소 + CI/CD + 컨테이너 레지스트리 + 보안 스캔 + 프로젝트 관리가 한 지붕 아래
- 클라우드 호스팅과 셀프 호스팅 모두 지원
- **적합한 팀**: GitLab으로 전체 개발 사이클 관리하는 팀, GitLab을 자체 호스팅하는 기업

#### Jenkins
- **한 줄 요약**: 최강의 커스터마이징, 최대의 유지관리 부담
- 오픈소스, 수천 개의 플러그인, 거의 모든 걸 다 할 수 있음
- 2024년 기준 전 세계에서 가장 많이 배포된 CI/CD 서버
- 단, 설정·업그레이드·보안 패치를 직접 해야 함
- **적합한 팀**: 복잡한 레거시 시스템을 가진 대기업, 특수한 인프라가 필요한 팀

#### CircleCI
- **한 줄 요약**: 속도와 성능에 집중한 전문 도구
- Docker, VM, ARM 하드웨어 등 다양한 실행 환경 지원
- SSH 디버깅 기능이 편리함 (빌드 서버에 직접 접속해서 디버깅)
- **적합한 팀**: 여러 저장소 플랫폼(GitHub, Bitbucket, GitLab)을 혼용하는 팀

#### Buildkite
- **한 줄 요약**: 대규모 조직, 보안 최우선
- SaaS 컨트롤 플레인 + 자체 인프라 에이전트 하이브리드
- 10만 개 이상의 병렬 잡 처리 가능
- 코드와 시크릿이 외부로 나가지 않음
- **적합한 팀**: 개발자 50명 이상 대조직, 금융/의료 등 보안 규정이 엄격한 산업

### 어떤 도구를 골라야 하나요?

```
GitHub 저장소 사용?
  → YES: GitHub Actions 시작 (가장 쉬움)
  → NO, GitLab 사용?
      → YES: GitLab CI
      → NO, 레거시 시스템/특수 인프라?
          → YES: Jenkins
          → NO, 50인 이상 대조직?
              → YES: Buildkite
              → NO: CircleCI
```

---

## 6. GitHub Actions YAML 워크플로 예제

GitHub Actions를 예시로, 실제 파이프라인이 어떻게 생겼는지 볼게요. 워크플로 파일은 프로젝트의 `.github/workflows/` 폴더 안에 YAML 파일로 저장해요.

### 6-1. 기본 CI 파이프라인 (빌드 + 테스트)

```yaml
# .github/workflows/ci.yml

name: CI Pipeline  # 워크플로 이름

on:                # 어떤 이벤트에 실행할지
  push:
    branches: [ main, develop ]   # main, develop 브랜치에 push할 때
  pull_request:
    branches: [ main ]             # main 브랜치 대상 PR 생성 시

jobs:                  # 실행할 잡(Job) 목록
  build-and-test:      # 잡 이름 (마음대로 지어도 됨)
    runs-on: ubuntu-latest  # 어떤 러너에서 실행할지 (GitHub-Hosted)

    steps:                  # 이 잡에서 순서대로 실행할 스텝들
      - name: 코드 체크아웃
        uses: actions/checkout@v4   # GitHub 공식 액션: 저장소 코드를 가져옴

      - name: Python 설정
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'

      - name: 의존성 캐시 복원
        uses: actions/cache@v4
        with:
          path: ~/.cache/pip
          key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}

      - name: 의존성 설치
        run: pip install -r requirements.txt

      - name: 린트 검사
        run: flake8 src/ --max-line-length=120

      - name: 테스트 실행
        run: pytest tests/ -v --cov=src --cov-report=xml

      - name: 커버리지 업로드
        uses: codecov/codecov-action@v4
        with:
          file: coverage.xml
```

### 6-2. 매트릭스 빌드 (여러 파이썬 버전 테스트)

```yaml
# .github/workflows/matrix-test.yml

name: Matrix Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:                          # 매트릭스: 조합별로 잡이 생성됨
        os: [ubuntu-latest, macos-latest]
        python-version: ['3.10', '3.11', '3.12']
      fail-fast: false                 # 하나가 실패해도 나머지는 계속 실행

    steps:
      - uses: actions/checkout@v4

      - name: Python ${{ matrix.python-version }} 설정
        uses: actions/setup-python@v5
        with:
          python-version: ${{ matrix.python-version }}

      - run: pip install -r requirements.txt
      - run: pytest tests/
```

> 이 설정 하나로 2개 OS × 3개 Python 버전 = **총 6개의 잡**이 병렬로 실행돼요!

### 6-3. 빌드 + 테스트 + 배포 전체 파이프라인

```yaml
# .github/workflows/deploy.yml

name: Build, Test & Deploy

on:
  push:
    branches: [ main ]

env:
  DOCKER_IMAGE: my-app

jobs:
  # ---- 1단계: 빌드 & 테스트 ----
  build-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Docker 이미지 빌드
        run: docker build -t ${{ env.DOCKER_IMAGE }}:${{ github.sha }} .

      - name: 테스트 실행
        run: docker run ${{ env.DOCKER_IMAGE }}:${{ github.sha }} pytest tests/

      - name: 이미지 아티팩트 저장
        run: docker save ${{ env.DOCKER_IMAGE }}:${{ github.sha }} | gzip > image.tar.gz

      - uses: actions/upload-artifact@v4
        with:
          name: docker-image
          path: image.tar.gz

  # ---- 2단계: 스테이징 배포 ----
  deploy-staging:
    needs: build-test        # build-test 잡이 성공해야 실행
    runs-on: ubuntu-latest
    environment: staging     # GitHub Environments 보호 규칙 적용

    steps:
      - uses: actions/download-artifact@v4
        with:
          name: docker-image

      - name: AWS 인증 (OIDC 방식 — 시크릿 없이!)
        uses: aws-actions/configure-aws-credentials@v4
        with:
          role-to-assume: arn:aws:iam::123456789:role/GitHubActionsRole
          aws-region: ap-northeast-2

      - name: ECR 로그인 & 푸시
        run: |
          aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
          docker load < image.tar.gz
          docker push $ECR_REGISTRY/${{ env.DOCKER_IMAGE }}:${{ github.sha }}

  # ---- 3단계: 프로덕션 배포 (수동 승인 필요) ----
  deploy-prod:
    needs: deploy-staging
    runs-on: ubuntu-latest
    environment: production  # 이 환경에 승인자 설정하면 수동 승인 게이트 생김

    steps:
      - name: 프로덕션 배포
        run: echo "프로덕션 배포 완료!"
```

### 6-4. 셀프 호스팅 러너 사용하기

셀프 호스팅 러너를 쓸 때는 `runs-on` 만 바꾸면 돼요:

```yaml
jobs:
  build-with-gpu:
    runs-on: self-hosted    # 또는 커스텀 레이블: [self-hosted, gpu, linux]
    steps:
      - uses: actions/checkout@v4
      - name: GPU 필요한 ML 테스트
        run: python test_model.py --device cuda
```

셀프 호스팅 러너 설치는 GitHub 저장소 → Settings → Actions → Runners → "New self-hosted runner" 에서 OS별 설치 스크립트를 받을 수 있어요.

---

## 7. 모범 사례 — 실전에서 바로 쓰는 팁

### 7-1. 캐싱으로 빌드 속도 올리기

의존성 설치는 시간이 오래 걸려요. 근데 `requirements.txt`가 바뀌지 않으면 다시 설치할 필요가 없잖아요? 캐싱을 활용하면 **빌드 시간을 50% 이상 단축**할 수 있어요.

```yaml
- uses: actions/cache@v4
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
    restore-keys: |
      ${{ runner.os }}-pip-
```

`key`가 같으면 캐시를 복원하고, 달라지면 새로 설치 후 캐시를 저장해요.

### 7-2. 시크릿 관리 — 비밀은 YAML에 절대 쓰지 마세요

API 키, 데이터베이스 비밀번호를 YAML 파일에 직접 쓰면... 저장소에 올라가는 순간 끝이에요. 올바른 방법:

```yaml
# ❌ 절대 이렇게 하지 마세요
- run: aws s3 sync . s3://my-bucket --access-key AKIAIOSFODNN7EXAMPLE

# ✅ GitHub Secrets 사용
- run: aws s3 sync . s3://my-bucket
  env:
    AWS_ACCESS_KEY_ID: ${{ secrets.AWS_ACCESS_KEY_ID }}
    AWS_SECRET_ACCESS_KEY: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
```

더 좋은 방법은 **OIDC(OpenID Connect)**를 쓰는 거예요. AWS, GCP, Azure 모두 지원해요. OIDC를 쓰면 장기 자격증명(Access Key) 없이, 잡이 실행될 때마다 임시 토큰을 발급받아요. 시크릿 자체를 저장할 필요가 없어지는 거죠.

### 7-3. 매트릭스 빌드

앞서 예제에서 봤듯이, `strategy.matrix`를 쓰면 여러 환경 조합을 병렬로 테스트할 수 있어요. Python 라이브러리 개발할 때 특히 유용해요.

### 7-4. 액션 버전 고정

```yaml
# ❌ 태그 사용 — 태그는 변경될 수 있어요!
uses: actions/checkout@v4

# ✅ 커밋 SHA 고정 — 불변(immutable)
uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683
```

2025년에 실제로 발생한 [공급망 공격 사례](https://www.trantorinc.com/blog/software-supply-chain-security-sbom-slsa-engineering-tools)를 보면, 타사 액션 저장소가 해킹당해 워크플로 코드가 변조됐어요. 태그(`@v1`)를 사용하던 저장소들이 자동으로 악성 코드를 실행했죠. 커밋 SHA로 고정하면 이런 공격을 막을 수 있어요.

### 7-5. 배포 전략 — 블루-그린과 카나리

[Harness 블로그](https://www.harness.io/blog/blue-green-canary-deployment-strategies)에 따르면, 프로덕션 배포 위험을 줄이는 두 가지 핵심 전략이 있어요.

#### 블루-그린 배포 (Blue-Green Deployment)

두 개의 동일한 프로덕션 환경을 유지해요. 한쪽(그린)은 현재 서비스 중, 다른 쪽(블루)에 새 버전을 배포하고 테스트해요. 문제없으면 트래픽을 블루로 전환. 문제가 생기면 그린으로 즉시 롤백.

```
사용자 트래픽
      |
   [로드밸런서]
   /           \
[그린 v1.0]  [블루 v1.1]  ← 신버전 배포 & 테스트
      |
  테스트 완료! 트래픽 전환
      |
   [로드밸런서]
         \
      [블루 v1.1]  ← 이제 여기로 트래픽
   [그린 v1.0]  ← 롤백 대기 상태
```

**장점**: 롤백이 빠르고 간단  
**단점**: 인프라 비용이 2배 (두 환경 유지)

#### 카나리 배포 (Canary Deployment)

신버전을 전체 사용자에게 한 번에 배포하지 않고, 소수에게 먼저 보여줘요.

```
전체 트래픽 (100%)
      |
   [로드밸런서]
   /         \
[기존 v1.0]  [카나리 v1.1]
  90%            10%
```

10%에서 문제없으면 25%, 50%, 100%로 점진적으로 늘려가요. 가장 위험이 낮은 배포 방식이에요.

**장점**: 위험 최소화, 실제 사용자로 검증  
**단점**: 복잡한 설정, 촘촘한 모니터링 필요

---

## 8. 최신 트렌드 (2025~2026)

### 8-1. AI 기반 CI/CD

2026년 CI/CD의 핵심 키워드는 "지능화"예요.

[DevOps.com](https://devops.com/ai-powered-devops-transforming-ci-cd-pipelines-for-intelligent-automation-2/)에 따르면 AI가 CI/CD 파이프라인을 바꾸는 방식:

- **테스트 우선순위 결정**: ML 모델이 과거 실패 패턴을 학습해서 "이번에 변경한 코드라면 이 테스트가 실패할 가능성이 높아"라고 예측. 불필요한 테스트를 건너뛰어 빌드 시간을 줄여요.
- **자가 치유 파이프라인**: 빌드가 실패하면 AI가 원인을 분석하고 자동으로 수정 시도
- **예측적 리소스 할당**: 빌드 부하를 예측해서 러너를 미리 스케일업

실제로 한 SaaS 기업은 AI 기반 테스트 우선순위 도입 후 **빌드 시간 40% 단축**을 달성했어요.

### 8-2. 소프트웨어 공급망 보안

2025년에 소프트웨어 공급망 공격이 전년 대비 두 배 이상 증가했어요. [Faith Forge Labs](https://faithforgelabs.com/blog_supplychain_security_2025.php) 보고에 따르면 전체 기업의 70% 이상이 서드파티 소프트웨어와 관련된 보안 사고를 경험했고, 전 세계 피해 규모가 600억 달러에 달해요.

이에 대응하기 위한 핵심 기술들:

**SLSA (Supply-chain Levels for Software Artifacts)**

> Google이 만든 소프트웨어 공급망 보안 프레임워크예요. SLSA v1.1이 안정 버전으로 운영 중이에요. — [Practical DevSecOps](https://www.practical-devsecops.com/slsa-framework-guide-software-supply-chain-security/)

레벨 1~3으로 나뉘어져 있고, 레벨이 높을수록 빌드 프로세스의 무결성을 더 강하게 보장해요.

**Sigstore**

구글, 레드햇, Purdue University가 만들고 Linux Foundation이 관리하는 오픈소스 프로젝트예요. 키 없이 OIDC 신원으로 컨테이너 이미지와 아티팩트에 서명할 수 있어요. 구성 요소:
- **Cosign**: 이미지 서명 및 검증
- **Fulcio**: OIDC 신원 기반 단기 인증서 발급
- **Rekor**: 모든 서명 이벤트를 기록하는 투명 로그

### 8-3. OIDC 기반 비밀 없는 인증

앞서 언급한 OIDC가 2025년을 기점으로 표준으로 자리잡고 있어요. GitHub Actions에서 AWS/GCP/Azure에 배포할 때 Access Key 대신 OIDC 토큰을 사용하는 방식이 best practice로 굳어졌어요. 시크릿 노출 위험을 근본적으로 없애는 접근이에요.

### 8-4. 2026년 시장 전망

[DevOps.com 통계](https://devops.com/ai-powered-devops-transforming-ci-cd-pipelines-for-intelligent-automation-2/)에 따르면, DevOps 시장은 2025년 149.5억 달러를 기록했고, 연 25.7% 성장률로 2029년에는 373.3억 달러에 달할 전망이에요. CI/CD는 이 성장의 핵심 축이에요.

---

## 9. 참고 문헌

| 번호 | 제목 | 출처 |
|------|------|------|
| 1 | What Is CI/CD? Complete 2026 Guide | [Octopus Deploy](https://octopus.com/devops/ci-cd/) |
| 2 | Best CI/CD Tools for 2026: What the Data Actually Shows | [JetBrains TeamCity Blog](https://blog.jetbrains.com/teamcity/2026/03/best-ci-tools/) |
| 3 | GitHub Actions Runner Architecture: The Listener | [Depot](https://depot.dev/blog/github-actions-runner-architecture-part-1-the-listener) |
| 4 | Self-hosted runners - GitHub Docs | [GitHub Docs](https://docs.github.com/en/actions/hosting-your-own-runners/managing-self-hosted-runners/about-self-hosted-runners) |
| 5 | When to choose GitHub-Hosted or Self-Hosted runners | [GitHub Blog](https://github.blog/enterprise-software/ci-cd/when-to-choose-github-hosted-runners-or-self-hosted-runners-with-github-actions/) |
| 6 | Actions Runner Controller | [GitHub Docs](https://docs.github.com/en/actions/concepts/runners/actions-runner-controller) |
| 7 | Guide to GitLab Runner | [Baeldung on Ops](https://www.baeldung.com/ops/gitlab-runner-guide) |
| 8 | Long polling for CI - GitLab | [GitLab Docs](https://lsds.doc.ic.ac.uk/gitlab/help/ci/runners/long_polling.md) |
| 9 | Best CI/CD tools in 2026 | [Northflank Blog](https://northflank.com/blog/best-ci-cd-tools) |
| 10 | Blue-Green and Canary Deployments Explained | [Harness](https://www.harness.io/blog/blue-green-canary-deployment-strategies) |
| 11 | AI-Powered DevOps: Transforming CI/CD Pipelines | [DevOps.com](https://devops.com/ai-powered-devops-transforming-ci-cd-pipelines-for-intelligent-automation-2/) |
| 12 | AI Transforming CI/CD in DevOps 2026 | [Tech360us](https://tech360us.com/ai-ml/how-ai-is-transforming-ci-cd-in-devops-in-2026/) |
| 13 | SLSA Framework Guide 2026 | [Practical DevSecOps](https://www.practical-devsecops.com/slsa-framework-guide-software-supply-chain-security/) |
| 14 | Software Supply Chain Security: SBOMs, SLSA & Sigstore | [Faith Forge Labs](https://faithforgelabs.com/blog_supplychain_security_2025.php) |
| 15 | Buildkite Pipelines Architecture | [Buildkite Docs](https://buildkite.com/docs/pipelines/architecture) |
| 16 | CI/CD Pipeline Automation: A Complete Guide | [Landskill](https://www.landskill.com/blog/ci-cd-pipeline-automation-complete-guide-devops/) |
| 17 | Deployment Strategies: Blue-Green, Canary Explained | [DevOps Daily](https://devops-daily.com/posts/deployment-strategies-guide) |
| 18 | GitHub Actions Runners - From Bottleneck to Full Automation | [Medium - MadgicalTechDom](https://madgicaltechdom.medium.com/github-actions-runners-from-bottleneck-to-full-automation-0b599bf9bc0f) |

---

> 이 글이 도움이 됐다면, 다음엔 "쿠버네티스 기반 CD 파이프라인"이나 "GitOps(ArgoCD)"로 한 단계 더 나아가보세요!

*작성일: 2026-06-13 | 작성: Auto Research Pipeline with Claude Code*
