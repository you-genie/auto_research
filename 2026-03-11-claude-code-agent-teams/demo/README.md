# Claude Code 에이전트 팀 데모

이 데모는 Claude Code의 에이전트 팀(Agent Teams) 기능과 Claude Agent SDK를 활용하는 패턴을 보여줍니다.

## 사전 요구사항

- Python 3.10 이상
- Anthropic API 키 ([console.anthropic.com](https://console.anthropic.com)에서 발급)
- Claude Code 설치 (`curl -fsSL https://claude.ai/install.sh | bash`)

## 설치

```bash
pip install -r requirements.txt
```

## API 키 설정

```bash
export ANTHROPIC_API_KEY=your-api-key
```

또는 `.env` 파일:

```
ANTHROPIC_API_KEY=your-api-key
```

## 실행

```bash
python demo_agent_sdk.py
```

## 데모 내용

### 패턴 1: 단일 에이전트 (SDK)

```python
from claude_agent_sdk import query, ClaudeAgentOptions

async for message in query(
    prompt="현재 디렉토리의 파일을 분석해줘",
    options=ClaudeAgentOptions(allowed_tools=["Read", "Glob", "Grep"]),
):
    if hasattr(message, "result"):
        print(message.result)
```

### 패턴 2: 서브에이전트 병렬 코드 리뷰 (SDK)

세 개의 전문 서브에이전트(보안·성능·품질)가 동시에 코드를 검토합니다.

```python
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

options = ClaudeAgentOptions(
    allowed_tools=["Read", "Glob", "Grep", "Agent"],
    agents={
        "security-reviewer": AgentDefinition(...),
        "performance-analyzer": AgentDefinition(...),
        "quality-checker": AgentDefinition(...),
    }
)
```

### 패턴 3: 에이전트 팀 (Claude Code CLI)

실제 에이전트 팀은 Claude Code CLI에서 실행합니다.

1. 에이전트 팀 활성화:
```bash
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

2. Claude Code 실행:
```bash
claude
```

3. 에이전트 팀 생성 프롬프트:
```
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
```

### 패턴 4: 서브에이전트 파일 자동 생성

스크립트가 `demo_agents/` 폴더에 4개의 서브에이전트 파일을 생성합니다:
- `code-reviewer.md`
- `security-auditor.md`
- `test-writer.md`
- `debugger.md`

`.claude/agents/`로 복사하면 Claude Code에서 바로 사용 가능합니다.

## 에이전트 팀 vs 서브에이전트

| 항목 | 서브에이전트 | 에이전트 팀 |
|------|-------------|------------|
| 인터페이스 | SDK (프로그래밍 방식) | CLI (대화형) |
| 팀원 간 소통 | 불가 (메인에게만 보고) | 가능 (직접 메시지) |
| 비용 | 낮음 | 3~4배 |
| 최적 용도 | CI/CD, 자동화 | 복잡한 협업 작업 |

## 참고 문서

- [에이전트 팀 공식 문서](https://code.claude.com/docs/en/agent-teams)
- [서브에이전트 공식 문서](https://code.claude.com/docs/en/sub-agents)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
