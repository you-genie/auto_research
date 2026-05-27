# SkillOpt: AI 에이전트가 자기 스스로 스킬을 훈련한다고?

> "Agent skills today are hand-crafted, generated one-shot, or evolved through loosely controlled self-revision, none of which behaves like a deep-learning optimizer for the skill, and none of which reliably improves over its starting point under feedback." — SkillOpt, arXiv:2605.23904

솔직히 말하면, 요즘 AI 에이전트 연구에서 "스킬"이라는 단어가 참 많이 나오는데요. Voyager가 Minecraft에서 스킬 라이브러리를 쌓고, Trace2Skill이 실행 궤적에서 교훈을 증류하고, EvoSkill이 폴더 단위로 스킬을 진화시키고... 근데 뭔가 하나씩 다 아쉬운 느낌이 들죠. "그래서 이게 진짜 optimizer처럼 체계적으로 학습되는 건가?" 하는 의문이요.

[SkillOpt](https://arxiv.org/abs/2605.23904)(arXiv:2605.23904, 2026년 5월 22일 제출)는 바로 그 질문에서 출발해요. Microsoft + 상하이교통대/동제대/복단대 공동 연구팀이 제안한 이 프레임워크는, 에이전트 스킬을 진짜 딥러닝처럼 — epoch, batch size, learning rate, validation gate까지 갖춰서 — 훈련하자는 아이디어거든요. 모델 가중치는 건드리지 않고, 오직 자연어 스킬 문서 하나를 최적화 대상으로 삼아서요.

---

## 논문 기본 정보

| 항목 | 내용 |
|------|------|
| 제목 | SkillOpt: Executive Strategy for Self-Evolving Agent Skills |
| arXiv | [2605.23904](https://arxiv.org/abs/2605.23904) |
| 프로젝트 페이지 | [microsoft.github.io/SkillOpt](https://microsoft.github.io/SkillOpt/) |
| GitHub | [microsoft/SkillOpt](https://github.com/microsoft/SkillOpt) |
| 제출일 | 2026년 5월 22일 (v2: 5월 25일) |
| 저자 | Yifan Yang, Ziyang Gong, Weiquan Huang, Qihao Yang, Ziwei Zhou, Zisu Huang, Yan Li, Xuemei Gao, Qi Dai, Bei Liu, Kai Qiu, Yuqing Yang, Dongdong Chen, Xue Yang, Chong Luo |
| 소속 | Microsoft, 상하이교통대학교(SJTU), 동제대학교, 복단대학교 |

---

## 왜 이 문제를 풀어야 하나?

기존 에이전트 스킬 접근 방식들을 크게 세 가지로 분류해볼 수 있어요.

**1. 수작업 스킬 (Hand-crafted)**
전문가가 직접 작성하는 방식이에요. 품질은 좋지만 비용이 비싸고, 새로운 도메인에 확장하기 어렵죠.

**2. 원샷 생성 (One-shot LLM)**
LLM에게 "이 태스크를 위한 스킬 문서 써줘" 하고 한 번 요청하는 방식이에요. 빠르지만 피드백 루프가 없으니 성능이 들쭉날쭉해요.

**3. 느슨한 자기 수정 (Loosely controlled self-revision)**
Voyager, EvoSkill처럼 실행 결과를 보고 스킬을 업데이트하는 방식이에요. 근데 "얼마나 고칠지", "나빠지면 어떻게 할지"에 대한 제어가 약해서 불안정할 수 있어요.

> "We argue the skill should instead be trained as the external state of a frozen agent, with the same discipline that makes weight-space optimization reproducible." — SkillOpt 논문

저자들의 핵심 주장은: **스킬을 "동결된 에이전트의 외부 상태"로 보고, 가중치 공간 최적화가 재현 가능하게 만드는 것과 똑같은 규율로 훈련하자**는 거예요.

---

## SkillOpt가 뭘 최적화하는 건가요?

한 줄로 요약하면: **frozen LLM 에이전트를 위한 자연어 스킬 문서를 text-space에서 최적화하는 시스템**이에요.

스킬 문서란 뭐냐면, 에이전트가 태스크를 수행할 때 context로 주어지는 마크다운 형식의 지시서예요. "어떤 순서로 생각해라", "어떤 도구를 어떻게 써라", "출력 형식은 이렇게 해라" 같은 내용을 담고 있죠.

형식적으로는 다음과 같이 정의해요:

```
frozen target model M, harness h, task x, skill s에 대해:
  (τ(s), r(s)) = h(M, x, s),   r(s) ∈ [0,1]

최적화 목표:
  s*_sel = argmax_{s ∈ C(D_tr)} (1/|D_sel|) Σ_{x ∈ D_sel} r(s)
```

training split으로 후보 스킬을 만들고, validation split으로 선택하고, test split으로 최종 평가하는 3-split 구조예요. 딥러닝 학습 파이프라인이랑 완전히 같은 구조죠.

---

## Executive Strategy: 메타-수준 의사결정 구조

"Executive Strategy"라는 이름이 왜 붙었을까요? 저자들은 SkillOpt를 단순한 프롬프트 수정 도구가 아니라, **스킬 훈련 전 과정을 통제하는 상위 레벨 의사결정 구조**로 설계했기 때문이에요.

이 전략의 핵심은 두 모델의 역할 분리예요:

- **Target Model (M)**: 실제 태스크를 수행하는 frozen 에이전트 (GPT-5.5, Qwen, Claude 등 어떤 모델이든)
- **Optimizer Model (O)**: 스킬 문서를 분석하고 수정안을 제안하는 별도 LLM (보통 frontier 모델)

Optimizer는 배포될 때 쓰이지 않아요. 훈련 시에만 동작하고, 최적화된 `best_skill.md` 파일만 배포하면 되는 거예요. 추론 시 추가 LLM 호출이 0회인 거죠.

### 알고리즘 흐름 (Algorithm 1)

```
입력: Model M, Optimizer O, Harness h, splits, 초기 스킬 s₀
출력: Best validation-gated 스킬 s_best, test score

s_cur ← s₀, s_best ← s₀, 거절 버퍼 B ← []

for epoch e = 1 to E:
  훈련 데이터를 rollout 배치로 셔플; B ← [] 리셋
  
  for each 최적화 스텝:
    1. [Rollout] A개 rollout 배치 실행 → 궤적 수집
    2. 실패/성공 미니배치로 분할
    3. [Reflect-Failure] O가 실패 패턴 분석 → 수정 제안
    4. [Reflect-Success] O가 성공 패턴 분석 → 보존 제안
    5. [Merge] 실패 우선 병합 → 최종 edit 리스트
    6. [Rank] Top L_t 개 edit 선택
    7. [Apply] 후보 스킬 s̃ 생성
    8. [Gate] D_sel에서 평가
    
    if score(s̃) > score(s_cur):
      s_cur ← s̃, s_best 갱신
    else:
      B에 거절 패턴 추가
  
  [Slow Update] 에포크 경계에서 종단적 가이던스 생성 → protected section
  [Meta Skill] 미래 에포크를 위한 optimizer 메모리 갱신
```

---

## 6가지 핵심 메커니즘

### 1. Bounded Text Updates (텍스트 학습률)

딥러닝에서 learning rate가 너무 크면 학습이 발산하듯, 스킬 문서도 한 번에 너무 많이 바꾸면 망가져요. SkillOpt는 **edit 예산 L_t**를 도입해서 한 스텝에 적용 가능한 최대 수정 횟수를 제한해요.

스케줄도 딥러닝과 똑같아요: constant, linear decay, cosine decay. 실험에서는 L=1~16 범위에서 모두 경쟁력 있고, 제어 없이 자유롭게 수정하면 성능이 2.5~3.0포인트 떨어진다는 걸 보여줘요.

edit 연산 종류는 4가지예요: `append`, `insert_after`, `replace`, `delete`.

### 2. Validation Gate (검증 게이트)

모든 후보 스킬은 held-out validation split에서 평가받고, **strictly improving**할 때만 채택돼요. 동점도 거절이에요. 실제로 제안된 edit의 95% 이상이 거절된다고 해요. 덕분에 최종 스킬에 들어간 accepted edit은 벤치마크별로 고작 1~4개에 불과하죠.

### 3. Rejected-Edit Buffer (거절 edit 버퍼)

거절된 edit들은 그냥 버리지 않고 버퍼에 저장돼요. 다음 최적화 스텝에서 optimizer에게 "이런 건 이미 시도해봤는데 안 됐어"라는 음성 피드백으로 전달되죠. 이걸 ablation하면 1.6~4.6포인트 성능 하락이 나타나요.

### 4. Epoch-Wise Slow Update (에포크 경계 느린 업데이트)

에포크가 끝날 때, 이전 에포크 vs 현재 에포크 스킬로 같은 태스크를 다시 실행해서 비교해요. 개선, 퇴행, 지속적 실패, 안정적 성공 패턴을 분석하고 **protected section**에 종단적 가이던스를 작성해요.

이 protected section은 step-level edit으로는 건드릴 수 없어요. 에포크 경계에서만 수정 가능하죠. SpreadsheetBench에서 Slow/Meta Update를 ablation하면 무려 **22.5포인트 하락**이 나타나요 (77.5 → 55.0). 가장 큰 ablation 효과예요.

### 5. Meta Skill (Optimizer 측 메모리)

Optimizer 모델이 자체적으로 유지하는 메모리예요. "어떤 edit 전략이 효과적이었는지", "어떤 패턴이 반복적으로 실패했는지"를 요약해서 미래 에포크의 optimizer 프롬프트에 prepend해요. 이 meta skill은 배포 artifact에는 포함되지 않아요. 순전히 훈련 시 optimizer의 학습을 위한 것이에요.

### 6. Harness-Agnostic 설계

같은 SkillOpt 루프가 direct chat, Codex 에이전트 루프, Claude Code 에이전트 루프 세 가지 harness에서 모두 동작해요. harness별 adapter가 rollout 실행 인터페이스를 통일시켜줘서, optimizer 로직은 harness에 무관하게 작동하죠.

---

## 실험: 6개 벤치마크, 7개 모델, 3개 Harness

### 벤치마크 구성

| 벤치마크 | 도메인 | 특징 |
|---------|--------|------|
| SearchQA | 웹 검색 QA | 검색 전략, 엔티티 추출 |
| SpreadsheetBench | 엑셀/스프레드시트 | 수식 평가, 셀 범위 처리 |
| OfficeQA | 오피스 문서 이해 | 테이블/날짜/단위 파싱 |
| DocVQA | 문서 시각 QA | 테이블, 폼, 차트 정렬 |
| LiveMathematicianBench | 수학 추론 | 정리 강도 비교, MCQ |
| ALFWorld | 실내 탐색 에이전트 | 목표 지향 탐색, 상태 관리 |

### 메인 결과 (GPT-5.5, Direct Chat)

| 벤치마크 | 스킬 없음 | SkillOpt | 향상 |
|---------|----------|----------|------|
| SearchQA | 77.7 | 87.3 | +9.6 |
| SpreadsheetBench | 41.8 | 80.7 | **+38.9** |
| OfficeQA | 33.1 | 72.1 | **+39.0** |
| DocVQA | 78.8 | 91.2 | +12.4 |
| LiveMathematicianBench | 37.6 | 66.9 | +29.3 |
| ALFWorld | 83.6 | 95.5 | +11.9 |
| **평균** | **58.8** | **82.3** | **+23.5** |

6개 벤치마크 × 7개 모델 × 3개 harness = 52개 evaluation cell 모두에서 best 또는 tied-best예요. Oracle(셀별 최선 baseline 선택)보다도 +5.4포인트 앞서고요.

### Harness별 평균 향상 (GPT-5.5)

| Harness | 평균 향상 |
|---------|---------|
| Direct Chat | +23.5 |
| Codex 에이전트 루프 | +24.8 |
| Claude Code | +19.1 |

### 비교 대상 Baseline

| Baseline | 설명 |
|---------|------|
| No Skill | frozen baseline |
| Human Skill | 전문가 작성 (145~516 토큰) |
| One-shot LLM Skill | GPT-5.5 단일 생성 |
| Trace2Skill | 궤적 증류 (arXiv:2603.25158) |
| TextGrad | gradient 스타일 프롬프트 최적화 |
| GEPA | Pareto reflective 프롬프트 진화 |
| EvoSkill | harness-side 스킬 폴더 진화 |

---

## 학습된 스킬은 어떻게 생겼나요?

최종 스킬 문서는 379~1,995 토큰 (중앙값 약 920)이고, committed edit은 겨우 1~4개예요. 몇 가지 예시를 볼게요:

**SearchQA에서 학습된 규칙:**
> "Infer the expected answer type from clue wording, then choose the shortest canonical entity supported by co-occurring distinctive evidence."

**SpreadsheetBench:**
> "Inspect workbook structure and formulas, then write evaluated static values across the full requested target range instead of relying on Excel recalculation."

**ALFWorld:**
> "Keep a horizon-aware visited/frontier ledger, diversify search after repeated same-type failures, and avoid revisiting the destination until holding the target."

솔직히 보면 이게 다 "아, 맞다 이게 당연하지" 싶은 내용들이에요. 근데 이걸 인간이 쓰지 않고 에이전트 실행 결과에서 자동으로 추출해냈다는 게 포인트죠.

---

## 전이 실험: 스킬이 진짜로 이식 가능한가?

### 모델 간 전이 (Cross-Model Transfer)

| 소스 스킬 | 타겟 모델 | 향상 |
|---------|---------|------|
| GPT-5.4 SpreadsheetBench | GPT-5.4-mini | +9.4 |
| GPT-5.4 SpreadsheetBench | GPT-5.4-nano | +3.0 |

### Harness 간 전이 (Cross-Harness Transfer)

이게 진짜 놀라운 결과예요:

| 소스 Harness | 타겟 Harness | 향상 |
|------------|------------|------|
| Codex → Claude Code | SpreadsheetBench | +59.7 (22.1 → 81.8) |
| Claude Code → Codex | SpreadsheetBench | +43.6 (27.5 → 71.1) |

Codex에서 학습한 스킬이 Claude Code에서 **in-domain SkillOpt 참조 결과(80.4)를 초과**했어요. 이건 스킬 문서가 harness-specific 구현 세부사항보다는 더 추상적인 절차적 지식을 인코딩한다는 걸 시사해요.

### 벤치마크 간 전이 (Cross-Benchmark Transfer)

| 소스 벤치마크 | 타겟 벤치마크 | 향상 |
|------------|------------|------|
| OlympiadBench | Omni-MATH (GPT-5.4) | +3.7 |

---

## Ablation 요약

| 제거 구성 요소 | SpreadsheetBench 하락 | SearchQA 하락 |
|-------------|---------------------|-------------|
| Slow/Meta Update 모두 제거 | **-22.5** (최대) | - |
| Rejected-Edit Buffer 제거 | -1.6 ~ -4.6 | -1.6 ~ -4.6 |
| Bounded LR (무제한 수정) | -2.5 ~ -3.0 | -2.5 ~ -3.0 |

---

## 한계점

SkillOpt가 좋긴 한데 솔직히 아쉬운 점도 있어요:

**1. 자동 검증자 필요**
scored feedback이 있어야 해요. 주관적 평가가 필요한 도메인(글쓰기 스타일, 창의적 작업)에는 바로 적용하기 어려워요.

**2. 훈련 비용**
배포 아티팩트는 가볍지만, 스킬 훈련 자체에는 rollout 실행 + optimizer 호출이 꽤 들어요.

**3. 단일 스킬 설계**
이질적인 서브태스크가 많은 도메인에서는 단일 스킬 문서로 커버하기 어려울 수 있어요.

**4. 분포 이동 시 주의**
학습 도메인 특화 휴리스틱이 인코딩되기 때문에, 큰 분포 이동이 있는 전이 전에는 검증이 필요해요.

---

## 에이전트 스킬 진화 연구 계보 안에서의 위치

SkillOpt가 어떤 계보에 있는지 정리해볼게요:

| 연구 | 핵심 접근 | SkillOpt와의 차이 |
|------|---------|----------------|
| [Voyager](https://arxiv.org/abs/2305.16291) (2023) | Minecraft 실체화 에이전트의 code 스킬 라이브러리 자동 확장 | 특정 환경 종속적; 스킬이 code function 단위; 검증 게이트 없음 |
| [ADAS](https://arxiv.org/abs/2408.08435) (2024) | 에이전트 설계 자체를 code로 최적화 | 에이전트 아키텍처 최적화; 스킬 문서가 아닌 code 레벨 |
| [TextGrad](https://arxiv.org/abs/2406.07496) | LLM 피드백으로 텍스트 gradient 계산 후 프롬프트 업데이트 | 검증 게이트 없음; 지속 스킬 아티팩트 없음 |
| [GEPA](https://github.com/gepa-ai/gepa) | Pareto reflective 프롬프트 진화, 적은 평가로 효율적 | bounded edit 예산 없음; rejected-edit 메모리 없음 |
| [Trace2Skill](https://arxiv.org/abs/2603.25158) (2026) | 궤적 풀을 병렬 분석해 스킬 디렉토리 구축 | 반복적 검증 게이트 없음; 단발성 증류 |
| [EvoSkill](https://arxiv.org/pdf/2603.02766) | 실패 분석으로 스킬 폴더 진화 | textual learning rate 없음; cross-epoch slow update 없음 |
| **SkillOpt** (2026) | 딥러닝 훈련 규율을 text-space에 적용 | **epoch/batch/LR/validation gate/negative feedback 모두 갖춤** |

SkillOpt의 핵심 차별점은 **"스킬 학습을 훈련 프로세스로 격상"**시켰다는 거예요. 기존 연구들이 스킬을 "어떻게 만들까"에 집중했다면, SkillOpt는 "어떻게 체계적으로 훈련할까"에 집중했죠.

Claude Code skills 관점에서 보면, SkillOpt로 최적화된 스킬이 Claude Code harness에서 +19.1포인트 향상을 보이고, Codex 스킬이 Claude Code로 전이되어 in-domain 결과를 초과한다는 건 실용적 함의가 꽤 커요.

---

## 시사점: 뭐가 진짜 중요한가?

**1. "Skill as trainable state" 패러다임**

이게 가장 중요한 개념 전환이에요. 스킬을 그냥 static resource로 보지 않고, frozen agent의 trainable external state로 보는 거죠. 이렇게 보면 prompt optimization, tool learning, skill library 관리가 모두 같은 최적화 문제의 다른 측면이 돼요.

**2. 배포 비용 = 0**

훈련 시 optimizer가 필요하지만, 배포 시에는 `best_skill.md` 하나만 있으면 돼요. 추론 오버헤드가 없죠. 이건 실용 배포 관점에서 매우 중요해요.

**3. 52/52 across-the-board**

6개 벤치마크, 7개 모델, 3개 harness에서 모두 best/tied-best라는 건 robustness 측면에서 인상적이에요. 특정 도메인에서만 잘 되는 게 아니라는 거죠.

**4. 향후 방향**

저자들이 제안하는 흥미로운 후속 연구 방향은:
- 여러 도메인에 걸친 스킬 라이브러리 (인프라 공유)
- Optimizer-side meta skill의 벤치마크 간 재사용
- 보상 없는 validation gate (오픈엔드 태스크)
- 최적화된 스킬 → 모델 가중치 self-distillation

---

## 마치며

SkillOpt는 "에이전트 스킬 최적화"라는 문제를 처음으로 딥러닝 훈련 프레임워크와 완전히 동형(isomorphic)으로 정의한 연구예요. epoch, minibatch, learning rate, validation gate, momentum, negative feedback... 이 모든 개념이 text-space에서 작동하도록 매핑되었어요.

가중치 공간이 아닌 텍스트 공간에서의 "학습"이라는 아이디어가 얼마나 멀리 갈 수 있을지, 앞으로의 연구가 기대되네요.

---

## 참고문헌

| 번호 | 제목 | URL |
|------|------|-----|
| 1 | SkillOpt: Executive Strategy for Self-Evolving Agent Skills (arXiv:2605.23904) | https://arxiv.org/abs/2605.23904 |
| 2 | SkillOpt 프로젝트 페이지 | https://microsoft.github.io/SkillOpt/ |
| 3 | SkillOpt GitHub | https://github.com/microsoft/SkillOpt |
| 4 | HuggingFace Paper Page | https://huggingface.co/papers/2605.23904 |
| 5 | Voyager: An Open-Ended Embodied Agent with Large Language Models | https://arxiv.org/abs/2305.16291 |
| 6 | Automated Design of Agentic Systems (ADAS) | https://arxiv.org/abs/2408.08435 |
| 7 | Trace2Skill: Distill Trajectory-Local Lessons into Transferable Agent Skills | https://arxiv.org/abs/2603.25158 |
| 8 | EvoSkill: Automated Skill Discovery for Multi-Agent Systems | https://arxiv.org/pdf/2603.02766 |
| 9 | GEPA GitHub | https://github.com/gepa-ai/gepa |
| 10 | SkillOpt alphaXiv | https://www.alphaxiv.org/abs/2605.23904 |
