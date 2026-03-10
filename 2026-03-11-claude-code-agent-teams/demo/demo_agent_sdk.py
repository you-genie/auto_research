"""
Claude Agent SDK 데모: 멀티에이전트 패턴 시뮬레이션

이 데모는 Claude Agent SDK의 주요 패턴을 보여줍니다:
1. 단일 에이전트 기본 사용
2. 서브에이전트를 활용한 병렬 코드 리뷰
3. 에이전트 팀 패턴 시뮬레이션 (실제 환경에서 실행 가능)

주의: 실제 실행 시 ANTHROPIC_API_KEY 환경 변수 필요
"""

import asyncio
import os
import json
from typing import AsyncIterator

# ────────────────────────────────────────────────────────────────
# 섹션 1: 환경 설정 확인
# ────────────────────────────────────────────────────────────────

def check_environment() -> bool:
    """API 키 및 SDK 설치 여부를 확인합니다."""
    # API 키 확인
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("⚠️  ANTHROPIC_API_KEY 환경 변수가 설정되지 않았습니다.")
        print("    export ANTHROPIC_API_KEY=your-api-key")
        return False

    # SDK 설치 확인
    try:
        import claude_agent_sdk  # noqa: F401
        print("✅ claude_agent_sdk 설치 확인")
    except ImportError:
        print("⚠️  claude_agent_sdk가 설치되지 않았습니다.")
        print("    pip install claude-agent-sdk")
        return False

    return True


# ────────────────────────────────────────────────────────────────
# 섹션 2: 단일 에이전트 패턴 (기본)
# ────────────────────────────────────────────────────────────────

async def demo_single_agent(prompt: str) -> str:
    """
    단일 에이전트로 간단한 작업을 수행합니다.

    에이전트 루프:
    1. 맥락 수집 (Read, Glob, Grep으로 코드베이스 탐색)
    2. 행동 수행 (파일 읽기, 분석)
    3. 작업 검증 (결과 반환)
    """
    from claude_agent_sdk import query, ClaudeAgentOptions

    print(f"\n{'='*60}")
    print("패턴 1: 단일 에이전트")
    print(f"{'='*60}")
    print(f"프롬프트: {prompt[:100]}...")

    result_text = ""

    # ClaudeAgentOptions로 허용 도구와 권한 모드 설정
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Bash"],
        permission_mode="acceptEdits",  # 파일 편집 자동 수락
    )

    async for message in query(prompt=prompt, options=options):
        # 결과 메시지 추출
        if hasattr(message, "result"):
            result_text = message.result
            print(f"\n✅ 에이전트 결과:\n{result_text[:500]}")
        elif hasattr(message, "type") and message.type == "assistant":
            # 에이전트 진행 상황 출력
            if hasattr(message, "message"):
                for block in message.message.content:
                    if hasattr(block, "text") and block.text:
                        print(f"  🤖 {block.text[:100]}")

    return result_text


# ────────────────────────────────────────────────────────────────
# 섹션 3: 서브에이전트 패턴 (병렬 코드 리뷰)
# ────────────────────────────────────────────────────────────────

