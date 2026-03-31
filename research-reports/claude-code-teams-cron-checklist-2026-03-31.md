# Claude Code 신기능 구현 체크리스트

**실제 프로젝트에 적용할 때 단계별로 확인하는 리스트**

---

## Phase 1: 준비 (사전 설정)

### 환경 설정

- [ ] Claude Code 버전 확인
  ```bash
  claude --version
  # v2.1.32 이상 필요 (Agent Teams)
  # v2.1.72 이상 필요 (Scheduled Tasks)
  ```

- [ ] Claude Code 업그레이드 (필요시)
  ```bash
  # Homebrew 사용자
  brew upgrade claude-code
  
  # 기타
  npm install -g @anthropic-ai/claude-code@latest
  ```

### Agent Teams 활성화 (선택사항)

- [ ] 환경 변수 설정
  ```bash
  export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
  ```

- [ ] 또는 settings.json 수정
  ```json
  {
    "env": {
      "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
    }
  }
  ```

- [ ] 활성화 확인
  ```bash
  claude
  # 프롬프트: "에이전트 팀을 만들어줄래"
  # 응답이 있으면 활성화됨
  ```

### 권한 설정 최적화

- [ ] `~/.claude.json` 생성/수정
  ```json
  {
    "permission_mode": "ask",
    "pre_approved_operations": [
      "file_write",
      "file_read",
      "git_diff",
      "git_status",
      "git_log",
      "test_execution"
    ]
  }
  ```

- [ ] 팀 구성 전 권한 테스트
  ```bash
  claude
  # 파일 쓰기 테스트
  # 권한 요청 빈도 확인
  ```

### 터미널 설정 (선택: Split-pane mode)

- [ ] tmux 설치 (macOS)
  ```bash
  brew install tmux
  tmux -V  # 버전 확인
  ```

- [ ] 또는 iTerm2 설정
  - [ ] iTerm2 → Settings → General → Magic → "Enable Python API" 체크
  - [ ] `it2` CLI 설치
    ```bash
    brew install mkusaka/it2/it2
    ```

---

## Phase 2: Agent Teams 설정

### 팀 구성 계획

- [ ] 작업 분석
  - [ ] 전체 목표 정의
  - [ ] 독립적 단위로 분해 (작업 크기 확인)
  - [ ] 의존성 맵핑

- [ ] 팀원 역할 정의
  - [ ] 역할명 확정 (예: 보안 리뷰어)
  - [ ] 각 역할의 책임 범위 명확화
  - [ ] 모델 선택 (Opus/Sonnet/Haiku)

- [ ] 팀 규모 결정
  ```
  작업 복잡도 vs 팀 규모:
  - 간단: 2명
  - 중간: 3-4명 ← 추천
  - 복잡: 5-6명
  - 매우 복잡: 6-10명 (조정 오버헤드 주의)
  ```

### 파일 충돌 방지 계획

- [ ] 작업별 담당 파일 지정
  ```
  팀원 A: src/auth/tokens.js
  팀원 B: src/auth/session.js
  팀원 C: src/auth/validators.js
  
  ❌ 금지: 모두 src/auth/handler.js 수정
  ```

- [ ] Git 전략 검토
  - [ ] 브랜치 전략 (각 팀원별 브랜치?)
  - [ ] Merge 전략 (충돌 해결 방법)
  - [ ] 커밋 메시지 규칙

### 컨텍스트 준비

- [ ] CLAUDE.md 작성/검토
  ```markdown
  # 프로젝트 가이드
  
  ## 팀 구성
  - 팀원 1: 보안 리뷰어
  - 팀원 2: 성능 분석가
  - 팀원 3: 테스트 커버리지 체커
  
  ## 주요 파일 구조
  src/
  ├─ auth/
  ├─ api/
  └─ db/
  
  ## 리뷰 기준
  - 보안: JWT, CSRF, SQLi 검사
  - 성능: DB 쿼리, 캐싱, N+1
  - 테스트: 엣지 케이스, 통합 시나리오
  ```

- [ ] 테스트 케이스 준비 (필요시)
- [ ] 참고 자료 링크 정리

### 팀 생성 스크립트 준비 (선택)

- [ ] 반복 가능한 팀 구성용 프롬프트 작성
  ```text
  "에이전트 팀을 생성해줄래.
  
  역할:
  1. 보안 리뷰어 - src/auth/ 검사, 토큰/CSRF/입력검증
  2. 성능 분석가 - DB 쿼리, N+1, 캐싱 전략
  3. 테스트 체커 - 엣지 케이스, 통합 테스트
  
  모델: Sonnet (각 팀원)
  
  작업:
  - [보안] 토큰 처리 감사 (1시간)
  - [성능] DB 쿼리 프로파일링 (2시간)
  - [테스트] 엣지 케이스 발굴 (1.5시간)
  
  작업 완료 후 각 팀원의 리포트를 summary.md에 통합해줄래."
  ```

---

## Phase 3: Scheduled Tasks 설정

### 필요성 분석

- [ ] 자동화할 작업 목록
  ```
  [ ] 배포 상태 폴링
  [ ] PR 감시
  [ ] 빌드 모니터링
  [ ] 정기 리포트
  [ ] 기타: ____________
  ```

