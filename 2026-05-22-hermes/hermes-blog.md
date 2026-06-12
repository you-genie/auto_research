# Nous Research Hermes 시리즈 완전 정복: 오픈웨이트 LLM의 가장 오래된 혈통

> 📊 **발표자료**: [slides.pptx](./slides.pptx)

> **오늘 날짜**: 2026-05-22 | **대상 독자**: LLM/AI 전문가 | **리서치 기준**: 2026년 5월 현재 공개 정보

---

## 목차

1. [Hermes가 뭔데요?](#1-hermes가-뭔데요)
2. [시리즈 계보 한눈에 보기](#2-시리즈-계보-한눈에-보기)
3. [Nous Research라는 곳](#3-nous-research라는-곳)
4. [핵심 철학: "Steerable" 어시스턴트](#4-핵심-철학-steerable-어시스턴트)
5. [ChatML: 모든 버전의 공통 언어](#5-chatml-모든-버전의-공통-언어)
6. [세대별 심층 분석](#6-세대별-심층-분석)
   - [6.1 OpenHermes → Hermes 1 (2023)](#61-openhermes--hermes-1-2023)
   - [6.2 Hermes 2 / 2 Pro (2024)](#62-hermes-2--2-pro-2024)
   - [6.3 Hermes 3 (2024.08)](#63-hermes-3-202408)
   - [6.4 DeepHermes 3 Preview (2025.02)](#64-deephermes-3-preview-202502)
   - [6.5 Hermes 4 (2025.08) — 메인](#65-hermes-4-202508--메인)
   - [6.6 Hermes 4.3 (2025.12) — Psyche 첫 모델](#66-hermes-43-202512--psyche-첫-모델)
7. [벤치마크: 숫자로 보는 성능](#7-벤치마크-숫자로-보는-성능)
8. [사용 방법: 호스팅 & 로컬 실행](#8-사용-방법-호스팅--로컬-실행)
9. [Nous 생태계: 모델 너머의 이야기](#9-nous-생태계-모델-너머의-이야기)
   - [9.1 Hermes Agent Framework](#91-hermes-agent-framework)
   - [9.2 Psyche 네트워크 & DisTrO](#92-psyche-네트워크--distro)
   - [9.3 $50M 시리즈 A & Paradigm](#93-50m-시리즈-a--paradigm)
10. [유즈케이스 & 실사용 평가](#10-유즈케이스--실사용-평가)
11. [한계 & 리스크: 솔직한 비판](#11-한계--리스크-솔직한-비판)
12. [결론](#12-결론)
13. [참고문헌](#13-참고문헌)

---

## 1. Hermes가 뭔데요?

솔직히 오픈소스 LLM 씬에서 "Hermes"를 모른다면 좀 늦은 거예요. 2023년 처음 등장한 이후로 Nous Research의 Hermes 시리즈는 오픈웨이트 파인튜닝 LLM의 가장 유명한 계보 중 하나가 됐거든요.

핵심을 한 문장으로 정리하면: **Llama·Mistral·Qwen 같은 베이스 모델을 잘 골라서, 고품질 데이터로 파인튜닝해 "사용자가 시스템 프롬프트로 완전히 제어할 수 있는" 어시스턴트를 만드는 것**이 Hermes의 존재 이유예요.

"Hermes"라는 이름이 붙은 다른 것들도 있긴 한데요:
- **Hermes Agent** — Nous Research가 2026년 출시한 오픈소스 에이전트 프레임워크 (별개 제품)
- 수학적 추론 관련 arXiv 논문에도 "HERMES"가 등장하지만 Nous와 무관

이 글의 주제는 **Nous Research의 Hermes LLM 모델 시리즈**에요.

---

## 2. 시리즈 계보 한눈에 보기

| 세대 | 출시 시점 | 베이스 모델 | 파라미터 | 핵심 혁신 |
|------|----------|------------|---------|----------|
| **OpenHermes 1** | 2023 중반 | Llama 7B/13B | 7B, 13B | ChatML 포맷 정착, GPT-4 합성 데이터 |
| **OpenHermes 2.5** | 2023 하반기 | Mistral 7B | 7B | 100만 항목 GPT-4 품질 데이터 |
| **Hermes 2 Pro** | 2024.05 | Llama 2/3, Mistral | 7B, 8B | `<tool_call>` 토큰, function calling 90% 정확도 |
| **Hermes 3** | 2024.08 | Llama 3.1 | 3B, 8B, 70B, 405B | 전 사이즈 라인업, 에이전트 개선, MT-Bench 1위 |
| **DeepHermes 3 Preview** | 2025.02 | Llama 3.1 | 3B, 8B, 24B | `<think>` 토글, reasoning/chat 통합 첫 모델 |
| **Hermes 4** | 2025.08 | Llama 3.1 | 14B, 70B, 405B | 하이브리드 reasoning, DataForge, 50x 데이터 확장 |
| **Hermes 4.3** | 2025.12 | Seed-OSS-36B (ByteDance) | 36B | 512K 컨텍스트, Psyche 분산 학습 첫 프로덕션 모델 |

> "Hermes 3 is a generalist language model with many improvements over Hermes 2, including advanced agentic capabilities, much better roleplaying, reasoning, multi-turn conversation, long context coherence." — [Hermes 3 Technical Report](https://arxiv.org/pdf/2408.11857), Nous Research, 2024
>
> Hermes 3는 단순한 버전업이 아니라 Llama 3.1 전 사이즈를 커버하는 첫 라인업이었어요. 특히 405B 모델은 당시 오픈소스 진영 최대 파인튜닝 모델 중 하나였죠.

---

## 3. Nous Research라는 곳

[Nous Research](https://nousresearch.com/)는 2023년 설립된 AI 연구 집단이에요. 창업자 라인업을 보면:

- **Jeffrey Quesnelle** — CEO
- **Karan Malhotra** — Head of Behavior
- **Teknium** (실명 Ryan) — Head of Post Training (X: [@Teknium1](https://x.com/Teknium1))
- **Shivani Mitra** — 공동창업자

"Teknium"이라는 핸들이 오픈소스 LLM 커뮤니티에선 꽤 유명한데요, OpenHermes 데이터셋을 직접 큐레이팅하고 배포한 인물이에요. HuggingFace에서 `teknium/OpenHermes-2.5` 같은 데이터셋을 찾으면 바로 이 분이 관리자예요.

회사 방향성을 한 마디로: **오픈소스 + 분산화 + 사용자 주권**. 폐쇄형 거대 랩들의 중앙집권식 개발에 대한 반발로 형성된 정체성이에요.

자금 면에서는 2025년 4월 [Paradigm 주도 5,000만 달러 시리즈 A](https://siliconangle.com/2025/04/25/nous-research-raises-50m-decentralized-ai-training-led-paradigm/)를 클로즈했고, 밸류에이션 10억 달러 (토큰 포함)를 달성했어요.

> "This open, community-oriented approach is a powerful contrast to the closed, centralized efforts from incumbent labs." — Arjun Balaji, Paradigm Partner
>
> 암호화폐 VC인 Paradigm이 AI 스타트업에 베팅한 게 특이한데, 이유가 있어요 — Nous의 분산 학습 인프라(Psyche)가 Solana 블록체인 기반이거든요.

---

## 4. 핵심 철학: "Steerable" 어시스턴트

Nous Hermes의 가장 독특한 점은 **시스템 프롬프트 제어권**에 대한 철학이에요.

대부분의 상용 모델은 안전 필터가 하드코딩돼 있어서 특정 콘텐츠를 시스템 프롬프트로 허용해도 거절해요. Hermes는 반대로 **시스템 프롬프트가 명시한 대로 동작**하는 걸 목표로 해요.

공식 표현으로는:

> "Focused on aligning LLMs to the user, with powerful steering capabilities and control given to the end user and operator." — [Hermes 3 Technical Report](https://arxiv.org/pdf/2408.11857)
>
> "사용자와 오퍼레이터에게 강력한 스티어링 능력과 제어권을 줌으로써 LLM을 사용자에게 맞추는 것"에 집중한다는 뜻이에요.

이게 실제로는:
- 캐릭터 롤플레이에서 캐릭터를 벗어나지 않음
- 시스템 프롬프트로 응답 스타일/언어/거절 패턴을 완전히 커스텀 가능
- `<think>` 태그 사용 여부를 사용자가 명시적으로 제어

RefusalBench라는 벤치마크에서 Hermes 4가 GPT-4o(17.67%), Claude Sonnet 4(17%)를 크게 제치고 57.1%를 기록한 것도 이 맥락이에요 — 불필요한 거절 최소화를 평가하는 벤치마크거든요.

---

## 5. ChatML: 모든 버전의 공통 언어

Hermes 1부터 4.3까지 모든 버전이 동일한 **ChatML** 포맷을 사용해요. OpenAI가 쓰는 포맷과 동일해서 OpenAI API 호환 툴체인에서 바로 쓸 수 있어요.

```
<|im_start|>system
당신은 도움이 되는 AI 어시스턴트입니다.<|im_end|>
<|im_start|>user
질문 내용<|im_end|>
<|im_start|>assistant
```

Function calling은 별도 XML 태그를 사용해요:

```xml
<tools>
[{"name": "get_weather", "description": "...", "parameters": {...}}]
</tools>

<tool_call>
{"name": "get_weather", "arguments": {"location": "Seoul"}}
</tool_call>

<tool_response>
{"temperature": 22, "condition": "맑음"}
</tool_response>
```

> "ChatML opening up a much more structured system for engaging the LLM in multi-turn chat dialogue... enables OpenAI endpoint compatibility." — [HuggingFace Hermes 2 Pro Mistral](https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B), Nous Research
>
> 이게 진짜 중요한 이유가 뭐냐면요, ChatML을 처음부터 채택한 덕분에 OpenAI SDK, LangChain, vLLM, Ollama 등 거의 모든 툴체인에서 설정 없이 바로 써요.

---

## 6. 세대별 심층 분석

### 6.1 OpenHermes → Hermes 1 (2023)

Teknium이 [teknium/openhermes](https://huggingface.co/datasets/teknium/openhermes) 데이터셋을 공개하고, 이를 Llama 7B/13B에 파인튜닝한 게 출발점이에요.

데이터 구성은 GPT-4로 생성된 인스트럭션-응답 쌍이 중심이고, WizardLM, GPTeacher, Code Instruct Datasets에서 필터링한 데이터가 섞여 있어요. 총 24만 항목에서 시작해서 OpenHermes 2.5에서 100만 항목까지 확장됐죠.

가장 중요한 기여: **ChatML 포맷 채택**. 이게 후속 모든 버전의 인터페이스 표준이 됐어요.

OpenHermes 2.5 Mistral 7B는 [Simon Willison](https://simonwillison.net/2024/Feb/1/open-hermes-25/)이 직접 리뷰할 정도로 커뮤니티 반응이 좋았어요 — 당시 7B급 모델 중 벤치마크 최상위권이었거든요.

### 6.2 Hermes 2 / 2 Pro (2024)

**Hermes 2**는 Llama 2와 Mistral을 베이스로 약 100만 항목의 합성·큐레이션 데이터로 학습했어요. Yi-34B, Mixtral 8x7B 같은 다양한 베이스에도 적용됐고요.

**Hermes 2 Pro** (2024년 5월)가 진짜 도약이었어요:

- `<tool_call>` 전용 토큰 도입 → function calling 구조화
- [Fireworks.AI와 공동 개발한 평가 셋](https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B)에서 **function calling 90%, JSON 모드 84%** 달성
- OpenHermes 2.5 데이터셋을 클리닝+업데이트한 버전 + 인하우스 function calling 데이터셋 추가

당시 7B 파라미터 모델이 10배 큰 모델들과 경쟁했다는 게 인상적이에요.

### 6.3 Hermes 3 (2024.08)

[기술 보고서](https://arxiv.org/pdf/2408.11857) 기준으로 Hermes 3는 **Llama 3.1** 전 라인업을 커버했어요:

| 모델 | 베이스 | 컨텍스트 |
|------|-------|---------|
| Hermes 3 3B | Llama 3.2 3B | 131K |
| Hermes 3 8B | Llama 3.1 8B | 131K |
| Hermes 3 70B | Llama 3.1 70B | 131K |
| Hermes 3 405B | Llama 3.1 405B | 131K |

주요 개선 사항:
- **시스템/인스트럭션 프롬프트 준수 강화** — "aggressively encourages the model to follow system and instruction prompts exactly"
- 멀티턴 대화 일관성, 롤플레이, 에이전트 도구 사용 대폭 개선
- MT-Bench에서 Hermes 3 70B가 12개 평가 모델 중 1위(8.990점) 달성

OpenRouter에서 Hermes 3 405B를 [무료로 제공](https://openrouter.ai/nousresearch/hermes-3-llama-3.1-405b:free)하는 건 여전히 유지 중이에요.

### 6.4 DeepHermes 3 Preview (2025.02)

> "Introducing DeepHermes-3 Preview, a new LLM that unifies reasoning and intuitive language model capabilities." — [@NousResearch](https://x.com/NousResearch/status/1890148000204485088), 2025.02
>
> 세계 최초로 reasoning 모드와 일반 대화 모드를 단일 모델에서 토글할 수 있게 만든 모델이에요.

**DeepHermes 3**는 o1-style long chain-of-thought와 일반 어시스턴트 기능을 통합한 첫 시도였어요.

- **베이스**: Hermes 3 데이터믹스 + 15만 개 chain-of-thought 예시
- **크기**: 8B (2025.02 출시) → 3B, 24B (2025.03.13 확장)
- **토글 방식**: 시스템 프롬프트에 "enable deep thinking" 지시 → `<think>...</think>` 자동 생성

성능 면에서는 MATH 벤치에서 67% 수준으로 DeepSeek R1 distilled(89.1%)보다 낮았지만, "순수 reasoning 모델"이 아닌 "reasoning과 대화를 함께 잘하는 모델"이라는 포지셔닝이었어요.

### 6.5 Hermes 4 (2025.08) — 메인

Hermes 4는 2025년 8월 26일 출시된 메인 플래그십이에요. [기술 보고서](https://arxiv.org/pdf/2508.18255)가 arXiv에 공개돼 있어요.

#### 모델 패밀리

| 모델 | 베이스 | 파라미터 |
|------|-------|---------|
| Hermes 4 14B | Llama 3.1 14B | 14B |
| Hermes 4 70B | Llama 3.1 70B | 70B |
| Hermes 4 405B | Llama 3.1 405B | 405B |

#### 핵심 기술

**DataForge**: 그래프 기반 합성 데이터 생성 시스템. DAG(방향 비순환 그래프) 구조로 약 **500만 샘플, 190억 토큰** 생성. Hermes 3 대비 50배 데이터 확장.

**Rejection Sampling**: 약 1,000개의 태스크별 검증기를 사용해 생성된 데이터를 필터링. 수학 문제는 정답 검증, 코드는 실행 테스트, 지식 Q&A는 교차 검증.

**하이브리드 Reasoning 모드**: `<think>...</think>` 태그로 추론 모드 토글. 추론 샘플은 비추론 샘플 대비 평균 5배 더 길어서 데이터 불균형 처리가 핵심이었음.

**학습 인프라**: NVIDIA B200 GPU 192개, TorchTitan 스택(flex attention 포함), 배치 효율 99.9% 이상 달성.

### 6.6 Hermes 4.3 (2025.12) — Psyche 첫 모델

[공식 발표 포스트](https://nousresearch.com/introducing-hermes-4-3)에 따르면 Hermes 4.3은 두 가지 이유로 특별해요:

1. **베이스가 Llama가 아니에요** — ByteDance의 [Seed-OSS-36B-Base](https://huggingface.co/ByteDance-Seed/Seed-Coder-8B-Base)를 베이스로 사용. Hermes 역사상 처음으로 Meta 외 베이스 채택.

2. **Psyche 분산 학습 첫 프로덕션 모델** — 전통적인 중앙집중식 클러스터가 아니라, 인터넷에 분산된 여러 데이터센터에서 DisTrO 옵티마이저로 학습.

주요 스펙:
- **컨텍스트**: 512K 토큰 (Hermes 시리즈 최장)
- **목표**: Hermes 4 70B와 유사한 성능을 절반 파라미터(36B)로

Psyche 학습 인프라:
- 24개 노드, 초당 144K 토큰 평균 처리량
- Solana 블록체인 기반 합의 메커니즘으로 노드 기여 검증
- P2P 메시 네트워크로 그래디언트 통신

---

## 7. 벤치마크: 숫자로 보는 성능

### Hermes 4 405B vs 동급 모델

아래 표는 공개된 [기술 보고서](https://arxiv.org/pdf/2508.18255)와 [MARKTechPost](https://www.marktechpost.com/2025/08/27/nous-research-team-releases-hermes-4-a-family-of-open-weight-ai-models-with-hybrid-reasoning/)의 수치를 기반으로 정리한 거예요. "R" = reasoning 모드 활성화.

| 벤치마크 | Hermes 4 405B (R) | Hermes 4 405B | DeepSeek R1 671B | DeepSeek V3 671B | GPT-4o |
|---------|-----------------|--------------|-----------------|----------------|-------|
| MMLU | 87.2 | 73.6 | 91.4 | 90.4 | ~88 |
| GPQA Diamond | 70.5 | 39.4 | 68.2 | 78.1 | 53.6 |
| MATH-500 | **96.3** | 73.8 | 91.8 | 97.5 | 76.6 |
| AIME'24 | 81.9 | — | 79.8 | 39.2 | 9.3 |
| AIME'25 | 78.1 | — | — | — | — |
| LiveCodeBench | 61.3 | — | 65.9 | 51.6 | — |
| IFEval (Loose) | 81.5 | 84.9 | 91.6 | 90.0 | — |
| RefusalBench | **57.1** | — | — | — | 17.67 |

**주의사항**: RefusalBench는 "불필요한 거절 최소화"를 측정해요. 높은 점수 = 더 도움이 됨. 그러나 이 메트릭이 안전성 트레이드오프를 의미할 수 있다는 점은 아래 한계 섹션에서 다룰게요.

### Hermes 3 vs Hermes 2 vs 베이스 모델 비교

| 모델 | 베이스 | MT-Bench | 특이사항 |
|------|-------|---------|---------|
| Hermes 3 70B | Llama 3.1 70B | **8.990** (12개 모델 중 1위) | 오픈소스 최상위 당시 |
| Hermes 3 8B | Llama 3.1 8B | — | 에이전트 워크플로 추천 |
| Hermes 2 Pro Mistral 7B | Mistral 7B | — | Function calling 90% |
| DeepHermes 3 8B | Llama 3.1 8B | — | MATH 67% (reasoning 모드) |

### VRAM별 모델 선택 가이드

| VRAM | 권장 모델 | 특징 |
|------|---------|------|
| 4GB | Hermes 3 3B (Q4) | 기본 대화 |
| 6~8GB | Hermes 3 8B (Q4_K_M) | 40~60 tok/s on RTX 4060 |
| 24GB | Hermes 4.3 36B (Q4) | 512K 컨텍스트, 최고 가성비 |
| 48GB+ | Hermes 4 70B | 프로덕션 품질 |
| 멀티노드 | Hermes 4 405B | 프론티어급 |

---

## 8. 사용 방법: 호스팅 & 로컬 실행

### 클라우드 API

| 플랫폼 | 모델 | 입력 가격 | 출력 가격 | 비고 |
|-------|------|---------|---------|------|
| [OpenRouter](https://openrouter.ai/nousresearch) | Hermes 4 70B | $0.13/M | $0.40/M | OpenAI 호환 |
| OpenRouter | Hermes 4 405B | $1.00/M | $3.00/M | |
| OpenRouter | Hermes 3 405B | **무료** | **무료** | 커뮤니티 풀 |
| OpenRouter | Hermes 3 70B | $0.30/M | $0.30/M | |
| [Nous Portal](https://portal.nousresearch.com/) | 200+ 모델 집계 | 다양 | 다양 | Nous 자체 포털 |
| Together AI | Hermes 3 시리즈 | 다양 | 다양 | |
| Hyperbolic | Hermes 4 시리즈 | 다양 | 다양 | |

### 로컬 실행

**Ollama** (가장 쉬운 방법):
```bash
ollama pull nous-hermes3:8b
ollama run nous-hermes3:8b
# 또는 API로
curl http://localhost:11434/api/chat -d '{
  "model": "nous-hermes3:8b",
  "messages": [{"role": "user", "content": "안녕하세요"}]
}'
```

**llama.cpp**:
```bash
# GGUF 다운로드 후
./llama-cli -m Hermes-3-Llama-3.1-8B.Q4_K_M.gguf \
  --chat-template chatml \
  -p "당신은 도움이 되는 어시스턴트입니다."
```

**vLLM** (고성능 서빙):
```bash
vllm serve NousResearch/Hermes-3-Llama-3.1-8B \
  --chat-template chatml \
  --max-model-len 32768
```

**HuggingFace Transformers**: 예시 코드는 `examples/` 폴더 참조.

---

## 9. Nous 생태계: 모델 너머의 이야기

### 9.1 Hermes Agent Framework

[Hermes Agent](https://hermes-agent.nousresearch.com/)는 LLM 모델과는 별개의 **오픈소스 에이전트 프레임워크**예요. 2026년 초 출시되어 두 달 만에 GitHub Star 27,000+를 달성했고, OpenRouter 글로벌 에이전트 사용량 1위를 기록했어요.

> "Every time Hermes encounters a complex task or receives feedback, it writes and stores the outcome as a reusable skill." — [NVIDIA Blog](https://blogs.nvidia.com/blog/rtx-ai-garage-hermes-agent-dgx-spark/)
>
> "자기 개선(self-improving)" 에이전트예요. 태스크를 성공/실패할 때마다 그 결과를 스킬로 저장해서 다음에 재사용해요.

v0.9.0 "Everywhere" 릴리즈 (2026.04.13) 기준:
- 지원 플랫폼: 16개 메시징 플랫폼 (iMessage/BlueBubbles, WeChat, WeCom, Android/Termux 등)
- 모델 에이전스틱: Claude/GPT-4/Gemini/로컬 Ollama 모델 모두 지원
- NVIDIA RTX PCs 및 DGX Spark 최적화

### 9.2 Psyche 네트워크 & DisTrO

[Psyche](https://nousresearch.com/nous-psyche/)는 Nous의 가장 야심찬 프로젝트예요 — 분산된 GPU를 인터넷으로 연결해 협력 학습하는 네트워크.

핵심 기술인 [DisTrO (Distributed Training Over-The-Internet)](https://github.com/NousResearch/DisTrO)는:

- **DeMo(Decoupled Momentum)** 옵티마이저: 그래디언트를 고빈도로 동기화하지 않고, 저대역폭으로도 분산 학습 가능하게 함
- 2024년 12월: 15B 파라미터 모델 11,000 스텝 학습 성공 (여러 데이터센터 분산)
- 2025년 12월: Hermes 4.3으로 **프로덕션 모델 첫 Psyche 학습** 달성

Solana 블록체인이 각 노드의 학습 기여를 검증하는 합의 레이어로 사용돼요. 향후 $NOUS 토큰 생태계와 연계될 예정이에요.

### 9.3 $50M 시리즈 A & Paradigm

2025년 4월 [Paradigm 주도 5,000만 달러 시리즈 A](https://siliconangle.com/2025/04/25/nous-research-raises-50m-decentralized-ai-training-led-paradigm/) 클로즈. 이전 시드 라운드 약 2,000만 달러 포함 총 7,000만 달러 이상 조달.

Paradigm은 암호화폐 전문 VC라서 이 투자가 흥미로운 건데 — Nous의 Psyche/Solana 연계가 직접적인 투자 근거예요. "분산 AI" 테마에서 Web3와 AI 교차점을 노린 베팅이죠.

---

## 10. 유즈케이스 & 실사용 평가

**잘 맞는 케이스:**

1. **캐릭터 롤플레이 & 크리에이티브 라이팅**: 시스템 프롬프트 제어력이 뛰어나서 캐릭터를 이탈하지 않음. Hermes 3 이후로는 커뮤니티 RP 워크플로에서 기본 모델로 자리잡음.

2. **Function Calling 에이전트**: `<tool_call>` 토큰 구조가 명확해서 파싱이 쉬움. Hermes 2 Pro부터 현재까지 function calling 지원이 일관적.

3. **프라이버시 민감 온프레미스 배포**: 로컬 실행 최적화(GGUF 제공), 데이터가 외부로 나가지 않음.

4. **시스템 프롬프트 제어 중심 앱**: 커스텀 어시스턴트, 도메인 특화 챗봇에서 안전 필터 없이 정확한 페르소나 구현.

**한국어 성능**: 공식 한국어 벤치마크 결과는 기술 보고서에 포함되지 않았어요. 베이스 모델(Llama 3.1)의 다국어 학습 데이터를 상속하지만, Nous의 파인튜닝 데이터 대부분이 영어 중심이라 한국어는 베이스 모델 수준이라고 보면 돼요.

---

## 11. 한계 & 리스크: 솔직한 비판

### 벤치마크와 실사용 괴리

RefusalBench에서 압도적 1위(57.1%)를 했지만, 이 메트릭은 "도움이 되는 응답 비율"을 측정하는 것이지 응답 품질 자체를 측정하는 게 아니에요. GPT-4o가 17.67%라는 건 GPT-4o가 더 많이 거절한다는 의미지, Hermes 4가 품질이 더 좋다는 의미가 아니에요.

MMLU에서는 DeepSeek R1(91.4%), DeepSeek V3(90.4%) 대비 Hermes 4 405B가 reasoning 모드에서 87.2%로 뒤처지고, IFEval(지시 따르기)에서도 84.9%로 DeepSeek 계열(90~91%)에 미치지 못해요.

### 검열 최소화의 양면성

Hermes의 "사용자 주권" 철학은 실용적이고 매력적이지만, 실제로는 양날의 검이에요. 안전 필터를 시스템 프롬프트로 우회할 수 있다는 건 정당한 사용자뿐만 아니라 악성 사용자에게도 똑같이 적용돼요. Nous는 이 책임을 "오퍼레이터"에게 전가하는 방식을 취하는데, 오퍼레이터가 책임질 수 없는 개인 사용 환경에서는 리스크가 그대로 남아요.

### 라이선스 복잡성

Hermes 4의 Llama 3.1 기반 모델은 [Meta의 Llama 3.1 Community License](https://ai.meta.com/llama/license/)를 상속해요. 월 사용자 7억 명 이상의 서비스에선 상용 사용 라이선스가 별도로 필요해요. Hermes 4.3은 Seed-OSS 기반이어서 ByteDance의 라이선스 조건을 따르고요.

### 클로즈드 모델 대비 성능 격차

2026년 현재 기준으로 Anthropic Claude 3.7 Sonnet, GPT-4o, Gemini 2.0 같은 최신 폐쇄형 모델과 비교하면 전반적인 능력(coding, instruction following, multilingual)에서 여전히 격차가 있어요. Hermes가 앞서는 건 RefusalBench처럼 Nous가 직접 설계에 영향을 미친 영역 또는 특정 reasoning 태스크에 한정돼요.

### Psyche/Crypto 리스크

분산 학습 + Solana 블록체인 조합은 기술적으로 흥미롭지만, 암호화폐 생태계 변동성이 인프라 안정성에 영향을 미칠 수 있어요. $NOUS 토큰 가치가 하락하면 노드 참여 인센티브가 줄어들고, 그게 Psyche 네트워크 품질로 이어질 수 있는 구조예요.

---

## 12. 결론

Hermes 시리즈는 오픈소스 LLM 파인튜닝의 가장 일관된 계보 중 하나예요. 2023년 ChatML 포맷을 처음 정착시킨 것부터 2025년 Hermes 4의 DataForge 기반 대규모 합성 데이터 학습까지, 방향성이 일관해요: **사용자 제어권 극대화 + 데이터 품질 집착 + 오픈소스 공개**.

특히 주목할 포인트는 두 가지예요:

1. **Hermes 4.3 + Psyche 조합** — 분산 학습으로 프로덕션 모델을 만들 수 있다는 걸 실제로 증명했어요. 향후 Psyche 네트워크가 확장되면 "누구나 AI 학습에 참여한다"는 비전이 현실화될 수 있어요.

2. **Hermes Agent 프레임워크** — LLM 모델을 넘어서 에이전트 레이어로의 확장이 시작됐고, 반응 속도(3개월 만에 GitHub Star 27,000)는 커뮤니티 수요가 실재함을 보여줘요.

단점도 솔직히 얘기하면, 최신 폐쇄형 모델 대비 전반적인 성능에서는 아직 격차가 있고, RefusalBench 최우수가 곧 "최고의 모델"을 의미하진 않아요. 그러나 프라이버시, 비용, 커스터마이즈 가능성 중심으로 평가한다면 Hermes는 여전히 최우선 고려 대상이에요.

---

## 13. 참고문헌

| # | 제목 | 출처 | URL |
|---|------|------|-----|
| 1 | Hermes 3 Technical Report | arXiv / Nous Research | https://arxiv.org/pdf/2408.11857 |
| 2 | Hermes 4 Technical Report | arXiv / Nous Research | https://arxiv.org/pdf/2508.18255 |
| 3 | Introducing Hermes 4.3: Local Intelligence Globally Trained | Nous Research 공식 블로그 | https://nousresearch.com/introducing-hermes-4-3 |
| 4 | Nous Research Releases Hermes 4 | MarkTechPost | https://www.marktechpost.com/2025/08/27/nous-research-team-releases-hermes-4-a-family-of-open-weight-ai-models-with-hybrid-reasoning/ |
| 5 | DeepHermes 3 Preview Release | MarkTechPost | https://www.marktechpost.com/2025/02/15/nous-research-released-deephermes-3-preview-a-llama-3-8b-based-model-combining-deep-reasoning-advanced-function-calling-and-seamless-conversational-intelligence/ |
| 6 | Nous Research API and Models | OpenRouter | https://openrouter.ai/nousresearch |
| 7 | Hermes 4 Model Page | Nous Research | https://hermes4.nousresearch.com/ |
| 8 | Hermes Agent Documentation | Nous Research | https://hermes-agent.nousresearch.com/ |
| 9 | Democratizing AI: The Psyche Network Architecture | Nous Research 공식 블로그 | https://nousresearch.com/nous-psyche/ |
| 10 | DisTrO GitHub Repository | NousResearch | https://github.com/NousResearch/DisTrO |
| 11 | Nous Research raises $50M (Paradigm) | SiliconANGLE | https://siliconangle.com/2025/04/25/nous-research-raises-50m-decentralized-ai-training-led-paradigm/ |
| 12 | Hermes Unlocks Self-Improving AI Agents | NVIDIA Blog | https://blogs.nvidia.com/blog/rtx-ai-garage-hermes-agent-dgx-spark/ |
| 13 | NousResearch/Hermes-2-Pro-Mistral-7B | HuggingFace | https://huggingface.co/NousResearch/Hermes-2-Pro-Mistral-7B |
| 14 | NousResearch/Hermes-3-Llama-3.1-8B | HuggingFace | https://huggingface.co/NousResearch/Hermes-3-Llama-3.1-8B |
| 15 | teknium/OpenHermes-2.5-Mistral-7B | HuggingFace | https://huggingface.co/teknium/OpenHermes-2.5-Mistral-7B |
| 16 | DeepHermes-3-Llama-3-8B-Preview | HuggingFace | https://huggingface.co/NousResearch/DeepHermes-3-Llama-3-8B-Preview |
| 17 | Hermes LLM Explained (2026) | Fast.io | https://fast.io/resources/hermes-llm/ |
| 18 | Nous Research AI Wiki | AI Wiki | https://aiwiki.ai/wiki/nous_research |
| 19 | Hermes 4 VentureBeat Coverage | VentureBeat | https://venturebeat.com/ai/nous-research-drops-hermes-4-ai-models-that-outperform-chatgpt-without-content-restrictions |
| 20 | DeepHermes-3 VentureBeat | VentureBeat | https://venturebeat.com/ai/personalized-unrestricted-ai-lab-nous-research-launches-first-toggle-on-reasoning-model-deephermes-3 |
| 21 | OpenHermes 2.5 (Simon Willison) | Simon Willison's Blog | https://simonwillison.net/2024/Feb/1/open-hermes-25/ |
| 22 | Nous Research Deep Dive (Gate.com) | Gate News | https://www.gate.com/news/detail/nous-research-deep-dive-a-decentralized-ai-lab-that-paradigm-invested-in-at-20290685 |
| 23 | Hermes Function Calling GitHub | NousResearch | https://github.com/NousResearch/Hermes-Function-Calling |
| 24 | OpenRouter Hermes Comparison | Artificial Analysis | https://artificialanalysis.ai/models/hermes-3-llama-3-1-70b |
| 25 | Hermes Agent v0.9 Review | heyuan110.com | https://www.heyuan110.com/posts/ai/2026-04-14-hermes-agent-guide/ |

---

*이 문서는 2026-05-22 기준 공개된 정보를 바탕으로 작성됐습니다. Nous Research는 활발하게 개발 중이므로 최신 정보는 [공식 사이트](https://nousresearch.com)와 [HuggingFace 페이지](https://huggingface.co/NousResearch)를 확인하세요.*

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. Hermes 시리즈의 가장 핵심적인 설계 철학은 뭘까요? 한 단어로 표현하면 "steerable"인데, 이게 구체적으로 무엇을 의미하나요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 시스템 프롬프트로 모델의 동작을 사용자/오퍼레이터가 완전히 제어할 수 있게 하는 것 (사용자 주권, 스티어링 능력)

**해설**: 대부분의 상용 모델은 안전 필터가 하드코딩돼 있어서 시스템 프롬프트로 허용해도 거절하는 경우가 많은데요, Hermes는 반대로 시스템 프롬프트가 명시한 대로 동작하는 걸 목표로 해요. 응답 스타일, 거절 패턴, 캐릭터 롤플레이까지 전부 시스템 프롬프트로 커스텀할 수 있다는 게 핵심이죠.

</details>

**Q2. (OX) Hermes 시리즈는 버전마다 프롬프트 포맷이 달라서, 버전을 바꿀 때마다 툴체인 설정을 새로 해야 한다.**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X

**해설**: Hermes 1부터 4.3까지 모든 버전이 동일한 ChatML 포맷을 사용해요. OpenAI가 쓰는 포맷과 같아서 OpenAI SDK, LangChain, vLLM, Ollama 등 거의 모든 툴체인에서 별도 설정 없이 바로 쓸 수 있다는 게 Hermes의 큰 장점이죠.

</details>

**Q3. DeepHermes 3 Preview가 "세계 최초"라고 불린 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: reasoning 모드와 일반 대화 모드를 단일 모델에서 토글할 수 있게 만든 첫 모델이라서

**해설**: 시스템 프롬프트에 "enable deep thinking" 지시를 넣으면 `<think>...</think>` 태그로 긴 chain-of-thought를 생성하고, 빼면 일반 어시스턴트처럼 동작해요. 순수 reasoning 모델보다 수학 점수는 낮았지만, "추론과 대화를 한 모델에서 함께 잘하는" 포지셔닝 자체가 새로웠던 거죠. 이 하이브리드 접근은 Hermes 4로 이어졌어요.

</details>

**Q4. Hermes 4의 핵심 기술인 DataForge와 Rejection Sampling은 각각 어떤 역할을 하나요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: DataForge는 그래프(DAG) 기반 합성 데이터 생성 시스템이고, Rejection Sampling은 태스크별 검증기로 생성된 데이터를 필터링하는 품질 관리 장치예요.

**해설**: DataForge가 대량의 합성 데이터를 만들어내면(Hermes 3 대비 50배 확장), 약 1,000개의 태스크별 검증기가 수학은 정답 검증, 코드는 실행 테스트, 지식 Q&A는 교차 검증으로 걸러내요. "데이터를 많이 만들고, 엄격하게 거른다"는 투트랙이 Hermes 4 품질의 핵심이죠.

</details>

**Q5. Hermes 4.3이 시리즈 역사에서 특별한 이유 두 가지는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: (1) Hermes 역사상 처음으로 Meta가 아닌 베이스 모델(ByteDance Seed-OSS-36B)을 사용했고, (2) Psyche 분산 학습 네트워크로 만든 첫 프로덕션 모델이에요.

**해설**: 그동안 Hermes는 Llama·Mistral 계열을 베이스로 써왔는데 4.3에서 처음 ByteDance 모델을 채택했어요. 더 큰 의미는 학습 방식인데요, 중앙집중식 클러스터가 아니라 인터넷에 분산된 여러 데이터센터에서 DisTrO 옵티마이저로 학습해서 "분산 학습으로 프로덕션 모델을 만들 수 있다"는 걸 실제로 증명했죠.

</details>

**Q6. RefusalBench에서 Hermes 4가 57.1%로 GPT-4o(17.67%)를 크게 앞섰는데요, 이 결과를 "Hermes 4가 GPT-4o보다 좋은 모델"이라고 해석하면 안 되는 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: RefusalBench는 "불필요한 거절을 얼마나 적게 하는지"를 측정하는 벤치마크지, 응답 품질 자체를 측정하는 게 아니기 때문이에요.

**해설**: GPT-4o의 17.67%는 GPT-4o가 더 많이 거절한다는 의미일 뿐이에요. 실제로 MMLU나 IFEval 같은 일반 능력 벤치마크에서는 Hermes 4가 DeepSeek 계열보다 뒤처지죠. 게다가 거절을 줄이는 건 안전성 트레이드오프를 동반할 수 있어서, 악성 사용자에게도 똑같이 적용된다는 양면성이 있어요.

</details>

**Q7. (시나리오) 회사 내부 데이터를 외부로 보낼 수 없는 환경에서, 24GB VRAM GPU 한 장으로 긴 문서를 다루는 커스텀 어시스턴트를 만들려고 해요. 본문 기준으로 어떤 선택이 적절할까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Hermes 4.3 36B (Q4 양자화)를 로컬로 실행하는 것

**해설**: 본문의 VRAM별 가이드에서 24GB 구간 권장 모델이 Hermes 4.3 36B(Q4)인데요, 512K 토큰이라는 시리즈 최장 컨텍스트를 지원해서 긴 문서 처리에 유리해요. 프라이버시 민감 온프레미스 배포는 Hermes가 잘 맞는 대표 유즈케이스이기도 하고, 시스템 프롬프트 제어력 덕분에 커스텀 페르소나 구현도 정확하죠.

</details>

**Q8. Psyche 네트워크에서 Solana 블록체인은 어떤 역할을 하고, 이 구조의 잠재적 리스크는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Solana는 각 노드의 학습 기여를 검증하는 합의 레이어 역할을 해요. 리스크는 암호화폐 생태계 변동성이 인프라 안정성으로 전이될 수 있다는 점이에요.

**해설**: Psyche는 분산된 GPU 노드들이 P2P로 그래디언트를 주고받으며 학습하는데, 누가 얼마나 기여했는지를 Solana 기반 합의로 검증해요. 문제는 $NOUS 토큰 가치가 하락하면 노드 참여 인센티브가 줄어들고, 그게 네트워크 품질 저하로 이어질 수 있는 구조라는 거죠.

</details>
