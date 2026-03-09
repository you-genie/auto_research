# AI의 World Models: 환각하는 에이전트에서 실시간 현실 시뮬레이션까지 🌍🤖

*세계 모델 연구의 가장 흥미로운 논문들을 통한 여정 (2018-2025)*

---

## 요약 (TL;DR)

World model은 AI 시스템이 세계를 이해하고, 예측하고, 상호작용하기 위해 현실의 내부 표현을 구축하는 방법입니다. 단 7년 만에 우리는 환각된 게임 환경에서 작은 에이전트를 훈련시키는 것에서 DeepMind의 Genie 3가 24 FPS로 실시간 인터랙티브 3D 세계를 생성하는 것까지 발전했습니다. 정말 놀랍습니다.

---

## World Model이란 대체 뭘까?

여러분이 하루를 어떻게 보내는지 생각해보세요. 커피 잔을 들 때 의식적으로 물리학에 대해 생각할 필요가 없습니다. 여러분의 뇌는 물체가 어떻게 행동하는지, 사물이 어디에 있는지, 그리고 상호작용할 때 무슨 일이 일어나는지에 대한 내부 모델을 가지고 있습니다. 연구자들이 AI 시스템에 제공하려는 것이 바로 이것입니다.

**World model은 AI가 다음을 할 수 있게 해줍니다:**
- 세계의 현재 상태 이해
- 다음에 무슨 일이 일어날지 예측
- 시나리오를 상상하고 행동 계획
- 시뮬레이션된 경험으로부터 학습

단순히 입력에 반응하는 대신, 세계 모델을 가진 에이전트는 *앞을 내다보고* 결과를 *시뮬레이션*할 수 있습니다. 멋지지 않나요?

---

## 타임라인: 어떻게 여기까지 왔나

### 2018: 기초의 시작 🏗️