- [ ] 각 작업별 요구사항
  | 작업 | 빈도 | 스케줄링 모드 | 로컬 파일 | 24/7 |
  |------|------|------------|---------|------|
  | 배포 감시 | 5분 | Session | ❌ | ❌ |
  | 일일 테스트 | 23:59 | Desktop | ✅ | ❌ |
  | 보고서 생성 | 1시간 | Cloud | ❌ | ✅ |

### Cron 표현식 검증

- [ ] 각 스케줄의 Cron 표현식 작성
  ```bash
  # 배포 감시 (5분마다)
  */5 * * * *
  
  # 일일 테스트 (매일 23:59)
  59 23 * * *
  
  # 평일 아침 리포트 (월-금 9:00)
  0 9 * * 1-5
  ```

- [ ] Cron 타임존 확인
  ```bash
  date  # 로컬 타임존 확인
  # 서울: Asia/Seoul (UTC+9)
  # 샌프란시스코: America/Los_Angeles (UTC-8)
  ```

- [ ] Jitter 고려
  ```
  ❌ 피하기 (Jitter ±90초):
  0 9 * * *    # 9:00 정각
  0 15 * * *   # 3:00 PM 정각
  
  ✅ 사용하기 (Jitter 없음):
  7 9 * * *    # 9:07
  13 15 * * *  # 3:13 PM
  ```

### Session Task 설정 (임시 폴링)

- [ ] `/loop` 명령 준비
  ```text
  /loop 5m 배포 상태 확인하고 완료되면 알려줄래
  ```

- [ ] 일회 알림 준비
  ```text
  in 2 hours, 릴리스 브랜치 푸시 상기시켜줄래
  ```

### Desktop Task 설정 (로컬 파일 접근)

- [ ] 스크립트 작성 (배포 확인 예)
  ```bash
  #!/bin/bash
  # scripts/check-deployment.sh
  
  status=$(curl -s https://api.example.com/status | jq .status)
  
  if [ "$status" = "complete" ]; then
    echo "✅ 배포 완료"
    exit 0
  elif [ "$status" = "failed" ]; then
    echo "❌ 배포 실패"
    exit 1
  else
    echo "⏳ 진행 중: $status"
    exit 0
  fi
  ```

- [ ] 스크립트 테스트
  ```bash
  chmod +x scripts/check-deployment.sh
  ./scripts/check-deployment.sh
  # 정상 동작 확인
  ```

### Cloud Task 설정 (24/7 자동화)

- [ ] Claude 웹 인터페이스 접속
- [ ] Tasks 탭 → Create Task
- [ ] 최소 간격: 1시간 준수
- [ ] Connectors 설정 (필요시)

---

## Phase 4: 모니터링 및 최적화

### Agent Teams 모니터링

- [ ] 팀 상태 확인
  ```bash
  # 팀원들 순회
  Shift+Down  # 다음 팀원
  Shift+Up    # 이전 팀원
  
  # 작업 목록 표시
  Ctrl+T
  ```

- [ ] 토큰 사용량 추적
  ```bash
  # 설치 (한번)
  npm install -g @anthropic-ai/ccusage
  
  # 사용량 확인
  ccusage
  ```

- [ ] 팀원 효율성 점검
  - [ ] 각 팀원의 진행률
  - [ ] 유휴 시간 확인
  - [ ] 타이밍 조정 필요성 평가

- [ ] 비용 분석
  ```
  예상 비용 계산:
  - 팀원 수: 3명
  - 예상 시간: 3시간
  - 기준: 3명 × 3시간 × 기본 요금
  = 예상 토큰 × 요금
  ```

### Scheduled Tasks 모니터링

- [ ] 작업 실행 확인
  ```bash
  # 세션 작업 목록
  사용자: "스케줄된 작업이 뭐가 있어?"
  
  # 실행 로그 확인
  사용자: "최근 배포 확인 작업 결과 보여줄래"
  ```

- [ ] 실패 패턴 감지
  - [ ] 연속 3회 실패 = 문제 신호
  - [ ] 에러 로그 정리
  - [ ] 실패 원인 분석

- [ ] 3일 만료 관리 (Session Tasks)
  - [ ] 중요 작업 만료 일정 추적
  - [ ] 만료 1일 전 재생성

### 비용 최적화 검토

- [ ] 비용 대비 효과 분석
  ```
  Agent Teams 비용:
  - 토큰 사용: 140만 → $0.21
  - 시간 절감: 2.5시간 (인건비 $100+?)
  - ROI: 긍정적 ✅
  ```

- [ ] 비용 절감 기회
  - [ ] 팀 규모 축소 가능?
  - [ ] 간격 조정 (5분 → 10분)?
  - [ ] 모델 다운그레이드 (Sonnet → Haiku)?

---

## Phase 5: 프로덕션화

### 문서화

