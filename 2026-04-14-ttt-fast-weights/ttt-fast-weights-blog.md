# Test Time Training & Fast Weights: 추론할 때도 배우는 AI의 등장

> "The key idea is to make the hidden state a machine learning model itself, and the update rule a step of self-supervised learning."
> — Yu Sun et al., *Learning to (Learn at Test Time)*, 2024

흠, AI가 '테스트 중에도 계속 배운다'는 게 무슨 뜻일까요? 보통 우리가 아는 딥러닝은 학습(train)과 추론(inference)이 철저히 분리돼 있잖아요. 모델을 왕창 학습시키고, 이후에는 가중치를 얼려버린 채 그냥 쓰는 거죠. 그런데 Test Time Training(TTT)은 이 경계를 허물어요. 추론하는 동안에도 모델이 "아, 지금 이 문맥에서는 이렇게 동작해야겠구나"를 학습하면서 자기 자신을 업데이트하거든요.

이 개념이 2024년부터 급격히 주목받으면서, 트랜스포머를 대체할 수도 있는 시퀀스 모델링 패러다임으로 떠오르고 있어요. 오늘은 TTT의 아이디어부터 최신 연구까지 쭉 정리해볼게요.

---

## 목차

1. [기존 패러다임의 한계: Train vs. Test 분리](#1-기존-패러다임의-한계)
2. [Fast Weights: 뿌리가 있었던 아이디어](#2-fast-weights-뿌리가-있었던-아이디어)
3. [TTT의 핵심 아이디어: 숨겨진 상태가 학습한다](#3-ttt의-핵심-아이디어)
4. [TTT-Linear & TTT-MLP: 구체적인 구현](#4-ttt-linear--ttt-mlp)
5. [Titans: 구글의 장기 메모리 아키텍처](#5-titans-구글의-장기-메모리-아키텍처)
6. [End-to-End TTT와 LaCT: 효율성을 향하여](#6-end-to-end-ttt와-lact)
7. [TTT vs. Transformer Attention: 비교 분석](#7-ttt-vs-transformer-attention)
8. [TTT 생태계: 관련 아키텍처들](#8-ttt-생태계-관련-아키텍처들)
9. [한계와 과제](#9-한계와-과제)
10. [향후 전망](#10-향후-전망)
11. [참고 문헌](#참고-문헌)

---

## 1. 기존 패러다임의 한계

### Transformer: 좋은데 느려

[트랜스포머(Vaswani et al., 2017)](https://arxiv.org/abs/1706.03762)의 Self-Attention은 강력하지만, 결정적인 약점이 있어요: **이차 복잡도(O(n²))**.

컨텍스트 길이가 2배 늘면 연산량은 4배가 되는 구조예요. 1M 토큰짜리 문서를 처리하려고 하면... 사실상 불가능에 가깝죠.

### RNN: 빠른데 멍청해

반면 RNN 계열(LSTM, GRU 등)은 **선형 복잡도(O(n))**를 가져요. 토큰을 하나씩 처리하면서 고정 크기의 히든 스테이트에 정보를 압축하거든요.

문제는 이 '히든 스테이트'의 표현력이 너무 낮다는 거예요. 32k, 64k 토큰처럼 긴 컨텍스트가 오면 제대로 기억을 못 하고 성능이 뚝 떨어지는 경향이 있어요.

> "Self-attention performs well in long context but has quadratic complexity. Existing RNN layers have linear complexity, but their performance in long context is limited by the expressive power of their hidden states."
> — Yu Sun et al., 2024

이 딜레마를 해결하려는 게 TTT의 출발점이에요.

---

## 2. Fast Weights: 뿌리가 있었던 아이디어

TTT가 갑자기 하늘에서 뚝 떨어진 개념은 아니에요. 사실 1980년대부터 비슷한 아이디어가 있었거든요.

### Hinton의 Fast Weights (1987)

[Geoffrey Hinton과 David Plaut (1987)](https://www.cs.toronto.edu/~hinton/absps/fastweights87.pdf)이 "Using fast weights to deblur old memories"라는 논문에서 처음 제안한 개념이에요.

핵심 아이디어는 이거예요:

- **Slow Weights**: 전통적인 학습 과정에서 천천히 업데이트되는 일반 가중치
- **Fast Weights**: 최근 경험에 빠르게 반응해 일시적으로 업데이트되는 별도의 가중치

생물학적으로도 그럴듯한 아이디어예요. 뇌의 시냅스도 시간 스케일이 다양하잖아요 — 어떤 연결은 몇 달에 걸쳐 강화되고, 어떤 연결은 몇 초 만에 단기적으로 활성화되죠.

### 2016: Ba et al. 의 Fast Weights

[Jimmy Ba, Geoffrey Hinton 등 (2016)](https://arxiv.org/abs/1610.06258)이 "Using Fast Weights to Attend to the Recent Past"에서 이 개념을 현대 딥러닝에 적용했어요.

> "Fast weights can be used to store temporary memories of the recent past and they provide a neurally plausible way of implementing the type of attention to the past that has recently proved very helpful in sequence-to-sequence models."
> — Ba et al., 2016

이 논문에서 Fast Weight는 최근 과거에 대한 "임시 메모리" 역할을 하는데, 이게 어텐션 메커니즘과 굉장히 닮아 있어요.

### TTT와 Fast Weights의 관계

TTT는 이 Fast Weights 아이디어를 한층 더 발전시킨 거예요.

> "The general idea of fast weights is to update the parameters of a 'fast' model on the most relevant data, as opposed to a 'slow' model on all data. In TTT, the most relevant data can be the test instance itself, where the update is performed without human supervision at test time."

즉, TTT는 "테스트 데이터 자체가 가장 관련성 높은 데이터니까, 그걸로 실시간 업데이트를 해버리자"는 거예요.

---

## 3. TTT의 핵심 아이디어

### "히든 스테이트가 학습 모델이다"

[Yu Sun et al. (2024)](https://arxiv.org/abs/2407.04620)의 핵심 아이디어는 단순하지만 파격적이에요:

**RNN의 히든 스테이트 `h_t`를 그냥 벡터로 두지 말고, 아예 작은 ML 모델(가중치 `W_t`)로 만들자.**

그러면 업데이트 규칙도 그냥 손으로 설계한 수식이 아니라, **자기지도학습(self-supervised learning)의 경사하강법 한 스텝**이 되는 거죠.

```
# 기존 RNN
h_t = f(h_{t-1}, x_t)   # 고정된 함수로 업데이트

# TTT Layer
W_t = W_{t-1} - η ∇ℓ(W_{t-1}; x_t)  # 경사하강법으로 업데이트
output_t = f(x_t; W_t)              # W_t를 써서 출력
```

### 자기지도학습 목적함수

TTT에서 쓰는 자기지도학습 손실함수는 멀티뷰 재구성(multi-view reconstruction) 방식이에요:

```
ℓ(W; x_t) = ||f(θ_K · x_t; W) - θ_V · x_t||²
```

- **θ_K** (키 프로젝션): 내부 모델의 입력으로 쓰는 뷰
- **θ_V** (밸류 프로젝션): 재구성 타겟 뷰
- **θ_Q** (쿼리 프로젝션): 최종 예측에 쓰는 뷰

이 세 프로젝션은 외부 루프(outer loop)에서 학습돼요. 즉, **재구성 과제 자체도 학습되는 거예요.**

### 이중 루프(Bilevel) 최적화

```
┌─────────────────────────────────────────────────────────┐
│ 외부 루프 (Outer Loop) - 학습 시                         │
│  · 다음 토큰 예측 손실로 θ_K, θ_V, θ_Q 등을 학습         │
│  · 내부 루프의 '자기지도 과제'가 뭘 배울지 방향 설정       │
└──────────────────────┬──────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────┐
│ 내부 루프 (Inner Loop) - 추론 시                         │
│  · 각 토큰 x_t에 대해 자기지도 손실로 W_t를 업데이트      │
│  · 이 W_t가 곧 히든 스테이트 역할                        │
└─────────────────────────────────────────────────────────┘
```

학습 때 외부 루프가 "어떻게 배워야 추론에 도움이 될지"를 미리 메타학습(meta-learning)해 두기 때문에, 추론 때 내부 루프가 새 시퀀스에 빠르게 적응할 수 있어요.

### 미니배치 TTT와 듀얼 폼

순수하게 토큰 하나씩 처리하면 GPU 병렬화가 안 돼서 느려요. 그래서 TTT는 **미니배치(보통 b=16 토큰)**를 단위로 경사하강법을 적용해요.

더 나아가, **듀얼 폼(Dual Form)**을 사용하면 중간 가중치 W_t를 실제로 계산하지 않고도 출력을 도출할 수 있어요. 이게 벽시계 시간(wall-clock time) 기준 **5배 이상 속도 향상**을 가져와요.

---

## 4. TTT-Linear & TTT-MLP

### TTT-Linear

내부 모델 f가 단순 선형 변환인 경우예요:

```python
f_linear(x) = W @ x
```

흥미로운 점이 있어요 — 이론적으로 TTT-Linear(배치 경사하강법 사용)는 **선형 어텐션(Linear Attention)과 수학적으로 동치**임이 증명됐어요. 이건 TTT 프레임워크가 기존 아키텍처들을 통합하는 시각을 제공한다는 것을 보여줘요.

### TTT-MLP

내부 모델 f가 2층 MLP인 경우예요:

```python
f_mlp(x) = W2 @ gelu(W1 @ x)  # 4배 확장 차원
# 최종 출력: x + LayerNorm(f_mlp(x))  # 잔차 연결 포함
```

표현력은 훨씬 뛰어나지만, 히든 스테이트 크기가 커지면서 메모리 I/O 병목이 생길 수 있어요.

### 실험 결과

[Yu Sun et al. (2024)](https://arxiv.org/abs/2407.04620)의 실험 결과를 보면:

| 모델 크기 | 컨텍스트 | TTT-Linear | TTT-MLP | Mamba | Transformer |
|----------|---------|-----------|---------|-------|-------------|
| 125M | 2k | 경쟁력 있음 | 경쟁력 있음 | 기준선 | 기준선 |
| 760M | 8k | Mamba 초과 | 최상 | 16k 이후 정체 | 유사 |
| 1.3B | 32k | Transformer와 동등 | Transformer 초과 | 성능 정체 | 기준선 |

> "Similar to Transformer, TTT-Linear and TTT-MLP can keep reducing perplexity by conditioning on more tokens, while Mamba cannot after 16k context."
> — Yu Sun et al., 2024

---

## 5. Titans: 구글의 장기 메모리 아키텍처

2024년 12월 31일, Google DeepMind의 Ali Behrouz, Peilin Zhong, Vahab Mirrokni가 [Titans: Learning to Memorize at Test Time](https://arxiv.org/abs/2501.00663)을 발표했어요.

### 세 가지 메모리 모듈

Titans는 인간의 기억 체계를 모방한 세 가지 모듈을 결합해요:

```
┌──────────────────────────────────────────────────────────┐
│                      Titans Architecture                  │
├───────────────┬─────────────────────┬────────────────────┤
│ Core Module   │ Long-Term Memory    │ Persistent Memory  │
│ (단기 기억)    │ (장기 기억)          │ (영구 지식)         │
│               │                     │                    │
│ 제한된 윈도우  │ 신경망 기반          │ 학습 가능하지만     │
│ 어텐션        │ 테스트 타임 학습      │ 데이터 독립적       │
└───────────────┴─────────────────────┴────────────────────┘
```

### 테스트 타임 메모리 학습

Titans의 핵심은 장기 메모리 모듈이에요. **컨텍스트 윈도우를 데이터셋처럼 취급**하고, 들어오는 토큰에 대해 미니 경사하강법 루프를 실행해요.

특히 흥미로운 점은, 가장 새롭고 중요한 정보만 선택적으로 장기 메모리에 저장한다는 거예요. 이미 알고 있는 것(낮은 서프라이즈)은 굳이 다시 저장하지 않아요.

> "Titans selectively updates its long-term memory only with the most novel and context-breaking information, keeping the overall process fast and efficient."

### 성능

[Titans (2025)](https://arxiv.org/abs/2501.00663)는 다양한 도메인에서 Transformer와 최신 선형 순환 모델들을 앞지르는 성능을 보여줬어요:

- 언어 모델링
- 상식 추론(Common-sense reasoning)
- 게놈학(Genomics)
- 시계열 예측

그리고 **2M 토큰 이상의 컨텍스트**를 처리하면서 needle-in-haystack 작업에서 기준선 대비 높은 정확도를 기록했어요.

---

## 6. End-to-End TTT와 LaCT

### E2E-TTT: 진짜 엔드-투-엔드

2025년 12월, [Arnuv Tandon, Karan Dalal, Xinhao Li 등 (2025)](https://arxiv.org/abs/2512.23675) 14명의 연구자가 End-to-End TTT를 발표했어요.

핵심 아이디어는 이래요:

- **테스트 타임**: 다음 토큰 예측 자체를 자기지도 목표로 사용 (별도의 재구성 손실 없이)
- **학습 타임**: 메타러닝으로 모델의 시작점 최적화

이렇게 하면 학습 목표와 테스트 목표가 완전히 일치(엔드-투-엔드)하는 거예요.

**성능**:
- 3B 파라미터, 164B 토큰 학습 기준으로 풀 어텐션 Transformer와 동등한 스케일링
- **128K 컨텍스트에서 풀 어텐션 대비 2.7배 빠른 추론**
- **2M 컨텍스트에서 풀 어텐션 대비 35배 빠른 추론**

> "The researchers suggest their results indicate that the research community might finally arrive at a basic solution to long context in 2026."

### LaCT: 대형 청크로 GPU 활용률 높이기

TTT의 고질적인 문제가 있어요. 기존 TTT 구현은 GPU 활용률이 **5% 미만**이에요. 왜냐면 토큰 16~64개씩 미니배치를 처리하면서 빈번하게 가중치를 업데이트하는데, 이게 GPU 병렬화에 맞지 않거든요.

[Test-Time Training Done Right (LaCT, 2025)](https://arxiv.org/abs/2505.23884)은 이걸 해결해요:

- 청크 크기를 **2048 ~ 1M 토큰**까지 크게 늘려서 GPU 병렬화 극대화
- 청크 내에서 로컬 의존성은 윈도우 어텐션으로 처리
- GPU 활용률 **70% 이상** 달성 (A100 기준)

```
기존 TTT: 청크 크기 16-64 → GPU 활용률 <5%
LaCT:     청크 크기 2048-1M → GPU 활용률 >70%
```

**검증된 도메인**:
- 소설 뷰 합성(Novel View Synthesis)
- 언어 모델링
- 자동회귀 비디오 확산(Auto-regressive Video Diffusion)

---

## 7. TTT vs. Transformer Attention: 비교 분석

### 복잡도 비교

| 항목 | Transformer (Full Attention) | RNN (예: Mamba) | TTT Layer |
|------|------------------------------|-----------------|-----------|
| 컨텍스트별 복잡도 | O(n²) | O(n) | O(n) |
| 히든 스테이트 | KV Cache (n에 비례) | 고정 크기 벡터 | 학습 가능한 모델 |
| 긴 컨텍스트 성능 | 뛰어남 | 16k+ 이후 정체 | 계속 향상 |
| 추론 메모리 | KV Cache 증가 | 일정 | 일정 (W_t 크기) |

### TTT의 장점

1. **선형 복잡도 + 긴 컨텍스트 표현력**: Mamba처럼 빠르면서도 Transformer처럼 긴 컨텍스트에서 성능이 유지돼요.
2. **적응성**: 새로운 시퀀스 패턴에 자동으로 적응하는 히든 스테이트
3. **메모리 효율**: KV Cache 없이도 긴 시퀀스 처리 가능
4. **이론적 통합**: TTT 프레임워크 아래 선형 어텐션, Self-Attention 등이 통합

### TTT의 단점

1. **GPU 활용률 문제**: 기존 구현에서 병렬화가 어려워 <5% GPU 활용률 (LaCT로 일부 해결)
2. **메모리 I/O 병목**: TTT-MLP처럼 큰 내부 모델은 메모리 대역폭 문제
3. **훈련 복잡성**: 이중 루프 최적화(bilevel optimization)이 학습을 복잡하게 만듦
4. **성숙도 부족**: Transformer에 비해 구현체와 생태계가 아직 부족

### Self-Attention과의 이론적 연결

흥미롭게도, TTT 논문은 비모수 학습기(Nadaraya-Watson estimator)를 내부 모델로 쓰면 **Self-Attention과 수학적으로 동치**임을 증명했어요. 즉, Transformer도 TTT의 특수한 케이스로 볼 수 있는 거예요!

```
TTT 프레임워크
├── 선형 내부 모델 → 선형 어텐션 (Linear Attention)
├── 비모수 학습기 → Self-Attention
└── MLP 내부 모델 → 새로운 TTT-MLP (더 강력)
```

---

## 8. TTT 생태계: 관련 아키텍처들

### DeltaNet과 GatedDeltaNet

[DeltaNet](https://sustcsonglin.github.io/blog/2024/deltanet-1/)은 Fast Weight 관점에서 선형 어텐션을 재해석한 모델이에요. 델타 규칙(Delta Rule)을 써서 이전 키-밸류 연관관계를 선택적으로 지우고 새로 업데이트해요.

[Gated DeltaNet (ICLR 2025)](https://arxiv.org/abs/2412.06464)은 여기에 Mamba2의 게이팅을 결합했어요:
- 게이팅: 빠른 메모리 삭제
- 델타 규칙: 정밀한 업데이트

```
GatedDeltaNet 결과 (1.3B 파라미터, H100):
- Wiki 당혹도(Perplexity): 16.42 (Mamba2: 16.56)
- 상식 추론 평균 정확도: 55.32% (Mamba2: 54.89%)
- 처리량: 45K 토큰/초
```

### Video Stream TTT

[Test-Time Training on Video Streams (2023)](https://arxiv.org/abs/2307.05014)는 TTT를 컴퓨터 비전의 스트리밍 설정에 적용했어요.

비디오 프레임이 시간 순서로 들어올 때, 현재 모델을 이전 모델로 초기화한 뒤 현재 프레임과 직전 몇 프레임으로 학습하는 "온라인 TTT" 방식이에요.

성능 향상:
- 인스턴스 세그멘테이션: 2.2배 이상
- 파노라마 세그멘테이션: 1.5배 이상

### HGRN2 (Hierarchical Gated Recurrent Neural Network)

HGRN2는 게이트 순환 메커니즘과 상태 확장을 결합한 모델이에요. 하이브리드 구성(6:1 선형-풀 어텐션 비율)에서 강력한 성능을 보여요.

---

## 9. 한계와 과제

### 기술적 한계

**1. 하드웨어 비효율성**
기존 TTT 구현의 GPU 활용률이 5% 미만이라는 건 꽤 심각한 문제예요. LaCT가 어느 정도 해결하긴 했지만, Transformer의 고도로 최적화된 CUDA 커널에 비하면 아직 갈 길이 멀어요.

**2. 이중 루프 학습의 복잡성**
메타러닝을 포함한 이중 루프 최적화는 학습 시 훨씬 복잡해요. 하이퍼파라미터 조정도 까다롭고요.

**3. TTT-MLP의 메모리 대역폭 병목**
내부 모델이 크면 클수록 W_t를 읽고 쓰는 데 메모리 대역폭이 많이 필요해요. 고속 HBM(High Bandwidth Memory)이 필수.

**4. 이론적 이해 부족**
TTT가 왜 잘 되는지에 대한 이론적 분석이 아직 부족해요. 어떤 유형의 시퀀스에서 가장 유리한지도 완전히 밝혀지지 않았어요.

### 실용적 한계

**1. 생태계 미성숙**: Transformer에 비해 라이브러리, 프레임워크, 사전학습 모델이 훨씬 부족
**2. 벤치마크 부족**: 다양한 태스크에 걸친 체계적인 비교 연구가 아직 부족
**3. 학습 불안정성**: 자기지도 과제와 주 과제의 정렬이 잘못되면 성능이 크게 떨어질 수 있음

---

## 10. 향후 전망

TTT 연구는 2025~2026년에 걸쳐 급격히 성숙해지고 있어요. 몇 가지 흥미로운 방향들이 보여요:

### 하이브리드 아키텍처

완전한 TTT 모델보다는 Transformer + TTT 레이어 혼합이 현실적인 방향으로 보여요. 단기 의존성은 로컬 어텐션, 장기 의존성은 TTT로 처리하는 식이죠.

### 멀티모달 TTT

LaCT가 언어, 비디오, 3D 뷰 합성에 걸쳐 검증된 것처럼, TTT는 멀티모달 시퀀스 처리에서 강점을 가질 것으로 보여요.

### 효율적인 구현체

GPU 활용률 문제는 계속 개선될 거예요. 전용 CUDA 커널, 하드웨어 인식 청크 전략 등이 연구되고 있어요.

### 장기 컨텍스트의 해법

E2E-TTT 연구자들은 "2026년에 긴 컨텍스트 문제의 기본적인 해법에 도달할 수 있을 것"이라고 했어요. TTT가 그 해법의 중심에 있을 가능성이 높아요.

> "The researchers suggest their results indicate that the research community might finally arrive at a basic solution to long context in 2026."
> — Tandon et al., End-to-End TTT for Long Context, 2025

---

## 결론

Test Time Training과 Fast Weights는 단순한 아이디어 하나에서 출발해요: "추론할 때도 배울 수 있다면?" 이 아이디어가 1987년 Hinton의 Fast Weights에서 싹을 틔워, 2024~2025년의 TTT-Linear, Titans, E2E-TTT, LaCT로 이어지는 연구 흐름을 만들었어요.

아직 성숙하지 않은 분야이고 해결해야 할 과제도 많지만, 긴 컨텍스트 처리라는 핵심 문제에서 Transformer와 RNN의 장점을 동시에 취할 수 있다는 가능성은 정말 매력적이에요. 앞으로 몇 년이 TTT에게 결정적인 시기가 될 것 같아요.

---

## 참고 문헌

1. [Yu Sun et al. (2024). Learning to (Learn at Test Time): RNNs with Expressive Hidden States. arXiv:2407.04620](https://arxiv.org/abs/2407.04620)
2. [Ali Behrouz, Peilin Zhong, Vahab Mirrokni (2025). Titans: Learning to Memorize at Test Time. arXiv:2501.00663](https://arxiv.org/abs/2501.00663)
3. [Arnuv Tandon et al. (2025). End-to-End Test-Time Training for Long Context. arXiv:2512.23675](https://arxiv.org/abs/2512.23675)
4. [Tianyuan Zhang et al. (2025). Test-Time Training Done Right (LaCT). arXiv:2505.23884](https://arxiv.org/abs/2505.23884)
5. [Jimmy Ba, Geoffrey Hinton et al. (2016). Using Fast Weights to Attend to the Recent Past. arXiv:1610.06258](https://arxiv.org/abs/1610.06258)
6. [Geoffrey Hinton & David Plaut (1987). Using Fast Weights to Deblur Old Memories. CogSci 1987](https://www.cs.toronto.edu/~hinton/absps/fastweights87.pdf)
7. [Songlin Yang et al. (2024). Gated Delta Networks: Improving Mamba2 with Delta Rule. arXiv:2412.06464](https://arxiv.org/abs/2412.06464)
8. [Yu Sun et al. (2023). Test-Time Training on Video Streams. arXiv:2307.05014](https://arxiv.org/abs/2307.05014)
9. [Yingfa Chen (2025). The Rise of Test-Time Training.](https://chen-yingfa.github.io/research_posts/2025-rise-of-ttt/)
10. [Google Research Blog (2025). Titans + MIRAS: Helping AI have long-term memory.](https://research.google/blog/titans-miras-helping-ai-have-long-term-memory/)
