# 일일 테크 트렌드 리포트 — 2026-11-21 (토)

> 조사 범위: 2026-11-17 ~ 11-21 (핵심 뉴스는 최근 24~48시간 위주)
> 관심 도메인: AI/LLM, 에이전트(Agent), 개발 도구
> 표기 규칙: **한글 (English 원문, [발음])**

---

## 한 줄 요약

**Anthropic이 Nasdaq에 상장(IPO)해 역대 최대 규모 공모를 기록했고, 같은 주에 OpenAI·Google·Moonshot이 프론티어 모델을 잇달아 냈다.** 개발 현장에서는 "모델 성능"보다 **에이전트 실행 인프라(Agent Infrastructure)**와 **안전·보안(Security)** 쪽으로 관심이 옮겨가고 있다.

---

## 1. 트렌딩 키워드 & 토픽

| 키워드 | 발음 | 설명 |
|---|---|---|
| **에이전틱 AI (Agentic AI)** | [어젠틱 에이아이, /əˈdʒɛntɪk/] | 스스로 계획·실행하는 AI. 이번 주 뉴스(Apple, Meta Muse, EU 해킹)를 관통하는 키워드 |
| **컴퓨터 유즈 (Computer Use)** | [컴퓨터 유즈, /kəmˈpjuːtər juːs/] | 에이전트가 화면·앱·브라우저를 직접 조작하는 기능. Apple도 개발 중이라는 보도 |
| **오픈 웨이츠 (Open Weights)** | [오픈 웨이츠, /ˈoʊpən weɪts/] | 가중치 공개 모델. 중국(Kimi, Tencent Hy4)과 Thinking Machines가 주도 |
| **프리페어드니스 프레임워크 (Preparedness Framework)** | [프리페어드니스, /prɪˈpɛrdnəs/] | OpenAI의 위험도 평가 체계. GPT-6.2 Astra가 "AI 자기개선(Self-Improvement) High" 단계에 처음 도달 |
| **소버린 AI (Sovereign AI)** | [사버린, /ˈsɑːvrɪn/] | 국가·지역 단위 AI 자립. 도이치텔레콤의 Mistral 투자 배경 |
| **스펙 주도 개발 (Spec-Driven Development, SDD)** | [스펙 드리븐 디벨롭먼트] | 명세(스펙)를 원본으로 두고 코드는 에이전트가 생성하는 방식 |
| **오케스트레이션 (Orchestration)** | [오케스트레이션, /ˌɔːrkɪˈstreɪʃən/] | 여러 에이전트·모델을 조율하는 일. 예: Gemini 4 Neon이 계획을 세우고(Planner) Hydrogen이 실행(Executor) |
| **AI 지원 사이버공격 (AI-assisted Cyberattack)** | [어시스티드 사이버어택] | EU 집행위원회가 AI 도구를 쓴 공격을 처음 공식 확인 |

---

## 2. 주목할 GitHub 레포 / 오픈소스 프로젝트

> ⚠️ 별 개수는 제3자 집계 블로그(coddykit, gittrend 등) 기준이며 출처마다 차이가 있다. 이번 실행에서는 GitHub Trending 페이지에 직접 접속할 수 없어 수치를 검증하지 못했다.

