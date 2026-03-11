# OpenClaw 완전 정복: 메신저 하나로 내 AI 비서를 24시간 굴리는 법

> 아직도 ChatGPT 창 열어서 하나하나 물어보고 계세요? 그거 너무 불편하잖아요 ㅎㅎ OpenClaw는 그냥 카톡 보내듯 Telegram에 한 줄 보내면, AI가 알아서 웹 뒤지고, 파일 정리하고, 코드까지 고쳐줘요. 그것도 24시간 내내요.

---

## 목차

1. [OpenClaw이 뭐야? — 한 줄 요약부터](#openclaw이-뭐야)
2. [어떻게 이렇게 빨리 유명해졌나 — 전설적인 탄생 스토리](#어떻게-이렇게-빨리-유명해졌나)
3. [이름이 세 번이나 바뀐 이유 — Clawdbot → Moltbot → OpenClaw](#이름이-세-번이나-바뀐-이유)
4. [핵심 기능 해부 — 도대체 뭘 할 수 있나요](#핵심-기능-해부)
5. [기술 아키텍처 — 내부는 어떻게 생겼나](#기술-아키텍처)
6. [실전 활용 사례 — 사람들이 진짜로 쓰는 방법](#실전-활용-사례)
7. [생태계 확장 — ClawHub, nanobot, ClawWork](#생태계-확장)
8. [보안 주의사항 — 이건 꼭 알아야 해요](#보안-주의사항)
9. [장단점 솔직 정리](#장단점-솔직-정리)
10. [Peter Steinberger OpenAI 합류 — 앞으로 어떻게 될까](#peter-steinberger-openai-합류)
11. [참고문헌](#참고문헌)

---

## OpenClaw이 뭐야?

[OpenClaw](https://openclaw.ai/)는 **여러분의 기기 위에서 24시간 돌아가는 오픈소스 개인용 AI 에이전트**예요.

ChatGPT가 "대화 창에서 질문하면 답 해주는 챗봇"이라면, OpenClaw는 그것보다 훨씬 더 나아가요. 파일을 열 수 있고, 웹을 직접 돌아다닐 수 있고, 쉘 명령어를 날릴 수 있고, 스케줄에 맞춰 자동으로 일을 처리해요. 심지어 여러분이 자는 동안에도요.

> "Unlike standard chatbots like ChatGPT, it has 'eyes and hands'—it can browse the web, read and write files, and run shell commands autonomously." — [DigitalOcean](https://www.digitalocean.com/resources/articles/what-is-openclaw)

직역하면 이래요: "ChatGPT 같은 일반 챗봇과 달리, OpenClaw는 '눈과 손'을 가지고 있어요. 웹을 브라우징하고, 파일을 읽고 쓰고, 쉘 명령어를 자율적으로 실행할 수 있거든요."

이게 얼마나 차별화된 거냐 하면 — **기존 AI 도구들은 대부분 여러분이 쓰러워야 반응**해요. OpenClaw는 반대로 **AI가 먼저 일하고 여러분에게 보고**해주는 구조예요.

어떤 메신저 앱으로든 연결할 수 있어요. Telegram, WhatsApp, Discord, Signal, iMessage, Slack, Microsoft Teams... 무려 20개 이상의 플랫폼을 지원하거든요. 쓰던 메신저 그대로 쓰면서 AI 비서를 부릴 수 있는 거예요.

| 항목 | 내용 |
|------|------|
| 개발자 | Peter Steinberger (오스트리아) |
| 라이선스 | MIT (완전 오픈소스) |
| GitHub 스타 | 302,000+ (2026년 3월 기준) |
| GitHub 포크 | 57,100+ |
| 커밋 수 | 18,000+ |
| 지원 LLM | OpenAI GPT, Anthropic Claude, Google Gemini, DeepSeek, 로컬(Ollama) |
| 지원 채팅 플랫폼 | 20개 이상 |
| ClawHub 스킬 수 | 3,200+ |

---

## 어떻게 이렇게 빨리 유명해졌나?

솔직히 이 프로젝트의 성장 속도는 좀 비현실적이에요 ㅋㅋ

**2025년 11월**: Peter Steinberger가 주말 프로젝트로 만들기 시작했어요.

> "출시 후 72시간 내에 GitHub에서 60,000개 이상의 별을 획득했다." — [DigitalOcean](https://www.digitalocean.com/resources/articles/what-is-openclaw)

72시간에 6만 스타예요. 하루 2만 개 꼴이에요. 웬만한 유명 오픈소스 프로젝트가 수년 걸려 쌓는 숫자를 3일 만에 찍은 거거든요.

**왜 이렇게 폭발적이었냐고요?** 타이밍이 기가 막혔어요:

1. **2025년 하반기 AI 에이전트 붐** — 모두가 "AI가 일 대신 해주는 시대"를 기다리고 있었는데, 실제로 작동하는 걸 보여준 거예요
2. **완전 무료 + 오픈소스** — OpenAI Operator나 Manus는 돈 내야 하잖아요. OpenClaw는 공짜예요
3. **내 기기에서 돌아간다** — 클라우드에 데이터 보내기 싫은 사람들한테 딱이었어요
4. **메신저 연동** — 별도 앱 없이 쓰던 메신저로 쓸 수 있다는 점이 진입장벽을 확 낮췄어요

> "The open-source project has 247,000 stars and 47,700 forks on GitHub as of March 2, 2026." — [DigitalOcean](https://www.digitalocean.com/resources/articles/what-is-openclaw)

불과 4개월 만에 25만 스타를 찍었고, 이후 2026년 3월 현재는 **30만 스타를 돌파**했어요. 이 성장 속도는 [GitHub 역사상 가장 빠른 오픈소스 성장 사례](https://github.com/openclaw/openclaw) 중 하나로 기록되고 있어요.

---

## 이름이 세 번이나 바뀐 이유

이게 좀 드라마틱해요 ㅋㅋ

### 1단계: Clawdbot (2025년 11월 출시)

처음 이름은 **Clawdbot**이었어요. 만든 사람이 원래 **Clawd(지금의 Molty)**라는 AI 비서를 갖고 있었는데, 그 이름 자체가 Anthropic의 Claude에서 따온 거잖아요. Clawdbot도 그 계보에서 나온 이름이었죠.

### 2단계: Moltbot (2026년 1월 27일)

> "Renamed 'Moltbot' on January 27, 2026, following trademark complaints by Anthropic, as the name phonetically resembled Claude." — [NxCode](https://www.nxcode.io/resources/news/openclaw-complete-guide-2026)

Anthropic이 상표권 문제를 제기했어요. "Clawd"라는 이름이 자사 브랜드 Claude와 너무 비슷하다는 거죠. 그래서 **로브스터 탈피(molt)** 개념을 따서 Moltbot으로 이름을 바꿨어요.

근데 이게 또 문제가 생겼어요. 이름을 바꾸자마자 사이버범죄자들이 유사 도메인, 복제 GitHub 저장소를 만들어서 악성코드를 배포하기 시작한 거예요. [Malwarebytes가 이를 보고](https://www.malwarebytes.com/blog/threat-intel/2026/01/clawdbots-rename-to-moltbot-sparks-impersonation-campaign)했을 정도였어요.

### 3단계: OpenClaw (2026년 1월 30일)

> "On January 29, 2026, the project was renamed again. OpenClaw combined two ideas the maintainers wanted to emphasize going forward: open-source development and continuity with the original claw motif." — [NxCode](https://www.nxcode.io/resources/news/openclaw-complete-guide-2026)

이번엔 자발적 이름 변경이었어요. **오픈소스 정체성**과 **원래의 발톱(claw) 모티프**를 살리는 방향으로. 그래서 OpenClaw가 됐어요.

이름 변천 과정이 오히려 프로젝트의 폭발적 성장과 맞물려서 더 많은 관심을 받았어요. "이름이 계속 바뀌는 저 프로젝트가 뭐야?" 하고 사람들이 찾아보기 시작한 거거든요.

---

## 핵심 기능 해부

### 1. 멀티채널 메신저 연동

OpenClaw의 가장 큰 특징이에요. 새 앱을 설치할 필요 없이 **지금 쓰는 메신저를 그대로** 써요.

지원 플랫폼:
- **메신저**: WhatsApp, Telegram, Signal, LINE, Zalo
- **업무용**: Slack, Discord, Microsoft Teams, Google Chat, Mattermost
- **Apple**: iMessage (BlueBubbles), iOS 앱
- **소셜/기타**: Twitch, Nostr, Matrix, IRC, Feishu, Tlon

```
# Telegram에서 이렇게 보내면
"어제 받은 이메일 중 미팅 관련된 거 요약해줘"

# OpenClaw가 자동으로
# 1. Gmail에 접근
# 2. 어제 이메일 필터링
# 3. 미팅 관련 이메일 파악
# 4. 요약 작성
# 5. Telegram으로 답장
```

### 2. 브라우저 자동화

[GitHub 공식 문서](https://github.com/openclaw/openclaw)에 따르면, OpenClaw 전용 Chrome/Chromium을 통해 웹 탐색, 폼 작성, 파일 업로드까지 가능해요.

스크린샷 기반이 아닌 **접근성 트리(Accessibility Tree) 방식**을 쓰기 때문에 더 정확하고 빨라요. 최신 자동화 에이전트 추세와도 일치하는 방향이에요.

### 3. 파일 시스템 접근

- 파일 읽기/쓰기
- 폴더 정리
- 문서 변환
- 코드 파일 분석 및 수정

### 4. 쉘 명령어 실행

샌드박스 모드와 전체 시스템 접근 모드 중 선택 가능해요. 개발자라면 이게 진짜 강력한 기능이에요. 배포, 테스트, 빌드를 자연어 명령 하나로 처리할 수 있으니까요.

### 5. 스케줄 자동화 (Cron)

> "Cron + Wake-ups: 스케줄 실행" — [OpenClaw 공식 GitHub](https://github.com/openclaw/openclaw)

매일 아침 9시에 뉴스 요약 받기, 주마다 경쟁사 분석 보고서 생성하기, 이런 걸 크론 작업으로 설정할 수 있어요. 한번 설정해두면 알아서 돌아가요.

### 6. 장기 메모리

> "마크다운 문서로 데이터를 저장하여 깊은 개인화와 지시사항 수동 조정 가능" — [DigitalOcean](https://www.digitalocean.com/resources/articles/what-is-openclaw)

마크다운 파일로 기억을 저장해요. 여러분이 좋아하는 작업 스타일, 자주 쓰는 포맷, 이전에 내린 결정들을 AI가 기억하고 다음에 반영해요.

### 7. 음성 인터페이스

- macOS/iOS: Wake Words 감지
- Android: 지속적 음성 모드
- ElevenLabs 및 시스템 TTS 지원

### 8. Live Canvas (시각적 워크스페이스)

A2UI를 활용한 에이전트 제어 시각 워크스페이스예요. AI가 작업하는 걸 시각적으로 볼 수 있어요.

---

## 기술 아키텍처

OpenClaw의 내부 구조는 이렇게 생겼어요:

```
[메신저 앱] ←→ [Gateway] ←→ [Pi Agent Runtime] ←→ [LLM]
                    ↕                ↕
              [WebSocket]        [Skills/MCP]
                    ↕
              [Local Storage]
```

### 핵심 컴포넌트

**1. Gateway (로컬 WebSocket 제어평면)**
- 기본 주소: `ws://127.0.0.1:18789`
- 모든 채널의 메시지를 수신하고 라우팅
- 세션 관리, 권한 제어

**2. Pi Agent Runtime**
- 실제 추론을 담당하는 에이전트 런타임
- RPC 모드로 도구 스트리밍 지원
- 모든 LLM 제공자와 연결

**3. Skills / MCP 서버**
- 모든 스킬은 **MCP(Model Context Protocol) 서버**
- 핫-리로드 지원 (재시작 없이 스킬 추가/제거)

**4. 설정 파일**
```json
// ~/.openclaw/openclaw.json
{
  "gateway": { "port": 18789 },
  "channels": { "telegram": { "token": "..." } },
  "model": { "provider": "anthropic", "model": "claude-3-7-sonnet" },
  "plugins": ["web-search", "file-manager", "code-runner"]
}
```

### 런타임 요구사항

```bash
# Node.js 22 이상 필요
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

[GitHub 공식 저장소](https://github.com/openclaw/openclaw)에 따르면 npm, pnpm, bun 모두 지원해요.

### 지원 LLM

| 제공자 | 모델 |
|--------|------|
| OpenAI | GPT-4o, GPT-4.5, o3 |
| Anthropic | Claude 3.7 Sonnet, Claude 3.5 |
| Google | Gemini 2.0 Flash, Gemini 2.5 Pro |
| DeepSeek | DeepSeek-V3, DeepSeek-R1 |
| 로컬 | Ollama 통한 모든 로컬 모델 |

---

## 실전 활용 사례

### 개발자를 위한 사용 사례

**코드 리팩토링 자동화**

> "Claude Code 세션을 자동으로 실행하고 테스트를 진행하며 오류를 해결하고 PR을 열기까지." — [OpenClaw 공식 사이트 사용자 후기](https://openclaw.ai/)

```
# Telegram에서 보내는 명령
"레거시 API v2 코드를 v3로 전부 업그레이드하고,
 테스트 돌려보고, 통과하면 PR 만들어줘"
```

**인프라 자동화**

```
# 매일 아침 자동 실행 (Cron 설정)
"서버 상태 체크하고 이상 있으면 나한테 알려줘"
```

### 비즈니스를 위한 사용 사례

**경쟁사 모니터링** ([Forward Future 리포트](https://forwardfuture.ai/p/what-people-are-actually-doing-with-openclaw-25-use-cases)):

> "Competitor analysis runs on weekly schedules, scraping competitor websites for product changes, pricing updates, and news, with OpenClaw formatting this into structured reports."

매주 자동으로 경쟁사 사이트 스크래핑 → 가격/제품 변화 감지 → 구조화된 보고서 작성까지 다 해줘요.

**SNS 콘텐츠 자동화**:

> "X and LinkedIn automation dominates, where users connect their blog RSS feed and have OpenClaw automatically generate platform-specific posts, with one user reporting saving 10+ hours per week on social media alone." — [TLDL](https://www.tldl.io/blog/openclaw-use-cases-2026)

블로그 RSS를 연결해두면, 새 글이 올라올 때마다 자동으로 X용, LinkedIn용 포스트를 만들어줘요. 주당 10시간 이상 절약됐다는 사람도 있어요.

### 개인 생산성을 위한 사용 사례

**이메일 정리**:

> "OpenClaw process large volumes of email: unsubscribing from noise, categorizing by urgency, drafting replies for review, and clearing thousands of messages over a few days." — [TLDL](https://www.tldl.io/blog/openclaw-use-cases-2026)

스팸 수신거부, 긴급도별 분류, 답장 초안 작성을 알아서 해줘요.

**회의 노트 자동화**:

> "Meeting notes are transcribed and summarized automatically, with OpenClaw identifying action items and emailing them to participants."

회의 녹음을 넣으면 → 요약 → 액션 아이템 추출 → 참가자들에게 이메일까지 보내줘요.

**스마트홈 제어**: Home Assistant 연동으로 자연어로 스마트홈 디바이스 제어도 돼요.

---

## 생태계 확장

### ClawHub — 스킬 마켓플레이스

[ClawHub](https://openclawlaunch.com/guides/openclaw-clawhub)는 3,200개 이상의 커뮤니티 제작 스킬을 제공해요. 모든 스킬은 MCP 서버 형태로 되어 있어요.

주요 스킬 카테고리:

| 카테고리 | 예시 스킬 |
|----------|-----------|
| 웹 & 검색 | web-search, browser, scraper |
| 코딩 | code-runner, git, github-actions |
| 파일 | file-manager, pdf-reader, image-gen |
| 생산성 | calendar, email-drafter, notion |
| 자동화 | http-request, cron-scheduler, webhook |
| 소셜미디어 | twitter, linkedin, reddit |
| 분석 | ga4, analytics, sheets |

> "Every skill on ClawHub — OpenClaw's skill marketplace — is an MCP server, and when you enable a skill, OpenClaw connects to that MCP server and makes its tools available to your AI agent." — [OpenClaw Launch](https://openclawlaunch.com/guides/openclaw-mcp)

### nanobot — 초경량 OpenClaw

[홍콩대 HKUDS 연구팀](https://github.com/HKUDS/nanobot)이 2026년 2월 2일에 공개한 프로젝트예요. "Ultra-Lightweight OpenClaw"라는 부제처럼, OpenClaw의 99% 작은 코드로 핵심 기능을 구현했어요.

- 핵심 코드 약 4,000줄 (Python)
- OpenClaw의 수백만 줄 대비 극도로 간결
- MCP 통합, 멀티채널 지원 유지
- 9,000+ GitHub 스타 (출시 한 달 만에)
- 로컬 LLM (vLLM) 지원

**학습용으로 최적**이에요. OpenClaw 소스 읽기 버거운 분들한테 nanobot이 훨씬 접근하기 쉬워요.

### ClawWork — AI 동료 (코워커)

[HKUDS의 ClawWork](https://github.com/HKUDS/ClawWork)는 "$15K earned in 11 Hours"라는 타이틀처럼 실제 돈 버는 프리랜서 작업을 AI가 대신하는 걸 목표로 해요. OpenClaw를 업무용 코워커로 활용하는 확장 프로젝트예요.

### 파생 프로젝트들

OpenClaw의 성공을 보고 유사 프로젝트들이 우후죽순으로 생겼어요 ㅋㅋ [Medium 아티클](https://evoailabs.medium.com/openclaw-nanobot-picoclaw-ironclaw-and-zeroclaw-this-claw-craziness-is-continuing-87c72456e6dc)에서 "Claw Craziness"라고 부를 정도예요:

- **ZeroClaw**: 제로샷 특화
- **PicoClaw**: 더 경량화
- **IronClaw**: 엔터프라이즈 보안 강화
- **NullClaw**: 최소 의존성 버전

---

## 보안 주의사항

이건 진짜 알아야 해요. 좋은 것만 얘기하고 싶지 않고요, 솔직하게 얘기할게요.

### 1. ClawJacked — 심각한 취약점

> "OpenClaw's Control UI accepts a gatewayUrl parameter from the query string and automatically establishes a WebSocket connection without user confirmation, allowing attackers to exfiltrate authentication tokens and then connect to modify configuration to disable sandboxing and execute arbitrary commands." — [The Hacker News](https://thehackernews.com/2026/02/clawjacked-flaw-lets-malicious-sites.html)

악성 웹사이트가 여러분의 로컬 OpenClaw에 무단으로 연결해서, 설정을 바꾸고 임의 명령을 실행할 수 있는 취약점이에요. 2026년 2월에 발견됐고 CVE-2026-25253으로 등록됐어요.

### 2. 악성 스킬 문제

> "Security firm Koi Security conducted an audit of all 2,857 skills available on ClawHub and found 341 malicious skills across multiple campaigns, with 335 traced back to a single coordinated operation dubbed 'ClawHavoc'." — [Microsoft Security Blog](https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/)

ClawHub에 올라온 스킬 중 341개(약 12%)가 악성 코드를 담고 있었어요. 주로 크립토 트레이딩 봇, 생산성 도구로 위장했어요.

**이렇게 하면 돼요:**
- 스킬 설치 전 반드시 GitHub 저장소 확인
- 별 수, 최근 업데이트 일자, 리뷰 확인
- 검증되지 않은 스킬은 설치하지 말기

### 3. 노출 인스턴스 문제

> "Over 40,000 exposed instances" — 보안 분석 보고서

기본 설정을 그대로 쓰면서 외부에 포트를 열어둔 인스턴스가 4만 개 이상이에요. 외부에서 완전히 접근 가능한 상태로요.

**기본 설정 `dmPolicy="pairing"` 절대 바꾸지 마세요.** `openclaw doctor` 명령으로 현재 보안 상태를 정기 점검하는 것도 필수예요.

### 4. AI 소셜 엔지니어링

> "Controlling the agent via chat apps means that it's not just the employee that becomes a target for social engineering, but also their AI agent." — [Cisco Blogs](https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare)

메신저 기반이라 AI 에이전트를 직접 공격하는 사이버 공격이 새로 생겼어요. AI 계정 탈취, AI 행세가 현실적인 위협이에요.

---

## 장단점 솔직 정리

### 좋은 점

**오픈소스, 완전 무료**
MIT 라이선스예요. 상업적 사용도 되고, 수정해도 되고, 재배포해도 돼요. Manus나 Devin처럼 월 수십만 원 낼 필요 없어요.

**모델 선택 자유도**
OpenAI만 써야 하는 게 아니에요. Claude 쓸 수도 있고, DeepSeek 쓸 수도 있고, 로컬 모델 돌릴 수도 있어요. API 비용 최적화가 가능해요.

**내 기기에서 작동 → 프라이버시**
데이터가 내 기기 밖으로 나가지 않아요(LLM API 호출 제외). 민감한 업무 자동화에 적합해요.

**20개 이상 메신저 지원**
새 앱 안 배워도 돼요. 기존 워크플로우에 자연스럽게 녹여넣을 수 있어요.

**3,200+ 커뮤니티 스킬**
직접 코딩 안 해도 웬만한 통합은 다 있어요.

**활발한 커뮤니티**
18,000+ 커밋, 5,000+ PR이 말해주듯 개발 속도가 엄청나요.

### 아쉬운 점

**초기 설정 복잡도**
기술 숙련도가 없으면 자체 호스팅이 2~6시간 걸릴 수 있어요. 서버 관리 개념을 모르면 좀 어렵죠.

**API 비용 발생**
OpenClaw 자체는 무료지만, LLM API 비용은 따로 내야 해요. 무거운 작업이 많으면 월 $50 이상도 가능해요.

**보안 리스크**
솔직히 현재로선 보안이 완벽하지 않아요. 최신 패치 적용, 보안 설정 검토가 필수예요.

**쉘 실행 권한 주의**
AI가 쉘 명령어를 실행할 수 있다는 게 양날의 검이에요. 잘못된 명령이 시스템에 영향을 줄 수 있어요.

**창업자가 OpenAI로 이직**
Peter Steinberger가 2026년 2월에 OpenAI로 가버렸어요. 오픈소스 파운데이션으로 이관된다고 했지만, 장기 방향성이 좀 불확실해졌죠.

---

## Peter Steinberger OpenAI 합류

2026년 2월 14일, OpenClaw의 창시자 Peter Steinberger가 OpenAI 합류를 발표했어요.

> "Sam Altman on X: 'Peter Steinberger is joining OpenAI to drive the next generation of personal agents. He is a genius with a lot of amazing ideas about the future of very smart agents interacting with each other to do very useful things for people.'" — [TechCrunch](https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/)

Sam Altman이 직접 X에서 발표했어요. "다음 세대의 개인용 에이전트를 이끌 천재"라고 소개했죠.

Peter 본인의 말:

> "OpenClaw를 거대한 회사로 키울 수 있었겠지만, 그게 나한테는 사실 별로 흥미롭지 않아요. OpenAI와 함께하는 것이 이걸 모든 사람에게 가장 빠르게 가져다 주는 방법이에요." — [steipete.me](https://steipete.me/posts/2026/openclaw)

OpenClaw는 오픈소스 파운데이션으로 이관되어 계속 유지/발전될 예정이에요. OpenAI도 "OpenClaw는 오픈소스로 살아남는다"고 발표했고요.

오스트리아 출신 개발자가 주말에 만든 프로젝트가 4개월 만에 30만 스타를 찍고, 세계에서 가장 유명한 AI 회사의 눈에 들어서 합류까지 — 진짜 AI 시대 신화 같은 이야기네요.

---

## 정리하며

OpenClaw는 **"AI가 나를 위해 일한다"는 개념을 가장 대중적이고 접근하기 쉬운 방식으로 구현**한 프로젝트예요.

완전 무료, 오픈소스, 내 기기에서 돌아가고, 쓰던 메신저로 쓸 수 있고, 3,200개 스킬로 확장 가능하고.

물론 보안 주의사항도 있고, 초기 설정 허들도 있어요. 하지만 이 정도 기능을 이 정도 가격(=무료)에 쓸 수 있다는 건 진짜 대단한 일이에요.

만약 자동화 좋아하는 분이라면, 혹은 반복 작업에 지친 개발자라면 한번 써보시는 걸 추천해요. 처음 설정하는 데 2시간 투자해두면 이후에 수십 시간을 돌려받을 수 있을 테니까요.

---

## 참고문헌

| 번호 | 제목 | 출처 | URL |
|------|------|------|-----|
| 1 | OpenClaw 공식 GitHub | openclaw/openclaw | https://github.com/openclaw/openclaw |
| 2 | OpenClaw 공식 웹사이트 | openclaw.ai | https://openclaw.ai/ |
| 3 | What is OpenClaw? | DigitalOcean | https://www.digitalocean.com/resources/articles/what-is-openclaw |
| 4 | OpenClaw Complete Guide 2026 | NxCode | https://www.nxcode.io/resources/news/openclaw-complete-guide-2026 |
| 5 | OpenClaw Moltbot Rebrand | Malwarebytes | https://www.malwarebytes.com/blog/threat-intel/2026/01/clawdbots-rename-to-moltbot-sparks-impersonation-campaign |
| 6 | OpenClaw MCP Guide | OpenClaw Launch | https://openclawlaunch.com/guides/openclaw-mcp |
| 7 | ClawHub Guide | OpenClaw Launch | https://openclawlaunch.com/guides/openclaw-clawhub |
| 8 | Getting Started with OpenClaw | All Things Open | https://allthingsopen.org/articles/getting-started-openclaw-autonomous-agent |
| 9 | nanobot GitHub | HKUDS | https://github.com/HKUDS/nanobot |
| 10 | ClawWork GitHub | HKUDS | https://github.com/HKUDS/ClawWork |
| 11 | ClawJacked Vulnerability | The Hacker News | https://thehackernews.com/2026/02/clawjacked-flaw-lets-malicious-sites.html |
| 12 | Running OpenClaw Safely | Microsoft Security Blog | https://www.microsoft.com/en-us/security/blog/2026/02/19/running-openclaw-safely-identity-isolation-runtime-risk/ |
| 13 | CISO Security Analysis | Trend Micro | https://www.trendmicro.com/en_us/research/26/c/cisos-in-a-pinch-a-security-analysis-openclaw.html |
| 14 | Peter Steinberger Joins OpenAI | TechCrunch | https://techcrunch.com/2026/02/15/openclaw-creator-peter-steinberger-joins-openai/ |
| 15 | Sam Altman on OpenClaw | X (Twitter) | https://x.com/sama/status/2023150230905159801 |
| 16 | OpenClaw Use Cases 2026 | TLDL | https://www.tldl.io/blog/openclaw-use-cases-2026 |
| 17 | What People Actually Do with OpenClaw | Forward Future | https://forwardfuture.ai/p/what-people-are-actually-doing-with-openclaw-25-use-cases
| 18 | Cisco Security Blog | Cisco | https://blogs.cisco.com/ai/personal-ai-agents-like-openclaw-are-a-security-nightmare |
| 19 | Peter Steinberger Blog | steipete.me | https://steipete.me/posts/2026/openclaw |
| 20 | Awesome OpenClaw Usecases | GitHub hesamsheikh | https://github.com/hesamsheikh/awesome-openclaw-usecases |
| 21 | CNBC - OpenClaw Rise | CNBC | https://www.cnbc.com/2026/02/02/openclaw-open-source-ai-agent-rise-controversy-clawdbot-moltbot-moltbook.html |
| 22 | OpenClaw vs Manus | FluxPix | https://flypix.ai/openclaw-vs-manus-ai/ |
| 23 | Claw Craziness Article | Medium | https://evoailabs.medium.com/openclaw-nanobot-picoclaw-ironclaw-and-zeroclaw-this-claw-craziness-is-continuing-87c72456e6dc |
| 24 | OpenClaw Kaspersky Analysis | Kaspersky | https://www.kaspersky.com/blog/openclaw-vulnerabilities-exposed/55263/ |
