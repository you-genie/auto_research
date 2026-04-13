# Meta HyperAgents 개념 데모

Meta FAIR의 HyperAgents(arXiv:2603.19461, ICLR 2026)의 핵심 개념을 Python으로 시뮬레이션하는 데모입니다.

## 실행 환경

- Python 3.9+
- 외부 API 키 불필요 (Mock 모드로 실행)
- rich 라이브러리 권장 (없어도 실행 가능)

## 설치 및 실행

```bash
# 의존성 설치
pip install -r requirements.txt

# 데모 실행
python hyperagent_demo.py
```

## 데모 구조

```
demo/
├── hyperagent_demo.py   # 메인 데모 스크립트
├── requirements.txt     # 의존성 목록
└── README.md            # 이 파일
```

## 핵심 개념 설명

### TaskAgent (태스크 에이전트)
실제 문제를 풀어요. `AgentConfig` 설정에 따라 다른 방식으로 문제를 해결합니다.

### MetaAgent (메타 에이전트)
태스크 에이전트의 설정을 개선해요. HyperAgents의 혁신 포인트는 이 메타 에이전트 자체도 수정 가능하다는 것입니다.

### 자기 개선 루프
```
태스크 실행 → 성능 평가 → 메타 분석 → 설정 개선 → 반복
```

메타 전략이 `basic` → `advanced` → `self_referential`로 자동 진화합니다.

## 실제 HyperAgents와의 차이

| 항목 | 이 데모 | 실제 HyperAgents |
|------|---------|-----------------|
| LLM 사용 | Mock(규칙 기반) | GPT-4/Claude/Gemini |
| 코드 수정 | 설정 파라미터만 | 실제 Python 소스코드 |
| 실행 환경 | 로컬 Python | Docker 샌드박스 |
| 비용 | 무료 | ~8,800만 토큰/실행 |
| 도메인 | 시뮬레이션 | 코딩/논문/로보틱스/수학 |

## 샘플 출력

```
============================================================
  Meta HyperAgents 자기 개선 데모 시작
============================================================

============================================================
  반복 1/5 — 도메인: 코딩 태스크
============================================================

현재 설정: CoT=False, Memory=False, MetaStrategy=basic, Temp=0.7
  태스크: 'Python으로 피보나치 수열을...' → 점수: 0.371
  태스크: '주어진 논문의 실험 방법론을...' → 점수: 0.384
  태스크: '로봇 팔의 보상 함수를...' → 점수: 0.352
평균 점수: 0.369

  [메타 에이전트] 분석 중... (전략: basic)
적용된 개선사항: {'use_chain_of_thought': True}
메타 인사이트: 성능 부족 감지 → Chain-of-Thought 추론 활성화

...

성능 향상: 0.369 → 0.721 (+95.4%)
영구 메모리 (자율 개발된 기능): 3개 태스크 인사이트 저장됨
```

## 참고 자료

- [HyperAgents 논문](https://arxiv.org/abs/2603.19461)
- [GitHub 리포](https://github.com/facebookresearch/Hyperagents)
- [Meta AI 공식 페이지](https://ai.meta.com/research/publications/hyperagents/)
