# AI 에이전트 평가 방식 종합 리서치 보고서

## 📊 Executive Summary

2026년 AI 에이전트 평가 분야는 **단일 에이전트 중심의 정적 벤치마크에서 멀티 에이전트 협력 중심의 동적 평가로의 대전환**을 맞고 있습니다. 기존 SWE-Bench, HumanEval 같은 벤치마크들이 여전히 유효하지만, **에이전트 간 협력, Emergent behaviors, 프로덕션 환경에서의 안정성**을 종합적으로 평가할 수 있는 새로운 프레임워크들이 급부상하고 있습니다.

---

## 1️⃣ 단일 에이전트 평가 방식 (기존)

### 1.1 주요 벤치마크

#### **SWE-Bench 패밀리** (코딩 에이전트 표준)
- **SWE-bench Verified**: GitHub 이슈 기반 소프트웨어 개발 작업 평가
  - 2024년 초: ~40% 성공률
  - 2025년 말: **>80% 성공률** (frontier models)
  - 평가 방식: 실제 테스트 스위트 실행 (Unit tests)
  - 진화: Multilingual, Multimodal, Lite 버전 추가

#### **HumanEval & HumanEval+** (코드 생성 평가)
- **원본 HumanEval**: 164개 프로그래밍 문제
  - 함수 서명, docstring, 단위 테스트 기반
  - 함수 정확성 (functional correctness) 평가
  - Zero-shot 형식 강제
  
- **HumanEval+**: 강화된 버전
  - 모든 기준 만족 필수 (all-or-nothing)
  - 더 높은 판별력 제공
  - 2025년 기준 아직도 가장 인용도 높은 벤치마크

#### **MATH & AIME 벤치마크** (수학 추론 평가)
- MATH: 중고등학교 수학 문제 (대략 12,500+ 문제)
- AIME 2024: 미국 고등학교 수학 올림피아드
- 평가 메트릭: 정확한 계산 검증 + 단계별 논리 검증

### 1.2 기본 평가 메트릭

| 메트릭 | 설명 | 사용 사례 |
|--------|------|----------|
| **Task Completion Rate** | 완료된 작업의 비율 | 모든 에이전트 유형 |
| **pass@k** | k회 시도 중 최소 1회 이상 성공 확률 | 코딩 에이전트 (여러 솔루션) |
| **pass^k** | k회 모든 시도 성공 확률 | 프로덕션 에이전트 (안정성) |
| **Accuracy** | 정확한 답변의 비율 | MATH, HumanEval |
| **Latency** | 평균 응답 시간 | 성능 평가 |
| **Cost** | 토큰 사용량 × 비용 | 경제성 평가 |
| **Error Rate** | 오류 발생 비율 | 신뢰성 평가 |

### 1.3 평가 방법론

#### **코드 기반 Grader (Code-based Graders)**
```yaml
장점:
  - 빠름, 저비용, 객관적, 재현 가능
  - 특정 조건 검증 가능
  - 디버깅 용이

단점:
  - 유효한 대안에 취약함
  - 뉘앙스 부족
  - 주관적 작업 평가 어려움
```

**구체적 방법:**
- 정확한 매칭 (exact, regex, fuzzy)
- 바이너리 테스트 (pass-fail)
- 정적 분석 (lint, type checking, security)
- 상태 검증 (outcome verification)

#### **모델 기반 Grader (LLM-as-Judge)**
```yaml
장점:
  - 유연함, 확장 가능
  - 뉘앙스 캡처
  - 오픈엔디드 작업 처리

단점:
  - 비결정적 (non-deterministic)
  - 비용 높음
  - 인간 Grader와 보정 필요
```

**구현 방식:**
- Rubric 기반 점수 부여
- 자연어 Assertion
- Pairwise comparison
- Reference 기반 평가
- 다중 심사자 합의

#### **인간 기반 평가 (Human Graders)**
```yaml
용도:
  - 금 기준(gold standard) 품질
  - 모델 기반 Grader 보정
  - 주관적 작업 (예: 글쓰기 질), UI/UX 평가
```

---

## 2️⃣ 멀티 에이전트 평가의 도전과제

### 2.1 왜 단일 평가로는 부족한가?

#### **문제점 1: 독립성 가정 위반**
- 단일 에이전트 평가는 **각 에이전트가 독립적으로 작동**한다고 가정
- 실제: 에이전트들의 출력이 다른 에이전트의 입력이 됨
- **연쇄 오류**: A 에이전트의 실패 → B 에이전트 입력 오염 → 시스템 전체 실패

#### **문제점 2: Emergent Behavior**
- 개별 에이전트는 모두 작동하지만, **조합했을 때 예측 불가능한 행동** 발생
- 협력 패턴의 효율성을 측정할 수 없음
- 에이전트 간 오해/충돌 시나리오 놓침

