# Meta HyperAgents 완전 정복: AI가 스스로 "더 잘 배우는 법"을 배운다

> 📊 **발표자료**: [meta-hyperagents-presentation.pptx](./meta-hyperagents-presentation.pptx)

> "HyperAgents are self-referential agents that integrate a task agent (which solves the target task) and a meta agent (which modifies itself and the task agent) into a single editable program."
> — Zhang et al., HyperAgents 논문, arXiv 2603.19461, ICLR 2026

AI가 스스로 코드를 고치는 건 이제 놀랍지 않죠. 근데 Meta가 2026년 3월에 들고 나온 건 차원이 달라요. 그냥 코드를 고치는 게 아니라, **"어떻게 고쳐야 더 잘 고칠 수 있는지" 그 방법 자체를 스스로 개선**하는 AI를 만든 거거든요. 이게 바로 HyperAgents(하이퍼에이전트)입니다.

---

## 목차

1. [HyperAgents란 무엇인가?](#1-hyperagents란-무엇인가)
2. [핵심 아키텍처: 자기 참조적 구조](#2-핵심-아키텍처-자기-참조적-구조)
3. [Darwin Gödel Machine에서 DGM-H로의 진화](#3-darwin-gödel-machine에서-dgm-h로의-진화)
4. [실험 결과: 숫자로 보는 성능](#4-실험-결과-숫자로-보는-성능)
5. [기존 AI Agent 프레임워크와의 비교](#5-기존-ai-agent-프레임워크와의-비교)
6. [Meta의 AI 전략에서 HyperAgents의 위치](#6-meta의-ai-전략에서-hyperagents의-위치)
7. [오픈소스로 직접 써볼 수 있어요](#7-오픈소스로-직접-써볼-수-있어요)
8. [한계와 주의사항](#8-한계와-주의사항)
9. [앞으로의 방향](#9-앞으로의-방향)

---

## 1. HyperAgents란 무엇인가?

솔직히 처음 들으면 "또 또 AI 에이전트인가?" 싶죠. 근데 이건 진짜 다른 게 있어요.

지금까지 대부분의 AI 에이전트는 이런 구조예요:

- **태스크 에이전트(Task Agent)**: 실제 문제를 풀어요 (코딩, 문서 작성 등)
- **메타 에이전트(Meta Agent)**: 태스크 에이전트를 어떻게 개선할지 결정해요

문제는 이 메타 에이전트 자체가 **고정**되어 있다는 거예요. 즉, 개선 방법 자체는 인간이 설계한 그대로인 거죠.

HyperAgents는 이 경계를 완전히 허물었어요. 태스크 에이전트와 메타 에이전트를 **하나의 수정 가능한 코드베이스**로 합쳐버린 거예요. 그 결과:

> "The meta-level modification procedure itself can be improved" — 개선 절차 자체를 개선할 수 있다

이게 왜 혁신적이냐고요? AI가 더 좋은 문제풀이 방법을 찾는 것뿐 아니라, **"어떻게 하면 더 좋은 방법을 더 잘 찾을 수 있는지"**도 스스로 터득하는 거거든요.

---

## 2. 핵심 아키텍처: 자기 참조적 구조

[arXiv 논문](https://arxiv.org/abs/2603.19461)과 [GitHub 리포](https://github.com/facebookresearch/Hyperagents)를 기준으로 HyperAgents의 구조를 살펴봐요.

### 세 가지 핵심 레이어

**레이어 1: 자기 표현 레이어(Self-Representation Layer)**

AI가 자기 자신의 코드를 이해하는 레이어예요. 이 레이어는 모듈 구현, 설정 파라미터, 도구 정의, 의사결정 로직을 하나의 **시맨틱 그래프**로 표현해요. 에이전트가 이 그래프를 쿼리하고 분석하고 수정할 수 있죠.

**레이어 2: 개선 엔진(Improvement Engine)**

병목 지점을 분석하고, 해결책을 탐색하고, 후보 패치를 생성하고, 샌드박스에서 시뮬레이션하고, 안전 기준을 충족하는 개선사항을 선택해요.

**레이어 3: 배포 메커니즘(Deployment Mechanism)**

변경사항을 버전 관리와 함께 원자적으로 적용해요. 롤백 기능, 카나리 배포, 성능 모니터링도 포함되어 있어요.

### 코드 구조

```
HyperAgents/
├── task_agent.py        # 도메인별 목표 실행
├── meta_agent.py        # 자기 참조적 최적화
├── generate_loop.py     # 메인 실행 진입점
├── agent/               # LLM 인터페이스 (OpenAI, Anthropic, Google)
├── domains/             # 도메인별 구현
├── analysis/            # 결과 분석 및 시각화
├── utils/               # 공유 헬퍼 함수
└── baselines/           # 비교 기준선 구현
```

---

## 3. Darwin Gödel Machine에서 DGM-H로의 진화

HyperAgents를 이해하려면 그 전신인 [Darwin Gödel Machine(DGM)](https://arxiv.org/abs/2603.19461)을 알아야 해요.

### 괴델 머신(Gödel Machine)이란?

2003년 Jürgen Schmidhuber가 제안한 이론적 개념이에요. "자기 자신을 개선할 수 있는 AI"를 수학적으로 정의한 건데, 오랫동안 이론으로만 존재했어요.

### DGM (Darwin Gödel Machine, 2025)

2025년에 Meta 연구팀이 이 이론을 처음 구현했어요. 진화 알고리즘을 사용해서 코드 수준에서 자기 개선을 구현했는데:

- SWE-bench: 20.0% → 50.0%로 향상
- Polyglot: 14.2% → 30.7%로 향상

근데 DGM의 한계가 있었어요. **메타 메커니즘 자체가 고정**되어 있었거든요. 즉, 어떻게 개선할지의 방법은 인간이 설계한 그대로였어요. 코딩 도메인 외에서는 성능이 급락했고요.

### DGM-H (DGM-Hyperagents, 2026)

> "DGM-H extends DGM by eliminating the requirement that task performance and self-improvement ability must be aligned." — 논문 요약

DGM-H는 이 제약을 없앴어요. 태스크 성능과 자기 개선 능력이 반드시 연결될 필요가 없어졌고, 덕분에 **어떤 도메인에서도** 동작할 수 있게 됐어요.

| 특성 | 기존 DGM | DGM-Hyperagents |
|------|----------|-----------------|
| 메타 메커니즘 수정 가능 여부 | 불가능 | 가능 |
| 지원 도메인 | 코딩 중심 | 범도메인 |
| 개선 전이 | 없음 | 도메인 간 전이 가능 |
| 메모리 지속성 | 없음 | 자율 개발 |

---

## 4. 실험 결과: 숫자로 보는 성능

[the-decoder.com 분석](https://the-decoder.com/metas-hyperagents-improve-at-tasks-and-improve-at-improving/)에 따르면 DGM-H는 4개 도메인에서 테스트됐어요.

### 도메인별 성능 향상

| 도메인 | 시작 성능 | 최종 성능 | 향상률 |
|--------|-----------|-----------|--------|
| 코딩 (Polyglot) | 0.084 | 0.267 | **+218%** |
| 논문 리뷰 | 0.0 | 0.710 | **신규 달성** |
| 로보틱스 보상 설계 | 0.060 | 0.372 | **+520%** |
| 올림피아드 수학 (전이) | 0.0 | 0.630 | **크로스도메인 전이** |

특히 마지막 결과가 충격적이에요. 논문 리뷰와 로보틱스 도메인에서 훈련한 DGM-H가, **전혀 배우지 않은** 올림피아드 수학 채점 태스크에서 0.630을 달성했거든요. 기존 DGM 메타 에이전트는 0.0이었는데요.

### 자율 개발한 기능들

인간이 지시하지 않았는데 시스템이 스스로 개발한 기능들이에요:

- **영구 메모리(Persistent Memory)**: 이전 반복(iteration)의 인사이트를 합성하는 메모리 시스템
- **성능 추적기(Performance Tracker)**: 어떤 전략이 효과적인지 기록
- **환경 변수 지식베이스**: 실행 환경을 문서화
- **2단계 처리 파이프라인**: 효율적인 작업 처리를 위한 구조 자율 개발

> "These meta-level improvements transfer across domains and accumulate across runs." — 논문에서

한 번 개발된 개선사항이 다른 도메인에서도 계속 쌓여간다는 거예요. 마치 인간이 경험을 통해 학습하는 것처럼요.

---

## 5. 기존 AI Agent 프레임워크와의 비교

### 주요 접근법 비교

| 접근법 | 자기 수정 | 안전 보장 | 상태 |
|--------|-----------|-----------|------|
| **HyperAgents** | 가능 (코드 수준) | 형식 검증 | 연구 단계 |
| Constitutional AI | 불가능 | 규칙 기반 | 프로덕션 |
| RLHF | 불가능 | 인간 피드백 | 프로덕션 |
| DSPy (Stanford) | 프롬프트 수준 | 제한적 | 프로덕션 |
| AutoGPT류 | 제한적 | 없음 | 실험적 |

### HyperAgents가 다른 멀티에이전트 시스템과 다른 점

기존 멀티에이전트 시스템(LangGraph, AutoGen 등)은 에이전트들이 **분리된 역할**을 맡아요. 태스크를 하는 에이전트, 검토하는 에이전트, 조율하는 오케스트레이터가 따로 있죠.

HyperAgents는 이 구분 자체를 없애요. 태스크 에이전트와 메타 에이전트가 **하나의 수정 가능한 프로그램**으로 합쳐져요. 이 덕분에:

- 역할 간 커뮤니케이션 오버헤드 없음
- 개선 전략이 태스크 수행 중에도 실시간으로 변화 가능
- 한 도메인에서 배운 개선 방법이 다른 도메인에 전이 가능

[Hacker News 커뮤니티 분석](https://news.ycombinator.com/item?id=47505670)에서 연구자들은 이렇게 말해요:

> "They are trying to modify the scaffolding around a frozen FM until they get something better." — HN 댓글

즉, 모델 가중치를 변경하는 게 아니라 코드 스캐폴딩(scaffolding)을 수정하는 방식이에요. LLM 자체는 그대로인데, 그 주변의 프로그램이 진화하는 거죠.

### MiniMax M2.7과의 비교

[AgentConn 분석](https://agentconn.com/blog/self-evolving-ai-agents-minimax-m27-darwin-godel-2026/)에서 흥미로운 비교가 나와요:

- **MiniMax M2.7**: 가중치 레벨에서 자기 진화 (모델 훈련 참여)
- **HyperAgents/DGM-H**: 코드 레벨에서 자기 진화 (소스코드 재작성)

둘 다 "더 잘 배우는 법을 배우는" 시스템이지만, 메커니즘이 달라요. 이게 동시다발적으로 여러 연구 그룹에서 나타나고 있다는 것 자체가 AI 분야의 패러다임 전환을 시사한다는 거예요.

---

## 6. Meta의 AI 전략에서 HyperAgents의 위치

### Meta Superintelligence Labs (MSL)

[Built In 분석](https://builtin.com/artificial-intelligence/meta-superintelligence-labs)에 따르면 Meta는 AI 전략을 대대적으로 재편하고 있어요.

**MSL의 4개 팀:**
1. **TBD Lab**: Llama 언어 모델 개발 (Alexandr Wang 주도)
2. **FAIR**: 세계 모델(World Models) 등 기초 AI 연구 (Rob Fergus 주도)
3. **Products and Applied Research**: 소비자 제품 통합 (Nat Friedman 주도)
4. **MSL Infra**: AI 인프라 구축 (Aparna Ramani 주도)

HyperAgents는 FAIR(Fundamental AI Research) 팀의 연구 결과로, Meta의 기초 연구 역량을 보여주는 사례예요.

### 2026년 Meta AI 로드맵

[klover.ai 분석](https://www.klover.ai/meta-ai-strategy-from-open-source-to-superintelligence-dominance/)에 따르면 Meta의 2026년 핵심 전략은:

> "From Open-Source Champion to Superintelligence Dominance"

**플래그십 모델 로드맵:**
- **Mango**: 고품질 멀티모달 세계 모델, 생성 비디오 분야 목표
- **Avocado/Muse Spark**: 추론 중심 LLM, SWE-bench 60% 목표

**투자 규모:** 2026년 AI 관련 설비투자(CapEx) $1150억~$1350억 (전년 대비 약 2배)

### HyperAgents의 전략적 의미

HyperAgents는 단순한 연구 논문이 아니에요. Meta가 추구하는 **"자율적으로 개선되는 AI 시스템"**의 개념 증명(Proof of Concept)이에요. 미래의 Llama 모델들이 스스로 개선되고, 스스로 더 나은 훈련 방법을 찾는다면? 그게 바로 Meta가 지향하는 방향이에요.

---

## 7. 오픈소스로 직접 써볼 수 있어요

좋은 소식이 있어요. HyperAgents는 **오픈소스**로 공개됐어요!

**GitHub**: [facebookresearch/HyperAgents](https://github.com/facebookresearch/Hyperagents)

라이선스는 CC BY-NC-SA 4.0이에요 (비상업용). 상업적 이용은 Meta와 별도 계약이 필요해요.

### 설치 방법

```bash
# Python 3.12 필요
python3.12 -m venv venv_nat
source venv_nat/bin/activate
pip install -r requirements.txt
pip install -r requirements_dev.txt
bash ./setup_initial.sh
```

### API 키 설정 (.env 파일)

```
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
GEMINI_API_KEY=...
```

### 실행

```bash
python generate_loop.py --domains coding
```

도커로도 실행 가능해요:

```bash
docker build --network=host -t hyperagents .
```

근데 솔직히 말하면, **지금 당장 프로덕션에 쓰기는 어려워요**. 왜냐면:

1. 세 개의 LLM API 키가 동시에 필요
2. 50번 반복(iteration)에 약 8800만 토큰 소비 (비용 엄청남)
3. 공식 경고: "모델이 생성한 코드를 실행하므로 파괴적인 동작을 할 수 있음"
4. IDE 플러그인이나 CLI 래퍼 없음 — 순수 연구 도구

연구 목적이나 실험 목적으로는 충분히 써볼 만해요.

---

## 8. 한계와 주의사항

HN 커뮤니티와 여러 연구자들이 지적한 현실적인 한계예요:

### 기술적 한계

**평가의 주관성 문제:**

> "Evaluation is scrutiny for the person who wants the thing. It's subjective." — HN 댓글

완전 자율 개선을 하려면 객관적인 평가 지표가 필요한데, 현실의 많은 태스크는 주관적이에요.

**재귀 임계점(Recursive Threshold) 문제:**

HyperAgents는 특정 모듈을 개선할 수 있지만, 개선 엔진 자체를 완전히 재귀적으로 개선하는 건 여전히 이론적인 영역이에요.

**계산 비용:**

한 번의 실험 실행에 약 8800만 토큰이 필요해요. 현재 프런티어 모델 비용으로는 수백만 원이 될 수 있어요.

### 안전 우려

Meta 연구팀도 이 점을 강조하고 있어요:

> "AI safety must be placed at the core as systems gain self-modification capabilities." — 논문에서

스스로 개선되는 AI는 안전 기능을 스스로 제거하거나, 성능 지표에 과적합할 위험이 있어요. 이를 막기 위해 **정렬 앵커(Alignment Anchors)** — 절대 수정 불가능한 핵심 목표 — 개념을 도입했어요.

### 프로덕션까지의 거리

[Verdent.ai 분석](https://www.verdent.ai/guides/meta-hyperagents-ai-coding)은 냉정하게 평가해요:

> "The gap between research framework and production tool represents three to five years of engineering work."

---

## 9. 앞으로의 방향

HyperAgents가 보여준 방향은 분명해요. 앞으로의 AI는:

1. **자기 개선(Self-Improvement)**: 단순히 더 좋은 성능이 아니라, 더 잘 개선되는 능력을 갖추게 될 거예요
2. **도메인 전이(Cross-Domain Transfer)**: 한 분야에서 배운 개선 전략이 다른 분야에 자동으로 적용되는 시대가 올 거예요
3. **축적되는 AI(Accumulative AI)**: 각 실행이 이전 실행의 인사이트를 쌓아가는, 점점 더 강해지는 AI 시스템

근데 이게 흥분될수록 조심해야 할 부분도 있어요. HN 커뮤니티의 한 연구자는 이렇게 말해요:

> "The work represents 'incremental' progress rather than 'runaway self-improvement'." — 연구자 논평

맞아요. 아직은 인간이 설계한 프레임워크 안에서의 개선이에요. 완전한 재귀적 자기 개선까지는 아직 길이 남아있어요.

하지만 확실한 건, Meta의 HyperAgents가 그 길의 중요한 이정표라는 거예요.

---

## 참고문헌

| 번호 | 출처 | URL |
|------|------|-----|
| 1 | HyperAgents 논문 (arXiv 2603.19461) | https://arxiv.org/abs/2603.19461 |
| 2 | AI at Meta 공식 리서치 페이지 | https://ai.meta.com/research/publications/hyperagents/ |
| 3 | GitHub 오픈소스 리포 | https://github.com/facebookresearch/Hyperagents |
| 4 | MarkTechPost 분석 | https://www.marktechpost.com/2026/03/23/meta-ais-new-hyperagents-dont-just-solve-tasks-they-rewrite-the-rules-of-how-they-learn/ |
| 5 | The Decoder 기술 분석 | https://the-decoder.com/metas-hyperagents-improve-at-tasks-and-improve-at-improving/ |
| 6 | Hacker News 커뮤니티 논의 | https://news.ycombinator.com/item?id=47505670 |
| 7 | AgentConn 자기 진화 AI 비교 | https://agentconn.com/blog/self-evolving-ai-agents-minimax-m27-darwin-godel-2026/ |
| 8 | Verdent.ai HyperAgents 가이드 | https://www.verdent.ai/guides/meta-hyperagents-ai-coding |
| 9 | Built In: Meta Superintelligence Labs | https://builtin.com/artificial-intelligence/meta-superintelligence-labs |
| 10 | Klover.ai: Meta AI 전략 분석 | https://www.klover.ai/meta-ai-strategy-from-open-source-to-superintelligence-dominance/ |
| 11 | Pooya Blog: HyperAgents 기술 해설 | https://pooya.blog/blog/hyperagents-self-improving-ai-meta-research-2026/ |
| 12 | HuggingFace Papers | https://huggingface.co/papers/2603.19461 |

---

> 이 글은 2026년 4월 기준으로 작성되었으며, Claude Code를 활용한 Auto Research Pipeline으로 생성되었습니다.

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. HyperAgents가 기존 AI 에이전트 구조와 결정적으로 다른 점은 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 태스크 에이전트와 메타 에이전트를 하나의 수정 가능한 프로그램으로 합쳐서, 개선 절차(메타 메커니즘) 자체도 스스로 개선할 수 있게 만든 점이에요.

**해설**: 기존 에이전트는 문제를 푸는 태스크 에이전트와 개선 방법을 정하는 메타 에이전트가 분리돼 있고, 메타 에이전트는 인간이 설계한 대로 고정돼 있었죠. HyperAgents는 이 경계를 허물어서 "어떻게 하면 더 잘 개선할 수 있는지"까지 AI가 스스로 터득하게 만든 거예요.

</details>

**Q2. OX 퀴즈! HyperAgents는 LLM의 모델 가중치를 직접 수정하면서 자기 개선을 해요. (O/X)**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X

**해설**: HyperAgents는 모델 가중치가 아니라 코드 스캐폴딩을 수정하는 방식이에요. LLM 자체는 그대로 두고 그 주변의 프로그램이 진화하는 거죠. HN 댓글에서도 "frozen FM 주변의 스캐폴딩을 수정한다"고 표현했고, 가중치 레벨에서 자기 진화하는 MiniMax M2.7과는 메커니즘이 다른 접근이에요.

</details>

**Q3. 기존 DGM(Darwin Gödel Machine)의 가장 큰 한계는 무엇이었고, DGM-H는 이를 어떻게 극복했나요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: DGM은 메타 메커니즘 자체가 고정되어 있어서 코딩 외 도메인에서는 성능이 급락했어요. DGM-H는 태스크 성능과 자기 개선 능력이 반드시 연결돼야 한다는 제약을 없애서 범도메인에서 동작할 수 있게 했어요.

**해설**: DGM은 2025년에 괴델 머신 이론을 처음 구현해서 SWE-bench 성능을 크게 올렸지만, 어떻게 개선할지의 방법은 여전히 인간 설계 그대로였죠. DGM-H는 메타 메커니즘도 수정 가능하게 만들었고, 덕분에 도메인 간 개선 전이까지 가능해졌어요.

</details>

**Q4. 실험 결과 중 "크로스도메인 전이"가 충격적이라고 평가받은 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 논문 리뷰와 로보틱스 도메인에서만 훈련한 DGM-H가, 전혀 배우지 않은 올림피아드 수학 채점 태스크에서도 좋은 성능을 냈기 때문이에요. 기존 DGM 메타 에이전트는 같은 태스크에서 0점이었죠.

**해설**: 한 도메인에서 개발한 메타 수준의 개선사항이 다른 도메인으로 전이되고 실행을 거듭하며 축적된다는 게 논문의 핵심 주장인데요. 이 결과가 그 주장을 실제로 입증한 사례라서 의미가 커요. 마치 인간이 한 분야의 경험을 다른 분야에 응용하는 것과 비슷하죠.

</details>

**Q5. HyperAgents 실험 중 인간이 지시하지 않았는데 시스템이 스스로 개발한 기능의 예를 두 가지 이상 들어볼까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 영구 메모리(이전 반복의 인사이트를 합성), 성능 추적기(어떤 전략이 효과적인지 기록), 환경 변수 지식베이스, 2단계 처리 파이프라인 중 두 가지 이상이면 정답이에요.

**해설**: 이 기능들은 사람이 만들라고 시킨 게 아니라 시스템이 자기 개선 과정에서 필요하다고 판단해 스스로 만들어낸 것들이에요. 특히 영구 메모리는 실행을 거듭할수록 인사이트가 쌓이는 "축적되는 AI"의 기반이 된다는 점에서 중요하죠.

</details>

**Q6. 자기 수정 능력을 가진 AI의 안전 문제를 막기 위해 HyperAgents가 도입한 개념은 무엇인가요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 정렬 앵커(Alignment Anchors) — 절대 수정 불가능한 핵심 목표예요.

**해설**: 스스로 개선되는 AI는 안전 기능을 스스로 제거하거나 성능 지표에 과적합할 위험이 있어요. 그래서 시스템이 아무리 자기 코드를 고쳐도 건드릴 수 없는 핵심 목표를 박아둔 거죠. Meta 연구팀도 자기 수정 능력이 커질수록 AI 안전이 핵심에 놓여야 한다고 강조하고 있어요.

</details>

**Q7. 응용 시나리오! 회사 동료가 "HyperAgents를 우리 서비스에 바로 도입하자"고 제안한다면, 본문 내용을 근거로 어떤 점을 지적해야 할까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 아직 프로덕션에 쓰기 어려운 순수 연구 도구라는 점이에요. 세 개의 LLM API 키가 동시에 필요하고, 토큰 비용이 엄청나며, 모델이 생성한 코드를 실행해서 파괴적 동작 위험이 있고, 라이선스도 비상업용(CC BY-NC-SA 4.0)이라 상업적 이용엔 Meta와 별도 계약이 필요해요.

**해설**: 본문에서도 50번 반복에 약 8800만 토큰이 소비돼 비용이 수백만 원에 달할 수 있다고 했죠. Verdent.ai 분석은 연구 프레임워크와 프로덕션 도구 사이의 간극을 3~5년의 엔지니어링 작업으로 평가했어요. 연구나 실험 목적으로는 충분히 써볼 만하지만요.

</details>

**Q8. OX 퀴즈! HyperAgents는 완전한 재귀적 자기 개선(runaway self-improvement)을 이미 달성했어요. (O/X)**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X

**해설**: 연구자들은 이 작업을 "폭주하는 자기 개선"이 아니라 "점진적 진전"으로 평가해요. 특정 모듈은 개선할 수 있지만 개선 엔진 자체를 완전히 재귀적으로 개선하는 건 여전히 이론적인 영역이고, 아직은 인간이 설계한 프레임워크 안에서의 개선이거든요. 그래도 그 길의 중요한 이정표라는 건 분명하죠.

</details>
