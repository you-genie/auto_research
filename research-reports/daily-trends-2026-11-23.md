# 데일리 AI·테크 트렌드 리포트 — 2026-11-23 (월)

> 조사 범위: 2026-11-17 ~ 11-23 (최근 24시간 이슈 중심 + 이번 주 맥락)
> 표기 규칙: **한글 (English 원문, [발음])**. 수치는 대부분 업체 발표·2차 보도 기준이며, 독립 검증되지 않은 항목은 ⚠️로 표시.

---

## 🔑 한 줄 요약
**"상장한 AI 랩 + 멀티 에이전트 군집(Agent Swarm)"의 한 주.** Anthropic 나스닥 상장 후 AI주 변동성이 커졌고, Replit·Perplexity가 동시에 다중 에이전트 제품을 출시했으며, OpenAI는 "에이전트가 2~4시간짜리 연구 업무의 46%를 끝낸다"는 내부 지표를 공개했습니다.

---

## 1. 트렌딩 키워드 & 토픽

| 키워드 (원문 / 발음) | 설명 |
|---|---|
| **에이전트 스웜** (Agent Swarm / [에이전트 스웜]) | 하나의 목표를 여러 에이전트가 계획·구현·테스트·검증까지 분담하는 방식. Replit Missions, Perplexity Multiagent가 같은 주에 출시되며 키워드 급부상. |
| **성과 기반 과금** (Outcome-based Pricing / [아웃컴 베이스드 프라이싱]) | 토큰이 아니라 "목표 달성 단위(미션)"와 예산 상한으로 과금. Replit Missions의 핵심 차별점. |
| **연구 가속** (Research Acceleration / [리서치 액셀러레이션]) | AI가 AI 연구 자체를 대신하는 정도를 측정하는 흐름. OpenAI 보고서 "The jagged frontier([재기드 프런티어], 들쭉날쭉한 경계)". |
| **AI 설계 칩** (AI-designed CPU / [에이아이 디자인드 씨피유]) | 컴파일러·ISA·RTL·검증·GDS까지 에이전트가 반복 설계. Architect Labs의 Frostbite. |
| **자기 가중치 수정** (Self-rewriting Weights / [셀프 리라이팅 웨이츠]) | 모델이 학습 루프 없이 스스로 가중치를 고친다는 주장의 논문이 HN 상위권. ⚠️ 원문 미확인. |
| **에이전트 스킬** (Agent Skills / [에이전트 스킬즈]) | 에이전트에 붙이는 재사용 가능한 절차 묶음. GitHub 신규 인기 레포의 상당수가 "*-skill" 형태. |
| **러스트 점진 이식** (Incremental Rust Rewrite / [인크리멘털 러스트 리라이트]) | 코딩 에이전트로 앱을 Rust로 조금씩 옮기되 원본 동작을 기록·대조하여 검증. rust-anything, fast-anything 동시 급상승. |
| **AI 버블 논쟁** (AI Bubble / [에이아이 버블]) | Anthropic 상장 직후 나스닥 약세로 "AI주 변동성" 토론이 HN 최다 댓글(900+). |

---

## 2. 주목할 GitHub 레포지토리

### 🆕 이번 달 새로 생겨 급성장 중 (생성일 11월 이후, 2026-11-23 기준 스타 수)

