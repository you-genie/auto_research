# 주요 PLM 논문들은 모델을 어떻게 평가했나? — GPT부터 DeepSeek·Qwen·Gemma까지 평가 방법론 비교 분석

> "The diversity of the tasks the model is tested on is as important as the number of parameters."
> — 여러 LLM 평가 연구자들이 공통으로 강조하는 원칙

사전학습 언어모델(PLM, Pretrained Language Model)이 폭발적으로 늘어나면서, **"이 모델이 진짜 잘하는 건지 어떻게 알 수 있어?"** 라는 질문이 점점 더 중요해졌어요. 근데 재밌는 게, 각 연구팀마다 평가를 조금씩 다르게 설계해왔거든요. GPT-1이 나왔던 2018년이랑 DeepSeek-V3가 나온 2024년의 평가 방식은 완전히 다른 세계예요.

이 글에서는 주요 PLM 논문들 — GPT 시리즈, InstructGPT, Qwen, DeepSeek, Gemma — 에서 **base model(사전학습 모델 자체)을 어떻게 평가했는지**를 집중적으로 뜯어볼 거예요. 단순 성능 비교가 아니라, *왜 그런 방식으로 평가했는지*, *시대별로 어떻게 달라졌는지*, *지금 기준으로 뭐가 문제인지*까지 파고들어 볼게요.

---

## 목차

