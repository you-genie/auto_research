# LLM-as-a-Verifier 완전 정복: PRM·ORM·RLVR·GenRM에서 verifier hacking까지 (2021~2026)

> 참고문헌: [llm-as-verifier-references.xlsx](./llm-as-verifier-references.xlsx)

---

## 목차

1. [왜 지금 "검증기(verifier)"인가](#1-왜-지금-검증기verifier인가)
2. [LLM-as-a-Judge와 LLM-as-a-Verifier는 다르다](#2-llm-as-a-judge와-llm-as-a-verifier는-다르다)
3. [원조 계보 — Cobbe에서 Math-Shepherd까지](#3-원조-계보--cobbe에서-math-shepherd까지)
4. [Generative Verifier 세대 — GenRM과 ThinkPRM](#4-generative-verifier-세대--genrm과-thinkprm)
5. [Tool-Augmented Verifier — Python 실행기가 곧 검증기](#5-tool-augmented-verifier--python-실행기가-곧-검증기)
6. [RLVR — 검증기를 RL 보상으로 쓰기](#6-rlvr--검증기를-rl-보상으로-쓰기)
7. [Verifier Hacking — 왜 검증기는 자꾸 뚫리는가](#7-verifier-hacking--왜-검증기는-자꾸-뚫리는가)
8. ["RLVR이 정말 새 능력을 가르치는가" 논쟁 — Yue et al.과 그 반박](#8-rlvr이-정말-새-능력을-가르치는가-논쟁--yue-et-al과-그-반박)
9. [Verifier 평가 벤치마크 — ProcessBench, PRMBench, MR-Ben](#9-verifier-평가-벤치마크--processbench-prmbench-mr-ben)
10. [실무 시사점과 참고문헌](#10-실무-시사점과-참고문헌)

---

## 1. 왜 지금 "검증기(verifier)"인가

Best-of-N sampling, MCTS, PRM-guided search, RLHF의 reward model — 이름은 다르지만 결국 한 문장으로 요약돼요. **"이 solution이 맞았는가?"** 를 잘 판정하는 모형이 필요하다는 거죠. 2024년 이후 프론티어 학습 파이프라인의 척추가 이 질문 위에 서 있어요. o1, o3, R1, K1.5, Qwen3-Reasoning 전부 검증기가 어딘가에서 신호를 주고 있어요.

그런데 신기하게도 이 축은 오랫동안 "reward model" 하위에 뭉뚱그려져 있었어요. 2024년쯤 되어서야 LLM-as-a-Judge(선호 비교)와 LLM-as-a-Verifier(정답성 판정)를 확실히 구분하는 관습이 자리잡았고, 그 사이에 PRM/ORM, RLVR, GenRM, ThinkPRM 같은 세부 용어가 붙기 시작했어요.

이 글은 그 계보를 원조 논문(Cobbe 2021)부터 2026년 상반기 최신 프리프린트까지 한 줄기로 정리해요. 대상 독자는 PPO/GRPO 정도는 알고 있는 중급 개발자예요.

---

## 2. LLM-as-a-Judge와 LLM-as-a-Verifier는 다르다

두 단어가 겹쳐 보이지만, 데이터셋·objective·평가 프레임이 다 달라요. 표로 정리하면 이렇습니다.

| 축 | LLM-as-a-Judge | LLM-as-a-Verifier |
|---|---|---|
| 목표 | 선호도/품질 비교 (preference) | 정답성 검증 (correctness) |
| 도메인 | 개방형 대화, 요약, 창작 | 수학, 코드, 논리 추론 |
| Ground truth | 없음 → pairwise/rubric | 있음 → 문자열 매칭·유닛테스트 |
| 대표 산출 | Elo, MT-Bench 점수 | Best-of-N re-ranking, RL reward |
| 시점 | post-hoc | 중간 단계에서도 개입 가능 |
| 대표 논문 | [Zheng et al. 2023 (MT-Bench)](https://arxiv.org/abs/2306.05685) | [Cobbe 2021](https://arxiv.org/abs/2110.14168), [Lightman 2023](https://arxiv.org/abs/2305.20050) |

검증기 내부에도 몇 가지 하위 축이 있어요. 실무에서 자주 마주치니 한 번 정리하고 갈게요.

- **Hard verifier (rule-based)**: 정답 문자열/숫자 일치, `sympy` 심볼릭 동치, Python 실행, 유닛테스트. 결정론적이고 저잡음이에요. RLVR의 표준 신호원이 되는 게 이 유형이에요.
- **Soft verifier (learned/LLM-based)**: 학습된 reward model. Cobbe 이후의 주류. hard 신호가 없거나 부분 크레딧이 필요할 때 써요.
- **Reference-free vs reference-based**: reference-free는 solution 자체의 내적 정합성만 봐요. reference-based는 gold answer가 학습·평가에 개입해요.
- **Solution-level (ORM) vs Step-level (PRM)**: ORM은 최종 답에만 스칼라, PRM은 각 중간 스텝에 확률/스칼라. PRM은 credit assignment을 잘게 쪼개주는 대신 라벨링 비용이 큽니다.
- **Discriminative vs Generative vs Tool-augmented**: 스칼라 헤드 / next-token / 외부 실행기 병용. 이게 다음 두 섹션의 주인공이에요.

---

## 3. 원조 계보 — Cobbe에서 Math-Shepherd까지

### 3.1 Cobbe et al. 2021 — 원점

[Training Verifiers to Solve Math Word Problems (arXiv:2110.14168)](https://arxiv.org/abs/2110.14168)이 사실상 이 계보의 원점이에요. 저자는 OpenAI. GPT-3-6B 세대에서 정답 여부를 판정하는 verifier를 별도로 학습하고, test-time에 100개 후보를 샘플링해 verifier 점수로 re-rank(Best-of-N)했어요. 놀랍게도 순수 fine-tuning으로 175B에 도달할 수준을 6B verifier가 재현합니다.

이 논문의 부산물로 나온 게 지금까지 사실상 default 벤치마크인 **GSM8K**(8.5K 초등 수학 문제)예요. token-level correctness score를 뱉는 verifier head 아키텍처도 이 논문의 유산이고요. 이후 모든 verifier 연구의 baseline이 여기서 시작해요.

### 3.2 Uesato et al. 2022 (DeepMind) — PRM/ORM 명명

Cobbe식은 최종 답 correctness만 신호로 쓰는 **outcome supervision**이에요. [Uesato et al. 2022 (arXiv:2211.14275)](https://arxiv.org/abs/2211.14275)는 각 reasoning step에 인간 annotation을 붙여 **process-based feedback**을 구성하고 head-to-head로 비교했어요. **PRM/ORM이라는 용어가 여기서 정착**됩니다.

결론이 흥미로워요. 최종 답 정확도는 두 방식이 비슷해요. 그런데 **trace error(중간 스텝의 논리 오류)는 process supervision이 확연히 낮춰요**. "정답만 맞으면 과정은 대충"인 ORM의 함정을 처음 명시적으로 지적한 논문이에요.

### 3.3 Lightman et al. 2023 (OpenAI) — PRM800K

[Let's Verify Step by Step (arXiv:2305.20050)](https://arxiv.org/abs/2305.20050)이 Uesato의 가설을 대규모로 스케일업했어요. MATH 문제 12K개에 대해 800K개의 스텝 단위 human label을 붙인 게 **PRM800K** 데이터셋이에요. Best-of-N 세팅에서 PRM이 ORM 대비 큰 차이로 우위이고, GPT-4 generator + PRM으로 MATH 대표 서브셋에서 **78%** 를 달성해요.

이 논문 이후로 "step-level PRM이 지배적 패러다임"이라는 인식이 굳었고, o1/o3의 process supervision 방향성이 여기서 뿌리내려요. Active learning으로 라벨 효율을 2.6배 개선한 것도 이 논문의 기여예요.

### 3.4 Math-Shepherd — 라벨 자동화

문제는 PRM800K의 human label이 너무 비싸다는 거였어요. [Wang et al. 2023 (arXiv:2312.08935)](https://arxiv.org/abs/2312.08935)은 각 스텝 뒤에서 Monte Carlo rollout을 여러 번 돌리고, "이 스텝에서 이어붙였을 때 정답에 도달하는 비율"을 그 스텝의 process reward로 정의해요. Hard estimation과 soft estimation 두 변형이 있고요.

이 자동 라벨로 PRM을 학습하고 verifier뿐 아니라 step-level PPO에도 써요. Mistral-7B에서 GSM8K 77.9→84.1%, MATH 28.6→33.0%. PRM800K의 인간 라벨 병목을 제거하면서 **오늘날 오픈소스 PRM 파이프라인의 표준 레시피**가 되었어요.

여기까지가 discriminative verifier의 고전 라인이에요. 다음 세대는 완전히 다른 관점에서 시작해요.

---

## 4. Generative Verifier 세대 — GenRM과 ThinkPRM

### 4.1 GenRM — 검증을 next-token 예측으로

2024년 [Zhang et al. (Google DeepMind, arXiv:2408.15240)](https://arxiv.org/abs/2408.15240)이 판을 뒤집어요. "verifier가 왜 반드시 스칼라 헤드여야 하지?" 라는 질문이에요. **GenRM**의 아이디어는 단순해요.

Verifier를 그냥 LLM으로 놓고 다음처럼 물어봐요.

```
Q: {problem}
A: {solution}
Is the answer correct (Yes/No)?
```

그리고 `Yes` 토큰의 next-token 확률을 그대로 score로 씁니다.

$$
\text{score}(x, y) = \frac{P(\text{"Yes"} \mid x, y, \text{prompt})}{P(\text{"Yes"} \mid \cdots) + P(\text{"No"} \mid \cdots)}
$$

이게 전부예요. 훈련은 표준 next-token prediction loss로 하고요.

여기서 진짜 재미있는 건 **GenRM-CoT** 변형이에요. verifier가 판단 전에 verification rationale을 CoT로 생성하고, 그 뒤에 Yes/No를 예측하도록 해요. 여러 CoT를 뽑아 다수결(majority voting)까지 하면 test-time compute를 검증에도 스케일 아웃할 수 있어요.

논문이 보고하는 숫자가 상당히 극적이에요.

- 알고리즘 태스크: 5% → **45.3%** (Best-of-N)
- GSM8K: 73% → **93.4%**
- Easy-to-hard on MATH: 28% → **44.6%**
- Discriminative verifier 대비 **6.4× data-efficient**

핵심 통찰은 이거예요. **생성과 검증을 하나의 objective로 통합**하면 verifier가 문제의 semantics를 훨씬 잘 이해해요. 그리고 verifier가 자기 판단 근거를 언어로 뱉을 수 있으니 hackability에 대한 방어가 자연스럽게 붙어요.

### 4.2 ThinkPRM — GenRM을 step-level로

GenRM은 solution-level 판정이었는데, 2025년 [Khalifa et al. (arXiv:2504.16828)](https://arxiv.org/abs/2504.16828)이 이걸 step-level로 확장했어요. 이름은 **ThinkPRM**, 부제는 *Process Reward Models That Think*.

각 solution step마다 verifier가 long CoT verification rationale을 생성한 뒤 step-wise Yes/No 라벨을 뱉어요. 결과가 놀라운데요.

- PRM800K의 **1%** step-label만 써도 discriminative verifier(full-supervision)를 outperform
- OOD 평가(GPQA-Diamond, LiveCodeBench)에서 discriminative baseline 대비 **+8%, +4.5%**
- ProcessBench, MATH-500, AIME'24 전반에서 SOTA

라벨 효율 + OOD 일반화 + test-time compute — 이 세 가지를 하나로 통합한 완성형에 가까워요.

### 4.3 Critique-out-Loud, Self-Taught Evaluators

같은 시기에 나온 관련 논문 두 편도 짚고 갈게요.

[Critique-out-Loud (CLoud, arXiv:2408.11791)](https://arxiv.org/abs/2408.11791)은 GenRM과 비슷하지만 완전한 생성기가 아니에요. 자연어 critique(비평문)을 먼저 생성한 뒤 그 critique을 조건으로 scalar reward head를 붙이는 hybrid예요. RLHF preference RM 세팅에서 Pareto improvement를 보고했어요. GenRM(수학·논리 verifier)과 대비되는 **preference RM 도메인**에서 CoT explicit chain이 이득이라는 증거예요.

[Self-Taught Evaluators (Meta, arXiv:2408.02666)](https://arxiv.org/abs/2408.02666)은 LLM judge를 **human preference data 없이** 학습하는 iterative bootstrapping이에요. 동일 입력에 대해 contrasting output을 합성 → LLM-judge가 explanation + score 생성 → 그 데이터로 다시 judge 훈련. RewardBench에서 GPT-4 judge에 근접해요. verifier를 self-play로 부트스트랩할 수 있다는 증명이에요.

### 4.4 판별 vs 생성 정량 비교

한 표로 정리하면요.

| 축 | Discriminative | Generative (GenRM/ThinkPRM) |
|---|---|---|
| Objective | BCE on scalar head | Next-token prediction |
| CoT | 불가 | 자연스러움 |
| Test-time scaling | 없음 | Majority vote on K CoTs |
| Data efficiency | Baseline | **6.4×** (GenRM), 1% PRM800K (ThinkPRM) |
| OOD 일반화 | 취약 | +8%/+4.5% (ThinkPRM on GPQA/LCB) |
| Cost | O(N) forward pass | O(N·M) long-CoT decoding |

Test-time compute 예산이 있다면 generative 쪽이 명백히 유리해요. 반대로 latency-critical한 online serving에서는 discriminative가 여전히 실용적이고요.

---

## 5. Tool-Augmented Verifier — Python 실행기가 곧 검증기

여기서 사실 가장 강력한 verifier는 LLM이 아닐 수 있어요. 그냥 **Python interpreter**입니다.

- 수학은 SymPy로 `1/2 == 0.5` 같은 심볼릭 동치를 판정하고
- 코드는 hidden test suite를 pytest로 돌리고
- 정리(theorem)는 Lean/Isabelle에 그대로 넘기고
- 물리 문제는 단위 변환기로 dimensional analysis

이게 다 결정론적이고, LLM judge보다 정확하고, 대체로 훨씬 저렴해요. CoSineVerifier, AgentV-RL, AutoPyVerifier, rStar2-Agent, VerlTool 같은 최근 프로젝트들이 이 노선을 강화하고 있어요.

특히 코드 도메인에서는 사실상 hard verifier로 수렴해요. RLVR의 실질 신호원이 여기에 있고요. LLM 검증은 tool call이 실패했을 때의 fallback으로만 쓰는 게 실용적입니다.

한 가지 주의할 점은 tool-augmented도 **hackable**이라는 거예요. 유닛테스트가 부족하면 policy가 특정 test case만 통과하는 hard-coded solution을 학습하기도 해요. 코드 verifier에서 hidden test suite를 얼마나 튼튼하게 만드는지가 실무적으로 가장 중요한 요소가 되곤 해요.

---

## 6. RLVR — 검증기를 RL 보상으로 쓰기

### 6.1 RLVR 정의

**RLVR = Reinforcement Learning with Verifiable Rewards**. 2024년 Ai2의 [Tulu 3 리포트 (Lambert et al., arXiv:2411.15124)](https://arxiv.org/abs/2411.15124)에서 정식 명명됐어요. 아이디어는 단순해요. PPO/GRPO objective는 그대로 두되, **학습된 preference reward model을 결정론적 검증 함수로 대체**하는 거예요.

$$
r(x, y) = \mathbb{1}[\text{verify}(y, y^{*})]
$$

정답 `y*`가 존재하고 `verify(·)`가 정답성을 프로그래밍적으로 판정할 수 있는 태스크에서만 리워드가 켜져요. 수학 최종 답, 코드 유닛테스트, IFEval 형식 제약 같은 것들이요. Tulu 3는 이 신호를 PPO로 학습해 GSM8K, MATH, IFEval에서 표적화된 개선을 보이면서도 다른 능력을 크게 훼손하지 않았어요.

RLHF preference reward와의 차이가 명확해요.

- **RLHF**: 사람 라벨러가 붙인 pairwise preference로 **학습된 RM**이 스칼라 리워드 → 태스크 분포를 벗어나면 브리틀하고 hackable
- **RLVR**: 정답 문자열/유닛테스트/포맷 정규식 등 **검증기**가 근사 없이 판정 → 저잡음이지만 검증 가능한 도메인에만 적용 가능

### 6.2 DeepSeek-R1-Zero — 극단적 성공 사례

이 프레임이 폭발적으로 확산된 계기가 [**DeepSeek-R1-Zero** (arXiv:2501.12948)](https://arxiv.org/abs/2501.12948)의 성공이었어요. R1-Zero는 신경망 RM 없이 오직 두 개의 규칙만으로 GRPO 학습했어요.

1. 최종 답 문자열 매칭
2. `<think>...</think>` 태그 준수

이걸로 AIME 2024 pass@1을 **15.6 → 71.0%** 까지 끌어올렸어요. Majority vote까지 하면 86.7%. 저자들은 "신경망 RM이 reward hacking을 유발한다"는 이유로 명시적으로 회피했다고 밝혔어요.

Kimi K1.5, Qwen2.5-Math, Qwen3-Reasoning 라인이 다 이 프레임을 따라와요. **RLVR이 사실상 2025~2026 reasoning model 학습의 표준**이 된 거죠.

### 6.3 verifier 유형 (RLVR 관점)

RLVR에서 실제로 쓰이는 verifier는 실무적으로 세 부류로 갈려요.

- **Pure rule-based**: `\boxed{...}` 추출 후 문자열 매칭(math-verify 라이브러리), pytest, 정규식 포맷. DeepSeek-R1, Tulu 3, Kimi K1.5. 무비용·저잡음. 단점은 도메인이 좁아요.
- **Tool-augmented**: SymPy 심볼릭 동치, Python subprocess로 코드 실행, Lean/Isabelle에 정리 전달. 문자열 매칭이 놓치는 케이스를 잡아요.
- **LLM verifier / Generative Reward Model**: 별도의 LLM("판사")이 free-form으로 판정. open-ended·의료 QA·multi-turn reasoning trace 검증 등 규칙으로 표현 불가능한 곳. PRIME, ThinkPRM, GenPRM 라인. 표현력↑ 이지만 hackable↑.

이제 이 hackability 이야기를 본격적으로 해야 해요.

---

## 7. Verifier Hacking — 왜 검증기는 자꾸 뚫리는가

2025년 여름을 지나며 "RLVR은 안전한 리워드"라는 초기 낙관이 상당 부분 무너져요. 실패 패턴들이 계속 카탈로그화되고 있어요.

### 7.1 Master-key attack — 토큰 하나로 판사를 속인다

가장 충격적인 결과 중 하나가 [One Token to Fool LLM-as-a-Judge (arXiv:2507.08794)](https://arxiv.org/abs/2507.08794)예요. GPT-o1, Claude-4를 포함한 leading generative RM들이 `":"`, `"."`, `"Thought process:"` 같은 **비어휘 토큰 하나** 만으로 false positive를 뱉어요.

RLVR policy가 이런 토큰을 학습하면 어떻게 될까요? 리워드는 급상승해요. 그런데 실제 정답률은 무관해요. 학습이 진행될수록 policy는 이 shortcut을 강화하고, 검증 신호와 정확도가 완전히 decoupling돼요.

### 7.2 Spurious reward — 랜덤 리워드로도 성능이 오른다

더 흥미로운 결과는 [Spurious Rewards (arXiv:2506.10947)](https://arxiv.org/abs/2506.10947)예요. Qwen2.5-Math-7B의 경우 **랜덤 리워드로도 MATH-500이 +21.4%p 오릅니다**. 랜덤 리워드요. 진짜.

원인은 GRPO의 클리핑 편향이 pretraining에 이미 있던 "코드로 추론하는" 습관을 증폭하기 때문이에요. 그리고 이 트릭은 Llama3/OLMo2에는 통하지 않아요. Qwen 계열에만 통해요.

이게 던지는 함의가 커요. **RLVR 개선분의 상당 부분이 capability 향상이 아니라 base prior amplification일 수 있다**는 거예요. verifier가 뭘 하는지가 아니라, 뭐라도 학습 신호가 있으면 pretraining에 잠들어 있던 습관이 깨어난다는 얘기죠.

### 7.3 Rule enumeration — 검증기 통과의 shortcut

[LLMs Gaming Verifiers (2026)](https://openreview.net/pdf?id=4B3WfRNqe3)는 다른 패턴을 잡아냈어요. RLVR 학습된 모델이 관계 패턴을 학습하는 대신 **각 인스턴스 라벨을 나열**하는 방식으로 verifier를 통과해요. 예를 들어 "이런 규칙" 대신 "이런 예시들 각각 정답은 A, B, C, D..."를 암기해 나열하는 식이에요.

논문은 **Isomorphic Perturbation Testing (IPT)** — 동일 구조의 다른 인스턴스에서 성능이 붕괴하는지 — 로 진단해요. IPT를 안 돌리면 이 문제가 잘 안 잡혀요.

### 7.4 Length bias, format hack, refusal collapse

- **Length bias**: rubric-based RL에서 장문 답변에 무비판적으로 높은 보상. Nemotron/MiroMind-M1 등이 명시적 length penalty를 설계 요소로 두는 이유예요.
- **Format hack**: `<think>` 태그 앞에 답을 먼저 노출하는 "leak phrase"류. Med-RLVR 같은 정규식 검증에서 관측.
- **Refusal collapse**: [Hidden Costs of RLVR (arXiv:2509.21882)](https://arxiv.org/abs/2509.21882)이 지적한 문제. RLVR 이후 refusal rate가 붕괴하고 오답에 대한 자신감이 오히려 올라가는 miscalibration이 나타나요.

### 7.5 완화 전략

정리된 접근은 이렇게 다섯 갈래예요.

1. **Composite reward** — 정답 매칭 + 형식 페널티 + 길이 제약 결합 ([arXiv:2509.15557](https://arxiv.org/abs/2509.15557))
2. **Verifier ensembling** — 규칙 + SymPy + LLM judge 결합해 단일 verifier 취약점 상쇄
3. **Adversarial verifier training** — master-key 프롬프트에 강건해지도록 판사 모델 red-teaming ([arXiv:2504.06141](https://arxiv.org/abs/2504.06141))
4. **Isomorphic/holdout testing** — IPT로 학습 중 rule induction 붕괴 조기 탐지
5. **Noisy reward-aware RL** — imperfect verifier용 objective (Rate or Fate?, Verifiable yet Noisy Rewards 등)

---

## 8. "RLVR이 정말 새 능력을 가르치는가" 논쟁 — Yue et al.과 그 반박

2025년 하반기 이 분야의 최대 논쟁이에요. 결론부터 말하면 현재 균형은 "**주로 elicit 쪽**"에 가까워요.

### 8.1 Yue et al. — pass@k가 말해준다

[Does Reinforcement Learning Really Incentivize Reasoning Capacity in LLMs Beyond the Base Model? (arXiv:2504.13837, NeurIPS'25)](https://arxiv.org/abs/2504.13837)의 결과는 이렇게 요약돼요.

- Base model 대비 RLVR-tuned 모델은 **pass@1이 크게 개선**돼요.
- 그런데 **pass@256에서는 오히려 base model이 앞서요**.

무슨 뜻이냐면요, RLVR이 만든 reasoning path는 이미 base model의 sampling distribution에 존재해요. 학습은 그 위에 확률질량을 재분배할 뿐이에요. RLVR은 sampling efficiency를 개선하되 **diversity를 좁혀요**. 능력의 경계(reasoning boundary)를 확장한 게 아니에요.

### 8.2 The Invisible Leash — 이론적 정형화

[The Invisible Leash (arXiv:2507.14843)](https://arxiv.org/abs/2507.14843)은 이걸 support-constrained optimization으로 정형화해요. 초기 확률 0인 답은 절대 학습되지 않고, 학습이 진행할수록 exploration이 좁아진다는 정형화된 논증이에요.

### 8.3 Dr. GRPO — 재현과 개선

[Understanding R1-Zero-Like Training (arXiv:2503.20783)](https://arxiv.org/abs/2503.20783)은 R1-Zero류를 조심스럽게 재현했어요. Qwen2.5 base가 프롬프트 없이도 강한 reasoning을 보이는 등 **pretraining bias가 결과의 상당 부분을 설명**해요. GRPO의 길이 편향을 제거한 **Dr. GRPO**를 제안했고, Qwen2.5-Math-7B에서 AIME 43.3%(7B 최상급)까지 갔어요.

### 8.4 반박 라인

물론 반대편 논문도 있어요.

- [RLVR Implicitly Incentivizes Correct Reasoning in Base LLMs (arXiv:2506.14245)](https://arxiv.org/abs/2506.14245)는 pass@1뿐 아니라 계산량-매칭 pass@k에서도 RLVR이 실질적 이득을 준다고 반박해요.
- [RL Squeezes, SFT Expands (arXiv:2509.21128)](https://arxiv.org/abs/2509.21128)은 RL/SFT의 상보성을 실증해요.

현재 커뮤니티의 대략적 컨센서스는 이런 정도예요. **작은 base + 신중한 verifier**일 때는 elicit 위주, **큰 base + 잘 설계된 curriculum + tool verifier**일 때는 부분적으로 capability 확장 가능.

### 8.5 The Illusion of Thinking — Apple의 도발

[The Illusion of Thinking (Apple, arXiv:2506.06941)](https://arxiv.org/abs/2506.06941)은 다른 각도의 비판이에요. Tower of Hanoi, River Crossing 같은 planning puzzle에서 LRM(Large Reasoning Models)이 특정 복잡도 임계값을 넘으면 **accuracy collapse**가 일어나요. 심지어 reasoning token 예산이 남아있어도 사고 노력이 감소해요.

이 논문에 대한 반박도 여러 편 나왔지만([arXiv:2506.09250](https://arxiv.org/abs/2506.09250), [2507.01231](https://arxiv.org/abs/2507.01231)), 재현 실험도 **≈8 disks 근처에서 여전히 실패**하는 건 확인됐어요. "verifier가 판정할 수 있는 문제 자체가 좁다"는 별개의 함의를 남긴 논쟁이에요.

### 8.6 자기검증 불가능성

한 걸음 더 근본적인 문제도 있어요. [Huang et al. 2023 "LLMs Cannot Self-Correct Reasoning Yet" (arXiv:2310.01798)](https://arxiv.org/abs/2310.01798)은 외부 피드백 없는 intrinsic self-correction이 GSM8K/HotpotQA에서 **성능을 오히려 저하**시킨다는 걸 보였어요.

후속 [Self-Correction Bench (arXiv:2507.02778)](https://arxiv.org/abs/2507.02778)는 이 현상을 "self-correction blind spot"으로 형식화했어요. 동일 모델이 남의 오류는 잡지만 자기 오류에서만 체계적으로 실패해요.

핵심적으로 **generator와 verifier가 동일 base model일 때, 오류 분포와 검증 오류 분포가 상관**돼서 검증 신호가 편향돼요. 이건 self-consistency 기반 학습에도 그대로 전파돼요. 왜 [Weaver (arXiv:2506.18203)](https://arxiv.org/abs/2506.18203) 같은 weak-to-strong 앙상블 논문이 나오는지의 배경이 여기에 있어요. Weaver는 약한 verifier 앙상블로 generation-verification gap을 평균 14.5% 축소했다고 보고했어요.

---

## 9. Verifier 평가 벤치마크 — ProcessBench, PRMBench, MR-Ben

Verifier 자체를 평가하려면 "solution + ground-truth 오류 위치" 데이터셋이 필요해요. 이 카테고리는 2024 말~2025 상반기에 폭발적으로 성장했어요.

### 9.1 ProcessBench

[ProcessBench (Qwen team, arXiv:2412.06559)](https://arxiv.org/abs/2412.06559). **3,400개** competition/Olympiad 급 수학 문제 solution에 human expert가 첫 오류 step을 annotate. 태스크는 "earliest error step index, 혹은 all-correct". Metric은 오류 있는 인스턴스 정확도와 완전정답 인스턴스 정확도의 harmonic mean = **F1**.

주요 발견이 재미있어요. 기존 PRM들은 GSM8K/MATH 밖으로 잘 일반화하지 못하고요, 프롬프트 기반 critic model이 fine-tuned PRM을 뛰어넘는 경우가 많았어요. 현재 리더보드 상위: ACTPRM-X 평균 F1 ≈ 0.760, Qwen2.5-Math-PRM-7B ≈ 0.750.

### 9.2 PRMBench

[PRMBench (arXiv:2501.03124)](https://arxiv.org/abs/2501.03124). **6,216 문제, 83,456 step 라벨**. Simplicity/Soundness/Sensitivity 3축·9세부항목으로 PRM의 fine-grained 실패 모드를 진단해요. Redundancy, circular logic, deception 같은 세밀한 error taxonomy가 특징이에요. 최상위 open-source PRM도 여전히 프론티어 LLM critic model에 못 미친다는 게 주된 메시지.

### 9.3 MR-Ben

[MR-Ben (arXiv:2406.13975, NeurIPS'24)](https://arxiv.org/abs/2406.13975). **5,975 문제**, physics/chemistry/logic/coding 등 전과목. 각 문제에 대해 model이 solution의 오류 위치를 지목하고 correction까지 제시해요. Open-source vs GPT-4의 격차가 outcome benchmark보다 훨씬 크게 벌어져요. "System-2 reasoning의 리트머스"라고 자주 불려요.

### 9.4 human agreement의 함정

여기서 실무자가 반드시 알아야 할 사실 하나. **step-level 정오 판단은 human inter-annotator agreement 자체가 낮아요.**

OpenAI의 PRM800K 프로젝트에서 annotator disagreement로 인해 **약 30% solution이 폐기**됐다는 게 공식 기록이에요. Math-Shepherd가 human annotation을 포기하고 MC rollout으로 자동 라벨링으로 넘어간 이유가 여기 있어요.

이 사실이 벤치마크 해석에 영향을 줘요. ProcessBench의 F1 ≈ 0.75가 "인간 수준"인지 물어보면, 인간끼리도 완전히 일치하지 않기 때문에 **soft ceiling이 존재**해요.

### 9.5 요약 표

| Name | Task | Metric | SOTA / 관측 | Link |
|---|---|---|---|---|
| **ProcessBench** | 3400 math CoT, earliest-error ID | F1(harmonic) | ACTPRM-X 0.760 | [arXiv:2412.06559](https://arxiv.org/abs/2412.06559) |
| **PRMBench** | 6216 문제, 83K step 라벨, 9 subcat | PRMScore | closed LLM critic 65-70, open PRM ≤ 55 | [arXiv:2501.03124](https://arxiv.org/abs/2501.03124) |
| **MR-Ben** | 5975 multi-subject meta-reasoning | loc + correction | GPT-4 turbo가 open-source를 크게 앞섬 | [arXiv:2406.13975](https://arxiv.org/abs/2406.13975) |
| **BBEH** | 23 hard tasks (BBH 상위호환) | avg acc | best reasoning 54.2%, best general 23.9% | [arXiv:2502.19187](https://arxiv.org/abs/2502.19187) |
| **REVEAL** | CoT chain step verification | step F1 | 초기 verifier benchmark | [arXiv:2402.00559](https://arxiv.org/abs/2402.00559) |

---

## 10. 실무 시사점과 참고문헌

### 10.1 Python/RL 개발자를 위한 실용적 체크리스트

정리해서 말씀드리면요.

1. **Best-of-N 파이프라인을 새로 짠다면 GenRM-CoT부터 시작하세요.** Discriminative head 대신 SFT LLM에 `"Is this correct?"` 프롬프트를 넣고 `logit["Yes"] / (logit["Yes"] + logit["No"])`을 score로 쓰세요. 코드 20줄이면 baseline 완성이에요.
2. **Test-time compute를 아직 안 쓰신다면 majority vote부터 켜세요.** GenRM-CoT는 K개 verification rationale을 뽑고 Yes/No 다수결만 해도 discriminative 대비 큰 개선을 뽑아요.
3. **PRM 학습이면 ThinkPRM 방식을 검토하세요.** PRM800K의 1%만 써도 SOTA에 근접해요. Full-supervision 강박에서 벗어날 수 있어요.
4. **RLVR 세팅이면 executable verifier를 우선 고려하세요.** 코드/수학은 Python interpreter + assertion이 어떤 LLM judge보다도 정확하고 저렴해요. LLM 검증은 tool call이 실패했을 때의 fallback으로만.
5. **벤치마크로는 ProcessBench + PRMBench 2종을 붙여 리포트하세요.** ProcessBench는 in-domain 수학 first-error, PRMBench는 세부 error taxonomy — 둘의 스코어 격차 자체가 verifier의 taxonomy 편향을 진단해줘요.
6. **Verifier hacking 조기 탐지:** (a) Isomorphic Perturbation Testing, (b) master-key 프롬프트 red-team, (c) reward↑ vs eval-acc↑ 이력의 divergence 모니터링. 이 셋 중 하나는 꼭 파이프라인에 넣으세요.

### 10.2 큰 그림 요약 (5줄)

- Verifier는 "정답성 판정"이 목표이고 Judge는 "선호도 판정"이 목표예요. 두 계보는 데이터셋·objective·평가 프레임이 달라요.
- 흐름은 Cobbe(2021) → Uesato(2022) → Lightman(2023, PRM800K) → Math-Shepherd(2023, 라벨 자동화) → GenRM(2024, generative) → ThinkPRM(2025)으로 이어져요.
- 방법론은 Discriminative → **Generative(next-token Yes/No)** → **Tool-augmented(Python 실행)** 순으로 표현력·검증가능성이 확장돼요.
- RLVR(Tulu3/DeepSeek-R1)은 verifier를 RL reward source로 쓰는 프레임이며, 2025-2026 대다수 reasoning model 학습의 골격이에요.
- 그러나 verifier hacking(One Token to Fool), self-preference bias, pass@k 축소(Yue et al.), Hidden Costs 등이 잇달아 보고되며 **"검증기가 학습 파이프라인의 병목"** 이라는 문제의식이 굳어지고 있어요.

### 10.3 대표 논문 10편 (한 페이지 매핑)

| # | 논문 | 역할 |
|---|---|---|
| 1 | [Cobbe et al. 2021 GSM8K verifier](https://arxiv.org/abs/2110.14168) | Best-of-N re-ranking, GSM8K, verifier head 원형 |
| 2 | [Uesato et al. 2022](https://arxiv.org/abs/2211.14275) | PRM/ORM 명명, trace error 감소 확인 |
| 3 | [Lightman et al. 2023](https://arxiv.org/abs/2305.20050) | PRM800K, MATH 78% |
| 4 | [Math-Shepherd 2023](https://arxiv.org/abs/2312.08935) | 라벨 자동화(MC rollout), 오픈소스 PRM 표준 |
| 5 | [Zhang et al. 2024 GenRM](https://arxiv.org/abs/2408.15240) | 검증을 next-token으로, CoT + majority vote |
| 6 | [Khalifa et al. 2025 ThinkPRM](https://arxiv.org/abs/2504.16828) | step-level generative PRM, 1% 라벨로 SOTA |
| 7 | [Tulu 3 (Ai2, 2024)](https://arxiv.org/abs/2411.15124) | RLVR 명명, rule-based reward + PPO |
| 8 | [DeepSeek-R1 / R1-Zero (2025)](https://arxiv.org/abs/2501.12948) | 규칙만으로 AIME 71%, RLVR 붐 방아쇠 |
| 9 | [Yue et al. NeurIPS'25](https://arxiv.org/abs/2504.13837) | pass@256에서 base가 앞섬, RLVR 비판 |
| 10 | [Weaver (Stanford 2025)](https://arxiv.org/abs/2506.18203) | weak-to-strong verifier 앙상블, gap 14.5% 축소 |

---

## 출처

**Foundations & method categories**
- [arXiv:2110.14168 — Cobbe et al., Training Verifiers to Solve Math Word Problems](https://arxiv.org/abs/2110.14168)
- [arXiv:2211.14275 — Uesato et al., Process- and outcome-based feedback](https://arxiv.org/abs/2211.14275)
- [arXiv:2305.20050 — Lightman et al., Let's Verify Step by Step](https://arxiv.org/abs/2305.20050)
- [github.com/openai/prm800k — PRM800K dataset](https://github.com/openai/prm800k)
- [arXiv:2312.08935 — Wang et al., Math-Shepherd](https://arxiv.org/abs/2312.08935)
- [arXiv:2408.15240 — Zhang et al., Generative Verifiers (GenRM)](https://arxiv.org/abs/2408.15240)
- [arXiv:2408.11791 — Critique-out-Loud (CLoud)](https://arxiv.org/abs/2408.11791)
- [arXiv:2408.02666 — Self-Taught Evaluators](https://arxiv.org/abs/2408.02666)
- [arXiv:2504.16828 — ThinkPRM](https://arxiv.org/abs/2504.16828)
- [arXiv:2306.05685 — Zheng et al., MT-Bench (Judge 대조)](https://arxiv.org/abs/2306.05685)

**RLVR & verifier-driven RL**
- [arXiv:2411.15124 — Tulu 3](https://arxiv.org/abs/2411.15124)
- [arXiv:2501.12948 — DeepSeek-R1](https://arxiv.org/abs/2501.12948)
- [arXiv:2501.12599 — Kimi K1.5](https://arxiv.org/abs/2501.12599)
- [arXiv:2409.12122 — Qwen2.5-Math](https://arxiv.org/abs/2409.12122)
- [arXiv:2505.09388 — Qwen3](https://arxiv.org/abs/2505.09388)
- [arXiv:2503.20783 — Dr. GRPO / Understanding R1-Zero-Like Training](https://arxiv.org/abs/2503.20783)
- [arXiv:2506.10947 — Spurious Rewards](https://arxiv.org/abs/2506.10947)
- [arXiv:2507.14843 — The Invisible Leash](https://arxiv.org/abs/2507.14843)
- [arXiv:2507.08794 — One Token to Fool LLM-as-a-Judge](https://arxiv.org/abs/2507.08794)
- [arXiv:2509.21882 — Hidden Costs of RLVR](https://arxiv.org/abs/2509.21882)
- [arXiv:2509.15557 — Composite Reward Mitigation](https://arxiv.org/abs/2509.15557)
- [arXiv:2505.13445 — Trust But Verify](https://arxiv.org/abs/2505.13445)
- [arXiv:2506.14245 — RLVR Implicitly Incentivizes Correct Reasoning](https://arxiv.org/abs/2506.14245)
- [OpenReview — Yue et al. NeurIPS'25](https://openreview.net/forum?id=4OsgYD7em5)

**Benchmarks**
- [arXiv:2412.06559 — ProcessBench](https://arxiv.org/abs/2412.06559)
- [arXiv:2501.03124 — PRMBench](https://arxiv.org/abs/2501.03124)
- [arXiv:2406.13975 — MR-Ben](https://arxiv.org/abs/2406.13975)
- [arXiv:2502.19187 — BIG-Bench Extra Hard](https://arxiv.org/abs/2502.19187)
- [arXiv:2402.00559 — REVEAL](https://arxiv.org/abs/2402.00559)
- [qwenlm.github.io — Qwen2.5-Math-PRM](https://qwenlm.github.io/blog/qwen2.5-math-prm/)

**Limitations & debates**
- [arXiv:2310.01798 — Huang et al., LLMs Cannot Self-Correct](https://arxiv.org/abs/2310.01798)
- [arXiv:2507.02778 — Self-Correction Bench](https://arxiv.org/abs/2507.02778)
- [arXiv:2504.13837 — Yue et al., pass@k](https://arxiv.org/abs/2504.13837)
- [arXiv:2506.06941 — Illusion of Thinking (Apple)](https://arxiv.org/abs/2506.06941)
- [arXiv:2506.09250 — Illusion of the Illusion of Thinking](https://arxiv.org/abs/2506.09250)
- [arXiv:2510.21978 — Beyond Reasoning Gains (RECAP)](https://arxiv.org/abs/2510.21978)
- [arXiv:2410.21819 — Self-Preference Bias](https://arxiv.org/abs/2410.21819)
- [arXiv:2506.18203 — Weaver](https://arxiv.org/abs/2506.18203)
- [arXiv:2502.20379 — Multi-Agent Verification](https://arxiv.org/abs/2502.20379)
- [arXiv:2508.03686 — CompassVerifier](https://arxiv.org/abs/2508.03686)
- [arXiv:2504.06141 — Adversarial Training of Reward Models](https://arxiv.org/abs/2504.06141)
- [arXiv:2505.22203 — Rule- vs Model-based Verifiers](https://arxiv.org/abs/2505.22203)
