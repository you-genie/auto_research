# 데일리 테크 트렌드 리포트 — 2026-11-14 (토)

> 조사 기준: 2026-11-13 ~ 11-14 (최근 24~48시간) · 관심 도메인: AI 에이전트(AI Agent) / LLM / 개발자 도구
> 표기 규칙: **한글 (English 원문, [영어 발음])**
> ⚠️ 일부 항목은 뉴스레터·애그리게이터 기반이라 **[미확인]** 으로 표시했습니다. 1차 출처로 교차 확인된 항목은 **[확인]** 입니다.

---

## 🔑 한 줄 요약

1. **엔비디아(Nvidia, [엔비디아]) CEO 젠슨 황(Jensen Huang) 사임**, CFO 콜렛 크레스(Colette Kress)가 임시 CEO를 맡았습니다. AI 하드웨어 생태계 전체에 영향을 주는 이번 주 최대 이슈입니다.
2. **앤트로픽(Anthropic, [앤쓰로픽]) IPO 청약이 수 배 초과**. 11/18 공모가 확정, 11/19 나스닥(Nasdaq) 상장 예정입니다.
3. GitHub 트렌딩은 **"에이전트용 인프라(Agent Infrastructure)"** 가 장악했습니다. 디자인 시스템, 브라우저/데스크톱 자동화, 스킬(Skills), 코드 리뷰가 상위권입니다.

---

## 1. 트렌딩 키워드 & 토픽 (Trending Keywords)

| 키워드 | 발음 | 설명 |
|---|---|---|
| **에이전틱 커머스 (Agentic Commerce)** | [에이전틱 커머스] | AI 에이전트가 사용자 대신 결제·구매를 수행하는 흐름. OpenAI "ChatGPT Wallet" 유출 보도, Visa 토큰화 카드, United Airlines가 개인 AI 에이전트의 항공권 예약을 차단한다는 보도가 동시에 나왔습니다. |
| **에이전트 하네스 (Agent Harness)** | [에이전트 하-니스] | 모델 바깥에서 루프·도구·샌드박스·세션을 관리하는 런타임 계층. DeepSeek Harness, Tencent LoopForge 등 빅테크 오픈소스 경쟁이 이어지고 있습니다. |
| **에이전트 스킬 (Agent Skills)** | [에이전트 스킬즈] | 에이전트에 주입하는 재사용 가능한 절차·지식 패키지. anthropics/skills, addyosmani/agent-skills, 도메인 특화 스킬(트레이딩 등)이 동시에 트렌딩 중입니다. |
| **컴퓨터 유즈 (Computer Use)** | [컴퓨터 유-즈] | 에이전트가 브라우저와 데스크톱 GUI를 직접 조작하는 기능. vercel-labs의 agent-browser와 agent-desktop이 강세입니다. |
| **토큰 절감 (Token Efficiency)** | [토큰 이피션시] | 프롬프트 압축용 프록시와 스킬. caveman(약 65% 절감 주장)의 스타가 12만에 육박합니다. |
| **AI 거버넌스 / 책임성 (Accountability)** | [어카운터빌러티] | 가짜 AI 인용 판례를 쓴 변호사 4명 전원이 사건에서 배제되었습니다. FAA는 AI 관제 시스템이 지상 정지 사태와 관련 있는지 조사 중입니다(인과관계는 미확인). |

---

## 2. 떠오르는 GitHub 저장소 (Emerging Repositories)

### 📈 이번 주 (Weekly) 상위

