---
layout: default
title: "현대 에이전트 SDK 전면 비교 (2026): LangGraph·OpenAI·Claude Agent SDK부터 13개 프레임워크까지"
---

# 현대 에이전트 SDK 전면 비교 (2026): LangGraph부터 각 벤더 Agent SDK까지 13개 프레임워크 총정리

> 📊 **인터랙티브 비교 페이지**: [Artifact 버전](https://claude.ai/code/artifact/d55d5e40-417e-4b15-b648-164535e5fc81) — 색상 코드화된 비교 매트릭스·상세 카드·의사결정 가이드를 시각적으로 볼 수 있습니다.

2024년이 "에이전트 프레임워크가 우후죽순 쏟아진 해"였다면, 2025~2026년은 **정리(consolidation)와 표준화(standardization)**의 시대다. Microsoft는 AutoGen과 Semantic Kernel을 하나로 합쳤고, Anthropic이 만든 **MCP(Model Context Protocol)**는 사실상 모든 프레임워크의 툴 연동 표준이 되었으며, Google의 **A2A(Agent2Agent)** 프로토콜은 에이전트 간 상호운용의 개방 표준으로 자리잡았다. 동시에 "순수 자율 LLM 루프"의 신뢰성 한계를 겪은 업계는 **명시적·결정론적 그래프 워크플로우**로 회귀하고 있다.

이 글은 2026년 7월 기준으로 주요 **13개 에이전트 프레임워크**를 6개 "가족(family)"으로 나눠 아키텍처·모델 유연성·멀티에이전트·라이선스 관점에서 비교한다.

---

## 목차

1. [6개 가족으로 나눠 본 지형도](#1-6개-가족으로-나눠-본-지형도)
2. [마스터 비교 매트릭스](#2-마스터-비교-매트릭스)
3. [가족별 상세 프로파일](#3-가족별-상세-프로파일)
4. [상황별 의사결정 가이드](#4-상황별-의사결정-가이드)
5. [2025→2026, 지형을 바꾼 6가지 흐름](#5-20252026-지형을-바꾼-6가지-흐름)
6. [참고문헌](#참고문헌)

---

## 1. 6개 가족으로 나눠 본 지형도

프레임워크마다 세계관이 다르다. 아래 분류는 이 글 전체에서 각 프레임워크가 속한 "가족"을 나타낸다.

| 가족 | 프레임워크 | 한 줄 설명 |
|------|-----------|-----------|
| **① 모델 제공사 SDK** | OpenAI Agents SDK, Claude Agent SDK | 모델 벤더가 직접 만든 공식 하네스 — 서로 정반대 철학 |
| **② 그래프·오케스트레이션** | LangGraph, Google ADK, MS Agent Framework | 명시적 상태·그래프로 제어권을 개발자에게 |
| **③ 역할·대화형 멀티에이전트** | CrewAI, AG2 | 역할/작업 기반 "AI 팀" 협업 모델 |
| **④ 데이터·RAG 중심** | LlamaIndex | 문서·검색 기반 에이전트의 명가 |
| **⑤ 타입세이프·경량 (Python)** | Pydantic AI, smolagents | 신뢰성/최소주의 지향 |
| **⑥ TS·웹 & 클라우드** | Mastra, Strands, Vercel AI SDK | 풀스택 DX & 프로덕션 배포 |

---

## 2. 마스터 비교 매트릭스

| 프레임워크 | 언어 | 버전 (2026 중반) | 유지관리 | 모델 | 라이선스 | 핵심 강점 |
|-----------|------|-----------------|----------|------|----------|----------|
| **LangGraph** | Python · JS/TS | 1.0 GA → 1.2.x | LangChain Inc. | 모든 모델 | MIT | 지속성·체크포인트·HITL, 프로덕션 검증 1위 |
| **OpenAI Agents SDK** | Python · JS/TS | 0.18.3 | OpenAI | 100+ (LiteLLM) | MIT | 경량 handoff, 내장 트레이싱·가드레일, 음성/실시간 |
| **Claude Agent SDK** | Python · TS | 0.2.x | Anthropic | Claude 전용 | Commercial | 자율 코딩·OS 조작, 서브에이전트, 네이티브 MCP |
| **Google ADK** | Python · Java + | 2.5.0 | Google | Gemini + 다수 | Apache 2.0 | 결정론적 그래프 워크플로우, A2A+MCP, Vertex |
| **CrewAI** | Python | 1.14.3 | CrewAI Inc. | 다수 (LiteLLM) | MIT | 역할/작업 기반 빠른 셋업, Crews + Flows |
| **MS Agent Framework** | .NET · Python | 1.0 GA | Microsoft | 다수 | Open src | AutoGen+SK 통합, .NET 최강, MCP+A2A |
| **AG2 (구 AutoGen)** | Python | 1.0.0b0 | 커뮤니티 포크 | 다수 | Apache 2.0 | 클래식 대화형 멀티에이전트 계승 |
| **Pydantic AI** | Python | 2.6.0 | Pydantic | 다수 | MIT | 타입세이프·구조화 출력·신뢰성, Logfire |
| **LlamaIndex Workflows** | Python · TS | Workflows 1.0 | LlamaIndex Inc. | 다수 | MIT | RAG·문서 중심 최강, 이벤트 기반 오케스트레이션 |
| **Mastra** | TypeScript | 2026 활발 | Mastra | 다수 | Apache 2.0* | TS 네이티브, 메모리+내구성 워크플로우+플레이그라운드 |
| **Strands Agents** | Python · TS | 1.0 | AWS | Bedrock + 다수 | Apache 2.0 | 모델 주도형, MCP 우선, AWS 프로덕션 검증 |
| **smolagents** | Python | 1.26.0 | Hugging Face | 모든 모델 | Apache 2.0 | ~1,000줄 초경량, 코드 실행 에이전트 |
| **Vercel AI SDK** | TS/JS | v5 → v6 | Vercel | 다수 | Apache 2.0 | 스트리밍 UI·프론트 통합 최강, Next.js 시너지 |

> \* Mastra 코어는 Apache 2.0, 일부 엔터프라이즈 기능은 source-available.

---

## 3. 가족별 상세 프로파일

### ① 모델 제공사 SDK — 정반대의 두 철학

#### OpenAI Agents SDK

- **계보**: 2024년 실험적 프레임워크 **Swarm** → 2025년 3월 프로덕션 SDK 출시 → 2025년 10월 DevDay에서 비주얼 도구 **AgentKit** 추가 (단, Agent Builder·Evals는 2026-11-30 종료 예정).
- **버전**: Python `openai-agents` **0.18.3** (2026-07-17), TS/JS 병행.
- **프로그래밍 모델**: 4개 프리미티브 — **Agents**(LLM+지시+툴), **Handoffs**(제어권 이전 라우팅), **Tools**(함수+호스티드 툴), **Guardrails**(입출력 검증, tripwire 예외). 여기에 **Sessions**(대화 이력 자동관리)와 **Runner**(에이전트 루프 구동)를 더함.
- **모델**: 프로바이더 중립 — OpenAI Responses/Chat Completions + LiteLLM로 **100+ LLM**. OpenAI 락인 없음(트레이싱·호스티드 툴은 OpenAI 중심).
- **철학**: *"여러 가벼운 에이전트를 오케스트레이션한다."*
- **➕ 강점**: 최소 추상화 + 내장 트레이싱/가드레일, 프로바이더 이식성, **음성·실시간(Realtime) 에이전트 업계 최강**.
- **➖ 약점**: 파일시스템/장기 자율 작업은 Claude SDK보다 약함. AgentKit 비주얼 도구 부분 종료로 약간의 혼란.
- **라이선스**: MIT (무료). 모델 사용료만 지불.

#### Claude Agent SDK

- **계보**: **Claude Code SDK**를 2025-09-29 **Claude Agent SDK**로 개명 (코딩을 넘어 법률·금융·SRE·보안 에이전트로 확산되면서).
- **버전**: Python `claude-agent-sdk` **0.2.x** (~2026-07), TS 병행. 네이티브 Claude Code 바이너리 번들.
- **프로그래밍 모델**: *"한 에이전트에게 컴퓨터를 통째로 준다."* `query()`가 메시지를 스트리밍하며 Claude가 자율적으로 툴 루프를 돌림.
  - **내장 툴**: Read·Write·Edit·Bash·Glob·Grep·WebSearch·WebFetch 등 즉시 사용.
  - **서브에이전트**: 각자 격리된 컨텍스트·툴·모델을 가진 자식 에이전트를 스폰.
  - **컨텍스트 관리**: Claude Code에서 상속한 자동 컴팩션.
  - **Sessions**: JSONL로 저장, 재개·포크 가능.
  - **Hooks / Permissions**: 생명주기 콜백과 세밀한 툴 허용/차단.
  - **MCP**: 프로토콜 저자답게 1급 네이티브 클라이언트.
- **모델**: **Claude 전용** (Anthropic API/Bedrock/Vertex/Foundry 인증).
- **2026-06 Dynamic Workflows**: 리드 에이전트가 수십~수백 개 서브에이전트를 한 세션에서 병렬 확장 + 루브릭 기반 재작성(Performance Outcomes).
- **➕ 강점**: 자율 코딩·문서·SRE 등 환경 조작형 작업 최강, 설정 제로, 네이티브 MCP.
- **➖ 약점**: Claude 모델 락인, 토큰 비용 높음, 음성 스토리 약함.
- **라이선스**: Anthropic Commercial ToS (SDK 자체 별도 비용은 없음).

> **핵심 대비**: OpenAI = "많은 경량 에이전트 라우팅(handoff·guardrail)", Claude = "한 에이전트에게 컴퓨터 주기(내장 툴·hooks·permissions)". 작업 성격이 선택을 가른다.

### ② 그래프·오케스트레이션 — 제어권을 개발자에게

#### LangGraph

- **정체**: LangChain 하위의 저수준 오케스트레이션 프레임워크. 상태를 가진 제어 가능한 에이전트를 **유향 그래프**로 표현. ~126K★.
- **버전**: **1.0 GA (2025-10-22)**, LangChain 라이브러리도 동시에 1.0. 2026년 1.2.x로 안정화.
- **아키텍처**: **StateGraph** — 노드(계산 스텝)+엣지(제어 흐름), 조건부 분기·루프·팬아웃. 중앙 상태 객체(TypedDict)가 리듀서로 병합. **체크포인터**가 노드마다 상태 스냅샷 → 크래시 복구·리플레이·"타임트래블". **interrupt** 프리미티브로 1급 HITL. **Send**로 병렬 맵.
- **멀티에이전트**: supervisor / swarm 라이브러리, Send 병렬.
- **프로덕션**: Klarna·Uber·LinkedIn·Replit·Cloudflare·JPMorgan 등 — **검증된 프로덕션 배포가 가장 많음**. LangSmith(관측)·LangGraph Platform(배포)은 유료 레이어(오픈코어).
- **➕ 강점**: 지속성·상태·HITL·리플레이 최강, 복잡한 순환 제어 흐름에 최적.
- **➖ 약점**: 장황함(CrewAI 20줄 = LangGraph 50줄+), API 잦은 변경(interrupt·체크포인트 포맷), JS/TS는 Python보다 뒤처짐.
- **라이선스**: MIT. LangSmith Plus $39/user/월, Platform Plus ~$35/월.

#### Google ADK (Agent Development Kit)

- **정체**: Google의 오픈소스 코드 우선 프레임워크. Cloud Next 2025 공개, Google 자체 Agentspace/Gemini Enterprise를 구동.
- **버전**: `google-adk` **2.5.0** (2026-07-16), `adk-java` 병행. 5개 언어(Python·Java·TS·Go·Kotlin) 지향. Apache 2.0.
- **아키텍처**: **Agent** + **Workflow**(그래프/DAG). **ADK 2.0(2026-03 알파)**에서 대화형 → **결정론적 그래프 워크플로우**로 전환(라우팅·팬아웃/인·루프·리트라이·중첩 워크플로우). **Task API**로 구조화된 에이전트 위임. **A2A** 네이티브(Agent Card로 상호 발견).
- **모델**: Gemini·Gemma·Claude(Vertex)·Ollama·vLLM·LiteLLM 등. Vertex AI Agent Engine 원클릭 배포.
- **➕ 강점**: 결정론적 워크플로우 + 네이티브 A2A/MCP + 멀티언어·모델.
- **➖ 약점**: Google Cloud/Vertex 중력, 잦은 API 변경(1.0→2.5, 14개월).

#### Microsoft Agent Framework — 가장 중요한 상태 정리

Microsoft 진영은 이제 **세 가지**로 나뉜다.

- **Microsoft Agent Framework (공식 미래 방향)**: **AutoGen + Semantic Kernel의 수렴체**. 2025-10 프리뷰 → **2026-04-03 v1.0 GA**. .NET과 Python 동시 지원(에이전트 프레임워크 중 **.NET 스토리 최강**). sequential·concurrent·handoff·group chat·Magentic-One 패턴, YAML 선언형, MCP+A2A+AG-UI. 모델 커넥터: Foundry·Azure·OpenAI·Claude·Bedrock·Gemini·Ollama.
- **원본 AutoGen (`microsoft/autogen`)**: 대화형 멀티에이전트의 선구자였으나 **유지보수 모드**. 신규 프로젝트 비권장.
- **AG2 (`ag2ai/ag2`, 커뮤니티 포크)**: 2024-11 포크. Apache 2.0, 오픈 거버넌스 "AgentOS". **v1.0.0b0(2026-07-03)**로 1.0 향해 진행. 클래식 AutoGen 모델을 살아있는 프로젝트로 계승.

> **결론**: AutoGen + Semantic Kernel은 **Microsoft Agent Framework 1.0**으로 합쳐졌고 두 전신은 유지보수 전용. 클래식 AutoGen 모델은 커뮤니티 **AG2**로 존속한다.

### ③ 역할·대화형 멀티에이전트

#### CrewAI

- **정체**: João Moura가 2023-12 만든 Python 멀티에이전트 프레임워크(LangChain 독립). ~54K★. **v1.14.3 (2026-04-24)**. MIT.
- **아키텍처**: **Crews**(역할·목표·백스토리·툴을 가진 Agent들이 Task 협업, "AI 팀") + **Flows**(이벤트 기반 결정론 오케스트레이션). 둘 조합 가능.
- **특징**: 단·장기·엔티티 메모리, LiteLLM 모델 유연성, MCP 지원, 체크포인트. 상용 **AMP Cloud**(비주얼 에디터·코파일럿·거버넌스). Fortune 500의 ~60%가 사용한다고 주장.
- **➕ 강점**: 역할 기반 앱 최단 셋업, 대형 커뮤니티.
- **➖ 약점**: 추상화 블랙박스화, 엔터프라이즈 실행당 과금 부담.
- **가격**: 코어 무료(MIT). AMP: Free(50 실행/월), Professional $25/월, Enterprise 커스텀.

#### AG2 (구 AutoGen 포크)

- 위 "Microsoft Agent Framework" 절 참조. AssistantAgent·UserProxy·GroupChat 대화형 모델. **AutoGen 프로그래밍 모델을 계속 쓰고 싶다면 정답**. 단, MS 백킹 상실·커뮤니티 규모 제한.

### ④ 데이터·RAG 중심

#### LlamaIndex (Workflows / AgentWorkflow)

- **정체**: LlamaIndex Inc.(구 GPT Index). Python·TS. **Workflows 1.0**이 현재 경량 에이전트 프레임워크. MIT.
- **아키텍처**: `@step` **이벤트 기반 스텝 합성**(타입 이벤트 emit/consume, async 우선). **AgentWorkflow**가 에이전트·상태·툴콜을 이해하는 사전 구성 경로(ReAct·function-calling). `llama-deploy`로 서비스화.
- **차별점**: **RAG·데이터 혈통 최강** — LlamaHub 커넥터·인덱싱·쿼리/검색 엔진. 멀티에이전트(오케스트레이터/handoff)·병렬·루프·상태 지속·HITL·MCP.
- **➕ 강점**: RAG·문서 중심 최강, 세밀한 오케스트레이션 제어, Python/TS 이중.
- **➖ 약점**: 패키지 난립·표면적 큼, 단순 에이전트엔 과함.

### ⑤ 타입세이프·경량 (Python)

#### Pydantic AI

- **정체**: Pydantic 팀(Pydantic 검증 라이브러리·Logfire 관측 제작사). **v2.0.0(2026-06-23)** → v2.6.0(2026-07). MIT. ~16.5K★.
- **아키텍처**: `Agent` + v2.0의 **capability**(툴·훅·지시·모델설정을 합성하는 단위). 구조화 출력은 검증된 Pydantic 모델, 의존성 주입으로 타입 컨텍스트 전달.
- **차별점**: 딥 타입세이프(핵심 셀링포인트), 모델 중립, 1급 MCP 클라이언트, 스트리밍, **내구성 에이전트**+HITL, Logfire/OpenTelemetry 네이티브, GEval 평가.
- **➕ 강점**: 신뢰성·타입세이프·구조화 출력·프로덕션 관측. FastAPI/Pydantic 사용자에게 자연스러움.
- **➖ 약점**: Python 전용, 2.x 빠른 릴리스로 API 변동, 멀티에이전트는 덜 성숙.

#### smolagents

- **정체**: Hugging Face의 미니멀 Python 라이브러리(~1,000줄). **v1.26.0(2026-05-29)**. Apache 2.0.
- **아키텍처**: **CodeAgent** — 액션을 JSON 툴콜이 아니라 **실행 가능한 Python 코드**로 표현(표현력 높은 제어 흐름). E2B·Modal·Docker 샌드박스 실행. ToolCallingAgent도 제공.
- **차별점**: 극단적 미니멀·해커블, 모델 완전 자유(transformers·Ollama·Hub·LiteLLM), 멀티모달 입력, HF Hub에서 툴/에이전트 공유.
- **➕ 강점**: 단순·투명, 모델 자유, Hub 통합.
- **➖ 약점**: 코드 실행 = 샌드박스 필수, 프로덕션 배포·내구성 기능 얇음.

### ⑥ TS·웹 & 클라우드

#### Mastra

- **정체**: TypeScript 종합 프레임워크(Gatsby 출신 팀). 코어 Apache 2.0, 엔터프라이즈 source-available. Replit·Sanity·SoftBank·WorkOS·Elastic 사용.
- **아키텍처**: **Agents** + **Graph Workflows**(분기·병렬·내구성, 무기한 pause/resume) + **Memory** + **Tools** + 관측. **Zod** 스키마로 전면 타입세이프.
- **차별점**: 메모리(작업+시맨틱), MCP(클라이언트+서버 저작), 평가, 로컬 **Developer Studio** 플레이그라운드. React/Next/Node 통합 또는 독립 서버.
- **➕ 강점**: JS/TS 팀 최강 DX, 메모리+내구성 워크플로우+플레이그라운드.
- **➖ 약점**: TS/JS 한정, 상대적 신생, 엔터프라이즈 기능 비공개.

#### Strands Agents (AWS)

- **정체**: AWS 오픈소스 SDK. Python 1.0(2026-05-21), TS 1.0(2026-04-30). Apache 2.0. Amazon Q·AWS Glue 내부 구동.
- **아키텍처**: **모델 주도형** — 모델·툴·프롬프트만 주면 모델이 추론/툴 루프 주도(하드코딩 그래프 아님). v1.0에 **SubAgent**·**A2A**·원격 세션 매니저 추가.
- **차별점**: 양쪽 언어 1급 MCP, 광범위 모델(Bedrock·Claude·Llama·Ollama·LiteLLM), Bedrock AgentCore 배포, OpenTelemetry.
- **➕ 강점**: 프로덕션 검증, MCP·모델 유연성, Python+TS 이중.
- **➖ 약점**: AWS/Bedrock 중력, 커뮤니티 통합 아직 신생.

#### Vercel AI SDK

- **정체**: Vercel의 TS/JS SDK. **v5** 타입 프로토콜 확립, **v6가 2026년 착지 중**(파괴적 변경). ~11.5M weekly npm, ~23.7K★. Apache 2.0.
- **아키텍처**: 프로바이더 추상화 코어(`generateText`/`streamText`/`generateObject`) + **Agent 클래스**(에이전트 루프). 툴은 `inputSchema`/`outputSchema`. UIMessage vs ModelMessage 분리, SSE 스트리밍. `useChat`·**AI Elements** 프리빌트 UI.
- **차별점**: **웹 프론트 스트리밍·UI 통합 최강**, 통합 프로바이더 인터페이스. 2026 추가: Workflows(내구성)·Sandbox·AI Elements. Next.js/Vercel 시너지.
- **➕ 강점**: UI/스트리밍 DX 최강, 프로바이더 중립, 대규모 채택.
- **➖ 약점**: v5→v6 잦은 파괴적 변경, 무거운 멀티에이전트·메모리·평가는 약함(모델+UI SDK가 먼저, 에이전트 프레임워크가 나중).

---

## 4. 상황별 의사결정 가이드

정답은 없다. 작업 성격·팀 언어·배포 환경·모델 종속 허용치에 따라 갈린다.

| 상황 | 1순위 추천 | 이유 |
|------|-----------|------|
| 복잡한 상태·장기 실행·사람 승인(HITL)이 핵심 | **LangGraph** (또는 MS Agent Framework) | 체크포인트·지속성·타임트래블·인터럽트가 1급 시민 |
| 코드·파일·쉘 조작 자율 코딩/SRE/문서 에이전트 | **Claude Agent SDK** | 내장 툴·컨텍스트 관리·서브에이전트 즉시 |
| 여러 모델 자유 교체 + 가벼운 라우팅·음성 | **OpenAI Agents SDK** | 최소 추상화+트레이싱, 100+ 모델, 실시간/음성 최강 |
| 몇 줄로 "역할 나눈 AI 팀" 빠른 프로토타이핑 | **CrewAI** | 역할/목표/작업 추상화로 램프업 최단 |
| 문서·검색(RAG)이 중심 | **LlamaIndex** | LlamaHub·인덱싱·쿼리 엔진 데이터 혈통 |
| 타입세이프·검증된 구조화 출력·신뢰성(Python) | **Pydantic AI** | Pydantic 검증 전면 + Logfire 관측 |
| Next.js/React 웹앱에 스트리밍 챗·에이전트 UI | **Vercel AI SDK** (또는 Mastra) | UI/스트리밍 DX 최강 |
| AWS 위 MCP 우선 프로덕션 멀티에이전트 | **Strands** | 모델 주도형 + Bedrock AgentCore 배포 |
| .NET 샵 / Azure·Foundry 엔터프라이즈 | **MS Agent Framework** | 유일하게 .NET 1급, AutoGen+SK 통합체 |
| 연구·학습·해킹 (라이브러리 내부를 다 읽고 싶다) | **smolagents** | ~1,000줄 초경량 코드 에이전트 |
| 조직·플랫폼 넘나드는 에이전트 협업(상호운용) | **Google ADK** (A2A 계열) | A2A(Agent Card) 네이티브 + 결정론 워크플로우 |
| 클래식 AutoGen 대화형 모델 계승 | **AG2** | 오리지널 AutoGen은 유지보수 모드 |

---

## 5. 2025→2026, 지형을 바꾼 6가지 흐름

1. **MCP가 사실상 표준.** Anthropic이 만든 MCP를 거의 모든 프레임워크가 툴 연동 표준으로 채택. "어느 SDK를 쓰든 MCP 서버는 재사용 가능."
2. **A2A로 에이전트 상호운용.** Google의 A2A(Agent2Agent)를 ADK·MS Agent Framework·Strands가 채택. 조직·런타임을 넘는 협업이 개방 표준으로.
3. **Microsoft의 대통합.** AutoGen + Semantic Kernel → Microsoft Agent Framework 1.0(2026-04). 두 전신은 유지보수 모드, 클래식 AutoGen은 AG2로 존속.
4. **"결정론적 그래프"로의 회귀.** 순수 자율 LLM 루프의 신뢰성 한계 후 LangGraph·ADK 2.0·CrewAI Flows·Mastra 모두 명시적 워크플로우 강화.
5. **두 철학의 양극화.** "많은 경량 에이전트 오케스트레이션"(OpenAI·CrewAI) vs "한 에이전트에게 컴퓨터 주기"(Claude SDK).
6. **오픈코어 + 유료 운영층.** 프레임워크는 MIT/Apache 무료, 관측·배포·거버넌스는 유료 플랫폼(LangSmith·AMP·Vertex·Foundry)으로 수익화.

---

## 참고문헌

> ⚠️ 세부 마이너 버전·릴리스 날짜·채택 통계 일부는 2차 출처(블로그·집계 사이트)에서 확인된 근사치입니다. 아키텍처·계보·라이선스 등 핵심 사실은 공식 문서로 교차 검증했습니다. 에이전트 생태계는 매우 빠르게 변하므로 실제 도입 전 각 공식 릴리스 노트를 재확인하시길 권합니다.

**LangGraph / LangChain**
- [LangChain & LangGraph reach v1.0](https://www.langchain.com/blog/langchain-langgraph-1dot0)
- [Is LangGraph used in production?](https://blog.langchain.com/is-langgraph-used-in-production/)
- [LangGraph interrupts docs](https://docs.langchain.com/oss/python/langgraph/interrupts)

**OpenAI Agents SDK / Claude Agent SDK**
- [OpenAI Agents SDK docs](https://openai.github.io/openai-agents-python/) · [PyPI](https://pypi.org/project/openai-agents/) · [Introducing AgentKit](https://openai.com/index/introducing-agentkit/)
- [Claude Agent SDK overview](https://code.claude.com/docs/en/agent-sdk/overview) · [Migration guide](https://platform.claude.com/docs/en/agent-sdk/migration-guide) · [Dynamic Workflows](https://claude.com/blog/a-harness-for-every-task-dynamic-workflows-in-claude-code)
- [Claude vs OpenAI vs ADK 비교 (Composio)](https://composio.dev/content/claude-agents-sdk-vs-openai-agents-sdk-vs-google-adk)

**Google ADK / CrewAI / Microsoft**
- [google-adk PyPI](https://pypi.org/project/google-adk/) · [ADK + A2A docs](https://google.github.io/adk-docs/a2a/)
- [crewAI GitHub](https://github.com/crewAIInc/crewAI/releases) · [Changelog](https://docs.crewai.com/en/changelog)
- [Microsoft Agent Framework 1.0](https://devblogs.microsoft.com/agent-framework/microsoft-agent-framework-version-1-0/) · [SK+AutoGen 병합 (VS Magazine)](https://visualstudiomagazine.com/articles/2025/10/01/semantic-kernel-autogen--open-source-microsoft-agent-framework.aspx)
- [AG2 GitHub](https://github.com/ag2ai/ag2)

**Pydantic AI / LlamaIndex / Mastra / Strands / smolagents / Vercel**
- [Pydantic AI releases](https://github.com/pydantic/pydantic-ai/releases) · [MCP client docs](https://ai.pydantic.dev/mcp/client/)
- [LlamaIndex Workflows 1.0](https://www.llamaindex.ai/blog/announcing-workflows-1-0-a-lightweight-framework-for-agentic-systems) · [AgentWorkflow](https://www.llamaindex.ai/blog/introducing-agentworkflow-a-powerful-system-for-building-ai-agent-systems)
- [Mastra](https://mastra.ai/) · [GitHub](https://github.com/mastra-ai/mastra)
- [Introducing Strands Agents (AWS)](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-an-open-source-ai-agents-sdk/) · [Strands 1.0](https://aws.amazon.com/blogs/opensource/introducing-strands-agents-1-0-production-ready-multi-agent-orchestration-made-simple/)
- [smolagents GitHub](https://github.com/huggingface/smolagents) · [docs](https://huggingface.co/docs/smolagents/en/guided_tour)
- [Vercel AI SDK v5→v6 migration](https://www.digitalapplied.com/blog/vercel-ai-sdk-v5-to-v6-migration-playbook-2026)

**비교 분석 아티클**
- [LangGraph vs CrewAI vs OpenAI Agents SDK 2026 (Particula)](https://particula.tech/blog/langgraph-vs-crewai-vs-openai-agents-sdk-2026)

---

*이 리서치는 Claude Code를 활용해 2026년 7월 웹 리서치를 종합하여 자동 작성되었습니다.*
