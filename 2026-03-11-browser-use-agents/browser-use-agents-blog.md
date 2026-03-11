# AI가 마우스를 잡다: Browser Use부터 OS 전체 제어까지, 웹·컴퓨터 자동화 에이전트 총정리

> 2026년 3월 기준 | 리서치 by Claude Code

---

## 들어가며 — "AI한테 그냥 대신 해줘" 시대의 서막

요즘 AI 쓰다 보면 이런 생각 한 번쯤 들지 않나요?

> "챗봇에 답 받는 건 알겠는데, 그 답대로 직접 뭔가 해주면 안 되나?"

바로 그 욕구에서 나온 게 **Computer Use(컴퓨터 사용) 에이전트** 계열이에요. AI가 브라우저를 직접 열고, 버튼을 클릭하고, 폼을 채우고, 심지어 파일도 열고 저장하는 것까지 — 사람이 컴퓨터 앞에 앉아서 하는 모든 것을 대신 해주는 거죠.

2024-2025년은 이 분야가 폭발적으로 성장한 시기였어요. 오픈소스부터 빅테크 상용 제품까지, 정말 다양한 플레이어들이 쏟아졌거든요. 이 글에서는 그 전체 지형도를 한눈에 정리해 드릴게요.

---

## 1. 이 기술이 왜 지금 이렇게 뜨나요?

### 1.1 RPA의 한계를 AI가 깨다

