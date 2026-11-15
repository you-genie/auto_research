# 데일리 트렌드 브리프 — 2026-11-15 (일)

> 범위: 2026-11-12 ~ 11-15 (최근 24~72시간) · 관심 도메인: **AI 에이전트 / LLM / 개발자 도구**
> 표기 규칙: 한글 설명 + 영어 원문 (주요 키워드는 *[발음]* 병기)
> ⚠️ = 1차 출처 미확인(애그리게이터 단일 보도)

---

## TL;DR — 오늘 꼭 알아야 할 5가지

1. **엔비디아(NVIDIA) CEO 젠슨 황 사임** — 33년 만. CFO 콜렛 크레스(Colette Kress)가 임시 CEO(*Interim CEO [인터림 씨이오]*). SEC 8-K로 확인. 실적 발표 직전.
2. **앤트로픽(Anthropic) IPO 6배 초과청약(*Oversubscribed [오버섭스크라이브드]*)** — 11/18 공모가 확정, 11/19 나스닥 상장(티커 **ANT**). 공모가 밴드 $70–78, 기업가치 약 $1.4T.
3. **OpenAI, ChatGPT Wallet [월렛] 출시** — 에이전트가 사용자 대신 결제. 카드번호 대신 네트워크 토큰(*Tokenization [토크나이제이션]*) + 생체인증. 미국 Pro 사용자 한정.
4. **비영리단체 4곳, 프런티어 AI 개발 중단 소송** — OpenAI·Anthropic·Google·Meta·SpaceX AI 상대로 "더 강력한 모델 개발 금지" 가처분(*Injunction [인정크션]*) 청구.
5. **에이전트 인프라 오픈소스화 가속** — Cloudflare **Kitesurf [카이트서프]** 브라우저 엔진 공개, LangChain $300M 시리즈C.

---

## 1. 트렌딩 키워드 & 토픽

| 키워드 | 발음 | 한 줄 설명 |
|---|---|---|
| **Agentic Commerce** | 에이전틱 커머스 | AI 에이전트가 직접 구매·결제까지 수행. ChatGPT Wallet, Google AP2, Visa/Mastercard 에이전트 결제 프로그램이 같은 방향 |
| **Agent Skills** | 에이전트 스킬즈 | 코딩 에이전트에 도메인 지식을 패키지로 주입. GitHub 트렌딩 상위권 다수가 "스킬 번들" (Google, NVIDIA, 커뮤니티) |
| **MCP (Model Context Protocol)** | 엠씨피 | 에이전트-도구 연결 표준. Chrome DevTools MCP, Stitch MCP 등 대형 벤더가 계속 채택 |
| **AG-UI (Agent-User Interaction)** | 에이지-유아이 | 에이전트 ↔ 프론트엔드 UI 연결 프로토콜. MCP(도구), A2A(에이전트 간)에 이어 "UI 계층" 표준 경쟁 |
| **Headless / Agent Browser** | 헤들리스 / 에이전트 브라우저 | Chromium보다 가벼운 에이전트 전용 브라우저 엔진 (Kitesurf) |
| **Frontier AI Freeze** | 프런티어 에이아이 프리즈 | 최첨단 모델 개발 동결 요구 — 소송·규제 이슈로 부상 |
| **AI IPO** | 에이아이 아이피오 | Anthropic 상장 — AI 랩의 공개시장 진입 시험대 |
| **Spec-Driven Development** | 스펙 드리븐 디벨롭먼트 | 명세 먼저 쓰고 에이전트가 구현 (github/spec-kit). "결정론(*Determinism [디터미니즘]*)" 확보 흐름 |

---

## 2. 주목받는 GitHub 저장소

GitHub Trending(일간, 11/15 기준) 직접 확인. 거의 전부가 **에이전트용 도구**라는 점이 핵심.