#### **문제점 3: 동적 환경**
- 단일 에이전트: 정적 입력 → 고정 출력
- 멀티 에이전트: 환경이 **에이전트 행동에 따라 동적으로 변함**
  - 예: A가 파일 생성 → B가 그 파일 수정 → C가 결과 검증
  - 순서, 타이밍, 상태 모두 중요

#### **문제점 4: 협력 비효율성**
- 불필요한 통신 (redundant messaging)
- 작업 중복
- 데드락 상황

### 2.2 에이전트 간 협력 평가의 핵심 요소

#### **1. Communication Efficiency (통신 효율성)**
```
메트릭:
- Messages per Task: 작업당 메시지 수
- Tokens per Task: 작업당 토큰 수
- Communication Overhead: (협력 메시지 / 전체 메시지) × 100%

계산식:
Efficiency Score = Task Success Rate / (Messages × Tokens)
```

**평가 예시:**
- A팀: 80% 성공, 50개 메시지 = 1.6
- B팀: 80% 성공, 30개 메시지 = 2.67 ⭐

#### **2. Coordination Quality (조율 품질)**
```
측정 항목:
1. 작업 할당 정확도 (Planning Score)
   - 에이전트가 올바른 작업을 받았는가?
   
2. 작업 인계 정확도 (Task Handoff Accuracy)
   - 이전 에이전트 결과가 다음 에이전트에게 올바르게 전달되었는가?
   
3. 협력 성공률 (Collaboration Success Rate)
   - 서브테스크들의 성공 비율 평균
```

#### **3. 협력 패턴 분석**
Amazon 평가 방식:
- **Planning Score**: 올바른 에이전트에게 올바른 작업이 할당되었는가?
- **Communication Score**: 작업 완료를 위한 메시지 수
- **Collaboration Success Rate**: 각 에이전트의 성공률 × 조율 성공률

### 2.3 Emergent Behaviors 평가

**Emergent Behavior 정의:** 개별 에이전트의 의도된 행동에서 나타나지 않는 시스템 수준의 새로운 행동

#### **MAEBE Framework (2025)** - 최신 접근법
```
평가 대상:
1. Safety Emergence Risks
   - Collusion: 에이전트들이 협력해서 시스템 규칙 우회
   - Deception: 멀티 에이전트 조작 행동
   - Reward Hacking: 목표를 왜곡한 협력

2. Functional Emergence
   - Novel Strategies: 예상 밖의 성공 전략
   - Behavioral Divergence: 지시와 다른 행동 패턴

3. Measurement Methods
   - Specification-based evaluation (의도된 사양과 비교)
   - Behavioral monitoring (실제 수행 추적)
   - Adversarial testing (공격자 역할 에이전트 도입)
```

---

## 3️⃣ 최신 멀티 에이전트 평가 방식

### 3.1 공신력 있는 벤치마크들

#### **MultiAgentBench (2025년 3월)** ⭐⭐⭐
**특징:**
- LLM 기반 멀티 에이전트 시스템의 협력 & 경쟁 평가
- 다양한 상호작용 시나리오 포함

**측정 메트릭:**
1. **Task Score (TS)**: 작업 완료도
2. **Coordination Score (CS)**: Milestone 기반 협력 품질
3. 다양한 조율 프로토콜 테스트:
   - Star (중앙 조정자)
   - Chain (순차적)
   - Tree (계층적)
   - Graph (완전 네트워크)

**최신 결과:**
- GPT-4o-mini: 평균 최고 점수
- 그래프 구조: 연구 시나리오에서 최고 성능
- Cognitive Planning: Milestone 달성률 +3%

**특이점:** Milestone 기반 KPI - 중간 성과물도 평가

---

#### **REALM-Bench (2025년 2월)** ⭐⭐⭐
**특징:**
- 실제 실시간 계획 & 스케줄링 작업
- 동적 환경 변화 포함
- 11가지 실제 시나리오 (공급망, 재난 대응 등)

**평가 메트릭 (6가지):**
```
1. Planning Quality Score
   - 생성된 계획의 타당성
   
2. Optimality Metric
   - 최적 해에 얼마나 가까운가?
   
3. Coordination Metric
   - 에이전트 간 조율 정도
   
4. Constraint Satisfaction
   - 제약 조건 만족도
   
5. Resource Utilization
   - 리소스 효율성
   
6. Adaptation to Disruptions
   - 예상 밖의 변화 대응 능력
```

**포함된 프레임워크:**
- LangGraph, AutoGen, CrewAI, Swarm
- GPT-4o, Claude-3.7, DeepSeek-R1

