---
layout: post
title: "LLM 환각(Hallucination) 완전 정복: 완화 기법부터 대기업 프로덕션 방안까지 (2025~2026)"
date: 2026-06-11
category: AI Safety & Alignment
---

# LLM 환각(Hallucination) 완전 정복: 완화 기법부터 대기업 프로덕션 방안까지 (2025~2026)

> 📊 **발표자료**: [llm-hallucination-presentation.pptx](./llm-hallucination-presentation.pptx)

LLM이 자신 있게 틀린 말을 내뱉는 문제, 즉 환각(hallucination)은 2026년 현재도 완전히 해결되지 않았다. 이 글은 환각의 정의와 원인, 분류 체계, 완화 기법, 측정 방법, 그리고 대기업들이 프로덕션에서 실제로 적용 중인 방안까지 2025~2026 최신 연구를 기준으로 정리한다.

**3줄 요약:**

- 환각은 이론적으로 **제거 불가능**하지만, RAG·추론·검증 레이어를 겹쳐 쌓으면 프로덕션 수준에서 **관리 가능**하다.
- 측정이 가장 약한 고리다. 최고 성능 모델(GPT-5)도 에이전트 환각의 발생 지점을 짚어내는 정확도가 41.1%에 그치고, 벤치마크 정답 레이블 자체가 오염된 사례도 보고된다.
- 대기업들은 모두 "출력을 근거 문서에 묶는(grounding)" 방향으로 수렴했다. AWS Guardrails, Vertex AI Grounding, Azure Groundedness Detection, Anthropic Citations가 모두 같은 계열이다.

---

## 목차