1. [평가 방법론의 시대적 진화](#1-평가-방법론의-시대적-진화)
2. [GPT 시리즈의 평가 방법](#2-gpt-시리즈의-평가-방법)
3. [InstructGPT — Base vs. RLHF 모델 평가의 분리](#3-instructgpt--base-vs-rlhf-모델-평가의-분리)
4. [Qwen 시리즈의 평가 전략](#4-qwen-시리즈의-평가-전략)
5. [DeepSeek의 Base Model 평가 심층 분석](#5-deepseek의-base-model-평가-심층-분석)
6. [Gemma 시리즈의 평가 방법론](#6-gemma-시리즈의-평가-방법론)
7. [주요 벤치마크 매트릭스 — 모델별 사용 현황](#7-주요-벤치마크-매트릭스--모델별-사용-현황)
8. [공통점과 차이점 — 중국 LLM vs. 서구 LLM](#8-공통점과-차이점--중국-llm-vs-서구-llm)
9. [벤치마크 포화 문제와 새로운 흐름](#9-벤치마크-포화-문제와-새로운-흐름)
10. [실용적 시사점 — 새로운 PLM을 만든다면](#10-실용적-시사점--새로운-plm을-만든다면)
11. [한국어 PLM 평가 특수 고려사항](#11-한국어-plm-평가-특수-고려사항)
12. [평가 도구 실습 스니펫](#12-평가-도구-실습-스니펫)

---

## 1. 평가 방법론의 시대적 진화

PLM 평가의 역사는 대략 네 단계로 나눌 수 있어요.

### Phase 1: Perplexity + Fine-tune 시대 (2017~2019)

GPT-1, BERT, ELMo가 활약하던 시기예요. 이때 평가의 핵심은 두 가지였죠.

- **Perplexity**: 사전학습 품질의 직접 척도. 낮을수록 좋아요.
- **Fine-tune 후 downstream 성능**: 사전학습 모델을 각 task마다 따로 fine-tuning해서 GLUE, SQuAD, NLI 같은 벤치마크에서 점수를 재는 방식.

이 시절에는 "base model 자체의 능력"보다 "fine-tuning 기반으로 얼마나 빨리 적응하는가"가 핵심이었어요. 전이학습(transfer learning)이 핫했던 이유도 여기에 있죠.

### Phase 2: Zero/Few-shot + In-Context Learning 시대 (2020~2022)

GPT-3가 나오면서 패러다임이 바뀌어요.

> "We test GPT-3 in the few-shot setting by giving it k examples of the desired behavior... with k typically ranging from 10 to 100."
> — Brown et al., 2020, "Language Models are Few-Shot Learners"

Fine-tuning 없이, 프롬프트에 예제 몇 개를 넣어주는 것만으로 base model이 다양한 task를 수행하게 됐거든요. 평가 방식도 그에 맞게 **0-shot / 1-shot / few-shot 비교**가 표준이 됐어요. 이때부터 base model과 fine-tuned 모델 평가가 다른 궤도를 달리기 시작해요.

### Phase 3: 통합 벤치마크 표준화 시대 (2022~2023)

MMLU(Massive Multitask Language Understanding), HellaSwag, ARC, BBH(BIG-Bench Hard), WinoGrande 등이 **사실상 표준 벤치마크 세트**로 자리잡아요. 이 시기부터 각 논문의 결과 테이블이 거의 비슷한 컬럼을 갖게 되죠.

중국 팀들은 여기에 **C-Eval, CMMLU** 같은 중국어 전용 벤치마크를 추가하고, 코드/수학 쪽은 **HumanEval, MBPP, GSM8K, MATH**가 필수로 들어왔어요.

### Phase 4: 오염(contamination) 문제 + 역동적 벤치마크 (2024~)

모델이 너무 좋아지면서 MMLU 같은 벤치마크가 **포화(saturation)**되기 시작했어요. 더 심각한 건 **데이터 오염(data contamination)** 문제 — 훈련 데이터에 테스트 셋이 포함되어 있을 가능성이죠. 이에 대응해:

- [LiveBench](https://livebench.ai/) — 매달 새 문제를 추가해 오염을 원천 차단
- [Open LLM Leaderboard v2](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard) — 더 어려운 벤치마크(GPQA, MMLU-Pro, MuSR, BBH, IFEval 등)로 업그레이드
- MMLU-Pro, MMLU-Redux — MMLU의 오류를 수정하고 난이도를 높인 변형

---

## 2. GPT 시리즈의 평가 방법

### 2-1. GPT-1 (Radford et al., 2018)

[GPT-1 논문](https://openai.com/research/language-unsupervised)은 지금 보면 꽤 단순한 평가 구조를 가지고 있어요. 핵심 아이디어는 **"generative pre-training + task-specific fine-tuning"** 이고, 평가도 그 구조를 따라가요.

**평가 방식:**
- 사전학습 후 각 downstream task별로 **supervised fine-tuning** 진행
- 평가 대상: 자연어 추론(NLI), QA, 문장 유사도, 분류

**사용 벤치마크:**
| 카테고리 | 벤치마크 | 비고 |
|----------|---------|------|
| NLI (자연어 추론) | SNLI, MultiNLI, SciTail, RTE | 당시 GLUE 서브셋 |
| QA | RACE, Story Cloze | 독해·상식 |
| 문장 유사도 | MRPC, QQP, STS-B | |
| 분류 | CoLA, SST-2, GLUE overall | |

> "Our model achieves absolute improvements of 8.9% on commonsense reasoning (Stories Cloze Test), 5.7% on question answering (RACE), and 1.5% on textual entailment (MultiNLI) and 5.5% on the GLUE multi-task benchmark compared to the previous best results in each category."
> — Radford et al., 2018

중요한 건, 이때 **base model 자체를 직접 평가하는 표**는 없어요. 모든 평가가 fine-tune 후 성능이에요. 이 점이 이후 GPT-3 접근 방식과 근본적으로 달라지는 부분이에요.

**평가 지표:** Accuracy, Matthews Correlation Coefficient(MCC), F1

### 2-2. GPT-2 (Radford et al., 2019)

GPT-2는 [Language Models are Unsupervised Multitask Learners](https://openai.com/research/better-language-models)에서 혁신적인 주장을 해요: **"fine-tuning 없이도 zero-shot으로 여러 task를 풀 수 있다"**.

**핵심 평가 철학:**
> "Language models can perform down-stream tasks in a zero-shot setting — without any parameter or architecture modification."
> — Radford et al., 2019

**사용 벤치마크 (모두 zero-shot):**
| 벤치마크 | 메트릭 | GPT-2(1.5B) 결과 |
|----------|--------|----------------|
| Penn Treebank | Perplexity | 35.76 (SOTA) |
| WikiText-103 | Perplexity | 17.48 (당시 SOTA) |
| WikiText-2 | Perplexity | 18.34 |
| LAMBADA | Accuracy / Perplexity | 52.66% / 8.63 |
| CBT-CN (Common Nouns) | Accuracy | 93.3% (SOTA) |
| CBT-NE (Named Entities) | Accuracy | 89.1% (SOTA) |
| Children's Book Test | Accuracy | 82.3% |
| CoQA | F1 | 55.0 |

특히 **LAMBADA** 결과가 드라마틱해요 — 정확도가 19%에서 52.66%로 뛰었거든요. Perplexity도 99.8에서 8.63으로 줄었고요. 이게 당시 "GPT-2가 뭔가 새로운 것"임을 보여준 증거였죠.

**평가 방식의 특징:**
- 순수 zero-shot (fine-tuning, few-shot 예제 모두 없음)
- 언어 모델링 태스크: Perplexity (bits-per-character 기준)
- 생성 기반 task: greedy decoding 사용

### 2-3. GPT-3 (Brown et al., 2020)

[GPT-3 논문](https://arxiv.org/abs/2005.14165)은 PLM 평가 역사에서 가장 중요한 전환점 중 하나예요. 175B 파라미터 모델이 **zero-shot / 1-shot / few-shot** 세 가지 설정 모두에서 평가되는 방식이 이때 표준이 됐거든요.

> "We evaluate GPT-3 on over two dozen NLP datasets, as well as several novel tasks designed to test rapid adaptation to tasks unlikely to be in the training set."
> — Brown et al., 2020

**평가 구조의 3가지 축:**

1. **Zero-shot**: 태스크 설명만 제공, 예제 없음
2. **One-shot**: 태스크 설명 + 예제 1개
3. **Few-shot**: 태스크 설명 + 예제 10~100개 (context window 허용 범위 내)

**주요 벤치마크 카테고리:**

| 카테고리 | 벤치마크 | Few-shot 설정 |
|----------|---------|--------------|
| 언어 모델링 | Penn Treebank, WikiText, LAMBADA | Zero-shot |
| 상식 추론 | HellaSwag, WinoGrande, PIQA, WinoGrad | Zero/Few-shot |
| QA | TriviaQA, NaturalQuestions, WebQA | 0~64 shot |
| 독해 | CoQA, QuAC, DROP, SQuAD v2 | Few-shot |
| 번역 | WMT'14 (En-Fr, En-De, En-Ro) | Few-shot |
| 산술 추론 | 2~5자리 덧셈·뺄셈 자체 제작 | Few-shot |
| 뉴스 생성 판별 | 자체 제작 (TDNews) | Zero-shot |

**주목할 만한 결과:**

> "GPT-3 achieves 64.3% accuracy on TriviaQA in the zero-shot setting, 68.0% in the one-shot setting, and 71.2% in the few-shot setting."
> — Brown et al., 2020

few-shot 예제가 많아질수록 성능이 올라가는 패턴 — 이게 in-context learning(ICL)의 핵심 증거였어요.

**디코딩 방식:** Greedy decoding (classification tasks), Beam search 없이 직접 생성

**중요한 평가 한계점 (논문 스스로 인정):**
- 훈련 데이터에 테스트 셋이 포함됐을 가능성 (data contamination)
- 추론 능력 체계적 평가 불충분
- Common sense reasoning에서 여전히 한계

---

## 3. InstructGPT — Base vs. RLHF 모델 평가의 분리

[InstructGPT (Ouyang et al., 2022)](https://arxiv.org/abs/2203.02155)는 PLM 평가 역사에서 특별한 위치를 차지해요. 이 논문이 처음으로 **"base model 평가"와 "instruction-following 모델 평가"를 명시적으로 분리**했거든요.

### 3-1. 평가 구조

InstructGPT의 평가는 크게 세 층으로 나뉘어요:

**Layer 1: Human preference evaluation (주요 평가)**
- 라벨러(labeler)들이 두 모델의 출력을 보고 어느 것이 더 좋은지 선택
- 1,550개의 held-out 프롬프트 사용
- 평가 차원: **helpfulness, harmlessness, honesty**

> "Labelers prefer InstructGPT outputs over outputs from GPT-3 on 85 ± 3% of cases."
> — Ouyang et al., 2022

놀라운 건, **1.3B InstructGPT가 175B GPT-3보다 선호됐다**는 점이에요. 파라미터 수가 100배 차이 나는데도요.

**Layer 2: NLP 벤치마크 (regression 체크)**
RLHF로 instruction-following을 학습하면 기존 NLP 성능이 떨어지는 **"alignment tax"** 문제가 있을 수 있어요. 이를 체크하기 위해:
- **SQuADv2** (독해 QA)
- **TriviaQA** (오픈 도메인 QA)
- **HellaSwag** (상식 추론)
- **BoolQ** (예/아니오 QA)
- **WinoGrande** (성별 편향 없는 상식)
- **RTE** (자연어 추론)
- **DROP** (수치 추론)

결론: PPO+SFT 혼합 방식으로 NLP 성능 regression을 최소화함.

**Layer 3: 안전성/유해성 평가**
- **TruthfulQA**: 모델이 사실과 다른 내용을 얼마나 생성하는지 (truthfulness)
- **RealToxicityPrompts**: 독성 콘텐츠 생성 비율
- 결과: InstructGPT가 GPT-3 대비 **약 25% 낮은 독성 출력** 기록

### 3-2. Base Model 평가와의 구분

InstructGPT 논문의 핵심 기여 중 하나는 이 질문에 답한 거예요: **"RLHF가 기존 능력을 망가뜨리지 않으면서 instruction-following만 개선할 수 있는가?"**

이를 위해 논문은 SFT, RM, PPO 각 단계의 모델을 따로 평가하고, GPT-3 base와 비교해요. 이 "비교 구조"가 이후 Qwen, DeepSeek가 base model 따로, chat model 따로 테이블을 만드는 관행의 원형이 됐다고 볼 수 있어요.

---

## 4. Qwen 시리즈의 평가 전략

Alibaba의 Qwen 시리즈는 [원본 Qwen Technical Report (Bai et al., 2023)](https://arxiv.org/abs/2309.16609), [Qwen2](https://arxiv.org/abs/2407.10671), [Qwen2.5](https://arxiv.org/pdf/2412.15115)까지 일관된 평가 철학을 발전시켜왔어요.

### 4-1. Qwen (2023) — 이중 언어 평가의 시작

원본 Qwen은 영어 벤치마크와 중국어 벤치마크를 동등하게 다뤄요.

**영어 벤치마크:**
- MMLU (5-shot), C-Eval, GSM8K, MATH, HumanEval, MBPP, BBH 등

**중국어 벤치마크:**
- **C-Eval**: 중국어 시험 기반 MMLU 유사 벤치마크 (52개 과목)
- **CMMLU**: Chinese Massive Multitask Language Understanding

> "Qwen models outperform baseline models of similar model sizes on benchmark datasets including MMLU, C-Eval, GSM8K, MATH, HumanEval, MBPP, BBH."
> — Bai et al., 2023

### 4-2. Qwen2 (2024) — 다국어 평가 확장

[Qwen2 Technical Report](https://arxiv.org/html/2407.10671v1)에서는 평가가 크게 네 카테고리로 체계화돼요.

**Base model 평가 카테고리:**

| 카테고리 | 벤치마크 | Shot 설정 |
|----------|---------|---------|
| 언어 이해·지식 | MMLU | 5-shot |
| | MMLU-Pro | 5-shot |
| | GPQA | 5-shot |
| | Theorem QA | 5-shot |
| 추론 | BBH | 3-shot |
| | HellaSwag | 10-shot |
| | WinoGrande | 5-shot |
| | ARC-C | 25-shot |
| | TruthfulQA | 0-shot |
| 코딩 | HumanEval, MBPP, EvalPlus | 0-shot |
| | MultiPL-E (다중 언어) | 0-shot |
| 수학 | GSM8K | 5-shot |
| | MATH | 4-shot |

**다국어 평가 (4개 하위 카테고리):**
- Exams: M3Exam, IndoMMLU, ruMMLU, translated MMLU
- Understanding: BELEBELE, XCOPA, XWinograd, XStoryCloze, PAWS-X
- Mathematics: MGSM (8-shot CoT)
- Translation: Flores-101 (5-shot)

**중국어 특화:**
- C-Eval (5-shot), CMMLU (5-shot)

### 4-3. Qwen2.5 (2024) — 코딩·수학 강화

[Qwen2.5 Technical Report](https://arxiv.org/pdf/2412.15115)에서는 코딩과 수학 평가가 더욱 정교해졌어요.

**기본 평가 세트 (base model):**
- General: MMLU (5-shot), MMLU-Pro (5-shot), MMLU-redux (5-shot), BBH (3-shot), ARC-C (25-shot), TruthfulQA (0-shot), WinoGrande (5-shot), HellaSwag (10-shot)
- Math & Science: GPQA (5-shot), TheoremQA (5-shot), GSM8K (4-shot), MATH (4-shot)
- Code: HumanEval (0-shot), HumanEval+ (0-shot), MBPP (0-shot), MBPP+ (0-shot), MultiPL-E (0-shot, 8개 언어)

**성능 향상 (Qwen2 → Qwen2.5, 72B 기준):**
- MMLU: 84.2 → 86.1
- MMLU-Pro: 베이스 대비 향상
- GSM8K: 상당한 향상
- HumanEval: 코딩 특화 훈련으로 개선

### 4-4. Qwen 평가의 특징적 관행

Qwen 시리즈에서 주목할 만한 평가 관행이 있어요:

1. **엄격한 Base vs. Chat 분리**: 각 technical report에서 base model 테이블과 instruction-tuned 모델 테이블을 별도로 제시
2. **오염 검사 명시**: Qwen2.5 report에서 훈련 데이터 오염 여부 확인 방법론 언급
3. **내부 평가 프레임워크 + 공개 툴 병용**: OpenCompass를 활용한 재현 가능성 확보

---

## 5. DeepSeek의 Base Model 평가 심층 분석

DeepSeek는 PLM base model 평가에서 가장 체계적인 접근을 취하는 팀 중 하나예요. 특히 [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437)는 base model 평가의 교과서라 불릴 만해요.

### 5-1. DeepSeek LLM (2024) — 기초 틀 수립

[DeepSeek LLM (arXiv:2401.02954)](https://arxiv.org/abs/2401.02954)에서는 base model 평가 프로토콜이 다음과 같이 정립돼요.

**3가지 평가 방식의 공존:**

1. **Perplexity 기반**: 객관식 문제에서 각 선택지의 perplexity를 계산해 가장 낮은 것 선택
2. **Generation 기반**: 수학·코드·추론에서 free-form generation 후 greedy decoding
3. **Language modeling**: Bits-per-byte(BPB) 계산으로 훈련 품질 직접 측정

**Shot 설정:**
- 0-shot: HellaSwag, PIQA, ARC, OpenBookQA
- 3-shot: BBH, MBPP
- 5-shot: TriviaQA, NaturalQuestions, MMLU, C-Eval
- 8-shot: GSM8K

### 5-2. DeepSeek-V3 (2024) — 가장 완결된 Base Model 평가

[DeepSeek-V3 Technical Report](https://arxiv.org/html/2412.19437v1)는 671B MoE 모델의 base 평가를 매우 상세하게 제시해요.

**평가 메트릭:**
- EM (Exact Match): QA 태스크
- F1 score: DROP 등
- Pass@1: 코드 태스크 (greedy decoding)
- BPB (Bits-Per-Byte): 언어 모델링 품질

**전체 벤치마크 결과 (DeepSeek-V3 Base):**

| 벤치마크 | Shot | 점수 |
|---------|------|------|
| **영어 — 지식/추론** | | |
| MMLU | 5-shot | 87.1% |
| MMLU-Redux | 5-shot | 86.2% |
| MMLU-Pro | 5-shot | 64.4% |
| BBH | 3-shot | 87.5% |
| DROP | 3-shot | 89.0% |
| ARC-Easy | 25-shot | 98.9% |
| ARC-Challenge | 25-shot | 95.3% |
| HellaSwag | 10-shot | 88.9% |
| PIQA | 0-shot | 84.7% |
| WinoGrande | 0-shot | 84.9% |
| TriviaQA | 3-shot | 82.9% |
| NaturalQuestions | 3-shot | 40.0% |
| AGIEval | 0-shot | 79.6% |
| **영어 — 코드** | | |
| HumanEval | 0-shot | 65.2% |
| MBPP | 0-shot | 75.4% |
| LiveCodeBench | 0-shot | 19.4% |
| **영어 — 수학** | | |
| GSM8K | 8-shot | 89.3% |
| MATH | 4-shot | 61.6% |
| MGSM | 8-shot | 79.8% |
| CMath | 0-shot | 90.7% |
| **중국어** | | |
| C-Eval | 5-shot | 90.1% |
| CMMLU | 5-shot | 88.8% |
| CLUEWSC | 5-shot | 82.7% |
| **다국어** | | |
| MMMLU (non-English) | 5-shot | 79.4% |
| Pile-test | 0-shot | 0.548 BPB |

**비교 대상 모델:** LLaMA-3.1-405B, Qwen2.5-72B, Mistral-Large-2-123B

### 5-3. DeepSeek-R1 — Base Model이 출발점

[DeepSeek-R1 (2025)](https://arxiv.org/abs/2501.12948)은 특이하게도 **DeepSeek-V3-Base에서 직접 RL을 적용**하는 방식을 택해요.

> "We directly apply RL to the base model without relying on SFT as a preliminary step."
> — DeepSeek-AI, 2025

이 때문에 R1 논문에서 base model 평가는 "R1-Zero의 출발점"으로서 의미를 갖고, 평가 벤치마크는 추론 중심이에요:

- **AIME 2024**: 79.8% Pass@1 (수학 경시대회)
- **MATH-500**: 97.3% (수학 종합)
- **GPQA Diamond**: 71.5% (대학원 수준 과학)
- **LiveCodeBench**: 65.9% (오염 방지 코딩)
- **Codeforces**: 2029 Elo 레이팅

평가 설정: `max_generation = 32,768`, sampling temperature = 0.6, top-p = 0.95

### 5-4. DeepSeek의 차별화 포인트

DeepSeek가 다른 팀들과 다른 점은:

1. **BPB(Bits-Per-Byte) 명시적 보고**: Pile-test 언어 모델링 품질을 숫자로 공개 — 사전학습 품질의 직접 지표
2. **내부 평가 프레임워크 (HAI-LLM)**: 재현 가능한 환경 + 코드 공개
3. **MoE base 평가 특수성**: 활성화 파라미터(37B)와 전체 파라미터(671B) 명시

---

## 6. Gemma 시리즈의 평가 방법론

Google DeepMind의 Gemma 시리즈는 "오픈 모델이지만 구글 수준의 엄격함"을 보여줘요.

### 6-1. Gemma (2024) — 표준 벤치마크 세트

[Gemma Technical Report](https://arxiv.org/abs/2403.08295)는 2B, 7B 모델에 대해 체계적인 평가를 제시해요.

**Pre-trained base model 벤치마크:**
- HellaSwag, BoolQ, PIQA, SIQA, TriviaQA, Natural Questions, ARC-C/E, WinoGrande (5-shot)
- MMLU, MATH, GSM8K (5-shot)
- HumanEval, MBPP (0-shot)
- BBH (3-shot)

**평가의 특징:** Knowledge distillation(2B, 9B)이 적용된 모델과 그렇지 않은 모델의 비교

### 6-2. Gemma 2 (2024) — 경량화 모델의 놀라운 성능

[Gemma 2 Technical Report](https://arxiv.org/abs/2408.00118)는 2B~27B 범위에서 "크기 대비 성능"을 보여줘요.

주요 특징: 로컬-글로벌 어텐션 교차 구조, 그룹 쿼리 어텐션, knowledge distillation 적극 활용.

### 6-3. Gemma 3 (2025) — 멀티모달 + 128K 컨텍스트

[Gemma 3 Technical Report (2025)](https://arxiv.org/abs/2503.19786)는 텍스트와 비전을 모두 다루고, 컨텍스트 창이 128K로 늘어났어요.

**Pre-trained model 평가 (few-shot):**
| 카테고리 | 벤치마크 | Shot |
|----------|---------|------|
| 일반 | HellaSwag, BoolQ, PIQA, SIQA, TriviaQA, NQ | 5-shot |
| | ARC-C/E, WinoGrande, BBH, DROP | 5-shot |
| STEM/코드 | MMLU, MMLU-Pro, AGIEval, MATH, GSM8K | 3~5-shot |
| | GPQA Diamond, MBPP, HumanEval | 5-shot |
| 멀티모달 | DocVQA, TextVQA, ChartQA, VQAv2, MMMU | 4-shot |
| 다국어 | MGSM, Global-MMLU, WMT24++, FLoRes, XQuAD | 5~8-shot |
| 장문 맥락 | RULER (32K, 128K), MRCR | — |

**Instruction-tuned model (0-shot):** 대부분의 벤치마크를 0-shot으로 재평가 — base와 IT 모델 평가 방식의 차이를 명확히 보여줘요.

**Human evaluation:** LMSYS Chatbot Arena Elo rating — 27B IT 모델이 1338점으로 상위 10위권 진입.

> "We use several standard benchmarks as probes during pre-training to ensure models capture general abilities including science, code, factuality, multilinguality, reasoning, and vision."
> — Gemma Team, Google DeepMind, 2025

---

## 7. 주요 벤치마크 매트릭스 — 모델별 사용 현황

아래 표는 각 모델/논문에서 어떤 벤치마크를 어떤 shot 설정으로 사용했는지를 정리한 거예요. "O"는 사용, "—"는 미사용 또는 미보고.

### 7-1. 지식·추론 벤치마크

| 벤치마크 | GPT-1 | GPT-2 | GPT-3 | InstructGPT | Qwen | Qwen2 | Qwen2.5 | DeepSeek-V3 | Gemma 3 |
|---------|-------|-------|-------|------------|------|-------|---------|------------|---------|
| MMLU | — | — | — | O | O(5) | O(5) | O(5) | O(5) | O(5) |
| MMLU-Pro | — | — | — | — | — | O(5) | O(5) | O(5) | O(5) |
| BBH | — | — | — | — | O(3) | O(3) | O(3) | O(3) | O(3) |
| HellaSwag | — | — | O(0) | O | O(10) | O(10) | O(10) | O(10) | O(5) |
| WinoGrande | — | — | O | O | O(5) | O(5) | O(5) | O(0) | O(5) |
| ARC-C/E | — | — | O | — | O(25) | O(25) | O(25) | O(25) | O(5) |
| PIQA | — | — | O | — | O | — | — | O(0) | O(5) |
| TriviaQA | — | — | O(64) | O | O(5) | O(5) | — | O(3) | O(5) |
| NaturalQ | — | — | O | — | — | — | — | O(3) | O(5) |
| GPQA | — | — | — | — | — | O(5) | O(5) | — | O(5) |
| TruthfulQA | — | — | — | O | — | O(0) | O(0) | — | — |
| AGIEval | — | — | — | — | O | — | — | O(0) | O(5) |

숫자 = shot 수, O = 사용하지만 shot 수 불명확, — = 미사용

### 7-2. 수학·코딩 벤치마크

| 벤치마크 | GPT-1 | GPT-2 | GPT-3 | InstructGPT | Qwen | Qwen2 | Qwen2.5 | DeepSeek-V3 | Gemma 3 |
|---------|-------|-------|-------|------------|------|-------|---------|------------|---------|
| GSM8K | — | — | O | — | O | O(5) | O(4) | O(8) | O(5) |
| MATH | — | — | — | — | O | O(4) | O(4) | O(4) | O(5) |
| MGSM | — | — | — | — | — | O(8) | — | O(8) | O(8) |
| HumanEval | — | — | — | — | O | O(0) | O(0) | O(0) | O(5) |
| MBPP | — | — | — | — | O | O(0) | O(0) | O(0) | O(5) |
| AIME 2024 | — | — | — | — | — | — | — | O | — |
| LiveCodeBench | — | — | — | — | — | — | — | O(0) | — |

### 7-3. 중국어·다국어 벤치마크

| 벤치마크 | GPT-3 | InstructGPT | Qwen | Qwen2 | Qwen2.5 | DeepSeek-V3 | Gemma 3 |
|---------|-------|------------|------|-------|---------|------------|---------|
| C-Eval | — | — | O(5) | O(5) | — | O(5) | — |
| CMMLU | — | — | O | O(5) | — | O(5) | — |
| MGSM | O | — | — | O(8) | — | O(8) | O(8) |
| MMMLU | — | — | — | O | — | O(5) | O(5) |
| Global-MMLU | — | — | — | — | — | — | O(5) |
| BELEBELE | — | — | — | O | O | — | — |
| WMT | O | — | — | — | — | — | O |
| Flores-101 | — | — | — | O(5) | — | — | O(8) |

---

## 8. 공통점과 차이점 — 중국 LLM vs. 서구 LLM

### 8-1. 공통 평가 관행 (거의 모든 최신 LLM)

2022년 이후 major PLM paper들이 공유하는 평가 관행을 정리하면:

- **MMLU (5-shot)**: 지식의 breadth를 측정하는 필수 벤치마크
- **BBH (3-shot)**: 복잡한 추론 능력 측정
- **GSM8K**: 수학 추론 (초등~중학 수준)
- **HumanEval / MBPP**: 코딩 능력
- **HellaSwag**: 상식 추론
- **Base vs. IT 모델 분리 보고**: InstructGPT 이후의 표준

### 8-2. 중국 LLM만의 추가 평가

Qwen, DeepSeek처럼 중국 팀이 서구 팀과 다른 점:

| 특징 | 중국 LLM (Qwen, DeepSeek) | 서구 LLM (GPT, Gemma) |
|------|--------------------------|---------------------|
| 중국어 벤치마크 | C-Eval, CMMLU 필수 포함 | 대부분 미포함 |
| 언어 모델링 | BPB (Pile-test) 직접 보고 | 일부만 보고 |
| 다국어 범위 | 50개 언어 이상 | 다양하지만 영어 중심 |
| 오염 검사 | 상세히 기술 | 일부만 기술 |
| 내부 평가 프레임워크 | HAI-LLM (DeepSeek), OpenCompass | 다양 |

### 8-3. 안전성 평가

안전성/유해성 평가는 논문마다 접근이 달라요:

- **InstructGPT**: TruthfulQA, RealToxicityPrompts, BBQ (편향 측정) — 가장 체계적
- **Gemma**: 사전학습 데이터에서 안전하지 않은 컨텐츠 필터링 기술 + 평가
- **Qwen**: Qwen-Chat 기준 safety 평가 포함, base model은 별도 언급 적음
- **DeepSeek**: 2,400개 안전성 테스트 케이스 (차별, 법적 권리, 유해 콘텐츠)

### 8-4. Human Evaluation

- **InstructGPT**: 전체 평가의 핵심 — labeler preference (85% 선호율), API 사용자 실제 프롬프트 기반
- **Gemma 3**: LMSYS Chatbot Arena Elo rating (blind side-by-side)
- **GPT-3**: 뉴스 기사 진위 판별 human evaluation (부수적)
- **Qwen/DeepSeek**: Chat 모델 평가에서 arena 기반 인간 평가 활용, base model은 자동 벤치마크 중심

---

## 9. 벤치마크 포화 문제와 새로운 흐름

### 9-1. 포화되고 있는 벤치마크들

솔직히 말하면, 지금 많은 벤치마크가 "측정 도구"로서의 수명을 다해가고 있어요.

| 벤치마크 | 포화 수준 | 대표 점수 (2025 기준) |
|---------|---------|------------------|
| LAMBADA | 거의 포화 | 90%+ 일반적 |
| ARC-Easy | 포화 | 97~99% |
| HellaSwag | 거의 포화 | 85~92% |
| WinoGrande | 상당 | 80~88% |
| MMLU | 접근 중 | GPT-4급 88~90% |
| GSM8K | 포화 진행 | 90%+ |

MMLU는 오염 문제도 심각해요:

> "MMLU performance is highly sensitive to the prompt and scoring function, causing significant leaderboard reordering. GPT-4o obtained only 1% improvement on MMLU to reach 87.4%, prompting the community to re-examine MMLU's utility."
> — LLM Benchmarks 2026, LXT

### 9-2. 새롭게 부상하는 벤치마크

**어려운 추론:**
- **GPQA Diamond**: 대학원 수준 물리·화학·생물 문제. GPT-4급도 50~60%대
- **MMLU-Pro**: 10지선다 + 더 어려운 문제
- **MATH-500**: 경시대회 수준 수학

**오염 방지:**
- **[LiveBench](https://arxiv.org/abs/2406.19314)**: 매달 새 문제 추가. arXiv 논문, 뉴스, IMDb 시놉시스에서 문제 생성

> "LiveBench is designed to limit potential contamination by releasing new questions monthly, as well as having questions based on recently-released datasets, arXiv papers, news articles, and IMDb movie synopses."
> — White et al., 2024, LiveBench

- **LiveCodeBench**: 오염 없는 코딩 평가 (Codeforces/LeetCode 최신 문제)

**코딩:**
- **SWE-bench**: 실제 GitHub 이슈 해결 능력 측정
- **Aider LLM Leaderboard**: 실제 코드 편집 성능

**오픈 리더보드:**
- [Hugging Face Open LLM Leaderboard v2](https://huggingface.co/spaces/open-llm-leaderboard/open_llm_leaderboard): IFEval, BBH, MATH Hard, GPQA, MuSR, MMLU-Pro 6개 벤치마크로 개편 (2024)

### 9-3. Contamination Check 방법들

최신 논문들은 오염 여부를 어떻게 체크할까요?

1. **N-gram overlap**: 훈련 데이터와 테스트 셋 간 n-gram 유사도 측정
2. **Min-k% Prob**: 모델이 테스트 문장에 비정상적으로 높은 확률을 부여하는지 체크
3. **ROUGE-L threshold**: 일정 임계값 이상 유사도 시 오염 의심
4. **Held-out 테스트**: 훈련 이전에 봉인된 평가 셋 사용

DeepSeek-V3는 이를 명시적으로 논문에 기술하고 있어요.

---

## 10. 실용적 시사점 — 새로운 PLM을 만든다면

2026년 기준으로 새 PLM을 훈련·평가한다면, 아래 프레임을 추천해요.

### 10-1. 필수 벤치마크 세트 (최소 기준)

**Tier 1 — 반드시 포함:**
- MMLU / MMLU-Pro (5-shot): 지식 breadth
- BBH (3-shot): 복잡 추론
- MATH (4-shot) + GSM8K (8-shot): 수학 능력
- HumanEval + MBPP (0-shot): 코딩 능력
- HellaSwag (10-shot): 상식 추론

**Tier 2 — 강력 권장:**
- GPQA Diamond (5-shot): 어려운 과학 추론
- LiveCodeBench: 오염 없는 코딩
- AGIEval: 실제 인간 시험 기반

**Tier 3 — 특화 용도:**
- C-Eval / CMMLU: 중국어 능력 평가 시
- TruthfulQA: 환각(hallucination) 측정
- MGSM: 다국어 수학 추론

### 10-2. 평가 프로토콜 체크리스트

```
[ ] Base model과 Instruction-tuned 모델 결과 분리 보고
[ ] Shot 설정 명시 (0/1/3/5/8/10/25-shot)
[ ] 디코딩 방식 명시 (greedy vs sampling, temperature)
[ ] 오염 검사 수행 및 방법 기술
[ ] BPB 또는 perplexity 보고 (사전학습 품질 직접 지표)
[ ] 비교 모델 명시 (동일 규모의 open/closed 모델)
[ ] 내부 vs. 공개 평가 프레임워크 명시
```

### 10-3. 점점 덜 쓸모 있어지는 벤치마크

새 PLM 개발 시 이것들은 이제 주요 지표로 쓰기 어려워요:

- **ARC-Easy**: 95%+ 가 당연 → 차별화 불가
- **LAMBADA**: 대부분 90% 이상
- **WinoGrad (Small)**: 포화
- **BoolQ (standalone)**: 단독으로는 정보량 적음

대신 **GPQA, MMLU-Pro, LiveBench, AIME** 등이 프런티어 모델 평가에 적합해요.

---

## 11. 한국어 PLM 평가 특수 고려사항

한국어 PLM을 만들거나 평가한다면 추가로 고려할 사항이 있어요.

### 11-1. 주요 한국어 벤치마크

**[KMMLU](https://arxiv.org/abs/2402.11548)** (Korean MMLU)
- 35,030개 전문가 수준 4지선다 문제, 45개 과목
- 공무원 시험, 국가기술자격시험, 수능에서 출제
- 특징: 번역이 아닌 **원본 한국어 시험 문제**
- GPT-4 기준 약 60% (인간 전문가 최소 80%)
- 2024년 기준 Hugging Face에서 300만+ 다운로드

**[KoBEST](https://huggingface.co/datasets/skt/kobest_v1)** (Korean Balanced Evaluation of Significant Tasks)
- 5개 카테고리: BoolQ-Ko, COPA-Ko, WiC-Ko, HellaSwag-Ko, SentiNeg
- 최초의 한국어 추론 능력 체계적 평가 벤치마크

**[HAE-RAE Bench](https://arxiv.org/abs/2309.02706)**
- 한국 문화·역사 지식 평가 특화
- 한국 고유 지식이 없으면 답하기 어려운 문제들

**[HRET](https://arxiv.org/abs/2503.22968)** (Haerae Evaluation Toolkit)
- 오픈소스 자기진화 한국어 LLM 평가 프레임워크
- HAE-RAE Bench, KMMLU, KUDGE, HRM8K 통합

**KMMLU-Pro (2025)**
- KMMLU-Redux (오류 제거 버전)의 발전형
- 국가전문직 시험 기반 → 더 어려운 전문 지식 요구

### 11-2. 한국어 평가 시 주의사항

1. **번역 벤치마크의 한계**: 영어 벤치마크를 한국어로 번역한 것은 문화적 맥락을 놓쳐요. KMMLU처럼 원본 한국어 자료 사용 권장
2. **형태소 분석기 의존성**: 토크나이저 방식에 따라 perplexity 값이 다르게 나올 수 있어요
3. **표준어 vs. 구어체**: 한국어는 정서법과 구어체 차이가 크므로, 평가 데이터의 언어 레지스터 확인 필요
4. **동형이의어 문제**: 한국어 특유의 중의성이 있어 WiC(Word in Context) 타입 평가 시 주의
5. **다국어 모델 vs. 한국어 특화 모델**: KMMLU 결과에 따르면, 대형 다국어 모델이 소형 한국어 특화 모델을 능가하는 경우가 많아요 → 규모가 충분하면 한국어 특화보다 다국어 방향이 유리할 수 있음

---

## 12. 평가 도구 실습 스니펫

마지막으로, 실제 LLM 평가를 돌려볼 때 쓸 수 있는 도구 예시예요.

### 12-1. lm-evaluation-harness (EleutherAI)

[lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness)는 Open LLM Leaderboard의 백엔드이자 수백 개 벤치마크를 지원하는 표준 평가 프레임워크예요.

```bash
# 설치
pip install lm-eval

# 기본 평가 (MMLU 5-shot, HellaSwag 10-shot, ARC-Challenge 25-shot)
lm_eval --model hf \
    --model_args pretrained=meta-llama/Llama-3.1-8B \
    --tasks mmlu,hellaswag,arc_challenge \
    --num_fewshot 5 \
    --device cuda:0 \
    --batch_size 8

# GSM8K (8-shot) + HumanEval (0-shot)
lm_eval --model hf \
    --model_args pretrained=your-base-model \
    --tasks gsm8k,humaneval \
    --num_fewshot 8,0 \
    --device cuda:0

# vLLM 백엔드로 빠른 평가
lm_eval --model vllm \
    --model_args pretrained=your-model,tensor_parallel_size=4 \
    --tasks mmlu_pro,bbh,gpqa_diamond \
    --num_fewshot 5,3,5 \
    --device cuda
```

### 12-2. OpenCompass

[OpenCompass](https://github.com/open-compass/opencompass)는 중국 LLM 팀들이 즐겨 쓰는 프레임워크로, C-Eval, CMMLU 등 중국어 벤치마크 지원이 강점이에요.

```python
# configs/eval_base_model.py 예시
from mmengine.config import read_base

with read_base():
    from opencompass.configs.datasets.mmlu.mmlu_gen_a484b3 import mmlu_datasets
    from opencompass.configs.datasets.ceval.ceval_gen_5f30c7 import ceval_datasets
    from opencompass.configs.datasets.gsm8k.gsm8k_gen_1d7fe4 import gsm8k_datasets
    from opencompass.configs.datasets.humaneval.humaneval_gen_8e312c import humaneval_datasets

datasets = [
    *mmlu_datasets,     # 5-shot
    *ceval_datasets,    # 5-shot
    *gsm8k_datasets,    # 8-shot
    *humaneval_datasets # 0-shot
]

models = [
    dict(
        type='HuggingFaceCausalLM',
        abbr='your-model-7b',
        path='path/to/your-model',
        max_out_len=1024,
        batch_size=8,
        run_cfg=dict(num_gpus=1)
    )
]
```

### 12-3. 빠른 contamination 체크

```python
import re
from nltk.tokenize import word_tokenize

def check_ngram_overlap(train_text: str, test_question: str, n: int = 8) -> float:
    """
    훈련 데이터와 테스트 문항 간 n-gram 중복률을 계산합니다.
    0.5 이상이면 오염 의심.
    """
    def get_ngrams(text, n):
        tokens = word_tokenize(text.lower())
        return set(zip(*[tokens[i:] for i in range(n)]))
    
    train_ngrams = get_ngrams(train_text, n)
    test_ngrams = get_ngrams(test_question, n)
    
    if not test_ngrams:
        return 0.0
    
    overlap = len(train_ngrams & test_ngrams)
    return overlap / len(test_ngrams)

# 사용 예시
score = check_ngram_overlap(
    train_text="The mitochondria is the powerhouse of the cell...",
    test_question="What is the function of mitochondria in a cell?",
    n=4
)
print(f"오염 점수: {score:.3f} ({'오염 의심' if score > 0.3 else '정상'})")
```

---

## 맺음말: 평가는 "무엇을 측정하느냐"의 문제

PLM 평가 방법론을 쭉 살펴보면, 결국 이런 흐름이에요:

1. **GPT-1 시절**: "fine-tuning 후 얼마나 빨리 적응하나?" → 전이학습 효율
2. **GPT-2 시절**: "zero-shot으로 뭘 할 수 있나?" → 내재된 능력
3. **GPT-3 이후**: "예제 몇 개로 in-context learning이 되나?" → 범용성
4. **2023~현재**: "표준화된 벤치마크 세트에서 몇 점이나 받나?" → 종합 능력
5. **2024~**: "오염 없이 진짜 실력을 어떻게 측정하나?" → 평가의 신뢰성

어떤 벤치마크를 선택하느냐가 모델의 어떤 능력을 "보이게" 하느냐를 결정해요. MMLU를 잘 올리는 모델이 실제로 더 유용한 건 아닐 수도 있거든요. 반대로, 실제로 좋은 모델이 특정 벤치마크에서 의외로 낮은 점수를 받을 수도 있고요.

가장 정직한 평가는 **다양한 카테고리의 벤치마크를 복합적으로 사용하고, 오염 체크를 하고, base model과 instruction-tuned 모델을 분리해서 보고하는 것** — 그게 최신 LLM paper들이 수렴해가고 있는 방향이에요.

---

## 참고문헌

1. [GPT-1: Improving Language Understanding by Generative Pre-Training](https://openai.com/research/language-unsupervised) — Radford et al., OpenAI, 2018
2. [GPT-2: Language Models are Unsupervised Multitask Learners](https://openai.com/research/better-language-models) — Radford et al., OpenAI, 2019
3. [GPT-3: Language Models are Few-Shot Learners](https://arxiv.org/abs/2005.14165) — Brown et al., 2020
4. [InstructGPT: Training language models to follow instructions with human feedback](https://arxiv.org/abs/2203.02155) — Ouyang et al., 2022
5. [Qwen Technical Report](https://arxiv.org/abs/2309.16609) — Bai et al., Alibaba, 2023
6. [Qwen2 Technical Report](https://arxiv.org/abs/2407.10671) — Qwen Team, 2024
7. [Qwen2.5 Technical Report](https://arxiv.org/pdf/2412.15115) — Qwen Team, 2024
8. [DeepSeek LLM: Scaling Open-Source Language Models with Longtermism](https://arxiv.org/abs/2401.02954) — DeepSeek-AI, 2024
9. [DeepSeek-V3 Technical Report](https://arxiv.org/abs/2412.19437) — DeepSeek-AI, 2024
10. [DeepSeek-R1: Incentivizing Reasoning Capability in LLMs via Reinforcement Learning](https://arxiv.org/abs/2501.12948) — DeepSeek-AI, 2025
11. [Gemma 3 Technical Report](https://arxiv.org/abs/2503.19786) — Gemma Team, Google DeepMind, 2025
12. [Gemma 2: Improving Open Language Models at a Practical Scale](https://arxiv.org/abs/2408.00118) — Gemma Team, Google DeepMind, 2024
13. [KMMLU: Measuring Massive Multitask Language Understanding in Korean](https://arxiv.org/abs/2402.11548) — Son et al., 2024
14. [LiveBench: A Challenging, Contamination-Limited LLM Benchmark](https://arxiv.org/abs/2406.19314) — White et al., 2024
15. [MMLU-Pro: A More Robust and Challenging Multi-Task Language Understanding Benchmark](https://arxiv.org/abs/2406.01574) — Wang et al., 2024
16. [EleutherAI lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) — EleutherAI
17. [OpenCompass](https://github.com/open-compass/opencompass) — OpenCompass Team
18. [HRET: A Self-Evolving LLM Evaluation Toolkit for Korean](https://arxiv.org/abs/2503.22968) — 2025
