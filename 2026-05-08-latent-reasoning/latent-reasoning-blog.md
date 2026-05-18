# Latent Reasoning: LLM이 토큰 없이 사고하는 법 — 6개 핵심 논문 + 해석 연구 종합 리뷰

> "Language is not thought. It is a compressed, lossy encoding of thought."
> — Yoshua Bengio (paraphrased)

> **2026-05-18 업데이트 1**: Single-model latent reasoning을 multi-agent system으로 확장한 RecursiveMAS (arXiv 2604.25917) 섹션 추가. 분야 지형도가 "4가지 흐름"에서 "5가지 흐름"으로 확장되었어요.
>
> **2026-05-18 업데이트 2**: 이 분야의 **베이스 논문인 Coconut을 deep-dive**로 확장 — motivation 3가지, GPT-2 base의 정확한 curriculum, 학습 hyperparameter, GSM8K에서 CoT보다 8.8%p 낮은 충격적 실제 결과까지. 그리고 **"latent를 해석하려는 시도"** 신설 섹션으로 Dynamics·Logit/Coda Lens·LTO·Causal Intervention 5개 후속 연구를 정리했어요.

솔직히 말하면, 우리가 지금까지 당연하게 여겨온 게 있어요. "AI가 추론하려면 그 과정을 텍스트로 써야 한다"는 가정이요. Chain-of-Thought(CoT)가 GPT-4 시대 이후 추론 성능의 핵심 레시피가 되면서, 모델이 생각하는 과정을 죄다 자연어로 뱉어내는 게 당연한 것처럼 느껴졌죠.

근데 최근 연구들이 이 가정에 심각한 의문을 던지고 있어요. **Latent Reasoning**이라는 분야가 바로 그거예요. 추론 과정을 discrete 토큰으로 verbalize하지 않고, 모델의 continuous hidden state 안에서 직접 수행하는 방식이죠.

오늘은 이 분야를 대표하는 6개 논문 — Survey, Coconut, HRM, Soft Thinking, Quiet-STaR, 그리고 가장 최근의 RecursiveMAS — 을 종합적으로 정리해볼게요. 각 논문이 풀려는 문제, 메커니즘, 결과가 모두 다르지만, 하나의 큰 흐름으로 읽히거든요. 특히 마지막의 RecursiveMAS는 latent reasoning을 single model 안에서가 아니라 multi-agent system 전체로 확장한, 분야의 다음 단계를 보여주는 논문이에요.

---

## 목차