**핵심 차별점:** 리소스 관리 & 동적 재계획 능력 평가

---

#### **Windows Agent Arena (2025년 6월)** ⭐⭐⭐
**특징:**
- 멀티모달 OS 에이전트 평가 (완전 자동화)
- 실제 Windows 환경에서 동작
- 150+ 다양한 작업

**평가 구조:**
- Planning 능력
- Screen understanding
- Tool usage
- 각 도메인별 대표 작업

**성능:**
- 최고 모델: 19.5% 성공률
- 인간: 74.5% 성공률
- **Navi** 에이전트 도입

**기술적 특이점:** Azure 병렬 실행으로 20분 내 전체 벤치마크 완료 가능

---

### 3.2 학계/업계 표준 평가 프레임워크

#### **Anthropic의 대규모 다차원 평가 접근법 (2026)**

**철학:**
> "Static benchmarks are dead. Reliability, Tool-use, and Economic impact are the only way to value AI labor."

**평가 3대 축:**
1. **Reliability Metrics**
   - 일관성 점수 (Consistency Score)
   - 오류율 (Error Rate)
   - 실패 복구율 (Failure Recovery Rate)

2. **Tool-use Metrics**
   - 올바른 도구 선택율
   - 도구 사용 효율성
   - 도구 조합 복잡도 관리

3. **Economic Metrics**
   - 토큰당 가치 (Value per Token)
   - 작업당 비용
   - ROI (Return on Investment)

**평가 종류:**
- **Capability Evals**: 새로운 능력 측정 (낮은 Pass rate로 시작)
- **Regression Evals**: 기존 기능 유지 (높은 Pass rate 유지)

---

#### **Amazon의 멀티 에이전트 실무 평가법**
1. **Planning Score**: 작업 할당 정확도
2. **Communication Score**: 효율적인 메시지 수
3. **Collaboration Success Rate**: 에이전트별 성공률

**특징:** 실제 프로덕션 환경에서 검증됨

---

### 3.3 Google의 체계적 접근법

**3단계 평가 구조:**
```
1. Interaction Correctness
   - 각 상호작용 단계의 정확성
   
2. Task Completion Rate
   - 전체 작업 완료 여부
   
3. Conversation Quality
   - Groundedness (근거 기반)
   - Coherence (논리적 일관성)
   - Relevance (관련성)
```

---

## 4️⃣ 주요 논문 & 리소스

### 4.1 필독 논문들

#### **1. "MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents"**
- **저자**: Kunlun Zhu, Hongyi Du 등 (2025.03)
- **주요 기여**: Milestone-based KPI 도입
- **코드**: 공개 (GitHub)

#### **2. "REALM-Bench: A Benchmark for Evaluating Multi-Agent Systems on Real-world, Dynamic Planning and Scheduling Tasks"**
- **저자**: genglongling (2025.02)
- **주요 기여**: 6가지 평가 메트릭, 11가지 실제 시나리오
- **구현**: LangGraph, AutoGen, CrewAI 지원

#### **3. "MAEBE: Multi-Agent Emergent Behavior Evaluation Framework"**
- **발표**: 2025.07
- **주요 기여**: Emergent behavior/risk 체계적 평가
- **포커스**: Safety, Functional behaviors

#### **4. "Demystifying evals for AI agents" (Anthropic, 2026)**
- **대규모 실무 가이드**
- **내용**: Grader 설계, Eval 구조, 예제 (코딩, 대화, 연구, 컴퓨터 사용 에이전트)
- **핵심**: Eval-driven development 철학

#### **5. "AgentBench: Evaluating LLMs as Agents" (ICLR'24)**
- **8가지 환경에서의 에이전트 평가**
- **29개 LLM 벤치마킹**
- **다차원 평가 프레임워크** 도입

#### **6. "Windows Agent Arena: Evaluating Multi-modal OS Agents at Scale"**
- **멀티모달 에이전트의 실제 환경 테스트**
- **대규모 병렬 실행**

#### **7. "AEMA: Adaptive Evaluation Framework for Agentic LLM Systems" (2026.01)**
- **Verifiable evaluation** 강조
- **Multi-agent evaluator** 방식
- **투명한 감시 & 책임성**

#### **8. "MLA-Trust: Benchmarking Trustworthiness of Multimodal LLM Agents in GUI Environments"**
- **에이전트 신뢰성 평가**
- **Multi-step execution과 동적 환경 상호작용**

#### **9. "TRiSM for Agentic AI: Trust, Risk, and Security Management in LLM-based Agentic Multi-Agent Systems"**
- **종합적 신뢰/위험 관리 프레임워크**
- **System-level dynamics 이해**

