# Google Antigravity 완전 정복: 에이전트 우선 개발 플랫폼의 모든 것

> 📊 **발표자료**: [slides.pptx](./slides.pptx)

> 작성일: 2026-05-22 | 분류: AI 코딩 에이전트 / 개발 도구

---

## 목차

1. [Antigravity가 뭐예요?](#1-antigravity가-뭐예요)
2. [발표 히스토리 — 어디서 나온 제품인가](#2-발표-히스토리--어디서-나온-제품인가)
3. [경쟁 도구와 포지셔닝 비교](#3-경쟁-도구와-포지셔닝-비교)
4. [아키텍처와 기술 스택](#4-아키텍처와-기술-스택)
5. [사용자 경험 — UI와 워크플로](#5-사용자-경험--ui와-워크플로)
6. [에이전트 능력 벤치마크](#6-에이전트-능력-벤치마크)
7. [가격 체계](#7-가격-체계)
8. [개발자 커뮤니티 반응](#8-개발자-커뮤니티-반응)
9. [한계와 보안 리스크](#9-한계와-보안-리스크)
10. [빠른 시작 가이드](#10-빠른-시작-가이드)
11. [결론 — 지금 써야 할까?](#11-결론--지금-써야-할까)
12. [참고문헌](#12-참고문헌)

---

## 1. Antigravity가 뭐예요?

솔직히 Google이 AI 코딩 도구 경쟁에서 항상 한 발 늦는 느낌이었잖아요? Copilot이 먼저 나오고, Cursor가 VS Code 포크로 시장을 먹고, Claude Code가 터미널 에이전트로 치고 들어오는 동안 Google은 Gemini Code Assist라는 확장 프로그램으로 버텼죠.

그런데 2025년 11월에 뭔가 다른 게 나왔어요. 이름이 **Antigravity**예요.

단순한 코드 완성 도우미가 아니라, Google이 "에이전트 우선(agent-first) 개발 플랫폼"이라고 부르는 물건인데요. AI가 코드 한 줄 제안하는 게 아니라 **작업 단위로 자율적으로 실행**하는 방식이에요. 계획 짜고, 파일 만들고, 터미널 명령 실행하고, 브라우저로 UI 테스트까지 스스로 해요.

그리고 2026년 5월 Google I/O에서 **Antigravity 2.0**이 발표되면서 단순 IDE를 넘어 CLI + SDK + 엔터프라이즈 플랫폼을 아우르는 풀스택 개발 자동화 플랫폼으로 진화했어요.

---

## 2. 발표 히스토리 — 어디서 나온 제품인가

### 2.1 출시 연혁

| 날짜 | 이벤트 |
|------|--------|
| 2025-11-18 | Antigravity v1.0 공개 프리뷰 출시 — Gemini 3 런칭과 동시 발표 |
| 2026-05-19 | **Google I/O 2026**에서 Antigravity 2.0 발표 — 데스크탑 앱 전면 개편, CLI/SDK 추가 |
| 2026-06-18 | Gemini CLI 및 Gemini Code Assist IDE 확장 서비스 종료 (개인/AI Pro 사용자) |

> "Google Antigravity is available today in public preview, at no cost for individuals."
> — [Google Developers Blog, 2025-11-18](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)

공개 프리뷰 시점부터 개인에게는 무료로 제공됐어요. Gemini 3와 같이 발표된 건데, 이건 Antigravity가 단순한 IDE 플러그인이 아니라 Google의 AI 모델 전략과 엮인 제품이라는 뜻이기도 해요.

### 2.2 개발 주체

**Google Antigravity Team** (Google Labs / Google AI 산하) 이 주도했고, Google Cloud의 Gemini 인프라 및 Google DeepMind의 Gemini 3 모델과 긴밀하게 통합되어 있어요. 공식 발표에서는 "Google Antigravity Team"으로 명시되어 있으며, 특정 조직명 코드네임은 공개된 바 없어요.

흥미로운 사실: [Wikipedia의 Antigravity 문서](https://en.wikipedia.org/wiki/Google_Antigravity)에 따르면 Antigravity는 **VS Code를 헤비하게 포크한 버전**이에요. 일부에서는 Windsurf(Codeium의 VS Code 포크)에서 파생됐는지 여부가 논쟁거리가 되기도 했는데, 공식적으로는 VS Code 직접 포크라고 알려져 있어요.

### 2.3 도구 통합 전략

Google I/O 2026에서 눈에 띄는 발표가 하나 더 있어요 — [The Register 보도](https://www.theregister.com/ai-ml/2026/05/20/bye-bye-gemini-cli-google-nudges-devs-toward-antigravity/5243605)에 따르면, **Gemini CLI(Apache 2.0 오픈소스)가 2026년 6월 18일을 기점으로 종료**돼요. 그리고 그 자리를 **Antigravity CLI(클로즈드 소스)**가 대체해요. 개발자들 사이에서 이 오픈소스→클로즈드 전환이 상당한 논쟁을 낳았는데, 이건 아래 커뮤니티 반응 섹션에서 자세히 다뤄볼게요.

---

## 3. 경쟁 도구와 포지셔닝 비교

AI 코딩 도구가 얼마나 많이 쏟아지고 있는지, 정리 안 하면 헷갈리죠. 아래 표로 핵심만 짚어봤어요.

### 3.1 주요 AI 코딩 도구 비교표

| 항목 | **Antigravity 2.0** | **Claude Code** | **Cursor** | **GitHub Copilot Workspace** | **Devin** | **OpenAI Codex CLI** |
|------|---------------------|-----------------|------------|------------------------------|-----------|----------------------|
| **인터페이스** | 데스크탑 앱 (VS Code 포크) + CLI + SDK | 터미널 CLI | VS Code 포크 (데스크탑) | 웹 + GitHub 통합 | 웹 (Slack/Jira 연동) | 터미널 CLI |
| **기반 모델** | Gemini 3.5 Flash (기본), Gemini 3.1 Pro, Claude Sonnet 4.5, GPT-OSS | Claude Opus 4.7 / Sonnet 4.6 | Claude / GPT-4o / Gemini | GPT-4o / Copilot 모델 | DeepSeek + 자체 모델 | GPT-4o / o3 |
| **멀티 에이전트** | 최대 5개 동시 실행 (Manager View) | Agent Teams (프리뷰) | 없음 (순차) | 없음 (순차) | 싱글 에이전트 | 없음 |
| **브라우저 통합** | 내장 Chromium 서브에이전트 | MCP 플러그인 경유 | 없음 | 없음 | 내장 | 없음 |
| **컨텍스트 창** | 1M 토큰 (Gemini 3.1 Pro) | 200K (표준) / 1M (베타) | 모델 의존 | 모델 의존 | 모델 의존 | 모델 의존 |
| **CI/CD 통합** | 미문서화 | GitHub Actions, GitLab CI | 없음 | GitHub 네이티브 | GitHub, Jira, Slack | 없음 |
| **개인 가격** | 무료 프리뷰 / AI Ultra $100/월 | $20~$200/월 | $20/월 (Pro) | $10/월 (Copilot Pro+) | $500/월 | 무료 (API 비용 별도) |
| **엔터프라이즈** | Gemini Enterprise Agent Platform | SOC 2 Type II, HIPAA, SSO | 팀 플랜 $40/월 | GitHub Enterprise | Enterprise 문의 | 없음 |
| **오프라인/온프레미스** | 불가 (클라우드 전용) | 불가 | 불가 | 불가 | 불가 | 불가 |
| **성숙도** | 프리뷰 (실험적) | GA (안정) | GA (안정) | GA (안정) | GA (안정) | GA (안정) |

### 3.2 포지셔닝 요약

[DataCamp 비교 분석](https://www.datacamp.com/blog/claude-code-vs-antigravity)에 따르면 세 도구의 철학적 차이가 명확해요:

- **Cursor** → 인간 중심 정밀 제어, 기존 VS Code 워크플로 유지
- **Claude Code** → 고성능 터미널 에이전트, 깊은 추론 + 감사 추적
- **Antigravity** → 자율 실행 에이전트, AI가 소프트웨어 엔지니어처럼 행동

Antigravity가 가장 미래지향적이지만, 그만큼 가장 불안정한 것도 사실이에요.

---

## 4. 아키텍처와 기술 스택

### 4.1 핵심 설계 철학

Antigravity의 아키텍처를 한 마디로 요약하면 "**에이전트 하네스(Agent Harness)를 중심으로 4개 인터페이스를 제공하는 플랫폼**"이에요.

[MarkTechPost 심층 분석](https://www.marktechpost.com/2026/05/19/google-launches-antigravity-2-0-at-i-o-2026-a-standalone-agent-first-platform-with-cli-sdk-managed-execution-and-enterprise-support/)에 따르면 세 가지 핵심 아키텍처 기둥이 있어요:

1. **Agent Harness** — 추론, 도구 사용, 코드 실행을 격리된 Linux 환경에서 처리
2. **Persistent State Management** — 멀티턴 세션에서 파일과 컨텍스트를 재초기화 없이 유지
3. **Custom Agent Definitions** — 마크다운 파일로 에이전트 행동 정의, Google AI Studio에 템플릿 보관

### 4.2 4개의 서비스 표면 (Antigravity 2.0 기준)

| 컴포넌트 | 역할 | 특징 |
|----------|------|------|
| **Antigravity 2.0 (데스크탑)** | 멀티 에이전트 오케스트레이션 허브 | 동시 에이전트 실행, 스케줄 태스크 |
| **Antigravity CLI** | 터미널 기반 경량 에이전트 | Go로 재작성, Gemini CLI 대체 |
| **Antigravity SDK** | 커스텀 에이전트 구축용 API | 임의 인프라에서 에이전트 호스팅 가능 |
| **Gemini Enterprise Agent Platform** | Google Cloud 기반 엔터프라이즈 배포 | Managed Agents, 격리된 실행 환경 |

### 4.3 지원 모델

[Wikipedia 문서](https://en.wikipedia.org/wiki/Google_Antigravity)와 공식 소스를 종합하면:

- **Gemini 3.5 Flash** — 2.0의 기본 모델, Gemini 3.1 Pro 대비 거의 모든 벤치마크 아웃퍼폼, 4배 빠름
- **Gemini 3.1 Pro** — 1M 토큰 컨텍스트 창 지원
- **Claude Sonnet 4.5 / Claude Opus 4.6** — Anthropic 모델 선택지
- **GPT-OSS-120B** — OpenAI 오픈소스 변형 모델

멀티모달(이미지/스크린샷 처리)은 Gemini 계열 모델이 네이티브 지원해요. Claude 계열은 제한적, GPT-OSS는 텍스트 전용이에요.

### 4.4 두 가지 뷰

```
┌─────────────────────────────────────────────┐
│           Google Antigravity 2.0            │
├──────────────────┬──────────────────────────┤
│   Editor View    │      Manager View         │
│                  │                           │
│  - AI 탭 완성   │  - 에이전트 스폰/종료     │
│  - 인라인 명령  │  - 최대 5개 동시 실행     │
│  - 코드 내비게이션│ - 스케줄 태스크          │
│  - 동기적 작업  │  - 비동기 백그라운드 실행  │
└──────────────────┴──────────────────────────┘
```

Artifacts(산출물) 시스템이 핵심인데요 — 에이전트가 태스크 목록, 구현 계획, 스크린샷, 브라우저 녹화 같은 검증 가능한 결과물을 생성해서 개발자가 중간에 피드백을 줄 수 있어요. Google Docs 스타일의 코멘트 시스템을 사용해요.

### 4.5 Google 생태계 통합

- **Google AI Studio** — 모바일 앱에서 캡처한 아이디어를 Antigravity로 내보내기 (전체 프로젝트 컨텍스트 유지)
- **Firebase** — 백엔드 배포 직접 연동
- **Android / Google Play Console** — 프롬프트로 Android 앱 개발 후 Play Console에 직접 배포
- **Google Workspace API** — Docs, Sheets, Calendar와 프로그래매틱 연동

---

## 5. 사용자 경험 — UI와 워크플로

### 5.1 UI 형태

Antigravity는 **무겁게 수정된 VS Code 포크**예요. VS Code 또는 Cursor에서 설정을 통째로 임포트할 수 있어서 전환 장벽이 낮아요. Open VSX 확장 마켓플레이스를 지원해요 (VS Code Marketplace는 아님).

지원 플랫폼:
- macOS Monterey 12+
- Windows 10+ (64-bit)
- Linux (64-bit, glibc 2.28+, glibcxx 3.4.25+)

### 5.2 에이전트 자율성 3단계

설치 시 세 가지 모드 중 하나를 선택해요:

| 모드 | 설명 | 권장 대상 |
|------|------|----------|
| **Autopilot** | AI가 묻지 않고 모두 실행 | 실험/프로토타이핑 |
| **Agent-Assisted** (추천) | AI가 안전한 자동화 실행, 중요 결정은 확인 | 일반 개발 |
| **Review-Driven** | 거의 모든 액션에 승인 필요 | 보안 중시 환경 |

### 5.3 워크플로 예시 — 논문 요약 AI 서비스 만들기

[피카부랩스 블로그](https://peekaboolabs.ai/blog/google-antigravity-guide)의 실제 사용 후기에 따르면:

> "논문 요약 AI 서비스 만들어줘"라고 프롬프트를 입력했더니 10분 안에 계획 수립 → 코딩 → Vercel 배포 → 오류 수정까지 자동으로 처리됐어요. 단, 토큰 소진으로 세 번 모델을 바꿔야 했어요.

### 5.4 컨텍스트 관리

- **지식 베이스**: `.gemini/antigravity/knowledge/` 폴더에 에이전트가 이전 상호작용에서 학습한 내용 저장 (Claude Code의 `CLAUDE.md`와 유사)
- **Rules**: 코드 스타일 등 전역 규칙 설정 (한국어 지원)
- **Workflows**: 커스텀 명령 템플릿

### 5.5 목소리로도 돼요

네이티브 음성 명령 지원이 2.0에서 추가됐어요. 타이핑 없이 에이전트에게 태스크 지시 가능해요.

---

## 6. 에이전트 능력 벤치마크

[antigravityaiide.com의 벤치마크 페이지](https://antigravityaiide.com/models-benchmarks)에서 발표된 수치를 정리했어요. 단, **이 벤치마크는 2025년 11월 기준 데이터**이며, 타사 독립 검증이 완전히 이루어지지 않은 수치예요. 비판적으로 봐야 해요.

### 6.1 SWE-bench Verified (실세계 GitHub 이슈 해결)

| 모델 | 점수 |
|------|------|
| Gemini 3 Pro (Antigravity) | **76.2%** |
| Claude Sonnet 4.5 (Antigravity) | 71.8% |
| GPT-OSS (Antigravity) | 68.3% |

### 6.2 Terminal-Bench 2.0 (커맨드라인 숙련도)

| 모델 | 점수 |
|------|------|
| Gemini 3 Pro (Antigravity) | **54.2%** |
| Claude Sonnet 4.5 (Antigravity) | 49.7% |
| GPT-OSS (Antigravity) | 45.1% |

### 6.3 WebDev Arena (웹 개발 도전 Elo 레이팅)

| 모델 | Elo |
|------|-----|
| Gemini 3 Pro (Antigravity) | **1487** |
| Claude Sonnet 4.5 (Antigravity) | 1432 |
| GPT-OSS (Antigravity) | 1389 |

### 6.4 벤치마크 신뢰성 주의사항

> "Data noted as of November 2025 with acknowledgment that results may vary by task complexity."
> — antigravityaiide.com

몇 가지 유의점이 있어요:

1. **자사 발표 벤치마크**: Google이 직접 집계한 수치라 독립 재현 검증이 부족해요
2. **태스크 선택 편향**: SWE-bench 하위 셋 선택에 따라 결과가 크게 달라질 수 있어요
3. **Gemini 3.5 Flash 미반영**: 2.0 기본 모델인 Gemini 3.5 Flash의 SWE-bench 점수가 아직 공식 발표되지 않았어요
4. **실사용 후기와의 괴리**: 실제 사용자들은 토큰 제한으로 장시간 작업이 중단되는 경우가 많다고 보고해요

---

## 7. 가격 체계

### 7.1 개인 구독 플랜

| 플랜 | 가격 | Antigravity 한도 | 비고 |
|------|------|-----------------|------|
| **무료 (프리뷰)** | $0 | 기본 한도 (5시간마다 갱신) | 공개 프리뷰 기간 |
| **Google AI Pro** | 미공개 | 기본 한도 | 기존 AI Pro 구독 포함 |
| **Google AI Ultra** | **$100/월** | Pro의 5배 | 2026-05-19 신규 출시 |
| **Google AI Ultra Premium** | **$200/월** | Pro의 20배 | $250에서 인하 |

### 7.2 경쟁사 가격 비교

| 도구 | 최저 유료 플랜 | 비고 |
|------|--------------|------|
| Claude Code Pro | $17/월 (연간) | Claude Sonnet 기반 |
| Cursor Pro | $20/월 | 가장 안정적인 일상 도구 |
| Antigravity AI Ultra | $100/월 | 5x 한도 |
| Devin | $500/월 | 완전 자율 에이전트 |
| GitHub Copilot Pro+ | $10/월 | GitHub 네이티브 |

### 7.3 가격 전략의 맥락

[The Next Web 분석](https://thenextweb.com/news/google-antigravity-2-desktop-cli-sdk-io-2026)에 따르면 AI Ultra $100/월 플랜은 OpenAI ChatGPT Pro($100)와 Anthropic Claude Max($200)와 직접 경쟁하는 위치예요.

주의할 점: 프리뷰 기간 무료 정책이 종료될 경우 유료로 전환될 가능성이 있어요. 토큰 한도 초과 시 작업이 중간에 멈추기 때문에, 실제로 2.0의 병렬 에이전트 기능을 제대로 활용하려면 AI Ultra가 사실상 필수예요.

---

## 8. 개발자 커뮤니티 반응

### 8.1 긍정적 평가

[DEV Community 글](https://dev.to/monsterprogrammer/antigravity-20-google-finally-built-the-dev-environment-nobody-asked-for-but-everyone-needed-57jk)에서는:

> "Antigravity 2.0 might be the announcement that actually rewrites how developers work — for better and for worse."
> (Antigravity 2.0은 개발자 업무 방식을 실제로 다시 쓸 수도 있는 발표다 — 좋게든 나쁘게든.)

병렬 에이전트가 주요 VS Code 포크 중 최초로 1급 기능이 된 것, 그리고 스케줄 태스크로 백그라운드 자동화가 가능해진 것은 분명히 차별화 포인트예요.

### 8.2 한국 개발자 커뮤니티 반응

[Brunch 사용기](https://brunch.co.kr/@a33f93b357b349e/229)와 [엘랜서 블로그](https://www.elancer.co.kr/blog/detail/1046)에서 정리된 한국 개발자들의 공통 의견:

- **장점**: 한국어 프롬프트 완벽 지원, 비개발자도 10분 안에 앱 프로토타입 만들 수 있음, 무료 프리뷰 기간이 매력적
- **단점**: 토큰 제한이 5시간 단위로 걸려서 장시간 작업에 불편, 실무 수준 안정성은 아직 Cursor에 못 미침

### 8.3 부정적 반응 — 2.0 강제 업데이트 사태

[Techloy 보도](https://www.techloy.com/why-googles-antigravity-2-0-ai-update-has-developers-furious/)에 따르면 2.0 출시 당일 심각한 문제가 발생했어요:

> 개발자들은 5월 19일 자동 업데이트 후 자신들의 개발 환경이 망가진 걸 발견했어요. **코드 에디터, 터미널, 파일 탐색기, 소스 컨트롤 도구가 사라졌어요.** 같은 날 Antigravity 2.0이 발표됐지만, 아무도 이게 세 개의 별도 도구로 분리된다는 걸 사전에 안내받지 못했거든요.

Google이 Antigravity 2.0(에이전트), Antigravity IDE(코딩), Antigravity CLI(터미널)로 제품을 분리했는데, 이걸 사전 공지 없이 강제 업데이트로 밀어붙인 거예요. 그 결과:

- Reddit과 Google AI Developers 포럼이 불만으로 넘쳐남
- 사용자들이 v1.23.2로 다운그레이드하고 자동 업데이트를 비활성화
- "비기술적인 사람들이 프로덕션에 코드를 올리는 것 같다"는 비판이 나옴

### 8.4 오픈소스 역주행 비판

[The Register](https://www.theregister.com/ai-ml/2026/05/20/bye-bye-gemini-cli-google-nudges-devs-toward-antigravity/5243605)가 특히 강하게 지적한 부분: Gemini CLI는 **Apache 2.0 라이선스 오픈소스**였는데, 이를 대체하는 Antigravity CLI는 **클로즈드 소스**예요. GitHub 레포지토리에는 코드가 없고 문서와 체인지로그만 있어요.

개발자들은 "커뮤니티 기여를 활용해 독점 제품을 만들었다"고 비판하고 있어요.

---

## 9. 한계와 보안 리스크

### 9.1 보안 취약점 — 실제 발생한 두 가지 CVE

#### 취약점 1: 프롬프트 인젝션 + 샌드박스 탈출 (Pillar Security 발견)

[CyberScoop 보도](https://cyberscoop.com/google-antigravity-pillar-security-agent-sandbox-escape-remote-code-execution/)에 따르면 2026년 1월 발견, 2월 패치됨:

> Strict Mode(가장 엄격한 보안 설정)에서 `find_by_name`이라는 네이티브 파일 탐색 도구가 Strict Mode 평가 이전에 직접 실행될 수 있어, 샌드박스 탈출 및 원격 코드 실행(RCE)이 가능했어요.

Strict Mode는 네트워크 접근 제한, 작업 디렉토리 외부 쓰기 금지, 모든 명령의 샌드박스 내 실행을 보장해야 하는데, 네이티브 도구 분류의 허점으로 무력화됐어요.

#### 취약점 2: 신뢰 작업공간 백도어 (Mindgard 발견)

[Mindgard 블로그](https://mindgard.ai/blog/google-antigravity-persistent-code-execution-vulnerability)에 따르면:

> 악성 "신뢰 작업공간(trusted workspace)"이 영구적인 백도어를 심어 임의 코드를 실행할 수 있었어요. Antigravity 사용의 필수 전제조건인 신뢰 작업공간 메커니즘 자체에 취약점이 있었어요.

현재 두 취약점 모두 패치됐고 Google이 버그 바운티를 지급했어요. 하지만 에이전트형 도구의 공격 표면이 얼마나 넓은지 보여준 사례예요.

### 9.2 데이터 학습 정책

공식 자료에서 코드가 모델 학습에 사용되는지 여부가 명확히 공개되지 않았어요. Google은 프리뷰 기간 중 데이터 처리 정책을 완전히 공개하지 않았어요. **민감 코드를 다루는 기업은 사용 전 반드시 확인이 필요해요.**

### 9.3 GDPR 및 온프레미스 옵션

- 현재 완전 클라우드 전용 서비스예요 (온프레미스 불가)
- Gemini Enterprise Agent Platform이 Google Cloud 내에서 격리 실행을 제공하나, GDPR 컴플라이언스 세부 조건은 공식 미발표 상태예요
- SOC 2 Type II, HIPAA 인증은 현재 미지원 (Claude Code는 지원)

### 9.4 기타 운영상 한계

| 한계 | 세부 내용 |
|------|----------|
| 토큰 제한 | 5시간마다 갱신, 장시간 작업 중단 빈번 |
| 브라우저 통합 | Chrome 전용 (Firefox, Safari 불가) |
| 안정성 | 프리뷰 단계, 버그/불안정 보고 다수 |
| CI/CD 통합 | 공식 문서화 없음 |
| 체크포인트/롤백 | 공식 문서화 없음 |
| 엔터프라이즈 컴플라이언스 | 미출시 |

---

## 10. 빠른 시작 가이드

아래는 [Google Codelabs 공식 가이드](https://codelabs.developers.google.com/getting-started-google-antigravity)와 [Second Talent 설치 가이드](https://www.secondtalent.com/resources/how-to-download-and-install-googles-antigravity-ide/)를 기반으로 정리한 내용이에요. 실제 검증된 흐름만 포함했어요.

### 10.1 시스템 요구사항

```
macOS:   Monterey 12+
Windows: 64-bit Windows 10+ (x64)
Linux:   64-bit, glibc 2.28+, glibcxx 3.4.25+
추가:    Chrome 브라우저 (브라우저 통합 기능 사용 시)
계정:    Gmail 개인 계정
```

### 10.2 설치 흐름

```bash
# 1. 다운로드
# antigravity.google/download 에서 OS별 설치파일 다운로드
# ※ 안정적인 버전을 원한다면 v1.23.2 이하를 명시적으로 선택할 것

# 2. 설치 후 첫 실행 시 설정 마법사
# - 기존 VS Code / Cursor 설정 임포트 여부 선택
# - 에이전트 자율성 모드 선택 (Autopilot / Agent-Assisted / Review-Driven)
# - 터미널 실행 정책, 브라우저 자동화 권한 설정

# 3. Google 계정으로 로그인
# Terms of Use 동의 → 무료 쿼터 활성화
```

### 10.3 첫 태스크 실행

```
1. "Open Folder" → 작업 디렉토리 선택

2. Agent Manager 패널 열기 (Manager View)

3. 태스크 입력 예시:
   "React와 TypeScript로 할 일 목록 앱을 만들어줘.
    로컬 스토리지에 저장하고, 완료 체크박스가 있어야 해."

4. 브라우저 기능 필요 시 → Chrome 확장 설치 프롬프트에 동의

5. Artifacts 패널에서 진행 상황 모니터링
   - 태스크 목록 / 구현 계획 / 스크린샷 실시간 확인

6. 코멘트로 피드백 제공 (에이전트가 중단 없이 반영)
```

### 10.4 컨텍스트 설정 팁

```markdown
# .gemini/antigravity/knowledge/project-rules.md 예시

## 코드 스타일
- TypeScript strict mode 사용
- 함수형 컴포넌트만 (클래스 컴포넌트 금지)
- 주석은 한국어로 작성

## 기술 스택
- Frontend: React 18 + TypeScript
- Styling: Tailwind CSS
- Testing: Vitest + Testing Library
```

---

## 11. 결론 — 지금 써야 할까?

Antigravity는 분명히 **방향은 맞아요**. 병렬 에이전트, 스케줄 태스크, 브라우저 서브에이전트 같은 기능은 경쟁 도구들이 아직 따라오지 못하는 영역이에요.

하지만 **지금 당장 메인 개발 도구로 쓰기에는 이르다는 게** 결론이에요.

| 상황 | 추천 |
|------|------|
| 프로토타이핑, 실험, 학습 | Antigravity (무료 프리뷰 활용) |
| 일상 업무, 안정성 중시 | Cursor 또는 Claude Code |
| 자율 에이전트 + 긴 작업 | Claude Code (Agent Teams) 또는 Devin |
| Google 생태계 (Firebase, Android) | Antigravity (통합 우수) |
| 보안/컴플라이언스 중요 환경 | Claude Code (SOC 2 Type II) |

2.0 강제 업데이트 사태와 Gemini CLI 오픈소스 종료 논란은 단순한 해프닝이 아니에요. Google이 이 제품을 얼마나 신중하게 롤아웃할 의지가 있는지에 대한 의문을 남겼어요.

그럼에도 불구하고 — 무료로 쓸 수 있는 지금이야말로 **부담 없이 실험해볼 최고의 시점**인 건 맞아요. 특히 Google 생태계(Firebase, Android, Workspace)를 많이 쓰는 개발자라면 지금 바로 다운로드해서 써볼 만해요.

---

## 12. 참고문헌

### 1차 공식 자료

1. Google Developers Blog (2025-11-20). [Build with Google Antigravity, our new agentic development platform](https://developers.googleblog.com/build-with-google-antigravity-our-new-agentic-development-platform/)
2. Google Blog (2026-05-19). [I/O 2026 developer highlights: Antigravity, Gemini API, AI Studio](https://blog.google/innovation-and-ai/technology/developers-tools/google-io-2026-developer-highlights/)
3. Google Codelabs. [Getting Started with Google Antigravity](https://codelabs.developers.google.com/getting-started-google-antigravity)
4. Wikipedia. [Google Antigravity](https://en.wikipedia.org/wiki/Google_Antigravity)
5. Google Blog (KR). [[I/O 2026] 에이전트의 미래를 향해: I/O 개발자 하이라이트](https://blog.google/intl/ko-kr/company-news/technology/building-the-agentic-future-kr/)

### 2차 기술 분석

6. MarkTechPost (2026-05-19). [Google Launches Antigravity 2.0 at I/O 2026](https://www.marktechpost.com/2026/05/19/google-launches-antigravity-2-0-at-i-o-2026-a-standalone-agent-first-platform-with-cli-sdk-managed-execution-and-enterprise-support/)
7. The Next Web (2026-05-19). [Google Antigravity 2.0 launches with CLI, SDK, and AI agents](https://thenextweb.com/news/google-antigravity-2-desktop-cli-sdk-io-2026)
8. DataCamp (2026). [Claude Code vs. Antigravity: Which AI Tool Is Better?](https://www.datacamp.com/blog/claude-code-vs-antigravity)
9. Antigravity AI IDE. [AI Models & Benchmarks](https://antigravityaiide.com/models-benchmarks)
10. The Register (2026-05-20). [Bye-bye, Gemini CLI; Google nudges devs toward Antigravity](https://www.theregister.com/ai-ml/2026/05/20/bye-bye-gemini-cli-google-nudges-devs-toward-antigravity/5243605)

### 보안 리서치

11. CyberScoop (2026). [Vuln in Google's Antigravity AI agent manager could escape sandbox](https://cyberscoop.com/google-antigravity-pillar-security-agent-sandbox-escape-remote-code-execution/)
12. The Hacker News (2026-04). [Google Patches Antigravity IDE Flaw Enabling Prompt Injection Code Execution](https://thehackernews.com/2026/04/google-patches-antigravity-ide-flaw.html)
13. Mindgard (2026). [Forced Descent: Google Antigravity Persistent Code Execution Vulnerability](https://mindgard.ai/blog/google-antigravity-persistent-code-execution-vulnerability)

### 커뮤니티 & 리뷰

14. Techloy (2026). [Why Google's Antigravity 2.0 AI Update Has Developers Furious](https://www.techloy.com/why-googles-antigravity-2-0-ai-update-has-developers-furious/)
15. DEV Community (2026). [Antigravity 2.0: Google Finally Built the Dev Environment Nobody Asked For](https://dev.to/monsterprogrammer/antigravity-20-google-finally-built-the-dev-environment-nobody-asked-for-but-everyone-needed-57jk)
16. XDA Developers (2026). [I tried Cursor, Claude Code, and Google Antigravity for a month](https://www.xda-developers.com/tried-cursor-claude-code-google-antigravity-for-month/)

### 한국어 자료

17. 피카부랩스 블로그 (2026). [구글 Antigravity 완벽 가이드](https://peekaboolabs.ai/blog/google-antigravity-guide)
18. 엘랜서 블로그 (2026). [구글 안티그래비티 사용법, Antigravity를 직접 써보니 놀라웠습니다](https://www.elancer.co.kr/blog/detail/1046)
19. Brunch (2026). [구글 Antigravity(안티그래비티) 사용법 총정리](https://brunch.co.kr/@a33f93b357b349e/229)
20. 나무위키. [Antigravity(에디터)](https://namu.wiki/w/Antigravity(%EC%97%90%EB%94%94%ED%84%B0))

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. Antigravity가 기존 코드 완성 도구(Copilot 같은)와 근본적으로 다른 점은 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 코드 한 줄을 제안하는 게 아니라, 작업 단위로 자율적으로 실행하는 "에이전트 우선(agent-first)" 방식이라는 점이에요.

**해설**: Antigravity는 계획 수립부터 파일 생성, 터미널 명령 실행, 브라우저를 통한 UI 테스트까지 에이전트가 스스로 처리해요. 단순 자동완성 도우미가 아니라 AI가 소프트웨어 엔지니어처럼 행동하는 플랫폼을 지향하는 거죠.

</details>

**Q2. OX 문제예요. "Antigravity 2.0의 CLI는 기존 Gemini CLI처럼 Apache 2.0 오픈소스로 공개되어 있다." 맞을까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X (틀렸어요)

**해설**: Gemini CLI는 Apache 2.0 오픈소스였지만, 이를 대체하는 Antigravity CLI는 클로즈드 소스예요. GitHub 레포에는 코드 없이 문서와 체인지로그만 있는데요, 이 오픈소스→클로즈드 전환 때문에 "커뮤니티 기여로 독점 제품을 만들었다"는 비판이 나왔죠.

</details>

**Q3. Antigravity 2.0의 두 가지 뷰, Editor View와 Manager View는 각각 어떤 역할을 할까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Editor View는 AI 탭 완성·인라인 명령 같은 동기적 코딩 작업을, Manager View는 에이전트를 스폰해서 최대 5개까지 동시에 비동기로 실행·관리하는 오케스트레이션을 담당해요.

**해설**: 사람이 직접 코드를 만지는 전통적 작업은 Editor View에서, 여러 에이전트에게 일을 시키고 진행 상황을 지켜보는 건 Manager View에서 하는 구조예요. 병렬 에이전트가 주요 VS Code 포크 중 최초로 1급 기능이 된 게 차별화 포인트죠.

</details>

**Q4. 설치할 때 고르는 에이전트 자율성 3단계 중, 보안이 중요한 환경에서 권장되는 모드는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Review-Driven 모드예요.

**해설**: Autopilot은 AI가 묻지 않고 전부 실행해서 실험·프로토타이핑용이고, Agent-Assisted는 안전한 자동화는 알아서 하되 중요 결정만 확인받는 일반 개발용 추천 모드인데요. Review-Driven은 거의 모든 액션에 승인이 필요해서 보안을 중시하는 환경에 맞아요.

</details>

**Q5. 에이전트가 작업하면서 만드는 "Artifacts(산출물)" 시스템이 왜 중요한 걸까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 태스크 목록, 구현 계획, 스크린샷, 브라우저 녹화 같은 검증 가능한 결과물을 생성해서, 개발자가 작업 중간에 확인하고 피드백을 줄 수 있게 해주기 때문이에요.

**해설**: 자율 에이전트의 가장 큰 불안 요소는 "뭘 하고 있는지 모른다"는 건데요, Artifacts가 그 과정을 투명하게 보여줘요. Google Docs 스타일 코멘트로 피드백을 남기면 에이전트가 중단 없이 반영하죠.

</details>

**Q6. 응용 문제예요. 보안 컴플라이언스(SOC 2 등)가 엄격한 회사에서 일상 업무용 AI 코딩 도구를 골라야 한다면, 본문 기준으로 Antigravity는 적절한 선택일까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 아니요. 본문은 보안/컴플라이언스가 중요한 환경에서는 Claude Code 같은 SOC 2 Type II 지원 도구를 추천해요.

**해설**: Antigravity는 현재 SOC 2 Type II, HIPAA 인증이 없고, 온프레미스도 불가능한 클라우드 전용 서비스인데요. 코드가 모델 학습에 쓰이는지에 대한 데이터 정책도 명확히 공개되지 않아서, 민감 코드를 다루는 기업은 사용 전 반드시 확인이 필요하다고 했죠.

</details>

**Q7. Antigravity에서 실제로 발견됐던 두 가지 보안 취약점은 각각 어떤 방식이었나요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 하나는 Strict Mode에서 네이티브 파일 탐색 도구가 보안 평가 이전에 실행되는 허점을 이용한 프롬프트 인젝션 + 샌드박스 탈출(RCE)이고, 다른 하나는 악성 "신뢰 작업공간"이 영구 백도어를 심는 취약점이었어요.

**해설**: 둘 다 패치됐고 Google이 버그 바운티를 지급했는데요, 에이전트가 파일·터미널·브라우저까지 만지는 만큼 공격 표면이 얼마나 넓어지는지 보여준 사례예요. 에이전트형 도구를 쓸 때 보안 설정을 가볍게 보면 안 되는 이유죠.

</details>

**Q8. 본문 결론 기준으로, 지금 Antigravity를 쓰기 가장 좋은 사람과 아직 이른 사람은 각각 누구일까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 프로토타이핑·실험·학습 목적이거나 Firebase, Android 같은 Google 생태계를 많이 쓰는 개발자에게는 지금 무료 프리뷰가 좋은 기회이고, 안정성이 중요한 일상 업무에는 아직 일러서 Cursor나 Claude Code가 낫다는 게 결론이에요.

**해설**: 병렬 에이전트나 브라우저 서브에이전트처럼 방향성은 앞서 있지만, 프리뷰 단계의 불안정성에 2.0 강제 업데이트 사태까지 겹쳐서 메인 도구로 쓰기엔 리스크가 있다고 했는데요. 무료인 지금 부담 없이 실험해 보는 게 가장 합리적인 활용법이죠.

</details>