| 저장소 | 언어 | ⭐ 전체 / 오늘 | 설명 |
|---|---|---|---|
| [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | TS | 7.0K / **+1,220** | 코딩 에이전트에게 최신 웹 모범사례(*Best Practice*)를 주입하는 가이드 소스 |
| [dream-num/univer](https://github.com/dream-num/univer) | TS | 25.5K / **+1,041** | 사람과 AI 에이전트를 위한 오피스 SDK (스프레드시트·문서 편집·계산·협업) |
| [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | TS | 11.7K / +860 | 에이전트의 계획(*Plan*)에 주석·리뷰·피드백을 다는 워크스페이스 |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | TS | 56.8K / +718 | 코딩 에이전트용 Chrome DevTools (MCP 서버) |
| [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | Py | 5.4K / +707 | 주식 투자·트레이딩용 Claude Code 스킬 모음 |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | Go | 51.9K / +688 | 결정론적 파이프라인 + LLM 에이전트 하이브리드 코드 리뷰 |
| [Tencent/LoopForge](https://github.com/Tencent/LoopForge) | Go | 1.4K / +484 | CodeBuddy·Codex·Claude Code를 승인 게이트(*Approval Gate [어프루벌 게이트]*)와 함께 오케스트레이션 |
| [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | TS | 17.7K / +393 | Agent-User Interaction 프로토콜 |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | TS | 9.2K / +248 | Stitch MCP용 에이전트 스킬 (디자인→코드) |
| [NVIDIA/SkillEvaluator](https://github.com/NVIDIA/SkillEvaluator) | Py | 1.5K / +205 | 에이전트 스킬 품질 게이트·라이브 평가 프레임워크 |
| [cloudflare Kitesurf](https://blog.cloudflare.com/kitesurf-open-source/) | Rust/Wasm | 신규 | 아래 4번 뉴스 참고 |

**Hugging Face 트렌딩 모델 (11/15)**
- [thinkingmachines/Inkling-2-Small](https://hf.co/thinkingmachines/Inkling-2-Small) — Thinking Machines의 Apache-2.0 MoE 멀티모달 모델 (11/4 공개)
- [moonshotai/Kimi-K3.1-Pro](https://hf.co/moonshotai/Kimi-K3.1-Pro) — Moonshot의 최신 오픈 웨이트 플래그십 (11/2)
- [MiniMaxAI/MiniMax-H3-Image](https://hf.co/MiniMaxAI/MiniMax-H3-Image) — 이미지 생성·편집, 다운로드 57만+
- [Zyphra/ZONOS3-Mini](https://hf.co/Zyphra/ZONOS3-Mini) — 다국어 TTS(*Text-to-Speech*)·보이스 클로닝 (11/9)
- [NousResearch/Arete-27B](https://hf.co/NousResearch/Arete-27B) — Qwen3.8-27B 기반 가치 정렬(*Value Alignment [밸류 얼라인먼트]*) SFT
- [speridlabs/idol](https://hf.co/speridlabs/idol) — 이미지→3D, 가우시안 스플래팅(*Gaussian Splatting [가우시안 스플래팅]*)
- 참고: 상위 1위는 "uncensored/heretic [언센서드/헤러틱]" 증류(*Distillation*) 모델 — 검열 제거 파인튜닝 수요가 여전히 큼

---

## 3. 모니터링할 만한 기술·프레임워크

| 기술 | 발음 | 왜 봐야 하나 |
|---|---|---|
| **Kitesurf** | 카이트서프 | Blitz(HTML/레이아웃)+Stylo(CSS)+Boa(JS, Wasm)로 조립한 무상태(*Stateless [스테이트리스]*) 엔진. CDP 호환이라 기존 Puppeteer 스크립트 그대로 연결. 에이전트 브라우징 비용 구조를 바꿀 잠재력 |
| **AG-UI** | 에이지-유아이 | 오늘 트렌딩 +393. 에이전트 프로토콜 3층(MCP/A2A/AG-UI) 중 UI 계층 표준 후보 — 이전 글 [OpenIntelligentUI 서베이](../2026-10-23-open-intelligent-ui/)와 연결 |
| **Agent Skill Evaluation** | 에이전트 스킬 이밸류에이션 | 스킬이 범람하면서 "스킬 품질 측정"이 다음 과제 (NVIDIA SkillEvaluator) |
| **Network Payment Tokens** | 네트워크 페이먼트 토큰 | 에이전트 결제의 보안 기반. 에이전트가 실제 카드번호를 보지 않음 |
| **Hybrid Code Review** | 하이브리드 코드 리뷰 | 정적 분석(결정론) + LLM 판단 결합 — 에이전트 생성 코드 검증 수요 증가 |
| **Gemini 4 라인업** | 제미나이 포 | Argon(프런티어) → Carbon(11/10 GA) → **Hydrogen [하이드로젠]**(11/13, 저가·고속 에이전트용). 3단 모델 구조 |

---

## 4. 최근 24~72시간 주요 뉴스

### 🏢 산업·기업
- **엔비디아 CEO 젠슨 황 사임 (11/12)** — CFO 콜렛 크레스가 CFO 겸 임시 CEO. 이사회는 내·외부 후보 검토 중. 사임 배경으로 사생활 관련 의혹이 보도됨(어디까지나 의혹). 주가 하락, 며칠 후 실적 발표 예정.
  [CNBC](https://www.cnbc.com/2026/11/12/nvidia-jensen-huang-ceo-live-updates.html) · [SEC 8-K](https://www.sec.gov/Archives/edgar/data/0001045810/000104581026000082/nvidiaannouncesceotransiti.htm) · [CNN](https://www.cnn.com/2026/11/12/tech/jensen-huang-nvidia-resigns)
- **Anthropic IPO 약 6배 초과청약** — 8.25억 주, $70–78, 최대 약 $64.4B 조달. 11/18 가격 확정 → 11/19 나스닥(ANT). 주관 Goldman Sachs·Morgan Stanley. 밴드 상향 검토설 있음.
  [Yahoo Finance](https://finance.yahoo.com/markets/stocks/articles/anthropic-ipo-reportedly-oversubscribed-company-143329410.html) · [StockAnalysis](https://stockanalysis.com/news/anthropic-ipo-six-times-oversubscribed/) · [TipRanks](https://www.tipranks.com/news/anthropics-ant-ipo-is-six-times-oversubscribed-as-investor-demand-builds)
- **LangChain $300M 시리즈C, 기업가치 $3B (11/13)** — CapitalG 리드. 자금은 에이전트 플랫폼 LangSmith에 집중. 이전 라운드($1.25B) 대비 2.4배.
  [LangChain 블로그](https://www.langchain.com/blog/series-c) · [Law360](https://www.law360.com/articles/2549981/software-biz-langchain-valued-at-3b-after-300m-fundraise)
- ⚠️ **CrowdStrike, AI 에이전트 보안 스타트업 2곳 $495M 인수** — 애그리게이터 단일 보도, 공식 발표 미확인.

### 🤖 제품·모델
- **OpenAI ChatGPT Wallet (11/13)** — Amex·Mastercard·Visa 협력. 상시 에이전트 "dots [닷츠]" 대화에서만 동작, 매 결제 생체인증. 미국 Pro·미국 발급 신용카드 한정. 추후 한도 내 사전승인 결제 지원 예정. OpenAI는 출시 시점에 수수료를 받지 않음.
  [Cointelegraph](https://cointelegraph.com/news/openai-ai-payments-chatgpt-wallet-visa-mastercard-amex) · [gHacks](https://www.ghacks.net/2026/11/15/openai-launches-chatgpt-wallet-so-agents-can-pay-without-seeing-your-card-details/) · [Fintech Magazine](https://fintechmagazine.com/news/openai-launches-chatgpt-wallet-for-secure-ai-agent-payments)
- **Google Gemini 4 Hydrogen (11/13)** — 에이전트 워크플로우용 "데일리 드라이버" 모델. Gemini 앱(무료 자동선택), AI Studio, Gemini API, Search에 배포. ⚠️ 출력 $7.50/1M 토큰 가격은 애그리게이터 보도만 있음.
  [Google 블로그](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-hydrogen/)
- **Cloudflare Kitesurf 오픈소스 공개 (11/12–13, Apache 2.0)** — 아직 실험(*Experimental [익스페리멘털]*) 단계, 웹 호환성 미완성. Workers Paid 플랜 필요.
  [Cloudflare 블로그](https://blog.cloudflare.com/kitesurf-open-source/) · [Changelog](https://developers.cloudflare.com/changelog/post/2026-11-12-kitesurf-open-source/) · [Phoronix](https://www.phoronix.com/news/Cloudflare-Kitesurf-Open-Source)
- (이번 주 맥락) **Claude Fable 5.2 / Mythos 5.2 (11/9)** — 가격 20% 인하($8/$40), 최대 30% 빠름. [9to5Mac](https://9to5mac.com/2026/11/09/anthropic-upgrades-claude-with-new-fable-5-2-model-details-here/) · [The New Stack](https://thenewstack.io/anthropic-fable-coding-upgrade/)

### ⚖️ 정책·법률
- **비영리 4곳, 프런티어 AI 동결 소송 (11/12, 샌프란시스코)** — Public Citizen, Heat Initiative, Alliance for Secure AI, Irreplaceable Education Fund. 캘리포니아 불공정경쟁법(UCL) 상 공공 방해(*Public Nuisance [퍼블릭 뉴선스]*) 논리. 에이전트가 테스트 환경을 벗어나 외부 시스템에 접근한 사례들을 근거로 제시. Anthropic IPO 일주일 전 제기.
  [Claims Journal](https://www.claimsjournal.com/news/national/2026/11/13/341283.htm) · [Just Security](https://www.justsecurity.org/164494/nonprofits-lawsuit-freeze-frontier-ai-development/) · [Dataconomy](https://dataconomy.com/2026/11/13/nonprofits-sue-openai-google-and-meta-to-halt-advanced-ai)

---

## 5. 관전 포인트 (다음 주)
- **11/18–19 Anthropic 공모가·상장 첫날** — 밴드 상향 여부, 소송 리스크 반영 여부
- **엔비디아 실적 발표** — 리더십 공백 속 가이던스, 후임 CEO 후보(Arm의 르네 하스 거론 ⚠️)
- **에이전트 결제 표준 경쟁** — OpenAI Wallet vs Google AP2 vs 카드사 자체 프로그램, 머천트 측 봇 차단 정책
- **블로그 주제 후보**: "에이전트 프로토콜 3층 구조(MCP·A2A·AG-UI)", "에이전트 전용 브라우저 엔진 비교(Kitesurf vs Chromium headless vs agent-desktop)"

---

### 수집 한계
- GitHub Trending·Hugging Face는 직접 조회. Hacker News(news.ycombinator.com) 및 일부 애그리게이터는 세션 네트워크 정책상 접근 불가 → 검색 결과로 대체.
- ⚠️ 표시 항목은 공식 출처 확인 전까지 참고용.