| 레포 | 대략적 별 수 | 설명 |
|---|---|---|
| [paperclipai/paperclip](https://github.com/paperclipai/paperclip) | ~110K+ | Claude Code·Codex 등 여러 하네스(Harness, [하네스])의 에이전트를 한곳에서 관리하는 플랫폼 |
| [github/spec-kit](https://github.com/github/spec-kit) | ~96K~147K (출처별 상이) | GitHub 공식 **SDD** 툴킷. 1.0.0 도달, 통합 30개·확장 91개 |
| [D4Vinci/Scrapling](https://github.com/D4Vinci/Scrapling) | ~92K | 에이전트용 웹 스크래핑(Scraping, [스크래핑]) 및 데이터 접근 계층 |
| [vercel-labs/agent-desktop](https://github.com/vercel-labs/agent-desktop) | ~8.4K (하루 +2.2K) | Rust로 만든 데스크톱 **컴퓨터 유즈** 에이전트. 하루 증가 폭이 큼 |
| [google-research/paper-orchestra](https://github.com/google-research/paper-orchestra) | ~1.7K | 연구 자료를 LaTeX 논문 원고로 만들어 주는 멀티 에이전트(Multi-Agent) 프레임워크 |

**Hugging Face 트렌딩 모델 (Hub API로 직접 확인)**

| 모델 | 공개일 | 특징 |
|---|---|---|
| [thinkingmachines/Inkling-2-Mini](https://hf.co/thinkingmachines/Inkling-2-Mini) | 11/17 | 트렌딩 1위. MoE, Apache-2.0. 아키텍처 태그가 `inkling2_loop`라 **루프 구조**로 보임 (언론 보도는 아직 찾지 못함) |
| [unsloth/Inkling-2-Mini-GGUF](https://hf.co/unsloth/Inkling-2-Mini-GGUF) | 11/20 | 로컬 실행용 GGUF([지지유에프]) 양자화판, 하루 만에 다운로드 23만 회 |
| [tencent/Hy4-flash](https://hf.co/tencent/Hy4-flash) | 11/17 | Tencent Hunyuan 4세대 경량 멀티모달 MoE |
| [sensenova/SenseNova-Loop-9B](https://hf.co/sensenova/SenseNova-Loop-9B) | 11/17 | **루프 트랜스포머(Looped Transformer)** 구조의 9B 멀티모달 모델 |
| [harness-hub/Qwen3.8-27B-pi-adapted](https://hf.co/harness-hub/Qwen3.8-27B-pi-adapted) | 11/16 | 특정 에이전트 하네스에 맞게 GRPO로 튜닝한 LoRA. "하네스 적응(Harness Adaptation)" 흐름 |
| [higurashi-ai/Haru-4B](https://hf.co/higurashi-ai/Haru-4B) | 11/12 | 4B **풀 듀플렉스(Full-Duplex, [풀 듀플렉스])** 음성-음성 모델, 한국어 지원 |
| [apple/FastFrames-L](https://hf.co/apple/FastFrames-L) | 11/16 | Wan2.1 기반 고속 텍스트→비디오 모델 |

---

## 3. 눈여겨볼 기술 / 프레임워크

1. **루프 트랜스포머 (Looped Transformer)** [룹트 트랜스포머]
   같은 층을 여러 번 반복해 적은 파라미터로 더 깊게 추론하는 구조다. 같은 주에 Inkling-2-Mini와 SenseNova-Loop-9B가 나왔다. **잠재 추론(Latent Reasoning)**이나 **TTT(Test-Time Training)** 연구와 이어지는 흐름이다.
2. **플래너-실행자 분리 (Planner–Executor Split)** [플래너 이그제큐터]
   비싼 모델은 계획을 세우고 싼 모델은 실행한다. Google Antigravity가 Neon과 Hydrogen을 짝지어 공식 지원한다. 비용 최적화의 표준 패턴이 되어 가고 있다.
3. **하네스 적응 파인튜닝 (Harness-adapted Fine-tuning)**
   오픈 모델을 특정 코딩 에이전트 하네스의 도구 형식에 맞춰 RL(GRPO)로 학습시키는 방식이다.
4. **스펙 주도 개발 (SDD) + 에이전트 관리 플랫폼**
   "모델을 더 똑똑하게"보다 "결과를 결정적(Deterministic, [디터미니스틱])으로 만드는 일"이 화두다. Spec Kit과 Paperclip이 성장하는 배경이다.
5. **풀 듀플렉스 음성 에이전트 (Full-Duplex Voice Agent)**
   사람처럼 말을 끊고 끼어들 수 있는 실시간 음성 모델이다. 4B 크기로 내려와 온디바이스(On-device)로 돌릴 수 있는 수준이 됐다.

---

## 4. 최근 24~48시간 주요 뉴스

### 💰 Anthropic, Nasdaq 상장 (11/19, 티커 `ANT`)
- 공모가 $83(희망 범위 $70~78 상회), 시초가 $111.50(+34%). 장중 $95대까지 밀림
- 공모 규모 약 **$81B로 역대 최대**(6월 SpaceX 기록 경신). 기업가치는 약 $1.5~2T
- 🔗 [Fox Business](https://www.foxbusiness.com/markets/anthropic-begins-trading-nasdaq-record-breaking-ipo) · [Al Jazeera](https://www.aljazeera.com/economy/2026/11/19/anthropic-starts-trading-in-the-us-after-blockbuster-ipo) · [TechRepublic](https://www.techrepublic.com/article/news-anthropic-ipo-nasdaq-trading-debut/)

### 🤖 Google, Gemini 4 Neon 출시 (11/18)
- Carbon(최상위)과 Hydrogen(경량) 사이의 중간 티어. 한 달 새 Gemini 4 계열 네 번째 모델
- 가격 $3/$15(백만 토큰당 입력/출력). Artificial Analysis 지수 3위, Vals Index 2위(제3자 집계)
- 사이버 보안 특화 변형은 Fairwind 프로그램의 방어 담당자에게 먼저 공개
- 🔗 [Google 블로그](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/) · [9to5Google](https://9to5google.com/2026/11/18/gemini-4-neon-announcement/) · [Antigravity 블로그](https://antigravity.google/blog/gemini-4-neon-in-google-antigravity/)

### 🧠 OpenAI, GPT-6.2 Astra / Sol 출시 (11/17)
- Astra(전문 업무용) $8/$40, Sol(일상용) $2/$10. ChatGPT Work·Codex·API에 출시
- **Preparedness Framework 기준 "AI 자기개선 High"에 해당하는 첫 외부 배포 모델**이며, 사이버보안은 Critical 등급. 앞서 6.1 Astra는 안전성 문제로 취소됐음
- 독립 평가에서는 Claude Fable 5.2에 이어 2위, 코딩 에이전트 성능은 제자리라는 보도
- 🔗 [OpenAI](https://openai.com/index/introducing-gpt-6-2-astra-sol) · [Decrypt](https://decrypt.co/383488/openai-gpt-6-2-astra-challenges-anthropic-price-but-not-every-benchmark) · [The Next Web](https://thenextweb.com/news/gpt-6-astra-benchmarks-monitorability-cyber)

### 🍎 Apple, 범용 "컴퓨터 유즈" 에이전트 개발 중 (11/19 보도)
- 채용 공고(11/17)에 "general-purpose computer-use agents"라는 표현이 등장. 앱 조작·웹 브라우징·코드 작성 기능
- 공식 발표나 출시 일정은 없음. 10-K 공시에는 "AI 에이전트가 승인되지 않은 행동을 할 수 있다"는 위험 경고가 들어 있음
- 🔗 [MacRumors](https://macrumors.com/2026/11/19/apple-ai-agent-development) · [Macworld](https://www.macworld.com/article/3280358/agentic-siri-is-coming-and-thats-just-the-beginning.html)

### 🛑 Nvidia, 미국 승인을 받고도 중국향 H200 출하 중단 (11/17 실적 발표)
- 3분기 중국향 Hopper 매출은 $2.4B. 향후 가이던스(약 $130B)에서는 중국을 제외
- 중단 이유는 밝히지 않음. 중국의 수입 제한, 미국의 수출 규제 강화(11/16), CEO 교체가 배경으로 거론됨
- 🔗 [Fox Business](https://www.foxbusiness.com/fox-news-tech/nvidia-halts-china-ai-chip-shipments-despite-us-approval) · [Business Today](https://www.businesstoday.in/technology/news/story/nvidias-2-4-billion-china-chip-business-hits-pause-interim-ceo-confirms-shipment-halt-568089-2026-11-18)

### 🔐 EU 집행위원회, AI 지원 사이버공격을 공식 확인 (11/19)
- 급여·휴가·의료비 환급 시스템이 10일 넘게 마비. 10월에 탐지됐고, EU가 AI 도구를 쓴 공격을 확인한 것은 처음
- CERT-EU는 AI 에이전트 기반 도구 "ARTEX"를 의심하고 있음(공식 확정은 아님). 공격 주체는 밝혀지지 않음
- 🔗 [The Register](https://theregister.com/cyber-crime/2026/11/19/european-commission-scrambles-to-contain-ai-assisted-cyberattack/5311103) · [Security Affairs](https://securityaffairs.com/?p=203483) · [Brussels Signal](https://brusselssignal.eu/2026/11/european-commission-confirms-ai-driven-cyberattack-weeks-after-detecting-it/)

### ⚠️ Meta Muse 에이전트 개인정보 유출 논란 (Reuters 보도)
- 직원들이 내부에서 "다른 사용자의 대화·은행 잔고가 섞여 노출된다"고 제보. Meta는 "일부 사례(isolated incidents)"라는 입장
- 🔗 [CTV News](https://www.ctvnews.ca/sci-tech/article/as-meta-bets-big-on-muse-ai-agent-early-safety-mishaps-surface/) · [Futurism](https://futurism.com/future-society/meta-muse-ai-agent-sharing-private-data.md)

### 기타 단신
- **Deutsche Telekom T.Capital, Mistral AI에 $110M 투자**: 독일의 소버린 AI 추진 흐름 ([Creati.ai 다이제스트](https://creati.ai/ai-news/2026-11-20/))
- **ChatGPT Live Dictation 추가**, 10분 녹음 제한 폐지 ([Creati.ai](https://creati.ai/ai-news/2026-11-20/))
- **Thinking Machines Inkling-2-Mini 공개(11/17)**, Apache-2.0 ([HF](https://hf.co/thinkingmachines/Inkling-2-Mini))
- 참고(지난 2주): **Claude Fable 5.2 / Mythos 5.2** 출시(11/9), **Kimi K3.1 Pro** 가중치 공개(11/5) ([TechNode](https://technode.com/2026/11/05/moonshot-ai-releases-kimi-k3-1-pro-model-weights/))

---

## 💡 시사점 (이 레포 관점)

- **후속 딥다이브 후보**
  1. 루프 트랜스포머 계열(Inkling-2-Mini, SenseNova-Loop)과 기존 [잠재 추론](../2026-05-08-latent-reasoning/)·[TTT](../2026-04-14-ttt-fast-weights/) 글의 연결
  2. 플래너-실행자 오케스트레이션 비용 분석. [에이전트 아키텍처](../2026-07-24-agent-architecture/) 글의 후속편으로 적합
  3. 에이전트 보안 사고 정리(Meta Muse, EU ARTEX). [에이전트 샌드박스](../2026-09-15-agent-sandbox-internals/) 글과 연결
- **주의**: 신모델 벤치마크 수치는 대부분 회사 자체 발표나 제3자 집계라 교차 검증이 필요하다.

---

### 조사 한계
- 이 세션의 네트워크 정책 때문에 `github.com/trending`, `news.ycombinator.com`, `hn.algolia.com`, `gittrend.io`, `theneuron.ai`에 직접 접속하지 못했다. GitHub 별 수는 2차 출처 기준이다.
- Hugging Face 트렌딩은 HF Hub API로 직접 확인했다.
