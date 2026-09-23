# 데일리 트렌드 브리핑 (2026-09-23)

> AI/개발 도메인 중심, 지난 24~48시간 기준 스캔. 스캔 시각: 2026-09-23 20:14 UTC

---

## 1. 트렌딩 키워드 & 토픽

| 키워드 | 설명 |
|---|---|
| **에이전트 하네스**(Agent Harness, 발음: 에이전트 하니스) | 모델을 감싸서 도구 사용·멀티스텝 작업을 가능케 하는 런타임 레이어. 이번 주 트렌딩의 중심 축 — 모델 자체보다 "모델을 둘러싼 기계 장치"가 화두. |
| **오케스트레이션**(Orchestration, 발음: 오r케스트레이션) | 다수의 자율 에이전트 워크로드를 클러스터 단위로 스케줄링·관리하는 기술. Google `ax` 출시로 재조명. |
| **월드 모델**(World Model, 발음: 월드 마들) | 카메라 시점·3D 일관성을 유지하며 장면을 생성/탐색하는 비디오 생성 모델 계열. 이번 주 HF 트렌딩 논문 상위권을 다수 차지. |
| **에이전틱**(Agentic, 발음: 에이전틱) | "자율적으로 계획·실행·복구하는" 시스템을 통칭하는 형용사. 하네스, 오케스트레이터, 스킬 프레임워크 전반에 공통으로 붙는 수식어. |
| 토큰 효율(Token Efficiency) | 장시간 무인 작업(unattended agent)이 늘면서 컨텍스트/비용 절감이 핵심 지표로 부상. |
| 감마(감시가 아니라) US-China AI 안보 논의 | UN 안보리 차원의 프런티어 AI 안전 논의가 처음으로 미·중 개발사를 한 테이블에 불러모음. |

---

## 2. 뜨는 GitHub 저장소

