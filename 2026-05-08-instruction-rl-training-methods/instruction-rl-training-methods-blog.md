# 오픈 LLM Post-Training 완전 정복: SFT·RL 레시피·데이터 합성·평가 종합 비교

> 📊 **발표자료**: [instruction-rl-training-methods-presentation.pptx](./instruction-rl-training-methods-presentation.pptx)

> **이 글은 [PLM 사전학습 평가 리서치(2026-05-06)](../2026-05-06-plm-pretraining-evaluation/)의 후속편입니다.**
> Post-training 단계 — SFT, Preference Optimization, RL — 전반을 실전 레시피 수준으로 다룹니다.

---

## §0 한 페이지 요약: Post-Training 패러다임 비교 표

| 모델 | SFT 데이터 규모 | Preference/RL 알고리즘 | Reward 타입 | 핵심 특징 |
|---|---|---|---|---|
| InstructGPT (2022) | ~14.7k (human demos) | PPO + KL penalty | Human RM (Bradley-Terry) | RLHF 원형, SFT→RM→PPO |
| LLaMA 2 (2023) | ~27.5k (SFT) + RS | PPO + Rejection Sampling | Helpfulness+Safety 이중 RM | PPO 직전에 RS로 초기화 |
| Zephyr-7B (2023) | dSFT (distill) | dDPO (UltraFeedback) | GPT-4 평가 (AI Feedback) | 순수 오프라인 DPO 베이스라인 |
| LLaMA 3.1 (2024) | ~10M (synthetic 위주) | Iterative DPO (6 rounds) | On-policy RM | RS+SFT+DPO 루프 반복 |
| Qwen2.5 (2024) | 1M+ | DPO (Online Merging Opt) | Human+Auto hybrid | 1M SFT + 150k DPO pairs |
| DeepSeek-V3 (2024) | 1.5M | GRPO | Rule-based (accuracy+format) | MoE 671B, 5K GPU-hr PT |
| DeepSeek-R1 (2025) | ~800k (cold-start+RS) | GRPO (multi-stage) | Rule-based 순수 RL | R1-Zero: SFT 없는 순수 RL |
| Qwen3 (2025) | 대규모 (4-stage) | GRPO + Iterative RL | Rule-based + reward model | 사고/비사고 모드 통합 |
| Gemma 3 (2025) | distill 위주 | BOND+WARM+WARP | Human+code exec+GT | KD 기반 SFT + RL 융합 |
| Tulu 3 (2024) | 다중 도메인 mix | SFT→DPO→RLVR | Verifiable reward (math/code) | 완전 공개 레시피의 모범 |
| Phi-4 (2024) | 1.4M pairs, 8.3B tok | SFT + iterative DPO | GPT-4 기반 auto-eval | 합성 교재 데이터 위주 |
| Nemotron-4 340B (2024) | 98% synthetic | SFT + DPO | 5차원 Reward Model | Helpfulness/Correctness 등 |

---

## §1 Post-Training 시대구분: InstructGPT → DPO → R1

### 1.1 RLHF 원년: InstructGPT (2022)