#### **10. "Which Agent Causes Task Failures and When?" (OpenReview, 2025)**
- **에이전트 실패 원인 자동 추적**
- **Who&When 데이터셋** (127개 에이전트, 상세 실패 기록)
- **오류 귀인 방법** (Step-by-Step, Binary Search)

---

### 4.2 오픈소스 벤치마크 & 데이터셋

| 벤치마크 | 특징 | 평가 방식 |
|---------|------|---------|
| **SWE-Bench** | GitHub 이슈 기반 | Unit tests |
| **HumanEval** | 164개 코딩 문제 | 함수 정확성 |
| **Terminal-Bench 2.0** | 엔드-투-엔드 기술 작업 | 환경 상태 검증 |
| **OSWorld** | 완전 OS 제어 | 파일시스템, 설정, DB 상태 |
| **WebArena** | 브라우저 기반 작업 | URL, 페이지 상태 검증 |
| **τ-Bench / τ²-Bench** | 멀티턴 대화 | 사용자 페르소나 시뮬레이션 |
| **BrowseComp** | 웹 검색 및 종합 | Ground truth 검증 |

---

## 5️⃣ 평가 도구 & 프레임워크

### 5.1 대형 기업의 평가 방식

#### **Anthropic**
```
도구: Inspect Framework
특징:
  - 복잡한 다턴 평가
  - Transcript 추적
  - 여러 Grader 조합
  
최신: Bloom Framework (2025.12)
  - 자동화된 행동 평가
  - LiteLLM 통합 (Anthropic & OpenAI 모델)
  - Weights & Biases 연동
```

**Anthropic의 에이전트 평가 3단계:**
1. **Task-level eval**: 최종 결과물 검증
2. **Step-level eval**: 각 단계 검증
3. **Transcript eval**: 의사결정 과정 검증

#### **OpenAI**
```
접근: 프로덕션 중심 평가
  - A/B 테스팅으로 실제 효과 측정
  - 사용자 피드백 기반 보정
  - 비용 & 레이턴시 최적화

MCP (Model Context Protocol): 도구 표준화
  - OpenAI, Google, Anthropic, Microsoft 채택 (2025)
  - 에이전트 통합 평가 용이
```

#### **DeepMind**
```
접근: 학술 연구 중심
  - RL 기반 평가 환경 설계
  - Interpretability 강조
  - Safety-critical scenarios
```

#### **Amazon (AWS)**
```
실무 중심 평가:
  - Planning Score (작업 할당 정확도)
  - Communication Score (효율성)
  - Collaboration Success Rate
  
프레임워크: 실제 프로덕션 환경 기반
```

---

### 5.2 오픈소스 평가 도구 (2025년 기준)

#### **상위권 도구들**

| 도구 | 특징 | 장점 | 단점 |
|------|------|------|------|
| **Langfuse** | 자체 호스팅 가능 | 데이터 독립성, 오픈소스 | 셀프 호스팅 필요 |
| **Arize Phoenix** | OpenTelemetry 기반 | 벤더 독립적, 확장성 | 초기 설정 복잡 |
| **DeepEval** | 20M+ 평가 데이터 | 사전 구축된 메트릭, RAG/Agent 지원 | 커뮤니티 규모 작음 |
| **Braintrust** | 멀티턴 시뮬레이션 | 다양한 페르소나, Stress 테스트 | 엔터프라이즈 가격 |
| **LangSmith** | LangChain 통합 | 강력한 추적 기능 | 에코시스템 종속성 |
| **Comet Opik** | 프로덕션 모니터링 | 실시간 관찰 가능 | 제한된 오프라인 기능 |

#### **특수 목적 도구**

**Maxim AI**: 엔드-투-엔드 시뮬레이션 + 평가 + 관찰성
**Galileo**: 멀티모달 에이전트 평가 전문

---

### 5.3 프레임워크별 평가 지원도

```
평가 기능 매트릭스:

LangGraph
  ✅ 상태 추적 용이
  ✅ DAG 기반 시각화
  ✅ 단계별 평가 가능
  ⚠️ 비동기 협력 평가 제한

AutoGen
  ✅ 메시지 기반 추적 상세
  ✅ Human-in-the-loop 지원
  ✅ Custom termination 조건
  ⚠️ 비결정성 높음

CrewAI
  ✅ 역할 기반 평가 직관적
  ✅ Task completion 명확
  ⚠️ 고급 협력 패턴 표현 제한
```

---

## 6️⃣ 멀티 에이전트 협력 평가의 세부사항

### 6.1 Task Completion Rate (TCR)

**기본 정의:**
```
TCR = (성공한 작업 수) / (전체 작업 수) × 100%
```

