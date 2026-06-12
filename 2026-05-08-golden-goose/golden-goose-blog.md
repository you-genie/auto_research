# Golden Goose: 검증 불가능한 인터넷 텍스트로 무한 RLVR 데이터 만들기

> 📊 **발표자료**: [golden-goose-presentation.pptx](./golden-goose-presentation.pptx)

> "The key bottleneck is verifiability, not data volume."
> — Lu et al., *Golden Goose*, 2026

RLVR(Reinforcement Learning with Verifiable Rewards)이라는 게 요즘 frontier reasoning 모델의 핵심이잖아요. DeepSeek-R1, OpenAI o3, Gemini 3 같은 모델들이 다 이 레시피로 학습해요. 그런데 여기에 치명적인 문제가 하나 있어요. **데이터가 부족하다**는 거예요 — 양이 부족한 게 아니라, *검증 가능한* 데이터가 부족한 거죠.

오늘 소개할 [Golden Goose](https://arxiv.org/abs/2601.22975) 논문은 이 문제를 굉장히 우아한 방법으로 해결해요. 검증 불가능한 인터넷 텍스트를 MCQ(객관식 문제)로 변환해서 RLVR 학습에 쓸 수 있는 데이터를 사실상 무한정 만들어내는 거예요. 아이디어 자체는 단순하지만, 실험 결과는 꽤 인상적이에요.

---

## 목차

1. [논문 개요](#1-논문-개요)
2. [문제의식: RLVR의 데이터 병목](#2-문제의식-rlvr의-데이터-병목)
3. [핵심 아이디어: Fill-in-the-Middle을 MCQ로](#3-핵심-아이디어-fill-in-the-middle을-mcq로)
4. [합성 파이프라인 상세](#4-합성-파이프라인-상세)
5. [왜 MCQ인가? 왜 선택지가 9개인가?](#5-왜-mcq인가-왜-선택지가-9개인가)
6. [데이터셋: GooseReason-0.7M & GooseReason-Cyber](#6-데이터셋-goosereason-07m--goosereason-cyber)
7. [학습 설정: ProRLv2](#7-학습-설정-prorlv2)
8. [실험 결과](#8-실험-결과)
9. [평가 벤치마크](#9-평가-벤치마크)
10. [한계와 향후 방향](#10-한계와-향후-방향)
11. [참고 문헌](#참고-문헌)

---

## 1. 논문 개요

| 항목 | 내용 |
|---|---|
| **제목** | Golden Goose: A Simple Trick to Synthesize Unlimited RLVR Tasks from Unverifiable Internet Text |
| **저자** | Ximing Lu, David Acuna, Jaehun Jung, Jian Hu, Di Zhang, Shizhe Diao, Yunheng Zou, Shaokun Zhang, Brandon Cui, Mingjie Liu, Hyunwoo Kim, Prithviraj Ammanabrolu, Jan Kautz, Yi Dong, Yejin Choi (15명) |
| **소속** | NVIDIA + University of Washington 계열 |
| **arXiv** | [2601.22975](https://arxiv.org/abs/2601.22975) (2026.01.30 제출, v1 2026.02.02) |
| **컨퍼런스** | ICML 2026 |

---

## 2. 문제의식: RLVR의 데이터 병목

### RLVR이 뭔지 잠깐만

RLVR은 모델의 답이 맞는지 자동으로 검증(verify)해서 그 신호를 강화학습 보상으로 쓰는 방식이에요. 수학 문제면 정답 숫자를 비교하고, 코딩 문제면 테스트 케이스를 돌려보면 되죠. 이 단순한 아이디어가 reasoning 모델의 성능을 급격히 끌어올린 비결이에요.

### 두 가지 구조적 한계

그런데 여기에 두 가지 근본적인 문제가 있어요.

**첫째, 검증 가능성 형식 제약이에요.** RLVR은 보상 자동 검증이 필수예요. 그러다 보니 단답형으로 답을 딱 잘라 낼 수 있는 문제만 쓸 수 있어요. 이론 증명, 의학 진단, 자유서술형 reasoning 같은 것들은 죄다 폐기되는 거예요. 인터넷에 있는 엄청난 양의 고품질 텍스트가 RLVR 학습에는 손도 못 대는 상황이죠.

**둘째, 데이터 포화(data saturation) 문제예요.** 강한 모델일수록 saturation이 빨리 와요. ProRL-1.5B-v2 같은 모델(R1-Distill-Qwen-1.5B를 ProRL 레시피로 20,000+ H100 시간 학습한 강력 모델)의 경우, ProRL 136K 샘플 중 25%만 *effective sample*로 동작해요. 학생 rollout이 성공도 나오고 실패도 나오는, 즉 학습 신호가 있는 샘플이 그 정도밖에 안 된다는 거예요. 나머지 75%는 이미 stale이에요.

더 극단적인 예로, Qwen-4B-Instruct는 ProRL 레시피로 학습하면 300 step 만에 plateau/regression이 와버려요. 기존 데이터로는 이 모델한테 더 줄 게 없는 거죠.

> 기존 해결책(ProRL prolonged training, BroRL rollout 확대, ScaleRL)은 모두 **알고리즘 쪽**을 건드리는 방향이었어요. Golden Goose는 정반대로 **데이터-centric 접근**을 택해요.

---

## 3. 핵심 아이디어: Fill-in-the-Middle을 MCQ로

한 줄 요약을 먼저 드리면:

> **검증 불가능한 텍스트를 MCQ로 감싸면 자동 검증이 가능해진다.**

아이디어 자체는 심플해요. 어떤 텍스트 S가 있을 때, 핵심 reasoning step 부분을 지워서 빈칸으로 만들고(masked context $S_\text{mask}$), 그 빈칸에 들어갈 내용이 뭔지를 고르는 MCQ로 변환하는 거예요.

수식으로 표현하면:

```
원본 텍스트 S
  → 마스킹: S_mask (핵심 구간 t를 제거)
  → MCQ task Q = (S_mask, {t} ∪ D)
    - t: 정답 (마스킹된 원본 구간)
    - D = {d_1, ..., d_k}: distractor 집합
```

보상은 단순해요. `predicted_option == gold_option`이면 1, 아니면 0. LLM-as-judge 같은 건 필요 없어요. RL 과정 중 추가 비용이 0이에요.

---

## 4. 합성 파이프라인 상세

실제로 이 MCQ를 어떻게 만드는지 살펴볼게요.

### Step 1: Masking

GPT-5에게 원본 텍스트 S에서 핵심 reasoning step의 연속 구간(contiguous span) $t$를 식별하고 마스킹하도록 프롬프트를 줘요. 이 마스킹된 부분이 정답이 되는 거예요.

### Step 2: Distractor 생성

같은 GPT-5가 $t$와 스타일은 비슷하지만, $S_\text{mask}$ 맥락에서는 부정확한 distractor 집합 $D = \{d_1, \ldots, d_k\}$를 생성해요. 그럴듯해 보이지만 틀린 선택지들이죠.

### Step 3: 웹 스크래핑 노이즈 처리

S가 웹에서 긁어온 거칠고 지저분한 텍스트라면, GPT-5가 먼저 교육적 가치가 있는 passage $S'$로 추출/요약해요. 그 위에서 mask + distractor 생성이 이루어지죠. 적당한 passage를 못 찾으면 빈 문자열을 반환해서 해당 텍스트는 걸러요.

### Step 4: 난이도 필터링

학생 모델(예: ProRL-1.5B-v2)이 16번 rollout에서 전부 성공하는 문제는 너무 쉬운 거예요. 학습 신호가 0이니까 제거해요.

전체 파이프라인을 그림으로 표현하면 이렇게 되는 거예요:

```
인터넷 텍스트 S
        │
        ▼
 [GPT-5] 노이즈 처리 → 교육적 passage S' 추출
        │
        ▼
 [GPT-5] 핵심 구간 t 식별 + 마스킹 → S_mask
        │
        ▼
 [GPT-5] distractor D = {d_1, ..., d_9} 생성
        │
        ▼
  MCQ = (S_mask, {t} ∪ D)
        │
        ▼
 [학생 모델] 16번 rollout → 모두 성공이면 제거
        │
        ▼
  최종 RLVR 학습 데이터
```

---

## 5. 왜 MCQ인가? 왜 선택지가 9개인가?

이 부분이 논문에서 꽤 중요하게 다뤄져요.

### Open-ended fill-in-the-mask는 왜 안 되나요?

사실 MCQ 말고 그냥 빈칸 채우기(open-ended)로 해도 되지 않냐는 생각이 들 수 있어요. 근데 두 가지 이유로 안 돼요.

**이유 1: LLM-as-judge 비용 폭증.** Open-ended 답변을 검증하려면 LLM-as-judge가 필요한데, 이게 RL 학습 루프 안에 들어가면 비용이 엄청 올라가요.

**이유 2: 더 결정적인 이유 — task instruction 무시.** RL-튜닝된 reasoning 모델들은 빈칸 채우기 포맷을 주면 instruction을 무시하고 문제를 처음부터 풀어버리는 경향이 있어요. 실제로 GooseReason-Math의 open-ended 버전에서 ProRL-1.5B-v2가 83% 이상의 샘플에서 accuracy 0%를 기록했어요. 학습 신호가 사실상 0인 거예요.

### 왜 선택지가 9개인가요?

선택지 수도 그냥 정한 게 아니에요.

| 선택지 수 | 문제점 |
|---|---|
| 3개 | 과도하게 쉬움. 모델이 정답 추론보다 elimination 전략을 써버림 |
| 9개 | 70% 이상의 문제가 medium-difficulty 영역에 안착. 학습 신호 최대화 |

ProRL-1.5B-v2 기준으로 9-choice MCQ를 주면 medium-difficulty 문제 비율이 가장 높아요. 그러니까 "9개"는 단순한 숫자가 아니라, 현재 학생 모델의 능력 수준에서 최적화된 난이도 설정이에요.

---

## 6. 데이터셋: GooseReason-0.7M & GooseReason-Cyber

### GooseReason-0.7M: 700K+ Reasoning Tasks

3개의 source corpus에서 데이터를 만들었어요. 모두 기존 RLVR 학습에 쓰지 못하던 데이터예요.

| Source | 원본 규모 | 특성 | 기존 RLVR에서 못 쓴 이유 |
|---|---|---|---|
| [AoPS-Instruct](https://arxiv.org/abs/2501.14275) | ~600K QA | Olympiad 수학 + 커뮤니티 풀이 | 노이즈 많고, 정리 증명은 verifier로 검증 불가 |
| [rStar-Coder](https://arxiv.org/abs/2505.21297) | 1,656K 합성 중 380K만 testcase 확보 | 경쟁 코딩 (IOI, Codeforces) | testcase 없는 split은 RL 학습 불가 |
| [MegaScience](https://arxiv.org/abs/2507.16812) | ~650K QA (12K 대학 교과서) | 물리·생물·화학·의학·CS·수학·경제 | 자유서술형, 화학식 등 verifier 검증 불가 |

이 세 corpus를 Golden Goose 파이프라인으로 변환해서 700K+ 개의 RLVR 학습 데이터를 만들었어요.

### Effective Sample 비교

모델이 실제로 학습 신호를 받을 수 있는 *effective sample* 비율이 얼마나 되는지 비교해볼게요. ProRL-1.5B-v2 기준이에요.

| 데이터셋 | Effective 비율 | 절대 샘플 수 |
|---|---|---|
| ProRL 136K | 25% | ~34K |
| GooseReason-0.7M | 70% | ~490K |

절대 effective 샘플 수 기준으로 +450K, ProRL 대비 13배예요. 포화된 모델에게 새로운 학습 신호를 줄 수 있다는 게 이 숫자로 증명되는 거예요.

### GooseReason-Cyber: 사이버보안 도메인

사이버보안은 오픈소스 RLVR 데이터가 아예 없던 영역이에요.

[Primus](https://arxiv.org/abs/2502.11191)의 두 소스(MITRE/Wikipedia/CTI 기반 Primus-Seed + 웹 스크랩 Primus-FineWeb)에서 Golden Goose 파이프라인을 적용해 180K RLVR task를 만들었어요. 기존엔 이런 데이터 자체가 없었던 거예요.

---

## 7. 학습 설정: ProRLv2

알고리즘은 [ProRLv2](https://hijkzzz.notion.site/prorl-v2)를 써요. GRPO의 변형이에요.

- **Clipped GRPO objective**: 기본 GRPO에서 PPO 스타일의 clipping 추가
- **Decoupled advantage normalization**: REINFORCE++에서 가져온 기법. group-wise mean subtraction 후 batch-level standardization

중요한 건 GooseReason 데이터가 **pluggable**하다는 거예요. 특정 알고리즘에 종속된 게 아니라, 어떤 RLVR 레시피에도 데이터만 끼워 넣으면 돼요.

---

## 8. 실험 결과

### (A) Data Saturation Revival: ProRL-1.5B-v2

이미 강력하게 학습된 ProRL-1.5B-v2 위에 GooseReason-0.7M을 추가로 1,100 H100 시간 학습했을 때의 결과예요.

| 도메인 | ProRL only | + GooseReason-0.7M |
|---|---|---|
| Math | +0.63% | **+2.71%** |
| Coding | +0.95% | **+2.12%** |
| STEM (GPQA Diamond) | +0.13% | **+3.48%** |

STEM 격차가 제일 크게 나왔어요. 기존 RLVR 데이터엔 일반 과학 영역이 부족했는데, GooseReason의 MegaScience 기반 데이터가 그 gap을 채운 거예요.

### (B) 강한 모델에서의 Saturation Revival: Qwen-4B-Instruct

더 극단적인 케이스예요. Qwen-4B-Instruct는 ProRL 300 step 만에 plateau/regression이 왔거든요.

| 도메인 | ProRL 계속 학습 | + GooseReason-0.7M |
|---|---|---|
| Math | -1.29% (regression!) | **+2.18%** |
| Coding | +0.43% | **+2.24%** |
| STEM | -1.52% (regression!) | **+2.40%** |

ProRL만 계속하면 오히려 성능이 떨어지는데, GooseReason을 넣으면 전 도메인에서 2% 이상 올라가요. 이 실험의 결과 모델인 **GooseReason-4B-Instruct**는 4B-Instruct 카테고리에서 SOTA를 달성하고, 7.5배 큰 Qwen3-30B-Instruct와 동등하거나 그 이상의 성능을 보여요.

### (C) Compute-Efficient Scaling

같은 200 step, 동일한 compute budget에서 ProRL only vs ProRL+GooseReason을 비교하면, 모든 step에서 GooseReason을 추가한 쪽이 우위예요.

### (D) Generalization: MCQ로 학습했는데 non-MCQ에서도 잘 되는가?

이 부분이 좀 흥미롭거든요. 학습은 MCQ 포맷으로 했는데, 평가 벤치마크는 대부분 비-MCQ예요. AIME, MATH, AMC, HumanEvalPlus, LiveCodeBench, GPQA Diamond 모두 MCQ가 아니죠.

그런데도 성능이 올라가요. Reasoning Gym의 logical puzzle에서도 향상이 나타나고, 이건 MCQ 포맷에서 배운 reasoning skill이 다른 포맷으로 transfer된다는 증거예요.

### (E) Cybersecurity: 100 Step만으로 SOTA 능가

| 설정 | 사이버보안 벤치마크 향상 |
|---|---|
| Qwen-4B-Instruct + GooseReason-Cyber (100 step) | **+4.44% (절대값)** |
| Llama-Primus-Instruct (Llama-3.1-8B + 광범위 도메인 학습, 이전 SOTA) | +1.44% |

4B 모델로 100 step RLVR 학습했더니, 8B 모델에 광범위한 도메인 학습을 한 이전 SOTA를 넘어버렸어요. 이전 RLVR 데이터가 아예 없던 도메인에서 이런 결과가 나왔다는 게 인상적이에요.

평가한 사이버보안 벤치마크는 CTI-Bench, CyberMetric, SecEval 세 개예요.

---

## 9. 평가 벤치마크

총 15개 벤치마크로 평가했어요.

| 분야 | 벤치마크 |
|---|---|
| Math | AIME 2024, AIME 2025, AMC, MATH, Minerva, Olympiad Bench |
| Coding | PRIME validation set (APPS, CodeContests, CodeForces, TACO), HumanEvalPlus, LiveCodeBench |
| STEM | GPQA Diamond |
| Logic | Reasoning Gym (Math / Algorithmic / Cognition / Logic 4개 카테고리) |
| Instruction Following | IFEval |

---

## 10. 한계와 향후 방향

### 저자가 직접 언급한 한계

**Dual-use 우려**: 사이버보안 RLVR은 방어뿐 아니라 공격 능력도 향상시킬 수 있어요. 저자들도 Impact Statements에서 이를 명시적으로 언급했어요.

**편향/유해성 상속**: 인터넷 텍스트 기반이라 source corpus의 bias·toxicity가 그대로 전파될 수 있어요.

### 개념적 한계 (우리가 추가로 생각해볼 것들)

**GPT-5 의존성**: 합성 파이프라인 전체가 GPT-5에 기댄다는 게 비용·라이선스 측면에서 종속성을 만들어요. 오픈소스 pipeline으로 대체할 수 있는지는 아직 검증 안 됐어요.

**Reasoning trace 품질 미평가**: MCQ 포맷은 정답을 맞히는지만 보지, reasoning trace 자체가 얼마나 좋은지는 reward에 반영이 안 돼요. reward hacking 여지가 있어요.

**"9-choice MCQ = medium-difficulty"의 모델 의존성**: 이 통계는 ProRL-1.5B-v2 기준이에요. 더 강한 모델에서는 9개도 부족할 수 있어요.

### 저자들의 전망

> "We envision extending to domains like law and medicine, where verifiable data is scarce but expert literature is abundant."

법률·의학처럼 검증 가능 데이터는 부족하지만 전문 문헌이 풍부한 영역으로의 확장이 자연스러운 다음 단계예요. 더 넓게 보면, 이 논문이 제시하는 패러다임 전환은 이거예요:

> **"검증 가능성이 진짜 병목이지, 데이터 양이 병목이 아니다."**

RLVR의 scale-up을 막고 있던 건 데이터 부족이 아니라 검증 불가능성이었고, Golden Goose는 그 병목을 데이터-centric 방식으로 우회하는 방법을 제시해요.

---

## 참고 문헌

| # | 제목 | 출처 |
|---|---|---|
| 1 | Golden Goose (arXiv abs) | [arxiv.org/abs/2601.22975](https://arxiv.org/abs/2601.22975) |
| 2 | Golden Goose (HTML 본문) | [arxiv.org/html/2601.22975](https://arxiv.org/html/2601.22975) |
| 3 | HuggingFace Paper Page | [huggingface.co/papers/2601.22975](https://huggingface.co/papers/2601.22975) |
| 4 | Papers Explained 539: Golden Goose (Ritvik Rastogi) | [ritvik19.medium.com](https://ritvik19.medium.com/papers-explained-539-golden-goose-af78d02a0741) |
| 5 | ResearchTrend.AI | [researchtrend.ai/papers/2601.22975](https://researchtrend.ai/papers/2601.22975) |
| 6 | ProRL | [arxiv.org/abs/2505.24864](https://arxiv.org/abs/2505.24864) |
| 7 | ProRLv2 | [hijkzzz.notion.site/prorl-v2](https://hijkzzz.notion.site/prorl-v2) |
| 8 | AoPS-Instruct | [arxiv.org/abs/2501.14275](https://arxiv.org/abs/2501.14275) |
| 9 | rStar-Coder | [arxiv.org/abs/2505.21297](https://arxiv.org/abs/2505.21297) |
| 10 | MegaScience | [arxiv.org/abs/2507.16812](https://arxiv.org/abs/2507.16812) |
| 11 | Primus (Cybersecurity) | [arxiv.org/abs/2502.11191](https://arxiv.org/abs/2502.11191) |
| 12 | GRPO / DeepSeekMath | [arxiv.org/abs/2402.03300](https://arxiv.org/abs/2402.03300) |
| 13 | RLVE | [arxiv.org/abs/2511.07317](https://arxiv.org/abs/2511.07317) |

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. Golden Goose 논문이 지적하는 RLVR의 진짜 병목은 뭘까요? 데이터의 "양"일까요, 아니면 다른 무언가일까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 데이터의 양이 아니라 **검증 가능성(verifiability)**이에요.

**해설**: 인터넷에는 고품질 텍스트가 넘쳐나지만, RLVR은 보상을 자동으로 검증할 수 있는 단답형 문제만 쓸 수 있어요. 그래서 이론 증명, 자유서술형 reasoning 같은 데이터는 죄다 버려지고 있었죠. Golden Goose는 이 검증 불가능한 텍스트를 검증 가능한 형태로 바꾸는 데서 출발해요.

</details>

**Q2. Golden Goose가 검증 불가능한 텍스트를 RLVR 데이터로 바꾸는 핵심 트릭은 무엇인가요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 텍스트의 핵심 reasoning 구간을 마스킹해서 빈칸으로 만들고, 그 빈칸에 들어갈 내용을 고르는 **MCQ(객관식 문제)**로 변환하는 거예요.

**해설**: 원본 텍스트 S에서 핵심 구간 t를 지워 S_mask를 만들고, 정답 t와 그럴듯한 distractor들을 선택지로 묶어요. 그러면 `predicted_option == gold_option` 비교만으로 보상을 줄 수 있어서, LLM-as-judge 없이도 자동 검증이 가능해지죠.

</details>

**Q3. OX 문제예요. "MCQ 대신 open-ended 빈칸 채우기로 해도 LLM-as-judge 비용만 감수하면 학습 신호는 충분히 얻을 수 있다." 맞을까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X예요.

**해설**: 비용 문제보다 더 결정적인 이유가 있어요. RL-튜닝된 reasoning 모델들은 빈칸 채우기 포맷을 주면 instruction을 무시하고 문제를 처음부터 풀어버리는 경향이 있거든요. 실제로 open-ended 버전에서 ProRL-1.5B-v2가 83% 이상의 샘플에서 accuracy 0%를 기록해서, 학습 신호가 사실상 0이었어요.

</details>

**Q4. 선택지를 3개가 아니라 9개로 정한 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 9개일 때 문제 대부분이 **medium-difficulty 영역**에 안착해서 학습 신호가 최대화되기 때문이에요.

**해설**: 선택지가 3개면 너무 쉬워서 모델이 정답 추론 대신 elimination 전략을 써버려요. ProRL-1.5B-v2 기준으로 9-choice일 때 70% 이상의 문제가 적당한 난이도에 들어갔죠. 다만 이건 해당 학생 모델 기준의 통계라서, 더 강한 모델에서는 9개도 부족할 수 있다는 한계도 있어요.

</details>

**Q5. 합성 파이프라인의 마지막 단계인 난이도 필터링에서는 어떤 문제를 걸러낼까요? 그리고 왜 걸러낼까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 학생 모델이 16번 rollout에서 **전부 성공하는 문제**를 제거해요. 너무 쉬워서 학습 신호가 0이기 때문이죠.

**해설**: RLVR에서 학습 신호는 rollout에 성공과 실패가 섞여 있을 때 생겨요. 모든 rollout이 성공하는 문제는 모델이 이미 잘 푸는 문제라서 줄 게 없는 거예요. 이게 본문에서 말한 *effective sample* 개념과도 연결되는데, ProRL 136K는 25%만 effective였던 반면 GooseReason-0.7M은 70%가 effective였어요.

</details>

**Q6. 이미 plateau에 빠진 Qwen-4B-Instruct에 ProRL 데이터로 계속 학습하는 것과 GooseReason-0.7M을 추가하는 것, 결과가 어떻게 달랐나요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: ProRL만 계속하면 Math와 STEM에서 오히려 성능이 **떨어졌고(regression)**, GooseReason을 넣으면 전 도메인에서 2% 이상 **올라갔어요**.

**해설**: 포화된 데이터로는 더 쥐어짤 게 없어서 계속 학습하면 역효과가 나는데, 새로운 학습 신호를 주는 데이터를 끼워 넣으니 다시 성장한 거예요. 이렇게 만들어진 GooseReason-4B-Instruct는 7.5배 큰 Qwen3-30B-Instruct와 동등하거나 그 이상의 성능을 보였죠.

</details>

**Q7. 학습은 MCQ 포맷으로만 했는데, AIME나 LiveCodeBench처럼 MCQ가 아닌 벤치마크에서도 성능이 올랐어요. 이게 왜 중요한 결과일까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: MCQ 포맷에서 배운 reasoning skill이 **다른 포맷으로 transfer**된다는 증거이기 때문이에요.

**해설**: 만약 모델이 "객관식 잘 찍는 요령"만 배웠다면 비-MCQ 벤치마크에서는 효과가 없었겠죠. 그런데 AIME, MATH, HumanEvalPlus, GPQA Diamond 같은 비-MCQ 평가에서도 성능이 올랐다는 건, 포맷이 아니라 reasoning 능력 자체가 향상됐다는 뜻이에요.

</details>

**Q8. 응용 시나리오예요. 여러분이 법률 도메인 reasoning 모델을 만들고 싶은데, 검증 가능한 RLVR 데이터가 하나도 없다고 해볼게요. Golden Goose 방식이라면 어떻게 접근할 수 있을까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 판례·법률 문헌 같은 전문 텍스트에서 핵심 reasoning 구간을 마스킹하고 distractor를 생성해서 MCQ 형태의 RLVR 데이터를 합성하면 돼요.

**해설**: 사이버보안이 딱 이런 케이스였어요. 오픈소스 RLVR 데이터가 아예 없던 도메인이었는데, Primus 텍스트로 180K task를 만들어 100 step만 학습하고도 이전 SOTA를 넘었죠. 저자들도 법률·의학처럼 검증 가능 데이터는 부족하지만 전문 문헌이 풍부한 영역으로의 확장을 다음 단계로 전망하고 있어요.

</details>
