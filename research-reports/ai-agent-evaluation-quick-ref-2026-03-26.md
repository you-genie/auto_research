# AI 에이전트 평가 방식 - 빠른 참고 가이드

## 🎯 한 페이지 요약

### 평가 방식 진화
```
2024: 단일 에이전트 벤치마크 (SWE-Bench 40%, HumanEval)
      ↓
2025: 멀티 에이전트 벤치마크 급증 (REALM-Bench, MultiAgentBench)
      ↓
2026: Agentic metrics 표준화 (신뢰성, 도구 사용, 경제적 영향)
```

---

## 📊 주요 벤치마크 비교

| 벤치마크 | 대상 | 평가 방식 | 최신 Pass Rate |
|---------|------|---------|---------------|
| **SWE-Bench** | 코딩 에이전트 | Unit tests | >80% |
| **HumanEval** | 코드 생성 | 함수 정확성 | ~70-80% |
| **MultiAgentBench** | 멀티에이전트 | Milestone-based KPI | 신규 |
| **REALM-Bench** | 계획/스케줄링 | 6가지 메트릭 | 신규 |
| **Windows Agent Arena** | OS 에이전트 | 환경 상태 검증 | 19.5% |
| **τ²-Bench** | 대화 에이전트 | 사용자 시뮬레이션 | - |

---

## 🔧 평가 도구 선택 가이드

### 자체 호스팅 원할 때
✅ **Langfuse** - 오픈소스, 완전 제어

### 빠른 시작 원할 때
✅ **DeepEval** - 사전 구축 메트릭 (20M+ 데이터)

### 멀티턴 시뮬레이션 원할 때
✅ **Braintrust** - 페르소나 기반 Stress 테스트

### 프로덕션 모니터링 원할 때
✅ **Arize Phoenix** - OpenTelemetry 기반, 벤더 독립적

### LangChain 생태계 원할 때
✅ **LangSmith** - 강력한 추적 & 평가

---

## 🏗️ 프레임워크별 평가 적합성

| 프레임워크 | 평가 강점 | 평가 약점 |
|-----------|---------|---------|
| **LangGraph** | DAG 시각화, 단계별 추적 | 비동기 협력 평가 어려움 |
| **AutoGen** | 메시지 기반 상세 추적, Human-in-loop | 비결정성 높음 |
| **CrewAI** | 역할 기반 평가 직관적 | 고급 협력 표현 제한 |

---

## 📈 멀티 에이전트 평가 핵심 메트릭

### 1️⃣ Task Completion Rate (40% 가중치)
```
= (성공한 작업 수) / (전체 작업 수)
목표: >85% (프로덕션 수준: 80%+)
```

### 2️⃣ Communication Efficiency (30% 가중치)
```
= Task Success Rate / (Message Count × Avg Tokens)
목표: 최소화된 메시지로 높은 완료율
벤치마크: 80% 성공 / 25 메시지 = 3.2
```

### 3️⃣ Robustness (20% 가중치)
```
한 에이전트 실패 시 시스템 작동 유지율
목표: >90% (9/10 시나리오 작동)
```

### 4️⃣ Economic Impact (10% 가중치)
```
= (자동화 가치) / (토큰 + 시간)
목표: ROI > 1.5x
```

---

## 🚀 최신 트렌드 (2026)

1. **Static Benchmark 포화**
   - SWE-Bench: 30% → 80% (1년만에)
   - 해결: 더 어려운 문제, 동적 환경

2. **Emergent Behavior 평가**
   - MAEBE Framework 표준화
   - Collusion, Deception, Reward Hacking 테스트

3. **Real-World 중심**
   - REALM-Bench (공급망, 재난 대응)
   - Windows Agent Arena (150+ 실제 작업)

4. **멀티모달 평가**
   - 스크린샷 기반 작업
   - GUI 이해 능력

---

## ✅ Eval 작성 체크리스트

- [ ] **명확한 작업 명세** (모호하지 않음)
- [ ] **Reference Solution** (작동하는 예시)
- [ ] **Balanced Test Set** (긍정/부정 케이스 혼합)
- [ ] **Multiple Grader Types** (코드 + LLM + 인간)
- [ ] **Transcript Review** (실제 결과 검증)
- [ ] **Edge Cases** (경계 조건 포함)
- [ ] **Regression Tests** (기존 기능 유지 확인)

---

## 🎓 학습 순서

**1단계 (1주):** SWE-Bench, HumanEval 이해
**2단계 (2주):** Anthropic 평가 가이드 읽기
**3단계 (3주):** MultiAgentBench, REALM-Bench 논문 읽기
**4단계 (4주):** 도구 선택 & 파일럿 프로젝트

---

## 🔗 빠른 링크

```
📖 필독 논문:
  • Anthropic - "Demystifying evals for AI agents"
  • MultiAgentBench (arXiv:2503.01935)
  • REALM-Bench (arXiv:2502.18836)
  • MAEBE Framework (arXiv:2506.03053)

🛠️ 도구 공식 문서:
  • Langfuse: langfuse.com
  • Arize Phoenix: arize.com
  • Braintrust: braintrust.dev
  • DeepEval: github.com/confident-ai/deepeval

📊 벤치마크:
  • SWE-Bench: swebench.com
  • REALM-Bench GitHub: genglongling/REALM-Bench
  • MultiAgentBench GitHub: 공개
  • AgentBench: github.com/THUDM/AgentBench
```

---

## 💡 실무 팁

### ❌ 하지 말 것
- 정확도만 보기 (신뢰성, 비용도 중요)
- 벤치마크 점수만 믿기 (프로덕션 모니터링 필수)
- 100% 자동 평가 기대 (인간 리뷰 필수)

### ✅ 해야 할 것
- Eval-driven development (기능 추가 전에 eval 작성)
- Transcript 읽기 (통계만으로는 부족)
- Regression eval 유지 (>95% pass rate)
- 정기적 보정 (LLM grader 검증)

---

**마지막 업데이트:** 2026년 3월 26일  
**다음 검토 예정:** 2026년 6월 (Q2 새로운 벤치마크)