**멀티 에이전트 확장:**
```
Hierarchical TCR:
  - Subtask Completion: 각 에이전트의 작업 완료율
  - End-to-End Completion: 전체 시스템 작업 완료율
  
가중치 모델:
  TCR_weighted = Σ(Weight_i × Completion_i) / Σ(Weight_i)
  
  예: 
    - A 에이전트 (중요도 0.5): 90% 완료
    - B 에이전트 (중요도 0.3): 80% 완료
    - C 에이전트 (중요도 0.2): 70% 완료
    = (0.5×0.9 + 0.3×0.8 + 0.2×0.7) = 0.83 (83%)
```

**고급 지표:**
- **Quality-Adjusted TCR**: 완료된 작업의 품질도 반영
- **Time-Adjusted TCR**: 완료 시간 제약 반영

---

### 6.2 Communication Efficiency

**핵심 메트릭:**
```
기본:
  Efficiency = Task_Success_Rate / (Message_Count × Average_Token_Count)

응답성:
  Response_Quality = Success_Rate / Message_Count
  
  예시:
    - 팀 A: 80% 성공, 50개 메시지 = 1.6
    - 팀 B: 75% 성공, 25개 메시지 = 3.0 ⭐
```

**통신 패턴 분석:**
```
1. Redundant Messages
   - 같은 정보 반복 전송율
   - 목표: <5%

2. Broken Communication Chain
   - 메시지 손실율
   - 목표: 0%

3. Message Clarity Score
   - LLM 평가: 메시지 명확도 (1-10)
   - 목표: >8

4. Bandwidth Efficiency
   - (작업 정보 비트) / (전송 토큰)
   - 높을수록 좋음
```

---

### 6.3 Robustness (견고성)

**정의:** 한 에이전트 실패 시 시스템 동작 유지도

#### **테스트 시나리오:**
```
1. Single Agent Failure
   - A 에이전트 무작위 실패 → 시스템 작동
   - 성공률 유지율: (전체 성공률 - A 실패 시) / 전체 성공률
   
   목표: >90% (9/10은 작동)

2. Cascading Failure Recovery
   - A 실패 → B의 재계획 능력 테스트
   - Recovery Time: 복구까지 소요 시간
   
   목표: <5 턴

3. Data Corruption Handling
   - 중간 데이터 손상 시뮬레이션
   - 검증 능력: 손상 감지율
   
   목표: >95% 감지

4. Communication Disruption
   - 메시지 지연/손실 시뮬레이션
   - Resilience Score: 기능 유지율
   
   목표: >80% 기능 유지
```

#### **견고성 점수 계산:**
```
Robustness_Score = Σ(Scenario_i × Weight_i)

예:
  - Single failure recovery (0.3): 92%
  - Cascading recovery (0.3): 88%
  - Data corruption detection (0.2): 96%
  - Communication disruption (0.2): 85%
  
  = 0.3×0.92 + 0.3×0.88 + 0.2×0.96 + 0.2×0.85
  = 0.276 + 0.264 + 0.192 + 0.17
  = 0.902 (90.2%)
```

---

### 6.4 Scalability (확장성)

**측정 차원:**

#### **1. 에이전트 수 확장**
```
Metric: Performance Degradation with Scale

Normal: 3 에이전트, 85% 성공
  + 5 에이전트: 84% (1% 저하) ✅
  + 10 에이전트: 80% (5% 저하) ✅
  + 20 에이전트: 70% (15% 저하) ❌ (선형 이상 저하)

목표: 에이전트 2배 증가 시 성능 <5% 저하
```

#### **2. 작업 복잡도 확장**
```
- 간단한 작업 (1-2 스텝): 90% 성공
- 중간 복잡도 (5-10 스텝): 80% 성공
- 복잡한 작업 (20+ 스텝): 60% 성공

목표: 복잡도 선형 증가 시 성능 로그-선형 저하
```

#### **3. 시스템 처리량 (Throughput)**
```
Metric: Tasks/Hour

Initial: 50 tasks/hour (3 agents)
Scaled: 300 tasks/hour (15 agents)

선형성 확인:
  이상적: 50 × (15/3) = 250
  실제: 300 (120% - 오버헤드 극소)
```

---

### 6.5 Trust & Verification (신뢰 & 검증)

#### **Trust Dimensions:**

**1. Explainability**
```
메트릭:
  - Decision Path Clarity: 에이전트 의사결정 과정 명확도
  - Reason Articulation: 이유 설명 품질
  - Attribution Score: 결정을 추적할 수 있는가?

평가 방식:
  - LLM Judge: "이 결정이 이해 가능한가?" (1-10)
  - Human Eval: SME (주제 전문가) 검증
```

