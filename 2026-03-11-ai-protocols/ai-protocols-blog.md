---
layout: default
title: "AI 프로토콜 완전 정복: MCP, A2A, Tool Use, AGENTS.md까지 한 번에"
date: 2026-03-11
---

# AI 프로토콜 완전 정복: MCP, A2A, Tool Use, AGENTS.md까지 한 번에

> "The protocol wars are over. MCP won the tool connectivity battle. A2A is winning the agent collaboration layer. And together, they're forming the backbone of the agentic web."
> — DEV Community, 2026

솔직히 AI 프로토콜 얘기 나오면 눈이 슬슬 감기기 시작하죠? MCP, A2A, Tool Use, Function Calling... 이게 다 뭔지, 뭐가 다른지, 내가 뭘 써야 하는지 헷갈리는 분들 많을 거예요. 이번 글에서 2026년 기준으로 AI 생태계를 떠받치는 핵심 프로토콜들을 한 번에 정리해 드릴게요. 커피 한 잔 들고 편하게 읽어보세요.

---

## 목차

1. [AI 프로토콜이 왜 필요해졌나요?](#왜-필요했나)
2. [Model Context Protocol (MCP)](#mcp)
3. [Agent2Agent Protocol (A2A)](#a2a)
4. [Tool Use Protocol: OpenAI vs. Claude](#tool-use)
5. [AGENTS.md - 에이전트를 위한 README](#agentsmd)
6. [기타 프레임워크 프로토콜: LangChain, AutoGen, Semantic Kernel](#frameworks)
7. [프로토콜 비교표 및 언제 뭘 써야 하나요?](#comparison)
8. [Agentic AI Foundation: 프로토콜 거버넌스의 미래](#aaif)
9. [2026년 전망 및 결론](#outlook)

---

## 1. AI 프로토콜이 왜 필요해졌나요? {#왜-필요했나}

2023년까지만 해도 LLM은 주로 "질문하면 답변하는" 형태였어요. 근데 2024~2025년부터 에이전트(Agent) 개념이 폭발적으로 성장하면서 상황이 완전히 달라졌거든요.

에이전트는 단순히 답변만 하는 게 아니라 **외부 도구를 사용하고, 데이터베이스에 접근하고, 다른 에이전트와 협력하면서 복잡한 작업을 자율적으로 수행**해야 해요. 그런데 에이전트마다, 회사마다, 프레임워크마다 도구 연결 방식이 제각각이었거든요.

```
[Before 프로토콜 표준화]
Claude 에이전트 → 독자적 API 연결 방식
ChatGPT 에이전트 → 또 다른 독자적 방식
LangChain 에이전트 → 또또 다른 방식
...
```

이게 바로 **M×N 통합 문제**예요. M개의 AI 시스템이 N개의 도구/데이터에 연결하려면 M×N개의 커스텀 연결을 만들어야 했죠. 유지보수 악몽이에요.

[Anthropic의 MCP 발표 블로그](https://www.anthropic.com/news/model-context-protocol)에서는 이 문제를 이렇게 표현했어요:

> "MCP addresses the challenge of providing AI systems with useful context in a standardized way, enabling them to connect to the data sources and tools they need."

그래서 등장한 게 바로 프로토콜 표준화예요. USB-C가 각종 기기 충전 방식을 통일한 것처럼, AI 프로토콜이 에이전트와 도구/데이터의 연결 방식을 표준화하기 시작한 거죠.

---

## 2. Model Context Protocol (MCP) {#mcp}

### 한 줄 요약

> MCP = "AI 에이전트에게 손을 주는 프로토콜" (도구와 데이터 연결 표준)

### 탄생 배경과 역사

[Anthropic이 2024년 11월 MCP를 오픈소스로 공개](https://www.anthropic.com/news/model-context-protocol)했을 때, 솔직히 업계 반응이 뜨뜻미지근했어요. "또 Anthropic이 뭔가 만들었네" 정도였죠. 근데 6개월 후에 OpenAI가 채택하고, Google이 채택하고, 2025년 12월에 Linux Foundation 산하 Agentic AI Foundation(AAIF)에 기부되면서 **사실상 업계 표준**이 됐거든요.

[Wikipedia MCP 문서](https://en.wikipedia.org/wiki/Model_Context_Protocol)에 따르면, MCP는 개발자들이 LLM과 코드 에디터 사이에서 컨텍스트를 끊임없이 복사-붙여넣기 해야 하는 불편함에서 출발했다고 해요.

**채택 타임라인:**

| 시기 | 사건 |
|------|------|
| 2024년 11월 | Anthropic, MCP 오픈소스 공개 (Python/TypeScript SDK) |
| 2025년 3월 | OpenAI, Agents SDK/Responses API/ChatGPT 데스크톱에 MCP 채택 |
| 2025년 4월 | Google DeepMind, Gemini 모델 MCP 지원 확인 |
| 2025년 11월 | 대규모 스펙 업데이트: 비동기 작업, 상태 비저장, 서버 ID, 공식 레지스트리 |
| 2025년 12월 | Anthropic, Linux Foundation AAIF에 MCP 기부 |
| 2026년 3월 현재 | 9,700만+ 월간 SDK 다운로드, 10,000+ 활성 서버 |

### 핵심 아키텍처

MCP는 [Language Server Protocol(LSP)](https://microsoft.github.io/language-server-protocol/)에서 영감을 받았어요. IDE들이 프로그래밍 언어 지원을 표준화한 것처럼, MCP는 AI 도구 통합을 표준화한 거죠.

```
┌─────────────────────────────────────────────────────┐
│                    MCP Architecture                   │
│                                                       │
│  ┌──────────┐    ┌──────────┐    ┌──────────────┐   │
│  │  Host    │    │  Client  │    │   Server     │   │
│  │ (Claude, │◄──►│(Connector│◄──►│(External     │   │
│  │ ChatGPT) │    │  Layer)  │    │ Service/DB)  │   │
│  └──────────┘    └──────────┘    └──────────────┘   │
│                                                       │
│            Transport: JSON-RPC 2.0                    │
│            (stdio, HTTP+SSE, WebSocket)               │
└─────────────────────────────────────────────────────┘
```

세 가지 핵심 역할:
- **Host**: LLM 애플리케이션 (Claude, ChatGPT, Cursor 등)
- **Client**: Host 안에 있는 MCP 연결 레이어
- **Server**: 외부 서비스/데이터를 노출하는 서버

### MCP가 제공하는 4가지 기능 {#mcp-features}

[MCP 공식 스펙(2025-11-25)](https://modelcontextprotocol.io/specification/2025-11-25)에 정의된 핵심 기능:

**서버 → 클라이언트:**
1. **Tools (도구)**: AI가 실행할 수 있는 함수들 (파일 읽기, API 호출, DB 쿼리 등)
2. **Resources (리소스)**: 컨텍스트 데이터 (파일 내용, DB 레코드, 메시지 등)
3. **Prompts (프롬프트)**: 템플릿화된 메시지와 워크플로우

**클라이언트 → 서버:**
4. **Sampling (샘플링)**: 서버가 LLM 추론을 요청하는 기능 (역방향!)

이 역방향 Sampling 기능이 좀 독특한 거예요. 서버 쪽에서 "AI한테 이것 좀 물어봐줘"라고 요청할 수 있는 구조거든요.

**2025년 11월 업데이트에서 추가된 것들:**
- **Elicitation**: 서버가 사용자에게 추가 정보를 요청
- **Roots**: 서버가 파일시스템 경계를 파악
- 비동기 작업 지원
- 서버 신원 인증 강화

### 보안 고려사항

MCP는 강력하지만 보안 이슈도 있어요. [공식 스펙 보안 섹션](https://modelcontextprotocol.io/specification/2025-11-25)에서는 이렇게 강조해요:

> "Tools represent arbitrary code execution and must be treated with appropriate caution."

핵심 보안 원칙:
- 사용자 명시적 동의 필수
- 데이터 프라이버시 보호
- 도구 호출 전 사용자 확인
- LLM 샘플링 제어

실제로 허용 목록(allowlist) 방식과 샌드박싱이 프로덕션 환경에서 권장돼요.

### 왜 MCP가 "이겼나"?

[The New Stack의 분석](https://thenewstack.io/why-the-model-context-protocol-won/)에 따르면:

> "MCP won because it arrived at exactly the right moment, solved the right problem, and was simple enough to actually implement."

세 가지 이유:
1. **LSP에서 검증된 패턴**: 개발자들이 이미 익숙한 방식
2. **단순한 JSON-RPC**: 복잡하지 않아서 쉽게 구현 가능
3. **오픈소스 + 중립 거버넌스**: 특정 회사에 종속되지 않음

---

## 3. Agent2Agent Protocol (A2A) {#a2a}

### 한 줄 요약

> A2A = "AI 에이전트에게 동료를 주는 프로토콜" (에이전트 간 협력 표준)

### 탄생 배경

[Google이 2025년 4월 A2A를 발표](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)할 때, 50개 이상의 파트너사를 동시에 공개했어요. Salesforce, SAP, ServiceNow, McKinsey, Deloitte... 엔터프라이즈 무게감이 장난 아니었죠.

MCP가 "에이전트 ↔ 도구" 연결이라면, A2A는 "에이전트 ↔ 에이전트" 연결이에요.

예를 들어볼게요:
- **MCP 없이**: 에이전트가 Slack에 메시지 보내려면 직접 Slack API 코드 작성
- **MCP 있으면**: 에이전트가 표준화된 방식으로 Slack MCP 서버에 연결
- **A2A 없이**: Salesforce 에이전트가 ServiceNow 에이전트에게 티켓 전달하려면 맞춤 연동 개발
- **A2A 있으면**: 표준 프로토콜로 에이전트 간 직접 소통

### 핵심 아키텍처

[A2A 공식 사이트](https://a2a-protocol.org/latest/)에서 설명하는 핵심 구성:

```
┌──────────────────────────────────────────────────────────┐
│                    A2A Architecture                        │
│                                                            │
│  ┌─────────────┐                    ┌─────────────────┐   │
│  │ Client Agent│──── Task Request ──►│ Remote Agent    │   │
│  │ (요청하는   │◄─── Status Update ──│ (실행하는 에이전트) │   │
│  │  에이전트)  │                    └─────────────────┘   │
│  └─────────────┘                                          │
│         │                                                  │
│         ▼                                                  │
│  ┌─────────────────────────────────────────────────┐      │
│  │          Agent Card (/.well-known/agent.json)    │      │
│  │  { "name": "...", "capabilities": [...],         │      │
│  │    "endpoint": "...", "auth": {...} }             │      │
│  └─────────────────────────────────────────────────┘      │
│                                                            │
│  Transport: HTTP + SSE + JSON-RPC                          │
└──────────────────────────────────────────────────────────┘
```

**Agent Card (에이전트 카드)**가 핵심이에요. 각 에이전트가 `/.well-known/agent.json`에 자신의 능력을 공개하는 거예요. 마치 명함 같은 거죠:

```json
{
  "name": "Customer Support Agent",
  "description": "Handles customer inquiries",
  "capabilities": ["ticket_creation", "status_check", "escalation"],
  "endpoint": "https://support.example.com/a2a",
  "auth": { "type": "oauth2" },
  "supported_modalities": ["text", "file"]
}
```

### 작업(Task) 생명주기

A2A에서 작업은 명확한 상태를 가져요:

```
submitted → working → (input_needed) → completed
                    ↘                ↗
                     → failed
                     → canceled
```

특히 **장기 실행 작업** 지원이 인상적이에요. 몇 시간, 며칠이 걸리는 작업도 상태를 유지하며 진행할 수 있거든요.

### A2A 발전 현황

[Linux Foundation 공식 발표](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)에 따르면, A2A는 2025년 6월에 Linux Foundation에 기부됐어요.

버전 0.3 주요 업데이트:
- gRPC 지원 추가
- 보안 카드 서명 기능
- Python SDK 클라이언트 사이드 지원 확장

지원 SDK: Python, JavaScript, Java, C#/.NET, Golang

> "A2A is designed to complement, not compete with, MCP. While MCP provides helpful tools and context to agents, A2A enables agents to work together as a team."
> — [IBM, What Is Agent2Agent Protocol](https://www.ibm.com/think/topics/agent2agent-protocol)

---

## 4. Tool Use Protocol: OpenAI vs. Claude {#tool-use}

### 개요

"Tool Use Protocol"은 단일 표준이 아니라, 각 LLM 제공사가 구현한 도구 호출 방식이에요. 하지만 2025년 기준으로 JSON Schema 기반 도구 정의가 사실상 공통 형식이 됐어요.

### OpenAI Function Calling / Tool Use

[OpenAI의 Responses API](https://openai.com/index/new-tools-and-features-in-the-responses-api/)가 2025년 3월 출시되면서 도구 사용 방식이 크게 진화했어요.

**기본 도구 정의 형식:**

```json
{
  "type": "function",
  "function": {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "parameters": {
      "type": "object",
      "properties": {
        "location": {
          "type": "string",
          "description": "City and country, e.g., 'Seoul, Korea'"
        },
        "unit": {
          "type": "string",
          "enum": ["celsius", "fahrenheit"]
        }
      },
      "required": ["location"]
    },
    "strict": true
  }
}
```

**Strict Mode** (2025년 추가): `"strict": true`로 설정하면 JSON Schema를 100% 준수하는 응답을 보장해요. 프로덕션 에이전트에서 파라미터 오류를 원천 차단할 수 있죠.

**Responses API 내장 도구들:**
- `web_search`: 실시간 웹 검색
- `file_search`: 파일/문서 검색
- `computer_use`: 스크린샷 기반 UI 조작
- `code_interpreter`: 코드 실행
- `mcp`: 원격 MCP 서버 연결 (!)

OpenAI가 MCP를 Responses API 내장 도구로 지원한다는 게 흥미롭죠? MCP가 얼마나 표준이 됐는지 보여주는 거예요.

### Claude Tool Use

[Anthropic 공식 도큐멘테이션](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview)에 따르면, Claude의 도구 정의 형식:

```json
{
  "name": "get_weather",
  "description": "Get the current weather in a given location",
  "input_schema": {
    "type": "object",
    "properties": {
      "location": {
        "type": "string",
        "description": "The city and state, e.g. San Francisco, CA"
      },
      "unit": {
        "type": "string",
        "enum": ["celsius", "fahrenheit"]
      }
    },
    "required": ["location"]
  }
}
```

OpenAI와 비교하면 `parameters` 대신 `input_schema`를 쓰는 게 차이점이에요. 하지만 JSON Schema 기반이라는 건 동일하죠.

**Claude 고유 기능 (2025년 추가):**
- **Tool Search Tool**: 수천 개의 도구에서 필요한 것만 동적으로 로드 (컨텍스트 창 절약!)
- **Programmatic Tool Calling**: 코드 실행 환경에서 프로그래밍 방식으로 도구 호출
- **Strict Tool Use**: `strict: true`로 스키마 완전 준수 보장

**다중 도구 호출 흐름:**

```
User Message
    ↓
Claude Response (stop_reason: "tool_use")
    → tool_use blocks with unique IDs
    ↓
Tool Execution (외부에서)
    ↓
Tool Results (tool_result 블록으로 전달)
    ↓
Claude Final Response
```

### OpenAI vs. Claude 도구 사용 비교

| 항목 | OpenAI | Claude |
|------|--------|--------|
| 정의 키 | `parameters` | `input_schema` |
| 엄격 모드 | `strict: true` | `strict: true` |
| 병렬 호출 | 지원 | 지원 |
| 내장 도구 | web_search, file_search, computer_use, code_interpreter | computer_use (별도 API) |
| MCP 지원 | Responses API 내장 | 네이티브 MCP 클라이언트 |
| 스펙 기반 | JSON Schema | JSON Schema |

---

## 5. AGENTS.md - 에이전트를 위한 README {#agentsmd}

### 뭔가요?

[AGENTS.md 공식 사이트](https://agents.md/)에서는 이렇게 설명해요:

> "AGENTS.md is a simple, universal standard that gives AI coding agents a consistent source of project-specific guidance needed to operate reliably across different repositories and toolchains."

쉽게 말하면, 코드베이스에 `README.md`가 있듯이 AI 에이전트를 위한 `AGENTS.md`를 만드는 거예요.

예를 들어:

```markdown
# AGENTS.md

## Build & Test
- 빌드: `npm run build`
- 테스트: `npm test` (PR 전 필수 실행)
- 린트: `npm run lint --fix`

## 코딩 컨벤션
- TypeScript strict mode 사용
- 함수 주석은 한국어로 작성
- 커밋 메시지는 Conventional Commits 형식

## 금지 사항
- `node_modules/` 직접 수정 금지
- `.env` 파일 커밋 금지
```

이걸 저장소에 두면 Copilot, Cursor, Claude Code, Devin 같은 AI 코딩 에이전트들이 자동으로 읽고 프로젝트 컨벤션을 따르게 돼요.

### 채택 현황

[OpenAI가 2025년 8월 공개](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)한 이후:
- **6만 개 이상**의 오픈소스 프로젝트 채택
- 지원 도구: Amp, Codex, Cursor, Devin, Factory, Gemini CLI, GitHub Copilot, Jules, VS Code

2025년 12월 AAIF에 기부되어 현재 Linux Foundation 중립 거버넌스 하에 운영 중이에요.

### AGENTS.md가 왜 중요한가요?

에이전트가 점점 더 많은 코드를 작성하는 시대에, 에이전트가 저장소의 규칙을 이해하지 못하면 엉뚱한 코드를 만들죠. `AGENTS.md`는 그 문제를 해결하는 단순하지만 강력한 방법이에요.

---

## 6. 기타 프레임워크 프로토콜 {#frameworks}

### LangChain / LangGraph

[LangGraph v1.0이 2025년 말 출시](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared)되면서 LangChain 에이전트의 기본 런타임이 됐어요.

LangChain의 도구 프로토콜:

```python
from langchain.tools import tool
from pydantic import BaseModel, Field

class SearchInput(BaseModel):
    query: str = Field(description="검색할 쿼리")

@tool("web_search", args_schema=SearchInput)
def web_search(query: str) -> str:
    """웹에서 정보를 검색합니다."""
    return f"검색 결과: {query}"
```

LangChain은 2025년부터 MCP 서버를 도구로 직접 로드하는 기능을 공식 지원해요. MCP와 LangChain이 협력하는 구조죠.

### Microsoft AutoGen + Semantic Kernel → Microsoft Agent Framework

[2025년 10월, Microsoft가 AutoGen과 Semantic Kernel을 통합](https://cloudsummit.eu/blog/microsoft-agent-framework-production-ready-convergence-autogen-semantic-kernel)해 **Microsoft Agent Framework**로 합쳤어요. 1.0 GA 목표는 2026년 Q1이에요.

통합 프레임워크 특징:
- **AutoGen의 멀티에이전트 대화** 패턴
- **Semantic Kernel의 플러그인/스킬** 시스템
- MCP와 A2A 모두 지원

AutoGen의 에이전트 대화 패턴:

```python
import autogen

assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config={"model": "gpt-4o"}
)

user_proxy = autogen.UserProxyAgent(
    name="user",
    code_execution_config={"work_dir": "coding"}
)

# 에이전트들이 자율적으로 대화하며 작업 수행
user_proxy.initiate_chat(
    assistant,
    message="Python으로 피보나치 수열 구현해줘"
)
```

### Microsoft Copilot Studio의 에이전트 스킬(Skills)

[VS Code 1.108 업데이트](https://visualstudiomagazine.com/articles/2026/01/12/vs-code-december-2025-update-puts-ai-agent-skills-front-and-center.aspx)에서 실험적 Agent Skills 지원이 추가됐어요. 워크스페이스에 정의된 스킬을 에이전트가 온디맨드로 로드하는 방식이에요.

[Microsoft Copilot Studio](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/whats-new-in-copilot-studio-november-2025/)는 MCP와 A2A를 모두 지원하며, 에이전트가 Microsoft 365, Azure AI, Fabric 에이전트들과 협력할 수 있도록 해요.

---

## 7. 프로토콜 비교표 및 언제 뭘 써야 하나요? {#comparison}

### 핵심 비교표

[TrueFoundry의 상세 비교 분석](https://www.truefoundry.com/blog/mcp-vs-a2a)을 바탕으로 정리했어요:

| 항목 | MCP | A2A | Tool Use (OpenAI/Claude) | AGENTS.md |
|------|-----|-----|--------------------------|-----------|
| **목적** | 에이전트 ↔ 도구/데이터 연결 | 에이전트 ↔ 에이전트 협력 | LLM ↔ 함수 호출 | 저장소 맥락 공유 |
| **아키텍처** | Client-Server | Peer-to-Peer | Request-Response | 파일 기반 컨벤션 |
| **통신 방식** | JSON-RPC 2.0 (stdio/HTTP/SSE) | HTTP + SSE + JSON-RPC | REST API | 마크다운 파일 |
| **발견 방식** | 서버 목록/레지스트리 | Agent Card (JSON) | 명시적 도구 목록 | 저장소 루트 파일 |
| **상태 관리** | Stateful 연결 | 장기 태스크 생명주기 | 대화 컨텍스트 | N/A |
| **보안** | 도구/리소스 접근 제어 | 크로스에이전트 인증 | API 키 기반 | N/A |
| **주요 사용처** | IDE, 개발 도구, 엔터프라이즈 통합 | 멀티에이전트 오케스트레이션 | 싱글 에이전트 도구 사용 | AI 코딩 에이전트 |
| **거버넌스** | AAIF (Linux Foundation) | AAIF (Linux Foundation) | 각사 독자 | AAIF (Linux Foundation) |
| **성숙도** | 성숙 (v2025-11-25) | 성장 중 (v0.3) | 성숙 | 성장 중 |

### 언제 뭘 써야 하나요?

[auth0 블로그의 실용적 가이드](https://auth0.com/blog/mcp-vs-a2a/)와 [MCP vs A2A 완전 가이드](https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li)를 참고해서 정리했어요:

**MCP를 쓰세요, 만약:**
- 에이전트가 데이터베이스, API, 파일시스템 등 외부 도구/데이터에 접근해야 할 때
- 단일 에이전트가 다양한 서비스와 연동해야 할 때
- 도구 통합 코드를 줄이고 싶을 때
- IDE 플러그인, 개발 도구 만들 때

**A2A를 쓰세요, 만약:**
- 여러 전문화된 에이전트가 협력해야 할 때
- 에이전트들이 서로 다른 벤더/프레임워크로 만들어졌을 때
- 장기 실행 작업을 에이전트 간에 분산 처리할 때
- 엔터프라이즈 멀티에이전트 오케스트레이션 구축 시

**Tool Use (Function Calling)를 쓰세요, 만약:**
- 특정 LLM API(OpenAI, Claude)를 직접 사용할 때
- MCP 없이 간단한 도구 연결이 필요할 때
- 실시간 응답이 중요한 간단한 에이전트 구축 시

**AGENTS.md를 쓰세요:**
- AI 코딩 에이전트가 작업하는 모든 저장소에 항상!

**실전 아키텍처 (대부분의 엔터프라이즈):**

```
사용자 요청
    ↓
오케스트레이터 에이전트 (A2A로 다른 에이전트와 소통)
    ├── 리서치 에이전트 ──(MCP)──► 웹 검색 서버
    ├── 코드 에이전트   ──(MCP)──► 파일시스템 서버
    └── DB 에이전트    ──(MCP)──► 데이터베이스 서버
```

MCP와 A2A는 경쟁이 아니라 **상호 보완적**이에요.

---

## 8. Agentic AI Foundation (AAIF): 프로토콜 거버넌스의 미래 {#aaif}

### AAIF란?

[2025년 12월 9일, Linux Foundation이 AAIF(Agentic AI Foundation) 출범을 발표](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation)했어요. 이건 AI 프로토콜 역사에서 매우 중요한 사건이에요.

> "The formation of AAIF marks a pivotal moment in the evolution of AI agent standards, bringing together the world's leading technology companies under neutral governance."
> — Linux Foundation, 2025

**Platinum 멤버:**
AWS, Anthropic, Block, Bloomberg, Cloudflare, Google, Microsoft, OpenAI

**AAIF에 기부된 프로젝트들:**
1. **MCP** (Anthropic 기부) - 도구/데이터 연결 표준
2. **A2A** (Google 기부) - 에이전트 간 통신 표준
3. **AGENTS.md** (OpenAI 기부) - 코딩 에이전트 컨벤션 표준
4. **goose** (Block 기부) - AI 에이전트 런타임

### 왜 이게 중요한가요?

AI 역사상 처음으로 OpenAI, Anthropic, Google이 **같은 재단** 아래 협력하고 있어요. 이는:

1. **중립 거버넌스**: 어느 회사도 혼자 프로토콜을 좌우하지 못함
2. **표준화 가속**: 업계 전체가 동일한 표준을 사용
3. **벤더 락인 방지**: 기업들이 특정 AI 벤더에 종속되지 않음

[Anthropic의 공식 블로그](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation)에서는:

> "By donating MCP to the AAIF, we're ensuring that the protocol remains open, community-driven, and truly interoperable across the entire AI ecosystem."

---

## 9. 2026년 전망 및 결론 {#outlook}

### 2026년 주요 트렌드

**MCP 로드맵** ([getknit.dev 분석](https://www.getknit.dev/blog/the-future-of-mcp-roadmap-enhancements-and-whats-next)):
- OAuth 2.1 엔터프라이즈 SSO 통합
- MCP Registry "앱스토어" 출시 (서버 발견/신뢰 시스템)
- 멀티에이전트 오케스트레이션 기능 (계층적 에이전트 그래프)
- 멀티모달 지원 확장 (비디오, 오디오)
- Java, Go, Rust SDK 추가

**시장 전망** ([solo.io AAIF 분석](https://www.solo.io/blog/aaif-announcement-agentgateway)):
- Gartner: 2026년 말까지 기업 애플리케이션의 40%에 AI 에이전트 포함 (현재 5% 미만)
- 기업의 65%가 이미 에이전트 시스템 파일럿/배포 중
- 90%의 경영진이 2026년 에이전트 투자 확대 계획

**NIST AI 에이전트 표준화** (2026년 2월 17일 발표):
- NIST AI Agent Standards Initiative 설립
- 3개 축: 산업 주도 표준, 오픈소스 프로토콜 개발, 에이전트 보안 연구

### 결론: 프로토콜 전쟁은 끝났다

[2026 AI 프로토콜 전쟁 분석](https://www.hungyichen.com/en/insights/ai-agent-protocol-wars)에서 이렇게 정리해요:

> "The protocol wars are settling into a clear hierarchy: MCP owns the vertical integration layer (agent-to-tool), A2A is establishing the horizontal collaboration layer (agent-to-agent), and AGENTS.md defines the behavioral contract layer (agent-to-codebase)."

각 프로토콜이 자기 레이어를 담당하는 구조로 정착되고 있어요:

```
┌─────────────────────────────────────────────────────────┐
│              AI 프로토콜 생태계 스택 (2026)                │
├─────────────────────────────────────────────────────────┤
│  AGENTS.md          │  에이전트 행동 컨벤션 레이어          │
├─────────────────────────────────────────────────────────┤
│  A2A                │  에이전트 ↔ 에이전트 수평 레이어      │
├─────────────────────────────────────────────────────────┤
│  MCP                │  에이전트 ↔ 도구/데이터 수직 레이어   │
├─────────────────────────────────────────────────────────┤
│  Tool Use (Function Calling)  │  LLM ↔ 함수 기본 레이어  │
└─────────────────────────────────────────────────────────┘
```

AI 에이전트 생태계는 이 4개 레이어가 **레고 블록처럼 조합**되는 방향으로 가고 있어요. 어느 하나만 배우는 게 아니라, 이 생태계 전체를 이해하는 게 2026년 AI 개발자에게 필수 역량이 됐어요.

여러분이 만드는 에이전트가 혼자 일하는 에이전트든, 팀을 이루는 에이전트든, 이제 표준 언어가 생겼어요. 그 언어를 잘 배워두면 AI 생태계 어디서나 통하는 개발자가 될 수 있을 거예요. 화이팅!

---

## 참고문헌

| # | 제목 | 출처 |
|---|------|------|
| 1 | [Introducing the Model Context Protocol](https://www.anthropic.com/news/model-context-protocol) | Anthropic |
| 2 | [MCP Specification 2025-11-25](https://modelcontextprotocol.io/specification/2025-11-25) | modelcontextprotocol.io |
| 3 | [Announcing the Agent2Agent Protocol (A2A)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/) | Google Developers Blog |
| 4 | [A2A Protocol Official Site](https://a2a-protocol.org/latest/) | a2a-protocol.org |
| 5 | [What Is Agent2Agent Protocol?](https://www.ibm.com/think/topics/agent2agent-protocol) | IBM |
| 6 | [MCP vs A2A: Key Differences](https://www.truefoundry.com/blog/mcp-vs-a2a) | TrueFoundry |
| 7 | [MCP vs A2A: Complete Guide 2026](https://dev.to/pockit_tools/mcp-vs-a2a-the-complete-guide-to-ai-agent-protocols-in-2026-30li) | DEV Community |
| 8 | [Why the Model Context Protocol Won](https://thenewstack.io/why-the-model-context-protocol-won/) | The New Stack |
| 9 | [A Year of MCP: 2025 Review](https://www.pento.ai/blog/a-year-of-mcp-2025-review) | Pento |
| 10 | [Linux Foundation AAIF Announcement](https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation) | Linux Foundation |
| 11 | [OpenAI co-founds AAIF](https://openai.com/index/agentic-ai-foundation/) | OpenAI |
| 12 | [AGENTS.md Official Site](https://agents.md/) | agents.md |
| 13 | [Tool use with Claude](https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview) | Anthropic Docs |
| 14 | [New tools in Responses API](https://openai.com/index/new-tools-and-features-in-the-responses-api/) | OpenAI |
| 15 | [Donating MCP to AAIF](https://www.anthropic.com/news/donating-the-model-context-protocol-and-establishing-of-the-agentic-ai-foundation) | Anthropic |
| 16 | [The Future of MCP: Roadmap](https://www.getknit.dev/blog/the-future-of-mcp-roadmap-enhancements-and-whats-next) | getknit.dev |
| 17 | [AAIF Changes Everything for MCP](https://www.solo.io/blog/aaif-announcement-agentgateway) | Solo.io |
| 18 | [VS Code December 2025: Agent Skills](https://visualstudiomagazine.com/articles/2026/01/12/vs-code-december-2025-update-puts-ai-agent-skills-front-and-center.aspx) | Visual Studio Magazine |
| 19 | [Copilot Studio November 2025](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/whats-new-in-copilot-studio-november-2025/) | Microsoft |
| 20 | [Microsoft Agent Framework](https://cloudsummit.eu/blog/microsoft-agent-framework-production-ready-convergence-autogen-semantic-kernel) | Cloud Summit |
| 21 | [MCP vs A2A: auth0 Guide](https://auth0.com/blog/mcp-vs-a2a/) | Auth0 |
| 22 | [2026 AI Protocol Wars](https://www.hungyichen.com/en/insights/ai-agent-protocol-wars) | Prof. Hung-Yi Chen |
| 23 | [2026: Enterprise-Ready MCP](https://www.cdata.com/blog/2026-year-enterprise-ready-mcp-adoption) | CData |
| 24 | [A2A Protocol Upgrade](https://cloud.google.com/blog/products/ai-machine-learning/agent2agent-protocol-is-getting-an-upgrade) | Google Cloud Blog |
| 25 | [Open Source AI Agent Frameworks 2026](https://openagents.org/blog/posts/2026-02-23-open-source-ai-agent-frameworks-compared) | OpenAgents |