David Ha와 Jürgen Schmidhuber의 **[World Models](https://worldmodels.github.io/)**이 NeurIPS 2018에서 시작을 알렸습니다. 그들의 핵심 통찰? 에이전트를 자신의 환각 속에서 훈련시키는 것입니다.

그들이 한 일:
1. 강화학습 환경(예: 자동차 경주)을 모델링하는 생성 신경망 훈련
2. 환경을 시공간 표현으로 압축
3. 이 *학습된* 환경 내에서 에이전트 훈련
4. 정책을 실제 환경으로 전이

그리고 실제로 작동했습니다! 상상된 세계에서 훈련된 에이전트가 실제 작업을 수행할 수 있었습니다. 이 논문은 그 이후 모든 것의 기초가 되었습니다.

### 2023: 범용화의 시작 🚀

Danijar Hafner와 동료들의 **[DreamerV3](https://github.com/danijar/dreamerv3)**는 "성배" 순간이었습니다. **Nature**(*그* Nature입니다)에 게재된 이 논문은 **단일 알고리즘**이 작업별 조정 없이 150개 이상의 다양한 작업을 마스터할 수 있음을 보여주었습니다.

획기적인 점? 각 작업에 대해 별도의 에이전트를 훈련하는 대신, DreamerV3는:
- 환경의 일반 모델 학습
- 미래 시나리오 상상
- 이러한 상상된 미래를 탐색하여 계획
- 게임, 로보틱스, 제어 작업 전반에서 작동

아, 그리고 마인크래프트에서 **처음부터** 다이아몬드를 수집했습니다 - 이전에는 사람의 시연과 신중한 커리큘럼 설계가 필요했던 작업을 DreamerV3는 그냥... 알아냈습니다.

### 2024: 산업계의 각성 💥

이때부터 상황이 미쳐 돌아가기 시작했습니다. 세 산업 거대 기업이 폭탄을 터뜨렸습니다:

#### **Sora** (OpenAI, 2024년 2월)

OpenAI의 Sora는 세계 모델로 마케팅되지 않았습니다 - 텍스트-비디오 생성기였습니다. 하지만 [기술 보고서](https://openai.com/index/video-generation-models-as-world-simulators/)는 그들이 더 크게 생각하고 있음을 드러냈습니다: "세계 시뮬레이터로서의 비디오 생성 모델."

Sora가 보여준 것:
- 창발적 객체 영속성 (가려져도 사라지지 않음)
- 물리 이해 (대부분... 바이럴했던 "Sora 실패" 영상들이 한계를 보여주긴 했지만)
- 시공간적 일관성

철학: 비디오 생성을 확장하는 것은 범용 물리적 세계 시뮬레이터를 구축하는 길입니다. 대단하죠.

2024년 12월, Sora Turbo가 ChatGPT 사용자들에게 출시되었고, 훨씬 빠르고 제어 가능해졌습니다.

#### **Genie** (Google DeepMind, 2024년 2월)

DeepMind의 [Genie](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)는 명시적으로 세계 모델로 설계되었습니다. 이 110억 파라미터 모델은 텍스트, 이미지, 사진, 심지어 스케치로부터 **인터랙티브 환경**을 생성합니다.

Sora와의 주요 차이점: Genie 세계는 **플레이 가능**합니다. 키보드/마우스 입력으로 제어할 수 있습니다.

그런 다음 2024년 12월, [Genie 2](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)가 레벨업했습니다:
- 3D 플레이 가능 환경 생성
- 최대 1분간 일관성 (대부분 예시는 10-20초)
- 사람이나 AI 에이전트가 플레이 가능
- 체화된 에이전트 훈련에 사용

#### **V-JEPA** (Meta AI, 2024년 2월)

OpenAI와 DeepMind가 완전 생성적으로 갔을 때, Yann LeCun의 Meta 팀은 [V-JEPA](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)로 다른 길을 택했습니다.

V-JEPA (Video Joint Embedding Predictive Architecture)는 **비생성적**입니다:
- 픽셀을 생성하는 대신, 추상 표현을 예측
- 잠재 공간에서 비디오의 누락된 부분을 채워 학습
- 픽셀 레벨 생성보다 더 효율적
- Yann의 비전: 이것이 "자율 지능"으로 가는 길

철학적 충돌이 흥미롭습니다. OpenAI/DeepMind: "모든 것을 생성하라!" Meta: "추상적 특징을 예측하라!" 양쪽 진영 모두 인상적인 결과를 가지고 있습니다.

### 2025: 성숙 및 전문화 🎯

2025년에 이 분야는 전방위적으로 개선되며 폭발했습니다:

#### **Genie 3** (DeepMind, 2025년 8월)

[Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)는 불과 1년 전만 해도 불가능해 보였던 것을 달성했습니다:
- **24 FPS로 실시간 상호작용**
- 720p 해상도
- **수분간** 일관성
- 전례 없는 생성 환경의 다양성

실제로 실시간으로 상호작용할 수 있는 첫 세계 모델. 체화된 AI 에이전트 훈련에 게임 체인저입니다.

#### **V-JEPA 2** (Meta AI, 2025년 6월)

[V-JEPA 2](https://ai.meta.com/vjepa/)는 예측 접근법을 두 배로 늘렸습니다:
- 12억 파라미터
- 100만 시간 이상의 비디오로 훈련
- 새로운 환경에서 **제로샷 로봇 제어**
- 비디오 이해 벤치마크에서 최고 수준

미친 부분: "웹 규모 비디오 사전학습 + 최소한의 로봇 데이터 = 실행 가능한 세계 모델." YouTube에서 훈련하고 로봇으로 일반화할 수 있습니다. 뭐라고요.

#### **VL-JEPA** (Meta AI, 2025년 후반)

Vision-language JEPA는 아키텍처를 멀티모달로 가져갔습니다:
- 토큰이나 픽셀 대신 임베딩 예측
- **50% 적은 파라미터로 최고 수준 성능**
- 표준 비전-언어 모델보다 더 효율적

Yann의 효율성 우선 접근법이 결실을 맺고 있습니다.

#### **Sora 2** (OpenAI, 2025년)

Sora가 GPT-3.5 순간을 맞았습니다:
- 향상된 물리적 정확도
- 더 나은 사실성과 제어 가능성
- "비디오를 위한 GPT-3.5 순간"으로 묘사됨

Sora 1보다 과대광고는 적지만, 더 유능하고 접근 가능합니다.

---

## 도메인 응용: 실제로 중요한 곳

World model은 단순한 학술적 호기심이 아닙니다. 실제 응용 분야에 배포되고 있습니다:

### 🚗 자율주행

자율주행차는 다음에 무슨 일이 일어날지 예측해야 합니다. World model이 이에 완벽합니다:

- **DriveWorld** (CVPR 2024): 자율주행을 위한 4D 장면 이해
- **World4Drive** (ICCV 2025): 의도 인식 세계 모델을 통한 엔드투엔드 주행
- **Epona** (ICCV 2025): **분 단위** 주행 시나리오를 고해상도로 생성, 실시간 모션 플래너로 작동

자율주행 커뮤니티는 이제 자체 [종합 서베이](https://arxiv.org/abs/2501.11260)를 가지고 있습니다. 3계층 분류법: 미래 세계 생성 → 행동 계획 → 응용.

### 🤖 로보틱스

로봇은 조작을 이해하고, 물체 동역학을 예측하고, 행동을 계획하기 위해 세계 모델이 필요합니다:

- **PIVOT-R** (NeurIPS 2024): 조작 작업을 위한 웨이포인트 인식 세계 모델
- **GWM** (ICCV 2025): 확장 가능한 로봇 조작을 위한 가우시안 세계 모델
- **RWM-U**: 실제 로봇 배포를 위한 불확실성 인식 세계 모델

로보틱스 분야도 인식, 예측, 제어 전반의 세계 모델을 분석하는 [자체 서베이](https://arxiv.org/abs/2511.02097)를 가지고 있습니다.

### 🎮 게임 및 가상 세계

Genie가 빛나는 곳입니다:
- 절차적 세계 생성
- 동적 NPC 행동
- 적응형 게임 환경
- AR/VR 응용

Fei-Fei Li는 2024년에 **World Labs**를 설립하고 텍스트, 이미지 또는 비디오로부터 3D 세계를 생성하는 **Marble** 소프트웨어를 출시했습니다. 상업적 응용이 시작되고 있습니다.

---

## 주요 연구 조직

### Google DeepMind: 생성 챔피언

DeepMind는 생성형 세계 모델에 올인하고 있습니다:
- Genie 시리즈 (1, 2, 3)
- 실시간 상호작용 중점
- 체화된 AI 에이전트를 위한 훈련장

전략: AI가 행동으로 학습할 수 있는 플랫폼 구축.

### Meta AI: 예측 효율성

Meta에서의 Yann LeCun의 비전:
- V-JEPA, V-JEPA 2, VL-JEPA
- **CWM**: 320억 파라미터 오픈 웨이트 코드 세계 모델
- 생성이 아닌 예측을 통한 효율성

전략: 픽셀이 아닌 추상 표현을 학습. 그리고: 오픈 웨이트 만세.

### OpenAI: 세계 시뮬레이션으로서의 비디오

OpenAI의 접근법:
- Sora, Sora 2
- AGI로 가는 길로서의 비디오 생성 확장
- ChatGPT 생태계와의 통합

전략: 현실적인 비디오를 생성할 수 있다면, 세계를 이해하는 것입니다.

### NVIDIA: 물리적 AI 플랫폼

NVIDIA는 인프라 게임을 하고 있습니다:
- **Cosmos**: 물리적 AI를 위한 세계 기초 모델 플랫폼
- 엔터프라이즈 중점
- 대규모 세계 모델 훈련 및 배포를 위한 도구

전략: 세계 모델 골드 러시에서 곡괭이와 삽이 되기.

---

## 철학적 분열

접근법에 흥미로운 분열이 있습니다:

### 생성 진영 (OpenAI, DeepMind)

**철학:** 세계를 픽셀 단위로 생성
- Sora, Genie 시리즈
- 높은 시각적 충실도
- 계산 비용이 많이 듦
- 사람이 해석 가능한 출력에 훌륭

**주장:** 현실적인 비디오를 생성할 수 있다면, 기본 물리학과 동역학을 이해해야 합니다.

### 예측 진영 (Meta/Yann LeCun)

**철학:** 픽셀이 아닌 추상적 특징 예측
- V-JEPA, VL-JEPA
- 더 효율적
- 추상 표현
- 다운스트림 작업에 더 좋음

**주장:** 픽셀 생성은 계산을 낭비합니다. 고수준 특징을 예측하면 더 빠르고 더 잘 배울 것입니다.

누가 맞을까요? 아마 둘 다? 양쪽의 결과가 모두 인상적입니다.

---

## 주요 기술적 접근법

주요 아키텍처 패턴은 다음과 같습니다:

### 시공간 패치의 트랜스포머
- 사용: Sora
- 아이디어: 비디오를 3D 데이터(x, y, 시간)로 취급하고 트랜스포머 적용
- 장점: 잘 확장됨, 가변 길이 처리
- 단점: 계산 비용이 많이 듦

### 확산 모델
- 사용: Genie, Epona
- 아이디어: 무작위 노이즈에서 구조화된 출력으로 노이즈 제거 학습
- 장점: 고품질 생성, 유연한 조건부
- 단점: 추론이 느림

### 결합 임베딩 예측 아키텍처 (JEPA)
- 사용: V-JEPA, VL-JEPA
- 아이디어: 잠재 공간에서 마스크된 영역의 임베딩 예측
- 장점: 효율적, 추상적 특징 학습
- 단점: 직접 해석하기 어려움

### 가우시안 표현
- 사용: GWM (로보틱스)
- 아이디어: 세계 상태를 가우시안 분포로 표현
- 장점: 불확실성을 자연스럽게 처리
- 단점: 도메인별

### 불확실성을 갖춘 자기회귀
- 사용: RWM-U (로보틱스)
- 아이디어: 인식론적 불확실성 추정을 갖춘 순차 예측
- 장점: 안전성을 갖춘 장기 계획
- 단점: 계산 오버헤드

---

## 앞으로의 과제

놀라운 진보에도 불구하고, 여전히 어려운 문제들이 있습니다:

### 1. 장기 일관성

현재 상태:
- Genie 3: 분 단위
- Sora: 최대 1분
- 대부분의 모델: 10-20초

목표: 시간 단위 또는 무한한 일관성. 우리는 아직 거기에 도달하지 못했습니다.

### 2. 물리적 정확도

모델은 여전히 물리 실수를 합니다:
- 물체가 나타나거나 사라짐
- 보존 법칙 위반
- 잘못된 충돌 동역학

창발적 물리 이해는 개선되고 있지만 완벽하지 않습니다.

### 3. 계산 비용

세계 상태를 생성하거나 예측하는 것은 비용이 많이 듭니다:
- Genie 3는 24 FPS를 위해 심각한 하드웨어 필요
- Sora 생성은 시간이 걸림
- 대규모 실시간 상호작용은 어려움

### 4. 일반화

비디오 게임에서 훈련된 모델이 로보틱스에 작동할 수 있을까요? 주행 모델이 조작으로 전이될 수 있을까요?

일부 유망한 결과(V-JEPA 2의 제로샷 로봇 제어)가 있지만 더 많은 작업이 필요합니다.

### 5. 안전성 및 검증

자율주행과 로보틱스를 위해서는 다음이 필요합니다:
- 불확실성 정량화
- 최악의 경우 보장
- 설명 가능한 예측

RWM-U(불확실성 인식 로보틱스 세계 모델)는 한 단계이지만, 할 일이 훨씬 더 많습니다.

---

## 중요한 서베이 논문

깊이 들어가고 싶다면, 필독 논문들입니다:

### [Understanding World or Predicting Future? A Comprehensive Survey](https://arxiv.org/abs/2411.14499)
- 15명의 저자, 지속적으로 업데이트 (최신: 2025년 12월)
- 이 분야의 가장 종합적인 개요
- 이해 vs 예측으로 분류
- 게임, 주행, 로보틱스, 사회 시뮬레이션 다룸

### [World Models in AI: Sensing, Learning, Reasoning Like a Child](https://arxiv.org/abs/2503.15168)
- Piaget의 인지 발달 이론에서 영감
- 중점: 물리 기반 학습, 신경기호 추론, 지속 학습, 인과 추론
- 흥미로운 인지과학 관점

### 도메인별 서베이
- [자율주행 서베이](https://arxiv.org/abs/2501.11260) (2025년 1월)
- [로봇 조작 서베이](https://arxiv.org/abs/2511.02097) (2025년 11월)

---

## 재미있는 사실 및 주목할 만한 순간

**Yann LeCun의 큰 움직임:** 2024년 11월, Yann은 지속적인 메모리, 추론, 계획을 갖춘 물리적 세계를 이해하는 시스템 구축에 중점을 둔 **AMI Labs** 시작을 위해 Meta를 떠난다고 발표했습니다. JEPA 비전이 계속됩니다.

**Fei-Fei Li의 스타트업:** "컴퓨터 비전의 대모"가 2024년에 **World Labs**를 설립했습니다. 그들의 **Marble** 소프트웨어는 텍스트/이미지/비디오로부터 3D 세계를 생성합니다. 상업적 세계 모델이 여기 있습니다.

**ICLR 2025 워크샵:** "World Models: Understanding, Modelling and Scaling" - 이것이 이제 전용 워크샵을 갖춘 주요 연구 분야임을 보여줍니다.

**GitHub 생태계:** 이제 100개 이상의 논문을 추적하는 여러 "Awesome World Models" 레포지토리가 있습니다. 이 분야는 폭발하고 있습니다.

**Nature 출판:** DreamerV3가 Nature(2025)에 실린 것은 세계 모델이 주류 학술적 인정을 받고 있음을 보여줍니다.

---

## 다음은 무엇? (2025-2026 예측)

현재 트렌드를 바탕으로, 주목해야 할 것들입니다:

### 실시간이 표준이 됨
- Genie 3의 24 FPS가 기준선이 될 것
- 상호작용을 위한 1초 미만 대기 시간
- 세계 모델의 모바일 배포

### 멀티모달 융합
- 비전 + 언어 + 촉각 + 오디오
- 모달리티 전반의 통합 세계 이해
- VL-JEPA는 시작일 뿐

### 하이브리드 접근법
- 생성 및 예측 패러다임 결합
- 두 세계의 장점: 효율성 + 품질
- 아마도 진영들이 합쳐질 것

### 도메인별 플랫폼
- 주행을 위한 전문 세계 모델 (NVIDIA Cosmos)
- 로보틱스별 아키텍처
- 게임 엔진 통합

### 오픈 웨이트 운동
- Meta의 CWM 릴리스에 따라
- 연구를 위한 더 많은 오픈 모델
- 세계 모델 개발의 민주화

### 더 긴 지평선
- 목표: 시간 단위 일관성
- 더 나은 장기 예측
- 계층적 세계 모델 (거친 것에서 세밀한 것으로)

---

## 자료 및 추가 탐색

### 인터랙티브 데모
- [World Models (2018)](https://worldmodels.github.io/) - 원조, 여전히 재미있게 플레이 가능
- [Genie](https://deepmind.google/genie) - DeepMind의 인터랙티브 세계 생성기

### GitHub 컬렉션
- [Awesome-World-Models](https://github.com/knightnemo/Awesome-World-Models) by knightnemo
- [Awesome-World-Models](https://github.com/leofan90/Awesome-World-Models) by leofan90
- [World-Models-Autonomous-Driving](https://github.com/HaoranZhuExplorer/World-Models-Autonomous-Driving-Latest-Survey)
- [Awesome-World-Model](https://github.com/LMD0311/Awesome-World-Model) (로보틱스 중점)

### 연도별 주요 논문

**2018:**
- [World Models](https://arxiv.org/abs/1803.10122) - Ha & Schmidhuber

**2023:**
- [DreamerV3](https://arxiv.org/abs/2301.04104) - Hafner et al.

**2024:**
- Genie (DeepMind) - 2월
- Sora (OpenAI) - 2월
- V-JEPA (Meta) - 2월
- Genie 2 (DeepMind) - 12월

**2025:**
- V-JEPA 2 (Meta) - 6월
- Genie 3 (DeepMind) - 8월
- [RLVR-World](https://arxiv.org/abs/2505.13934) - 강화학습으로 훈련
- 주행 및 로보틱스에 대한 다수의 ICCV/NeurIPS 논문

### 팔로우할 조직
- **Google DeepMind** - Genie 시리즈 업데이트
- **Meta AI** - V-JEPA 개발, 오픈 릴리스
- **OpenAI** - Sora 개선
- **World Labs** - 상업적 3D 세계 생성
- **AMI Labs** - Yann LeCun의 새로운 벤처
- **NVIDIA** - Cosmos 플랫폼 업데이트

---

## 내 생각

World model은 뒤늦게 보면 명백히 옳은 아이디어 중 하나처럼 느껴집니다. 물론 AI는 현실의 내부 표현이 필요합니다. 물론 에이전트는 상상하고 계획할 수 있어야 합니다. 물론 시뮬레이션된 경험으로부터 학습하는 것이 실제 세계에서의 시행착오보다 더 효율적입니다.

놀라운 것은 우리가 "귀여운 강화학습 데모"(2018)에서 "실시간 3D 인터랙티브 세계"(2025)로 얼마나 빨리 갔는지입니다. 산업 지원(DeepMind, Meta, OpenAI, NVIDIA)은 이것이 단순한 학술적 배꼽 응시가 아니라 실제 상업적 가치가 있음을 보여줍니다.

생성 대 예측 논쟁은 상징적 대 연결주의 AI 전쟁을 떠올리게 합니다. 아마도 두 접근법 모두 가치가 있고 하이브리드 시스템이 등장할 것입니다. Yann의 효율성 논증은 설득력이 있지만, Genie 3가 실시간으로 플레이 가능한 세계를 생성하는 것에 대해서는 뭔가 본능적으로 인상적입니다.

응용 분야로는 로보틱스가 가장 기대됩니다. V-JEPA 2의 제로샷 일반화는 놀랍습니다 - 웹 비디오로 훈련하고, 로봇에 배포. 이것이 확장된다면, 우리는 마침내 범용 로봇 조작을 해결할 수 있을 것입니다.

자율주행은 다른 명백한 승자입니다. 훈련과 테스트를 위해 희귀하거나 위험한 시나리오를 시뮬레이션할 수 있는 것은 안전 검증에 엄청납니다.

AGI로 가는 길? 그것이 10억 달러짜리 질문입니다. Yann은 세계 모델이 중요하다고 생각합니다. OpenAI는 Sora에 베팅하고 있습니다. DeepMind는 Genie로 훈련 플랫폼을 구축하고 있습니다. 그들이 모두 옳다면, 우리는 실시간으로 AGI 인프라가 구축되는 것을 보고 있습니다.

어느 쪽이든, 우리는 AI 역사의 매혹적인 순간을 살고 있습니다. 2026년에 다시 확인해보고 얼마나 많이 변했는지 봅시다.

---

## 부록: 논문 데이터베이스

언급된 모든 논문의 종합 목록은 함께 제공되는 **`World_Model_논문_데이터베이스.xlsx`** 파일을 참조하세요:
- 2018-2025년의 22개 이상 주요 논문
- 저자, 학회, 주요 기여
- 카테고리 및 연구 분야
- 타임라인 시각화
- 조직 분류

---

*마지막 업데이트: 2026년 3월*

*World model에 대해 논의하고 싶으신가요? 댓글 남겨주세요!*

---

## 출처

이 블로그 포스트는 다음으로부터 정보를 종합했습니다:

- [World Models Reading List (Medium)](https://medium.com/@graison/world-models-reading-list-the-papers-you-actually-need-in-2025-882f02d758a9)
- [Scientific American: World Models Could Unlock AI Revolution](https://www.scientificamerican.com/article/world-models-could-unlock-the-next-revolution-in-artificial-intelligence/)
- [arXiv:2411.14499 - Understanding World or Predicting Future Survey](https://arxiv.org/abs/2411.14499)
- [Nature: Mastering Diverse Control Tasks through World Models](https://www.nature.com/articles/s41586-025-08744-2)
- [Meta AI: V-JEPA](https://ai.meta.com/blog/v-jepa-yann-lecun-ai-model-video-joint-embedding-predictive-architecture/)
- [Meta AI: V-JEPA 2](https://ai.meta.com/vjepa/)
- [Google DeepMind: Genie 2](https://deepmind.google/blog/genie-2-a-large-scale-foundation-world-model/)
- [Google DeepMind: Genie 3](https://deepmind.google/blog/genie-3-a-new-frontier-for-world-models/)
- [OpenAI: Sora](https://openai.com/index/sora/)
- [OpenAI: Video Generation Models as World Simulators](https://openai.com/index/video-generation-models-as-world-simulators/)
- [arXiv:1803.10122 - World Models](https://arxiv.org/abs/1803.10122)
- [arXiv:2301.04104 - DreamerV3](https://arxiv.org/abs/2301.04104)
- 2024-2025 CVPR, ICCV, NeurIPS proceedings 다수
- 전반에 걸쳐 인용된 다양한 GitHub 레포지토리 및 서베이