1. [왜 Latent Reasoning인가? — 대역폭 이야기](#1-왜-latent-reasoning인가--대역폭-이야기)
2. [분류 체계 — Survey 논문 (arXiv 2507.06203)](#2-분류-체계--survey-논문)
3. [Coconut — Hidden State가 곧 생각이다 (arXiv 2412.06769)](#3-coconut--hidden-state가-곧-생각이다)
4. [HRM — 27M 파라미터로 ARC-AGI를 이기다 (arXiv 2506.21734)](#4-hrm--27m-파라미터로-arc-agi를-이기다)
5. [Soft Thinking — Training-free Latent Reasoning (arXiv 2505.15778)](#5-soft-thinking--training-free-latent-reasoning)
6. [Quiet-STaR — 모든 토큰에서 조용히 생각한다 (arXiv 2403.09629)](#6-quiet-star--모든-토큰에서-조용히-생각한다)
7. [RecursiveMAS — Multi-Agent System으로 Latent Reasoning 확장 (arXiv 2604.25917)](#7-recursivemas--multi-agent-system으로-latent-reasoning-확장)
8. [Latent를 해석하려는 시도 — Probing·Causal·Reward Signal](#8-latent를-해석하려는-시도--probingcausalreward-signal)
9. [5가지 흐름 종합 — 분야 전체 지형도](#9-5가지-흐름-종합--분야-전체-지형도)
10. [미해결 과제와 향후 전망](#10-미해결-과제와-향후-전망)
11. [참고 문헌](#참고-문헌)

---

## 1. 왜 Latent Reasoning인가? — 대역폭 이야기

먼저 "왜 굳이 latent reasoning이냐"는 질문부터 시작해봐요.

### CoT 토큰의 한계

일반 Chain-of-Thought 추론은 생각 과정을 자연어로 써내는 거잖아요. 근데 여기엔 두 가지 근본적인 문제가 있어요.

**문제 1: 표현 대역폭이 터무니없이 작아요**

| 추론 매체 | 정보량 (per step) |
|---|---|
| 자연어 토큰 (vocab ~32k) | log₂(32000) ≈ 15 bits |
| 2,560-dim FP16 hidden state | 2,560 × 16 = 40,960 bits |
| 차이 | **약 2,700배** |

토큰 한 개가 담을 수 있는 정보는 15 bits 남짓인데, 모델 내부 hidden state 하나는 4만 bits에 가깝거든요. 생각을 자연어로 강제로 압축하는 순간, 엄청난 정보 손실이 발생해요.

**문제 2: 단일 경로 commit 문제 (premature commitment)**

CoT는 매 step에서 하나의 토큰을 골라야 해요. 그 선택이 이후 모든 추론 경로를 고정해버리죠. "먼저 A를 시도해보고, 안 되면 B" 같은 병렬 탐색이 원칙적으로 불가능해요.

**문제 3: CoT 토큰의 상당수는 '추론'이 아니에요**

"a", "of", "we know that", "therefore" 같은 언어적 연결사들은 추론이 아니라 fluency를 위해 존재해요. 이 토큰들이 계산 예산을 잡아먹는 거죠.

> "A significant portion of tokens in CoT serve linguistic fluency rather than reasoning — fillers like 'we know that' or 'therefore' consume inference budget without contributing to the reasoning chain."
> — Rui-Jie Zhu et al., *A Survey on Latent Reasoning*, 2025

이 세 가지 문제를 해결하려는 시도가 바로 Latent Reasoning 분야예요.

---

## 2. 분류 체계 — Survey 논문

**논문**: A Survey on Latent Reasoning
**저자**: Rui-Jie Zhu et al. (33인 공저)
**소속**: UCSC, Fudan, Nanjing, Peking, Renmin, U. Melbourne, UW-Madison, HK PolyU, M-A-P
**arXiv**: [2507.06203](https://arxiv.org/abs/2507.06203)
**GitHub**: [LatentCoT-Horizon](https://github.com/multimodal-art-projection/LatentCoT-Horizon)

이 survey는 Latent Reasoning 분야 전체를 2축으로 정리해요. 크게 세 가지 분기로 나눌 수 있어요.

```
Latent Reasoning
├── Vertical Recurrent (Activation-Based)
│   ← 같은 layer를 깊이 방향으로 반복
│   ├── Architectural recurrence
│   │   Universal Transformer, CoTFormer,
│   │   Recursive Transformer, AlgoFormer,
│   │   Recurrent-Depth
│   └── Training-induced
│       Coconut, CODI, CCOT,
│       Stepwise Internalization,
│       Filler/Pause Tokens, Planning Tokens
│
├── Horizontal Recurrent (Hidden-State-Based)
│   ← 시퀀스 방향으로 상태를 전파
│   ├── Linear-state: Mamba-2, GLA, RWKV-6, HGRN-2, DeltaNet
│   └── Gradient-state: TTT, Titans, ATLAS
│
└── Infinite-depth / Diffusion-based
    ├── Masked Diffusion: D3PM, SEDD
    ├── Embedding diffusion: Diffusion-LM, CDCD
    └── Hybrid AR-Diffusion: DiffuLLaMA, Dream
```

### 두 가지 핵심 축

**Vertical Recurrent (수직 반복)**

같은 layer를 여러 번 반복하는 방식이에요. 트랜스포머 레이어를 K번 반복한다고 생각하면 돼요. 파라미터 수는 같은데 계산 깊이를 늘릴 수 있죠. Coconut이나 HRM이 이 계열에 속해요.

**Horizontal Recurrent (수평 전파)**

시퀀스를 처리할 때 hidden state를 토큰 간에 전파하는 방식이에요. Mamba, RWKV, TTT 같은 선형 어텐션 계열이 여기 들어가요. 이쪽은 long-context 효율성 측면에서 트랜스포머의 대안으로 연구되고 있어요.

### 평가 영역과 Open Challenges

Survey가 정리한 평가 벤치마크들:
- **수학 추론**: GSM8K
- **논리 추론**: ProsQA, ProntoQA
- **알고리즘 일반화**: BFS/DFS/Shortest Path
- **Multi-hop QA**

Survey가 짚은 Open Challenges 5가지:

| # | 과제 | 내용 |
|---|---|---|
| 1 | Interpretability gap | Latent state를 symbolic equivalent로 해독 불가 |
| 2 | 학습 안정성 | Recurrent 구조의 gradient 흐름 문제 |
| 3 | Scaling laws | Latent vs. explicit compute 트레이드오프 미규명 |
| 4 | 이론적 이해 | Layer specialization 메커니즘 미해명 |
| 5 | Turing completeness | Layer-based latent CoT의 표현력 증명 필요 |

---

## 3. Coconut — Hidden State가 곧 생각이다

**논문**: Training Large Language Models to Reason in a Continuous Latent Space
**저자**: Shibo Hao, Sainbayar Sukhbaatar, DiJia Su, Xian Li, Zhiting Hu, Jason Weston, Yuandong Tian
**소속**: Meta FAIR + UCSD
**arXiv**: [2412.06769](https://arxiv.org/abs/2412.06769)
**발표**: COLM 2025

> Coconut은 이 분야의 **베이스 논문**이에요. 다른 5개 논문(Survey, HRM, Soft Thinking, Quiet-STaR, RecursiveMAS) 모두가 이 논문을 reference point로 삼고 있어요. 그래서 이 섹션은 다른 섹션보다 두 배쯤 자세히 짰어요. WHY → HOW(학습) → HOW(메커니즘) → BENCHMARK → 상용 모델과의 격차 → 한계 순서로 풀어볼게요.

Coconut(COntinuous Chain Of THought)은 이 분야에서 가장 직관적으로 "latent reasoning"을 구현한 논문이에요. 한 문장으로 요약하면: **마지막 레이어의 hidden state를 디코딩하지 않고 그대로 다음 input embedding으로 밀어넣자**.

### 3.1 WHY — 저자들이 명시한 3가지 동기

저자들이 논문에서 직접 제시한 motivation 3가지가 있어요. 1번 섹션의 추상적 동기를 Coconut 저자의 언어로 다시 보면 이래요.

**(a) CoT 토큰 대부분은 reasoning이 아니라 fluency용**

> "Most word tokens are primarily for textual coherence and not essential for reasoning, whereas some critical tokens require complex planning."

추론 토큰의 정보 가치가 균등하지 않다는 관찰이에요. "we know that", "therefore", "since" 같은 토큰은 사실 추론이 아니라 자연어 흐름을 위한 거고, "let x = ..." 같은 critical token만 진짜 계산을 담아요. 이 균등하지 않음을 단일 vocab projection이 강제로 평탄화하는 게 문제라는 거예요.

**(b) Premature commitment — 단일 path lock-in**

표준 CoT는 매 step에서 token을 argmax/sample로 하나 골라야 해요. 그 선택이 이후 모든 추론 경로를 고정해버려요. "A를 시도하고 안 되면 B로 돌아가자" 같은 backtracking이 원칙적으로 불가능하죠. 특히 ProntoQA·ProsQA처럼 search가 필요한 logical reasoning에서 이게 치명적이에요.

**(c) 인간 뇌의 reasoning은 verbal하지 않다 (신경과학 motivation)**

이게 사실 가장 강력한 근거예요. 신경과학 연구(Amalric & Dehaene 2019, Fedorenko et al. 2024)는 인간이 복잡한 추론을 할 때 **language network는 거의 비활성화**되고 별도의 reasoning network가 활성화된다는 걸 보였어요. "Language might not be necessary for reasoning"이라는 가설이 신경과학에서 점점 합의되고 있고, Coconut은 이 가설을 LLM에 그대로 적용한 첫 대규모 실증이에요.

### 3.2 HOW — 메커니즘 상세

Coconut의 추론 흐름을 정확히 보면 이래요.

**일반 LLM**:

```
input → [transformer layers] → h_t → vocab projection → token_{t+1} → embedding lookup → e_{t+1} → ...
```

`vocab projection → token sampling → embedding lookup` 이 세 단계가 bottleneck이에요. 40,960 bits 짜리 hidden state를 15 bits짜리 토큰으로 압축했다가 다시 임베딩으로 풀죠.

**Coconut**:

```
input → [transformer layers] → h_t → (그대로 e_{t+1}로 사용) → [transformer layers] → ...
```

`h_t`를 디코딩 없이 바로 `e_{t+1}`로 입력해요. 이 step을 c번 반복한 다음, 마지막에 일반 토큰 디코딩 모드로 전환해 답을 생성하죠.

**`<bot>` / `<eot>` special token 역할**:

- `<bot>` (begin-of-thought): 이 토큰을 만나면 모델이 "지금부터 latent mode다"로 전환. 다음 c개 forward pass는 hidden state를 직접 다음 input으로 흘려보냄.
- `<eot>` (end-of-thought): 이 토큰을 만나면 latent mode 종료, 다시 일반 토큰 디코딩 모드로.

이 두 토큰은 학습 가능한 vocab 항목으로 추가돼요. 즉 모델이 "언제 latent로 들어가고 언제 나올지"를 학습할 수 있어요.

**Loss function**:

CE loss는 자연어 토큰 부분에만 적용해요. Latent 구간(`<bot>...<eot>`)에는 supervised signal이 **없어요**.

$$\mathcal{L} = -\sum_{i: y_i \notin \text{latent}} \log P(y_i \mid y_{<i}, \text{model})$$

이 점이 결정적이에요 — latent thought에 대한 ground truth가 없으니, 모델이 "어떤 latent를 만들면 최종 답이 좋아질지"를 알아서 발견해야 해요. **BFS-like emergent behavior가 나오는 이유**가 바로 이거예요.

### 3.3 HOW — 학습 세부 (curriculum이 진짜 핵심)

**Base 모델**: **GPT-2** (~124M 파라미터). 굉장히 작은 모델이에요. 이게 나중에 다룰 "상용 모델과의 격차" 이야기와 연결돼요.

**Multi-stage curriculum**의 정확한 스케줄:

| Task | Stages | c (latent thoughts/step) | Epochs |
|---|---|---|---|
| GSM8K (수학) | 3 | 2 | 첫 stage 6 epoch, 나머지 stage 각 3 epoch |
| ProntoQA / ProsQA (논리) | 6 | 1 | stage당 5 epoch |

각 stage k에서 CoT 시퀀스의 **앞 k개 reasoning step**을 c개의 latent thought로 치환해요. Stage가 진행될수록 더 많은 CoT step이 latent로 옮겨가는 거죠.

논리 task에서는 catastrophic forgetting 방지를 위해 **0.3 확률로 다른 stage의 데이터를 섞어** 학습해요. 이게 안 되면 모델이 가장 최근 stage 형식만 외워버려요.

**한계가 노출되는 부분**: 이 curriculum이 essential해서 — curriculum 없이 학습하면 모델은 latent reasoning을 전혀 못 배워요. 즉 "Coconut의 학습 절차" 자체가 매우 정교한 inductive bias예요. 단순히 architecture 변경이 아니라.

**Hyperparameter** (논문 명시):
- Optimizer: AdamW
- Learning rate, batch size: 논문 본문에 명시되어 있으나 abstract에서는 비공개. 일반적 GPT-2 fine-tuning 범위로 보임 (lr ~1e-4, batch 32-64)

### 3.4 BENCHMARK 결과 (GPT-2 scale)

**정확한 수치**:

| 방법 | GSM8K | ProntoQA | ProsQA | 토큰 예산 |
|---|---|---|---|---|
| No-CoT | 16.5% | 77.5% | 76.7% | ~2 |
| iCoT (선행 연구, 2024) | 30.0% | 99.8% | 98.2% | - |
| Pause Token | 16.5% | 77.5% | 75.9% | - |
| **Coconut (c=2 또는 1)** | **34.1%** | **97.0%** | **96.7%** | **8.2** |
| Discrete CoT (CoT-SFT) | 42.9% | 98.8% | 77.5% | 25.0 |

**해석**:

1. **Coconut은 GSM8K에서 discrete CoT보다 8.8%p 낮음** (34.1% vs 42.9%). 이게 가장 의외의 결과예요. 마케팅된 "더 효율적인 추론"이라는 메시지와 다르게, 실제 GSM8K 정확도는 CoT를 못 따라가요.
2. **ProsQA**에서는 압도적 (96.7% vs 77.5%, +19.2%p). Search-heavy task에서는 진짜 강해요. CoT는 ProsQA에서 No-CoT(76.7%)와 거의 같은데, Coconut만 천장에 가까운 성능을 냄.
3. **토큰 예산은 3배 절감** (25.0 → 8.2). 이게 Coconut의 가장 확실한 이점.

후속 연구 [CODI](https://arxiv.org/abs/2502.21074) (EMNLP 2025)가 이 GSM8K 격차를 self-distillation으로 메꿔 GPT-2에서 **43.7%** 달성, 처음으로 latent CoT가 discrete CoT를 GSM8K에서 따라잡았어요. LLaMA-3.2-1B로 scale up 시 **55.6%**까지.

### 3.5 상용 모델과의 격차 (분야의 가장 큰 미해결 과제)

Coconut을 정직하게 평가하려면 절대 빼놓을 수 없는 부분이에요.

| 모델 | GSM8K 정확도 |
|---|---|
| Coconut (GPT-2, ~124M, 2024-12) | 34.1% |
| CODI (LLaMA-3.2-1B, 2025-02) | 55.6% |
| GPT-4 + CoT | 92%+ |
| Claude 3.5 Sonnet + CoT | 96%+ |
| Claude 4.6 (현재 LLM 상위권) | 98%+ |
| o1 / DeepSeek-R1 (reasoning 모델) | 95-97% |

**Coconut은 상용 모델과 직접 비교한 적이 없어요.** 평가 setup이 통제된 비교(같은 base 모델 위에서 CoT vs Coconut)에 한정되었거든요. 그래서 "Coconut이 더 좋다"는 주장은 **scale-invariant하지 않을 수 있어요**.

이게 분야의 가장 큰 미해결 질문이에요: **Latent reasoning이 70B+ 규모 모델에서도 동일한 우위를 보일까?** 작은 모델에서는 표현 대역폭이 부족해서 latent가 도움이 되지만, 큰 모델에서는 이미 충분한 capacity가 있어서 latent가 marginal해질 수도 있거든요.

지금까지 70B+ 규모에서 latent reasoning을 from-scratch로 학습한 공개 연구는 없어요(2026-05 기준). Soft Thinking이 QwQ-32B에 training-free로 적용된 게 가장 큰 scale.

### 3.6 Emergent BFS-like Behavior — 가장 흥미로운 발견

Coconut에서 가장 놀라운 건 명시적인 supervision 없이 emergent한 behavior가 나온다는 거예요. 3.2에서 본 것처럼 latent 구간에 loss가 없거든요.

> "The continuous thought implicitly encodes multiple candidate reasoning paths simultaneously, exhibiting a BFS-like search behavior that was never explicitly trained."
> — Shibo Hao et al., *Coconut*, 2024

저자들은 ProsQA에서 첫 번째 continuous thought를 강제로 디코딩해봤어요. 그러면 단일 token이 아니라 **여러 candidate path의 시작 토큰들이 비슷한 확률로 분포**돼 있는 걸 발견했어요. 마치 implicit value function이 모든 후보를 동시 평가하는 것처럼요.

후속 연구 ([Dynamics, 2602.08783](https://arxiv.org/abs/2602.08783))가 이걸 mechanistic하게 확증했어요 — 8번 섹션에서 자세히 다뤄볼게요.

### 3.7 Coconut의 한계 (저자 + 후속 연구 종합)

저자 본인이 인정한 + 후속 연구가 지적한 한계를 합치면 7가지예요.

1. **GSM8K에서 CoT를 못 이김** (34.1% vs 42.9%). Latent thought 수를 늘려도 saturating.
2. **Curriculum이 essential** — 없으면 학습 실패. 이게 architectural elegance를 해침.
3. **Curriculum forgetting + error propagation** ([CODI](https://arxiv.org/abs/2502.21074) 지적): stage 간 forgetting이 일어나면 후속 stage 학습이 무너짐.
4. **Sequential 의존성** → vanilla transformer처럼 parallel decoding 불가, inference 가속 어려움.
5. **해석성 부재**: Continuous thought는 사람이 읽을 수 없음. (단, 8번 섹션에서 보겠지만 후속 연구는 일부 해석 가능성을 발견함.)
6. **GPT-2 scale에 한정**: 큰 모델에서의 효과 미검증.
7. **도메인 transfer 미검증**: 수학·논리 외 도메인 (코드 생성, 자연어 이해)에서의 효과 미검증.

---

## 4. HRM — 27M 파라미터로 ARC-AGI를 이기다

**논문**: Hierarchical Reasoning Model
**저자**: Guan Wang et al.
**소속**: Sapient Intelligence (Singapore) + Tsinghua University
**arXiv**: [2506.21734](https://arxiv.org/abs/2506.21734)
**GitHub**: [sapientinc/HRM](https://github.com/sapientinc/HRM)

HRM은 이 분야에서 제일 충격적인 논문이에요. **27M 파라미터**짜리 모델이 Claude 3.7이나 o3-mini-high를 ARC-AGI에서 꺾었거든요. 단 **1,000개 샘플**로, pretraining 없이.

### Brain-inspired 설계: 두 시간 스케일

HRM의 핵심 아이디어는 대뇌 피질의 hierarchical 구조에서 왔어요. 뇌의 고차원 영역(prefrontal cortex)은 느리게 long-timescale 정보를 통합하고, 저차원 감각 영역은 빠르게 즉각적인 처리를 담당하잖아요. HRM이 정확히 이 구조를 모방해요.

| 모듈 | 역할 | 업데이트 빈도 | Participation Ratio |
|---|---|---|---|
| **H-module** (high-level) | 느린 추상 plan 생성 | T 타임스텝마다 1회 | 89.95 (고차원 관여) |
| **L-module** (low-level) | 빠른 세부 계산 처리 | 매 타임스텝 | 30.22 (저차원 처리) |

Participation Ratio는 모듈이 얼마나 고차원 표현을 쓰는지 나타내요. H-module이 더 높은 값을 가지는 게 "느리고 추상적인 계획" 역할을 반영해요.

### Recurrent Dynamics

L-module은 매 step에서 fixed point를 향해 수렴해요:

```
z_L^★ = f_L(z_L^★, z_H^{k-1}, x̃; θ_L)
```

L-module이 이 fixed point에 수렴하면, H-module이 그 결과를 받아서 한 번 업데이트해요. 그 뒤 L-module은 리셋되고 다음 사이클이 시작돼요.

**핵심**: single forward pass로 최종 결과를 도출해요. Explicit reasoning chain 출력이 없어요. 사람이 "이 모델이 어떻게 생각했는지" 볼 수가 없죠.

### 학습 방법

HRM은 기존 CoT 기반 학습과 완전히 달라요:

**1-step gradient (메모리 효율)**
BPTT(Backpropagation Through Time) 대신 Implicit Function Theorem을 씁니다. 각 모듈 final state의 gradient만 계산하므로 메모리 복잡도가 O(1)이에요.

**Deep Supervision**
세그먼트마다 출력을 감독하고 hidden state를 detach해요. 긴 시퀀스에서도 gradient가 안정적으로 흘러요.

**ACT (Adaptive Computation Time)**
Q-learning으로 동적 halting을 구현해요. 어려운 문제는 더 많은 computation step을 쓰도록 스스로 조절해요.

**데이터**: 단 1,000 샘플. Pretraining 없음. CoT supervision 없음.

### 결과 — 충격적인 성능

| 벤치마크 | HRM (27M) | Claude 3.7 | o3-mini-high |
|---|---|---|---|
| **ARC-AGI-1** | **40.3%** | 21.2% | 34.5% |
| Sudoku-Extreme | ~95% | - | - |
| Maze-Hard 30×30 | ~95% | - | - |

Sudoku-Extreme과 Maze-Hard 30×30에서 CoT 기반 모델들은 **0%**를 기록했는데 HRM은 95%예요.

> "Our model achieves 40.3% on ARC-AGI-1 with only 27M parameters, outperforming Claude 3.7 Sonnet (21.2%) and o3-mini-high (34.5%)."
> — Guan Wang et al., *HRM*, 2025

### HRM의 의의와 논쟁

HRM이 중요한 이유는 단순한 성능 숫자가 아니에요. "토큰 verbalization은 추론의 필요조건이 아님"을 가장 강력하게 시연한 사례거든요.

다만 논쟁도 있어요:
- 27M 파라미터는 ARC-AGI 전용 task-specific 모델에 가까워서, 일반 LLM과 직접 비교하기 어렵다는 시각이 있어요.
- 1,000 샘플이라는 극도로 작은 학습 데이터로 일반화가 가능한지 의문이요.
- 벤치마크 외 도메인에서의 검증이 아직 부족해요.

그럼에도 이 결과는 현재 LLM 패러다임에 심각한 질문을 던져요: 수조 원짜리 pretraining이 정말 "추론"에 필수적인가?

---

## 5. Soft Thinking — Training-free Latent Reasoning

**논문**: Soft Thinking: Unlocking the Reasoning Potential of LLMs in Continuous Concept Space
**arXiv**: [2505.15778](https://arxiv.org/abs/2505.15778)
**GitHub**: [eric-ai-lab/Soft-Thinking](https://github.com/eric-ai-lab/Soft-Thinking)
**소속**: UC Santa Barbara, UC Santa Cruz, UCLA, Purdue, LMSYS, Microsoft
**발표**: NeurIPS 2025

Soft Thinking은 이 다섯 논문 중 가장 실용적이에요. **기존 모델 가중치를 전혀 바꾸지 않아요**. Inference 방식만 바꿔서 latent reasoning을 구현하는 training-free 방법이거든요.

### 핵심 아이디어: Concept Token

일반 inference와 Soft Thinking의 차이를 비교해볼게요:

**표준 추론 (argmax/sampling)**:
```python
# 다음 토큰을 하나 선택
next_token = argmax(logits)  # 또는 sample()
next_embedding = embedding_matrix[next_token]
```

**Soft Thinking**:
```python
# 확률 가중합으로 next embedding 계산
probs = softmax(logits)  # shape: [vocab_size]
next_embedding = probs @ embedding_matrix  # soft weighted sum
```

수식으로 쓰면:

```
ẽ_next = Σ_{k=1}^{|V|} p[k] · e(k)
```

- `p[k]`: 모델 출력 다음-토큰 확률 분포
- `e(k)`: 토큰 k의 임베딩 벡터
- `ẽ_next`: 어떤 단일 단어로도 환원되지 않는 continuous concept token

argmax로 단 하나의 토큰을 고르는 대신, **vocabulary 전체에 걸친 확률 가중합**으로 다음 step의 입력을 만드는 거예요. 이게 "concept token"이에요.

### 왜 이게 효과적이냐?

Concept token은 확률 분포의 superposition이에요.

예를 들어 "사과를 먹는다"라는 문장에서 다음 단어를 생성할 때, 모델이 "먹는다"(0.4), "먹었다"(0.3), "먹을"(0.2), 기타(0.1)의 분포를 가졌다면:
- Standard: "먹는다" 하나를 선택 → 나머지 path 버림
- Soft Thinking: 네 개를 동시에 인코딩한 연속 벡터 → 모든 path가 살아있음

여러 reasoning path를 동시에 진행하는 효과가 나타나요. 그리고 단순히 단일 토큰을 선택하는 정보 손실이 없어요.

### 결과 (QwQ-32B 기준)

| 벤치마크 | Standard | **Soft Thinking** | 향상 |
|---|---|---|---|
| MATH-500 | 97.66% | **98.00%** | +0.34%p |
| AIME 2024 | 76.88% | **83.33%** | **+6.45%p** |
| GSM8K | 96.67% | **96.81%** | +0.14%p |
| GPQA-Diamond | 64.17% | **67.17%** | +3.00%p |
| HumanEval | 97.63% | **98.17%** | +0.54%p |

AIME 2024에서 +6.45%p가 눈에 띄어요. 어려운 문제일수록 효과가 크거든요. 쉬운 GSM8K는 이미 천장에 가까워서 개선 폭이 작고요.

**Generation length도 11.6~22.4% 감소**해요. 정확도는 오르고 토큰은 줄었다는 게 직관에 반하는 것 같지만, 논리적으로는 이해돼요. 더 효율적인 경로를 찾으니까 불필요한 탐색을 덜 하는 거예요.

**검증 모델**: QwQ-32B, DeepSeek-R1-Distill-Qwen-32B, DeepSeek-R1-Distill-Llama-70B — 세 모델 모두에서 일관된 개선이 나타났어요.

### Soft Thinking의 의의

다른 논문들은 새로운 아키텍처나 학습 방법이 필요한데, Soft Thinking은 **오늘 당장 기존 모델에 적용할 수 있어요**. argmax 하나를 weighted sum으로 바꾸는 것만으로 효과를 볼 수 있다는 게 실용적으로 굉장히 중요한 포인트예요.

---

## 6. Quiet-STaR — 모든 토큰에서 조용히 생각한다

**논문**: Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking
**arXiv**: [2403.09629](https://arxiv.org/abs/2403.09629)
**발표**: ICLR 2025

Quiet-STaR는 이 분야의 선구적인 논문이에요. 핵심 가설은 이거예요: **"모든 텍스트에는 명시되지 않은 추론 과정이 잠재한다."** 그 잠재적 추론을 internal thought로 명시화해서 언어 모델링 자체를 개선하자는 거죠.

### 메커니즘: Think → Talk → Learn

**1단계: Think (생각)**

텍스트의 모든 토큰 위치에서, 모델이 `<|startofthought|>` 마커를 발사하고 짧은 rationale을 internal하게 샘플해요. 이 rationale은 출력되지 않고 내부적으로만 존재해요.

```
... the sky is [THINK: "blue because light scattering..."] blue ...
... she opened the [THINK: "door, maybe a box..."] box ...
```

**2단계: Talk (말하기)**

Rationale이 있는 상태에서 예측한 next-token 분포와, rationale 없이 예측한 분포를 **mixing head**로 조합해요:

```
p_final = α · p(next | rationale) + (1-α) · p(next | no rationale)
```

초기엔 rationale이 별로 도움이 안 되니 α가 작고, 학습이 진행되면서 점점 커져요.

**3단계: Learn (학습)**

미래 토큰의 likelihood를 개선한 rationale에 REINFORCE 알고리즘으로 reward를 줘요. 좋은 rationale = 더 나은 토큰 예측 → 더 많은 reward. 모델이 스스로 더 좋은 rationale을 생성하는 법을 배워요.

### Implementation Tricks

**Tokenwise parallel sampling**: 모든 위치에서 rationale을 병렬로 생성해요. 순차적으로 하면 너무 느리거든요.

**Learnable thought boundary tokens**: `<|startofthought|>`, `<|endofthought|>` 마커를 학습 가능한 특수 토큰으로 두어, 모델이 "생각을 시작하는 법"과 "생각을 끝내는 법"을 배우도록 해요.

**Extended teacher-forcing**: rationale 다음 토큰까지 한 번에 학습해서 효율을 높여요.

### 결과 (Mistral-7B에 continued pretrain)

| 벤치마크 | Before | After | 향상 |
|---|---|---|---|
| GSM8K | 5.9% | **10.9%** | +5.0%p |
| CommonsenseQA | 36.3% | **47.2%** | +10.9%p |

Zero-shot, fine-tune 없이 이 정도 향상이면 인상적이에요. 특히 어려운 토큰(높은 perplexity)에서 개선이 두드러져요.

### Quiet-STaR의 의의

Quiet-STaR는 나머지 논문들과는 조금 다른 각도에서 중요해요. Coconut이나 HRM이 "추론할 때 latent를 쓰자"라면, Quiet-STaR는 "pretraining 자체에서 latent reasoning을 학습하자"거든요.

> "Every token predicted by a language model is implicitly preceded by unstated reasoning. Quiet-STaR makes this reasoning explicit and uses it as a self-supervised signal."
> — Quiet-STaR 논문 (2024)

Task-specific fine-tuning 없이, 자연 텍스트 corpus만으로 reasoning 능력을 끌어올릴 수 있다는 걸 보인 첫 번째 대규모 실증이에요. 이후 Coconut, Soft Thinking 같은 논문들의 개념적 토대를 닦았다고 볼 수 있어요.

---

## 7. RecursiveMAS — Multi-Agent System으로 Latent Reasoning 확장

**논문**: Recursive Multi-Agent Systems
**저자**: Xiyuan Yang, Jiaru Zou, Rui Pan, Ruizhong Qiu, Pan Lu, Shizhe Diao, Jindong Jiang, Hanghang Tong, Tong Zhang, Markus J. Buehler, Jingrui He, James Zou
**소속**: UIUC, Stanford, MIT, NVIDIA
**arXiv**: [2604.25917](https://arxiv.org/abs/2604.25917)
**프로젝트 페이지**: [recursivemas.github.io](https://recursivemas.github.io)
**제출**: 2026-04-28

지금까지 본 5개 논문은 모두 **하나의 모델 안**에서 latent reasoning을 어떻게 구현할지의 이야기였어요. 그런데 RecursiveMAS는 질문을 한 단계 더 밀어붙여요: **"agent들의 collaboration 자체를 latent space에서 recursion으로 scaling할 수 있을까?"**

지금까지 multi-agent 시스템(MAS)은 agent들이 자연어 메시지를 주고받으며 협력했어요. Planner가 plan을 텍스트로 쓰고, Critic이 그걸 읽고 비판을 텍스트로 쓰고, Solver가 다시 그걸 읽어서 답을 만들고. 매 단계마다 vocab projection — detokenize — re-embed가 일어나죠. 1번 섹션에서 봤던 그 15-bit 병목이 agent 경계마다 반복되는 거예요.

RecursiveMAS는 이 병목을 system 전체에서 제거해요. 모든 intermediate agent 통신을 latent space에서 하고, **최종 round에서만 텍스트로 디코딩**해요.

### 7.1 RecursiveLink — agent를 잇는 가벼운 다리

핵심 컴포넌트는 **RecursiveLink** 모듈이에요. 두 가지 형태가 있어요.

**Inner RecursiveLink** (같은 agent 안에서 latent thought를 다음 forward로 흘려보냄):

$$\mathcal{R}_\text{in}(h) = h + W_2 \sigma(W_1 h)$$

이건 사실상 Coconut을 일반화한 거예요. Agent가 마지막 layer hidden state $h$를 받아서, 다음 forward pass의 input embedding으로 변환하는 residual MLP죠. residual connection이 원본 의미를 유지하면서, MLP가 distribution alignment만 담당해요.

**Outer RecursiveLink** (서로 다른 agent 사이에서 latent state를 전달):

$$\mathcal{R}_\text{out}(h) = W_3 h + W_2 \sigma(W_1 h)$$

이건 heterogeneous agent를 연결할 때 써요. Source agent의 hidden dim과 target agent의 hidden dim이 다를 수 있거든요(예: Qwen-7B는 4096-dim, Llama-3-8B는 4096-dim, Gemma-9B는 3584-dim). $W_3$이 차원을 맞춰주는 projection이에요.

**왜 "lightweight"냐**: base LLM 파라미터는 전부 frozen하고, **RecursiveLink의 작은 MLP만 학습**해요. 전체 trainable parameter는 ~13M (전체 모델의 0.31%) 정도예요. 4-9B 규모 agent 4개를 묶는데 GPU 메모리 15GB로 학습 가능해요.

### 7.2 시스템 구조 — 4가지 collaboration pattern

RecursiveMAS는 4가지 대표적인 agent 협업 패턴에 적용돼요.

| 패턴 | 구조 | Latent reasoning 효과 |
|---|---|---|
| **Sequential** | Planner → Critic → Solver | 중간 plan/critique이 latent로만 흐름 |
| **Mixture** | Math + Code + Science 병렬 → Summarizer | 각 specialist의 latent thought를 그대로 aggregate |
| **Distillation** | Expert ↔ Learner | Expert의 latent guidance가 token으로 압축되지 않음 |
| **Deliberation** | Reflector ↔ Tool-Caller | Tool 실행 결과만 텍스트, 내부 reflection은 latent |

핵심 원칙은 동일해요: **"최종 round만 텍스트를 디코딩한다. 모든 intermediate round는 순수 latent space에서 협업한다."**

### 7.3 학습 — Inner-Outer Loop

RecursiveMAS는 2단계 학습으로 RecursiveLink를 훈련해요.

**Inner Loop (warm-start, 병렬 학습)**

각 agent의 inner RecursiveLink를 독립적으로 학습해요. Latent thought $\mathcal{R}_\text{in}(H)$가 ground-truth 답변의 임베딩 $\text{Emb}_{\theta_i}(y)$와 cosine similarity가 높아지도록:

$$\mathcal{L}_\text{in} = 1 - \cos(\mathcal{R}_\text{in}(H), \text{Emb}_{\theta_i}(y))$$

이렇게 하면 agent가 "latent thought를 생성하는 법"을 미리 배워요.

**Outer Loop (system-level joint training)**

전체 시스템을 $n$ recursion round로 unroll한 다음, 최종 출력에 대해서만 cross-entropy를 계산해요:

$$\mathcal{L}_\text{out} = \text{CE}(\mathcal{S}^{(n)}(\mathcal{S}^{(n-1)}(\ldots \mathcal{S}^{(1)}(x))), y)$$

그리고 gradient를 모든 recursion round의 RecursiveLink로 역전파해요. 이게 "**shared gradient-based credit assignment**"라고 부르는 거예요. 모든 round의 RecursiveLink가 함께 최적화되니까, 어느 round에서 어떤 latent transformation이 일어나야 하는지 system-wide로 학습돼요.

학습 setup: AdamW, lr=5e-4, cosine scheduler, batch size 4, max seq length 4096.

### 7.4 이론 분석 — 왜 text recursion보다 좋은가

논문은 두 가지 이론적 분석을 제공해요. 이게 latent reasoning이 "왜" 좋은지에 대한 가장 엄밀한 논증 중 하나라서 중요해요.

**Proposition 3.1 (런타임 복잡도)**

Text 기반 recursive MAS는 매 round마다 vocab projection $|V| \cdot d_h$가 들어가요. RecursiveMAS는 이걸 $d_h^2$로 대체해요.

| 방식 | round당 복잡도 |
|---|---|
| Text-MAS | $\Theta(N(m\|V\|d_h + \ldots))$ |
| RecursiveMAS | $\Theta(N(m d_h^2 + \ldots))$ |

여기서 $\|V\| \approx 150k$, $d_h \approx 4k$니까 $d_h^2 \ll \|V\| d_h$ 죠. 이게 실제로 1.2-2.4× 추론 가속과 34.6-75.6% 토큰 감소로 이어져요.

**Theorem 4.1 (Gradient 안정성)**

Text 기반 SFT에서는 token 분포의 entropy $\epsilon$이 작아질수록 gradient가 vanishing해요:

$$\left\|\frac{\partial \mathcal{R}_\text{text}(h)}{\partial h}\right\|_2 \leq O(\epsilon) \ll 1$$

반면 RecursiveMAS는 high probability로 안정적인 gradient를 유지해요:

$$\left\|\frac{\partial \mathcal{R}(h)}{\partial h}\right\|_2 \geq \Omega\left(1 - \sqrt{\frac{1}{d_h} \log\frac{1}{\delta}}\right) \approx O(1)$$

이건 "왜 latent space recursion이 학습 가능한가"에 대한 첫 번째 명시적 답변이에요. 1번 섹션에서 봤던 표현 대역폭 argument와 더불어, 이제는 학습 안정성 측면에서도 latent가 유리하다는 증명이 있는 거죠.

### 7.5 결과 — 9개 벤치마크 종합

평가는 9개 벤치마크에서 진행돼요: MATH500, AIME 2025/2026, GPQA-Diamond, MedQA, LiveCodeBench-v6, MBPP+, HotpotQA, Bamboogle. 도메인이 수학·과학·의학·검색·코드를 폭넓게 커버해요.

**평균 결과 ($r=3$ recursion rounds)**

| 지표 | RecursiveMAS vs. 최강 baseline |
|---|---|
| 정확도 | **+8.3%** |
| End-to-end 추론 속도 | **1.2-2.4× 가속** |
| 토큰 사용량 | **34.6-75.6% 감소** |

**구체적 수치 — MATH500 Scaled setting**

| 방법 | 정확도 | 추론 시간 | 토큰 |
|---|---|---|---|
| Recursive-TextMAS | 85.8% | 6010s | 4100 |
| **RecursiveMAS** | **88.0%** | **2320s** | **893** |

같은 ARC-AGI류 task에서 HRM이 "27M으로 거대 모델 격파"했다면, RecursiveMAS는 "agent 4개를 latent로 묶어 60%의 추론 시간과 22%의 토큰으로 더 높은 정확도"를 보였어요.

**패턴별 성능 향상**

| 협업 패턴 | 평균 향상 |
|---|---|
| Mixture | +6.2% |
| Distillation | +8.0% |
| Deliberation | +4.8% |
| Sequential | (구체값 미공개, 전체 평균에 포함) |

**비용 대비 효율 (Table 5)**

| 방법 | GPU 메모리 | Trainable params | 비용 추정 | 평균 정확도 |
|---|---|---|---|---|
| LoRA fine-tuning | - | (큼) | $6.64 | 66.9% |
| Full-SFT | - | 전체 모델 | $9.67 | 68.6% |
| **RecursiveMAS** | **15.29 GB** | **13.12M (0.31%)** | **$4.27** | **74.9%** |

정확도, 비용, 메모리 모두 다른 fine-tuning 방법들을 앞서요.

### 7.6 RecursiveMAS의 의의 — Latent Reasoning의 system-level 일반화

RecursiveMAS가 분야에 던지는 메시지를 정리하면:

**1. Coconut을 multi-agent로 확장한 자연스러운 후속편**

Inner RecursiveLink는 본질적으로 "agent 내부의 Coconut"이에요. Outer RecursiveLink가 더해진 게 진짜 새로운 부분이죠. "Hidden state를 다음 input embedding으로 보낸다"는 Coconut의 핵심 통찰이, 같은 agent의 self-loop를 넘어 **agent 경계까지 확장**된 거예요.

**2. Latent reasoning이 system-level scaling axis가 될 수 있다는 증명**

지금까지 latent reasoning은 주로 single model의 "추론 깊이"를 늘리는 방법으로 인식됐어요. RecursiveMAS는 이걸 "system의 collaboration round 수"라는 새로운 차원으로 확장해요. Test-time compute scaling에 또 다른 축이 생긴 거예요.

**3. Multi-agent 시스템이 텍스트 인터페이스에 묶일 필요가 없다는 첫 대규모 실증**

지금까지 LangChain, AutoGPT, CrewAI 같은 대부분의 multi-agent 프레임워크는 agent 간 통신을 텍스트로 가정해요. 사람이 디버깅하기 좋다는 장점은 있지만, 그게 정말 필요한가? RecursiveMAS는 "중간 round는 latent로, 최종 round만 텍스트로" 라는 절충점을 제시해요.

### 7.7 한계와 열린 질문

논문이 직접 언급하지는 않지만 짚어볼 만한 점들:

- **Base LLM이 freeze된다는 점**: 이는 efficiency 이점이지만, 동시에 RecursiveLink가 표현할 수 있는 transformation에 제약을 둬요. 만약 latent space가 task에 안 맞으면 어떡할지가 불명확해요.
- **Latent thought 길이 $m$의 saturation**: ablation에서 $m=80$ 정도에서 성능이 saturating한다고 보여요. 더 어려운 task에서 이 한계가 어떻게 변할지 미해명.
- **Inner-loop 학습이 큰 모델로 data rewriting에 의존**: Role-specific data를 만들어 줄 "선생 모델"이 필요해요. 이게 fully self-supervised인 다른 latent reasoning 방법들과 다른 점이에요.
- **Agent 수 scaling**: 평가는 2-4 agent 시스템에 한정됐어요. 20+ agent로 갈 때 RecursiveLink가 어떻게 scale하는지는 미검증.

### 7.8 코드와 모델

- **GitHub**: [RecursiveMAS/RecursiveMAS](https://github.com/RecursiveMAS/RecursiveMAS) (저자 페이지에서 공개)
- **HuggingFace**: RecursiveLink 체크포인트 공개
- **프로젝트 페이지**: [recursivemas.github.io](https://recursivemas.github.io)
- **분량**: 36 페이지 (long paper)

당장 재현해보고 싶다면, 4-9B 규모 모델 4개 + GPU 1장으로 작은 setup에서도 돌려볼 수 있어요. Coconut/HRM에 비해 인프라 요구가 합리적인 편이에요.

---

## 8. Latent를 해석하려는 시도 — Probing·Causal·Reward Signal

3번 섹션 3.7의 한계 5번에서 적은 "해석성 부재"는 Coconut의 가장 자주 인용되는 약점이에요. CoT는 틀린 추론 step을 사람이 찾아 디버깅할 수 있지만, latent reasoning은 그게 불가능하니까요. Alignment 관점에서도 심각한 문제고요 — RLHF는 surface 토큰에만 작용하거든요.

그런데 2025년 후반부터 이 한계에 정면으로 도전하는 후속 연구들이 폭발적으로 늘었어요. "**Continuous thought 안에 정말 뭐가 들었나?**"를 mechanistic하게 들여다보는 연구들이에요. 5개 핵심 논문을 정리해볼게요.

### 8.1 Dynamics Within Latent Chain-of-Thought (arXiv 2602.08783, 2026-02)

**핵심 질문**: Coconut/CODI는 정말 multi-step reasoning을 하는가, 아니면 표면적 패턴 매칭인가?

**방법**:
- **Causal probing**: 특정 latent step을 ablate(noise 추가/zeroing)하고 최종 정답률 변화 측정
- **Mechanistic tracing**: layer/step별 정보 흐름을 추적

**타겟**: **Coconut과 CODI를 직접 분석** (이 분야에서 Coconut을 가장 깊이 본 연구)

**핵심 발견 3가지**:
1. **인과적 필수성**: 특정 latent step을 ablate하면 정답률이 통계적으로 유의하게 떨어짐 → 그 step이 정답에 인과적으로 필요했다는 증거
2. **점진적 정보 전파**: latent step이 진행될수록 intermediate result가 layer 단위로 누적/변환됨 (단순히 "마지막 step에서 답이 튀어나오는" 형태가 아님)
3. **다중 가설 동시 유지**: Coconut의 BFS-like behavior 가설을 mechanistic하게 확증. 여러 candidate hypothesis가 latent space에서 동시 활성

**결론**: Coconut은 진짜로 구조화된 reasoning을 하고 있어요. 단순 pattern matching 아닙니다. 다만 그 "reasoning"이 인간의 reasoning과 같은 종류인지는 별개 문제예요.

### 8.2 Latent CoT? Decoding the Depth-Recurrent Transformer (arXiv 2507.02199, 2025-07)

8.1과 정반대로 **회의적인 결과**를 낸 논문이에요. 이런 양쪽 결과가 공존하는 게 분야의 현재 상태예요.

**타겟**: Huginn-3.5B (depth-recurrent transformer). Coconut의 사촌 격이지만 학습 방식이 달라요.

**방법**:
- **Logit lens** (Nostalgebraist 2020): 각 layer의 hidden state를 unembedding matrix로 디코딩해서 "이 layer는 어떤 토큰을 생각하는가" 추적
- **Coda lens** (논문 신규): logit lens를 recurrent block에 맞춰 변형. 각 recurrent iteration에서 디코딩

**발견**:
1. "Limited evidence of interpretable latent CoT" — 검증 가능한 reasoning step이 거의 나타나지 않음
2. **Probe disagreement**: Logit lens와 Coda lens가 같은 hidden state를 다르게 디코딩. 즉 "latent reasoning"의 모습이 측정 방법에 따라 크게 달라짐
3. **Marginal gains**: Recurrent depth를 늘려도 정확도 향상이 미미

**시사점**: 모든 latent reasoning 모델이 같은 메커니즘으로 작동하지 않아요. Huginn 스타일 depth-recurrent는 Coconut 스타일 hidden-feedback과 본질적으로 다른 dynamics를 가질 수 있어요.

### 8.3 Latent Thinking Optimization (LTO) (arXiv 2509.26314, ICLR 2026)

**핵심 발견**: **Latent thought 안에 reward signal이 인코딩되어 있다.**

이게 정말 놀라운 결과예요. 학습 중에 reward로 명시적으로 supervise한 적이 없는데, latent thought만 보고도 "이 추론이 정답에 도달할지"를 예측할 수 있어요.

**증거**:
- 작은 classifier를 latent thought 위에 학습시키면 **정답/오답을 신뢰성 있게 예측** (구체 정확도는 task별 다름)
- 도메인 일반화도 됨: 한 reasoning task에서 학습한 classifier가 다른 task에서도 작동

**활용 (LTO)**:
- Test time에 여러 후보 latent thought를 sampling
- Latent classifier(이제 "Latent Reward Model")로 각 후보 평가
- 가장 reward 높은 latent thought 선택 → 더 좋은 정답

**결과**: 다양한 reasoning task에서 일관된 성능 향상. RLHF 없이 inference만 변경해서 성능을 올린 거예요.

**시사점**: Latent thought는 단순히 "내부 표현"이 아니라 **자체적으로 정답성을 평가하는 정보**를 담고 있어요. 이게 alignment 관점에서 양날의 검이에요 — 좋은 점은 reasoning 품질을 외부에서 측정 가능, 나쁜 점은 모델이 "내부에서 정답을 알면서 다른 답을 출력"할 수 있다는 가능성.

### 8.4 Unlocking the Black Box of Latent Reasoning (ACL ARR 2026 Jan, submission #1192)

3종 probe를 동시에 사용한 종합 해석 연구예요.

**방법** — 3종 probe:
- **Structural probe**: latent vector의 기하학적 구조 분석 (PCA, clustering)
- **Causal probe**: 8.1과 유사한 ablation 기반
- **Geometric probe**: latent space의 manifold 구조 분석

**핵심 발견**:
1. Latent vector는 **"compressed, faithful representations of reasoning steps"** — 실제 reasoning step에 대응하는 압축된 표현
2. **초기 latent vector가 critical causal hub**. 즉 추론 초반의 latent가 후속 추론을 좌우. 이건 "왜 Coconut curriculum이 stage 0(앞에서부터 latent화)부터 시작하는지" 정당화해주는 결과예요.

**활용**: Training-free, decode-time intervention
- 추론 중 latent vector에 geometric/semantic constraint를 부여
- Parameter 업데이트 없이 inference만 바꿔서 정확도 향상

**결과**: 다양한 모델 크기와 task에서 일관된 정확도 향상.

### 8.5 SPAR Project — Interpreting Latent Reasoning (Spring 2026, 진행 중)

Anthropic 출신 연구자가 멘토링하는 [SPAR](https://sparai.org/projects/sp26/recip3J5fnlBXUyFB/) (Supervised Program for Alignment Research) 프로젝트.

- **목표**: "Methods for understanding continuous chain-of-thought"
- **상태**: 2026 Spring 학기 진행 중. mentee가 결정된 단계.
- **현재 미공개**, 결과는 2026 하반기 예상.

이 프로젝트가 alignment 커뮤니티의 관심을 보여줘요 — latent reasoning은 이제 "성능 좋은 트릭"이 아니라 "안전성 측면에서 반드시 해석해야 하는 도전 과제"로 인식되고 있어요.

### 8.6 해석 연구 3대 관점 정리

5개 연구를 종합하면 latent reasoning 해석에 대한 3가지 관점이 공존해요.

| 관점 | 대표 연구 | 메시지 |
|---|---|---|
| **긍정**: latent이 진짜 reasoning 한다 | 8.1 Dynamics, 8.3 LTO, 8.4 Unlocking | 인과 구조·정답 신호 모두 발견됨, intervention도 가능 |
| **회의**: latent reasoning은 measurement artifact일 수 있다 | 8.2 Depth-Recurrent Decoding | Huginn에서는 marginal dynamics만, probe 결과가 일관되지 않음 |
| **활용**: 해석을 inference 개선에 쓰자 | 8.3 LTO, 8.4 Unlocking | Training-free intervention으로 성능 향상 |

### 8.7 해석 연구가 Coconut에 던지는 의미

3번 섹션에서 본 Coconut의 한계 5번("해석성 부재")이 2025-2026에 들어서 부분적으로 깨지고 있어요. 더 이상 latent thought는 완전한 black box가 아니에요. 다만:

- **완전한 해석은 아직 멀어요**: 자연어처럼 "이 step에서 모델이 X를 추론했다"고 명확히 말할 수는 없어요.
- **Architecture-specific 차이**: Coconut style(8.1) vs Depth-Recurrent style(8.2) vs continuous thinking(8.3-8.4)이 모두 다른 해석 방법이 필요해요.
- **Safety 관점에서 매우 중요**: LTO(8.3)의 reward signal 발견은 "모델이 내부에서 정답을 알면서 외부로 다른 답을 출력할 수 있다"는 가능성을 시사해요. RLHF가 latent에 도달하지 못하면 misalignment를 못 잡을 수 있어요.

10번 섹션에서 다시 이 알리고먼트 문제를 다뤄볼게요.

---

## 9. 5가지 흐름 종합 — 분야 전체 지형도

지금까지 본 논문들을 분야 전체 지형도 위에 배치해볼게요.

| 흐름 | 대표 논문 | 핵심 아이디어 | 특징 |
|---|---|---|---|
| **Continuous thought feedback** | Coconut, CODI, CCOT | Hidden state를 다음 input embedding으로 | 학습 필요, BFS emergent |
| **Concept-level superposition** | Soft Thinking | argmax 대신 probability-weighted embedding | Training-free, 즉시 적용 |
| **Architectural recurrence** | HRM, Universal Transformer | Layer 깊이를 동적으로 반복 | 소형 모델 가능, 극한 효율 |
| **Self-supervised internal thought** | Quiet-STaR, STaR 계열 | Rationale을 latent로 self-supervised 학습 | Pretraining 단계에서 적용 |
| **Multi-Agent latent recursion** | RecursiveMAS | Agent 간 통신을 latent로, 최종 round만 텍스트 | System-level scaling, 4가지 패턴 |

### 공통 동인

다섯 흐름을 관통하는 공통 동인이 있어요:

1. **CoT 토큰의 비효율성**: fluency용 토큰, 단일 path commitment 문제
2. **Hidden state의 표현 대역폭**: discrete 토큰 대비 ~2,700배
3. **Test-time compute scaling의 새 차원**: 이전에는 "더 많은 토큰을 생성하면 더 잘 생각한다"였는데, latent reasoning은 "더 깊은 iteration을 하면 더 잘 생각한다"는 방향을 열어줌. RecursiveMAS는 여기에 "더 많은 agent collaboration round"라는 system-level 축까지 추가
4. **Token bottleneck은 모든 경계에 존재**: layer 사이, agent 사이, 모델 사이 어디든 텍스트로 압축하는 순간 정보 손실. Latent는 그 경계를 부순다는 일관된 메시지

### 방법별 접근 비교

| 논문 | 학습 변경 | 아키텍처 변경 | 즉시 적용 가능 | 해석성 | 적용 범위 |
|---|---|---|---|---|---|
| Coconut | 필요 (curriculum) | 없음 | 아니오 | 낮음 | Single model |
| HRM | 필요 (from scratch) | 필요 | 아니오 | 낮음 | Single model (전용) |
| Soft Thinking | 불필요 | 없음 | **예** | 낮음 | Single model |
| Quiet-STaR | 필요 (continued pretrain) | 없음 | 아니오 | 중간 | Single model (pretraining) |
| RecursiveMAS | 필요 (RecursiveLink만) | 추가 (RecursiveLink) | 부분적 (~13M 학습) | 낮음 | **Multi-agent system** |

재밌는 건 다섯 방법 모두 해석성이 낮다는 거예요. 어느 접근을 쓰든 "모델이 어떻게 생각했는지"는 여전히 블랙박스예요. RecursiveMAS는 한 단계 더 나아가서 "agent 사이에 무엇을 주고받았는지"까지 블랙박스화돼요.

### 시점 정렬 — 분야의 시간축

```
2024-03 │ Quiet-STaR        — pretraining에서 latent rationale 학습 (ICLR 2025)
2024-12 │ Coconut           — continuous thought feedback (COLM 2025)
2025-05 │ Soft Thinking     — training-free concept token (NeurIPS 2025)
2025-06 │ HRM               — 27M으로 ARC-AGI 격파
2025-07 │ Survey            — 분야 분류 체계 정립
2026-04 │ RecursiveMAS      — multi-agent로 system-level 확장
```

2년이 채 안 되는 기간에 single-model latent reasoning이 system-level까지 일반화된 거예요. 이 흐름이 다음으로 어디로 갈지는 9번 섹션에서 다뤄볼게요.

---

## 10. 미해결 과제와 향후 전망

### 6가지 핵심 미해결 과제

**1. 해석성 (Interpretability)**

Latent thought는 사람이 읽을 수 없어요. CoT는 틀린 추론 step을 찾아서 디버깅할 수 있지만, latent reasoning은 그게 불가능해요. Alignment 관점에서도 심각한 문제예요 — RLHF는 surface 토큰에만 작용하거든요. Internal thought가 alignment training의 사각지대가 될 수 있어요. RecursiveMAS는 한 단계 더 심각해요 — agent 간 통신까지 latent화하면, "어떤 agent가 무슨 정보를 누구에게 전달했는지"조차 볼 수 없거든요.

**2. 학습 불안정성**

Recurrent 구조는 gradient 폭발/소실 문제가 심해요. HRM이 Implicit Function Theorem으로 이를 일부 해결했고, RecursiveMAS는 Theorem 4.1로 "왜 latent가 text보다 gradient 안정적인지"를 증명했죠. 다만 이게 모든 recurrence 형태에 일반화되는 건 아니에요.

**3. 장기 추론 확장성**

Continuous thought를 수십~수백 step으로 늘릴 때 신호 감쇠 문제가 생겨요. RecursiveMAS의 ablation에서도 latent thought 길이 $m \approx 80$에서 성능이 saturating 한다는 게 보고됐어요. 이론적으로 어떻게 해결할지 아직 열려있어요.

**4. 벤치마크 부족**

현재 평가는 주로 GSM8K, ARC-AGI 같은 기존 벤치마크를 쓰는데, 이것들이 latent reasoning의 강점을 제대로 측정하지 못할 수 있어요. RecursiveMAS는 9개로 도메인을 넓혔지만, **multi-agent latent collaboration만의 고유 강점이 드러나는 새로운 평가 세트**가 필요해요. 예컨대 "agent 간 정보 전달 효율"을 직접 측정하는 벤치마크 같은 거요.

**5. Safety와 Alignment**

내부에서 "생각하고" 외부로 답만 내놓는 구조는 safety 측면에서 새로운 도전이에요. 모델의 실제 reasoning 과정이 외부에서 감사(audit)되지 않는다면, misaligned reasoning을 탐지하기 어려워지거든요. RecursiveMAS는 multi-agent collusion까지 latent로 일어날 가능성을 열어요 — agent들이 텍스트가 아닌 latent로 공모할 수 있다는 거죠.

**6. System-level scaling laws (RecursiveMAS가 새로 던진 질문)**

지금까지 latent reasoning의 scaling은 single model의 깊이/길이 차원이었어요. RecursiveMAS는 "**agent 수** × **recursion round** × **latent dim**" 이라는 3축 scaling 공간을 새로 열었어요. 이 공간 안에서 어떤 trade-off가 있는지, 효율이 saturating하는 지점이 어디인지 — 전혀 모르는 상태예요. 다음 1-2년의 핵심 연구 과제가 될 것 같아요.

### 향후 전망

**단기 (~6개월)**: Soft Thinking류의 training-free 방법이 먼저 실용화될 것 같아요. 기존 모델에 바로 적용할 수 있으니까요. 동시에 RecursiveMAS 스타일의 latent-MAS가 production multi-agent 프레임워크에 흡수되기 시작할 거예요 — LangChain이나 AutoGen이 "latent transport" 옵션을 추가하는 모습을 상상해볼 수 있어요.

**중기 (~1년)**: Coconut과 HRM 계열 접근이 특수 도메인(수학, 알고리즘, 코드)에서 특화 모델로 등장할 가능성이 높아요. RecursiveMAS의 RecursiveLink가 agent endpoint API의 표준 인터페이스가 될 가능성도 있어요 — 즉, "이 모델은 RecursiveLink-compatible입니다" 같은 호환성 spec이 나올 수 있어요.

**장기 (2-3년)**: Latent reasoning과 explicit CoT의 하이브리드가 main stream이 될 것 같아요. 어떤 부분은 latent로, 어떤 부분은 verbalize해서 해석 가능하게 — 이 균형점을 찾는 게 핵심 연구 과제가 될 거예요. RecursiveMAS의 "최종 round만 decode" 아이디어가 이 균형의 한 형태예요. 더 세밀한 hybrid (예: "critical reasoning step만 verbalize")가 나올 거예요.

**가장 중요한 미해결 질문 (2026 기준 업데이트)**:

기존 질문: "Latent reasoning이 더 나은 성능을 보이는 이유가 정말 '표현 대역폭'인가, 아니면 다른 메커니즘이 있는가?"

새로 추가된 질문: "**Multi-agent system 전체가 latent로 협업할 때, 시스템이 단일 거대 모델과 어떻게 다른 행동을 보이는가?** 한 거대 모델로 합칠 수 있는데도 굳이 여러 agent로 나누는 게 의미 있는가?" — 이건 RecursiveMAS가 던진 가장 깊은 질문이에요. 모듈성(modularity)의 이론적 근거가 latent space에서도 유효한지가 핵심 쟁점이 될 거예요.

---

## 참고 문헌

| # | 논문/자료 | 링크 |
|---|---|---|
| 1 | A Survey on Latent Reasoning (Zhu et al., 2025) | [arXiv:2507.06203](https://arxiv.org/abs/2507.06203) |
| 2 | Reasoning Beyond Language: A Survey | [arXiv:2505.16782](https://arxiv.org/abs/2505.16782) |
| 3 | Coconut: Training LLMs to Reason in a Continuous Latent Space | [arXiv:2412.06769](https://arxiv.org/abs/2412.06769) |
| 4 | HRM: Hierarchical Reasoning Model | [arXiv:2506.21734](https://arxiv.org/abs/2506.21734) |
| 5 | HRM GitHub | [sapientinc/HRM](https://github.com/sapientinc/HRM) |
| 6 | Soft Thinking: Unlocking the Reasoning Potential of LLMs in Continuous Concept Space | [arXiv:2505.15778](https://arxiv.org/abs/2505.15778) |
| 7 | Soft Thinking GitHub | [eric-ai-lab/Soft-Thinking](https://github.com/eric-ai-lab/Soft-Thinking) |
| 8 | Quiet-STaR: Language Models Can Teach Themselves to Think Before Speaking | [arXiv:2403.09629](https://arxiv.org/abs/2403.09629) |
| 8a | **Recursive Multi-Agent Systems (RecursiveMAS)** | [arXiv:2604.25917](https://arxiv.org/abs/2604.25917) |
| 8b | RecursiveMAS 프로젝트 페이지 | [recursivemas.github.io](https://recursivemas.github.io) |
| 8c | RecursiveMAS GitHub | [RecursiveMAS/RecursiveMAS](https://github.com/RecursiveMAS/RecursiveMAS) |
| 8d | **CODI: Compressing CoT into Continuous Space via Self-Distillation (EMNLP 2025)** | [arXiv:2502.21074](https://arxiv.org/abs/2502.21074) |
| 8e | **Dynamics Within Latent Chain-of-Thought** (Coconut/CODI 인과 분석) | [arXiv:2602.08783](https://arxiv.org/abs/2602.08783) |
| 8f | **Latent CoT? Decoding the Depth-Recurrent Transformer** (Logit/Coda Lens) | [arXiv:2507.02199](https://arxiv.org/abs/2507.02199) |
| 8g | **Latent Thinking Optimization (LTO)** (ICLR 2026) | [arXiv:2509.26314](https://arxiv.org/abs/2509.26314) |
| 8h | **Unlocking the Black Box of Latent Reasoning** (ACL ARR 2026) | [OpenReview](https://openreview.net/forum?id=VHsfDkWqkS) |
| 8i | SPAR Project — Interpreting Latent Reasoning (Spring 2026) | [sparai.org](https://sparai.org/projects/sp26/recip3J5fnlBXUyFB/) |
| 9 | LaDiR: Latent Diffusion Reasoning | [arXiv:2510.04573](https://arxiv.org/abs/2510.04573) |
| 10 | Latent Thinking Optimization | [arXiv:2509.26314](https://arxiv.org/abs/2509.26314) |
| 11 | Multimodal CoCoT | [arXiv:2508.12587](https://arxiv.org/abs/2508.12587) |
| 12 | Implicit Reasoning Survey | [arXiv:2509.02350](https://arxiv.org/abs/2509.02350) |
| 13 | LatentCoT-Horizon GitHub | [multimodal-art-projection/LatentCoT-Horizon](https://github.com/multimodal-art-projection/LatentCoT-Horizon) |
| 14 | Universal Transformer | [arXiv:1807.03819](https://arxiv.org/abs/1807.03819) |
| 15 | Mamba-2 | [arXiv:2405.21060](https://arxiv.org/abs/2405.21060) |
| 16 | TTT: Learning to (Learn at Test Time) | [arXiv:2407.04620](https://arxiv.org/abs/2407.04620) |
| 17 | Titans: Learning to Memorize at Test Time | [arXiv:2501.00663](https://arxiv.org/abs/2501.00663) |
