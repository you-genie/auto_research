# Latent Reasoning: LLM이 토큰 없이 사고하는 법 — 5개 핵심 논문 종합 리뷰

> "Language is not thought. It is a compressed, lossy encoding of thought."
> — Yoshua Bengio (paraphrased)

솔직히 말하면, 우리가 지금까지 당연하게 여겨온 게 있어요. "AI가 추론하려면 그 과정을 텍스트로 써야 한다"는 가정이요. Chain-of-Thought(CoT)가 GPT-4 시대 이후 추론 성능의 핵심 레시피가 되면서, 모델이 생각하는 과정을 죄다 자연어로 뱉어내는 게 당연한 것처럼 느껴졌죠.

근데 최근 연구들이 이 가정에 심각한 의문을 던지고 있어요. **Latent Reasoning**이라는 분야가 바로 그거예요. 추론 과정을 discrete 토큰으로 verbalize하지 않고, 모델의 continuous hidden state 안에서 직접 수행하는 방식이죠.

오늘은 이 분야를 대표하는 5개 논문 — Survey, Coconut, HRM, Soft Thinking, Quiet-STaR — 을 종합적으로 정리해볼게요. 각 논문이 풀려는 문제, 메커니즘, 결과가 모두 다르지만, 하나의 큰 흐름으로 읽히거든요.

---

## 목차

