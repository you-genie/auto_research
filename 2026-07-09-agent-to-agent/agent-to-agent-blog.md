---
layout: post
title: "Agent-to-Agent(A2A) 통합 리서치: '그냥 agent를 tool처럼 부르는 것'과 진짜 A2A는 무엇이 다른가"
date: 2026-07-09
categories: [research, ai-agents]
tags: [a2a, agent-to-agent, tool-calling, mcp, multi-agent-system, google-a2a, openai-agents-sdk, claude-agent-sdk, autogen, crewai, langgraph, bedrock, agentforce]
---

# Agent-to-Agent(A2A) 통합 리서치

> **핵심 질문**: 요즘 "multi-agent"라고 불리는 것 대부분은 사실 "agent API를 그냥 tool처럼 감싼 것"이다. 다른 agent에 요청 던지고 응답 받고 끝 — 이건 tool calling과 실질적으로 아무 차이가 없다. **이걸 넘어서는 "진짜 A2A"는 무엇이고, 언제 필요한가?** 이 리포트는 이 질문에 답한다.

---

## 0. 리포트를 관통하는 3단 대조 프레임

기존 논의는 흔히 **(1) tool call vs (2) A2A** 라는 이분법을 쓴다. 이 프레임은 실무의 절반을 놓친다. 왜냐하면 시장에 나온 대부분의 "multi-agent 프레임워크"는 실질적으로 **(2) agent API를 tool처럼 호출하는 RPC-agent** 층에 머무르고, 진짜 자율·비동기·negotiable 협업인 **(3)** 은 소수만 도달했기 때문이다. 이 리포트는 세 층을 명시적으로 분리해 프레임을 세운다.

| 축 | **(1) 일반 Tool Call** | **(2) Agent API를 tool처럼 호출 (RPC-agent)** | **(3) 진짜 A2A** |
|---|---|---|---|
| **세션** | one-shot | one-shot (agent가 매번 clean slate) | 장기 세션·task lifecycle |
| **상태** | stateless | 상대 agent도 사실상 stateless로 취급 | callee가 state·목표·memory 유지 |
| **통신 방향** | 요청→응답 | 요청→응답 | 양방향, callee가 clarification·역제안 가능 |
| **자율성** | 지시대로 실행 | 결과만 반환 (거절 없음) | callee가 accept / reject / renegotiate |
| **인터페이스 계약** | 고정 JSON schema | 고정 endpoint 스펙 (사설 API) | AgentCard·capability advertisement로 협의 |
| **프로토콜 상태** | 없음 | HTTP 요청-응답만 | task/state 머신 (submitted→working→input-required→completed 등) |
| **병렬성** | sync | sync (또는 streaming) | async, streaming, push notification |
| **정체성·신뢰** | 소유 관계 | API key | 상호 DID / mTLS / OAuth / 평판 |
| **오류 처리** | retry | retry | negotiation, alternative proposal, `rejected` 상태 |
| **관측·감사** | tool log | tool log | multi-turn conversation trace + artifact provenance |
| **경계** | 프로세스 내부 | 조직 내부 API | **조직 간 계약 표면** |

### 왜 (2)가 위험한 함정인가

(2)는 tool call과 프로토콜 레벨에서 구분 불가능하다. HTTP endpoint 뒤에 함수가 있든 LLM agent가 있든 호출자 입장에선 똑같이 "요청 → JSON 응답"이다. 그런데 **agent라는 이름을 붙이는 순간 사람들은 자율성·기억·협업을 기대**한다. 이 gap이 실무에서 실패의 주 원인이다.