async def demo_subagent_code_review(target_dir: str = ".") -> dict:
    """
    서브에이전트를 활용한 병렬 코드 리뷰 패턴.

    세 가지 전문 서브에이전트가 동시에 다른 관점으로 코드를 검토합니다:
    - 보안 리뷰어: 취약점 탐지
    - 성능 분석가: 최적화 기회 발견
    - 코드 품질 검사기: 가독성·유지보수성 평가
    """
    from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

    print(f"\n{'='*60}")
    print("패턴 2: 서브에이전트 병렬 코드 리뷰")
    print(f"{'='*60}")

    # 세 가지 전문 서브에이전트 정의
    agents = {
        "security-reviewer": AgentDefinition(
            description="보안 취약점 탐지 전문가. 코드 변경 후 즉시 사용할 것.",
            prompt="""당신은 보안 전문가입니다. 다음을 검토하세요:

            ## 검토 항목
            - SQL 인젝션, XSS, CSRF 취약점
            - 하드코딩된 시크릿/API 키
            - 불안전한 직렬화/역직렬화
            - 입력 유효성 검사 부재
            - 인증·인가 결함

            결과를 JSON 형식으로 반환하세요:
            {"issues": [{"severity": "high/medium/low", "location": "파일:라인", "description": "설명", "fix": "수정 방법"}]}
            """,
            tools=["Read", "Glob", "Grep"],  # 읽기 전용 (수정 없음)
        ),
        "performance-analyzer": AgentDefinition(
            description="성능 분석 전문가. 병목 및 최적화 기회 탐지.",
            prompt="""당신은 성능 최적화 전문가입니다. 다음을 분석하세요:

            ## 분석 항목
            - N+1 쿼리 패턴
            - 불필요한 루프 내 DB 호출
            - 메모리 누수 패턴
            - 캐시 미활용 영역
            - 동기 블로킹 I/O

            결과를 JSON 형식으로 반환하세요:
            {"issues": [{"impact": "high/medium/low", "location": "파일:함수명", "description": "설명", "optimization": "최적화 방법"}]}
            """,
            tools=["Read", "Glob", "Grep"],
        ),
        "quality-checker": AgentDefinition(
            description="코드 품질 검사기. 가독성·유지보수성·테스트 커버리지 평가.",
            prompt="""당신은 코드 품질 전문가입니다. 다음을 평가하세요:

            ## 평가 항목
            - 함수/변수 명명 규칙
            - 복잡도 (너무 긴 함수, 깊은 중첩)
            - 중복 코드 (DRY 원칙 위반)
            - 주석 부재 또는 과도한 주석
            - 테스트 커버리지 부족

            결과를 JSON 형식으로 반환하세요:
            {"score": 0-100, "issues": [{"type": "naming/complexity/duplication/docs/tests", "location": "파일:함수명", "description": "설명"}]}
            """,
            tools=["Read", "Glob", "Grep"],
        ),
    }

    # 메인 에이전트 옵션 설정
    # - allowed_tools에 "Agent" 포함 → 서브에이전트 사용 허용
    options = ClaudeAgentOptions(
        allowed_tools=["Read", "Glob", "Grep", "Agent"],
        agents=agents,
        permission_mode="dontAsk",  # 자동 처리
    )

    # 메인 에이전트가 서브에이전트들에게 작업 위임
    prompt = f"""
    {target_dir} 디렉토리의 Python 파일들을 세 전문 에이전트로 병렬 검토해주세요:

    1. security-reviewer: 보안 취약점 탐지
    2. performance-analyzer: 성능 이슈 분석
    3. quality-checker: 코드 품질 평가

    각 에이전트를 동시에 실행하고 결과를 종합해서 우선순위 순으로 개선사항을 정리해주세요.
    """

    review_results = {}

    async for message in query(prompt=prompt, options=options):
        if hasattr(message, "result"):
            print(f"\n✅ 종합 리뷰 결과:\n{message.result[:800]}")
            review_results["summary"] = message.result

    return review_results


# ────────────────────────────────────────────────────────────────
# 섹션 4: 에이전트 팀 패턴 (CLI 레벨) 시뮬레이션
# ────────────────────────────────────────────────────────────────