- **[google/ax](https://github.com/google/ax)** (Go) — Google이 공개한 "쿠버네티스 스타일"의 에이전트 오케스트레이터. `Agent Substrate` 위에서 에이전트를 상태 유지형 액터로 다루며, 유휴 상태면 체크포인트 후 서브초 단위로 재개. Apache 2.0. 약 8,600★, 하루 +1,500★ 수준으로 급상승 중.
- **[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)** — DeepSeek의 오픈소스 에이전트 하네스 "dsh". "Everything is a Plugin" 철학, `npx @deepseek-ai/dsh web`으로 로컬 실행. Claude Code의 정면 경쟁자로 8월 한 달 새 19만★ 이상 증가.
- **[obra/superpowers](https://github.com/obra/superpowers)** — Claude Code용 스킬 프레임워크. TDD·설계 브레인스토밍·플래닝을 마크다운 스킬 묶음으로 강제해 "장난감 코드"가 아닌 "엔지니어링급 코드"를 유도. 약 29만★.
- **[dream-num/univer](https://github.com/dream-num/univer)** (TypeScript) — "AI 에이전트용 오피스 하네스". 스프레드시트/문서/슬라이드/PDF를 하나의 런타임에서 다루는 오픈소스 오피스 스위트.
- **[browser-use/video-use](https://github.com/browser-use/video-use)** (Python) — 코딩 에이전트로 비디오를 편집하는 도구. browser-use 팀의 신작.
- **[DeusData/codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp)** (C) — 영속적 지식 그래프 기반 코드 인텔리전스 MCP 서버. 코드베이스를 장기 메모리처럼 색인.

(출처: [GitHub Trending](https://github.com/trending), [Trendshift](https://trendshift.io/weekly))

---

## 3. 주목할 기술/프레임워크

1. **DeepSeek Harness (dsh)** — 모델·툴·스킬·세션·샌드박스를 전부 플러그인으로 교체 가능하게 만든 아키텍처. Standard/Code/Minimal/Creator 4가지 런타임 모드 제공. Claude Code의 오픈소스 대항마로 주목받는 중이며, 아직 개발자 프리뷰 단계라 호환성 깨지는 변경이 잦음. ([VentureBeat](https://venturebeat.com/technology/deepseek-harness-launches-as-open-source-rival-to-claude-code-alongside-v4-pro-on-api-with-higher-prices), [InfoQ](https://www.infoq.com/news/2026/08/deep-seek-harness/))
2. **Google AX** — `Task`/`Workspace`/`Gateway`/`Model` 4개의 선언적 프리미티브로 자율 에이전트를 클러스터에서 대량 운영. `kubectl` 스타일의 CLI(`ax apply/get/describe/watch`)를 제공해 진입장벽을 낮춤. ([InfoQ](https://www.infoq.com/news/2026/09/google-ax-orchestrator/))
3. **컨텍스트 트리밍 미들웨어** (예: context-mode류 프로젝트) — 에이전트-툴 사이에서 노이즈 섞인 툴 출력을 대폭(주장상 최대 98%) 줄여 컨텍스트 윈도우를 아끼는 미들웨어 계열. MCP 기반으로 여러 에이전트 플랫폼을 가로질러 동작.
4. **SoL-Pi (하네스 레벨 RSI 논문)** — 코딩 에이전트 하네스 자체를 재귀적으로 자기개선시켜 토큰 트래픽을 44~49%, API 비용을 약 1/3 절감했다고 주장하는 연구. GPT-5.6/Opus 5 양쪽에서 검증. ([Hugging Face Papers](https://huggingface.co/papers/2609.20519))
5. **비디오 월드 모델 계열** (WorldCrafter, GAE 등) — 카메라 궤적 조건화 + 3D 일관성 있는 잠재공간(latent space)으로, 한 장의 이미지/텍스트 프롬프트에서 분 단위로 일관된 장면 탐색을 가능케 하는 연구가 이번 주 HF 트렌딩 상위권을 휩씀.

---

## 4. 지난 24시간 주요 뉴스

- **Anthropic, Claude Opus 5.5 출시 (9/22)** — Opus 5 대비 워크로드 비용 40%↓, 출력 속도 30%↑, 가격 $4/$20 per MTok(20%↓), 캐시 읽기 $0.20/MTok(60%↓). Dario Amodei의 "속도 조절" 선언 이후 첫 모델. 컨테인먼트 우회 시도가 Opus 5 대비 85% 감소했다고 자체 안전성 평가에서 발표. AWS/GCP/Azure 동시 배포, Sonnet 5.5·Haiku 5.5도 수주 내 출시 예고. ([TechCrunch](https://techcrunch.com/2026/09/22/anthropic-releases-opus-5-5-with-lower-prices-and-fable-level-performance/), [SiliconANGLE](https://siliconangle.com/2026/09/22/anthropic-releases-claude-opus-5-5-and-openai-counters-with-two-cheaper-gpt-6-models/))
- **OpenAI, GPT-6 Luna / GPT-6 Sol 출시 (9/22)** — Opus 5.5 출시에 맞대응한 저가형 라인업 2종 공개. (같은 날 xAI Grok 4.7, 샤오미 MiMo V2.6 Flash/Pro도 출시되며 9월에만 신규 모델 20종 이상 등장)
- **UN 안보리, AI 안보 세션 개최 (9/23)** — 프랑스 주재로 15개 이사국이 AI-국제안보 논의. Sam Altman, Anthropic 고위 관계자, DeepSeek·Moonshot 등 중국 프런티어 개발사가 처음으로 한 자리에. DeepSeek 창업자 량원펑은 불참 예정. ([Bloomberg](https://www.bloomberg.com/news/articles/2026-09-23/xi-and-trump-seek-safe-ai-without-slowing-the-race-for-supremacy))
- **Alphabet Intrinsic, Intrinsic Core 로보틱스 스택 공개 (ROSCon 2026, 토론토)** — Apache 2.0, ROS 호환. Nvidia FoundationPose 기반 포즈 추정, 모션/그립 플래닝, 시뮬레이션·캘리브레이션 서비스를 묶은 오픈소스 로보틱스 환경.

---

## 참고 자료

- [GitHub Trending](https://github.com/trending)
- [Trendshift Weekly](https://trendshift.io/weekly)
- [Hugging Face Trending Papers](https://huggingface.co/papers/trending)
- [Hugging Face Trending Models](https://huggingface.co/models?sort=trending)
- [TechCrunch — Opus 5.5](https://techcrunch.com/2026/09/22/anthropic-releases-opus-5-5-with-lower-prices-and-fable-level-performance/)
- [InfoQ — Google AX](https://www.infoq.com/news/2026/09/google-ax-orchestrator/)
- [InfoQ — DeepSeek Harness](https://www.infoq.com/news/2026/08/deep-seek-harness/)
- [Bloomberg — UN Security Council AI session](https://www.bloomberg.com/news/articles/2026-09-23/xi-and-trump-seek-safe-ai-without-slowing-the-race-for-supremacy)