- CrewAI의 `hierarchical` 모드가 manager LLM 판단에 의존해 비결정성·디버깅 난이도가 폭증한다는 커뮤니티 교훈, LangGraph supervisor의 boilerplate, AutoGen의 계약 없는 group chat 실패 사례 모두 이 지점에서 발생한다.
- Anthropic Multi-Agent Research System의 핵심 교훈이 정확히 이 지점이다: **"subagent 간 isolation boundary를 크게 두고 tool call처럼 취급했을 때가 실제로 잘 동작했다"** ([Anthropic 2025](https://www.anthropic.com/engineering/multi-agent-research-system)).

즉 **(2)에 머물 거면 처음부터 tool call로 설계하는 게 정직**하고, **자율성·negotiation·cross-org identity가 필요하면 (3)까지 가야 한다**. 그 중간에서 "agent 이름만 붙인 tool"에 정치적 자율성을 기대하는 것이 가장 흔한 실수다.

### 실무자용 판정 가이드

| 시나리오 | 필요 층 |
|---|---|
| 다른 벤더/조직의 agent와 상호운용 | **(3) 필요** |
| 팀 내 여러 agent가 같은 프레임워크에서 협업 | **(2)로 충분** |
| 장기 task (수 시간~며칠 걸리는 위임) | **(3) 필요** |
| 짧은 handoff (5초짜리 서브태스크) | **(1)-(2)로 충분** |
| Cross-org 신원·감사·규제 대응 | **(3) 필요** |
| Callee가 조건부 거절·역제안을 해야 하는 워크플로 | **(3) 필요** |
| 결과만 필요한 사내 병렬 리서치 | **(2)로 충분, isolation 크게** |
| Callee가 다시 다른 agent에 재위임하는 계층 협업 | **(3) 강력 권고** |
| 결정론적 파이프라인 | **(1) tool call, 오히려 agent를 빼는 게 정답** |

---

## 1. Google Agent2Agent (A2A) Protocol — (3)의 표준 후보

Google이 2025년 4월 Cloud Next에서 발표하고 6월 Linux Foundation에 이관한 A2A 프로토콜은 현시점 (3)의 사실상 표준 후보다. 왜 이게 (3)에 해당하는지 스펙 근거로 짚는다.

### 1.1 왜 (3)인가 — 스펙 primitive가 (2)로는 표현 불가능

- **Agent Card (`/.well-known/agent-card.json`)** — capability advertisement. 함수 시그니처가 아니라 skill 이름·설명·예시·입출력 modality·인증 요구사항을 광고 → **(2)의 "고정 endpoint 스펙"과 달리 협의 가능한 계약**.
- **Task 상태 머신** — `submitted → working → {input-required | auth-required} → {completed | canceled | failed | rejected}`. `input-required`는 callee가 되묻는 상태, `rejected`는 위임 자체를 거절하는 상태. **(2)엔 개념적으로 존재하지 않는 primitive**.
- **Artifact + SSE streaming** — 최종/중간 산출물을 incremental streaming으로 전달. Long-running task를 first-class로 다룸.
- **Push notification (webhook)** — Client가 연결을 유지하지 못하는 몇 시간~며칠 task 지원.
- **"Opaque agent" 원칙** — 공식 저장소 정의: *"open protocol enabling communication and interoperability between opaque agentic applications"* ([a2aproject/A2A](https://github.com/a2aproject/A2A)). 상대 agent의 prompt·모델·tool chain을 알 필요도, 알아서도 안 됨. **AgentCard와 Task lifecycle만이 계약 표면** — 이것이 (3)을 (2)와 구분짓는 결정적 원칙이다.

### 1.2 통신 메커니즘

- **Transport**: JSON-RPC 2.0 over HTTPS. v0.3부터 gRPC/REST 바인딩 추가.
- **주요 메서드**: `message/send`, `message/stream`, `tasks/get`, `tasks/cancel`, `tasks/pushNotificationConfig/set`, `tasks/resubscribe`.
- **인증**: OpenAPI 스타일 `securitySchemes` — apiKey / HTTP Bearer / OAuth2 / OIDC / mTLS.
- **상태 유지**: Task ID 기반. 모든 후속 message는 `taskId` 참조.

### 1.3 거버넌스와 채택

- 2025-04-09 Google Cloud Next 발표, 초기 50+ 파트너.
- 2025-06-23 **Linux Foundation Agent2Agent Protocol Project**로 이관. Founding members: AWS, Cisco, Google, Microsoft, Salesforce, SAP, ServiceNow ([LF press](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)).
- 2025-08 IBM ACP가 A2A로 흡수 ([Zuplo](https://zuplo.com/blog/agent-protocol-stack-mcp-a2a-acp-2026)).
- 2026-04 1주년: 150+ 프로덕션 조직, 5개 언어 SDK (Python/JS/Java/Go/.NET), GitHub star 22,000+ ([LF 1주년 press](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)).

### 1.4 Agent Card 예시

```json
{
  "protocolVersion": "0.3.0",
  "name": "Weather Agent",
  "description": "Provides current weather and forecasts.",
  "url": "https://weather-agent.example.com/",
  "version": "1.0.0",
  "capabilities": {
    "streaming": true,
    "pushNotifications": true,
    "stateTransitionHistory": true
  },
  "defaultInputModes": ["text/plain"],
  "defaultOutputModes": ["text/plain", "application/json"],
  "securitySchemes": {
    "oauth2": {
      "type": "oauth2",
      "flows": { "authorizationCode": { "authorizationUrl": "...", "tokenUrl": "...", "scopes": {"weather.read": "Read weather"} } }
    }
  },
  "skills": [{
    "id": "get_current_weather",
    "name": "Get Current Weather",
    "description": "Return current weather for a given city",
    "tags": ["weather", "forecast"],
    "examples": ["What's the weather in Seoul?"],
    "inputModes": ["text/plain"],
    "outputModes": ["application/json"]
  }]
}
```

### 1.5 한계

- 아직 프로덕션 트래픽 벤치마크 부족. 자체 프로토콜 성숙도는 v0.3까지 왔지만 audit/governance는 [arXiv 2606.31498](https://arxiv.org/html/2606.31498v1)에서 지적하듯 미성숙.
- **AAIF (Agent-to-Agent Interoperability Framework)** 라는 대체 청사진이 2025-12에 부상 ([Blocks & Files](https://blocksandfiles.com/2025/12/11/a2a-aaif-ai-agents/)) — sole standard 지위는 확정 아님. *확인 필요*.

---

## 2. 상용 SDK 매핑 — 대부분은 (2), 진짜 (3)까지 간 곳은 소수

각 SDK를 3단 프레임으로 판정한다.

### 2.1 Anthropic MCP + Claude Agent SDK — **(1)–(2) 경계**

- **MCP**는 명시적으로 "agent ↔ tool" 프로토콜 → **(1)**. Server가 tools/resources/prompts를 노출하고 client가 스키마 기반으로 호출.
- **Claude Agent SDK의 `Task` (Agent) tool**은 subagent 스폰. Subagent는 자체 격리 컨텍스트에서 loop를 돌고 요약만 반환 → **(2)** (표면은 tool call, 의미론은 위임).
- Sub-agent가 자기 subagent를 스폰할 수 없어 (재귀 방지) 계층 협업이 얕음. Task lifecycle·rejected 같은 (3)의 primitive는 부재.
- Google A2A 프로토콜 네이티브 지원은 SDK 레벨에서 확인되지 않음. *확인 필요*. 다만 2025-12 Linux Foundation Agentic AI Foundation에 Anthropic·Google 공동 창립사로 합류 → MCP와 A2A가 같은 governance 아래.
- **판정**: Anthropic 스택은 (1)–(2)를 명확히 다루고, (3)에는 아직 표준 프로토콜 연결이 없다. 사내 병렬 리서치 시나리오처럼 **isolation을 크게 둔 (2)** 에 최적화.

Sources: [Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview), [Building agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk), [TrueFoundry MCP vs A2A](https://www.truefoundry.com/blog/mcp-vs-a2a).

### 2.2 OpenAI Agents SDK — **거의 (2), 부분적 (3) 요소**

- **`handoffs=[...]` 필드**는 내부적으로 `transfer_to_<agent>` 형태의 tool call로 표현. 대화 전체 히스토리를 새 agent가 이어받아 loop 소유 → 같은 프로세스 안에서 context가 넘어감.
- **Agent-as-tool (`.as_tool()`)** — 서브 agent를 매니저의 tool로 노출. 완전한 (2) 패턴.
- **왜 A2A인지 애매한가**: handoff가 다른 벤더 agent나 별도 조직의 agent와 대화하는 게 아니라 **같은 SDK, 같은 프로세스, 같은 신원**의 agent 간 컨텍스트 전달. 즉 프로토콜적으로는 (2)에 가깝지만, 대화 히스토리를 넘긴다는 점에서 "함수 반환값 이상"의 상태 이전이 일어나 (3)의 그림자가 있음.
- Google A2A protocol 네이티브 지원은 미확인 (Linux Foundation Agentic AI Foundation 창립사).
- **판정**: 팀 내 여러 agent가 같은 프레임워크에서 협업하는 시나리오에는 이상적. Cross-vendor·cross-org이 필요하면 별도 A2A 어댑터 필요.

Sources: [Handoffs docs](https://openai.github.io/openai-agents-python/handoffs/), [Agent orchestration docs](https://openai.github.io/openai-agents-python/multi_agent/).

### 2.3 Microsoft Agent Framework + Copilot Studio — **네이티브 (3) 도달**

- **Microsoft Agent Framework** (AutoGen + Semantic Kernel 통합, 2026-04 1.0 GA): graph 기반 workflow + sequential/concurrent/handoff/group chat/Magentic-One 오케스트레이션 패턴.
- **Copilot Studio**: **A2A protocol 네이티브 지원**. 외부 A2A agent를 커넥터처럼 추가 가능 ([Learn — Add A2A agent](https://learn.microsoft.com/en-us/microsoft-copilot-studio/add-agent-agent-to-agent)). **Entra Agent ID**로 agent에 독립 신원 부여 → (3)의 identity 요건 충족.
- **MCP GA** in Copilot Studio ([MCP GA blog](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/)).
- **판정**: 프로토콜 지원과 신원 인프라 양쪽을 갖춰 사실상 (3) 도달. Enterprise (특히 M365 stack) 에서 cross-org agent 연동을 원하면 현 시점 가장 성숙.

Sources: [MS Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/), [Agent Framework 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/), [Ignite 2025 blog](https://www.microsoft.com/en-us/microsoft-365/blog/2025/11/18/microsoft-ignite-2025-copilot-and-agents-built-to-power-the-frontier-firm/).

### 2.4 CrewAI — **(2) + 얼마간의 (3) 요소**

- **Crew / Agent / Task** role 모델. `Process.sequential`(정적 파이프라인) vs `Process.hierarchical`(manager agent가 delegation).
- `allow_delegation=True` 정책 레이어로 위임 가능 여부 제어 → 2026 기준 기본 disabled로 바뀜.
- **왜 완전한 (3)이 아닌가**: 프로토콜 개방성 없음, 다른 벤더 agent와 통신 불가, task state 머신 부재. Role delegation은 자연어 프롬프트로만 표현되어 명시적 lifecycle 없음.
- **판정**: 팀 시뮬레이션 시나리오 (역할 기반 협업)에는 강점. 프로덕션에서는 sequential 권장, hierarchical은 비결정성으로 디버깅 지옥 경계.

Sources: [Hierarchical Process](https://docs.crewai.com/en/learn/hierarchical-process), [Why CrewAI Manager-Worker Fails](https://towardsdatascience.com/why-crewais-manager-worker-architecture-fails-and-how-to-fix-it/).

### 2.5 LangGraph — **(2) 중심, 어댑터로 (3) 확장 가능**

- **State graph의 node = agent**. `langgraph-supervisor`(중앙 라우팅), `langgraph-swarm`(peer-to-peer handoff).
- Handoff tool의 반환값이 `Command(goto=..., graph=Command.PARENT)`라는 특수 객체 → 그래프 엔진이 노드 전환으로 해석. **tool과 A2A의 구분이 반환 타입에 있음**.
- 같은 프로세스 안에서 state를 공유하므로 프로토콜적으로는 (2). LangChain이 A2A 초기 파트너사인 만큼 별도 어댑터로 (3) 확장 가능 (*확인 필요*).
- **판정**: 그래프 명시성으로 디버깅·시각화 유리. 사내 협업 (2) 에는 최적, cross-org (3)엔 어댑터 필요.

Sources: [langgraph_supervisor](https://reference.langchain.com/python/langgraph-supervisor), [langgraph_swarm](https://reference.langchain.com/python/langgraph-swarm).

### 2.6 smolagents (HuggingFace) — **(1)–(2) 경계, 가장 흐릿**

- `managed_agents=[...]` 파라미터로 매니저 agent가 서브 agent 호출. CodeAct 스타일이라 모든 액션이 Python 코드로 표현되어 **서브 agent도 결국 함수 호출로 포섭**된다.
- A2A protocol 미지원.
- **판정**: <1000 LoC의 극단적 단순성 + 코드 액션 표현력이 매력. 하지만 (2)의 형식적 표현만 있고 세션·negotiation은 없음.

Sources: [smolagents docs](https://huggingface.co/docs/smolagents/en/index).

### 2.7 Mastra (TypeScript) — **(2) with 3계층 분리**

- **Workflow / Agent / Tool 3계층 분리**가 명시적. Agent는 자체 loop 주체, Tool은 stateless 함수, Workflow는 흐름 제어자.
- suspend/resume 지원 (human-in-the-loop). Google A2A 프로토콜 지원은 미확인.
- **판정**: TypeScript·Next.js 통합 강점. 개념 분리가 SDK 중 가장 깔끔한 편.

### 2.8 Pydantic AI — **(2)에 가깝지만 명시적 이중 패턴**

- **Agent delegation** (부모 tool 안에서 자식 agent 호출, 결과 반환 후 부모 재개) vs **Programmatic hand-off** (애플리케이션 코드가 다음 agent 결정).
- Delegation은 "tool 안에 agent가 들어있는" 형태 → tool call의 특수 케이스. `ctx.usage` 전파로 부모 usage에 합산.
- A2A protocol 이슈 오픈되어 있으나 미지원. *확인 필요*.

Sources: [Multi-Agent Patterns](https://pydantic.dev/docs/ai/guides/multi-agent-applications/), [Issue #1978](https://github.com/pydantic/pydantic-ai/issues/1978).

### 2.9 LlamaIndex AgentWorkflow / Haystack

- **LlamaIndex**: `can_handoff_to=[...]`로 handoff. Handoff tool 호출이 워크플로우 노드 전환. (2)의 표현력 좋음.
- **Haystack**: **Agent를 `ComponentTool`로 래핑** → A2A를 tool의 특수 케이스로 완전 흡수. 가장 (1)–(2) 경계에 있음.

### 2.10 SDK 판정 요약 표

| SDK | A2A primitive | 판정 | Google A2A protocol |
|---|---|---|---|
| Anthropic Claude Agent SDK | `Task`/Agent tool → subagent | **(1)–(2) 경계** | 미확인 |
| OpenAI Agents SDK | `handoffs=` + `agent.as_tool()` | **거의 (2), 부분 (3)** | 미확인 |
| Microsoft Agent Framework | GroupChat / Handoff / Magentic-One | **네이티브 (3)** | ✅ 지원 |
| CrewAI | Hierarchical + `allow_delegation` | **(2) + α** | 미확인 |
| LangGraph | Supervisor / Swarm | **(2), 어댑터로 (3)** | 어댑터 존재 (*확인 필요*) |
| smolagents | `managed_agents=` | **(1)–(2) 경계** | 미지원 |
| Mastra | Workflow steps + agent-in-tool | **(2) with 3계층** | 미확인 |
| Pydantic AI | Agent delegation + hand-off | **(2)** | 이슈만 |
| LlamaIndex AgentWorkflow | `can_handoff_to=` | **(2)** | 미확인 |
| Haystack | Agent-as-ComponentTool | **(1)–(2) 완전 흡수** | MCP 지원, A2A 미확인 |

---

## 3. 상용 서비스 — 하이퍼스케일러가 (3)에 진입 중

### 3.1 Salesforce Agentforce — **(3) 진입**

- **Atlas Reasoning Engine** (비동기 pub/sub, Planner+Action Selector+Reflection). Agent → Topic(≤15) → Action(≤15) → Flow/Apex 계층.
- **A2A**: Salesforce가 Agent Card 개념을 기여, Multi-Agent Orchestration Summer '26 GA. **MCP**: Agentforce 3에서 네이티브 지원.
- 통합 패턴을 **API / MCP / A2A** 세 층으로 명시 분리 안내 ([Salesforce blog](https://www.salesforce.com/blog/how-to-choose-integration-pattern-for-agentforce/)).
- **판정**: 계약 표면(A2A protocol) + 신원(CRM 계정 연계) + task lifecycle 모두 갖춤. Cross-org 시나리오는 아직 초기지만 (3)에 도달.

### 3.2 Microsoft Copilot Studio — **네이티브 (3)**

- **Connected Agents** (진짜 A2A 위임): 부모 agent가 독립 자식 agent 호출. Entra Agent ID로 독립 신원.
- MCP GA, A2A Preview→GA 진행. Foundry Agent Service Multi-Agent Workflows (Public Preview).
- **판정**: 프로토콜 + 신원 + 관측 인프라 완비. M365 스택 전제라면 현재 가장 성숙한 (3) 스택.

### 3.3 ServiceNow AI Agent Fabric — **가장 명료한 (3)**

- **3계층 실행 모델** — Workflow (결정론적) / Skill (GenAI 단일 태스크) / AI Agent (자율 추론). Skill = tool, Agent = A2A.
- A2A **Primary(client) + Secondary(server) 양방향** 지원. JSON-RPC 2.0 over HTTPS, OAuth 2.0 Client Credentials. A2A Linux Foundation TSC 멤버.
- MCP: Client + Server 양쪽, Streamable HTTP + OAuth 2.1.
- **판정**: (1)/(2)/(3)의 개념 분리가 스펙 수준에서 가장 뚜렷. Enterprise ITSM 도메인의 참고 표준.

Sources: [ServiceNow Community MCP+A2A FAQ](https://www.servicenow.com/community/now-assist-articles/enable-mcp-and-a2a-for-your-agentic-workflows-with-faqs-updated/ta-p/3373907).

### 3.4 AWS Bedrock Agents + AgentCore — **자체 협업은 (2), AgentCore Runtime의 A2A 지원으로 (3) 진입**

- **Bedrock Multi-Agent Collaboration** (2025-03 GA): Supervisor / Supervisor-with-routing 2종. `collaborator_name`, `collaboration_instruction`, `relay_conversation_history` 필드로 sub-agent 등록. **프로토콜 개방성 없음, 사설 계약** → **(2)** 에 해당.
- **AgentCore** (2025-10 GA): Runtime(최대 8시간 세션·session isolation·VPC), Memory, Gateway(Lambda/OpenAPI/MCP→tool 변환), Identity(OAuth·delegated identity), Observability.
- **A2A 네이티브 지원 2025-11 발표** ([블로그](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)) — Strands, Google ADK, OpenAI SDK 등 크로스 프레임워크 상호운용.
- **판정**: Bedrock Agents 자체의 협업은 여전히 (2)지만, AgentCore Runtime을 A2A 엔드포인트로 노출하는 경로가 열리면서 프로덕션 (3) 진입 가능.

### 3.5 Google Cloud Vertex AI / ADK / Agent Engine — **표준 제정자 (3)**

- 3층: A2A(오픈 프로토콜) / ADK(오픈소스 SDK) / Agent Engine(관리형 런타임).
- ADK Python 1.0.0 GA(2025-05), `to_a2a()` 헬퍼로 ADK agent에서 Agent Card 자동 생성 + `/.well-known/agent-card.json` 노출 + Cloud Run 배포.
- **판정**: A2A 표준 그 자체. 다만 프로덕션 case study 정량 데이터는 *확인 필요*.

Sources: [Convert ADK agents for A2A](https://cloud.google.com/blog/products/ai-machine-learning/unlock-ai-agent-collaboration-convert-adk-agents-for-a2a).

### 3.6 IBM watsonx Orchestrate — **하이브리드**

- **Skill vs Agent 이중 계약**: Skill = 단일 원자 액션 (OpenAPI), AI Agent = 자율 추론.
- MCP(ADK v1.13+), A2A(외부 A2A agent를 컬래버레이터로 등록), ACP(BeeAI 발, LF 이관, A2A로 흡수 흐름).
- **판정**: 개념 분리는 명료하나 세 프로토콜 병존이 프로덕션 복잡도 증가 요인.

### 3.7 Zapier Agents / NVIDIA NeMo Agent Toolkit / Cohere North / HubSpot Breeze — 요약

| 플랫폼 | 판정 | 비고 |
|---|---|---|
| **Zapier Agents** | (2) | agent-to-agent 오케스트레이션 도입(2025-08), MCP GA, A2A 공식 구현 *확인 필요* |
| **NVIDIA NeMo Agent Toolkit** | (2)+(3) 하이브리드 | "everything is Function" 통일, A2A 클라이언트/서버 양방향 |
| **Cohere Command / North** | (1)–(2) | 단일 agent 내부 tool orchestration 중심 |
| **HubSpot Breeze** | (1)–(2) | vertical siloed, A2A 미지원 |

### 3.8 상용 서비스 판정 대조 표

| 플랫폼 | 자체 프로토콜 | Google A2A | MCP | 판정 |
|---|---|---|---|---|
| Salesforce Agentforce | Atlas + Topic/Action | ✅ Agent Card 기여, Summer '26 GA | ✅ 네이티브 | **(3) 진입** |
| MS Copilot Studio | Connected Agents | ✅ Preview→GA | ✅ GA | **네이티브 (3)** |
| ServiceNow AI Agent Fabric | Group-Action Framework | ✅ 양방향 (TSC) | ✅ 양방향 | **가장 명료한 (3)** |
| AWS Bedrock + AgentCore | Supervisor+Collaborator | ✅ 2025-11 네이티브 | ✅ Gateway | Bedrock=**(2)**, AgentCore=**(3)** |
| Google Vertex/ADK | A2A 자체 발명 | ✅ 표준 제정자 | ✅ ADK 내장 | **표준 (3)** |
| IBM watsonx Orchestrate | Skill+Agent + BeeAI | ✅ ADK 경유 | ✅ ADK v1.13+ | 하이브리드 |
| Zapier Agents | Pods | ⚠️ *확인 필요* | ✅ 2025-03 GA | **(2)** |
| NVIDIA NeMo Agent Toolkit | YAML Function | ✅ 양방향 | ✅ FastMCP | (2)+(3) |
| Cohere Command/North | 단일 agent | ⚠️ 파트너 등재만 | ✅ | **(1)–(2)** |
| HubSpot Breeze | Context Layer | ❌ 미지원 | ✅ | **(1)–(2)** |

---

## 4. 오픈소스 프로토콜 — Google A2A 이외의 (3) 시도들

### 4.1 ANP (Agent Network Protocol) — 개방형 웹 지향
- OSS 커뮤니티 발, 3-layer(Identity/Encrypted → Meta-Protocol → Application). W3C DID 확장인 `did:wba` 채택 → **identity를 프로토콜에 강제**. A2A가 기업 간 interoperability에 초점이라면 ANP는 **인터넷 전체를 agent가 크롤 가능한 네트워크로**.

### 4.2 AITP (Agent Interaction & Transaction Protocol) — 결제 1급 시민
- NEAR AI. Threads / Transports / Capabilities 3-primitive. A2A가 결여한 **cross-trust-boundary transaction** (crypto 정산, 데이터 판매, 항공권 구매)을 스펙 목적으로 명시.

### 4.3 IBM ACP → A2A로 흡수 (2025-08)
- BeeAI 발, RESTful HTTP, 빌드타임 metadata embed → scale-to-zero discovery. 2026 기준 A2A로 사실상 흡수.

### 4.4 Cisco AGNTCY / SLIM — 인프라 스택
- 2025-07 Linux Foundation 이관, 65+ 기업. Directory + Identity + Observability + **SLIM (Secure Low-Latency Interactive Messaging)** — IETF draft, gRPC over HTTP/2·3 + MLS E2E 암호화. **A2A/MCP 위에 얹는 인프라 레이어**로 포지셔닝, 경쟁이 아닌 상보.

### 4.5 Agora (Oxford) — 메타 프로토콜
- arXiv [2410.11905](https://arxiv.org/abs/2410.11905). "Agent Communication Trilemma" (versatility·efficiency·portability) 해결. 자주 쓰는 통신은 routine, 드문 통신은 자연어, 중간은 **LLM이 즉석에서 Protocol Document를 생성**해 협상 후 routine으로 저장. **primitive를 런타임에 만들어냄** — A2A와 정반대 지향.

### 4.6 NLIP (Natural Language Interaction Protocol) — Ecma 표준
- Ecma TC-56, 2025-12 ECMA-430/431/432 승인. 자연어 프롬프트를 1급 메시지 포맷으로. WebSocket + CBOR. human↔agent와 agent↔agent를 동일 포맷으로.

### 4.7 AGP (Agent Gateway Protocol) — Solo.io
- 2025-08 Linux Foundation 기부. A2A의 flat mesh 위에 도메인 게이트웨이 + 정책 기반 라우팅. Istio가 서비스 메시에서 하는 역할을 agent mesh에서 담당.

### 4.8 Crypto 궤도 — Fetch.ai uAgents / Olas / Virtuals ACP / Naptha
- 별도 궤도. 온체인 registry, DID, 결제 정산을 프로토콜에 내장. web2 표준이 방치한 영역에서 자율 진화.

### 4.9 프로토콜 지형 대조 표

| 프로토콜 | Discovery | 통신 계층 | vs Google A2A | 채택 |
|---|---|---|---|---|
| **ANP** | `.well-known` + DID:wba | HTTPS + JSON-LD | 개방형 웹·crawlable | 학술, 프로덕션 *확인 필요* |
| **AITP** | NEAR registry | Threads/Transports | 결제·거래 1급 | NEAR 생태계 |
| **ACP (IBM)** | Build-time metadata | HTTP REST | A2A로 흡수 | (은퇴) |
| **AGNTCY / SLIM** | Agent Directory | gRPC+MLS | A2A **위·아래** 레이어 | 65+ 기업, LF |
| **Agora** | 자동 협상 PD | 임의 | 프로토콜 자체를 LLM이 생성 | 프로토타입 |
| **NLIP** | 미정 | WebSocket+CBOR | 자연어 message-format 표준 | Ecma 승인 초기 |
| **AGP** | Capability table | Gateway proxy | A2A mesh 위 라우팅 | LF 프로젝트 |
| **Fetch.ai uAgents** | Almanac 온체인 | 자체 msg + Mailbox | crypto agent economy | Agentverse 프로덕션 |
| **Olas** | 온체인 NFT | Tendermint+ACN | crypto-economic security | DeFi/ML |
| **Virtuals ACP** | 온체인 | Base L2 | agent 상거래 특화 | crypto |

### 4.10 수렴 전망

2026년 시점 Linux Foundation 산하만 6개 프로토콜(A2A·MCP·ACP·AGNTCY·AGP·SLIM)이 병존한다. 두 흐름이 명확: (a) LF AAIF 산하에서 A2A·MCP가 "application/transport" vs "tool" 축을 나눠 갖는 **de facto 이원 표준**으로 굳는 방향, (b) crypto·decentralized 진영(AITP·Virtuals·Olas·ANP)이 identity·payment 영역에서 별도 궤도로 남는 방향. Agora·NLIP는 학술·공식 표준 실험이지만 인력 흡수력은 약함. 2027~2028년쯤 **"A2A + MCP + SLIM/AGP + DID-based identity"** 조합이 스택으로 굳고, ACP처럼 중복 스펙은 A2A profile로 재정의될 가능성이 높다.

---

## 5. 연구 논문 계보 — "Tool → Agent" 경계는 40년 전부터 있었다

### 5.1 Classic MAS (1980s–2000s)

Classic MAS가 이미 "tool call ≠ agent communication"이라는 구분을 40년 전에 못박았다. LLM 시대에 되살아난 것은 재발명이 아니라 **자율성이 실제로 가능해진 substrate 위에서 옛 이론이 유효화된 것**이다.

- **Contract Net Protocol** (Smith, 1980) — Manager가 task broadcast → Contractor가 bid → Manager가 award. 오늘날 오케스트레이터-서브에이전트 구조와 동일.
- **KQML** (Finin et al., 1994) — **Performative** 개념. 메시지는 데이터가 아니라 **행위**(ask-one, tell, achieve, subscribe). Tool call이 항상 `invoke(args)→return`인 반면, KQML은 의도를 인코딩. [Wikipedia](https://en.wikipedia.org/wiki/Knowledge_Query_and_Manipulation_Language).
- **FIPA ACL** (1996–) — Speech act 이론(Searle, Austin) 기반. `request`, `inform`, `propose`, `agree`, `refuse` 표준화. Contract Net·Iterated Contract Net·Subscribe/Notify interaction protocol 규격화. 2025 arxiv 서베이 [arXiv:2505.02279](https://arxiv.org/abs/2505.02279)가 지적하듯 오늘날 오픈 프로토콜 논의는 **FIPA를 사실상 재발명**하고 있다.

### 5.2 1세대 LLM Multi-Agent (2023) — 대화를 계산 substrate로

- **CAMEL** (Li et al., NeurIPS 2023, [arXiv:2303.17760](https://arxiv.org/abs/2303.17760)) — Role-playing + inception prompting. AI User와 AI Assistant 두 agent가 자율 대화로 task 완결. **호출자-피호출자 비대칭이 사라지고 대화가 산출물**.
- **AutoGen** (Wu et al., 2023, [arXiv:2308.08155](https://arxiv.org/abs/2308.08155)) — Microsoft. Conversable agent + programmable group chat. 함수 호출이 대화 message로 승격되고 다른 agent가 관찰·개입.
- **MetaGPT** (Hong et al., ICLR 2024, [arXiv:2308.00352](https://arxiv.org/abs/2308.00352)) — SOP를 프롬프트로 인코딩. PM/아키텍트/엔지니어/QA가 정형 문서(PRD, design doc, test)를 주고받음. FIPA ACL의 content language 규격화와 계보 이어짐.
- **ChatDev** (Qian et al., ACL 2024, [aclanthology 2024.acl-long.810](https://aclanthology.org/2024.acl-long.810/)) — 자연어(설계 논의)와 프로그래밍 언어(디버깅)를 채널 분리.
- **Multi-Agent Debate** (Du et al., [arXiv:2305.14325](https://arxiv.org/abs/2305.14325)) — 동일 task를 여러 LLM 인스턴스가 독립적으로 풀고 서로의 답을 비판·수렴.
- **Generative Agents / Smallville** (Park et al., [arXiv:2304.03442](https://arxiv.org/abs/2304.03442)) — Stanford 25명 sandbox agent, memory stream + reflection + planning으로 emergent social behavior.
- **AgentVerse** (Chen et al., [arXiv:2308.10848](https://arxiv.org/abs/2308.10848)) — Recruitment→decision→action→evaluation 4단계 협업.

### 5.3 2024–2026 계보 — 인프라화, 벤치마크, 실패 모드

- **LLM MAS Survey** ([arXiv:2402.01680](https://arxiv.org/abs/2402.01680), Guo et al.) — "How do agents communicate"를 별도 축으로 명시.
- **Multi-Agent Collaboration Mechanisms Survey** ([arXiv:2501.06322](https://arxiv.org/pdf/2501.06322)) — cooperation/competition/coopetition 분류.
- **MultiAgentBench / MARBLE** (Zhu et al., ACL 2025, [arXiv:2503.01935](https://arxiv.org/abs/2503.01935)) — 협업·경쟁 통합 벤치마크. Tool-use 벤치마크와의 차이는 **함수 성공률이 아니라 대화의 사회적 성공**을 잼.
- **Google A2A + arxiv 2505.02279** — MCP(tool 계층) ↔ A2A/ACP/ANP(agent 계층)를 명시적으로 층 분리.
- **Anthropic Multi-Agent Research System** (2025) — Orchestrator-worker (lead + 3–5 parallel subagents), 별도 citation pass. 비용 ≈ single chat의 15×. **핵심 발견: subagent isolation을 크게 두고 tool처럼 취급**한 게 답이었다. 코딩·디버깅처럼 dependency가 조밀한 도메인은 MAS 부적합.
- **Rogue Agent 방지** ([arXiv:2502.05986](https://arxiv.org/abs/2502.05986)) — 한 agent 오정보가 대화 전체 오염.

### 5.4 계보가 3단 프레임에 시사하는 것

Classic MAS의 speech-act가 이론상 (3)의 뿌리다. 하지만 프로덕션 성공 사례(Anthropic Research System)는 정확히 반대로 **(2)로 후퇴할수록 성능-비용 곡선이 살아난다**는 것을 증명했다. 즉 **(3)의 언어는 옳지만, 오늘의 엔지니어링은 CNP + parallel tool call**로 수렴 중. 계보의 최전선은 "**어디까지 (2)로 밀고, 어디부터 (3)의 프로토콜적 자율성이 필요한가**"의 경계 탐색이다.

---

## 6. 크로스컷 이슈

### 6.1 왜 지금 A2A가 뜨는가

MCP가 tool interoperability를 어느 정도 해결하니 다음 병목이 **agent interoperability**로 이동했다. 특히 벤더 락인 우려(Salesforce agent가 ServiceNow agent와 대화하려면?)가 실제 엔터프라이즈 도입에서 진입 장벽이 되면서 표준 프로토콜 요구가 폭발.

### 6.2 Agent 신원과 인증

Tool은 client 조직이 소유하므로 신원 문제가 없다. A2A remote agent는 **외부 조직 소유** → OAuth2/OIDC/mTLS로 정체성 검증 필수. 발전 방향:
- **W3C DID** (Decentralized Identifiers) 재활용 (ANP `did:wba`)
- **Microsoft Entra Agent ID** — 사내 agent에 독립 신원 부여
- **W3C Verifiable Credentials** — 감사 가능한 위임 체인

### 6.3 비용·지연 문제

Multi-agent orchestration의 실무적 병목:
- Anthropic Research System: single chat 대비 **15× 비용** — token usage가 성능 분산의 80%
- Bedrock MAC: supervisor prompt 오버헤드로 5–10× token 사례 (*확인 필요*)
- 각 hop마다 LLM inference + 네트워크 latency + task state 저장 인프라

### 6.4 Hallucination Cascading

Agent chain에서 오류가 증폭. 한 agent의 오정보가 대화 전체를 오염. 방어:
- Subagent 결과의 **verification/citation pass** 별도 실행 (Anthropic 사례)
- Rogue Agent Detection ([arXiv:2502.05986](https://arxiv.org/abs/2502.05986))
- Adversarial multi-agent debate로 상호 검증

### 6.5 표준화 지형 요약

2026년 시점: Google A2A + Anthropic MCP가 Linux Foundation Agentic AI Foundation 아래 사실상 이원 표준. Cisco AGNTCY/SLIM이 인프라 레이어, Solo.io AGP가 게이트웨이 레이어, W3C DID가 identity 레이어로 스택 구성. crypto 궤도는 별도.

---

## 7. 최종 시나리오별 권장

3단 프레임에 매핑한 최종 판정.

| 시나리오 | 권장 | 이유 |
|---|---|---|
| **간단한 함수 위임 (계산, 검색)** | **(1) Tool call** | A2A 오버킬. MCP 서버로 충분 |
| **다른 벤더/조직 agent와 연동** | **(3) A2A protocol (Google A2A)** | Cross-org 계약 표면·신원·감사 필수 |
| **역할 기반 협업 (팀 시뮬레이션)** | **(2) CrewAI / AutoGen** | 같은 프레임워크 내 role delegation |
| **위임/handoff 위주 (컨텍스트 전달)** | **(2) OpenAI Agents SDK handoff** | 같은 프로세스, 대화 히스토리 전달 |
| **워크플로 그래프 (명시적 흐름)** | **(2) LangGraph**, 어댑터로 (3) 확장 | 그래프 명시성으로 디버깅 유리 |
| **대규모 병렬 리서치** | **(2) Claude Agent SDK subagent** | Isolation 크게, 요약만 반환 |
| **엔터프라이즈 M365 스택** | **(3) MS Copilot Studio + Agent Framework** | 프로토콜 + Entra Agent ID 완비 |
| **엔터프라이즈 ITSM/CRM** | **(3) ServiceNow AI Agent Fabric / Salesforce Agentforce** | 3계층 실행 모델 or Atlas |
| **AWS 인프라 위 크로스 프레임워크** | **(3) Bedrock AgentCore Runtime + A2A** | Strands / ADK / OpenAI SDK 상호운용 |
| **결정론적 파이프라인** | **(1) Tool call, agent 빼는 게 정답** | Agent 자율성이 오히려 노이즈 |
| **crypto agent economy** | AITP / Virtuals / Olas | 온체인 정산·registry 필요 |
| **개방형 웹 agent 크롤** | ANP | DID 기반 identity + `.well-known` discovery |

---

## 8. 핵심 인사이트

1. **"multi-agent"라는 단어에 속지 말라**. 시장의 대부분은 **(2)** — agent를 tool처럼 감싼 것에 불과하다. 프로토콜 레벨에서 (1)과 구분 불가능하다.
2. **(2)에 자율성을 기대하지 말라**. Callee가 clarification·거절·역제안을 못 하는 시스템은 tool call과 정확히 같은 실패 모드를 갖는다. CrewAI hierarchical의 비결정성 폭증이 대표 사례.
3. **(3)의 결정적 primitive는 세 가지**: (a) Task 상태 머신 (`input-required`, `rejected`가 스펙에 있는가), (b) capability advertisement (고정 스키마 대신 협의 가능한 skill 광고), (c) cross-org identity (외부 조직이 발급한 agent 신원 검증).
4. **Anthropic의 역설**: 프로덕션에서 잘 되는 MAS는 **agent 간 통신을 최소화하고 각 subagent를 잘 정의된 tool로 취급**할 때 성능-비용 곡선이 살아난다. 즉 오늘의 성공한 MAS는 **(3)의 언어**를 쓰지만 **(2)의 엔지니어링**을 한다.
5. **표준은 정해졌다**: Linux Foundation 아래 **Google A2A (agent 계층) + Anthropic MCP (tool 계층)** 가 사실상 이원 표준. 자체 프로토콜 고수하는 벤더는 소멸 중.

---

## 9. 한 줄 요약

> **"Agent를 tool처럼 부르는 것"은 A2A가 아니다. Task lifecycle·capability advertisement·cross-org identity가 스펙 primitive로 박혀 있어야 진짜 A2A(3)다. 그리고 오늘의 프로덕션 대부분은 여전히 (2)에 머물러야 하고, 실제로 그편이 낫다.**

---

## Sources

### Google A2A Protocol
- [Google Developers Blog — Announcing the Agent2Agent Protocol](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)
- [Linux Foundation — Launches Agent2Agent Protocol Project](https://www.linuxfoundation.org/press/linux-foundation-launches-the-agent2agent-protocol-project-to-enable-secure-intelligent-communication-between-ai-agents)
- [A2A Protocol Specification v0.3.0](https://a2a-protocol.org/v0.3.0/specification/)
- [a2aproject/A2A GitHub](https://github.com/a2aproject/A2A)
- [Life of a Task](https://a2a-protocol.org/latest/topics/life-of-a-task/)
- [Google ADK — A2A Quickstart](https://google.github.io/adk-docs/a2a/quickstart-exposing/)
- [Convert ADK agents for A2A](https://cloud.google.com/blog/products/ai-machine-learning/unlock-ai-agent-collaboration-convert-adk-agents-for-a2a)
- [A2A 1주년 press](https://www.linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year)

### 상용 SDK
- [Claude Agent SDK Overview](https://code.claude.com/docs/en/agent-sdk/overview)
- [Building agents with Claude Agent SDK](https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk)
- [OpenAI Agents SDK — Handoffs](https://openai.github.io/openai-agents-python/handoffs/)
- [OpenAI Agents SDK — Multi-agent](https://openai.github.io/openai-agents-python/multi_agent/)
- [Microsoft Agent Framework Overview](https://learn.microsoft.com/en-us/agent-framework/overview/)
- [Microsoft Agent Framework 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/)
- [CrewAI Hierarchical Process](https://docs.crewai.com/en/learn/hierarchical-process)
- [langgraph_supervisor](https://reference.langchain.com/python/langgraph-supervisor)
- [langgraph_swarm](https://reference.langchain.com/python/langgraph-swarm)
- [smolagents docs](https://huggingface.co/docs/smolagents/en/index)
- [Mastra Agents Overview](https://mastra.ai/docs/agents/overview)
- [Pydantic AI — Multi-Agent Patterns](https://pydantic.dev/docs/ai/guides/multi-agent-applications/)
- [LlamaIndex Multi-Agent Patterns](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/)
- [Haystack Multi-Agent Tutorial](https://haystack.deepset.ai/tutorials/45_creating_a_multi_agent_system)

### 상용 서비스
- [Salesforce — Inside Atlas Reasoning Engine](https://engineering.salesforce.com/inside-the-brain-of-agentforce-revealing-the-atlas-reasoning-engine/)
- [Salesforce — Integration Pattern Guide](https://www.salesforce.com/blog/how-to-choose-integration-pattern-for-agentforce/)
- [MS Copilot Studio — Multi-Agent Patterns](https://learn.microsoft.com/en-us/microsoft-copilot-studio/guidance/multi-agent-patterns)
- [MCP GA in Copilot Studio](https://www.microsoft.com/en-us/microsoft-copilot/blog/copilot-studio/model-context-protocol-mcp-is-now-generally-available-in-microsoft-copilot-studio/)
- [ServiceNow — MCP+A2A FAQ](https://www.servicenow.com/community/now-assist-articles/enable-mcp-and-a2a-for-your-agentic-workflows-with-faqs-updated/ta-p/3373907)
- [ServiceNow AI Agent Fabric](https://newsroom.servicenow.com/press-releases/details/2026/ServiceNow-opens-its-full-system-of-action-to-every-AI-Agent-in-the-enterprise/default.aspx)
- [AWS Bedrock MAC GA](https://aws.amazon.com/blogs/machine-learning/amazon-bedrock-announces-general-availability-of-multi-agent-collaboration/)
- [AWS AgentCore GA](https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available/)
- [AWS AgentCore A2A 지원](https://aws.amazon.com/blogs/machine-learning/introducing-agent-to-agent-protocol-support-in-amazon-bedrock-agentcore-runtime/)
- [Zapier MCP](https://zapier.com/mcp)
- [NVIDIA NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit)
- [IBM ACP](https://www.ibm.com/think/topics/agent-communication-protocol)

### 오픈소스 프로토콜
- [ANP GitHub](https://github.com/agent-network-protocol/AgentNetworkProtocol)
- [ANP did:wba spec](https://agent-network-protocol.com/specs/did-method.html)
- [AITP nearai/aitp](https://github.com/nearai/aitp)
- [IBM ACP research](https://research.ibm.com/blog/agent-communication-protocol-ai)
- [AGNTCY Linux Foundation](https://www.linuxfoundation.org/press/linux-foundation-welcomes-the-agntcy-project-to-standardize-open-multi-agent-system-infrastructure-and-break-down-ai-agent-silos)
- [SLIM IETF draft](https://datatracker.ietf.org/doc/draft-mpsb-agntcy-slim/)
- [Agora arxiv 2410.11905](https://arxiv.org/abs/2410.11905)
- [Ecma NLIP](https://ecma-international.org/news/ecma-international-approves-nlip-standards-suite-for-universal-ai-agent-communication/)
- [Solo.io agentgateway](https://agentgateway.dev/blog/2025-08-25-solo-contributes-agentgateway-to-lf/)
- [Zuplo — ACP 정리](https://zuplo.com/blog/agent-protocol-stack-mcp-a2a-acp-2026)

### 연구 논문
- [KQML Wikipedia](https://en.wikipedia.org/wiki/Knowledge_Query_and_Manipulation_Language)
- [Agent Interoperability Protocols Survey — arXiv:2505.02279](https://arxiv.org/abs/2505.02279)
- [CAMEL — arXiv:2303.17760](https://arxiv.org/abs/2303.17760)
- [AutoGen — arXiv:2308.08155](https://arxiv.org/abs/2308.08155)
- [MetaGPT — arXiv:2308.00352](https://arxiv.org/abs/2308.00352)
- [ChatDev — ACL 2024](https://aclanthology.org/2024.acl-long.810/)
- [Multi-Agent Debate — arXiv:2305.14325](https://arxiv.org/abs/2305.14325)
- [Generative Agents — arXiv:2304.03442](https://arxiv.org/abs/2304.03442)
- [AgentVerse — arXiv:2308.10848](https://arxiv.org/abs/2308.10848)
- [LLM MAS Survey — arXiv:2402.01680](https://arxiv.org/abs/2402.01680)
- [MultiAgentBench — arXiv:2503.01935](https://arxiv.org/abs/2503.01935)
- [Anthropic Multi-Agent Research System](https://www.anthropic.com/engineering/multi-agent-research-system)
- [Rogue Agents — arXiv:2502.05986](https://arxiv.org/abs/2502.05986)
- [Governance Gaps — arXiv:2606.31498](https://arxiv.org/html/2606.31498v1)

### 비교·해설
- [Descope — A2A vs MCP](https://www.descope.com/blog/post/mcp-vs-a2a)
- [Auth0 — MCP vs A2A](https://auth0.com/blog/mcp-vs-a2a/)
- [O'Reilly Radar — Designing Collaborative Multi-Agent Systems with A2A](https://www.oreilly.com/radar/designing-collaborative-multi-agent-systems-with-the-a2a-protocol/)
- [Rost Glukhov — A2A Protocol 2026: Adoption, Hype, Reality](https://www.glukhov.org/ai-systems/comparisons/a2a-protocol-2026-adoption)

### BibTeX (핵심 몇 개)

```bibtex
@article{finin1994kqml,
  title={KQML as an Agent Communication Language},
  author={Finin, Tim and Fritzson, Richard and McKay, Don and McEntire, Robin},
  booktitle={CIKM}, year={1994}
}
@inproceedings{li2023camel,
  title={CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society},
  author={Li, Guohao and Hammoud, Hasan Abed Al Kader and Itani, Hani and Khizbullin, Dmitrii and Ghanem, Bernard},
  booktitle={NeurIPS}, year={2023}, eprint={2303.17760}
}
@misc{wu2023autogen,
  title={AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation},
  author={Wu, Qingyun and Bansal, Gagan and Zhang, Jieyu and Wu, Yiran and Zhang, Shaokun and Zhu, Erkang and Li, Beibin and Jiang, Li and Zhang, Xiaoyun and Wang, Chi},
  year={2023}, eprint={2308.08155}
}
@inproceedings{hong2024metagpt,
  title={MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework},
  author={Hong, Sirui and others},
  booktitle={ICLR}, year={2024}, eprint={2308.00352}
}
@inproceedings{du2024debate,
  title={Improving Factuality and Reasoning in Language Models through Multiagent Debate},
  author={Du, Yilun and Li, Shuang and Torralba, Antonio and Tenenbaum, Joshua B. and Mordatch, Igor},
  booktitle={ICML}, year={2024}, eprint={2305.14325}
}
@misc{anthropic2025multiagent,
  title={How we built our multi-agent research system},
  author={{Anthropic}}, year={2025},
  howpublished={\url{https://www.anthropic.com/engineering/multi-agent-research-system}}
}
```