| 저장소 | 언어 | ⭐ 총 / 주간 | 한 줄 설명 |
|---|---|---|---|
| [meta/astryx](https://github.com/meta/astryx) | TS | 28.0k / **+13.4k** | Meta가 공개한 **AI 에이전트용 디자인 시스템(Design System, [디자인 시스템])**. 생성형 UI(Generative UI) 흐름의 연장선에 있습니다. |
| [milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot) | TS | 22.7k / +7.8k | VM 기반의 오픈소스 봇 실행 환경 |
| [anthropics/skills](https://github.com/anthropics/skills) | Py | 194.5k / +6.2k | 공식 Agent Skills 저장소 |
| [google/elephant-goldfish-model](https://github.com/google/elephant-goldfish-model) | Py | 19.1k / +5.6k | 에이전트와 함께 소프트웨어를 설계·리뷰하는 플러그인 |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Rust | 51.1k / +4.4k | 에이전트용 **브라우저 자동화 CLI** |
| [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills) | JS | 117.5k / +3.5k | 프로덕션급 코딩 에이전트 스킬 모음 |

### 🔥 오늘 (Daily) 급상승

| 저장소 | ⭐ 오늘 | 설명 |
|---|---|---|
| [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | **+1,225** | 코딩 에이전트가 최신 웹 베스트 프랙티스를 따르도록 돕는 가이드 소스 |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | +897 | 결정론적 파이프라인과 LLM 에이전트를 결합한 **하이브리드 코드 리뷰** 도구 (Go) |
| [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | +673 | DevTools를 **MCP (Model Context Protocol, [엠씨피])** 로 에이전트에 노출 |
| [tradermonty/claude-trading-skills](https://github.com/tradermonty/claude-trading-skills) | +556 | 주식 투자자용 Claude Code 스킬 |
| [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | +412 | 에이전트 작업 계획 수립·주석·리뷰용 워크스페이스 |
| [Tencent/LoopForge](https://github.com/Tencent/LoopForge) | +101 (신규) | 사람 승인 게이트(Human Approval Gate)가 있는 자체 호스팅 코딩 에이전트 워크플로 |
| [ashhart/TensorFold](https://github.com/ashhart/TensorFold) | +53 | Zig로 작성된 Metal/CUDA/Vulkan용 LLM 추론 엔진 |

> 💡 **관찰**: 상위권 대부분이 "모델" 자체가 아니라 **에이전트가 쓰는 도구(Tools for Agents)** 입니다. Google, Meta, Alibaba, Tencent, Vercel 같은 빅테크가 직접 이 영역에 저장소를 내고 있습니다.

---

## 3. 주목할 기술 / 프레임워크 (Rising Tech to Watch)

- **에이전트 런타임 프레임워크 (Agent Runtime Framework)**
  [DeepSeek Harness (`dsh`)](https://github.com/deepseek-ai/deepseek-harness)는 "모든 것이 플러그인(Everything is a plugin)"이라는 구조이고, Landlock/Seatbelt 기반 샌드박스를 씁니다. 특정 모델에 종속되지 않습니다. Tencent LoopForge도 같은 계열입니다. → 레포 기존 글 *agent-sandbox-internals* 와 연결됩니다.
- **AG-UI 프로토콜 (Agent-User Interaction Protocol, [에이지-유아이])**
  [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui)는 에이전트와 프론트엔드를 잇는 표준이고, Meta astryx 같은 에이전트용 디자인 시스템과 맞물립니다. → 기존 글 *open-intelligent-ui* 의 후속 주제로 적합합니다.
- **하이브리드 코드 리뷰 (Deterministic + LLM Review)**
  Alibaba open-code-review(51k⭐)처럼 정적 분석 결과에 LLM 판단을 겹치는 방식이 주류로 자리 잡는 추세입니다.
- **초대형 오픈 MoE (Mixture-of-Experts, [믹스처 오브 엑스퍼츠])**
  [Tencent Hy4-preview](https://letsdatascience.com/news/tencent-releases-hy4-preview-open-model-weights-0f4d878a)는 770B 총 파라미터, 49B 활성, 1M 컨텍스트, Apache 2.0입니다. 11/4에 정식 Hy4가 발표되었고 가중치는 순차 공개 예정이라고 합니다 [일부 미확인].

---

## 4. 최근 24시간 주요 뉴스 (Notable News)

| # | 뉴스 | 신뢰도 | 링크 |
|---|---|---|---|
| 1 | **젠슨 황, 엔비디아 CEO·이사직 즉시 사임** (11/12 공시). CFO 콜렛 크레스가 임시 CEO를 겸임합니다. 시가총액 약 1.76조 달러가 증발했고 의회 청문 소환까지 이어졌습니다. 후임으로 Arm CEO 르네 하스(Rene Haas) 접촉설이 나옵니다(FT). | ✅ 확인 | [TechCrunch](https://techcrunch.com/2026/11/12/nvidias-jensen-huang-resigns-chipmaker-names-cfo-colette-kress-as-interim-ceo/) · [CNN](https://www.cnn.com/2026/11/11/business/live-news/nvidia-jensen-huang-investigation-fallout) · [Al Jazeera](https://www.aljazeera.com/news/2026/11/12/why-did-nvidia-ceo-jensen-huang-resign-and-who-is-colette-kress) |
| 2 | **앤트로픽 IPO 수 배 초과 청약**. 주당 $70~78, 기업가치 약 1.4조 달러(완전희석 기준)이고 밴드 상단 초과 가격 책정이 검토되고 있습니다. 11/18 가격 확정, 11/19 나스닥 상장 예정입니다. | ✅ 확인 (Bloomberg/FT 인용) | [StockAnalysis](https://stockanalysis.com/news/anthropic-ipo-multiple-times-oversubscribed/) · [TNW](https://thenextweb.com/news/anthropic-ipo-terms-1-4-trillion-valuation) |
| 3 | **Claude for Manufacturing** 출시 (Infor 파트너십) | ⚠️ 미확인 | [Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-13-2026-leadership-transitions) |
| 4 | **Gemini 4 "Hydrogen"** (Flash급, 코딩·에이전트용 고속 모델). 일부 트래커는 11/13 출시로 기록했지만 Google 공식 모델 ID는 확인되지 않았습니다. 확인된 공식 모델은 9/30 발표된 Gemini 4 Argon입니다. | ⚠️ 상충 | [LLM Gateway](https://llmgateway.io/timeline) · [kie.ai](https://kie.ai/blog/what-is-gemini-4-hydrogen) · [Google Blog (Argon)](https://blog.google/intl/en-mena/company-news/technology/gemini-4-argon-our-next-era-of-frontier-intelligence/) |
| 5 | **ChatGPT Wallet**: 에이전트 구매용 결제 지갑. 데스크톱 앱 코드에서 발견된 단계이고, OpenAI 공식 출시는 확인되지 않았습니다. | ⚠️ 유출/보도 | [RuntimeWire](https://runtimewire.com/article/exclusive-openai-is-building-a-chatgpt-wallet-for-agentic-purchases) |
| 6 | **OpenAI 로보틱스 팀 해체·재배치** (Fortune 보도 인용) | ⚠️ 미확인 | [Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-13-2026-leadership-transitions) |
| 7 | **United Airlines, 개인 AI 에이전트의 항공권 예약 차단** (WSJ 보도 인용). 에이전틱 커머스에 대한 첫 대형 업체의 반발로 볼 수 있습니다. | ⚠️ 미확인 | [Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-13-2026-leadership-transitions) |
| 8 | **FAA, 신규 AI 관제 시스템과 항공 지상 정지(Ground Stop) 연관성 조사**. 당국은 인과관계를 확정하지 않았습니다. | ⚠️ 조사 중 | [Click2Houston](https://www.click2houston.com/news/local/2026/11/13/faa-investigating-whether-new-ai-technology-contributed-to-nationwide-ground-stop/) · [Futurism](https://futurism.com/advanced-transport/flights-grounded-east-coast-government-faa-ai-air-traffic-control) |
| 9 | **가짜 AI 인용(Hallucinated Citations)** 으로 변호사 4명 전원이 사건에서 배제되고 1명은 $2,500 벌금을 받았습니다. | ⚠️ 미확인 | [Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-13-2026-leadership-transitions) |

**이번 달 모델 릴리스 참고** (트래커 기준, [LLM Gateway](https://llmgateway.io/timeline) · [nocode.mba](https://www.nocode.mba/ai-release-tracker/2026/11)): Claude Fable 5.2 (11/9), Gemini 4 Carbon (11/10), Meta Muse Ember 1.0 (11/10), ElevenLabs Scribe v3 (11/10), Gemini Omni 1.2 Flash (11/5), GPT Image 2.6 (11/4), Tencent Hy4 (11/4).

---

## 5. 블로그 후속 주제 제안

- **"에이전트용 디자인 시스템"** — Meta astryx와 AG-UI 분석 (기존 OpenIntelligentUI 글의 후속편)
- **"빅테크 에이전트 하네스 비교"** — DeepSeek Harness, Tencent LoopForge, Claude Agent SDK
- **"에이전틱 커머스와 결제 레일"** — ChatGPT Wallet, Visa 토큰, 가맹점의 차단 움직임

---

### 조사 한계
- `theneuron.ai`, `huggingface.co`, `josedacruz.com` 은 세션 네트워크 정책상 접근할 수 없어 검색 스니펫으로 대체했습니다. Hugging Face 트렌딩 모델은 이번 리포트에서 빠졌습니다.
- GitHub 트렌딩 수치는 2026-11-14 조회 시점 스냅샷입니다.