def demo_agent_team_prompts() -> None:
    """
    Claude Code CLI에서 에이전트 팀을 활용하는 프롬프트 패턴을 보여줍니다.

    실제 에이전트 팀은 Claude Code CLI에서 사용하며, 이 함수는
    실전에서 사용할 수 있는 프롬프트 템플릿을 출력합니다.
    """
    print(f"\n{'='*60}")
    print("패턴 3: 에이전트 팀 CLI 프롬프트 템플릿")
    print(f"{'='*60}")

    templates = {
        "병렬 코드 리뷰": {
            "활성화": 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1',
            "프롬프트": """Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings to me.""",
            "적합한 경우": "하나의 PR을 여러 관점에서 동시 검토할 때",
            "예상 비용": "단일 세션 대비 약 3~4배 토큰",
        },
        "경쟁 가설 디버깅": {
            "활성화": 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1',
            "프롬프트": """Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses:
1. WebSocket connection management
2. Session timeout settings
3. Memory leak in message handler
4. Race condition in async code
5. Load balancer configuration
Have them talk to each other to try to disprove each other's theories.
Update the findings.md with whatever consensus emerges.""",
            "적합한 경우": "원인 불명의 버그를 여러 방향으로 동시 조사할 때",
            "예상 비용": "단일 세션 대비 약 5~6배 토큰",
        },
        "크로스 레이어 기능 개발": {
            "활성화": 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1',
            "프롬프트": """I need to add a real-time notification system.
Create an agent team with three teammates:
- Backend teammate: implement notification service at src/services/notification.ts,
  REST API at src/api/notifications.ts
- Frontend teammate: build notification UI at src/components/NotificationPanel.tsx,
  state management at src/store/notifications.ts
- Test teammate: write unit tests in tests/notification.test.ts,
  integration tests in tests/integration/
Each teammate should own their domain completely without touching other files.""",
            "적합한 경우": "프론트·백엔드·테스트를 동시에 개발할 때 (파일 충돌 없음)",
            "예상 비용": "단일 세션 대비 약 3배 토큰 + 시간 1/3",
        },
        "아키텍처 탐색": {
            "활성화": 'export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1',
            "프롬프트": """I'm designing a CLI tool for tracking TODO comments.
Create an agent team with 3 different perspectives:
- UX teammate: focus on user workflow and command design
- Architecture teammate: focus on technical implementation and data storage
- Devil's advocate teammate: challenge assumptions and find edge cases
Have them discuss and share findings with each other.
Synthesize their insights into a design recommendation.""",
            "적합한 경우": "설계 결정 시 다양한 관점을 동시에 탐색할 때",
            "예상 비용": "단일 세션 대비 약 3배",
        },
    }

    for name, t in templates.items():
        print(f"\n{'─'*50}")
        print(f"📌 {name}")
        print(f"{'─'*50}")
        print(f"활성화: {t['활성화']}")
        print(f"\n프롬프트 예시:")
        print(f'"""\n{t["프롬프트"]}\n"""')
        print(f"\n✅ 적합한 경우: {t['적합한 경우']}")
        print(f"💰 예상 비용: {t['예상 비용']}")


# ────────────────────────────────────────────────────────────────
# 섹션 5: 서브에이전트 파일 생성기
# ────────────────────────────────────────────────────────────────