1. [왜 Latent Reasoning인가? — 대역폭 이야기](#1-왜-latent-reasoning인가--대역폭-이야기)
2. [분류 체계 — Survey 논문 (arXiv 2507.06203)](#2-분류-체계--survey-논문)
3. [Coconut — Hidden State가 곧 생각이다 (arXiv 2412.06769)](#3-coconut--hidden-state가-곧-생각이다)
4. [HRM — 27M 파라미터로 ARC-AGI를 이기다 (arXiv 2506.21734)](#4-hrm--27m-파라미터로-arc-agi를-이기다)
5. [Soft Thinking — Training-free Latent Reasoning (arXiv 2505.15778)](#5-soft-thinking--training-free-latent-reasoning)
6. [Quiet-STaR — 모든 토큰에서 조용히 생각한다 (arXiv 2403.09629)](#6-quiet-star--모든-토큰에서-조용히-생각한다)
7. [4가지 흐름 종합 — 분야 전체 지형도](#7-4가지-흐름-종합--분야-전체-지형도)
8. [미해결 과제와 향후 전망](#8-미해결-과제와-향후-전망)
9. [참고 문헌](#참고-문헌)

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

Coconut(COntinuous Chain Of THought)은 이 분야에서 가장 직관적으로 "latent reasoning"을 구현한 논문이에요. 한 문장으로 요약하면: **마지막 레이어의 hidden state를 디코딩하지 않고 그대로 다음 input embedding으로 밀어넣자**.

### 메커니즘

일반적인 LLM 추론 흐름을 생각해보면:

```
input → [transformer layers] → hidden_t → vocab projection → token_{t+1} → embedding → [transformer layers] → ...
```

여기서 `vocab projection → token_{t+1} → embedding` 부분이 bottleneck이에요. 40,960 bits 짜리 hidden state를 15 bits짜리 토큰으로 압축했다가 다시 풀죠.

Coconut은 이걸 없애요:

```
input → [transformer layers] → h_t → (그대로) e_{t+1} → [transformer layers] → ...
```

`h_t`를 디코딩 없이 바로 `e_{t+1}`로 입력해요. 이 "continuous thought"를 N번 반복한 다음, 마지막에 일반 토큰 디코딩 모드로 전환해 답을 생성하죠.

### 학습: Multi-Stage Curriculum

처음부터 모든 추론을 latent로 하면 학습이 너무 어려워요. 그래서 점진적 curriculum을 씁니다:

| Stage | 내용 |
|---|---|
| Stage 0 | 일반 CoT supervised learning |
| Stage 1 | CoT의 앞 1개 step → continuous thought, 나머지는 자연어 |
| Stage k | CoT의 앞 k개 step → continuous thought |
| Stage K+ | 모든 reasoning이 continuous, 답만 자연어 |

앞에서부터 CoT step을 하나씩 latent로 바꿔가는 distillation curriculum이에요. 기존 CoT의 감독 신호를 최대한 활용하면서 점진적으로 latent space로 이전하는 거죠.

### 결과

| Task | No-CoT | Standard CoT | **Coconut** |
|---|---|---|---|
| GSM8K | ~70% | ~85% | **~89%** |
| ProntoQA | ~45% | ~72% | **~78%** |
| ProsQA | ~55% | ~68% | **~74%** |

토큰은 50-70% 줄이면서 정확도는 오히려 올랐어요. 특히 ProntoQA, ProsQA처럼 search가 필요한 논리 추론에서 격차가 더 크게 나요.

### Emergent BFS-like Behavior — 가장 흥미로운 발견

Coconut에서 가장 놀라운 건 명시적인 supervision 없이 emergent한 behavior가 나온다는 거예요.

> "The continuous thought implicitly encodes multiple candidate reasoning paths simultaneously, exhibiting a BFS-like search behavior that was never explicitly trained."
> — Shibo Hao et al., *Coconut*, 2024

Coconut의 continuous thought를 분석해보면 단일 trajectory가 아니라 여러 candidate path를 동시에 인코딩하는 superposition 상태예요. 자연어로 특정 path를 선택하는 순간 발생하는 premature commitment를 latent space가 자연스럽게 회피하는 거죠.

이게 왜 중요하냐면 — explicit BFS를 구현하거나 beam search를 쓰거나 하는 게 아니라, latent space의 선형 결합 특성이 알아서 "병렬 탐색"을 구현한다는 거거든요.

### Coconut의 한계

- **해석성 부재**: Continuous thought는 사람이 읽을 수 없어요. 디버깅이 사실상 불가능하죠.
- **긴 reasoning chain 확장 불확실**: continuous thought를 수십, 수백 step으로 늘릴 때 신호 감쇠 문제가 있어요.
- **도메인 transfer 미검증**: 수학, 논리 추론 이외 도메인으로의 일반화가 충분히 검증되지 않았어요.

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

## 7. 4가지 흐름 종합 — 분야 전체 지형도

지금까지 본 논문들을 분야 전체 지형도 위에 배치해볼게요.

| 흐름 | 대표 논문 | 핵심 아이디어 | 특징 |
|---|---|---|---|
| **Continuous thought feedback** | Coconut, CODI, CCOT | Hidden state를 다음 input embedding으로 | 학습 필요, BFS emergent |
| **Concept-level superposition** | Soft Thinking | argmax 대신 probability-weighted embedding | Training-free, 즉시 적용 |
| **Architectural recurrence** | HRM, Universal Transformer | Layer 깊이를 동적으로 반복 | 소형 모델 가능, 극한 효율 |
| **Self-supervised internal thought** | Quiet-STaR, STaR 계열 | Rationale을 latent로 self-supervised 학습 | Pretraining 단계에서 적용 |

### 공통 동인

네 흐름을 관통하는 공통 동인이 있어요:

1. **CoT 토큰의 비효율성**: fluency용 토큰, 단일 path commitment 문제
2. **Hidden state의 표현 대역폭**: discrete 토큰 대비 ~2,700배
3. **Test-time compute scaling의 새 차원**: 이전에는 "더 많은 토큰을 생성하면 더 잘 생각한다"였는데, latent reasoning은 "더 깊은 iteration을 하면 더 잘 생각한다"는 방향을 열어줌

### 방법별 접근 비교

| 논문 | 학습 변경 | 아키텍처 변경 | 즉시 적용 가능 | 해석성 |
|---|---|---|---|---|
| Coconut | 필요 (curriculum) | 없음 | 아니오 | 낮음 |
| HRM | 필요 | 필요 | 아니오 | 낮음 |
| Soft Thinking | 불필요 | 없음 | **예** | 낮음 |
| Quiet-STaR | 필요 (continued pretrain) | 없음 | 아니오 | 중간 |

재밌는 건 네 방법 모두 해석성이 낮다는 거예요. 어느 접근을 쓰든 "모델이 어떻게 생각했는지"는 여전히 블랙박스예요.

---

## 8. 미해결 과제와 향후 전망

### 5가지 핵심 미해결 과제

**1. 해석성 (Interpretability)**

Latent thought는 사람이 읽을 수 없어요. CoT는 틀린 추론 step을 찾아서 디버깅할 수 있지만, latent reasoning은 그게 불가능해요. Alignment 관점에서도 심각한 문제예요 — RLHF는 surface 토큰에만 작용하거든요. Internal thought가 alignment training의 사각지대가 될 수 있어요.

**2. 학습 불안정성**

Recurrent 구조는 gradient 폭발/소실 문제가 심해요. HRM이 Implicit Function Theorem으로 이를 일부 해결했지만, 일반적인 해법은 아직 없어요.

**3. 장기 추론 확장성**

Continuous thought를 수십~수백 step으로 늘릴 때 신호 감쇠 문제가 생겨요. 시퀀스가 길어질수록 초기 latent state의 정보가 희석되는 현상이요. 이론적으로 어떻게 해결할지 아직 열려있어요.

**4. 벤치마크 부족**

현재 평가는 주로 GSM8K, ARC-AGI 같은 기존 벤치마크를 쓰는데, 이것들이 latent reasoning의 강점을 제대로 측정하지 못할 수 있어요. Latent reasoning만의 고유한 강점이 드러나는 평가 세트가 필요해요.

**5. Safety와 Alignment**

내부에서 "생각하고" 외부로 답만 내놓는 구조는 safety 측면에서 새로운 도전이에요. 모델의 실제 reasoning 과정이 외부에서 감사(audit)되지 않는다면, misaligned reasoning을 탐지하기 어려워지거든요.

### 향후 전망

**단기**: Soft Thinking류의 training-free 방법이 먼저 실용화될 것 같아요. 기존 모델에 바로 적용할 수 있으니까요.

**중기**: Coconut과 HRM 계열 접근이 특수 도메인(수학, 알고리즘, 코드)에서 특화 모델로 등장할 가능성이 높아요.

**장기**: Latent reasoning과 explicit CoT의 하이브리드가 main stream이 될 것 같아요. 어떤 부분은 latent로, 어떤 부분은 verbalize해서 해석 가능하게 — 이 균형점을 찾는 게 핵심 연구 과제가 될 거예요.

**가장 중요한 미해결 질문**: "Latent reasoning이 더 나은 성능을 보이는 이유가 정말 '표현 대역폭'인가, 아니면 다른 메커니즘이 있는가?" 이걸 엄밀히 증명하는 mechanistic interpretability 연구가 필요해요.

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
| 9 | LaDiR: Latent Diffusion Reasoning | [arXiv:2510.04573](https://arxiv.org/abs/2510.04573) |
| 10 | Latent Thinking Optimization | [arXiv:2509.26314](https://arxiv.org/abs/2509.26314) |
| 11 | Multimodal CoCoT | [arXiv:2508.12587](https://arxiv.org/abs/2508.12587) |
| 12 | Implicit Reasoning Survey | [arXiv:2509.02350](https://arxiv.org/abs/2509.02350) |
| 13 | LatentCoT-Horizon GitHub | [multimodal-art-projection/LatentCoT-Horizon](https://github.com/multimodal-art-projection/LatentCoT-Horizon) |
| 14 | Universal Transformer | [arXiv:1807.03819](https://arxiv.org/abs/1807.03819) |
| 15 | Mamba-2 | [arXiv:2405.21060](https://arxiv.org/abs/2405.21060) |
| 16 | TTT: Learning to (Learn at Test Time) | [arXiv:2407.04620](https://arxiv.org/abs/2407.04620) |
| 17 | Titans: Learning to Memorize at Test Time | [arXiv:2501.00663](https://arxiv.org/abs/2501.00663) |