- [ ] 팀/작업 설명서 작성
  ```markdown
  # 병렬 코드 리뷰 팀
  
  ## 목적
  PR #142 보안/성능/테스트 커버리지 3각도 검토
  
  ## 팀 구성
  - 팀원 1: 보안 리뷰어 (Claude Sonnet)
  - 팀원 2: 성능 분석가 (Claude Sonnet)
  - 팀원 3: 테스트 체커 (Claude Sonnet)
  
  ## 작업 목록
  1. 토큰 처리 감사 (1시간)
  2. DB 쿼리 최적화 (2시간)
  3. 엣지 케이스 발굴 (1.5시간)
  
  ## 예상 결과
  3가지 관점의 종합 리포트 (30분 내)
  
  ## 비용
  약 $0.25 (토큰 140만)
  ```

- [ ] Scheduled Task 설명
  ```markdown
  # 배포 상태 폴링
  
  ## 목적
  배포 진행 상황 실시간 모니터링
  
  ## 스케줄
  5분마다 (*/5 * * * *)
  
  ## 실행 위치
  현재 세션
  
  ## 동작
  1. 배포 API 호출
  2. 상태 확인
  3. 진행률 표시
  4. 완료 시 알림
  
  ## 최대 실행
  3일 후 자동 만료
  ```

### 에러 처리 계획

- [ ] Agent Teams 에러 대응
  - [ ] 팀원 종료 → 대체 팀원 스폰
  - [ ] 작업 상태 지연 → 수동 업데이트
  - [ ] 파일 충돌 → 충돌 해결 후 병합

- [ ] Task 에러 대응
  - [ ] 연속 실패 → 작업 취소 + 원인 파악
  - [ ] API 에러 → 재시도 정책 검토
  - [ ] 권한 에러 → 권한 설정 수정

### 운영 가이드 작성

- [ ] 문제 해결 가이드
  ```markdown
  ## 팀원이 보이지 않는 경우
  1. Shift+Down으로 순환 (배경에서 실행 중일 수 있음)
  2. 터미널 모드 확인 (in-process vs split-pane)
  3. 필요시 새 팀원 스폰
  
  ## 작업이 진행되지 않는 경우
  1. 의존성 확인 (선행 작업 완료 여부)
  2. 팀원에게 직접 메시지 (상태 재확인)
  3. 작업 상태 수동 업데이트
  ```

---

## Phase 6: 지속적 개선

### 성능 측정

- [ ] 주간 메트릭 수집
  ```
  [ ] 토큰 사용량 vs 계획
  [ ] 시간 단축 효과
  [ ] 품질 개선 정도 (버그 감소)
  [ ] 비용 대비 효과 (ROI)
  ```

- [ ] 팀 효율성 평가
  - [ ] 각 팀원의 생산성
  - [ ] 조정 오버헤드
  - [ ] 팀 규모 적정성

### 프로세스 개선

- [ ] 작업 분할 재검토
  ```
  현재: 10 to-do per teammate → 최적인가?
  개선: 5-6 to-do per teammate로 조정?
  ```

- [ ] 팀원 역할 재정의
  ```
  추가 필요 역할?
  불필요한 역할?
  역할 간 겹침?
  ```

- [ ] 의존성 재분석
  ```
  현재 의존성 구조가 병렬화 방해?
  독립적 작업으로 재구성 가능?
  ```

### 비용 최적화 (지속)

- [ ] 월간 비용 리뷰
  ```
  | 항목 | 예상 | 실제 | 편차 |
  |------|------|------|------|
  | AT1 | $0.2 | $0.23 | +15% |
  | AT2 | $0.3 | $0.28 | -7% |
  | Task | $0.1 | $0.12 | +20% |
  ```

- [ ] 최적화 기회 탐색
  - [ ] 모델 크기 조정 (Opus → Sonnet?)
  - [ ] 빈도 조정 (5분 → 10분?)
  - [ ] Batch 작업으로 통합?

---

## 체크리스트 완료 가이드

### 첫 팀 생성 (예상 시간: 1시간)

1. ✅ Phase 1: 준비 (10분)
   - 버전 확인
   - Agent Teams 활성화

2. ✅ Phase 2: 팀 설정 (30분)
   - 팀 구성 계획
   - 파일 충돌 방지

3. ✅ Phase 3: Tasks (10분)
   - 선택사항 (필요시)

4. ✅ Phase 4-6: 스킵 (첫 팀에서는 선택)

### 프로덕션 운영 (예상 시간: 2-3주)

- 1주차: Phase 1-5 완료
- 2주차: Phase 4 (모니터링) 진행
- 3주차: Phase 6 (개선) 시작

---

## 문제 해결 퀵 링크

| 문제 | 해결책 | 더보기 |
|------|--------|--------|
| 팀원이 안 보임 | Shift+Down 순환 | 보고서 Troubleshooting |
| 비용 폭증 | 팀 규모 축소 | 보고서 성능 섹션 |
| 작업 상태 지연 | 수동 업데이트 | 보고서 한계 섹션 |
| 파일 충돌 | 파일 경계 명확화 | 보고서 3.5절 |
| 권한 요청 과다 | Pre-approve 설정 | 보고서 1.8절 |

---

**버전:** v1.0  
**마지막 업데이트:** 2026-03-31  
**상세 정보:** `claude-code-features-report.md` 참조