def generate_subagent_files(output_dir: str = ".claude/agents") -> None:
    """
    실전에서 바로 사용할 수 있는 서브에이전트 파일들을 생성합니다.

    생성되는 서브에이전트:
    - code-reviewer.md: 코드 품질 검토
    - security-auditor.md: 보안 감사
    - test-writer.md: 테스트 코드 작성
    - debugger.md: 버그 진단 및 수정
    """
    import pathlib

    output_path = pathlib.Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    agents = {
        "code-reviewer.md": """---
name: code-reviewer
description: >
  코드 품질과 보안을 검토하는 전문 리뷰어.
  코드 변경 후 즉시 사용할 것.
  커밋 전 자동으로 실행.
tools: Read, Glob, Grep, Bash
model: sonnet
memory: project
---

당신은 시니어 코드 리뷰어입니다.

## 실행 절차
1. `git diff HEAD~1` 또는 `git diff --staged`로 변경 내용 확인
2. 변경된 파일에 집중
3. 즉시 리뷰 시작

## 검토 체크리스트
- 코드 가독성 및 명명 규칙 준수
- 중복 코드 (DRY 원칙)
- 에러 처리 적절성
- API 키·비밀번호 하드코딩 여부
- 입력 유효성 검사
- 테스트 커버리지
- 성능 최적화 가능성

## 결과 형식
**심각 문제** (반드시 수정):
- [파일:라인] 문제 설명 + 수정 예시

**경고** (수정 권장):
- [파일:라인] 문제 설명

**제안** (선택적 개선):
- [파일:라인] 개선 아이디어
""",

        "security-auditor.md": """---
name: security-auditor
description: >
  보안 취약점을 탐지하는 전문 감사자.
  보안 관련 코드 변경 시 반드시 사용.
  인증·인가·입력 처리 코드에 적극 활용.
tools: Read, Glob, Grep
model: opus
permissionMode: plan
---

당신은 애플리케이션 보안 전문가입니다. OWASP Top 10 기준으로 검토합니다.

## 검토 우선순위

### 즉시 차단 (Critical)
- SQL 인젝션 취약점
- 하드코딩된 API 키·비밀번호·토큰
- 인증 우회 가능성
- 원격 코드 실행 (RCE) 벡터

### 높은 위험 (High)
- XSS (Cross-Site Scripting)
- CSRF 토큰 부재
- 불안전한 직접 객체 참조
- 민감 데이터 평문 저장

### 중간 위험 (Medium)
- 입력 유효성 검사 부재
- 과도한 권한 설정
- 에러 메시지에 스택 트레이스 노출
- 세션 관리 문제

## 보고 형식
각 취약점에 대해:
- **위험도**: Critical / High / Medium / Low
- **위치**: 파일경로:라인번호
- **설명**: 취약점 내용
- **공격 시나리오**: 실제 악용 방법
- **수정 방법**: 구체적 코드 예시
""",

        "test-writer.md": """---
name: test-writer
description: >
  유닛 테스트와 통합 테스트를 작성하는 전문가.
  새 기능 구현 후 사용. 테스트 커버리지 개선 시 사용.
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
memory: project
isolation: worktree
---

당신은 테스트 주도 개발(TDD) 전문가입니다.

## 테스트 작성 원칙

### 구조 (AAA 패턴)
```python
def test_기능_상황_예상결과():
    # Arrange: 테스트 데이터 준비
    # Act: 테스트 대상 실행
    # Assert: 결과 검증
```

### 커버리지 목표
- 해피 패스 (정상 흐름)
- 경계값 (빈 값, 최대값, 최소값)
- 에러 케이스 (잘못된 입력, 예외 상황)
- 동시성 이슈 (해당하는 경우)

## 실행 절차
1. 대상 코드 분석 (Read/Grep으로 기존 테스트 패턴 파악)
2. 테스트 케이스 설계
3. 테스트 파일 작성
4. `python -m pytest -v` 실행으로 통과 확인
5. 커버리지 리포트 생성: `pytest --cov=. --cov-report=term-missing`

## 메모리 업데이트
각 작업 후 `.claude/agent-memory/test-writer/MEMORY.md`에 기록:
- 프로젝트 테스트 프레임워크와 패턴
- 재사용 가능한 픽스처
- 발견한 테스트 공백 영역
""",

        "debugger.md": """---
name: debugger
description: >
  버그 진단과 수정 전문가. 에러 발생 시 즉시 사용.
  테스트 실패, 예상치 못한 동작, 성능 저하 시 활용.
tools: Read, Edit, Bash, Grep, Glob
model: sonnet
---

당신은 근본 원인 분석(RCA) 전문가입니다.

## 디버깅 프로세스
1. **에러 수집**: 에러 메시지와 스택 트레이스 전체 캡처
2. **재현 조건**: 재현 단계와 환경 파악
3. **격리**: 실패 위치 정확히 특정
4. **최소 픽스**: 증상이 아닌 근본 원인 수정
5. **검증**: 수정 후 테스트 실행으로 확인

## 각 버그 보고서
- **근본 원인**: 왜 이 버그가 발생했는가
- **증거**: 진단을 뒷받침하는 근거
- **코드 수정**: 구체적인 변경 내용
- **테스트**: 버그를 포착하는 테스트 케이스
- **예방법**: 향후 유사 버그 방지 방법

## 디버깅 기법
- `git log --oneline -20`: 최근 변경 이력 확인
- `git bisect`: 버그 도입 커밋 이진 탐색
- 전략적 로그 추가로 변수 상태 추적
- 단위 테스트로 가설 검증
""",
    }

    print(f"\n{'='*60}")
    print("패턴 4: 서브에이전트 파일 생성")
    print(f"{'='*60}")

    for filename, content in agents.items():
        filepath = output_path / filename
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"✅ {filepath} 생성 완료")

    print(f"\n📁 {len(agents)}개 서브에이전트 파일이 {output_dir}에 생성됐습니다.")
    print("💡 Claude Code를 실행하면 자동으로 로드됩니다.")
    print("💡 '/agents' 명령으로 서브에이전트 목록을 확인하세요.")


