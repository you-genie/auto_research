# LLM도 잠이 필요하다 — "Language Models Need Sleep" 논문 완전 해부

> **들어가기 전에:** 2026년 5월에 쏟아진 "수면(Sleep)" 관련 LLM 논문이 세 편이나 됩니다. 오늘은 그 중 핵심 두 편을 집중 해부할게요. 아키텍처 트릭도 있고, 인간 기억 메커니즘과의 유비도 있고 — 읽으면 읽을수록 신선한 논문들이거든요.

---

## 목차

1. [왜 지금 "수면"인가?](#1-왜-지금-수면인가)
2. [논문 A: arXiv 2605.26099 — 수면으로 Fast Weight를 갱신하다](#2-논문-a-arxiv-260526099)
3. [논문 B: ICLR 2026 — Self-Modify와 Dreaming으로 Continual Learning을](#3-논문-b-iclr-2026-openreview)
4. [두 논문의 공통 문제의식](#4-두-논문의-공통-문제의식)
5. [방법론 심층 비교](#5-방법론-심층-비교)
6. [실험 결과 정리](#6-실험-결과-정리)
7. [한계점과 후속 연구 방향](#7-한계점과-후속-연구-방향)
8. [커뮤니티 시사점: Continual Learning, Catastrophic Forgetting, Memory Consolidation](#8-커뮤니티-시사점)
9. [참고문헌](#참고문헌)

---

## 1. 왜 지금 "수면"인가?

솔직히 처음 제목 보고 "LLM이 잠을 자? 웬 비유야?" 싶었는데요. 실제로 읽어보면 꽤 진지한 문제를 다루고 있어요.

현재 LLM이 직면한 핵심 딜레마는 이렇습니다:

| 문제 | 현상 | 기존 접근 |
|------|------|-----------|
| Attention 이차 복잡도 | 컨텍스트 길이 ↑ → 연산/메모리 비용 O(L²) | KV cache 압축, sliding window |
| 장기 기억 부재 | 컨텍스트 창 밖의 정보는 그냥 버려짐 | RAG, external memory |
| Catastrophic Forgetting | 새 지식 학습 시 기존 지식 파괴 | EWC, LoRA replay |
| 추론 깊이 한계 | 토큰 수보다 reasoning step이 많아지면 성능 급락 | CoT, scratchpad |

이 중에서 특히 "컨텍스트 창 밖으로 밀려난 정보를 어떻게 내재화할 것인가"라는 질문에, **수면(Sleep)**이라는 아이디어가 꽤 우아한 답을 제시하거든요.

> "Animals consolidate memories during sleep through hippocampal replay, converting short-term episodic memories into long-term representations." — 논문 2605.26099 서론

해마 리플레이(hippocampal replay), 즉 수면 중 낮에 경험한 것을 반복 재생하면서 장기 기억으로 굳히는 과정 — 이게 이 논문들의 핵심 영감이에요.

---

## 2. 논문 A: arXiv 2605.26099 — 수면으로 Fast Weight를 갱신하다

### 2.1 논문 기본 정보

| 항목 | 내용 |
|------|------|
| **제목** | Language Models Need Sleep |
| **저자** | Sangyun Lee, Sean McLeish, Tom Goldstein, Giulia Fanti |
| **소속** | Carnegie Mellon University (Lee, Fanti), University of Maryland (McLeish, Goldstein) |
| **제출일** | 2026년 5월 25일 |
| **arXiv** | [2605.26099](https://arxiv.org/abs/2605.26099) |
| **주요 타겟** | SSM-Attention 하이브리드 모델의 장문맥 추론 한계 |

### 2.2 핵심 문제의식

저자들이 관찰한 현상은 이렇습니다. SSM(State Space Model)-Attention 하이브리드 모델을 쓰면 메모리 효율은 좋아지는데, **정보 저장량이 문제가 아니라 추론 깊이가 문제**라는 거예요.

> "We show that the bottleneck is not memory capacity but rather the lack of computation needed to transform evicted context into useful internal states."

쉽게 말하면: KV 캐시를 날려버리면 메모리는 아끼는데, 그 날아간 정보가 "어디 잘 녹아들어가질" 충분한 계산이 안 된다는 거죠. 그냥 버리는 거랑 다름없어요.

### 2.3 아키텍처: Sleep Phase란?

핵심 아이디어는 **컨텍스트 윈도우가 가득 찼을 때 KV 캐시를 날리기 전에 "잠"을 자게 한다**는 겁니다.

```
Wake Phase:
  토큰 읽기 → Single Forward Pass → 예측 → KV cache 누적

Sleep Phase (컨텍스트 윈도우 L 도달 시):
  Step 1: 누적된 컨텍스트에 대해 N번 반복 Forward Pass (offline)
  Step 2: 각 패스에서 SSM 블록의 Fast Weight S_t를 Gated Hebbian Rule로 갱신
  Step 3: KV cache 완전 초기화
  
다시 Wake Phase로 복귀 (Fast Weight에 통합된 정보 보유 상태)
```

#### Fast Weight란?

SSM 블록 내부에는 고정 크기의 hidden state **S_t** 가 있는데, 이게 "Fast Weight"입니다. 일반 모델 파라미터(slow weight)와 달리, 이 상태는 컨텍스트에 따라 동적으로 갱신되죠.

수면 중에는 이 Fast Weight를 **Gated Hebbian Rule**로 반복 개선합니다. 재미있는 건, 이 업데이트가 단순한 hidden state 업데이트가 아니라 **정제된 Fast Weight 자체에 그래디언트가 흐른다**는 점이에요. 기존 깊이-재귀 모델들과의 차별점이 여기에 있어요.

#### 학습 방식

전체 계산 그래프(Sleep Phase + Prediction Phase)에 대해 엔드-투-엔드 역전파를 수행합니다. Sleep N번의 패스가 전부 미분 가능한 계산 그래프에 포함돼요.

```
손실 계산:
  - Consolidation phase (N loops): 별도 loss 없음, 순수 상태 갱신
  - Prediction phase: masked cross-entropy loss
  - 전체에 대해 역전파
```

#### 추론 시 레이턴시 보존

중요한 점은 **Wake 단계 예측은 여전히 단일 포워드 패스**라는 거예요. 추가 연산(N번 반복)은 전부 Sleep Phase에 몰려 있고, 실제 추론 레이턴시는 영향받지 않습니다.

---

## 3. 논문 B: ICLR 2026 (OpenReview) — Self-Modify와 Dreaming으로 Continual Learning을

### 3.1 논문 기본 정보

| 항목 | 내용 |
|------|------|
| **제목** | Language Models Need Sleep: Learning to Self Modify and Consolidate Memories |
| **저자** | Ali Behrouz, Farnoosh Hashemi, Vahab Mirrokni |
| **게재처** | ICLR 2026 |
| **OpenReview** | [iiZy6xyVVE](https://openreview.net/forum?id=iiZy6xyVVE) |
| **주요 타겟** | In-context 지식의 장기 파라미터 내재화, Continual Learning |

### 3.2 핵심 문제의식

이 논문은 다른 각도에서 출발합니다.

> "Despite advances in LLMs showing promising results in tasks requiring instant prediction or in-context learning, existing models lack the ability to continually learn and effectively transfer their temporal in-context knowledge to their long-term parameters."

ICL(In-Context Learning)이 아무리 강력해도, 컨텍스트 창 안에서만 유효한 "단기 기억"이라는 거예요. 인간으로 치면 공부한 게 자고 일어나면 다 사라지는 것과 같죠.

### 3.3 Sleep 패러다임의 구조

이 논문의 Sleep은 두 단계로 구성됩니다:

#### Stage 1: Memory Consolidation — Knowledge Seeding

핵심 메커니즘은 **Knowledge Seeding**이라 불리는 RL 기반 상향식 증류(Upward Distillation)입니다.

- 작은 모델(단기 기억을 담은)의 표현을 더 큰 네트워크로 **파라미터 확장(Parameter Expansion)**을 통해 전달
- RL을 활용해 어떤 메모리를 장기 파라미터로 승격시킬지 선택
- 일종의 "공부한 내용 중 중요한 것만 골라 장기 기억화"

#### Stage 2: Dreaming — Self-Generated Training

두 번째 단계는 **Dreaming**, 즉 강화학습을 이용한 자기 생성 훈련입니다:

- 모델이 스스로 **합성 데이터 커리큘럼(Synthetic Data Curriculum)** 생성
- 인간 감독 없이 새로운 지식 습득
- Catastrophic Forgetting 방지를 위한 선택적 간섭 제어

#### 두 단계의 시너지

| 단계 | 역할 | 생물학적 유비 |
|------|------|--------------|
| Memory Consolidation (Knowledge Seeding) | In-context → Long-term parameter 전환 | NREM 수면 — 기억 재활성화 및 강화 |
| Dreaming | Self-improvement, interference 제어 | REM 수면 — 기억 통합 및 창의적 연결 |

---

## 4. 두 논문의 공통 문제의식

겉보기엔 달라 보이는 두 논문이지만, 공통 문제의식은 명확합니다:

> **"컨텍스트 창은 단기 기억이다. LLM에게 이를 내재화할 오프라인 시간이 필요하다."**

| 관점 | 논문 A (arXiv 2605.26099) | 논문 B (ICLR 2026) |
|------|--------------------------|-------------------|
| 타겟 문제 | 장문맥 추론 시 KV cache 증가 | ICL 지식의 비영속성 |
| Sleep의 역할 | Fast Weight 갱신으로 정보 압축 | 단기→장기 파라미터 전환 |
| 생물학적 유비 | 해마 리플레이 | NREM/REM 수면 사이클 |
| 추론 비용 | Wake 단계 레이턴시 보존 | 메모리 압력 감소 |
| 학습 방식 | E2E 역전파 + Gated Hebbian | RL 기반 Knowledge Seeding |

---

## 5. 방법론 심층 비교

### 5.1 논문 A의 기술적 위치

이 논문은 **Test-Time Compute 재분배** 관점으로도 읽힌다는 게 흥미로워요. 기존 연구들이 추론 시 compute를 늘리는 방향(CoT, Best-of-N, Process Reward Model)이었다면, 이 논문은 **수면이라는 오프라인 단계에 compute를 투자해 Wake 단계 레이턴시를 아낀다**는 발상이거든요.

#### SSM과 Fast Weight의 관계

SSM(예: Mamba)의 hidden state는 선형 재귀로 유지됩니다:

```
S_t = A·S_{t-1} + B·x_t   (일반 SSM)
```

수면 중에는 이 상태가 N번의 반복 패스를 통해 정제됩니다:

```
S_t^{(n+1)} = f(S_t^{(n)}, context)   (Sleep의 Gated Hebbian update)
```

N이 커질수록 더 정교한 추상화가 이루어지는데, 이게 "긴 잠 → 더 깊은 기억 통합"이라는 생물학적 직관과 일치해요.

### 5.2 논문 B와 Continual Learning 관계

지금까지 Continual Learning의 고전 접근들을 보면:

| 방법 | 전략 | 단점 |
|------|------|------|
| EWC (Elastic Weight Consolidation) | 중요한 파라미터 변화 억제 | 태스크 수 증가 시 제약 과도 누적 |
| Replay Buffer | 이전 데이터 혼합 | 메모리 증가, 프라이버시 이슈 |
| LoRA Continual | 별도 어댑터 | 태스크 간 전이 미흡 |
| SLEEP (논문 B) | RL 기반 Knowledge Seeding + Dreaming | 파라미터 확장 비용 |

논문 B의 핵심 차별점은 **"무엇을 기억할지"를 모델 스스로 선택한다**는 거예요. RL이 커리큘럼을 생성하고, 어떤 in-context 지식을 장기 파라미터로 승격할지도 학습으로 결정합니다.

---

## 6. 실험 결과 정리

### 6.1 논문 A 실험 결과

#### 실험 1: Cellular Automaton (Rule 110)

- 설정: 24비트 초기 상태 4개, t 스텝 진화 후 첫 비트 예측
- 윈도우 크기 L=24 (추론 깊이 t만 변화)
- 메모리 용량 자체는 충분 — 순수하게 **추론 깊이** 테스트

| Sleep N | t=16 정확도 | t=32 정확도 |
|---------|------------|------------|
| N=1 (수면 없음) | ~35% | ~10% |
| N=2 | ~55% | ~20% |
| N=4 | ~65% | >30% |

추론이 깊어질수록 Sleep의 이득이 극적으로 커집니다.

#### 실험 2: Depo — 다중 홉 그래프 검색

- 설정: 방향성 순환 그래프에서 k-홉 쿼리 답변
- 윈도우 L=75, 순환이 4개 윈도우에 걸쳐 분산

| 홉 수 (k) | N=1 | N=2 | N=4 |
|-----------|-----|-----|-----|
| k ≤ 2 | 학습 진행 | 학습 진행 | 학습 진행 |
| k = 4~8 | 거의 정체 | 약간 개선 | 개선 시작 |
| k = 16 | 진전 없음 | 정체 | 유일하게 진전 |

깊은 멀티홉 추론에서 N=4만 훈련 예산 내에서 의미 있는 성능을 보였어요.

#### 실험 3: GSM-Infinite — 수학 추론

실제 사전학습된 모델(Jet-Nemotron 2B, Ouro 1.4B)을 파인튜닝한 결과:

**Jet-Nemotron 2B:**

| 연산 수 | N=1 | N=6 | 향상 |
|---------|-----|-----|------|
| 6 연산 | 0.742 | 0.812 | +9.4% |
| 8 연산 | 0.351 | 0.388 | +10.5% |

**Ouro 1.4B (더 뚜렷한 효과):**

| 연산 수 | N=1 | N=6 | 향상 |
|---------|-----|-----|------|
| 6 연산 | 0.419 | 0.615 | +**47%** |
| 8 연산 | 0.210 | 0.272 | +29.5% |

Ouro 1.4B에서 6 연산 문제의 47% 향상은 정말 인상적이에요. 이건 단순히 파라미터를 늘린 게 아니라 **동일한 모델이 Sleep Phase를 더 오래 가져갈수록 더 잘 푼다**는 거거든요.

#### Ablation: Sliding-Window Eviction

전체 KV cache를 날리지 않고 L=512 윈도우를 유지하면서 Sleep을 적용한 경우:

| Sleep N | 정확도 |
|---------|--------|
| N=1 | 0.596 |
| N=4 | **0.905** (+52%) |

윈도우를 유지해도 Sleep이 중요하다는 걸 보여줘요.

### 6.2 논문 B 실험 결과

ICLR 2026 논문은 구체적 수치가 공개된 부분이 제한적이지만, 저자들이 보고한 결론은:

> "Across long-context understanding, knowledge incorporation, few-shot reasoning, and continual learning, SLEEP yields consistent gains over ICL, compression-based baselines, and self-adapting methods, while reducing memory pressure."

즉, SLEEP 패러다임이 다음 베이스라인들을 모두 능가:

- **ICL** (In-Context Learning 순수 활용)
- **Compression-based baselines** (KV cache 압축 방법론들)
- **Self-adapting methods** (기존 self-improvement 접근들)

특히 **Continual Learning 시나리오**에서 Catastrophic Forgetting에 대한 내성이 확인되었어요.

---

## 7. 한계점과 후속 연구 방향

### 7.1 논문 A의 한계

**1. 훈련 안정성 문제**

N이 커질수록 역전파 그래프가 깊어지면서 불안정해질 수 있어요. 저자들은 암시적 그래디언트(Implicit Gradients)나 절단된 BPTT(Truncated BPTT)를 해결책으로 제시하지만, 실용적 구현에서 여전히 까다로운 부분입니다.

**2. 순차적 작업에만 유리**

Sleep 메커니즘은 본질적으로 **순차적인 추론 구조**를 가진 작업에서 이득이 커요. 셀룰러 자동화, 그래프 순회, 수학적 추론 같은 작업이죠. 단순한 지식 검색(knowledge retrieval) 위주 작업에선 이득이 제한적일 수 있어요.

**3. 훈련 비용 vs. 추론 레이턴시 트레이드오프**

- 추론 레이턴시: 보존됨 (Wake 단계는 단일 패스)
- 훈련 처리량: N에 대략 반비례 (N=4면 약 4배 느림)

처리량 오버헤드를 감수할 가치가 있는지는 도메인에 따라 다릅니다.

**4. SSM 블록 의존성**

현재 구현은 SSM 블록의 Fast Weight를 활용하므로, **Pure Transformer에는 직접 적용 불가**. SSM-Attention 하이브리드 아키텍처가 전제입니다.

### 7.2 논문 B의 한계

**1. 파라미터 확장 비용**

Knowledge Seeding의 파라미터 확장(Parameter Expansion)은 모델 크기를 키우는 작업이에요. 이 비용이 실용적 배포 환경에서 얼마나 허용될지는 미지수입니다.

**2. RL 기반 학습의 불안정성**

Dreaming 단계에서 RL을 사용한 자기 생성 훈련은 reward 설계에 민감하고, 분포 이탈(distribution shift) 위험이 있어요.

### 7.3 후속 연구 방향

두 논문이 공통적으로 제시하는 방향:

1. **Sleep 스케줄 자동화**: 언제, 얼마나 오래 잘지를 모델이 스스로 결정하는 메타-러닝 방식
2. **Pure Transformer 확장**: Fast Weight 없이 attention만으로 Sleep 구현
3. **Sleep-Aware 사전학습**: 처음부터 Sleep Phase를 고려한 사전학습 방식
4. **실용적 배포 최적화**: 배치 처리에서 Sleep Phase를 비동기로 처리하는 시스템 최적화

---

## 8. 커뮤니티 시사점

### 8.1 Continual Learning의 새로운 지평

기존 Continual Learning 연구는 주로 **파인튜닝 단계**에서 Catastrophic Forgetting을 막는 것에 집중했어요. Sleep 프레임워크는 이를 **추론 단계의 메모리 관리 문제**로 재정의한다는 점에서 패러다임 전환적이에요.

> "Sleep prevents catastrophic forgetting in spiking neural networks by forming joint synaptic weight representations." — bioRxiv, 신경과학 연구

신경과학 연구에서도 수면이 기억 간섭(proactive interference)을 해소하는 핵심 메커니즘으로 밝혀졌는데, 이 논문들이 그 원리를 LLM에 적용한 거예요.

### 8.2 Fast-Slow Learning Framework와의 연결

2026년에는 [Fast-Slow Learning Framework](https://arxiv.org/abs/2605.12484) 같은 연구도 같은 관점을 공유해요:

- **Slow weights**: 일반 모델 파라미터 (장기 기억)
- **Fast weights**: 컨텍스트 의존적 상태 (단기 기억)

Sleep 메커니즘은 이 이분법을 **동적으로 연결하는 다리** 역할을 합니다. 단기 기억(Fast Weight)의 정보를 장기 파라미터(Slow Weight)에 통합하는 거죠.

### 8.3 Test-Time Compute 트렌드과의 접점

최근 OpenAI o-series, DeepSeek-R1 등이 이끄는 **Test-Time Compute 확장** 트렌드와도 맥이 닿아 있어요:

| 접근 | Compute 투자 시점 | 목표 |
|------|-----------------|------|
| CoT / o-series | 추론 시 (Wake) | 단계별 추론 개선 |
| Sleep (논문 A) | 수면 시 (오프라인) | 메모리 통합, Wake 레이턴시 보존 |
| Knowledge Seeding (논문 B) | 파라미터 업데이트 시 | ICL → 파라미터 영속화 |

Sleep은 Test-Time Compute를 "추론 중"이 아니라 "추론 사이"에 투자한다는 점에서 독특한 위치를 차지해요.

### 8.4 Memory Consolidation과 뇌 과학의 유비

이 논문들이 차용한 뇌 과학 개념들:

| 뇌 현상 | LLM 유비 |
|---------|---------|
| 해마 리플레이 (Hippocampal Replay) | N번의 오프라인 재귀 패스 |
| NREM 수면 — 기억 강화 | Memory Consolidation (Knowledge Seeding) |
| REM 수면 — 기억 통합/창의적 처리 | Dreaming (Self-Generated Training) |
| 선택적 망각 (Selective Forgetting) | Interference 제어, 중요 기억 선별 |
| 시냅스 항상성 (Synaptic Homeostasis) | Fast Weight의 정제 및 초기화 |

뇌는 수면 중에 필요 없는 시냅스 연결을 가지치기(pruning)하기도 하는데, LLM의 KV 캐시 초기화가 이 역할을 한다고 볼 수 있어요.

---

## 마무리

"LLM도 잠이 필요하다"는 주장, 처음엔 마케팅 문구 같아 보였지만 뚜껑 열어보니 꽤 깊은 곳에서 나온 인사이트예요.

핵심을 한 줄로 요약하면:

> **"컨텍스트 창에 쌓인 단기 기억을 오프라인으로 반복 처리해 fast weight에 내재화하면, 동일한 메모리 예산으로 훨씬 깊은 추론이 가능하다."**

앞으로 SSM-Transformer 하이브리드 모델이 주류화되는 흐름에서, Sleep Phase는 장문맥 처리 파이프라인의 표준 구성요소로 자리 잡을 가능성이 높습니다. 특히 수학 추론, 코드 실행, 다중 홉 지식 추론 같은 **깊은 추론이 필요한 도메인**에서의 잠재력은 상당히 크거든요.

---

## 참고문헌

| 번호 | 제목 | 저자/출처 | URL |
|------|------|----------|-----|
| 1 | Language Models Need Sleep | Lee et al. (CMU, UMD), 2026 | https://arxiv.org/abs/2605.26099 |
| 2 | Language Models Need Sleep: Learning to Self Modify and Consolidate Memories | Behrouz et al., ICLR 2026 | https://openreview.net/forum?id=iiZy6xyVVE |
| 3 | Learning to Forget: Sleep-Inspired Memory Consolidation for Resolving Proactive Interference in LLMs | Xie, 2026 | https://arxiv.org/abs/2603.14517 |
| 4 | SCM: Sleep-Consolidated Memory with Algorithmic Forgetting for LLMs | Shinde, 2026 | https://arxiv.org/abs/2604.20943 |
| 5 | Learning, Fast and Slow: Towards LLMs That Adapt Continually | arXiv 2605.12484 | https://arxiv.org/abs/2605.12484 |
| 6 | Language Models Need Sleep (HTML 전문) | arXiv, 2026 | https://arxiv.org/html/2605.26099v1 |