1. [환각이란 무엇이고, 왜 생기는가](#1-환각이란-무엇이고-왜-생기는가)
2. [환각의 분류 체계](#2-환각의-분류-체계)
3. [완화 기법: RAG와 추론](#3-완화-기법-rag와-추론)
4. [측정: 평가와 벤치마크](#4-측정-평가와-벤치마크)
5. [에이전트 환각](#5-에이전트-환각)
6. [대기업 프로덕션 방안](#6-대기업-프로덕션-방안)
7. [한계와 미해결 과제](#7-한계와-미해결-과제)
8. [정리](#8-정리)
9. [참고문헌](#9-참고문헌)

---

## 1. 환각이란 무엇이고, 왜 생기는가

환각은 단순한 "틀린 정보"가 아니다. **사실처럼 들리지만 근거가 없거나, 입력 문맥과 모순되는 내용을 생성하는 현상**을 말한다. 출력이 세계의 사실과 일치하는지를 따지는 factuality(사실성)와는 구별되는 개념이다([Lakera 가이드](https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models)).

원인은 구조적이다. [OpenAI의 분석](https://openai.com/index/why-language-models-hallucinate/)에 따르면, 언어 모델은 검증된 사실을 조회하는 게 아니라 학습 데이터의 패턴으로 다음 토큰을 예측한다. 정보가 없으면 그럴듯한 내용으로 빈칸을 채우며, "모른다"고 말하는 메커니즘이 기본적으로 내장되어 있지 않다. 여기에 학습 데이터 편향, 희소 지식, 컨텍스트 길이 초과 같은 요인이 겹친다.

[Frontiers in AI (2025)](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1622292/full)의 원인 귀인 프레임워크는 환각의 변동 요인을 세 가지로 나눈다.

| 요인 | 의미 |
| :--- | :--- |
| Prompt Sensitivity | 같은 질문도 표현 방식에 따라 환각 여부가 달라짐 |
| Model Variability | 같은 프롬프트라도 샘플링 랜덤성 때문에 결과가 달라짐 |
| Joint Attribution Score | 위 두 요인의 복합 효과를 정량화한 지표 |

이 글 전체를 관통하는 결론을 먼저 말하면: **환각은 불가피(inevitable)하지만 완화는 가능(mitigable)하다.** 완전 제거는 현재 기술로 불가능하고, 목표는 프로덕션 수준의 관리다.

---

## 2. 환각의 분류 체계

최신 서베이([arXiv:2510.24476](https://arxiv.org/abs/2510.24476), [MDPI AI 2025](https://www.mdpi.com/2673-2688/6/10/260))는 환각을 세 축으로 분류한다. 어떤 축의 환각이냐에 따라 효과적인 완화 기법이 달라지기 때문에, 분류는 단순한 교과서적 정리가 아니라 대응 전략 선택의 출발점이다.

| 분류 축 | 유형 | 설명 | 예시 / 비고 |
| :--- | :--- | :--- | :--- |
| 내용 | Knowledge Hallucination | 사실 관계 오류 | "아인슈타인은 1925년에 태어났다" |
| 내용 | Logic Hallucination | 추론 과정 자체의 오류 | "A>B이고 B>C이므로 C>A" |
| 컨텍스트 | Extrinsic | 주어진 문서에 **없는** 정보를 생성 | 요약·RAG에서 특히 문제 |
| 컨텍스트 | Intrinsic | 주어진 문서와 **모순되는** 내용을 생성 | 입력 대조로 검출 가능 |
| 발생 원인 | Prompt-induced | 입력 프롬프트가 유도한 환각 | 프롬프트 수정으로 완화 |
| 발생 원인 | Model-induced | 파라미터 지식 부족·편향에서 비롯 | 학습 단계 개입 필요 |

[HalluLens (arXiv:2504.17550)](https://arxiv.org/html/2504.17550v1)는 이 분류를 정교화해 평가 프레임워크로 발전시켰다.

---

## 3. 완화 기법: RAG와 추론

### 3.1 RAG: 검색 증강 생성

RAG(Retrieval-Augmented Generation)는 가장 널리 채택된 완화 기법이다. 외부 지식 베이스에서 관련 문서를 검색한 뒤 그것을 근거로 생성하는 방식으로, 사실 지식을 모델 파라미터 밖으로 빼내는(externalize) 효과가 있다([arXiv:2601.19927](https://arxiv.org/pdf/2601.19927)). 최신 정보 반영과 출처 추적이 가능하다는 점이 핵심 장점이다.

다만 RAG는 환각을 **줄일 뿐 제거하지 못한다.** 실패 경로가 두 갈래다.

- 검색 단계에서 잘못된 문서를 가져오면, 오히려 잘못된 근거가 환각을 **유발**한다([arXiv:2401.11817](https://arxiv.org/abs/2401.11817)).
- 모델이 검색 결과를 무시하고 파라미터 지식에 의존하는 경우가 있다.

### 3.2 추론(Reasoning) 기반 완화

Chain-of-Thought, ReAct, 자기 일관성 체크처럼 추론 과정을 명시적으로 거치게 하는 방법도 효과적이다. 복잡한 작업을 단계로 분해하고 중간 단계를 검증하게 만들면 최종 답의 오류율이 낮아진다([MDPI Information 2025](https://www.mdpi.com/2078-2489/16/7/517)).

단, 역설이 있다. [Emergent Mind의 정리](https://www.emergentmind.com/topics/reasoning-driven-hallucination)처럼 **추론이 환각을 줄이기도 하지만 만들기도 한다.** 긴 추론 체인에서 중간 단계 하나가 틀리면 그 오류가 최종 답까지 전파된다.

### 3.3 기타 완화 기법

[MDPI Mathematics (2025)](https://www.mdpi.com/2227-7390/13/5/856) 기준으로 정리하면 다음과 같다.

| 기법 | 원리 | 특징 |
| :--- | :--- | :--- |
| Self-Consistency | 여러 번 샘플링 후 가장 일관된 답 선택 | 추론 비용 증가, 단순 사실 질문에 효과적 |
| Validation Agent | 별도 모델이 출력을 검증 | 멀티 에이전트 시스템에서 활용 |
| RLHF / Constitutional AI | 사람 피드백·규칙 기반 파인튜닝 | 범용 품질에 좋지만 도메인 특화에는 한계 |
| Calibration | 불확실성 표현 개선 | "모른다"고 말하도록 훈련 |

---

## 4. 측정: 평가와 벤치마크

환각을 막으려면 먼저 측정할 수 있어야 하는데, 측정 자체가 현재 가장 약한 고리다.

### 4.1 SimpleQA — 명확한 사실 질문

[OpenAI SimpleQA (arXiv:2411.04368)](https://arxiv.org/abs/2411.04368)는 정답이 명확한 사실 질문으로 구성된 벤치마크다. 채점이 3분류라는 점이 핵심이다.

| 판정 | 의미 |
| :--- | :--- |
| correct | 완전히 정확한 답 |
| incorrect | 틀린 답 (환각 포함) |
| not_attempted | "모른다"고 인정하거나 답하지 않음 |

`not_attempted`를 별도로 분리한 것이 포인트다. 틀리게 답하는 것과 모른다고 하는 것은 완전히 다른 행동이고, 이 둘을 구분해야 calibration 개선을 측정할 수 있다.

### 4.2 Semantic Entropy — 확률적 환각 탐지

[Nature (2024)](https://www.nature.com/articles/s41586-024-07421-0)에 실린 semantic entropy 기법은 같은 질문에 대한 여러 생성 결과의 **의미적 다양성**을 측정한다. 엔트로피가 높으면 모델이 불확실하다는 신호이고, 환각 가능성이 높다고 본다.

AUROC **0.790**으로 완벽하진 않지만, 별도 레이블 데이터 없이 환각 가능성을 추정할 수 있다는 것이 강점이다.

### 4.3 AgentHallu — 에이전트 전용 벤치마크

[AgentHallu (arXiv:2601.06818)](https://arxiv.org/abs/2601.06818)는 다단계 추론·툴 호출 에이전트에 특화된 벤치마크다. 693개의 에이전트 작업 궤적(trajectory)을 7개 프레임워크, 5개 도메인(의료·코딩·법률 등)에 걸쳐 수집했다.

가장 주목할 숫자: **환각 귀인(attribution) 정확도가 최고 성능 모델(GPT-5)조차 41.1%**다. 환각이 발생했다는 사실을 아는 것과, 어떤 단계에서 왜 발생했는지 짚어내는 것은 전혀 다른 문제이며 후자는 아직 미해결이다.

### 4.4 벤치마크 자체의 오염

[arXiv:2411.15594](https://arxiv.org/abs/2411.15594)에 따르면 벤치마크 정답 레이블(gold label)의 **최대 60%가 오염**(레이블 자체에 환각 포함)된 사례가 보고됐다. 벤치마크 점수를 액면 그대로 믿어선 안 되고, 환각 평가 연구에서 human evaluation이 여전히 필수인 이유다.

---

## 5. 에이전트 환각

에이전트가 툴을 호출하거나 여러 단계에 걸쳐 추론할 때의 환각은 일반 텍스트 생성과 다른 양상을 보인다. 핵심 차이는 **오류의 전파**다. ReAct 루프에서 Thought 단계 하나가 틀리면 이후의 모든 Action·Observation이 오염된다([MindStudio](https://www.mindstudio.ai/blog/what-is-react-loop-ai-agent-reasoning)).

### 5.1 주요 패턴

[arXiv:2509.18970](https://arxiv.org/html/2509.18970v1)과 [arXiv:2510.22977](https://arxiv.org/pdf/2510.22977)이 정리한 에이전트 환각의 대표 패턴은 다음과 같다.

| 패턴 | 설명 |
| :--- | :--- |
| 툴 파라미터 오류 | 존재하지 않는 API 파라미터나 잘못된 값을 생성 |
| 루프 환각 | ReAct 루프에서 이전 단계 결과를 잘못 해석하거나 무시 |
| 컨텍스트 손실 | 긴 멀티스텝 작업에서 이전 정보를 잊어버림 |
| 계획 환각 | 실행 불가능한 계획을 수립 |

### 5.2 멀티 에이전트 검증

[AWS의 멀티 에이전트 검증 패턴](https://dev.to/aws/how-to-stop-ai-agents-from-hallucinating-silently-with-multi-agent-validation-3f7e)은 "침묵하는 환각(silent hallucination)" — 에러 없이 조용히 틀리는 경우 — 을 잡기 위해 생성 에이전트와 별도의 검증 에이전트를 두는 구조를 제안한다.

참고로, "에이전트 환각이 일반 LLM 환각보다 본질적으로 더 어려운 문제다"라는 주장은 자주 보이지만 아직 방법론적으로 충분히 입증되지 않았다. 현재 확실히 말할 수 있는 것은 귀인(attribution)이 어렵다는 것까지다.

---

## 6. 대기업 프로덕션 방안

벤더들의 접근은 한 문장으로 요약된다: **출력을 근거 문서에 묶고(grounding), 묶이지 않은 출력을 탐지·차단한다.**

| 벤더 | 제품 | 방식 |
| :--- | :--- | :--- |
| AWS | Bedrock Guardrails + Automated Reasoning Checks | grounding 점수 기반 차단 + 형식 검증 |
| Google | Vertex AI Grounding | 실시간 검색·기업 데이터 기반 grounding |
| Microsoft | Azure Groundedness Detection | 소스 문서 근거 여부를 0~1 점수화 |
| Anthropic | Citations API | 응답의 각 주장에 출처 인용을 명시 |
| OpenAI | 시스템 카드 + 원인 연구 | 벤치마크 공개 + 메커니즘 분석 |

> **주의**: 아래 효과 수치들은 모두 벤더 자사 문서 기준이며, 독립적인 제3자 검증은 부족하다. 도입 전 자체 평가가 필요하다.

### 6.1 AWS Bedrock

- **Contextual Grounding Check** ([문서](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html)): 응답이 제공된 컨텍스트에 근거하는지 자동 체크하고, grounding 점수가 임계값 미만이면 응답을 차단한다.
- **Automated Reasoning Checks** ([블로그](https://aws.amazon.com/blogs/aws/minimize-ai-hallucinations-and-deliver-up-to-99-verification-accuracy-with-automated-reasoning-checks-now-available/)): 형식적 검증(formal verification)으로 정책 준수 여부를 체크한다. AWS는 정책 준수 문장에 대해 최대 99% 검증 정확도를 주장한다.

### 6.2 Google Vertex AI

[Vertex AI Grounding](https://cloud.google.com/blog/products/ai-machine-learning/how-vertex-ai-grounding-helps-build-more-reliable-models)은 두 가지 옵션을 제공한다. **Google Search Grounding**(실시간 검색 결과를 근거로 활용 — 최신 정보 환각에 효과적)과 **Enterprise Data Grounding**(기업 자체 문서·DB 기반)이다.

### 6.3 Microsoft Azure AI

[Groundedness Detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness)은 모델 출력이 소스 문서에 근거하는지를 0~1 점수로 평가하며, RAG 파이프라인에 직접 통합되도록 설계됐다.

### 6.4 Anthropic

[Citations API](https://www.anthropic.com/news/introducing-citations-api)는 응답의 각 주장이 컨텍스트의 어느 소스에서 왔는지를 인용 형태로 반환한다. 환각 감소뿐 아니라 사용자가 직접 출처를 검증할 수 있게 한다는 점에서 접근이 다르다.

### 6.5 OpenAI

[GPT-5 시스템 카드](https://cdn.openai.com/gpt-5-system-card.pdf)에서 SimpleQA 등 환각 벤치마크 결과를 공개하고, [별도 연구](https://openai.com/index/why-language-models-hallucinate/)로 환각의 발생 메커니즘을 분석했다. 제품 기능보다는 측정·공개 중심의 접근이다.

### 6.6 Vectara Hallucination Leaderboard

벤더 중립 비교가 필요하면 [Vectara의 리더보드](https://www.vectara.com/blog/introducing-the-next-generation-of-vectaras-hallucination-leaderboard)가 유용하다. 다양한 LLM의 환각 비율을 도메인·유형별로 비교한다.

---

## 7. 한계와 미해결 과제

- **평가 자체가 환각에 취약하다.** LLM-as-judge는 평가 과정에서 스스로 환각할 수 있고, human judge 간 불일치와 벤치마크 레이블 오류도 겹친다([arXiv:2401.11817](https://arxiv.org/abs/2401.11817)).
- **귀인이 안 된다.** GPT-5조차 에이전트 환각의 발생 지점·원인을 짚는 정확도가 41.1%다(4.3절).
- **완화 기법이 새 환각을 만든다.** RAG는 잘못된 검색 결과로 오히려 환각을 유발할 수 있고, 추론 체인은 중간 단계 오류를 증폭할 수 있다([arXiv:2411.16594](https://arxiv.org/pdf/2411.16594)).
- **벤더 주장의 독립 검증이 부족하다.** 6장의 프로덕션 방안 효과는 대부분 벤더 1차 문서 기준이다.

---

## 8. 정리

| 레이어 | 방법 | 성숙도 |
| :--- | :--- | :---: |
| 학습 단계 | RLHF, Constitutional AI, Calibration | 높음 |
| 추론 단계 | RAG, CoT, Self-Consistency | 높음 |
| 에이전트 레이어 | 멀티 에이전트 검증, ReAct 검증 루프 | 중간 |
| 인프라/플랫폼 | AWS Guardrails, Vertex Grounding, Azure Groundedness, Anthropic Citations | 중간~높음 |
| 측정·평가 | SimpleQA, Semantic Entropy, AgentHallu | 진행 중 |

환각은 없애는 문제가 아니라 **관리하는** 문제다. 여러 레이어에 방어선을 두고, 지속적으로 측정하며 개선하는 것이 현재로서는 가장 현실적인 접근이다. 그리고 그 측정이 지금 가장 약한 고리라는 점이, 2026년 환각 연구의 핵심 과제다.

---

## 9. 참고문헌

1. [Hallucination Survey — arXiv:2510.24476](https://arxiv.org/abs/2510.24476)
2. [Hallucination Mitigation — MDPI AI 2025](https://www.mdpi.com/2673-2688/6/10/260)
3. [Mathematical approaches — MDPI Mathematics 2025](https://www.mdpi.com/2227-7390/13/5/856)
4. [RAG & Mitigation Survey — arXiv:2601.19927](https://arxiv.org/pdf/2601.19927)
5. [Lakera Hallucination Guide](https://www.lakera.ai/blog/guide-to-hallucinations-in-large-language-models)
6. [Attribution Framework — Frontiers in AI 2025](https://www.frontiersin.org/journals/artificial-intelligence/articles/10.3389/frai.2025.1622292/full)
7. [SimpleQA — arXiv:2411.04368](https://arxiv.org/abs/2411.04368)
8. [Semantic Entropy — Nature 2024](https://www.nature.com/articles/s41586-024-07421-0)
9. [AgentHallu — arXiv:2601.06818](https://arxiv.org/abs/2601.06818)
10. [HalluLens — arXiv:2504.17550](https://arxiv.org/html/2504.17550v1)
11. [Benchmark Label Quality — arXiv:2411.15594](https://arxiv.org/abs/2411.15594)
12. [AWS Bedrock Contextual Grounding](https://docs.aws.amazon.com/bedrock/latest/userguide/guardrails-contextual-grounding-check.html)
13. [AWS Automated Reasoning Checks](https://aws.amazon.com/blogs/aws/minimize-ai-hallucinations-and-deliver-up-to-99-verification-accuracy-with-automated-reasoning-checks-now-available/)
14. [Google Vertex AI Grounding](https://cloud.google.com/blog/products/ai-machine-learning/how-vertex-ai-grounding-helps-build-more-reliable-models)
15. [Microsoft Azure Groundedness Detection](https://learn.microsoft.com/en-us/azure/ai-services/content-safety/concepts/groundedness)
16. [Anthropic Citations API](https://www.anthropic.com/news/introducing-citations-api)
17. [GPT-5 System Card](https://cdn.openai.com/gpt-5-system-card.pdf)
18. [Agentic Tool-Call Hallucination — arXiv:2509.18970](https://arxiv.org/html/2509.18970v1)
19. [Agentic Hallucination — arXiv:2510.22977](https://arxiv.org/pdf/2510.22977)
20. [Multi-Agent Validation — AWS Dev Blog](https://dev.to/aws/how-to-stop-ai-agents-from-hallucinating-silently-with-multi-agent-validation-3f7e)
21. [Reasoning-Driven Hallucination — Emergent Mind](https://www.emergentmind.com/topics/reasoning-driven-hallucination)
22. [ReAct Loop — MindStudio](https://www.mindstudio.ai/blog/what-is-react-loop-ai-agent-reasoning)
23. [Agentic LLM Hallucination — MDPI Information 2025](https://www.mdpi.com/2078-2489/16/7/517)
24. [Vectara Hallucination Leaderboard](https://www.vectara.com/blog/introducing-the-next-generation-of-vectaras-hallucination-leaderboard)
25. [AWS Bedrock Automated Reasoning Blog](https://aws.amazon.com/blogs/machine-learning/minimize-generative-ai-hallucinations-with-amazon-bedrock-automated-reasoning-checks/)
26. [Hallucination in RAG — arXiv:2401.11817](https://arxiv.org/abs/2401.11817)
27. [Why LLMs Hallucinate — OpenAI](https://openai.com/index/why-language-models-hallucinate/)
28. [Mitigation Limits — arXiv:2411.16594](https://arxiv.org/pdf/2411.16594)

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. 환각(hallucination)과 factuality(사실성)는 같은 개념일까요? 환각의 정의를 떠올리며 답해 보세요.**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 다른 개념이에요. 환각은 "사실처럼 들리지만 근거가 없거나 입력 문맥과 모순되는 내용을 생성하는 현상"이고, factuality는 출력이 세계의 사실과 일치하는지를 따지는 개념이에요.

**해설**: 환각은 단순히 "틀린 정보"가 아니라 근거 없이 그럴듯하게 지어내는 행동 자체를 가리키는 거예요. 언어 모델은 검증된 사실을 조회하는 게 아니라 패턴으로 다음 토큰을 예측하기 때문에, 정보가 없으면 그럴듯한 내용으로 빈칸을 채우게 되죠.

</details>

**Q2. (OX) 환각은 RAG, 추론, 검증 레이어를 충분히 겹쳐 쌓으면 완전히 제거할 수 있다.**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X예요.

**해설**: 이 글 전체를 관통하는 결론이 바로 "환각은 불가피(inevitable)하지만 완화는 가능(mitigable)하다"는 거였죠. 완전 제거는 현재 기술로 불가능하고, 여러 레이어에 방어선을 두어 프로덕션 수준에서 **관리**하는 것이 현실적인 목표예요.

</details>

**Q3. 컨텍스트 기준 분류에서 Extrinsic 환각과 Intrinsic 환각은 어떻게 다를까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Extrinsic은 주어진 문서에 **없는** 정보를 지어내는 것이고, Intrinsic은 주어진 문서와 **모순되는** 내용을 생성하는 거예요.

**해설**: Extrinsic은 요약이나 RAG에서 특히 문제가 되고, Intrinsic은 입력과 대조하면 검출이 가능하다는 차이가 있어요. 어떤 축의 환각이냐에 따라 효과적인 완화 기법이 달라지기 때문에, 이 분류는 대응 전략 선택의 출발점이 되죠.

</details>

**Q4. RAG는 가장 널리 쓰이는 환각 완화 기법인데요, RAG가 오히려 환각을 유발할 수 있는 경우는 어떤 경우일까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 검색 단계에서 잘못된 문서를 가져오면 그 잘못된 근거가 오히려 환각을 유발해요. 또 모델이 검색 결과를 무시하고 파라미터 지식에 의존하는 실패 경로도 있어요.

**해설**: RAG는 사실 지식을 모델 파라미터 밖으로 빼내는 효과가 있어서 환각을 줄여주지만, 제거하지는 못해요. 추론 체인도 마찬가지로 중간 단계 하나가 틀리면 오류가 최종 답까지 전파되니, 완화 기법이 새 환각을 만들 수 있다는 점을 늘 염두에 둬야 하죠.

</details>

**Q5. SimpleQA 벤치마크가 채점을 correct / incorrect 2분류가 아니라 not_attempted까지 3분류로 나눈 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 틀리게 답하는 것과 "모른다"고 인정하는 것은 완전히 다른 행동이라서예요. 이 둘을 구분해야 calibration(불확실성 표현) 개선을 측정할 수 있어요.

**해설**: 환각의 핵심 원인 중 하나가 모델에 "모른다"고 말하는 메커니즘이 내장되어 있지 않다는 점이었죠. 그래서 모른다고 인정하는 행동을 별도 판정으로 분리해야, 모델이 얼마나 정직하게 불확실성을 표현하는지 따로 평가할 수 있는 거예요.

</details>

**Q6. (OX) 현재 최고 성능 모델은 에이전트 환각이 발생했다는 사실뿐 아니라 어느 단계에서 왜 발생했는지도 높은 정확도로 짚어낼 수 있다.**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X예요.

**해설**: AgentHallu 벤치마크에서 최고 성능 모델(GPT-5)조차 환각 귀인(attribution) 정확도가 41.1%에 그쳤어요. 환각이 발생했다는 걸 아는 것과 발생 지점·원인을 짚어내는 건 전혀 다른 문제이고, 후자는 아직 미해결 과제로 남아 있죠.

</details>

**Q7. AWS, Google, Microsoft, Anthropic 같은 대기업들의 프로덕션 환각 대응 방안은 공통적으로 어떤 방향으로 수렴했나요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: "출력을 근거 문서에 묶는(grounding)" 방향이에요. 묶이지 않은 출력은 탐지하고 차단하는 식이죠.

**해설**: AWS Bedrock의 Contextual Grounding Check, Google의 Vertex AI Grounding, Azure의 Groundedness Detection, Anthropic의 Citations API가 모두 같은 계열이에요. 다만 이 제품들의 효과 수치는 대부분 벤더 자사 문서 기준이라 독립적인 제3자 검증이 부족하다는 점도 같이 기억해 두면 좋아요.

</details>

**Q8. (응용) 사내 문서 기반 Q&A 챗봇을 RAG로 구축했는데, 답변이 그럴듯해 보여도 가끔 문서에 없는 내용을 지어내는 게 걱정이에요. 본문에서 소개한 방안 중 어떤 것들을 추가로 적용할 수 있을까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: grounding 검증 레이어를 추가하는 게 정석이에요. 예를 들어 Azure Groundedness Detection이나 AWS Contextual Grounding Check로 응답이 소스 문서에 근거하는지 점수화해 임계값 미만이면 차단하고, Anthropic Citations처럼 주장마다 출처를 인용하게 하거나, 별도 검증 에이전트(Validation Agent)를 두는 방법도 있어요.

**해설**: 문서에 없는 내용을 지어내는 건 전형적인 Extrinsic 환각이라서, 출력을 근거 문서와 대조하는 grounding 계열 검증이 잘 맞아요. 핵심은 한 가지 기법에 의존하지 말고 여러 레이어에 방어선을 두고 지속적으로 측정하며 개선하는 거죠.

</details>