# ────────────────────────────────────────────────────────────────
# 메인 실행
# ────────────────────────────────────────────────────────────────

def print_banner() -> None:
    """데모 시작 배너를 출력합니다."""
    print("\n" + "="*60)
    print("  Claude Code 에이전트 팀 데모")
    print("  Agent Teams in Claude Code - Demonstration")
    print("="*60)
    print("\n이 데모는 다음 패턴을 보여줍니다:")
    print("  1. 단일 에이전트 기본 사용 (SDK)")
    print("  2. 서브에이전트 병렬 코드 리뷰 (SDK)")
    print("  3. 에이전트 팀 CLI 프롬프트 템플릿")
    print("  4. 서브에이전트 파일 자동 생성")
    print()


def print_architecture_diagram() -> None:
    """멀티에이전트 아키텍처 다이어그램을 출력합니다."""
    print("\n" + "="*60)
    print("에이전트 팀 아키텍처")
    print("="*60)
    diagram = """
    ┌─────────────────────────────────────────────────────┐
    │                   에이전트 팀                        │
    │                                                     │
    │  ┌─────────────┐      ┌──────────────────────────┐ │
    │  │  팀 리드    │◄────►│    공유 태스크 목록       │ │
    │  │ (메인 세션) │      │  pending / in-progress / │ │
    │  └──────┬──────┘      │  completed               │ │
    │         │ spawn       └──────────────────────────┘ │
    │    ┌────▼──────────────────────────┐               │
    │    │         팀원들                │               │
    │    │                               │               │
    │    │  [팀원 A] ←──메시지──► [팀원 B] │               │
    │    │      ↕                   ↕    │               │
    │    │  [팀원 C] ←──메시지──► [팀원 D] │               │
    │    └───────────────────────────────┘               │
    │                                                     │
    │  저장 위치:                                          │
    │  - ~/.claude/teams/{name}/config.json               │
    │  - ~/.claude/tasks/{name}/                          │
    └─────────────────────────────────────────────────────┘

    vs 서브에이전트:

    메인 에이전트 → 서브A → 결과 반환
                 → 서브B → 결과 반환  (팀원 간 소통 없음)
                 → 서브C → 결과 반환
    """
    print(diagram)


if __name__ == "__main__":
    print_banner()
    print_architecture_diagram()

    # 환경 확인
    has_api = check_environment()

    # 패턴 3: 에이전트 팀 CLI 프롬프트 (항상 실행 가능)
    demo_agent_team_prompts()

    # 패턴 4: 서브에이전트 파일 생성 (항상 실행 가능)
    generate_subagent_files("./demo_agents")

    if has_api:
        # SDK가 설치되고 API 키가 있을 때만 실제 에이전트 실행
        print("\n\n⚡ 실제 에이전트 SDK 데모를 실행합니다...")

        # 패턴 1: 단일 에이전트
        asyncio.run(demo_single_agent(
            "현재 디렉토리의 Python 파일들을 나열하고 각 파일의 주요 역할을 한 줄로 설명해주세요."
        ))

        # 패턴 2: 서브에이전트 코드 리뷰
        asyncio.run(demo_subagent_code_review("."))
    else:
        print("\n\n📌 실제 에이전트 실행은 건너뜁니다 (API 키 또는 SDK 없음)")
        print("   위의 프롬프트 템플릿과 서브에이전트 파일을 Claude Code에서 활용하세요.")

    print("\n\n✅ 데모 완료!")
    print("📚 더 자세한 내용: https://code.claude.com/docs/en/agent-teams")