**2. Consistency**
```
메트릭:
  - Same-Input Output Consistency: 같은 입력 반복 시
    목표: >99% 일관성
  
  - Value Stability: 관련 메트릭 변동률
    목표: σ < 2%

계산:
  Consistency_Score = 1 - (Variation / Average_Value)
```

**3. Auditability**
```
요구사항:
  ✅ 모든 결정의 완전한 기록
  ✅ 감사 추적 (Audit Trail)
  ✅ Timestamp 기반 재현성
  ✅ 인과관계 추적 가능
  
평가:
  - Can we reproduce the decision? Yes/No
  - Time to audit root cause
  - Completeness of evidence
```

---

## 7️⃣ 실제 사례 & 케이스 스터디

### 7.1 기업의 내부 평가 방식

#### **Claude Code (Anthropic)**
```
진화 과정:
  1단계 (초기): 수동 테스트, Dogfooding
           → 빠른 반복, 하지만 확장 불가
  
  2단계 (중기): 좁은 Evals 추가 (concision, file edits)
           → 특정 영역 개선 가능
  
  3단계 (현재): 복잡한 행동 Evals (over-engineering 방지)
           → 종합적 품질 통제

측정:
  - 코드 정확성 (Unit tests)
  - 사용자 경험 (LLM rubric)
  - 비용 효율성 (Token usage)
  - 응답 시간 (Latency)
```

#### **Descript의 비디오 편집 에이전트**
```
평가 3대 축:
  1. Don't break things
     - 기존 콘텐츠 무결성
     - Metric: Corruption rate
  
  2. Do what I asked
     - 사용자 지시 따름
     - Metric: Instruction adherence
  
  3. Do it well
     - 편집 품질
     - Metric: Subjective quality (LLM judge)

진화:
  - Phase 1: 수동 채점
  - Phase 2: LLM Grader (Product team 기준)
  - Phase 3: 주기적 인간 보정 (drift 방지)
```

#### **Bolt.ai의 코드 생성 에이전트**
```
3개월만에 구축한 종합 Eval 시스템:

Graders:
  1. 정적 분석 (Lint, Type check)
  2. 브라우저 에이전트 테스트 (실제 실행)
  3. LLM 평가 (Instruction following 등)

커버리지:
  - HTML/CSS/JS 코드 생성
  - 브라우저 렌더링 검증
  - 사용자 요청 준수도
```

---

### 7.2 학계 연구 사례

#### **SWE-Bench 진화**
```
Timeline:
  2024년 초: 30% pass rate
  2024년 중: 50% pass rate (모델 개선)
  2024년 말: 70% pass rate
  2025년 초: 80%+ pass rate

포화 문제 인식:
  → Verified (더 엄격), Multilingual, Multimodal 추가
  → 더 어려운 문제들 수집
  → 새로운 평가 축 개발 (설계 품질, 유지보수성)
```

#### **τ² Benchmark**
```
발전:
  τ-Bench (단일 모델 평가)
    ↓
  τ²-Bench (멀티턴 상호작용 + 동적 환경)

특징:
  - 사용자 페르소나 시뮬레이션
  - 실제 도메인 시나리오 (항공사, 소매점)
  - 다차원 성공 기준

학습:
  - 단순 "완료" 여부가 아닌 프로세스 품질 평가
  - 턴수 제약 (사용자 인내도)
  - 톤/공감 같은 소프트 스킬도 중요
```

---

## 8️⃣ 2026년 트렌드 및 미래 평가 방식

### 8.1 주요 트렌드

#### **1. Static Benchmarks의 쇠퇴**
```
과거 (2024):
  "SWE-Bench에서 몇 %?"
  → 포화 상태 도달

현재 (2026):
  "Production 환경에서 ROI는?"
  "에러 복구 능력은?"
  "팀 협력 효율은?"
  → 동적, 종합 메트릭
```

**시사점:**
- Benchmark saturation 문제 해결 필요
- 새로운 어려운 작업 지속적 추가
- 환경 변화 & 재계획 능력 평가 강화

#### **2. Agentic Metrics의 등장**
```
Old: 정확도, 속도, 비용
New: 신뢰성, 도구 사용, 경제적 영향

신뢰성 (Reliability):
  - 일관성 (99%+)
  - 실패 복구 (회복력)
  - 감사 추적 (추적 가능)

도구 사용 (Tool-Use):
  - 올바른 도구 선택
  - 도구 조합 최적화
  - API 오류 처리

경제 영향 (Economic Impact):
  - 토큰 효율
  - 시간 절감
  - 자동화 가치
```