| 레포 | ★ | 한 줄 설명 |
|---|---|---|
| [erkamyaman/rust-anything](https://github.com/erkamyaman/rust-anything) | 8.6K (11/16 생성) | 앱 전체를 Rust로 **조각 단위 이식**, 각 단계마다 원본의 기록된 동작과 대조 검증 (CLI·HTTP 서버·라이브러리). |
| [EL4CTEO/fast-anything](https://github.com/EL4CTEO/fast-anything) | 3.0K (11/21 생성, 이틀 만에) | "전부 다시 쓰지 말고 느린 5%만" — Python/Node/Ruby를 **프로파일링**(Profiling, [프로파일링])한 뒤 핫 함수만 에이전트로 Rust 이식. |
| [deepseek-ai/chat-demo](https://github.com/deepseek-ai/chat-demo) | 5.3K | DeepSeek 공식 채팅 데모 (TypeScript). 설명은 짧지만 공식 계정이라 주목. |
| [simplexai-labs/linger](https://github.com/simplexai-labs/linger) | 4.2K | PC에서 **완전 로컬**로 도는 개인 에이전트(Personal Agent). |
| [FrigadeHQ/yogurt](https://github.com/FrigadeHQ/yogurt) | 3.1K | 봇 없이 로컬에서 도는 AI 회의록. Mac/Win/Linux. |
| [sybil-solutions/inference-optimisation-skill](https://github.com/sybil-solutions/inference-optimisation-skill) | 2.1K | 로컬 LLM 서빙 속도(디코드, **추측 디코딩** Speculative Decoding [스페큘러티브 디코딩], KV 캐시, TTFT)를 에이전트가 자동 최적화하는 스킬. |
| [HybridRobotics/supermimic](https://github.com/HybridRobotics/supermimic) | 2.0K | 미분 가능한 **월드 모델**(World Model, [월드 모델]) 하나로 휴머노이드 전신 모션 추적. |
| [bookwjitchieni1986/blender-ai-mcp-addon](https://github.com/bookwjitchieni1986/blender-ai-mcp-addon) | 2.8K | Blender용 AI 어시스턴트 + **MCP** 서버. ⚠️ 신생 개인 계정 — 설치 전 코드 확인 권장. |

### 📈 기존 대형 프로젝트 중 계속 활발한 것

| 레포 | ★ | 설명 |
|---|---|---|
| [obra/superpowers](https://github.com/obra/superpowers) | 325K | 에이전트 스킬 프레임워크 + 개발 방법론. 스킬 생태계의 사실상 표준 레퍼런스. |
| [stablyai/orca](https://github.com/stablyai/orca) | 134K | Claude Code·Codex 등 **코딩 에이전트 여러 개를 함대(Fleet, [플릿])처럼** 내 구독으로 운영. |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 73K | Reddit·X·YouTube·HN·Polymarket을 훑어 최근 30일 동향을 요약하는 스킬 (이 리포트와 같은 용도!). |
| [vercel-labs/agent-desktop](https://github.com/vercel-labs/agent-desktop) | 26K | AI 에이전트용 **컴퓨터 유즈**(Computer Use, [컴퓨터 유즈]) CLI (Rust). |

> 참고: 11월 신규 레포 1위는 게임 재컴파일 프로젝트(29K★)였으나, 저작권 이슈 소지가 있어 목록에서 제외했습니다.

---

## 3. 주시할 기술·프레임워크

1. **멀티 에이전트 오케스트레이션** (Multi-agent Orchestration / [멀티 에이전트 오케스트레이션])
   — Replit Missions(11/17), Perplexity Multiagent(11/17, 최대 16개 에이전트 상호 검증), 앞서 Factory Missions까지. "단일 에이전트 → 예산·승인 규칙이 붙은 군집"으로 제품 형태가 수렴 중.
2. **동작 대조 기반 AI 리팩터링** (Behavior-checked Migration / [비헤이비어 체크드 마이그레이션])
   — 녹화한 원본 동작을 오라클(Oracle, [오라클])로 삼아 에이전트가 이식한 코드를 검증. rust-anything/fast-anything가 대표. 레거시 성능 개선 실무에 바로 쓸 만함.
3. **로컬 우선 에이전트** (Local-first Agent / [로컬 퍼스트 에이전트])
   — linger, yogurt, 로컬 LLM 서빙 최적화 스킬 등. 프라이버시·비용 이슈로 꾸준히 증가.
4. **AI 기반 하드웨어 설계 (EDA)** (Electronic Design Automation / [일렉트로닉 디자인 오토메이션])
   — Frostbite: 7nm, interaction nets([인터랙션 네츠]) 기반 신규 ISA, 와트당 성능 4.59배 주장. ⚠️ 실리콘 이전 추정치, 비교 대상 CPU 비공개.
5. **신규 모델 라인업 (11월)** — 트래커 기준: OpenAI GPT-6.2 Astra/Sol(11/17), Google Gemini 4 Neon(11/18), Alibaba Qwen4-Max(11/16, 1M 컨텍스트), Mistral Large 4(오픈 웨이트), Moonshot Kimi K3.1(11/20). ⚠️ 3차 트래커 정보라 각 사 공식 발표로 재확인 필요.

---

## 4. 최근 24~72시간 주요 뉴스

| 날짜 | 뉴스 | 요약 |
|---|---|---|
| 11/19~ | **Anthropic 나스닥 상장** (IPO, [아이피오]) | 티커 ANT, 공모가 $83 → 시가 $111.50(+34%) → 첫날 종가 $97.17(+17%). 미국 사상 최대 IPO(약 $81B). 이후 AI주 매도세로 나스닥이 연초 대비 상승분을 반납했다는 보도가 HN 최다 토론(921 댓글). [Al Jazeera](https://www.aljazeera.com/economy/2026/11/19/anthropic-starts-trading-in-the-us-after-blockbuster-ipo) · [TechRepublic](https://www.techrepublic.com/article/news-anthropic-ipo-nasdaq-trading-debut/) · [Guardian](https://www.theguardian.com/business/2026/nov/20/global-stock-markets-slump-anthropic-ipo-ai-sell-off) |
| 11/18 | **OpenAI "Research acceleration: The jagged frontier"** | 사내 연구 업무 중 사람 기준 2~4시간짜리의 46%를 에이전트가 자율 완료(3월 23%). 4~8시간 업무는 13%→35%. 학습 모니터링 79% vs 서빙 코드 작성 25%로 편차 큼. 자체 측정치. [The New Stack](https://thenewstack.io/openai-agent-research-bottleneck/) |
| 11/18 | **Architect Labs Frostbite CPU** | 에이전트가 컴파일러~GDS까지 설계·검증한 CPU. HN 678점. [원문](https://architectlabs.com/blog/frostbite) · [분석](https://explainx.ai/blog/architect-labs-frostbite-ai-designed-cpu-interaction-nets-4-59x-perf-per-watt-claimed-vs-verified-2026) |
| 11/17 | **Replit Missions** | 목표·예산·승인 규칙을 정하면 에이전트 스웜이 리뷰 통과까지 작업. [공식 블로그](https://replit.com/blog/introducing-replit-missions) · [The New Stack](https://thenewstack.io/replit-missions-agent-swarms/) |
| 11/17 | **Perplexity Computer "Multiagent"** | 리드 에이전트 + 최대 16개 보조 에이전트가 여러 프런티어 모델로 교차 검증. Max 구독자 대상. [MarkTechPost](https://www.marktechpost.com/2026/11/17/perplexity-computer-multiagent-effort-level/) |
| ~11/22 | **HN 화제: "Language Models Can Rewrite Their Own Weights"** | 491점. ⚠️ 2차 출처만 확인, 원문 검증 전. [arXiv 2611.21885](https://arxiv.org/abs/2611.21885) |
| ~11/22 | **OpenAI "Perplexity and Intelligence"** | 퍼플렉시티(Perplexity, [퍼플렉시티] — 언어모델 지표) 지표와 지능 측정의 관계. HN 513점. [원문](https://openai.com/index/perplexity-and-intelligence/) |
| 이번 주 | 기타 (⚠️ 뉴스레터 단일 출처) | AMD×HUMAIN 500MW AI 컴퓨트 계약, 도이치텔레콤 Mistral에 €1억 투자, Bing AI Overviews 광고 도입. |

---

## 💡 시사점 (이 블로그 관점)
- **후속 심층 글 후보:** ① 에이전트 스웜 제품 비교 (Replit Missions vs Perplexity Multiagent vs Factory Missions) ② OpenAI "jagged frontier" 보고서 해부 — 어떤 연구 업무가 자동화되고 어떤 건 안 되는가 ③ rust-anything 류 "동작 대조 기반 에이전트 리팩터링" 실습.
- 기존 글 [2026-07-24 에이전트 아키텍처](../2026-07-24-agent-architecture/)의 멀티에이전트 장(章) 업데이트 필요성 있음.

## 출처
- https://aiagentstore.ai/ai-agent-news/this-week
- https://github.com/yaojiejia/agents-radar/issues/522 (HN AI Digest 11-23)
- https://www.aljazeera.com/economy/2026/11/19/anthropic-starts-trading-in-the-us-after-blockbuster-ipo
- https://www.techrepublic.com/article/news-anthropic-ipo-nasdaq-trading-debut/
- https://www.itv.com/news/2026-11-19/anthropic-begins-trading-in-the-biggest-ipo-on-record
- https://thenewstack.io/openai-agent-research-bottleneck/
- https://replit.com/blog/introducing-replit-missions
- https://www.marktechpost.com/2026/11/17/perplexity-computer-multiagent-effort-level/
- https://explainx.ai/blog/architect-labs-frostbite-ai-designed-cpu-interaction-nets-4-59x-perf-per-watt-claimed-vs-verified-2026
- https://llmgateway.io/timeline/2026 · https://www.nocode.mba/ai-release-tracker/2026/11
- GitHub Search API (2026-11-23 조회, 생성일 11/09 이후 ★500+ 레포)
