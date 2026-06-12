# Andrej Karpathy의 LLM 세계: nanoGPT부터 microGPT까지, "가장 단순한 방법으로 LLM 이해하기"

> 📊 **발표자료**: [karpathy-llm-presentation.pptx](./karpathy-llm-presentation.pptx)

> 작성일: 2026-04-08  
> 카테고리: AI Research & Foundations

---

AI를 공부하다 보면 한 번쯤은 이 사람 이름을 보게 되죠. **Andrej Karpathy**. OpenAI 공동 창업자, Tesla AI 디렉터, 그리고 지금은 AI 교육 스타트업 Eureka Labs의 창업자. 근데 진짜 그가 유명한 이유는 그 커리어 때문만은 아니에요. 복잡한 걸 극도로 단순하게 만들어서 *"아, 이거 나도 할 수 있겠다"* 는 느낌을 주는 사람이거든요.

이 글에서는 그가 공개한 LLM 관련 프로젝트들, 강의 시리즈, 그리고 최근까지의 활동을 한 번에 정리해볼게요.

---

## 1. 그는 누구인가: 간략한 커리어 정리

[Wikipedia에 따르면](https://en.wikipedia.org/wiki/Andrej_Karpathy), Andrej Karpathy는 1986년 슬로바키아 브라티슬라바에서 태어난 슬로박-캐나다 출신 AI 연구자예요. 15살에 토론토로 이민 왔고, 토론토 대학교에서 컴퓨터과학과 물리학 학사를 마쳤어요.

이후 커리어를 정리하면 이렇게 돼요:

| 기간 | 활동 |
|------|------|
| 2011-2015 | Stanford 박사 (지도교수: Fei-Fei Li, CV+NLP) |
| 2015-2017 | OpenAI 공동 창업 & 리서치 사이언티스트 |
| 2017-2022 | Tesla AI 디렉터 (자율주행 AI 총괄) |
| 2023-2024 | OpenAI 복귀 |
| 2024- | Eureka Labs 창업 |

[Stanford CS 페이지](https://cs.stanford.edu/people/karpathy/)에서도 확인할 수 있듯이, 그는 Stanford에서 CS231n이라는 딥러닝 강의를 직접 설계하고 강의했는데 — 2015년 150명으로 시작해서 2017년엔 750명이 수강하는 Stanford 최대 인기 강의가 됐어요. 가르치는 것에 진심인 사람이에요.

---

## 2. 핵심 프로젝트들: "가장 작은 코드로 LLM 이해하기"

Karpathy의 프로젝트들은 공통된 철학을 가지고 있어요: **외부 의존성을 최소화하고, 코드 한 줄 한 줄을 직접 이해할 수 있도록 만든다**. 블랙박스 없이 바닥부터.

### 2-1. micrograd: 자동미분의 씨앗

[GitHub: karpathy/micrograd](https://github.com/karpathy/micrograd)

출발점은 **micrograd**예요. 스칼라값 기반의 자동미분(autograd) 엔진인데, PyTorch API와 거의 똑같이 생겼어요. 코드가 정말 짧거든요. 근데 이걸 직접 따라 구현하고 나면 *"아, backpropagation이 이런 거구나"* 가 진짜로 이해돼요.

```python
# micrograd 사용 예시 (PyTorch랑 똑같이 생겼죠)
from micrograd.engine import Value

a = Value(-4.0)
b = Value(2.0)
c = a + b        # c = -2.0
d = a * b + b**3  # d = -8.0 + 8.0 = 0.0
c.backward()     # 그라디언트 계산!
print(a.grad)    # -출력: 1.0
```

### 2-2. makemore: 문자 단위 언어 모델

[GitHub: karpathy/makemore](https://github.com/karpathy/makemore)

**makemore**는 문자 단위(character-level) 자동회귀 언어 모델이에요. bigram 모델부터 시작해서 MLP, RNN, GRU, Transformer까지 순서대로 구현해볼 수 있어요. 학습 데이터는 간단한 이름 리스트 — 이걸로 새 이름을 생성하는 거예요. 근데 이게 진짜 언어 모델의 핵심 구조를 다 담고 있어요.

> "Makemore takes one text file as input, where each line is a training example, and the model learns to make more things like it." — [karpathy/makemore README](https://github.com/karpathy/makemore)

### 2-3. minGPT: 최초의 "최소한의 GPT"

[GitHub: karpathy/minGPT](https://github.com/karpathy/minGPT)

**minGPT**는 GPT를 PyTorch로 최소한으로 재구현한 프로젝트예요. 교육 목적이 강하고, 현재는 semi-archived 상태 — 후속 프로젝트 nanoGPT를 보라고 안내하고 있어요.

### 2-4. nanoGPT: "실제로 쓸 수 있는 최소한의 GPT"

[GitHub: karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)

**nanoGPT**는 minGPT를 리라이트한 프로젝트예요. 교육적 목적보다는 실용성 쪽으로 기울어진 버전이죠.

> "The simplest, fastest repository for training/finetuning medium-sized GPTs." — [nanoGPT README](https://github.com/karpathy/nanoGPT)

GPT-2 규모의 모델을 직접 훈련시키거나 파인튜닝할 수 있어요. 코드가 매우 단순하고 읽기 쉬워서, LLM 구조를 처음부터 공부하려는 사람들에게 교과서 같은 프로젝트가 됐어요.

```bash
# nanoGPT로 GPT-2 스타일 학습 시작하기
git clone https://github.com/karpathy/nanoGPT.git
cd nanoGPT
pip install torch numpy transformers datasets tiktoken wandb tqdm

# 데이터 준비
python data/shakespeare_char/prepare.py

# 학습 시작
python train.py config/train_shakespeare_char.py
```

### 2-5. llm.c: "PyTorch도 없이 C/CUDA로 LLM 훈련"

[GitHub: karpathy/llm.c](https://github.com/karpathy/llm.c)

이건 진짜 충격적인 프로젝트예요. **245MB짜리 PyTorch도, 107MB짜리 Python도 없이** — 순수 C와 CUDA만으로 LLM을 훈련시켜요.

> "LLM training in simple, raw C/CUDA. No need for 245MB of PyTorch or 107MB of cPython." — [llm.c README](https://github.com/karpathy/llm.c)

더 놀라운 건 성능이에요. llm.c는 현재 PyTorch Nightly보다 약 7% 빠르게 동작해요. GPT-2 (124M) 모델을 단 **90분, 약 20달러**로 재현할 수 있어요 (8x A100 80GB 노드 기준).

[llm.c 토론 #481](https://github.com/karpathy/llm.c/discussions/481)에서 Karpathy 본인이 직접 이 벤치마크 결과를 공유했어요.

### 2-6. build-nanogpt: "강의 따라 nanoGPT 직접 구현"

[GitHub: karpathy/build-nanogpt](https://github.com/karpathy/build-nanogpt)

유튜브 강의 "Let's build GPT"에 대응하는 코드 저장소예요. 비디오를 보면서 함께 코딩할 수 있는 자료들이 담겨 있어요.

### 2-7. microGPT: 최종 보스 — 243줄의 순수 Python

[GitHub Gist: karpathy/microgpt.py](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95)

그리고 2026년 2월 12일, Karpathy가 [블로그](http://karpathy.github.io/2026/02/12/microgpt/)에서 새 프로젝트를 공개했어요. **microGPT**: 외부 import 없이 **순수 Python 243줄**로 GPT를 구현한 거예요.

> "This is a new art project: a single file of 200 lines of pure Python with no dependencies that trains and inferences a GPT." — Andrej Karpathy, 2026

이 파일 하나에 전부 들어있어요:
- 학습 데이터셋
- 토크나이저
- Autograd 엔진
- GPT-2 스타일 신경망 구조
- Adam 옵티마이저
- 훈련 루프
- 추론 루프

총 파라미터 수: **4,192개**. Hacker News에서 공개 몇 시간 만에 960+ 포인트를 받았어요.

> "This script is the culmination of multiple projects (micrograd, makemore, nanogpt, etc.) and a decade-long obsession to simplify LLMs to their bare essentials." — Karpathy

---

## 3. "Neural Networks: Zero to Hero" 강의 시리즈

[공식 강의 페이지](https://karpathy.ai/zero-to-hero.html) | [GitHub](https://github.com/karpathy/nn-zero-to-hero)

2022년 8월부터 YouTube에서 시작한 강의 시리즈예요. 총 7개 비디오로 구성된 플레이리스트인데, backpropagation 기초부터 시작해서 GPT 구현까지 올라가요.

### 강의 목록

| # | 제목 | 내용 |
|---|------|------|
| 1 | **The spelled-out intro to neural networks and backpropagation: building micrograd** | micrograd 직접 구현, backprop 핵심 |
| 2 | **The spelled-out intro to language modeling: building makemore** | bigram 모델, 언어 모델 기초 |
| 3 | **Building makemore Part 2: MLP** | MLP 기반 언어 모델, Bengio et al. 2003 논문 구현 |
| 4 | **Building makemore Part 3: Activations & Gradients, BatchNorm** | 활성화 함수, BatchNorm, 가중치 초기화 |
| 5 | **Building makemore Part 4: Becoming a Backprop Ninja** | 수동 backprop 집중 훈련 |
| 6 | **Building makemore Part 5: Building a WaveNet** | WaveNet 스타일 계층적 구조 |
| 7 | **Let's build GPT: from scratch, in code, spelled out** | Transformer + GPT 처음부터 구현 |
| 보너스 | **Let's build the GPT Tokenizer** | BPE 토크나이저 처음부터 구현 |

> "I believe language models are an excellent place to learn deep learning, even if the intention is to eventually move to other areas like computer vision, because most of what you learn will be immediately transferable." — Karpathy, [karpathy.ai](https://karpathy.ai/)

이 강의의 특징은 **"마법이 없다"**는 거예요. PyTorch의 `.backward()`가 내부적으로 어떻게 동작하는지, Transformer의 attention이 왜 그런 식으로 생겼는지 — 전부 코드로 직접 구현하면서 이해해요.

---

## 4. Karpathy의 핵심 철학: Software 1.0 → 2.0 → 3.0

Karpathy가 유명해진 또 다른 이유 중 하나는 소프트웨어 패러다임에 대한 통찰이에요.

### Software 2.0 (2017년 제안)

[latent.space 팟캐스트 정리](https://www.latent.space/p/s3)에 따르면, Karpathy는 이미 2017년에 "Software 2.0"이라는 개념을 제안했어요:

> "Software 1.0 is the hand-written code we're all familiar with. Software 2.0 is the neural network: the weights are the code, and the training process is the compiler." — Karpathy

개발자가 규칙을 직접 코드로 작성하는 게 아니라, 데이터로부터 모델이 규칙을 학습하는 패러다임을 뜻해요.

### Software 3.0 (2025년 확장)

그리고 LLM 시대가 되자 이 프레임워크가 다시 확장됐어요:

| 패러다임 | 방식 | 예시 |
|----------|------|------|
| **Software 1.0** | 사람이 규칙 코드를 직접 작성 | Python, Java |
| **Software 2.0** | 데이터로부터 모델이 학습 | 딥러닝, 신경망 가중치 |
| **Software 3.0** | 영어(자연어)로 LLM에게 지시 | 프롬프트 엔지니어링 |

[Analytics Vidhya 요약](https://www.analyticsvidhya.com/blog/2025/06/andrej-karpathy-on-the-rise-of-software-3-0/)에서도 다루고 있듯이, Software 3.0에서는 프롬프트가 곧 프로그램이 되고, LLM의 사전학습 지식이 실행 엔진이 되는 거예요.

### "Vibe Coding" (2025년 2월)

[Karpathy의 X 포스트](https://x.com/karpathy)를 통해 유명해진 개념으로, AI 도구를 이용해서 "느낌으로" 코딩하는 방식을 뜻해요 — 프롬프트만 입력하고 코드 구조를 일일이 신경 쓰지 않는 것. 이 단어가 2025년에 급속도로 퍼졌고, 이제는 업계 공용어가 됐어요.

### LLM Knowledge Base (2026년 4월)

가장 최근 활동이에요. [VentureBeat 기사](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)에 따르면, 2026년 4월 3일 Karpathy는 "LLM Knowledge Base" 워크플로우를 공개했어요.

> "A large fraction of my recent token throughput is going less into manipulating code, and more into manipulating knowledge." — Karpathy, 2026

핵심은 이래요: 원시 자료(논문, 기사, 저장소, 데이터셋)를 디렉토리에 던져두면, LLM이 이걸 구조화된 Markdown 위키로 점진적으로 컴파일해요. RAG도 필요 없어요. 특정 벤더에도 종속되지 않아요.

[GitHub Gist 링크](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)에서 아이디어 파일을 공개했는데 — "에이전트 시대에는 구체적 구현을 공유하는 의미가 줄어들었다"고 설명했어요.

---

## 5. Eureka Labs: "AI 네이티브 학교"

[공식 사이트](https://eurekalabs.ai/) | [TechCrunch 기사](https://techcrunch.com/2024/07/16/after-tesla-and-openai-andrej-karpathys-startup-aims-to-apply-ai-assistants-to-education/)

2024년 2월 OpenAI를 떠난 Karpathy는 같은 해 7월 **Eureka Labs**를 창업했어요. 비전은 간단해요: **"AI 네이티브 학교"**.

> "Human expert-written course materials will be scaled and guided with an AI Teaching Assistant." — Eureka Labs 발표

기존 교육 플랫폼이 콘텐츠를 올리는 데 그친다면, Eureka Labs는 AI 조교가 실시간으로 학습자를 가이드하는 구조예요.

### 첫 번째 코스: LLM101n

[GitHub: karpathy/LLM101n](https://github.com/karpathy/LLM101n)

첫 코스 **LLM101n: Let's Build a Storyteller**는 Python, C, CUDA를 이용해서 "스토리텔러 AI"를 처음부터 만들어보는 학부 수준 온라인 강의예요.

커리큘럼(계획 중):

1. Bigram Language Model
2. MLP, Attention
3. Transformer
4. Tokenization (BPE)
5. 사전학습 (Pre-training)
6. 파인튜닝 (SFT)
7. RLHF
8. Deployment
9. 멀티모달 확장

아직 개발 중이라 구체적인 일정은 없지만, GitHub에 실루엣은 공개돼 있어요.

---

## 6. 2025 LLM 연간 리뷰: Karpathy의 시선

[karpathy.bearblog.dev](https://karpathy.bearblog.dev/year-in-review-2025/)에 Karpathy가 직접 2025년 LLM 트렌드 리뷰를 올렸어요.

그의 관점을 간략히 정리하면:

- LLM 성능이 급격히 발전하면서 "추론(reasoning)" 능력이 핵심 화두가 됐어요
- 코딩 작업에서의 LLM 활용이 폭발적으로 늘었고, Karpathy 자신도 Cursor의 탭 자동완성이 전체 LLM 사용량의 75%를 차지한다고 밝혔어요
- 코드 생성보다 **지식 구조화(knowledge structuring)**로 관심이 이동 중

---

## 7. 실무자/학습자에게 주는 시사점

Karpathy의 모든 프로젝트와 강의에서 공통적으로 발견되는 패턴이 있어요:

### 첫째, "최소 단위로 쪼개라"

micrograd → makemore → nanoGPT → llm.c → microGPT. 매번 더 작게, 더 단순하게 만들었어요. 복잡한 시스템도 핵심만 남기면 이해할 수 있어요.

### 둘째, "직접 구현해봐야 안다"

> "The best way to understand something is to build it from scratch." — Karpathy 강의 곳곳에서 반복

블랙박스로 API 호출하는 게 아니라, backprop을 손으로 계산하고, attention을 직접 짜봐야 진짜 이해가 돼요.

### 셋째, "교육 자료는 공개로"

모든 코드가 GitHub에 공개돼 있고, 강의는 YouTube에서 무료예요. 지식의 민주화에 진심인 사람이에요.

### 넷째, "현재 위치에서 시작해도 된다"

Zero to Hero 시리즈는 진짜 0에서 시작해요. 행렬 곱셈을 모르는 상태에서도 시작할 수 있도록 설계됐어요.

---

## 8. 학습 로드맵: Karpathy 방식으로 LLM 공부하기

```
[단계 1] micrograd 강의 시청 + 직접 구현
    ↓
[단계 2] makemore 시리즈 (Part 1-5) 완주
    ↓
[단계 3] "Let's build GPT" 비디오 + build-nanogpt 코드
    ↓
[단계 4] nanoGPT로 실제 데이터 학습 실험
    ↓
[단계 5] llm.c 코드 읽기 (C/CUDA 구현 이해)
    ↓
[단계 6] microGPT 243줄 라인 by 라인 분석
    ↓
[단계 7] LLM101n 수강 (출시 시)
```

---

## 마무리

Karpathy는 엄청난 커리어를 가진 사람이지만, 가장 인상적인 건 그게 아니에요. "이렇게 복잡한 걸 왜 이렇게 단순하게 만들 수 있지?" — 이 질문에 답을 계속 내놓는 사람이에요.

microGPT 243줄짜리 코드를 보면서, "10년간의 집착으로 여기까지 왔다"고 표현한 걸 보면서 — 이 사람이 단순히 스타 연구자가 아니라 진짜 교육자이자 장인이라는 게 느껴져요.

LLM 공부를 시작하려는 분, 이미 하고 있는데 뭔가 빈 게 있는 것 같은 분 — Karpathy의 강의 시리즈부터 시작해보세요. 보장해요, 뭔가 달라질 거예요.

---

## 참고 자료

1. [Andrej Karpathy 공식 사이트](https://karpathy.ai/)
2. [Neural Networks: Zero to Hero](https://karpathy.ai/zero-to-hero.html)
3. [GitHub: karpathy/nanoGPT](https://github.com/karpathy/nanoGPT)
4. [GitHub: karpathy/llm.c](https://github.com/karpathy/llm.c)
5. [GitHub: karpathy/micrograd](https://github.com/karpathy/micrograd)
6. [GitHub: karpathy/makemore](https://github.com/karpathy/makemore)
7. [GitHub: karpathy/LLM101n](https://github.com/karpathy/LLM101n)
8. [microGPT 블로그 포스트](http://karpathy.github.io/2026/02/12/microgpt/)
9. [microGPT GitHub Gist](https://gist.github.com/karpathy/8627fe009c40f57531cb18360106ce95)
10. [Eureka Labs 공식 사이트](https://eurekalabs.ai/)
11. [TechCrunch: Eureka Labs 창업](https://techcrunch.com/2024/07/16/after-tesla-and-openai-andrej-karpathys-startup-aims-to-apply-ai-assistants-to-education/)
12. [Wikipedia: Andrej Karpathy](https://en.wikipedia.org/wiki/Andrej_Karpathy)
13. [llm.c GPT-2 90분 재현 토론](https://github.com/karpathy/llm.c/discussions/481)
14. [LLM Knowledge Base - VentureBeat](https://venturebeat.com/data/karpathy-shares-llm-knowledge-base-architecture-that-bypasses-rag-with-an)
15. [LLM Knowledge Base GitHub Gist](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
16. [2025 LLM Year in Review](https://karpathy.bearblog.dev/year-in-review-2025/)
17. [Software 3.0 - latent.space](https://www.latent.space/p/s3)
18. [Andrej Karpathy on Software 3.0 - Analytics Vidhya](https://www.analyticsvidhya.com/blog/2025/06/andrej-karpathy-on-the-rise-of-software-3-0/)
19. [Time 100 Most Influential People in AI 2024](https://time.com/7012851/andrej-karpathy/)
20. [microGPT 분석 - Analytics Vidhya](https://www.analyticsvidhya.com/blog/2026/02/andrej-karpathy-microgpt/)

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. Karpathy의 교육용 프로젝트들은 공통된 철학을 가지고 있어요. 그게 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 외부 의존성을 최소화하고, 코드 한 줄 한 줄을 직접 이해할 수 있게 "바닥부터" 만든다는 거예요.

**해설**: micrograd부터 microGPT까지 모든 프로젝트가 블랙박스 없이 핵심만 남긴 최소 구현을 지향해요. API를 호출하는 게 아니라 backprop과 attention을 직접 짜보면서 이해하게 만드는 게 그의 일관된 방식이죠.

</details>

**Q2. micrograd, makemore, nanoGPT — 세 프로젝트의 역할을 구분할 수 있나요? 각각 뭘 배우기 위한 프로젝트일까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: micrograd는 자동미분(backpropagation)을, makemore는 문자 단위 언어 모델의 기초(bigram부터 Transformer까지)를, nanoGPT는 GPT-2 규모 모델을 실제로 훈련·파인튜닝하는 실용적인 구현을 배우기 위한 프로젝트예요.

**해설**: 세 프로젝트는 난이도와 목적이 계단식으로 이어져요. micrograd로 그라디언트 계산 원리를 익히고, makemore로 언어 모델 구조를 단계별로 쌓아본 다음, nanoGPT에서 "실제로 쓸 수 있는" 수준의 학습 코드로 넘어가는 흐름이죠.

</details>

**Q3. OX 문제: llm.c는 PyTorch 위에서 동작하는 경량 래퍼(wrapper) 라이브러리다. 맞을까요, 틀릴까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X (틀려요)

**해설**: llm.c는 PyTorch도 Python도 전혀 쓰지 않고 순수 C와 CUDA만으로 LLM을 훈련시키는 프로젝트예요. 오히려 PyTorch Nightly보다 약 7% 빠르게 동작하고, GPT-2(124M)를 90분·약 20달러에 재현할 수 있다는 게 포인트죠.

</details>

**Q4. 2026년 공개된 microGPT가 "최종 보스"라고 불리는 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 외부 import 없이 순수 Python 243줄 안에 토크나이저, autograd 엔진, GPT-2 스타일 신경망, Adam 옵티마이저, 훈련·추론 루프까지 전부 담았기 때문이에요.

**해설**: Karpathy 본인이 "micrograd, makemore, nanoGPT 등 여러 프로젝트의 정점이자 LLM을 본질만 남기려는 10년간의 집착의 결과물"이라고 표현했어요. 단일 파일 하나로 GPT의 전체 파이프라인을 보여주는 거죠.

</details>

**Q5. Software 1.0, 2.0, 3.0의 차이를 설명할 수 있나요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Software 1.0은 사람이 규칙을 직접 코드로 작성하는 방식(Python, Java), Software 2.0은 데이터로부터 모델이 규칙을 학습하는 방식(신경망 가중치가 곧 코드), Software 3.0은 자연어 프롬프트로 LLM에게 지시하는 방식이에요.

**해설**: Karpathy는 2017년에 "가중치가 코드이고 학습 과정이 컴파일러"라는 Software 2.0 개념을 제안했고, LLM 시대가 되자 프롬프트가 곧 프로그램이 되는 Software 3.0으로 확장했어요.

</details>

**Q6. 응용 시나리오: 딥러닝을 거의 모르는 친구가 "LLM을 바닥부터 이해하고 싶다"고 해요. Karpathy 방식의 학습 로드맵이라면 어디서 시작해서 어떤 순서로 가야 할까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: micrograd 강의로 backprop을 익히는 데서 시작해서, makemore 시리즈 → "Let's build GPT" + build-nanogpt → nanoGPT 실험 → llm.c 코드 읽기 → microGPT 분석 순서로 올라가면 돼요.

**해설**: Zero to Hero 시리즈는 진짜 0에서 시작하도록 설계됐기 때문에, 행렬 곱셈을 모르는 상태에서도 출발할 수 있어요. 핵심은 매 단계에서 블랙박스 없이 직접 구현해보면서 다음 단계로 넘어가는 거죠.

</details>

**Q7. Karpathy가 2026년에 공개한 "LLM Knowledge Base" 워크플로우의 핵심 아이디어는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 논문·기사·저장소 같은 원시 자료를 디렉토리에 던져두면, LLM이 이걸 구조화된 Markdown 위키로 점진적으로 컴파일하는 방식이에요. RAG도, 특정 벤더 종속도 필요 없어요.

**해설**: Karpathy는 최근 자신의 토큰 사용량이 코드 조작보다 지식 조작 쪽으로 옮겨가고 있다고 말했어요. 코드 생성에서 지식 구조화로 관심이 이동하는 흐름을 보여주는 대표적인 사례죠.

</details>

**Q8. Karpathy가 OpenAI를 떠나 창업한 Eureka Labs는 기존 온라인 교육 플랫폼과 뭐가 다를까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 콘텐츠를 올려두는 데 그치지 않고, 사람 전문가가 만든 강의 자료를 AI 조교(Teaching Assistant)가 실시간으로 학습자를 가이드하며 확장하는 "AI 네이티브 학교"를 지향해요.

**해설**: 첫 코스인 LLM101n은 Python, C, CUDA로 "스토리텔러 AI"를 처음부터 만들어보는 학부 수준 강의예요. 사람이 설계한 커리큘럼과 AI 조교의 결합이 핵심 차별점이죠.

</details>
