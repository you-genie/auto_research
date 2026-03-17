# Yann LeCun과 World Models 완전 정복: "LLM은 AGI가 아니다"를 외치는 남자의 진짜 비전

> "There's absolutely no way that autoregressive LLMs, the type that we know today, will reach human intelligence." — Yann LeCun, CES 2025

솔직히 말하면, AI 업계에서 가장 유명한 '반골'이 있어요. OpenAI가 GPT-4로 세상을 떠들썩하게 만들고, 모두가 LLM 스케일링에 환호할 때 혼자 "그거 틀렸어"를 외치는 사람이죠. 바로 [Yann LeCun](https://en.wikipedia.org/wiki/Yann_LeCun)이에요. 튜링상을 받은 딥러닝의 아버지 중 한 명이 왜 현재 AI의 주류인 LLM을 그토록 강하게 비판하는 걸까요? 그리고 그가 제안하는 대안인 **World Models**는 뭔데요?

2026년 3월, LeCun은 META를 떠나 [AMI Labs](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/)를 설립하고 무려 **10억 3천만 달러 (약 1.4조 원)** 의 시드 투자를 받았어요. 이게 단순한 스타트업 창업이 아니라 AI의 방향성을 두고 벌어지는 진짜 큰 싸움의 시작이거든요. 한번 제대로 파봅시다.

---

## 1. Yann LeCun은 누구인가요?

### 딥러닝의 아버지

[Yann André LeCun](https://amturing.acm.org/award_winners/lecun_6017366.cfm)은 1960년 7월 8일 프랑스 파리 근교에서 태어났어요. 아버지가 엔지니어였던 덕분에 어릴 때부터 전자기기를 뜯고 조립하면서 컸다고 하죠.

- **학력**: ESIEE Paris 공학 학위(1983), 파리 피에르-마리 퀴리 대학 박사(1987)
- **경력**: Bell Labs → NYU(Courant Institute 교수) → Facebook/META AI Research 창립 이사
- **주요 성과**: CNN(합성곱 신경망) 개발, MNIST 손글씨 인식 시스템, LeNet

> "LeCun developed convolutional neural networks, a foundational principle in the field, and in the late 1980s, while working at the University of Toronto and Bell Labs, he was the first to train a convolutional neural network system on images of handwritten digits." — ACM Turing Award 공식 설명

즉, 우리가 지금 쓰는 이미지 인식, 얼굴 인식, 자율주행 카메라 시스템 등등 CNN이 들어가는 모든 것의 기반을 만든 사람이에요. 그냥 유명인이 아니라 진짜 실력자죠.

### 튜링상 수상 (2018)

[2018년 ACM A.M. 튜링상](https://awards.acm.org/about/2018-turing)은 LeCun, [Yoshua Bengio](https://yoshuabengio.org/), [Geoffrey Hinton](https://geoffreyhinton.ca/) 세 사람이 공동 수상했어요. ACM이 이들을 "딥러닝 혁명의 아버지들"이라고 불렀죠. 튜링상은 컴퓨터 과학의 노벨상이라고 불리는 최고 권위의 상이에요.

### META에서의 12년

LeCun은 2013년부터 2025년 11월까지 META(구 Facebook)에서 일했어요. 처음 5년은 [FAIR(Facebook AI Research)](https://ai.meta.com/research/)의 창립 이사로, 이후 7년은 META의 수석 AI 과학자(Chief AI Scientist)로 활동했죠.

---

## 2. AMI Labs: "세상을 이해하는 AI"를 만들다

### META 퇴사와 새 출발

2025년 11월 18일, LeCun은 META를 떠난다고 공식 발표했어요. META가 Scale AI 창업자 [Alexandr Wang](https://techcrunch.com/2025/12/19/yann-lecun-confirms-his-new-world-model-startup-reportedly-seeks-5b-valuation/)을 새 AI 총괄(Chief AI Officer)로 임명하면서 전략이 LLM 강화 쪽으로 기울었고, LeCun의 비전과 맞지 않게 된 거죠.

### AMI Labs란?

[AMI(Advanced Machine Intelligence) Labs](https://builtin.com/articles/ami-labs-yann-lecun)는 프랑스어로 "친구(ami)"라는 뜻을 담고 있어요. 본사는 파리에 있고, LeCun은 집행 이사장(Executive Chairman)을 맡고 있어요.

**경영진 라인업이 진짜 화려한데요:**

| 역할 | 이름 | 이전 경력 |
|------|------|-----------|
| CEO | Alexandre LeBrun | 프랑스 헬스테크 스타트업 Nabla 창업자 |
| Chief Science Officer | Saining Xie | META AI Research 연구자 |
| Chief Research & Innovation Officer | Pascale Fung | 홍콩과기대 교수 |
| VP of World Models | Michael Rabbat | META AI 연구자 |
| COO | Laurent Solly | META 유럽 부사장 |

### 사상 최대 규모 시드 투자

[2026년 3월, AMI Labs는 $1.03억 달러 규모의 시드 라운드를 마감했어요](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/). **유럽 스타트업 역사상 최대 규모의 시드 투자**예요.

투자자 명단도 화려하죠:
- 주요 투자사: Cathay Innovation, Greycroft, Hiro Capital, HV Capital, **Bezos Expeditions**(제프 베이조스 펀드)
- 개인 투자자: Tim & Rosemary Berners-Lee(WWW 발명가 부부), Jim Breyer, **Mark Cuban**, Mark Leslie, Xavier Niel, **Eric Schmidt**(전 구글 CEO)

기업 가치평가(pre-money)는 **$35억 달러**예요. 제품도 없는 스타트업에 이런 투자가 몰린다는 게... LeCun의 이름값이 어마어마하다는 거죠.

> "We expect 'world models' to become a buzzword across the industry in the coming months, with many companies borrowing the term for fundraising purposes." — Alexandre LeBrun, AMI Labs CEO

---

## 3. LeCun이 LLM을 싫어하는 이유

### "자동회귀 LLM은 인간 지능에 못 도달한다"

LeCun의 핵심 주장을 딱 한 줄로 요약하면 이래요:

> "There's absolutely no way that autoregressive LLMs, the type that we know today, will reach human intelligence." — Yann LeCun, CES 2025

왜 그럴까요? LeCun이 꼽은 LLM의 4가지 근본적 한계를 살펴볼게요.

### 한계 1: 토큰 예측의 오류 누적

[오토회귀(Autoregressive) 방식](https://www.marktechpost.com/2025/02/11/are-autoregressive-llms-really-doomed-a-commentary-on-yann-lecuns-recent-keynote-at-ai-action-summit/)은 이전 토큰들을 보고 다음 토큰을 예측하는 방식이에요. 문제는 각 토큰 예측마다 오류 확률이 존재하고, 이 오류가 독립적으로 쌓인다면 전체 답변이 올바를 확률은 **지수적으로 감소**한다는 거예요.

LeCun의 설명:

> "Because of autoregressive prediction, every time a model produces a token there is a probability it diverges from reasonable answers, and if errors are independent across tokens, the probability of staying within correct answers decreases exponentially." — Yann LeCun

이게 바로 **환각(hallucination)** 문제의 근원이에요.

### 한계 2: 물리 세계를 이해 못 함

LeCun은 자주 고양이 비유를 써요:

> "Any housecat can plan very highly complex actions and they have causal models of the world." — Yann LeCun

집고양이도 할 수 있는 일 — 컵을 치면 떨어진다는 걸 알고, 좁은 공간을 어떻게 통과할지 계획하는 것 — 을 LLM은 못 한다는 거죠. 물리적 세계에 대한 **인과적 모델(causal model)** 이 없으니까요.

### 한계 3: 지속적 기억 없음

LLM은 컨텍스트 윈도우 안에서만 기억해요. 대화가 끝나면 다 잊죠. 진짜 지능이라면 **영구적 기억(persistent memory)** 이 있어야 하는데요.

### 한계 4: 스케일링은 한계에 도달하고 있다

[스케일링 법칙(Scaling Laws)](https://fortune.com/2025/02/19/generative-ai-scaling-agi-deep-learning/)이 수확 체감(diminishing returns)에 접어들고 있어요. LeCun의 표현으로는:

> "Scaling is saturating."

실제로 2024-2025년 들어 모델 크기를 늘려도 성능 향상이 예전만 못하다는 연구들이 나오고 있죠.

---

## 4. World Models란 무엇인가요?

### 핵심 개념

**World Model(세계 모델)**이란 AI 에이전트가 환경의 작동 방식을 내부적으로 표현하는 모델이에요. 쉽게 말하면, "AI의 머릿속에 있는 세상 시뮬레이터"죠.

모델 기반 강화학습(Model-Based RL)에서 유래한 개념인데, 에이전트가 정책(policy)만 배우는 게 아니라 **환경 자체를 이해하는 모델**을 함께 학습해요. 덕분에 상상 속에서 미래를 시뮬레이션하고 계획을 세울 수 있죠.

### LLM vs. World Model 비교

| 특성 | 오토회귀 LLM | World Model (JEPA 방식) |
|------|-------------|------------------------|
| 학습 목표 | 다음 토큰 예측 | 표현 공간에서 미래 상태 예측 |
| 물리 이해 | 텍스트 패턴에서 간접 추론 | 물리적 인과관계 직접 모델링 |
| 불확실성 처리 | 확률적 토큰 분포 | 잠재 변수로 모호성 포착 |
| 계획 능력 | 제한적 (chain-of-thought 의존) | 계층적 계획 가능 |
| 샘플 효율성 | 낮음 (엄청난 데이터 필요) | 높음 (압축적 표현) |
| 환각 경향 | 높음 | 낮음 (공간 내 일관성) |

### DreamerV3: 다른 접근법의 World Model

META의 JEPA 외에도, Google DeepMind의 [Danijar Hafner가 개발한 DreamerV3](https://arxiv.org/abs/2301.04104)도 유명한 World Model이에요.

DreamerV3는 RSSM(Recurrent State Space Model)을 핵심으로 쓰는데요:
1. 감각 입력을 잠재 표현으로 압축
2. 잠재 공간에서 미래 상태 예측 (상상)
3. 상상 속 롤아웃으로 정책 최적화

실제로 DreamerV3는 **마인크래프트에서 다이아몬드를 처음부터 캐는 데 성공한 최초의 AI**였어요. 인간 데이터나 커리큘럼 없이요.

---

## 5. JEPA: LeCun의 핵심 아이디어

### "A Path Towards Autonomous Machine Intelligence" (2022)

2022년 6월, LeCun은 [OpenReview에 이 논문](https://openreview.net/pdf?id=BZ5a1r-kVsf)을 올렸어요. 정식 저널 논문이 아닌 "포지션 페이퍼"인데도 AI 커뮤니티에서 엄청난 주목을 받았죠. LeCun이 자신의 AI 비전을 가장 체계적으로 정리한 문서예요.

이 논문의 핵심 주장은 **자율적 지능 에이전트를 구축하기 위해 필요한 6가지 모듈**이에요:

1. **Configurator**: 다른 모듈의 목표와 동작 설정
2. **Perception**: 세계로부터 정보 수집
3. **World Model**: 세계의 상태와 미래 예측
4. **Cost/Reward**: 행동의 좋고 나쁨 평가
5. **Short-term Memory**: 현재 상태 추적
6. **Actor**: 실제 행동 결정

이 중 **World Model**이 핵심이에요. 나머지 모듈들이 World Model을 중심으로 작동하거든요.

### JEPA (Joint Embedding Predictive Architecture)

[JEPA](https://www.shaped.ai/blog/yann-lecun-a-path-towards-autonomous-machine-intelligence)는 LeCun이 제안하는 World Model의 구체적인 아키텍처예요.

**핵심 아이디어:** 입력 공간(pixel space)에서 직접 예측하지 말고, **표현 공간(representation space)** 에서 예측하자.

왜냐고요? 세상에는 본질적으로 예측 불가능한 세부 사항들이 엄청 많아요. 영상의 모든 픽셀을 완벽하게 예측하려면 불필요한 정보(나무 잎사귀의 흔들림 등)까지 다 예측해야 해요. 대신 **의미 있는 표현(semantic representation)** 만 예측하면 훨씬 효율적이고 정확하죠.

JEPA의 수식으로 표현하면:
- `sx = Enc(x)`: 입력 x의 표현
- `sy = Enc(y)`: 목표 y의 표현
- `ŝy = Pred(sx, z)`: sx와 잠재변수 z로 sy 예측
- 손실: `D(sy, ŝy)` 최소화

여기서 `z`는 **잠재 변수(latent variable)** 로, 예측의 불확실성을 처리해줘요. "고양이가 왼쪽으로 갈 수도 있고 오른쪽으로 갈 수도 있다"는 상황에서 어느 쪽인지를 z가 결정하는 거죠.

> "The main attraction of JEPAs is that they can be trained with non-contrastive methods. The basic principle of such training is that (1) sx should be maximally informative about x; (2) sy should be maximally informative about y; (3) sy should be easily predictable from sx; (4) z should have minimal information content." — Shaped.ai, LeCun JEPA 해설

### Energy-Based Models (EBM)

JEPA의 이론적 기반은 [에너지 기반 모델(EBM)](https://cs.nyu.edu/~yann/research/ebm/)이에요. EBM은 각 변수 구성에 스칼라 에너지 값을 할당해요.

> "An energy-based model is a scalar-valued energy function: E(W, Y, X), where X is the input, Y the variable to be predicted, and W is the parameter vector. Inference consists in clamping the value of observed variables and finding configurations of the remaining variables that minimize the energy." — LeCun, EBM Tutorial

쉽게 말하면, **좋은 상태(타당한 예측) = 낮은 에너지, 나쁜 상태(말도 안 되는 예측) = 높은 에너지**예요. 학습은 관찰된 데이터의 에너지를 낮추고, 관찰되지 않은 데이터의 에너지를 높이는 방향으로 진행되죠.

---

## 6. META의 JEPA 구현체들

### I-JEPA (Image JEPA, 2023)

[I-JEPA](https://www.turingpost.com/p/jepa)는 JEPA를 이미지에 적용한 첫 번째 구현체예요 (Assran et al., 2023).

**작동 방식:**
1. 이미지를 N개의 겹치지 않는 패치로 분할
2. 큰 컨텍스트 블록과 작은 타겟 블록 샘플링
3. Vision Transformer(ViT)로 컨텍스트 인코딩
4. Predictor가 타겟 블록의 표현 예측
5. EMA(Exponential Moving Average)로 타겟 인코더 붕괴 방지

결과적으로 I-JEPA는 픽셀 레벨 재구성 없이도 강력한 이미지 표현을 학습해요.

### V-JEPA (Video JEPA, 2024)

[V-JEPA](https://ai.meta.com/research/publications/v-jepa-2-self-supervised-video-models-enable-understanding-prediction-and-planning/)는 I-JEPA를 3D(공간+시간)로 확장했어요.

- **입력**: 약 2.1초 비디오 (64프레임)
- **패치**: 16×16×2 크기의 시공간 패치
- **마스킹**: 2D 마스크를 시간 차원에 반복 적용
- **학습 데이터**: 22M개 비디오

성능:
- Kinetics-400, Something-Something-v2, ImageNet1K에서 경쟁력 있는 결과
- 이전 선도 비디오 모델들과 동등하거나 능가

### V-JEPA 2 (2025-2026)

[V-JEPA 2](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)는 한 단계 더 나아갔어요. **12억 파라미터** 모델로, 진짜 World Model로서의 역할을 목표로 해요.

**학습 규모:**
- 사전학습: 100만 시간 이상의 비디오 + 100만 장 이미지
- 행동 조건부 학습: 단 62시간의 로봇 데이터

**성능 하이라이트:**
- Something-Something v2: **77.3 top-1 accuracy** (액션 인식)
- Epic-Kitchens-100: **39.7 recall@5** (인간 행동 예측, SOTA)
- PerceptionTest: **84.0** (비디오 QA)
- TempCompass: **76.9** (시간적 이해)
- 로봇 제어 실험: **65~80% 성공률**

**새로운 물리 추론 벤치마크:**
- **IntPhys 2**: 물리적으로 타당한 vs 불가능한 시나리오 구별
- **MVPBench**: 비디오-언어 모델의 물리 이해 평가
- **CausalVQA**: 인과관계 이해 및 미래 예측

(참고: 인간은 이 벤치마크에서 85~95% 정확도를 보이지만, 현재 모델들은 아직 격차가 있어요.)

### MC-JEPA (Motion & Content JEPA)

[MC-JEPA](https://www.thesingularityproject.ai/p/yann-lecuns-joint-embedding-predictive)는 동작(Motion)과 내용(Content)을 동시에 학습하는 변형 모델이에요. 학습된 콘텐츠 특징이 동작을 포함하고, 그 역도 성립해서 — 시맨틱 세그멘테이션과 광학 흐름(optical flow) 벤치마크 모두에서 지도 학습 없이도 좋은 성능을 냈어요.

### VL-JEPA (Vision-Language JEPA, 2024)

[VL-JEPA](https://arxiv.org/abs/2512.10942)는 비전과 언어를 통합한 모델이에요.

> "On eight video classification and eight video retrieval datasets, the average performance of VL-JEPA surpasses that of CLIP, SigLIP2, and Perception Encoder. Additionally, VL-JEPA achieves stronger performance while having 50% fewer trainable parameters compared to standard token-space VLM training." — VL-JEPA 논문 (arXiv:2512.10942)

CLIP, SigLIP2 같은 강력한 모델들을 파라미터는 절반만 쓰면서 이겼다는 게 인상적이죠?

---

## 7. Hierarchical Planning: 계층적 계획

LeCun의 자율 기계 지능 비전에서 또 하나의 핵심은 **계층적 계획(Hierarchical Planning)** 이에요.

### 왜 계층적이어야 하나요?

인간이 "파리에서 뉴욕까지 간다"는 계획을 세울 때를 생각해봐요:
1. **고수준 계획**: 비행기 타기
2. **중수준 계획**: 공항 가기 → 탑승 → 비행 → 도착
3. **저수준 계획**: 택시 잡기 → 탑승 수속 밟기 → ...

단일 레벨에서 "다음 동작은 무엇인가?"를 묻는 건 비효율적이에요. LeCun이 제안하는 **H-JEPA(Hierarchical JEPA)** 는 여러 추상화 레벨에서 동시에 계획을 세우는 구조예요.

> "JEPA and Hierarchical JEPA: a non-generative architecture for predictive world models that learn a hierarchy of representations." — LeCun의 "A Path Towards Autonomous Machine Intelligence"

---

## 8. 경쟁 World Model 연구

### Google DeepMind: Genie 시리즈

구글 딥마인드는 [Genie](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/) 시리즈로 World Model 경쟁에 뛰어들었어요.

**Genie 2 (2024년 12월 발표)**
- 단일 프롬프트 이미지에서 조작 가능한 3D 환경 생성
- 키보드+마우스로 인간 또는 AI 에이전트가 조작 가능
- 1인칭, 등각, 3인칭 등 다양한 시점 지원
- 10~20초 지속 가능한 일관된 세계 생성

[Genie 3 (2025년 8월 공개)](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)는 한 단계 더 나아갔어요:

> "Genie 3 is the first world model to allow interaction in real-time, while also improving consistency and realism compared to Genie 2. Genie 3 environments remain largely consistent for several minutes, with visual memory extending as far back as one minute ago." — Google DeepMind

- **해상도**: 720p
- **속도**: 24 FPS 실시간
- **일관성**: 몇 분간 유지
- **입력**: 텍스트 프롬프트로 동적 세계 생성

2026년 1월 Google AI Ultra 구독자에게 공개됐어요.

### Waymo: 자율주행용 World Model

[Waymo는 2026년 2월](https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation/) **Waymo World Model**을 발표했어요. Google DeepMind의 Genie 3를 기반으로 구축된, 자율주행 특화 World Model이에요.

> "The World Model changes that equation entirely. Traditional simulation has a fundamental limitation: it can only recreate what has already been observed. Rare events barely appear in real-world training data." — Waymo Blog

Waymo World Model의 핵심:
- 카메라 + LiDAR 데이터를 동시에 생성
- 실제로는 거의 일어나지 않는 **희귀 시나리오** (어린이가 갑자기 도로로 뛰어드는 상황 등) 합성
- 이를 통해 자율주행 시스템을 더 안전하게 훈련

Waymo는 2025년에 **1400만 건 이상의 실제 이동** 서비스를 제공했고, 2026년에 런던, 도쿄 등 20개 이상 도시로 확장할 계획이에요.

### Tesla: 내재화된 World Model

테슬라는 공식적으로 "World Model"이라고 부르진 않지만, 실제로 비슷한 접근을 쓰고 있어요. 50,000개 H100 GPU로 구성된 Cortex 클러스터에서 엔드-투-엔드 아키텍처로 훈련하고 있죠.

---

## 9. LeCun의 주장에 대한 비판적 시각

### 찬성 의견: "LeCun이 맞다"

1. **스케일링 포화**: 2024-2025년 실제로 스케일링 수익 체감이 관찰되고 있어요
2. **물리 이해 부재**: LLM이 물리 추론에 약하다는 건 여러 벤치마크로 확인됐어요
3. **샘플 비효율성**: GPT-4 수준의 모델 훈련에는 수조 토큰이 필요하지만 아기는 훨씬 적은 감각 경험으로 물리 법칙을 배워요

### 반대 의견: "LLM을 너무 무시한다"

1. **o1/o3의 등장**: OpenAI의 추론 모델들은 LeCun이 "불가능"하다고 했던 수학, 코딩, 과학 추론에서 놀라운 성능을 보여주고 있어요
2. **실용성**: 지금 당장 가치를 창출하는 건 LLM이에요. World Model은 아직 연구 단계죠
3. **멀티모달 발전**: GPT-4V, Gemini 등 멀티모달 LLM이 일부 물리 이해 능력을 보여주고 있어요

### 진짜 질문: "둘 다 필요한 거 아닐까?"

솔직히 이 논쟁의 가장 현명한 답은 "둘 다 필요하다"일 수 있어요. LLM의 언어 이해 능력 + World Model의 물리적 추론 = 더 강력한 시스템이 될 수 있거든요.

실제로 V-JEPA 2는 [LLM과 결합했을 때 비디오 QA에서 SOTA 성능](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)을 냈어요. **JEPA가 세계 이해를 담당하고, LLM이 언어 처리를 담당**하는 하이브리드 구조가 현실적인 방향일 수도 있죠.

---

## 10. 향후 전망

### AMI Labs의 계획

CEO Alexandre LeBrun은 "향후 6개월 내 'World Model'이 업계의 유행어가 될 것"이라고 예측했어요. 1조 원 넘는 투자를 받은 AMI Labs가 어떤 제품을 내놓을지가 진짜 관전 포인트죠.

### World Model의 로보틱스 적용

V-JEPA 2가 **62시간의 로봇 데이터만으로 65~80% 성공률**을 달성했다는 건 굉장히 인상적이에요. 로보틱스에서 데이터 효율성은 핵심 문제거든요. World Model이 로봇 훈련을 혁신할 가능성이 진짜 있어요.

### Waymo + Genie 3 = 자율주행의 미래?

Waymo가 Genie 3 기반의 World Model로 실제 서비스를 강화하고 있다는 건 단순한 연구가 아니라 **실제 상업적 적용**이 시작됐다는 신호예요.

---

## 마무리: 왜 지금 이게 중요한가요?

LeCun이 META를 떠나 AMI Labs를 차린 건 단순히 새 직장을 찾은 게 아니에요. 이건 **AI의 미래 방향성을 두고 벌어지는 진짜 큰 베팅**이에요.

- OpenAI, Anthropic, Google은 "LLM을 더 크고 강하게"
- LeCun과 AMI Labs는 "아니, 다른 아키텍처가 필요해"

둘 중 누가 맞을지는 아직 모르지만, 한 가지는 확실해요. 10억 달러 넘는 투자를 받았다는 건 **세상이 이 베팅을 진지하게 생각하고 있다**는 거예요.

World Models가 정말 AI의 다음 단계인지, 아니면 또 다른 AI 붐의 버블인지 — 2026년 지금, 그 답이 조금씩 나오기 시작하고 있어요.

---

## 참고문헌

1. [Yann LeCun - Wikipedia](https://en.wikipedia.org/wiki/Yann_LeCun)
2. [ACM A.M. Turing Award 2018](https://awards.acm.org/about/2018-turing)
3. [A Path Towards Autonomous Machine Intelligence (OpenReview, 2022)](https://openreview.net/pdf?id=BZ5a1r-kVsf)
4. [AMI Labs raises $1.03B - TechCrunch](https://techcrunch.com/2026/03/09/yann-lecuns-ami-labs-raises-1-03-billion-to-build-world-models/)
5. [MIT Technology Review: Yann LeCun's new venture](https://www.technologyreview.com/2026/01/22/1131661/yann-lecuns-new-venture-ami-labs/)
6. [V-JEPA 2 Blog - Meta AI](https://ai.meta.com/blog/v-jepa-2-world-model-benchmarks/)
7. [V-JEPA 2 Paper - arXiv](https://arxiv.org/abs/2506.09985)
8. [VL-JEPA Paper - arXiv](https://arxiv.org/abs/2512.10942)
9. [DreamerV3 - arXiv](https://arxiv.org/abs/2301.04104)
10. [Genie 2 - Google DeepMind](https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/)
11. [Genie 3 - Google DeepMind](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
12. [Waymo World Model](https://waymo.com/blog/2026/02/the-waymo-world-model-a-new-frontier-for-autonomous-driving-simulation/)
13. [Are Autoregressive LLMs Really Doomed? - MarkTechPost](https://www.marktechpost.com/2025/02/11/are-autoregressive-llms-really-doomed-a-commentary-on-yann-lecuns-recent-keynote-at-ai-action-summit/)
14. [JEPA Deep Dive - Rohit Bandaru](https://rohitbandaru.github.io/blog/JEPA-Deep-Dive/)
15. [Energy-Based Models - NYU](https://cs.nyu.edu/~yann/research/ebm/)