기존 [RPA(Robotic Process Automation)](https://en.wikipedia.org/wiki/Robotic_process_automation) 툴들 — UiPath나 Automation Anywhere 같은 것들 — 은 사실 꽤 오래됐어요. 버튼 위치, 텍스트 좌표를 코드로 딱 박아두고 "거기 클릭해!" 하는 방식이거든요. 문제는 웹사이트가 조금만 바뀌어도 스크립트가 통째로 깨진다는 거예요.

반면 AI 기반 에이전트는 화면을 보고 **이해**해요. "로그인 버튼 어디 있지?" 하고 스스로 찾아내거든요. 덕분에 유지보수 비용이 훨씬 줄어들죠.

> "Instead of making specific tools to help Claude complete individual tasks, they're teaching it general computer skills—allowing it to use a wide range of standard tools and software programs designed for people." — [Anthropic, Computer Use 발표문](https://www.anthropic.com/news/3-5-models-and-computer-use)
>
> 번역: "특정 작업을 위한 별도 도구를 만드는 대신, Claude에게 일반적인 컴퓨터 사용 능력을 가르치고 있습니다. 사람을 위해 설계된 다양한 도구와 소프트웨어를 그대로 활용할 수 있도록요."

### 1.2 시장 규모가 증명하는 성장세

[Index.dev의 AI 에이전트 통계](https://www.index.dev/blog/ai-agents-statistics)에 따르면, AI 에이전트 시장은 2025년 기준 78억 달러 규모로, **연간 46.3% 성장률(CAGR)**로 2030년에는 526억 달러에 달할 것으로 예측돼요. Gartner는 2026년 말까지 엔터프라이즈 애플리케이션의 40%에 AI 에이전트가 내장될 것이라고 예측했고요.

---

## 2. 기술 접근 방식 3가지 — 어떻게 화면을 "보나요"?

에이전트가 컴퓨터 화면을 인식하는 방법은 크게 세 가지로 나뉘어요.

| 방식 | 설명 | 장점 | 단점 |
|------|------|------|------|
| **스크린샷 기반** | 화면 이미지를 캡처해 Vision LLM으로 분석 | 어떤 화면이든 동작 | 느리고 좌표 오류 발생 가능 |
| **DOM/HTML 파싱** | 웹페이지 소스코드를 직접 읽음 | 정확하고 빠름 | 동적 콘텐츠에 취약 |
| **접근성 트리(Accessibility Tree)** | 스크린 리더가 사용하는 구조화된 요소 정보 활용 | 빠르고 신뢰성 높음 | 접근성 미지원 사이트에서 실패 |

> "The most capable agents combine approaches. OpenAI's Computer-Using Agent (CUA), which powers both Operator and Atlas, layers screenshot analysis with DOM processing and accessibility tree parsing." — [No Hacks Podcast](https://www.nohackspod.com/blog/how-ai-agents-see-your-website)
>
> 번역: "가장 뛰어난 에이전트들은 여러 방식을 조합합니다. Operator와 Atlas를 구동하는 OpenAI의 CUA는 스크린샷 분석, DOM 처리, 접근성 트리 파싱을 계층적으로 활용합니다."

---

## 3. 브라우저 사용(Browser Use) 계열 에이전트들

### 3.1 Browser Use — 오픈소스 챔피언

[Browser Use](https://browser-use.com/)는 현재 **GitHub 스타 80,300개 이상**을 보유한 브라우저 자동화 분야의 대세 오픈소스 프로젝트예요. 2024년 말 Magnus Muller와 Gregor Zunic이 시작한 이 프로젝트는 순식간에 트렌딩 레포지토리 1위를 차지하며 커뮤니티의 폭발적인 관심을 받았죠.

**핵심 아키텍처:**
- Python + [Playwright](https://playwright.dev/) 기반의 비동기 설계
- 웹페이지 스크린샷과 HTML을 텍스트로 변환해 LLM에게 전달
- OpenAI GPT-4o, Claude, Gemini, Llama 등 다양한 LLM 지원
- Docker 컨테이너 지원으로 격리된 실행 환경 제공

**벤치마크 성과:**

[공식 기술 보고서](https://browser-use.com/posts/sota-technical-report)에 따르면 WebVoyager 벤치마크에서 **89.1%의 성공률**을 달성했어요.

| 웹사이트 | 성공률 | 평균 단계 수 |
|----------|--------|-------------|
| Huggingface | 100% | 9.7 |
| Google Flights | 95% | 36.2 |
| Amazon | 92% | 14.7 |
| GitHub | 92% | 15.9 |
| Apple | 91% | 12.5 |
| Booking.com | 80% | 32.7 |

**가격 정책:**
- 자체 호스팅: 완전 무료
- Cloud API: $0.05/step

> 버전 0.12.1(2026년 3월 3일)까지 **296명의 기여자**와 **118번의 릴리즈**, **8,764번의 커밋**이 이루어진 활발한 프로젝트예요.

---

### 3.2 Anthropic Computer Use — 빅테크의 첫 타석

[Anthropic의 Computer Use](https://www.anthropic.com/news/3-5-models-and-computer-use)는 2024년 10월 Claude 3.5 Sonnet과 함께 베타로 공개된 **데스크톱 전체 제어** 기능이에요. 브라우저뿐 아니라 OS 레벨의 전체 GUI를 제어할 수 있다는 점이 특징이죠.

**작동 방식:**
1. 화면 스크린샷을 주기적으로 캡처
2. 이미지를 좌표 그리드로 변환
3. 버튼, 텍스트 필드, 아이콘의 픽셀 위치를 정밀하게 파악
4. 가상 키보드/마우스로 상호작용 실행

> "By late 2025, with the advent of Claude 4 and Sonnet 4.5, these success rates have climbed into the high 80s for standard office tasks." — [Financial Content](https://www.financialcontent.com/article/tokenring-2025-12-30-the-rise-of-the-digital-intern-how-anthropics-computer-use-redefined-the-ai-agent-landscape)
>
> 번역: "2025년 말, Claude 4와 Sonnet 4.5의 등장으로 일반 오피스 업무에서의 성공률이 80% 후반대로 올라섰습니다."

**현황:**
- [Claude API](https://platform.claude.com/docs/en/agents-and-tools/tool-use/computer-use-tool)를 통해 베타 제공
- Asana, Canva, Cognition, DoorDash, Replit, The Browser Company 등이 파트너로 참여
- 아직 실험적 단계, Zero Data Retention(ZDR) 미지원

---

### 3.3 OpenAI Operator — 잠깐 반짝하고 사라진 제품

[OpenAI Operator](https://openai.com/index/introducing-operator/)는 2025년 1월 23일에 출시되어 ChatGPT Pro(월 $200) 구독자에게 제공됐어요. [TechCrunch](https://techcrunch.com/2025/01/23/openai-launches-operator-an-ai-agent-that-performs-tasks-autonomously/)에 따르면 Web 기반의 자율 에이전트로 큰 주목을 받았지만, **2025년 8월 31일 ChatGPT 에이전트 출시와 함께 서비스 종료**됐어요.

**기술 스택:**
- GPT-4o의 비전 기능 + 강화학습으로 훈련된 CUA(Computer-Using Agent) 모델
- 독립 브라우저 세션에서 작동
- 폼 작성, 온라인 주문, 예약 등의 반복 작업에 특화

**벤치마크:**
- OSWorld(OS 레벨 작업): 38.1%
- WebArena(웹 인터랙션): 58.1%

---

### 3.4 Google Project Mariner — Gemini의 브라우저 에이전트

[Google Project Mariner](https://deepmind.google/models/project-mariner/)는 Google DeepMind가 개발한 웹 브라우징 AI 에이전트예요. 2024년 12월 처음 발표되어 [Google I/O 2025](https://techcrunch.com/2025/05/20/google-rolls-out-project-mariner-its-web-browsing-ai-agent/)에서 정식 출시됐어요.

**특징:**
- Gemini 2.5 Pro 기반으로 구동
- Chrome 확장 프로그램 형태로 브라우저 내 작동
- 클라우드 VM 기반으로 **최대 10개 작업 동시 처리** 가능
- 텍스트, 이미지, 버튼, 폼, 코드 등 웹 페이지 전 요소 파싱
- Google Search AI Mode와 연동해 레스토랑 예약, 티켓 검색 등 통합

**한계:**
- 현재 미국의 Google AI Ultra 구독자에게만 제공
- 아직 실험적 단계

---

### 3.5 Playwright MCP — 개발자를 위한 정밀 자동화

[Microsoft의 Playwright MCP](https://github.com/microsoft/playwright-mcp)는 2025년 3월 출시된 MCP(Model Context Protocol) 서버로, Playwright를 LLM이 직접 제어할 수 있게 해주는 도구예요.

기존 스크린샷 방식과 달리 **접근성 트리(Accessibility Tree)** 방식을 채택해 더 빠르고 안정적인 자동화를 제공해요.

> "Unlike traditional automation which relies on manual scripts or pixel-based inputs, Playwright MCP uses the browser's accessibility tree — a structured, text-based representation of a webpage — for fast, deterministic control." — [Codemify](https://codemify.com/pageplaywritestepbystep)
>
> 번역: "수동 스크립트나 픽셀 기반 입력에 의존하는 전통적 자동화와 달리, Playwright MCP는 빠르고 결정론적 제어를 위해 브라우저의 접근성 트리를 활용합니다."

**특이점:**
- GitHub Copilot의 코딩 에이전트와 통합되어 개발 워크플로우 자동화
- E2E 테스트, 웹 스크래핑, 폼 자동화에 최적화
- 비전 모델이나 스크린샷 불필요

---

### 3.6 Skyvern — LLM + Computer Vision 융합

[Skyvern](https://www.skyvern.com/)은 LLM과 컴퓨터 비전을 결합한 브라우저 자동화 플랫폼으로, GitHub 스타 20,000개 이상을 보유하고 있어요.

**독특한 아키텍처 — Skyvern 2.0:**
- **Planner**: 고수준 목표 유지
- **Actor**: 개별 단계 실행
- **Validator**: 액션 후 화면을 확인해 성공 여부 검증

특히 "Route Memorization" 기능이 흥미로운데, AI가 처음 경로를 파악하면 이를 고속 Playwright 스크립트로 "컴파일"해두고, 사이트가 변경되면 AI가 다시 깨어나 경로를 "치유(heal)"하는 방식이에요.

> "$2.7M 시드 투자를 받으며 '브라우저 자동화를 고치겠다'는 비전으로 시작한 스타트업" — [Skyvern 블로그](https://www.skyvern.com/blog/skyvern-we-raised-2-7m-to-fix-browser-automation-open-source/)

---

### 3.7 Stagehand — TypeScript 개발자의 선택

[Browserbase의 Stagehand](https://github.com/browserbase/stagehand)는 TypeScript 기반의 AI 브라우저 자동화 프레임워크예요. MIT 라이선스로 오픈소스이며, 2025년 v3로 재아키텍처되어 **44% 속도 향상** 및 네이티브 CDP(Chrome DevTools Protocol) 통합을 달성했어요.

**v3의 혁신:**
- 발견된 요소와 액션을 자동 캐싱 → 추가 LLM 추론 비용 없이 재사용
- AI 네이티브 설계로 처음부터 재구성
- Stagehand API를 통한 클라우드 인프라 통합

---

### 3.8 Steel Browser — 인프라 걱정 없는 브라우저 샌드박스

[Steel Browser](https://github.com/steel-dev/steel-browser)는 "배터리 포함(batteries-included)"을 표방하는 오픈소스 브라우저 API예요. AI 에이전트가 인프라 걱정 없이 웹을 자동화할 수 있도록 브라우저 샌드박스 환경을 제공해요.

---

## 4. OS 전체 제어 계열 에이전트들

### 4.1 OpenClaw — 190,000 스타의 신성

[OpenClaw](https://openclaw.ai/)는 오스트리아 개발자 Peter Steinberger가 2025년 11월 주말 프로젝트로 시작한 오픈소스 자율 AI 에이전트예요. 원래 이름은 Clawdbot이었다가 상표 문제로 OpenClaw로 이름을 바꿨고, **출시 약 90일 만에 190,000개 GitHub 스타**를 돌파하는 기록을 세웠어요.

**작동 방식:**
- Signal, Telegram, Discord, WhatsApp 등 메시징 플랫폼을 UI로 사용
- 로컬에서 실행되며 Claude, DeepSeek, GPT 등 외부 LLM과 연결
- OS 레벨에서 이메일, 캘린더, 메시징, 파일 시스템에 접근

**주의사항:**
[Malwarebytes의 보안 분석](https://www.malwarebytes.com/blog/news/2026/02/openclaw-what-is-it-and-can-you-use-it-safely)에 따르면, 광범위한 시스템 접근 권한이 필요하기 때문에 잘못 구성된 인스턴스는 보안·프라이버시 위험을 초래할 수 있어요.

---

### 4.2 Open Interpreter — 코드로 컴퓨터를 지배하다

[Open Interpreter](https://github.com/openinterpreter/open-interpreter)는 LLM이 로컬 컴퓨터에서 코드(Python, JavaScript, Shell 등)를 실행할 수 있게 해주는 오픈소스 도구예요. ChatGPT 같은 인터페이스에서 자연어로 명령하면 코드를 생성하고 즉시 실행해요.

**핵심 능력:**
- OS Mode + Computer API를 통한 GUI 레벨 액션 (스크린샷 캡처, 브라우저 조작 등)
- 비전 기능으로 이미지 분석 및 해석
- Ollama, LM Studio 등을 통한 로컬 모델 지원
- 데이터 분석, 스크립팅, 파일 관리에 특히 강력

---

### 4.3 Manus — 중국의 완전 자율 에이전트

[Manus](https://en.wikipedia.org/wiki/Manus_(AI_agent))는 우한 스타트업 Butterfly Effect가 개발해 2025년 3월 6일 공식 출시한 완전 자율 AI 에이전트예요. 출시 당시 [MIT Technology Review](https://www.technologyreview.com/2025/03/11/1113133/manus-ai-review/)가 "전 세계 AI 커뮤니티가 주목하고 있다"고 평가했을 만큼 큰 반향을 일으켰어요.

**차별점:**
- 사용자가 연결을 끊어도 클라우드에서 계속 작업 지속
- 한 번의 세션에서 **50개 이상의 화면**을 넘나들며 작업
- X(트위터), Telegram 등 다양한 소스에서 정보 수집
- "Manus's Computer" 창을 통해 사용자가 실시간 감독 및 개입 가능

**GAIA 벤치마크 성과:**
- Level 1: ~86.5%
- Level 3: ~57.7%

**2025년 후속 사건:**
2025년 12월 Meta가 약 20-30억 달러에 인수 발표, 2026년 1월 중국 당국의 규제 심사 착수.

---

## 5. 주요 제품 종합 비교

### 5.1 접근 방식 비교

| 제품 | 개발사 | 타입 | 제어 범위 | 인식 방식 | 오픈소스 |
|------|--------|------|-----------|-----------|----------|
| Browser Use | 커뮤니티 | 라이브러리 | 브라우저 | 스크린샷+HTML | O (MIT) |
| Computer Use | Anthropic | API | OS 전체 | 스크린샷 | X |
| Operator | OpenAI | 제품 (종료) | 브라우저 | 스크린샷+DOM | X |
| Project Mariner | Google | 제품 | 브라우저 | 스크린샷+접근성트리 | X |
| Playwright MCP | Microsoft | MCP 서버 | 브라우저 | 접근성 트리 | O (MIT) |
| Skyvern | Skyvern-AI | 플랫폼 | 브라우저 | LLM+CV 혼합 | O |
| Stagehand | Browserbase | 프레임워크 | 브라우저 | AI+접근성트리 | O (MIT) |
| Open Interpreter | openinterpreter | 도구 | OS 전체 | 코드 실행+스크린샷 | O (MIT) |
| OpenClaw | Peter Steinberger | 에이전트 | OS 전체 | LLM 기반 | O |
| Manus | Butterfly Effect | 제품 | OS+웹 | 멀티모달 | X |

### 5.2 가격 및 접근성

| 제품 | 가격 | 접근 방법 |
|------|------|-----------|
| Browser Use | 무료 / $0.05/step (Cloud) | pip install |
| Computer Use | Claude API 토큰 기반 | API 키 |
| Project Mariner | Google AI Ultra 구독 ($249.99/월) | Chrome 확장 |
| Playwright MCP | 무료 | npm install |
| Skyvern | 무료 (오픈소스) / 상용 플랜 | self-host or API |
| Open Interpreter | 무료 | pip install |
| OpenClaw | 무료 | self-host |

### 5.3 기술 스택 비교

| 제품 | 주요 언어 | 기반 기술 | LLM 지원 |
|------|-----------|-----------|----------|
| Browser Use | Python | Playwright | OpenAI, Claude, Gemini, Ollama |
| Playwright MCP | TypeScript | Playwright (접근성 트리) | 모든 MCP 호환 |
| Skyvern | Python | Playwright + CV | 다중 LLM |
| Stagehand | TypeScript | CDP 네이티브 | Claude, OpenAI |
| Open Interpreter | Python | 코드 실행 엔진 | 다중 (로컬 포함) |

---

## 6. RPA vs AI 에이전트 — 뭐가 달라요?

전통적 RPA와 새로운 AI 에이전트의 차이를 이해하는 건 중요해요.

| 구분 | 전통 RPA (UiPath, AA) | AI 브라우저 에이전트 |
|------|----------------------|---------------------|
| 규칙 정의 | 명시적 코드/규칙 필요 | 자연어 지시만으로 가능 |
| 유지보수 | UI 변경 시 전면 재작업 | 자가 적응 (Self-healing) |
| 학습 비용 | 높음 (전용 IDE 필요) | 낮음 (자연어) |
| 복잡한 판단 | 어려움 | 가능 (LLM 추론) |
| 신뢰성 | 높음 (규칙 기반) | 아직 개선 중 |
| 거버넌스 | 성숙한 엔터프라이즈 기능 | 초기 단계 |
| 가격 | 높음 (엔터프라이즈 라이선스) | 다양 (무료~API 기반) |

Gartner 2025 Magic Quadrant에서 [UiPath](https://www.relevancelab.com/post/uipath-vs-other-rpa-platforms)가 RPA 부문 6년 연속 1위를 차지하고 있지만, AI 에이전트의 약진으로 RPA 대형 플레이어들도 AI 통합에 속도를 내고 있어요. UiPath는 이미 NLP, ML, IDP를 플랫폼에 내장했고, Automation Anywhere는 AARI(Robotic Interface) 2026으로 인간-봇 협업을 강화하고 있죠.

---

## 7. 벤치마크로 보는 실제 성능

여러 벤치마크들이 에이전트 성능을 측정하고 있어요.

| 벤치마크 | 측정 내용 | 현재 최고 성능 |
|---------|----------|---------------|
| **WebVoyager** | 15개 웹사이트 자연어 태스크 완수율 | Surfer 2: 97.1% |
| **OSWorld** | OS 레벨 50단계 워크플로우 | Simular Agent S2: 34.5% |
| **GAIA Level 3** | 복잡한 현실 세계 태스크 | Writer's Action Agent: 61% |
| **CUB** | 실제 106개 비즈니스 워크플로우 | Writer's Action Agent: 10.4% |
| **WebArena** | 현실적 웹 인터랙션 | 다양 |

> WebVoyager에서는 90%대 성공률이 나오는데, 실제 비즈니스 워크플로우 벤치마크(CUB)에서는 10%대에 그치는 걸 볼 수 있어요. 벤치마크와 실전의 갭이 아직 크다는 의미이기도 하죠.

---

## 8. 2025-2026 주요 트렌드

### 트렌드 1: "클라우드 VM" 모델의 부상
Project Mariner, Manus처럼 에이전트가 클라우드 서버에서 작동하고 사용자는 결과만 받는 모델이 확산되고 있어요. 로컬 리소스를 아끼면서 보안도 강화할 수 있거든요.

### 트렌드 2: 멀티 에이전트 오케스트레이션
Gartner는 Q1 2024 대비 Q2 2025에 멀티 에이전트 시스템 문의가 **1,445% 증가**했다고 밝혔어요. 단일 에이전트에서 팀으로의 전환이 가속화되고 있는 거죠.

### 트렌드 3: MCP(Model Context Protocol) 생태계
Anthropic이 제안한 MCP가 업계 표준으로 자리 잡으면서, Playwright MCP를 비롯한 다양한 MCP 서버들이 에이전트가 도구를 사용하는 방식을 표준화하고 있어요.

### 트렌드 4: 접근성 트리 중심으로 이동
초기의 단순 스크린샷 방식에서 벗어나 접근성 트리를 활용하는 방식이 더 빠르고 신뢰성 높다는 게 입증되면서, 주요 에이전트들이 이 방향으로 이동하고 있어요.

### 트렌드 5: 오픈소스의 폭발적 성장
Browser Use(80K+ 스타), OpenClaw(190K+ 스타) 같은 오픈소스 프로젝트들이 빅테크 상용 제품을 능가하는 커뮤니티 관심을 받고 있어요.

---

## 9. 주요 활용 사례

| 분야 | 활용 사례 | 추천 도구 |
|------|----------|-----------|
| 리서치/정보 수집 | 여러 사이트 탐색, 데이터 취합 | Browser Use, Manus |
| E-커머스 | 가격 비교, 주문, 재고 확인 | Operator (구), Skyvern |
| 업무 자동화 | CRM 입력, 이메일 처리, 폼 작성 | Computer Use, Open Interpreter |
| 소프트웨어 테스팅 | E2E 테스트 자동화 | Playwright MCP, Stagehand |
| 데이터 스크래핑 | 웹 데이터 수집 | Steel Browser, Browser Use |
| 개인 비서 | 예약, 쇼핑, 일정 관리 | OpenClaw, Manus |

---

## 마치며 — 인간 감독은 여전히 필수

이 기술들이 아무리 발전했어도, 현시점에서는 여전히 **인간 감독(Human-in-the-loop)**이 중요해요. 실제 비즈니스 워크플로우 벤치마크(CUB)에서 최고 성능이 10%대에 그친다는 것이 현실을 잘 보여주죠.

그러나 방향은 명확해요. AI가 마우스를 잡고 직접 일을 처리하는 세상은 이미 시작됐고, 그 속도는 점점 빨라지고 있어요. 2024년에 "신기한 데모"였던 것들이 2026년에는 일상 도구가 되어가고 있는 거죠.

> "By 2026, IDC expects AI copilots to be embedded in nearly 80% of enterprise workplace applications, reshaping how teams work, decide, and execute." — [Master of Code](https://masterofcode.com/blog/ai-agent-statistics)
>
> 번역: "2026년까지 IDC는 AI 코파일럿이 엔터프라이즈 업무 애플리케이션의 80% 가까이에 내장될 것으로 예측하며, 이는 팀이 일하고, 결정하고, 실행하는 방식을 근본적으로 바꿀 것입니다."

어떤 도구를 선택하든, 지금 이 생태계를 이해하고 있다는 것 자체가 큰 경쟁력이 될 거예요. 서둘러 실험해보세요!

---

## 참고문헌

1. [Browser Use 공식 사이트](https://browser-use.com/) — 브라우저 사용 공식 문서 및 SOTA 리포트
2. [Anthropic Computer Use 발표](https://www.anthropic.com/news/3-5-models-and-computer-use) — Claude Computer Use 공식 발표
3. [OpenAI Operator 발표](https://openai.com/index/introducing-operator/) — Operator 공식 출시 발표
4. [Google Project Mariner](https://deepmind.google/models/project-mariner/) — DeepMind 공식 페이지
5. [Playwright MCP GitHub](https://github.com/microsoft/playwright-mcp) — Microsoft Playwright MCP 레포지토리
6. [Skyvern GitHub](https://github.com/Skyvern-AI/skyvern) — Skyvern 오픈소스 레포지토리
7. [Open Interpreter GitHub](https://github.com/openinterpreter/open-interpreter) — Open Interpreter 레포지토리
8. [OpenClaw GitHub](https://github.com/openclaw/openclaw) — OpenClaw 레포지토리
9. [Stagehand GitHub](https://github.com/browserbase/stagehand) — Browserbase Stagehand 레포지토리
10. [Manus Wikipedia](https://en.wikipedia.org/wiki/Manus_(AI_agent)) — Manus AI 에이전트 위키
11. [Helicone 비교 분석](https://www.helicone.ai/blog/browser-use-vs-computer-use-vs-operator) — Browser Use vs Computer Use vs Operator 비교
12. [o-mega AI 벤치마크 가이드](https://o-mega.ai/articles/the-2025-2026-guide-to-ai-computer-use-benchmarks-and-top-ai-agents) — 2025-2026 벤치마크 종합 가이드
13. [TechCrunch - Operator 출시](https://techcrunch.com/2025/01/23/openai-launches-operator-an-ai-agent-that-performs-tasks-autonomously/) — OpenAI Operator 출시 기사
14. [TechCrunch - Project Mariner 출시](https://techcrunch.com/2025/05/20/google-rolls-out-project-mariner-its-web-browsing-ai-agent/) — Google Project Mariner 출시 기사
15. [Index.dev AI 에이전트 통계](https://www.index.dev/blog/ai-agents-statistics) — AI 에이전트 시장 통계