2022년 OpenAI의 [InstructGPT](https://arxiv.org/abs/2203.02155)는 현대 post-training의 원형을 정의했거든요. 세 단계로 구성된 RLHF 파이프라인입니다:

1. **SFT** — 사람이 직접 작성한 데모(~14.7k 샘플)로 GPT-3를 미세조정
2. **Reward Model 학습** — 동일한 프롬프트에 대한 모델 출력 쌍을 사람이 비교 평가 → Bradley-Terry 모델로 RM 학습
3. **PPO** — RM 신호로 정책 최적화 + per-token KL penalty로 SFT 모델과의 과도한 이탈 방지

> "We trained InstructGPT models by fine-tuning GPT-3 to follow a broad class of written instructions using human feedback." — Ouyang et al., 2022

핵심 발견은 **1.3B InstructGPT가 175B GPT-3보다 인간 평가자에게 선호된다**는 것이었어요. 파라미터 수보다 학습 방식이 훨씬 중요하다는 증거.

### 1.2 DPO 혁명 (2023)

[DPO(Direct Preference Optimization)](https://arxiv.org/abs/2305.18290)(Rafailov et al., 2023)는 RM→PPO 2단계를 단일 분류 손실로 압축했어요.

핵심 아이디어: 최적 정책과 reward function 사이의 closed-form 관계를 이용하면, 별도 RM을 학습하지 않고 preference pair만으로 직접 정책을 최적화할 수 있다는 것. 학습이 안정적이고, PPO처럼 on-policy 샘플링이 불필요합니다.

[Zephyr-7B](https://arxiv.org/abs/2310.16944)(2023)는 DPO의 실용성을 가장 잘 보여준 사례예요. Mistral-7B 베이스에 distilled SFT(dSFT) + distilled DPO(dDPO)를 적용해서, GPT-4 평가 기반 UltraFeedback 64k 쌍만으로 인상적인 성능을 달성했죠.

### 1.3 Reasoning RL 시대: DeepSeek-R1 (2025)

2025년 초, [DeepSeek-R1](https://arxiv.org/abs/2501.12948)이 "SFT 없는 순수 RL로도 추론 능력이 창발한다"는 걸 보여주면서 패러다임이 또 한 번 바뀌었어요.

- **R1-Zero**: 베이스 모델에 rule-based reward만으로 GRPO → chain-of-thought 자발적 창발
- **R1**: cold-start SFT → RL → rejection sampling SFT → 최종 RL의 4단계 파이프라인

이후 Qwen3, Sky-T1, S1 등 수많은 reasoning 모델이 이 레시피를 따르거나 변형하고 있습니다.

---

## §2 데이터 합성 방법 카탈로그

### 2.1 Self-Instruct (Wang et al., 2022)

[Self-Instruct](https://arxiv.org/abs/2212.10560)는 175개의 인간 작성 seed instruction에서 출발해 LLM이 스스로 instruction을 생성·필터링하는 방법이에요. Alpaca(52k 샘플)가 이 방식으로 만들어졌고, text-davinci-003 API 호출로 생성했습니다.

**실제 사용 모델**: Stanford Alpaca, Alpaca-GPT4

**한계**: 반복적 패턴, 낮은 다양성, 쉬운 instruction 편향

### 2.2 Evol-Instruct (WizardLM, 2023)

[WizardLM](https://arxiv.org/abs/2304.12244)의 Evol-Instruct는 기존 instruction을 더 복잡하게 진화시키는 방식입니다:

- **In-depth evolution**: 제약 추가, 구체화, 추론 단계 증가 등으로 복잡도 향상
- **In-breadth evolution**: 토픽 다양성·스킬 커버리지 확대

같은 아이디어를 코드에 적용한 [WizardCoder](https://arxiv.org/abs/2306.08568)도 있어요. 수학에는 WizardMath.

**실제 사용 모델**: WizardLM-70B, WizardMath, WizardCoder

### 2.3 Teacher 모델에서의 Distillation (Vicuna, Orca, Phi)

- **[Vicuna](https://lmsys.org/blog/2023-03-30-vicuna/)** — ShareGPT에서 수집한 70k 인간 GPT-4 대화로 LLaMA 미세조정. user/assistant 구분 마스킹 처리
- **[Orca](https://arxiv.org/abs/2306.02707)** — FLAN-v2에서 1M GPT-4 설명 트레이스 추출. 추론 과정(explanation trace)까지 distill
- **[Phi 시리즈](https://arxiv.org/abs/2412.08905)** — "교과서 같은" 합성 데이터 위주 학습. Phi-4는 1.4M pairs, 8.3B 토큰의 고품질 합성 데이터

### 2.4 Persona-Driven Synthesis (Persona-Hub, 2024)

[Persona-Hub](https://arxiv.org/abs/2406.20094)(Chan et al., 2024)는 웹 데이터에서 자동 추출한 10억 개의 페르소나를 활용해 다양한 합성 데이터를 생성합니다.

> "Simply adding a persona to a data synthesis prompt can steer the LLM towards the corresponding perspective to create distinctive synthetic data." — Chan et al., 2024

수학, 논리 추론, instruction, 지식 등 다양한 도메인에 적용 가능. Qwen2.5 post-training 데이터 생성에 활용됐어요.

### 2.5 Magpie (2024, ICLR 2025)

[Magpie](https://arxiv.org/abs/2406.08464)는 별도의 seed prompt 없이 chat template의 left-side만 LLM에 입력해서 user query를 자동 생성하는 방법이에요.

```
[INST] (← 여기까지만 입력)
→ 모델이 자동으로 user turn을 완성함
```

정렬된 LLM(예: LLaMA-3-Instruct)에서 직접 user query를 추출하기 때문에 **별도 prompt engineering 불필요**. Magpie-Pro-1M 등 대규모 데이터셋을 공개했습니다.

### 2.6 Rejection Sampling / Best-of-N

여러 응답을 생성하고 reward model 또는 verifier로 최고 응답을 선택하는 방법. 단순하지만 강력해요.

- **LLaMA 2** — 70B 모델로 reject sampling 후 더 작은 모델 학습에 재사용
- **DeepSeek-R1** — stage 3에서 ~600k reasoning 샘플을 reject sampling으로 수집
- **Best-of-N (BoN)** — inference-time에 N개 생성 후 RM으로 best 선택 (test-time compute)

### 2.7 Self-Rewarding LM (Yuan et al., 2024)

[Self-Rewarding LM](https://arxiv.org/abs/2401.10020)은 LLM 자체를 judge로 사용해서 preference pair를 생성하고, iterative DPO로 학습합니다.

- LLM-as-Judge: 5점 척도로 자체 응답 평가
- Iterative DPO: 매 iteration마다 on-policy 선호 데이터 생성

**문제점**: judge 품질이 정책 품질과 함께 높아져야 함 → circular feedback 위험

### 2.8 Constitutional AI / RLAIF (Anthropic, 2022)

[Constitutional AI](https://arxiv.org/abs/2212.08073)는 AI가 원칙(constitution)에 따라 자기 비평·수정을 통해 안전한 응답을 생성하는 방법이에요.

1. **SL-CAI**: 모델이 응답 생성 → 헌법 원칙에 따른 자기 비평 → 수정 → SFT 학습
2. **RLAIF**: AI 평가 기반 preference 데이터 → RM 학습 → PPO

**실제 사용**: Claude 시리즈의 안전성 학습에 핵심 활용

### 2.9 합성 Preference 데이터 (UltraFeedback, HelpSteer2)

- **[UltraFeedback](https://arxiv.org/abs/2310.01377)** — 64k 프롬프트 × 4개 모델 응답, GPT-4로 각 응답 평가 (instruction-following, honesty, helpfulness). Zephyr, Tulu 학습에 활용
- **[HelpSteer2](https://arxiv.org/abs/2406.08673)** — NVIDIA의 10만 preference pair. Nemotron reward model 학습에 사용. 5차원(helpfulness, correctness, coherence, complexity, verbosity) 평가

### 2.10 코드·수학 특화 합성

| 데이터셋 | 방법 | 규모 | 사용 모델 |
|---|---|---|---|
| [MetaMathQA](https://arxiv.org/abs/2309.12284) | 질문 역변환(backward reasoning) | 395k | WizardMath |
| [NuminaMath](https://huggingface.co/datasets/AI-MO/NuminaMath-CoT) | 경시 수학 CoT | 860k | DeepSeek-Math, OpenR1 |
| [OpenCodeInstruct](https://arxiv.org/abs/2504.04030) | Evol-Instruct 변형 | 5M+ | CodeLLaMA 후속 |
| Magpie-Code | chat template 기반 | 다양 | 다양 |

### 2.11 Reasoning Trace Synthesis (R1-distill 계열)

[DeepSeek-R1-Distill](https://arxiv.org/abs/2501.12948)은 R1의 long CoT reasoning trace를 더 작은 모델에 distill하는 방식이에요.

- **[OpenThoughts](https://huggingface.co/open-thoughts)** — 오픈소스 reasoning trace 데이터셋
- **[S1K](https://arxiv.org/abs/2501.17161)** — 1000개의 고난도 수학 문제 + Gemini Flash reasoning trace → Qwen2.5-32B fine-tuning으로 o1-preview 능가
- **[Bespoke-Stratos](https://huggingface.co/datasets/bespokelabs/Bespoke-Stratos-17k)** — 17k reasoning traces
- **OpenR1-Math-220k** — NuminaMath 기반 R1 distill traces

---

## §3 SFT 레시피 비교

### 3.1 공통 원칙: Loss Masking

모든 모델에서 공통으로 적용되는 SFT 원칙:

```python
# Assistant turn만 loss 계산, system/user는 마스킹
labels = torch.full_like(input_ids, -100)  # 전체 -100 (무시)
# assistant 발화 구간만 원래 token ID로 복원
labels[assistant_start:assistant_end] = input_ids[assistant_start:assistant_end]
```

**Multi-turn**: 각 assistant turn마다 loss를 계산하고, user/system은 -100으로 마스킹.

### 3.2 LLaMA 시리즈

**LLaMA 2 (2023)**:
- SFT: 27,540개 human-written demonstrations (상당히 소규모!)
- Iterative RLHF: Rejection Sampling → PPO 순서
- 이중 RM: Helpfulness RM + Safety RM, 선형 조합으로 최종 reward
- PPO KL penalty + PPO-ptx (pretraining gradient mixing)

> "After RLHF-V4, we sequentially combined Rejection Sampling and PPO fine-tuning." — Touvron et al., 2023

**LLaMA 3.1 (2024)**:
- SFT 데이터: ~10M 이상, 거의 모두 합성 데이터
- Post-training loop을 **6 rounds** 반복
- **Iterative DPO**: on-policy preference pair (Tulu 3와 유사 방식)
- Rejection Sampling + SFT → DPO 순서 (PPO 버림)
- System prompt 다양화, multi-turn conversation 비중 높음

### 3.3 Qwen 시리즈

**Qwen2.5 (2024)**:
- SFT: **1M+ 샘플** (general / math / code / multilingual / long-context / safety 혼합)
- Chat template: ChatML 형식 (`<|im_start|>user\n...<|im_end|>\n`)
- DPO: 150k preference pairs, Online Merging Optimizer, lr=7×10⁻⁷, 1 epoch
- GRPO: 수학/코딩 도메인 중심 rule-based reward

**Qwen3 (2025)**:
- **4단계 post-training**:
  1. Long Thinking SFT (reasoning CoT 데이터)
  2. Reasoning RL (GRPO, 3,995 query-verifier pairs, large batch + high rollouts)
  3. Thinking Mode Fusion (사고/비사고 통합 SFT)
  4. General RL (helpfulness + harmlessness 일반 RL)
- AIME'24 스코어: 70.1 → 85.1 (170 RL training steps 동안)

### 3.4 DeepSeek 시리즈

**DeepSeek-V3 (2024)**:
- SFT: **1.5M 인스턴스**, 도메인별 다양한 생성 방법
- 시퀀스 패킹 + 샘플 간 attention masking (mutual invisibility)
- GRPO 기반 RL (rule-based reward: accuracy + format)
- post-training 전체: 5,000 GPU hours (pre-training의 0.18%!)

**DeepSeek-R1-Zero** (순수 RL):
- 베이스 모델에서 직접 GRPO 적용
- SFT cold-start 없음
- Rule-based reward만 사용:
  - **Format reward**: `<think>...</think>` 태그 형식
  - **Accuracy reward**: 수학은 boxed 답 정확도, 코드는 컴파일/테스트
- 자발적 chain-of-thought, self-reflection 창발

**DeepSeek-R1** (multi-stage):
1. **Cold-start SFT**: 수천 개 long CoT 데이터로 미세조정
2. **Reasoning RL**: GRPO + rule-based reward, language consistency reward 추가
3. **Rejection Sampling SFT**: ~600k reasoning + ~200k non-reasoning = 800k 합산, 2 epoch
4. **General RL**: 다양한 프롬프트 + helpfulness/harmlessness

### 3.5 Gemma 시리즈 (Google DeepMind)

**Gemma 3 (2025)**:
- **Knowledge Distillation 기반 SFT**: 큰 teacher IT 모델에서 증류, pre-training부터 통합
  - 256 logits/token을 teacher 확률로 가중 샘플링, soft target으로 cross-entropy
- **BOND**: Best-of-N Distillation — BoN 샘플링 결과로 policy 학습
- **WARM** (Weight-Averaged Reward Models): 여러 RM의 weight averaging으로 reward hacking 방지
- **WARP** (Weight-Averaged Reward Policies): RL 정책들을 weight space에서 평균
- Reward 함수: Helpfulness, Math, Code, Reasoning, IF, Multilingual, Safety 7개 목표 동시 최적화

### 3.6 Tulu 3 (AI2, 2024) — 완전 공개 레시피

[Tulu 3](https://arxiv.org/abs/2411.15124)는 가장 투명하게 공개된 post-training 레시피예요:

**4단계 파이프라인**:
1. **Prompt Curation + Synthesis**: 도메인별 고품질 프롬프트 선별·합성
2. **SFT**: Core skill 혼합 데이터 (tulu-3-sft-mixture) — math, code, safety, IF, knowledge
3. **DPO**: On-policy preference pair (Tulu 3 SFT output vs 타 모델 output 비교)
4. **RLVR**: Verifiable reward RL (수학 정답 검증, 코드 실행 검증)

**RLVR**이 핵심 기여로, 검증 가능한 정답이 있는 도메인(수학, 코딩, IF)에서는 외부 verifier를 reward로 직접 사용. SWE-Bench, MATH 등에서 효과적.

데이터, 학습 코드, 체크포인트 모두 공개: [github.com/allenai/open-instruct](https://github.com/allenai/open-instruct)

### 3.7 Phi 시리즈 (Microsoft)

**Phi-4 (2024)**:
- SFT 데이터: 1.4M prompt-response pairs, 8.3B unique tokens
- 데이터 대부분이 합성: 교과서 형식, 문제-풀이 형식의 고품질 reasoning 데이터
- 추가: 공개 웹 데이터 + 라이선스 도서에서 seed 추출 → 합성 확장
- Iterative DPO + SFT 반복
- 14B 파라미터임에도 GPT-4o와 경쟁하는 수학/코딩 성능

### 3.8 Nemotron-4 340B (NVIDIA, 2024)

[Nemotron-4 340B](https://arxiv.org/abs/2406.11704):
- **98% 합성 데이터**로 alignment 진행
- 합성 파이프라인: Nemotron-4-340B-Instruct로 응답 생성 → Nemotron-4-340B-Reward로 필터링
- **5차원 Reward Model**: Helpfulness, Correctness, Coherence, Complexity, Verbosity
- RewardBench에서 당시 SOTA (GPT-4o, Gemini 1.5 Pro 능가)
- 단일 DGX H100(8×GPU, FP8)에서 배포 가능

---

## §4 Preference/RL 알고리즘 카탈로그

### 4.1 PPO (Proximal Policy Optimization)

InstructGPT, LLaMA 2에서 사용된 RLHF의 표준 알고리즘이에요.

**핵심 구성**:
- **Policy network** (π_θ): 학습 대상 LM
- **Value network** (V_φ): 기댓값 추정, 보통 policy와 같은 크기
- **Reward model** (R): 사람 선호도 학습 RM
- **Reference model** (π_ref): KL penalty의 기준

**PPO-clip 목적함수**:
```
J_PPO(θ) = E_t[min(r_t(θ)·A_t, clip(r_t(θ), 1-ε, 1+ε)·A_t)]
r_t(θ) = π_θ(a_t|s_t) / π_θ_old(a_t|s_t)
```

**LLM에서의 KL penalty** (per-token):
```
R_total(x, y) = R(x, y) - β * KL(π_θ || π_ref)
```

**LLaMA 2 특이사항**:
- PPO-ptx: `J = J_PPO - γ * J_pretraining` (공개 NLP 데이터의 pretraining 기울기 혼합)
- Rejection Sampling으로 초기화 후 PPO 적용
- 이중 RM: `R = c1 * R_help + c2 * R_safety`

### 4.2 DPO (Direct Preference Optimization)

[DPO](https://arxiv.org/abs/2305.18290)(Rafailov et al., 2023)의 손실 함수:

```
L_DPO(θ) = -E_(x,y_w,y_l)[log σ(β * log(π_θ(y_w|x)/π_ref(y_w|x)) 
                               - β * log(π_θ(y_l|x)/π_ref(y_l|x)))]
```

- `y_w`: 선호 응답 (winner), `y_l`: 비선호 응답 (loser)
- `β`: KL penalty 계수 (보통 0.1~0.5)
- `π_ref`: 고정된 SFT 모델

**핵심**: RM을 직접 학습하지 않고, preference data만으로 정책 최적화.

**DPO 변형 비교**:

| 알고리즘 | 손실 함수 변형 | 특징 | 장점 |
|---|---|---|---|
| **IPO** | identity transformation | reference-free 변형 | label noise에 강함 |
| **KTO** | Kahneman-Tversky value fn | 단일 라벨(좋음/나쁨) 적용 가능 | pair 불필요 |
| **ORPO** | odds-ratio 기반 | SFT loss와 통합 | reference model 불필요 |
| **SimPO** | reference log-ratio 제거 | 더 단순한 gradient | 더 안정적 |

**SimPO** (Meng et al., 2024):
```
L_SimPO = -E[log σ(β/|y_w| * log π_θ(y_w|x) - β/|y_l| * log π_θ(y_l|x) - γ)]
```
reference model 없이 평균 log-prob으로 정규화. 길이 편향도 완화.

### 4.3 GRPO (Group Relative Policy Optimization)

[DeepSeek-Math](https://arxiv.org/abs/2402.03300)에서 도입한 GRPO는 PPO에서 value network를 제거하고 그룹 기준선을 사용합니다.

**완전한 수식** (논문에서 직접 인용):

$$\mathcal{J}_{GRPO}(\theta) = \mathbb{E}\left[\frac{1}{G}\sum_{i=1}^{G}\frac{1}{|o_{i}|}\sum_{t=1}^{|o_{i}|}\left\{\min\left[\frac{\pi_{\theta}(o_{i,t}|q,o_{i,<t})}{\pi_{\theta_{old}}(o_{i,t}|q,o_{i,<t})}\hat{A}_{i,t}, \text{clip}(\cdot,1-\varepsilon,1+\varepsilon)\hat{A}_{i,t}\right]-\beta\mathbb{D}_{KL}\left[\pi_{\theta}||\pi_{ref}\right]\right\}\right]$$

**Advantage 계산 (그룹 기준선)**:

$$\hat{A}_{i,t} = \tilde{r}_{i} = \frac{r_{i} - \text{mean}(\mathbf{r})}{\text{std}(\mathbf{r})}, \quad \mathbf{r} = \{r_1, \ldots, r_G\}$$

**KL 발산 추정 (unbiased estimator)**:

$$\mathbb{D}_{KL}[\pi_{\theta}||\pi_{ref}] = \frac{\pi_{ref}}{\pi_{\theta}} - \log\frac{\pi_{ref}}{\pi_{\theta}} - 1$$

**PPO 대비 장점**:
- Value network 불필요 → GPU 메모리 40~60% 절약
- Group 내 상대 비교로 baseline 추정 → critic bias 없음
- 수학/코딩처럼 rule-based reward가 있을 때 특히 강력

**하이퍼파라미터 가이드 (DeepSeek-R1 기준)**:
- G (group size): 보통 8~16
- β (KL coeff): 0.01~0.1
- ε (clip): 0.2 (PPO 기본값)
- large batch + high rollouts + off-policy training 권장

### 4.4 Rejection Sampling Fine-Tuning (RS-FT)

별도 알고리즘이라기보다는 데이터 생성 방법. Best-of-N 샘플링 후 높은 reward의 응답만 SFT에 사용.

```python
# pseudocode
for prompt in prompts:
    candidates = model.generate(prompt, n=N)
    scores = reward_model.score(candidates)
    best = candidates[scores.argmax()]
    sft_data.append((prompt, best))
```

LLaMA 2에서는 RS 후 PPO로 이어지는 파이프라인. DeepSeek-R1 stage 3에서는 대규모 RS로 600k CoT 샘플 수집.

### 4.5 DAPO (ByteDance/Tsinghua, 2025)

GRPO의 불안정성을 개선한 [DAPO](https://arxiv.org/abs/2503.14476):

1. **Clip-Higher**: KL penalty 비대칭 clipping (높은 ratio는 더 강하게 clip)
2. **Dynamic Sampling**: 너무 쉽거나 어려운 문제 필터링 (all-correct, all-wrong 그룹 제거)
3. **Token-level Policy Gradient**: sequence-level이 아닌 token-level gradient
4. **Overlong Reward Shaping**: 과도하게 긴 응답에 음수 reward

AIME 2024에서 Qwen2.5-32B로 50점 달성, DeepSeek-R1-Zero 능가.

### 4.6 REINFORCE++ / RLOO

**[REINFORCE++](https://arxiv.org/abs/2501.03262)**:
- Critic 없음 + global batch normalization
- PPO보다 안정적, GRPO보다 단순
- OpenRLHF에서 지원

**RLOO (REINFORCE Leave-One-Out)**:
- G개 샘플에서 자기 자신을 제외한 나머지의 평균 reward를 baseline으로 사용
- RAFT보다 sample-efficient (동일 on-policy 샘플에서 더 좋은 성능)

### 4.7 Online vs Offline DPO

| | Offline DPO | Online DPO | Iterative DPO |
|---|---|---|---|
| **Preference 데이터** | 사전 수집된 고정 데이터셋 | 학습 중 on-policy 생성 | 라운드별 on-policy 생성 반복 |
| **장점** | 간단, 재현 가능 | distribution shift 최소화 | 점진적 개선 |
| **단점** | distribution mismatch | 계산 비용 높음 | 복잡한 파이프라인 |
| **사례** | Zephyr, 초기 DPO | LLaMA 3.1 | Tulu 3, LLaMA 3.1 |

### 4.8 PRM vs ORM (수학 추론)

**ORM (Outcome Reward Model)**:
- 최종 답만 평가 (정답/오답)
- 구현 간단, 수집 용이
- 중간 오류를 감지 못함

**PRM (Process Reward Model)**:
- 각 추론 단계마다 점수 부여
- 오류 조기 감지, 더 세밀한 피드백
- 레이블링 비용 높음 (단계별 human 평가 필요)

**[Math-Shepherd](https://arxiv.org/abs/2312.08935)**: MCTS 기반 자동 step-level 레이블 생성

**[OmegaPRM](https://arxiv.org/abs/2406.06592)**: rule-based partitioning으로 OmegaPRM이 Math-Shepherd 능가 (Gemini Pro: MATH500 69.4%)

### 4.9 RLVR (Tulu 3 도입)

Verifiable reward를 RM 대신 사용하는 RL:

```python
def rlvr_reward(response, ground_truth, task_type):
    if task_type == "math":
        return 1.0 if verify_math_answer(response, ground_truth) else 0.0
    elif task_type == "code":
        return 1.0 if run_tests(response, test_cases) else 0.0
    elif task_type == "instruction_following":
        return verify_constraints(response, constraints)
```

외부 verifier를 reward로 직접 사용 → reward hacking 원천 차단. Tulu 3에서 math/coding 성능 크게 향상.

---

## §5 모델별 RL 레시피 비교

### 5.1 R1 계열 vs 전통적 RLHF 비교

| 항목 | 전통 RLHF (LLaMA 2) | DPO 기반 (LLaMA 3.1) | GRPO 기반 (DeepSeek-R1) |
|---|---|---|---|
| **RM 필요 여부** | 필요 (학습) | 불필요 | 불필요 (rule-based) |
| **On-policy 샘플링** | PPO 학습 중 필요 | 오프라인 가능 | GRPO 중 필요 |
| **학습 안정성** | 불안정 (RM hacking) | 안정적 | 안정적 |
| **주 도메인** | 일반 helpfulness | 일반 instruction | 수학, 코딩, 추론 |
| **Reward 설계** | 사람 선호도 → RM | preference pair | rule-based verifier |

### 5.2 Qwen3 4단계 RL 파이프라인 (상세)

```
[Stage 1] Long Thinking SFT
→ Long CoT reasoning data (수학, 코딩, 과학)
→ 모델이 <think>...</think> 패턴 습득

[Stage 2] Reasoning RL (GRPO)  
→ 3,995 query-verifier pairs
→ Large batch, high rollouts, off-policy training
→ AIME'24: 70.1 → 85.1 (170 steps)

[Stage 3] Thinking Mode Fusion SFT
→ 사고 데이터 + 비사고 데이터 혼합
→ /think, /no_think 또는 thinking_budget 제어 가능
→ 다양한 일반 태스크 포함

[Stage 4] General RL
→ Helpfulness + Harmlessness 최적화
→ 다양한 도메인 프롬프트
```

### 5.3 R1 재현 프로젝트들

| 프로젝트 | 베이스 모델 | 방법 | 주요 결과 |
|---|---|---|---|
| [OpenR1](https://huggingface.co/blog/open-r1) (HuggingFace) | LLaMA-3/Qwen2.5 | GRPO + R1 distill | OpenR1-Math-220k 공개 |
| [S1](https://arxiv.org/abs/2501.17161) (Stanford) | Qwen2.5-32B | SFT only (1k samples) | o1-preview 능가 (수학) |
| [Sky-T1](https://github.com/NovaSky-AI/SkyT1) (NovaSky) | QwQ-32B-Preview | SFT | AIME ~43점 |
| [Light-R1](https://arxiv.org/abs/2503.10460) | DeepSeek-R1-Distill | Curriculum SFT+DPO+RL | 작은 모델 효율적 학습 |
| [Skywork-OR1](https://arxiv.org/abs/2505.22312) | DeepSeek-R1-Distill | RL (GRPO 계열) | AIME24 82.2, 32B로 R1 능가 |
| [Open-Reasoner-Zero](https://github.com/Open-Reasoner-Zero) | 다양 | R1-Zero 레시피 재현 | cold-start 없는 RL |

---

## §6 평가 방법론

### 6.1 자동 벤치마크

**일반 능력**:
- **[MMLU](https://arxiv.org/abs/2009.03300)** / **[MMLU-Pro](https://arxiv.org/abs/2406.01574)**: 57개/122개 학문 분야 다지선다. 지식 폭 측정. Pro는 더 어렵고 10지선다
- **[IFEval](https://arxiv.org/abs/2311.07911)**: 명시적 instruction following 검증 (길이 제약, 형식 등 파싱 가능한 규칙)
- **[BBH (BIG-Bench Hard)](https://arxiv.org/abs/2210.09261)**: 23개 어려운 추론 태스크
- **[GPQA Diamond](https://arxiv.org/abs/2311.12022)**: 박사급 과학 문제 (198문항)

**수학**:
- **[GSM8K](https://arxiv.org/abs/2110.14168)**: 초등 수학 8.5k 문제
- **[MATH](https://arxiv.org/abs/2103.03874)** / **MATH-500**: AMC/AIME 수준 12.5k / 500문제
- **[AIME](https://artofproblemsolving.com/wiki/index.php/AMC_Problems)**: 실제 미국 수학 올림피아드 (2024, 2025)
- **[AMC](https://artofproblemsolving.com/wiki/index.php/AMC_Problems)**: AMC 10/12 경시 수학

**코딩**:
- **[HumanEval+](https://github.com/evalplus/evalplus)** / **[MBPP+](https://github.com/evalplus/evalplus)**: 164/378 문제, 더 강력한 테스트케이스
- **[LiveCodeBench](https://livecodebench.github.io/)**: 실시간 업데이트, contamination 방지
- **[BigCodeBench](https://bigcode-bench.github.io/)**: 1,140개 실용 코딩 태스크
- **[SWE-Bench Verified](https://www.swebench.com/)**: GitHub 실제 이슈 500개 해결

**추론**:
- **[ZebraLogic](https://arxiv.org/abs/2406.01556)**: 논리 퍼즐
- **[ARC-Challenge](https://arxiv.org/abs/1803.05457)**: 과학 상식 (어려운 버전)
- **[MuSR](https://arxiv.org/abs/2310.16049)**: 다단계 소프트 추론

**롱컨텍스트**:
- **[RULER](https://arxiv.org/abs/2404.06654)**: Needle-in-Haystack 변형
- **[LongBench](https://arxiv.org/abs/2308.14508)**: 6개 카테고리 중국어/영어 long-context
- **NeedleHaystack**: 긴 문서에서 사실 검색

**다국어**:
- **[MGSM](https://arxiv.org/abs/2210.01330)**: 11개 언어 수학 추론
- **[MMMLU](https://huggingface.co/datasets/Babelscape/MMMLU)**: 다국어 MMLU
- **[C-Eval](https://arxiv.org/abs/2305.08322)** / **[CMMLU](https://arxiv.org/abs/2306.09212)**: 중국어 평가
- **[KMMLU](https://arxiv.org/abs/2402.11548)**: 한국어 MMLU, 전문 지식 중심
- **[HAE-RAE Bench](https://arxiv.org/abs/2309.02706)**: 한국 문화·언어 이해
- **[KoBEST](https://arxiv.org/abs/2204.04541)**: 한국어 NLU 5개 태스크

**안전성**:
- **[TruthfulQA](https://arxiv.org/abs/2109.07958)**: 거짓 정보 생성 경향 측정
- **[ToxiGen](https://arxiv.org/abs/2203.09509)**: 독성 텍스트 생성 벤치마크
- **[BBQ](https://arxiv.org/abs/2110.08193)**: 사회적 편향 측정
- **WildGuard**: 다양한 안전성 카테고리

**Tool/Agent**:
- **[BFCL (Berkeley Function Calling)](https://gorilla.cs.berkeley.edu/leaderboard.html)**: 함수 호출 능력
- **[SWE-Bench](https://www.swebench.com/)**: GitHub 이슈 해결
- **[AgentBench](https://llmbench.ai/agent/data)**: 에이전트 태스크 8개

### 6.2 LM-Judge / Pairwise 평가

**[MT-Bench](https://arxiv.org/abs/2306.05685)** (FastChat):
- 80개 multi-turn 질문 (8개 카테고리)
- GPT-4가 1~10점 채점
- **한계**: 단일 judge, 소규모 문제 세트, GPT-4 모방 모델에 유리한 편향

**[AlpacaEval 2.0 (LC Win-Rate)](https://arxiv.org/abs/2404.04475)**:
- 805개 instruction, GPT-4 Turbo가 GPT-4 baseline과 비교
- **LC (Length-Controlled) win-rate**: 길이 편향 제거, Arena와 Spearman r=0.98
- **문제**: LC win-rate도 GPT-4 finetuned 모델에 유리할 수 있음

**[Arena-Hard / Arena-Hard-Auto v0.1](https://arxiv.org/abs/2406.11939)**:
- 500개 어려운 기술 문제, GPT-4-Turbo 대비 win-rate
- AlpacaEval 대비 더 도전적 문제 세트

**LM-judge 공통 편향**:
- **Length bias**: 긴 응답을 선호하는 경향
- **Position bias**: 먼저 나온 응답을 선호
- **Sycophancy**: judge와 같은 제조사 모델에 유리
- **Contamination**: judge가 학습 데이터와 유사한 응답을 선호
- **Null model 공격**: 구조화된 일정 응답으로 86.5% LC win-rate 달성 가능 (Shi et al., 2024)

### 6.3 Human / Arena 평가

**[LMSYS Chatbot Arena](https://chat.lmsys.org/)** Elo:
- 크라우드소싱 A/B 비교, 익명 전투
- 6M+ 투표 데이터, 신뢰도 높은 인간 평가
- Bradley-Terry 모델로 Elo 계산
- **강점**: contamination 어려움, 다양한 실제 쿼리
- **약점**: 사용자 풀 편향(영어/기술 중심), 안전성 태스크 포함 어려움

**인간 평가 셋업 표준**:
- **Likert 5점**: 응답 품질 직접 평가
- **A/B 비교**: 두 응답 중 더 선호하는 것 선택
- **다차원 평가**: 정확성, 유창성, 안전성, 유용성 별도 평가
- **Golden set**: 전문가가 작성한 정답 대조 평가

---

## §7 모델 × 벤치마크 매트릭스

아래 표는 주요 모델들이 기술 보고서에서 **보고한** 벤치마크를 나타냅니다 (점수가 아닌 사용 여부):

| 모델 | MMLU | MATH | GSM8K | HumanEval | IFEval | MT-Bench | AlpacaEval2 | GPQA | LiveCB | KMMLU |
|---|---|---|---|---|---|---|---|---|---|---|
| InstructGPT | △ | - | - | - | - | - | - | - | - | - |
| LLaMA 2 | ○ | △ | ○ | ○ | - | ○ | - | - | - | - |
| LLaMA 3.1 | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | ○ | - |
| Qwen2.5 | ○ | ○ | ○ | ○ | ○ | - | - | ○ | ○ | ○ |
| Qwen3 | ○ | ○ | ○ | ○ | ○ | - | - | ○ | ○ | ○ |
| DeepSeek-V3 | ○ | ○ | ○ | ○ | ○ | - | - | ○ | ○ | - |
| DeepSeek-R1 | ○ | ○ | ○ | ○ | ○ | - | - | ○ | ○ | - |
| Gemma 3 | ○ | ○ | ○ | ○ | ○ | - | - | ○ | - | - |
| Phi-4 | ○ | ○ | ○ | ○ | ○ | ○ | - | ○ | - | ○ |
| Tulu 3 | ○ | ○ | ○ | ○ | ○ | ○ | ○ | - | - | - |
| Zephyr | ○ | - | ○ | ○ | - | ○ | ○ | - | - | - |
| Nemotron-4 | ○ | ○ | ○ | ○ | - | ○ | ○ | - | - | - |

○: 보고됨, △: 부분 보고, -: 미보고

---

## §8 새 Instruction 모델 만들 때의 실용 가이드

### 8.1 데이터 비율 권장

**SFT 단계**:
```
일반 instruction-following: 30~40%
수학/코딩: 20~30% (품질 특히 중요)
안전성/거절: 5~10%
롱컨텍스트: 5~10%
다국어 (한국어 포함): 10~20%
멀티턴 대화: 15~25%
```

**DPO 단계** (on-policy 권장):
- 총 50k~200k pair 이상이면 충분
- On-policy > Off-policy (distribution shift 최소화)
- 어려운 프롬프트 위주 샘플링 권장

**GRPO / RLVR 단계**:
- 검증 가능한 도메인(수학, 코딩) 집중
- Group size G=8~16, batch 크게
- rule-based reward 우선 (reward hacking 방지)

### 8.2 학습 단계 권장 순서

```
1. 고품질 SFT (500k~2M 샘플)
   - loss masking: assistant turn만
   - packing with masking
   
2. Iterative DPO (on-policy, 2~6 rounds)
   - β = 0.1~0.5
   - on-policy preference pair 생성
   
3. RLVR 또는 GRPO (선택적)
   - 수학/코딩처럼 verifiable reward 있을 때
   - G=8~16, β_KL=0.01~0.1
   
4. 최종 safety fine-tuning
```

### 8.3 학습 하이퍼파라미터 (경험치)

| 단계 | LR | Batch Size | Epoch | 주요 설정 |
|---|---|---|---|---|
| SFT | 1e-5 ~ 2e-5 | 128~512 | 2~3 | warmup 5%, grad clip 1.0 |
| DPO | 5e-7 ~ 2e-6 | 64~256 | 1~3 | β=0.1~0.5, reference model frozen |
| GRPO | 1e-6 ~ 5e-6 | 128~512 | 에포크 개념 없음 | G=8~16, clip ε=0.2 |

### 8.4 평가셋 구성 권장

**최소 평가셋 (빠른 반복)**:
- MATH-500 (수학)
- HumanEval+ (코딩)
- IFEval (instruction following)
- MT-Bench (일반)

**전체 평가셋**:
- 위 + MMLU-Pro, GPQA Diamond, LiveCodeBench
- AlpacaEval 2.0 LC, Arena-Hard
- 한국어 모델: KMMLU, HAE-RAE, HRM8K 추가

### 8.5 흔한 함정

1. **Benchmark contamination**: 학습 데이터에 평가 문제가 포함되면 점수 부풀려짐. LiveCodeBench처럼 동적으로 업데이트되는 벤치마크 병행 사용 권장
2. **Judge bias**: MT-Bench, AlpacaEval은 GPT-4 finetuned 모델에 유리. 여러 judge 평가 병행
3. **Length bias**: DPO로 학습하면 응답이 길어지는 경향. LC win-rate, SimPO로 완화
4. **Safety-helpfulness tradeoff**: 안전성 강화 → helpfulness 하락. 두 메트릭 동시 모니터링
5. **Reward hacking**: 신경망 RM보다 rule-based reward가 안전. RM 학습시 OOD 프롬프트 포함

---

## §9 한국어 모델 추가 고려사항

### 9.1 한국어 특화 평가 벤치마크

| 벤치마크 | 내용 | 특징 |
|---|---|---|
| **[KMMLU](https://arxiv.org/abs/2402.11548)** | 전문 지식 다지선다 (11개 카테고리) | 영어 MMLU의 한국어 버전 |
| **[KMMLU-Pro](https://arxiv.org/abs/2507.08924)** | 국가 자격증 시험 기반 | 더 높은 난이도 |
| **[HAE-RAE Bench](https://arxiv.org/abs/2309.02706)** | 한국 문화·언어·상식 | 독자적 문화 이해 필요 |
| **[HRM8K](https://huggingface.co/datasets/HAERAE-HUB/HRM8K)** | 한국어 수학 + 영어 수학 이중 언어 | KSAT 수학 포함 |
| **[KoBEST](https://arxiv.org/abs/2204.04541)** | NLI, BoolQ, COPA, WIC, HellaSwag | 5개 NLU 태스크 |
| **[LogicKor](https://github.com/instructkr/LogicKor)** | 한국어 논리 추론, LM-judge | MT-Bench 한국어 버전 |
| **[KoMT-Bench](https://github.com/dnotitia/KoMT-Bench)** | MT-Bench 한국어화 | 다중턴 한국어 대화 평가 |

### 9.2 한국어 데이터 합성 전략

**공개 한국어 데이터**:
- [KoAlpaca](https://github.com/Beomi/KoAlpaca): Self-Instruct 한국어화
- [LIMA-ko](https://huggingface.co/datasets/changpt/ko-lima-vicuna): LIMA 한국어 번역
- [OpenOrca-ko](https://huggingface.co/datasets/kyujinpy/KOR-OpenOrca-Platypus4): Orca 방식 한국어

**합성 전략 권장**:
1. **번역 + 검증**: 영어 고품질 데이터 → 한국어 번역 → 품질 필터링
2. **한국어 Magpie**: ChatML 기반 한국어 instruction 추출 (한국어 잘 하는 모델 필요)
3. **문화 특화**: KSAT(수능), 법령, 사회 상식 등 한국 특화 문제 합성
4. **코드스위칭**: 기술 용어는 영어, 설명은 한국어인 혼합 데이터

**주의사항**:
- 한국어 수학 표기(분수, 단위 등)와 영어 수학 표기 혼용 주의
- 경어법 일관성 (존댓말/반말 혼재 방지)
- 한자어 vs 순우리말 vs 영어 차용어 표기 표준화
- Tokenizer에서 한국어 효율: BPE 기반 tokenizer는 한국어를 영어보다 약 2~3배 더 많은 토큰으로 표현

### 9.3 한국어 모델 평가 시 주의사항

- **LogicKor LM-judge**: GPT-4o가 judge인데, 한국어 응답 품질 평가에서 언어 유창성 편향 있음
- **KMMLU 오염 위험**: KMMLU 문제 자체가 공개 웹에 있어 contamination 가능
- **HAE-RAE 문화 지식**: 한국 역사, 시조, 속담 등 문화 지식은 순수 번역으로 달성 어려움
- **다국어 모델 vs 한국어 전용**: Qwen3, LLaMA 3.1 같은 다국어 강화 모델이 한국어 전용 소형 모델보다 성능 좋아지는 추세

---

## §10 참고문헌

| 번호 | 논문/소스 | URL |
|---|---|---|
| 1 | InstructGPT (Ouyang et al., 2022) | [arxiv.org/abs/2203.02155](https://arxiv.org/abs/2203.02155) |
| 2 | LLaMA 2 (Touvron et al., 2023) | [arxiv.org/abs/2307.09288](https://arxiv.org/abs/2307.09288) |
| 3 | DPO (Rafailov et al., 2023) | [arxiv.org/abs/2305.18290](https://arxiv.org/abs/2305.18290) |
| 4 | Zephyr (Tunstall et al., 2023) | [arxiv.org/abs/2310.16944](https://arxiv.org/abs/2310.16944) |
| 5 | DeepSeek-Math (Shao et al., 2024) | [arxiv.org/abs/2402.03300](https://arxiv.org/abs/2402.03300) |
| 6 | DeepSeek-V3 (DeepSeek-AI, 2024) | [arxiv.org/abs/2412.19437](https://arxiv.org/abs/2412.19437) |
| 7 | DeepSeek-R1 (DeepSeek-AI, 2025) | [arxiv.org/abs/2501.12948](https://arxiv.org/abs/2501.12948) |
| 8 | Qwen2.5 Technical Report (2024) | [arxiv.org/abs/2412.15115](https://arxiv.org/abs/2412.15115) |
| 9 | Qwen3 Technical Report (2025) | [arxiv.org/abs/2505.09388](https://arxiv.org/abs/2505.09388) |
| 10 | Gemma 3 Technical Report (2025) | [arxiv.org/abs/2503.19786](https://arxiv.org/abs/2503.19786) |
| 11 | Tulu 3 (Lambert et al., 2024) | [arxiv.org/abs/2411.15124](https://arxiv.org/abs/2411.15124) |
| 12 | Phi-4 Technical Report (2024) | [arxiv.org/abs/2412.08905](https://arxiv.org/abs/2412.08905) |
| 13 | Nemotron-4 340B (2024) | [arxiv.org/abs/2406.11704](https://arxiv.org/abs/2406.11704) |
| 14 | WizardLM (Xu et al., 2023) | [arxiv.org/abs/2304.12244](https://arxiv.org/abs/2304.12244) |
| 15 | Orca (Mukherjee et al., 2023) | [arxiv.org/abs/2306.02707](https://arxiv.org/abs/2306.02707) |
| 16 | Self-Instruct (Wang et al., 2022) | [arxiv.org/abs/2212.10560](https://arxiv.org/abs/2212.10560) |
| 17 | Persona-Hub (Chan et al., 2024) | [arxiv.org/abs/2406.20094](https://arxiv.org/abs/2406.20094) |
| 18 | Magpie (Xu et al., 2024) | [arxiv.org/abs/2406.08464](https://arxiv.org/abs/2406.08464) |
| 19 | Self-Rewarding LM (Yuan et al., 2024) | [arxiv.org/abs/2401.10020](https://arxiv.org/abs/2401.10020) |
| 20 | Constitutional AI (Bai et al., 2022) | [arxiv.org/abs/2212.08073](https://arxiv.org/abs/2212.08073) |
| 21 | SimPO (Meng et al., 2024) | [arxiv.org/abs/2405.14734](https://arxiv.org/abs/2405.14734) |
| 22 | DAPO (Yu et al., 2025) | [arxiv.org/abs/2503.14476](https://arxiv.org/abs/2503.14476) |
| 23 | Math-Shepherd (Wang et al., 2024) | [arxiv.org/abs/2312.08935](https://arxiv.org/abs/2312.08935) |
| 24 | REINFORCE++ (2025) | [arxiv.org/abs/2501.03262](https://arxiv.org/abs/2501.03262) |
| 25 | AlpacaEval LC Win-Rate (2024) | [arxiv.org/abs/2404.04475](https://arxiv.org/abs/2404.04475) |
| 26 | Chatbot Arena (Zheng et al., 2023) | [arxiv.org/abs/2403.04132](https://arxiv.org/abs/2403.04132) |
| 27 | KMMLU (Ko et al., 2024) | [arxiv.org/abs/2402.11548](https://arxiv.org/abs/2402.11548) |
| 28 | HAE-RAE Bench (Son et al., 2023) | [arxiv.org/abs/2309.02706](https://arxiv.org/abs/2309.02706) |
| 29 | UltraFeedback (Cui et al., 2023) | [arxiv.org/abs/2310.01377](https://arxiv.org/abs/2310.01377) |
| 30 | SPIN (Chen et al., 2024) | [arxiv.org/abs/2401.01335](https://arxiv.org/abs/2401.01335) |
| 31 | S1 (Muennighoff et al., 2025) | [arxiv.org/abs/2501.17161](https://arxiv.org/abs/2501.17161) |
| 32 | Skywork-OR1 (2025) | [arxiv.org/abs/2505.22312](https://arxiv.org/abs/2505.22312) |
| 33 | OpenR1 (HuggingFace, 2025) | [huggingface.co/blog/open-r1](https://huggingface.co/blog/open-r1) |
| 34 | MetaMathQA (Yu et al., 2023) | [arxiv.org/abs/2309.12284](https://arxiv.org/abs/2309.12284) |
| 35 | IFEval (Zhou et al., 2023) | [arxiv.org/abs/2311.07911](https://arxiv.org/abs/2311.07911) |

---

*이 문서는 2026-05-08 기준으로 작성되었습니다. 모든 수치는 해당 기술 보고서에서 발췌했으며, 인용이 불확실한 경우 "approx" 표시를 했습니다.*

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. InstructGPT 논문의 가장 유명한 발견은 "1.3B InstructGPT가 175B GPT-3보다 인간 평가자에게 선호된다"는 것이었는데요. 이 결과가 시사하는 핵심 메시지는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 모델 파라미터 수보다 학습 방식(post-training, 즉 인간 피드백 기반 정렬)이 사용자 만족도에 훨씬 더 중요하다는 것.

**해설**: 100배 이상 작은 모델이 RLHF(SFT → RM → PPO) 파이프라인을 거치는 것만으로 거대 모델을 이겼거든요. 이게 현대 post-training 시대를 연 결정적 증거였고, 이후 모든 오픈 LLM이 SFT + preference 학습을 표준으로 채택하게 됐죠.

</details>

**Q2. OX 문제예요. "DPO는 PPO처럼 별도의 Reward Model을 먼저 학습한 뒤, 그 RM 신호로 정책을 최적화한다." 맞을까요, 틀릴까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X (틀렸어요)

**해설**: DPO의 핵심이 바로 RM 학습 단계를 없앤 거예요. 최적 정책과 reward function 사이의 closed-form 관계를 이용해서, preference pair(선호/비선호 응답 쌍)만으로 단일 분류 손실을 통해 정책을 직접 최적화하죠. 그래서 RM→PPO 2단계가 필요한 RLHF보다 학습이 훨씬 간단하고 안정적이에요.

</details>

**Q3. GRPO가 PPO와 구조적으로 가장 크게 다른 점은 뭐고, 그 덕분에 얻는 실질적 이득은 뭔가요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Value network(critic)를 제거하고, 같은 프롬프트에 대한 G개 응답 그룹의 평균/표준편차를 baseline으로 사용해요. 덕분에 GPU 메모리를 40~60% 절약하고 critic bias 문제도 없어지죠.

**해설**: PPO는 policy와 비슷한 크기의 value network를 따로 둬서 기댓값을 추정하는데요, GRPO는 그룹 내 reward를 정규화한 값을 advantage로 바로 쓰기 때문에 그 네트워크 자체가 필요 없어요. 수학/코딩처럼 rule-based reward가 있는 도메인에서 특히 강력해서 DeepSeek-R1, Qwen3 등이 채택했죠.

</details>

**Q4. DeepSeek-R1-Zero와 DeepSeek-R1의 학습 파이프라인은 어떻게 다른가요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: R1-Zero는 SFT 없이 베이스 모델에 rule-based reward만으로 GRPO를 바로 적용한 순수 RL이고, R1은 cold-start SFT → Reasoning RL → Rejection Sampling SFT → General RL의 4단계 파이프라인이에요.

**해설**: R1-Zero는 "SFT 없이도 순수 RL만으로 chain-of-thought와 self-reflection이 창발한다"는 걸 보여준 실험적 증명이었는데요, 가독성 문제 등이 있어서 실제 제품 모델인 R1은 수천 개의 long CoT 데이터로 cold-start를 한 뒤 다단계로 다듬었죠. 이 레시피를 Qwen3, Sky-T1 같은 후속 reasoning 모델들이 따라가고 있어요.

</details>

**Q5. ORM(Outcome Reward Model)과 PRM(Process Reward Model)의 차이를 구분해 보세요. 각각의 장단점은 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: ORM은 최종 답만 평가(정답/오답)하고, PRM은 추론의 각 단계마다 점수를 부여해요. ORM은 구현이 간단하고 데이터 수집이 쉽지만 중간 오류를 못 잡고, PRM은 오류를 조기에 감지하고 세밀한 피드백을 주지만 단계별 레이블링 비용이 높죠.

**해설**: PRM의 레이블링 비용 문제를 풀려고 Math-Shepherd는 MCTS 기반으로 step-level 레이블을 자동 생성했어요. 수학 추론처럼 긴 풀이 과정이 있는 태스크에서는 "어디서 틀렸는지"를 아는 PRM이 더 정밀한 학습 신호를 주는 거죠.

</details>

**Q6. 응용 시나리오예요. 수학과 코딩 성능을 끌어올리는 RL을 하려는데, reward model이 자꾸 hacking당하는 게 걱정이에요. 본문에서 소개한 접근 중 어떤 걸 쓰는 게 좋고, 왜 그럴까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: RLVR(또는 rule-based reward 기반 GRPO)을 쓰는 게 좋아요. 수학은 정답 검증, 코드는 테스트 실행처럼 외부 verifier를 reward로 직접 사용하면 reward hacking을 원천 차단할 수 있거든요.

**해설**: 신경망 RM은 모델이 RM의 약점을 파고드는 hacking에 취약한데요, "테스트를 통과했는가"처럼 검증 가능한 신호는 속일 방법 자체가 없죠. Tulu 3가 RLVR로 math/coding 성능을 크게 올렸고, DeepSeek-R1도 accuracy + format의 rule-based reward만으로 학습했어요.

</details>

**Q7. Self-Instruct, Evol-Instruct, Magpie는 모두 instruction 데이터를 합성하는 방법인데요. 세 방법의 핵심 아이디어를 각각 한 줄로 구분해 보세요.**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Self-Instruct는 175개의 인간 작성 seed에서 출발해 LLM이 새 instruction을 생성·필터링하는 방식, Evol-Instruct는 기존 instruction을 더 복잡하게(in-depth) 또는 더 다양하게(in-breadth) 진화시키는 방식, Magpie는 seed prompt 없이 chat template의 앞부분만 입력해서 정렬된 LLM이 user query를 스스로 완성하게 하는 방식이에요.

**해설**: 세 방법은 "시작점"이 다른 게 포인트인데요. Self-Instruct는 사람이 만든 seed가 필요하고, Evol-Instruct는 기존 데이터를 변형하고, Magpie는 아예 아무것도 없이 모델 안에 학습된 분포에서 query를 뽑아내죠. Self-Instruct의 한계(반복 패턴, 쉬운 instruction 편향)를 후속 방법들이 보완해 온 흐름이에요.

</details>

**Q8. LM-judge 기반 평가(MT-Bench, AlpacaEval 등)에는 여러 편향이 있다고 했는데요. 본문에서 소개한 대표적 편향을 두 가지 이상 들고, 완화 방법도 하나 말해 보세요.**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Length bias(긴 응답 선호), Position bias(먼저 나온 응답 선호), Sycophancy(judge와 같은 제조사 모델에 유리) 등이 있어요. 완화 방법으로는 AlpacaEval 2.0의 LC(Length-Controlled) win-rate처럼 길이 효과를 통제하거나, 여러 judge로 병행 평가하는 게 있죠.

**해설**: 심지어 구조화된 일정 응답만으로 86.5% LC win-rate를 뚫은 null model 공격 사례도 있을 만큼 judge 평가는 취약한데요. 그래서 단일 LM-judge 점수만 믿지 말고 Chatbot Arena 같은 인간 평가나 IFEval 같은 규칙 기반 검증을 함께 보는 게 안전해요.

</details>