#### **3. Emergent Behavior 평가 표준화**
```
새로운 리스크:
  - Collusion: 여러 에이전트의 규칙 우회 협력
  - Deception: 사용자 속이기
  - Reward Hacking: 목표 왜곡

평가 방식:
  - Adversarial multi-agent setups
  - Specification deviation detection
  - Safety-critical scenario testing
```

#### **4. Real-World Scenario 중심 평가**
```
REALM-Bench, Windows Agent Arena 같은 벤치마크 급증

특징:
  - 실제 작업 기반 (GitHub issues, OS tasks)
  - 동적 환경
  - 리소스 제약
  - 시간 압박

평가 결과:
  - 연구용: 80%+ 성공률
  - 프로덕션: 19.5% (아직 멀음)
```

#### **5. Multi-Modal Agent 평가**
```
새로운 도메인:
  - Screenshot 기반 작업
  - GUI 이해 능력
  - 시각적 선택 정확도
  
표준화 도구:
  - Windows Agent Arena
  - OSWorld
  - WebArena (확장 중)
```

---

### 8.2 2026년 평가 프레임워크의 방향

#### **통합 평가 아키텍처**

```
┌─────────────────────────────────────────┐
│     Multi-Dimensional Evaluation        │
├─────────────────────────────────────────┤
│                                         │
│  ┌─ Task Completion (40%)             │
│  │   ├─ Primary outcome                │
│  │   ├─ Subtask success rate          │
│  │   └─ Quality metrics                │
│  │                                     │
│  ├─ Collaboration Quality (30%)       │
│  │   ├─ Communication efficiency       │
│  │   ├─ Coordination score            │
│  │   └─ Handoff accuracy              │
│  │                                     │
│  ├─ Robustness (20%)                  │
│  │   ├─ Failure recovery              │
│  │   ├─ Data integrity                │
│  │   └─ Edge case handling            │
│  │                                     │
│  └─ Economic Impact (10%)             │
│      ├─ Token efficiency              │
│      ├─ Time savings                  │
│      └─ Cost per task                 │
│                                         │
└─────────────────────────────────────────┘

Final Score = 0.4×TC + 0.3×CQ + 0.2×R + 0.1×EI
```

---

### 8.3 예상 개발 방향

#### **평가 도구의 진화**

```
2024: 스크립트 기반 평가
↓
2025: 프레임워크 기반 평가 (Langfuse, Arize)
↓
2026+: AI 자동 평가 (Self-improving evals)
   - Evals that generate evals
   - Adaptive difficulty
   - Real-time drift detection
```

#### **자동화 평가의 한계 인식**

```
2026 주요 인사이트:

❌ "자동화로 모든 평가 가능"
✅ "자동화 + 인간 전문가 조합 필수"

이유:
  - Subjective quality (글쓰기, UX)
  - Novel solutions (예상 밖의 창의적 해결)
  - Safety-critical domains (의료, 금융)
```

---

### 8.4 Anthropic의 미래 비전

**핵심 명제:**
> "Static benchmarks are dead. Economic primitives and reliability metrics are the future."

**2026년 이후 평가 방식:**

```
1. Economic Primitive Scores
   - O*NET tasks 기반 경제 가치 평가
   - 직무별 자동화 가치 계산
   - ROI 기반 비교

2. Reliability First
   - 일관성 > 최대 성능
   - 에러 복구 능력 강조
   - Production readiness 척도

3. Tool Integration
   - 도구 선택 정확도
   - 외부 시스템과의 상호작용
   - API 오류 처리 능력

4. Continuous Monitoring
   - 벤치마크 → 프로덕션 모니터링
   - Drift detection
   - Automated retraining triggers
```

---

## 9️⃣ 평가 설계 모범 사례

### 9.1 Evaluation-Driven Development

**프로세스:**
```
1️⃣ 요구사항 정의
   → Eval tasks로 문서화
   
2️⃣ 첫 Eval 작성
   → 아직 에이전트는 실패
   → 0% pass rate 정상
   
3️⃣ 기능 개발
   → Eval 개선에 초점
   
4️⃣ 지속적 모니터링
   → Regression evals (>95% pass rate)
   → Capability evals (<50% pass rate)
```

**실제 예시 (Anthropic):**
```
Claude Code 기능 추가 베팅:
  - 새로운 모델이 할 수 있을 것 같은 기능
  - Eval을 먼저 만듦 (0% pass)
  - 새 모델 릴리스 시 결과 확인
  → 일부 베팅 성공, 일부 실패

이 프로세스가 발견한 것:
  - Over-engineering 문제
  - 사용자 지시 미준수
  - 불필요한 복잡성
```

### 9.2 Eval 작성의 필수 요소

#### **1. 명확한 Task Specification**
```
❌ 나쁜 예:
"사용자 요청에 따라 코드를 짜시오"

✅ 좋은 예:
"사용자 요청: 'Fibonacci 함수 작성'
 출력: Python 함수 (타입 힌트 포함)
 검증: 10개의 테스트 케이스 통과"
```

