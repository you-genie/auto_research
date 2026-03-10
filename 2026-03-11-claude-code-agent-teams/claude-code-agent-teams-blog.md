# Claude Code의 에이전트 팀: AI가 팀을 이루어 일한다는 게 어떤 건가요?

> "Agent Teams enable orchestration of multiple Claude Code sessions working collaboratively on shared projects." — [Claude Code 공식 문서](https://code.claude.com/docs/en/agent-teams)

솔직히 말하면, 처음 "에이전트 팀"이라는 말을 들었을 때 좀 황당했거든요. 그냥 AI 한 명도 잘 쓰면 되지, 왜 팀이야? 싶었죠. 근데 실제로 파고들어 보니까 이게 진짜 판도 바꾸는 개념이에요. AI 여럿이 서로 대화하면서 코드 리뷰를 하고, 버그 원인을 토론하고, 각자 맡은 모듈을 병렬로 개발한다? 그거 그냥 AI 쓰는 게 아니라 **AI 엔지니어링 팀을 굴리는 거잖아요.**

이 글에서는 Claude Code의 에이전트 팀 기능을 처음부터 끝까지 뜯어보겠습니다. 개념부터 아키텍처, 실제 사용법, 베스트 프랙티스까지 다 다룰 거예요.

---

## 목차

1. [에이전트 팀이 뭔데요?](#1-에이전트-팀이-뭔데요)
2. [서브에이전트 vs 에이전트 팀: 뭐가 다른가요?](#2-서브에이전트-vs-에이전트-팀-뭐가-다른가요)
3. [에이전트 팀의 아키텍처](#3-에이전트-팀의-아키텍처)
4. [서브에이전트 완전 정복](#4-서브에이전트-완전-정복)
5. [Git Worktree로 에이전트 격리](#5-git-worktree로-에이전트-격리)
6. [Claude Agent SDK와의 연결](#6-claude-agent-sdk와의-연결)
7. [실전 사용 사례와 패턴](#7-실전-사용-사례와-패턴)
8. [베스트 프랙티스](#8-베스트-프랙티스)
9. [한계와 주의사항](#9-한계와-주의사항)

---

## 1. 에이전트 팀이 뭔데요?

에이전트 팀(Agent Teams)은 [Claude Code](https://code.claude.com)에서 여러 Claude Code 인스턴스를 하나의 팀으로 조율하는 기능이에요. 2026년 초, Anthropic이 Opus 4.6 릴리스와 함께 실험적 기능으로 출시했습니다.

핵심을 한 줄로 요약하면 이렇습니다:

> "One session acts as the team lead, coordinating work, assigning tasks, and synthesizing results. Teammates work independently, each in its own context window, and communicate directly with each other." — [공식 문서](https://code.claude.com/docs/en/agent-teams)
>
> 하나의 세션이 팀 리드 역할을 맡아서 작업을 조율하고, 태스크를 배분하고, 결과를 취합합니다. 팀원들은 각자의 컨텍스트 윈도우 안에서 독립적으로 일하면서 서로 직접 소통합니다.

기존 AI 코딩 도구들은 대부분 "하나의 AI, 하나의 컨텍스트" 방식이에요. 그런데 현실의 복잡한 소프트웨어 개발은 그렇게 단선적이지 않잖아요. 프론트엔드, 백엔드, 테스트, 보안 검토가 동시에 진행되어야 하는데, 에이전트 팀은 바로 그 병렬성을 AI에게도 가져다 줍니다.

### 에이전트 팀 활성화 방법

기본적으로 비활성화된 실험 기능이라 설정이 필요해요.

```bash
# 환경 변수로 활성화
export CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1
```

또는 `settings.json`에 영구 설정:

```json
{
  "env": {
    "CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS": "1"
  }
}
```

---

## 2. 서브에이전트 vs 에이전트 팀: 뭐가 다른가요?

이게 가장 많이 헷갈리는 부분이에요. 두 개념을 비교해봅시다.

### 서브에이전트 (Subagents)

서브에이전트는 메인 세션 안에서 돌아가는 전문화된 AI 도우미예요. 각자 독립적인 컨텍스트 윈도우를 갖지만, 결과는 메인 에이전트한테만 보고해요.

- 쉽게 말하면: 팀장이 일을 시키고, 팀원은 결과만 가져와요
- 팀원끼리 직접 얘기는 못 해요
- 비용이 상대적으로 저렴

### 에이전트 팀 (Agent Teams)

에이전트 팀은 각 팀원이 완전히 독립적인 Claude Code 세션이에요. 팀원들이 서로 직접 메시지를 보낼 수 있고, 공유 태스크 목록을 통해 자기조율이 가능해요.

- 쉽게 말하면: 실제 엔지니어링 팀처럼 서로 토론하고 협력해요
- 팀원 A가 팀원 B에게 발견한 내용을 바로 전달할 수 있어요
- 비용이 더 높지만 복잡한 작업에선 그만한 가치가 있어요

| 항목 | 서브에이전트 | 에이전트 팀 |
|------|-------------|------------|
| **컨텍스트** | 자체 컨텍스트 윈도우 | 자체 컨텍스트 윈도우 (완전 독립) |
| **소통 방식** | 메인 에이전트에게만 결과 보고 | 팀원 간 직접 메시지 |
| **조율 방식** | 메인 에이전트가 모든 작업 관리 | 공유 태스크 목록으로 자기조율 |
| **최적 용도** | 결과만 필요한 집중된 태스크 | 토론과 협업이 필요한 복잡한 작업 |
| **토큰 비용** | 낮음 | 높음 (각 팀원이 별도 인스턴스) |

[공식 문서](https://code.claude.com/docs/en/agent-teams)에서 핵심을 이렇게 정리해 줘요:

> "Use subagents when you need quick, focused workers that report back. Use agent teams when teammates need to share findings, challenge each other, and coordinate on their own."
>
> 빠르고 집중적으로 결과만 필요할 땐 서브에이전트를. 팀원들이 발견한 걸 공유하고 서로 반론을 제기하며 자체 조율이 필요하면 에이전트 팀을 사용하세요.

---

## 3. 에이전트 팀의 아키텍처

에이전트 팀은 크게 네 가지 컴포넌트로 이루어져 있어요.

```
┌─────────────────────────────────────────────────────────┐
│                    에이전트 팀 구조                      │
│                                                         │
│  ┌─────────────┐         ┌──────────────────────────┐  │
│  │  Team Lead  │◄───────►│     Shared Task List     │  │
│  │ (메인 세션) │         │  ┌──────────┐            │  │
│  └──────┬──────┘         │  │ Task 1   │ pending    │  │
│         │                │  │ Task 2   │ in-progress│  │
│    spawn│                │  │ Task 3   │ completed  │  │
│         ▼                │  └──────────┘            │  │
│  ┌──────────────────┐    └──────────────────────────┘  │
│  │    Teammates     │                                   │
│  │                  │              ┌─────────────────┐  │
│  │  ┌────────────┐  │    Mailbox   │                 │  │
│  │  │Teammate A  │◄─┼─────────────►│ 에이전트 간     │  │
│  │  └────────────┘  │              │ 직접 메시지    │  │
│  │  ┌────────────┐  │              │ 시스템          │  │
│  │  │Teammate B  │◄─┼─────────────►│                 │  │
│  │  └────────────┘  │              └─────────────────┘  │
│  │  ┌────────────┐  │                                   │
│  │  │Teammate C  │  │                                   │
│  │  └────────────┘  │                                   │
│  └──────────────────┘                                   │
└─────────────────────────────────────────────────────────┘
```

### 팀 리드 (Team Lead)

팀을 생성하고, 팀원을 소환하고, 작업을 조율하고, 결과를 종합하는 메인 세션이에요. 팀의 존속 기간 동안 리드는 고정되어 있어요 — 팀원을 리드로 승격시키거나 리더십을 이전할 수 없다는 게 현재의 제약사항이에요.

### 팀원 (Teammates)

각자 독립적인 Claude Code 세션이에요. 소환될 때 팀 리드의 소환 프롬프트를 받아서 시작하고, `CLAUDE.md`, MCP 서버, 스킬 등 프로젝트 컨텍스트를 자동으로 로드해요. 리드의 대화 히스토리는 넘어오지 않는다는 점이 중요해요.

### 공유 태스크 목록 (Shared Task List)

팀 전체가 보는 작업 목록이에요. 태스크는 세 가지 상태를 가집니다: `pending(대기)`, `in progress(진행 중)`, `completed(완료)`. 태스크 간 의존성도 설정할 수 있어서, 선행 태스크가 완료되어야만 다음 태스크를 클레임할 수 있어요.

> "Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously." — [공식 문서](https://code.claude.com/docs/en/agent-teams)
>
> 태스크 클레임은 파일 잠금을 사용해서 여러 팀원이 동시에 같은 태스크를 가져가려 할 때 발생하는 경합 조건을 방지합니다.

### 메일박스 (Mailbox)

에이전트 간 비동기 메시지 시스템이에요. 팀원이 메시지를 보내면 수신자에게 자동 전달되고, 리드가 폴링할 필요가 없어요. 팀원이 작업을 마치고 멈추면 리드에게 자동 알림이 가요.

### 로컬 저장 위치

팀 데이터는 로컬에 저장돼요:
- **팀 설정**: `~/.claude/teams/{team-name}/config.json`
- **태스크 목록**: `~/.claude/tasks/{team-name}/`

---

## 4. 서브에이전트 완전 정복

에이전트 팀의 기반이 되는 서브에이전트도 자세히 봐야 해요. 사실 서브에이전트만으로도 엄청 강력하거든요.

### 내장 서브에이전트

Claude Code에는 기본으로 탑재된 서브에이전트가 있어요.

| 서브에이전트 | 모델 | 역할 |
|------------|------|------|
| **Explore** | Haiku (빠름) | 코드베이스 탐색 및 파일 검색 (읽기 전용) |
| **Plan** | 메인과 동일 | 플랜 모드에서 컨텍스트 수집 |
| **General-purpose** | 메인과 동일 | 복잡한 멀티스텝 작업 |
| **Bash** | 메인과 동일 | 별도 컨텍스트에서 터미널 명령 실행 |

### 커스텀 서브에이전트 만들기

서브에이전트는 YAML 프론트매터가 있는 마크다운 파일로 정의해요.

```markdown
---
name: code-reviewer
description: 코드 품질과 보안을 검토하는 전문가. 코드 변경 후 자동으로 사용.
tools: Read, Grep, Glob, Bash
model: sonnet
memory: project
---

당신은 시니어 코드 리뷰어입니다. 코드가 변경될 때마다 다음을 검토하세요:

## 검토 체크리스트
- 코드 가독성 및 명명 규칙
- 중복 코드 여부
- 에러 처리 적절성
- API 키 등 민감 정보 노출 여부
- 입력 유효성 검사
- 테스트 커버리지
- 성능 최적화 가능성

결과를 다음 형식으로 보고하세요:
- 심각 문제 (반드시 수정)
- 경고 (수정 권장)
- 제안 (고려해볼 개선 사항)
```

저장 위치에 따라 범위가 달라져요:

| 위치 | 범위 | 우선순위 |
|------|------|---------|
| `--agents` CLI 플래그 | 현재 세션만 | 1 (최고) |
| `.claude/agents/` | 현재 프로젝트 | 2 |
| `~/.claude/agents/` | 모든 프로젝트 | 3 |
| 플러그인 `agents/` | 플러그인 활성화 위치 | 4 (최저) |

### 프론트매터 주요 필드

| 필드 | 필수 | 설명 |
|------|------|------|
| `name` | Y | 소문자 + 하이픈 식별자 |
| `description` | Y | Claude가 언제 이 에이전트에 위임할지 결정하는 설명 |
| `tools` | N | 사용 가능한 도구 목록 (생략 시 모두 상속) |
| `disallowedTools` | N | 명시적으로 차단할 도구 |
| `model` | N | `sonnet`, `opus`, `haiku`, `inherit` 중 하나 |
| `permissionMode` | N | `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | N | 최대 에이전트 턴 수 |
| `skills` | N | 시작 시 주입할 스킬 목록 |
| `memory` | N | 영구 메모리 범위: `user`, `project`, `local` |
| `background` | N | `true`면 항상 백그라운드 실행 |
| `isolation` | N | `worktree`로 설정 시 격리된 git worktree에서 실행 |

### 영구 메모리 (Persistent Memory)

서브에이전트에 메모리를 활성화하면 대화 간에 지식이 누적돼요.

```markdown
---
name: codebase-expert
description: 코드베이스 전문가. 자주 묻는 구조와 패턴을 기억함.
memory: project
---

새로운 코드패스, 패턴, 라이브러리 위치, 아키텍처 결정을 발견할 때마다
에이전트 메모리를 업데이트하세요. 각 세션에서 배운 것을 간결하게 기록합니다.
```

메모리 범위:

| 범위 | 저장 위치 | 용도 |
|------|----------|------|
| `user` | `~/.claude/agent-memory/<name>/` | 모든 프로젝트에 걸친 학습 |
| `project` | `.claude/agent-memory/<name>/` | 프로젝트 특화 지식, 버전 관리 가능 |
| `local` | `.claude/agent-memory-local/<name>/` | 프로젝트 특화, 버전 관리 제외 |

### 워크트리 격리

고용량 작업이나 파일 충돌이 우려될 때 `isolation: worktree`를 쓰면 서브에이전트가 격리된 git worktree에서 돌아요.

```markdown
---
name: large-refactor
description: 대규모 리팩토링 작업을 격리된 환경에서 수행
tools: Read, Edit, Bash
isolation: worktree
---
```

---

## 5. Git Worktree로 에이전트 격리

[공식 트위터 스레드](https://www.threads.com/@boris_cherny/post/DVAAnexgRUj/)에서 Claude Code에 내장 worktree 지원이 추가되었다는 발표가 있었어요:

> "Now, agents can run in parallel without interfering with one another. Each agent gets its own worktree and can work independently."
>
> 이제 에이전트들이 서로 간섭 없이 병렬로 실행될 수 있습니다. 각 에이전트는 자체 worktree를 갖고 독립적으로 작업할 수 있습니다.

### Worktree 방식의 핵심 이점

같은 파일을 여러 에이전트가 동시에 편집해도 충돌이 없어요. 에이전트 A가 `src/auth.ts`를 한 방식으로 리팩토링하고, 에이전트 B가 같은 파일을 다른 방식으로 리팩토링한 다음, 둘 다 검토하고 더 나은 것을 선택하거나 합칠 수 있어요.

```bash
# CLI에서 격리된 worktree로 실행
claude --worktree my-feature-branch

# tmux 세션도 함께 생성
claude --worktree my-feature --tmux
```

Worktree를 사용하면 각 에이전트의 워크트리가 `.claude/worktrees/{name}/`에 생성돼요.

---

## 6. Claude Agent SDK와의 연결

Claude Code SDK가 **Claude Agent SDK**로 이름이 바뀌었어요. 단순한 코딩 도구를 넘어선 범용 에이전트 프레임워크로 포지셔닝한 거예요.

> "At its core, the SDK gives you the primitives to build agents for whatever workflow you're trying to automate." — [Anthropic Engineering Blog](https://claude.com/blog/building-agents-with-the-claude-agent-sdk)
>
> SDK의 핵심은 자동화하려는 어떤 워크플로우에든 에이전트를 구축할 수 있는 기본 요소를 제공하는 것입니다.

### SDK 설치

```bash
# Python
pip install claude-agent-sdk

# TypeScript
npm install @anthropic-ai/claude-agent-sdk
```

### 기본 사용 예시

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions

async def main():
    async for message in query(
        prompt="auth.py에 있는 버그를 찾아서 수정해줘",
        options=ClaudeAgentOptions(allowed_tools=["Read", "Edit", "Bash"]),
    ):
        print(message)

asyncio.run(main())
```

### SDK에서 서브에이전트 활용

```python
import asyncio
from claude_agent_sdk import query, ClaudeAgentOptions, AgentDefinition

async def main():
    async for message in query(
        prompt="code-reviewer 에이전트로 이 코드베이스를 리뷰해줘",
        options=ClaudeAgentOptions(
            allowed_tools=["Read", "Glob", "Grep", "Agent"],
            agents={
                "code-reviewer": AgentDefinition(
                    description="품질과 보안 검토를 위한 전문 코드 리뷰어.",
                    prompt="코드 품질을 분석하고 개선 사항을 제안하세요.",
                    tools=["Read", "Glob", "Grep"],
                )
            },
        ),
    ):
        if hasattr(message, "result"):
            print(message.result)

asyncio.run(main())
```

### 에이전트 루프의 핵심 구조

SDK는 다음 피드백 루프를 기반으로 동작해요:

```
맥락 수집 (Gather Context)
        ↓
행동 수행 (Take Action)
        ↓
작업 검증 (Verify Work)
        ↓
     반복 (Repeat)
```

이 루프가 태스크 완료까지 자동으로 반복되는 거예요.

### Claude Code CLI vs Agent SDK 비교

| 항목 | CLI | Agent SDK |
|------|-----|----------|
| **주 용도** | 인터랙티브 개발 | CI/CD, 커스텀 앱 |
| **인터페이스** | 터미널 대화형 | 프로그래밍 방식 |
| **자동화** | 제한적 | 완전한 자동화 가능 |
| **컨트롤** | 사용자 직접 개입 | 코드로 완전 제어 |

많은 팀이 일상 개발엔 CLI를, 프로덕션 자동화엔 SDK를 함께 써요.

---

## 7. 실전 사용 사례와 패턴

### 패턴 1: 병렬 코드 리뷰

PR 하나를 여러 관점에서 동시에 검토하는 방법이에요.

```text
Create an agent team to review PR #142. Spawn three reviewers:
- One focused on security implications
- One checking performance impact
- One validating test coverage
Have them each review and report findings.
```

[공식 문서](https://code.claude.com/docs/en/agent-teams#use-case-examples)에서 이 패턴을 이렇게 설명해요:

> "A single reviewer tends to gravitate toward one type of issue at a time. Splitting review criteria into independent domains means security, performance, and test coverage all get thorough attention simultaneously."
>
> 단일 리뷰어는 한 번에 한 종류의 문제에만 집중하는 경향이 있습니다. 검토 기준을 독립적인 영역으로 나누면 보안, 성능, 테스트 커버리지가 모두 동시에 철저하게 검토됩니다.

### 패턴 2: 경쟁 가설로 버그 조사

원인을 모를 때 특히 강력한 패턴이에요.

```text
Users report the app exits after one message instead of staying connected.
Spawn 5 agent teammates to investigate different hypotheses.
Have them talk to each other to try to disprove each other's theories,
like a scientific debate. Update the findings doc with whatever consensus emerges.
```

이 "토론 구조"가 핵심이에요. 하나의 에이전트가 한 이론을 찾으면 그걸로 닻이 내려져서 다른 가능성을 못 봐요. 여러 에이전트가 서로의 이론을 반박하려 할 때, 살아남는 이론이 진짜 원인일 가능성이 훨씬 높아요.

### 패턴 3: 크로스 레이어 기능 개발

프론트엔드, 백엔드, 테스트를 동시에 작업하는 패턴이에요.

```text
I need to add a new user notification system.
Create an agent team:
- Backend teammate: implement notification service and API endpoints
- Frontend teammate: build the notification UI components
- Test teammate: write unit and integration tests for both
Each teammate should own their domain completely.
```

각 팀원이 서로 다른 파일을 소유하므로 충돌이 없어요.

### 패턴 4: 연구 + 리뷰 조합

라이브러리 선택이나 아키텍처 결정 시 유용해요.

```text
I'm designing a CLI tool that helps developers track TODO comments across
their codebase. Create an agent team to explore this from different angles:
one teammate on UX, one on technical architecture, one playing devil's advocate.
```

[공식 문서](https://code.claude.com/docs/en/agent-teams#when-to-use-agent-teams)에 따르면 에이전트 팀이 빛나는 순간은:

- **리서치 & 리뷰**: 다양한 관점에서 동시 조사 후 서로 검증
- **새 모듈/기능**: 각 팀원이 서로 다른 부분을 소유
- **경쟁 가설 디버깅**: 여러 이론을 병렬로 테스트
- **크로스 레이어 조율**: 프론트엔드, 백엔드, 테스트 동시 작업

### 패턴 5: 서브에이전트 체이닝

여러 서브에이전트를 순차적으로 연결하는 패턴이에요.

```text
Use the code-reviewer subagent to find performance issues,
then use the optimizer subagent to fix them
```

각 서브에이전트가 작업을 완료하고 결과를 메인 컨텍스트로 반환하면, Claude가 관련 컨텍스트를 다음 서브에이전트에 전달해요.

---

## 8. 베스트 프랙티스

### 팀 크기 결정하기

팀원 수에는 하드 제한이 없지만 실용적인 제약이 있어요:

- **토큰 비용이 선형으로 증가**: 팀원마다 독립적인 컨텍스트 윈도우
- **조율 오버헤드 증가**: 더 많은 팀원 = 더 많은 소통과 태스크 조율
- **체감 수익 감소**: 일정 이상은 팀원 추가의 효과가 줄어들어요

> "Start with 3-5 teammates for most workflows. This balances parallel work with manageable coordination." — [공식 문서](https://code.claude.com/docs/en/agent-teams#best-practices)
>
> 대부분의 워크플로우에서 3-5명의 팀원으로 시작하세요. 병렬 작업과 관리 가능한 조율의 균형이 잡혀요.

팀원 한 명당 5-6개 태스크가 적당해요. 15개의 독립적 태스크가 있으면 3명의 팀원이 좋은 출발점이에요.

### 팀원에게 충분한 컨텍스트 주기

팀원들은 프로젝트 컨텍스트(`CLAUDE.md`, MCP 서버, 스킬)는 자동으로 로드하지만, 리드의 대화 히스토리는 없어요. 소환 프롬프트에 태스크 특화 정보를 포함하세요:

```text
Spawn a security reviewer teammate with the prompt:
"Review the authentication module at src/auth/ for security vulnerabilities.
Focus on token handling, session management, and input validation.
The app uses JWT tokens stored in httpOnly cookies.
Report any issues with severity ratings."
```

### CLAUDE.md 활용

`CLAUDE.md` 파일은 모든 팀원이 정상적으로 읽어요. 프로젝트 특화 가이드를 여기에 넣으면 모든 에이전트 팀원이 동일한 코딩 컨벤션과 아키텍처 결정을 따르게 돼요.

### 태스크 크기 적절히 조절

- **너무 작음**: 조율 오버헤드가 이익을 초과
- **너무 큼**: 팀원이 너무 오래 체크인 없이 작업하여 낭비 위험
- **적당**: 명확한 결과물을 내는 자기완결적 단위 (함수, 테스트 파일, 리뷰)

### 파일 충돌 피하기

같은 파일을 두 팀원이 편집하면 덮어쓰기가 발생해요. 각 팀원이 서로 다른 파일 집합을 소유하도록 작업을 분배하세요.

### 지속적인 모니터링

팀을 방치하면 낭비가 늘어요. 진행 상황을 주기적으로 확인하고, 잘 안 되는 방향은 수정하고, 결과가 나오면 바로 종합하세요.

---

## 9. 한계와 주의사항

에이전트 팀은 실험 기능이라 알려진 제약사항이 있어요.

| 제약사항 | 설명 |
|---------|------|
| **세션 재개 불가** | 인프로세스 팀원 포함 시 `/resume`와 `/rewind`가 팀원을 복원하지 않음 |
| **태스크 상태 지연** | 팀원이 가끔 태스크를 완료 표시 안 해서 의존 태스크가 막힐 수 있음 |
| **종료 속도** | 현재 요청/도구 호출 완료 후 종료하므로 시간이 걸릴 수 있음 |
| **팀 하나만** | 리드는 한 번에 팀 하나만 관리 가능 |
| **중첩 팀 불가** | 팀원은 자신의 팀이나 팀원을 생성할 수 없음 |
| **리드 고정** | 팀 생성한 세션이 평생 리드. 팀원을 리드로 승격 불가 |
| **스플릿 패널 제약** | tmux 또는 iTerm2 필요. VS Code 통합 터미널, Windows Terminal, Ghostty 미지원 |

### 토큰 비용 현실

에이전트 팀은 비용이 상당해요:

> "A 3-teammate team uses roughly 3-4x the tokens of a single session doing the same work sequentially." — [claudefa.st](https://claudefa.st/blog/guide/agents/agent-teams)
>
> 3명 팀원 팀은 같은 작업을 순차적으로 하는 단일 세션보다 약 3-4배의 토큰을 사용합니다.

팀원들이 20-30초 내에 생성되고 1분 안에 결과를 내기 시작한다는 게 위안이에요. 복잡한 태스크에서 시간 절약이 비용을 정당화하죠.

### 언제 쓰지 말아야 할까?

이런 경우엔 단일 세션이나 서브에이전트를 쓰는 게 나아요:
- 순차적 태스크 (이전 결과에 다음이 의존)
- 같은 파일 편집 작업
- 의존성이 많아 병렬화가 어려운 작업
- 빠른 일회성 작업

---

## 정리하며

Claude Code의 에이전트 팀은 아직 실험 단계지만, AI 개발 워크플로우의 미래를 엿볼 수 있는 기능이에요. 단순히 "AI가 코드를 짜준다"에서 "AI 엔지니어링 팀이 협력해서 복잡한 문제를 풀어낸다"로의 전환이거든요.

특히 인상적인 건 서로 이론을 반박하는 구조예요. 혼자 답을 찾는 것보다 서로 검증하는 팀이 훨씬 신뢰할 수 있는 결론에 도달한다는 건, 소프트웨어 개발에서도 인간 팀에서도 마찬가지잖아요. AI 팀도 그 원칙을 따르는 거죠.

지금 당장 모든 걸 에이전트 팀으로 대체하려 하기보다는, 병렬 코드 리뷰나 경쟁 가설 디버깅처럼 명확히 병렬성이 가치 있는 곳부터 시작해 보세요. 비용과 조율 오버헤드를 감수할 만한 충분한 복잡도가 있을 때 진가를 발휘하는 기능이에요.

---

## 참고 자료

| 번호 | 출처 | URL |
|------|------|-----|
| 1 | Claude Code - Agent Teams 공식 문서 | https://code.claude.com/docs/en/agent-teams |
| 2 | Claude Code - Sub-agents 공식 문서 | https://code.claude.com/docs/en/sub-agents |
| 3 | Claude Code - Overview 공식 문서 | https://code.claude.com/docs/en/overview |
| 4 | Claude Agent SDK - Overview 공식 문서 | https://platform.claude.com/docs/en/agent-sdk/overview |
| 5 | Building Agents with Claude Agent SDK | https://claude.com/blog/building-agents-with-the-claude-agent-sdk |
| 6 | Claudefast - Agent Teams Complete Guide | https://claudefa.st/blog/guide/agents/agent-teams |
| 7 | Shipyard - Multi-agent Orchestration | https://shipyard.build/blog/claude-code-multi-agent/ |
| 8 | Boris Cherny - Worktree 발표 | https://www.threads.com/@boris_cherny/post/DVAAnexgRUj/ |
| 9 | TLDR Agent Teams (Medium) | https://bertomill.medium.com/tldr-agent-teams-multi-agent-coordination-in-claude-code-a73590d8453f |
| 10 | Turing College - Agent Teams Explained | https://www.turingcollege.com/blog/claude-agent-teams-explained |