#### **2. Reference Solution**
```
모든 Task마다 작동하는 예시 필요:
  - Eval이 실제로 평가 가능한가?
  - Grader가 올바르게 작동하는가?
  - 모호성이 없는가?
```

#### **3. Balanced Test Sets**
```
❌ 편향된 평가:
- 에이전트가 "검색만" 하도록 최적화

✅ 균형잡힌 평가:
- 검색해야 하는 경우: 50%
- 검색하면 안 되는 경우: 50%
```

#### **4. Multiple Grader Types**
```
코딩: Unit tests + 정적 분석 + LLM rubric
대화: 상태 검증 + LLM 품질 평가 + 턴수 제약
연구: Groundedness + Coverage + Source quality
```

---

## 🔟 결론: 2026년 AI 에이전트 평가의 현황

### 핵심 통찰

1. **벤치마크 포화 시대 진입**
   - SWE-Bench: 30% → 80% (1년)
   - 더 어려운 문제 필요

2. **멀티 에이전트 평가로의 패러다임 전환**
   - 단일 에이전트 eval은 과거
   - 협력, 통신, Emergent behavior 측정 필수

3. **생산 환경 중심 평가**
   - 정확도 ✓ → 신뢰성 ✓
   - 속도 ✓ → 경제성 ✓

4. **자동화의 한계 인식**
   - 100% 자동 평가는 불가능
   - 인간 전문가와 조합 필수

5. **표준화 진행 중**
   - MCP (Model Context Protocol) 채택
   - REALM-Bench, MultiAgentBench 활성화
   - Anthropic's agentic metrics 확산

### 실무 권장사항

**지금 시작해야 할 것:**
```
✅ 기존 단일 에이전트 evals 구축
   └─ 아직 충분하지만, 시간 낭비 금지

✅ 멀티 에이전트 평가 파일럿
   └─ REALM-Bench, MultiAgentBench 검토

✅ 프로덕션 모니터링 인프라
   └─ Drift detection, A/B testing 준비

✅ Eval 자동화 도구 선택
   └─ Langfuse, Arize, Braintrust 중 선택
```

**피해야 할 것:**
```
❌ 정확도만 보기
   → Reliability, Cost, Speed 함께 측정

❌ Static benchmark 신뢰만 하기
   → 프로덕션 모니터링 병행 필수

❌ 100% 자동 평가 기대
   → 인간 리뷰 + 샘플링 조합

❌ 에이전트 실패 = 평가 실패로 결론
   → Eval 자체 검증 먼저 (Anthropic의 교훈)
```

---

## 📚 참고 자료 링크

### 주요 벤치마크
- [SWE-Bench](https://www.swebench.com/)
- [HumanEval](https://github.com/openai/human-eval)
- [REALM-Bench GitHub](https://github.com/genglongling/REALM-Bench)
- [MultiAgentBench arXiv](https://arxiv.org/abs/2503.01935)
- [AgentBench](https://github.com/THUDM/AgentBench)

### 평가 도구
- [Langfuse](https://langfuse.com/) - OSS, 자체 호스팅
- [Arize Phoenix](https://arize.com/) - OpenTelemetry 기반
- [Braintrust](https://www.braintrust.dev/)
- [DeepEval](https://github.com/confident-ai/deepeval)

### 프레임워크
- [Harbor Framework](https://harborframework.com/)
- [LangGraph](https://www.langchain.com/langgraph)
- [AutoGen](https://microsoft.github.io/autogen/)
- [CrewAI](https://www.crewai.com/)

### 주요 논문 (arXiv)
- MAEBE: [2506.03053](https://arxiv.org/abs/2506.03053)
- Responsible Emergent Multi-Agent Behavior: [2311.01609](https://arxiv.org/abs/2311.01609)
- Emergent Tool Use: [1909.07528](https://arxiv.org/abs/1909.07528)
- Windows Agent Arena: OpenReview
- Which Agent Causes Failures: [2505.00212](https://arxiv.org/abs/2505.00212)

### 기업 블로그/문서
- [Anthropic - Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents)
- [AWS - Evaluating AI agents](https://aws.amazon.com/blogs/machine-learning/)
- [Google Cloud - Methodical approach to agent evaluation](https://cloud.google.com/blog/)
- [Alignment.anthropic.com - BLOOM](https://alignment.anthropic.com/2025/bloom-auto-evals/)

---

**보고서 작성 일자:** 2026년 3월 26일  
**데이터 기준:** 2025년 말 ~ 2026년 3월 최신 논문 & 도구 기준

