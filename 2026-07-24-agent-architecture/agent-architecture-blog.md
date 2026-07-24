---
layout: post
title: "요즘 에이전트, 진짜로 뭘로 만들어지나 — '가장 복잡한 에이전트'를 상정한 구성요소 전면 해부 (2026)"
date: 2026-07-24
categories: [research, ai-agents]
tags: [agent-architecture, harness, context-engineering, mcp, agent-skills, memory, rag, react, plan-and-execute, multi-agent, a2a, evaluation, observability, guardrails, claude-code, devin, manus, codex, cursor]
---

# 요즘 에이전트, 진짜로 뭘로 만들어지나

> **이 리포트가 답하려는 질문**: "에이전트 = LLM + 툴"이라는 요약은 2023년까지만 유효했다. 2026년의 프로덕션 에이전트는 **하네스(harness)·컨텍스트 엔지니어링·MCP·스킬·메모리·플래닝·멀티에이전트·평가/가드레일**이 겹겹이 쌓인 시스템이다. 이 글은 **상상할 수 있는 가장 복잡한 에이전트 하나**를 상정하고, 그 에이전트를 완성하기 위해 실제로 필요한 모든 구성 요소를 레이어별로 해부한다. 각 레이어마다 **개념 → 대표 논문/1차 자료 → 상용에서 실제로 쓰는 것**을 함께 붙였다.

---

## 0. 리포트를 관통하는 프레임: "가장 복잡한 에이전트"의 8-레이어 참조 아키텍처

우리가 상정하는 "가장 복잡한 에이전트"는 다음과 같다. **수 시간~며칠 걸리는 소프트웨어/리서치 작업을, 격리된 샌드박스에서, 수백 개의 툴과 여러 서브에이전트를 동원해, 사람 개입 없이 자율적으로 수행하고, 그 결과를 검증·감사·복구까지 하는 에이전트.** (Claude Code, Devin, Manus, Codex를 한 몸에 합친 가상의 상한선이라 보면 된다.)

이 에이전트를 완성하려면 아래 8개 레이어가 모두 필요하다. 이 글의 목차이기도 하다.

| # | 레이어 | 한 줄 요약 | 대표 구현 |
|---|---|---|---|
| 1 | **하네스 / 에이전트 루프** | 모델을 감싸 "동작하는 에이전트"로 만드는 while-loop 골격 | Claude Code `nO` loop, Codex harness |
| 2 | **컨텍스트 엔지니어링** | 유한한 attention budget에 "최소·고신호 토큰"만 채우는 규율 | Anthropic CE, Manus KV-cache |
| 3 | **툴 / MCP / 스킬** | 에이전트의 손(행동)·연결 표준·전문 지식(절차) | function-calling, MCP, Agent Skills |
| 4 | **메모리 & 검색(RAG)** | 컨텍스트 밖에 기억을 쓰고 필요할 때 되읽기 | memory tool, Letta, Zep, agentic RAG |
| 5 | **플래닝 / 추론 / 자기수정** | 무엇을 다음에 할지 결정하는 제어 흐름 | ReAct, Plan-and-Execute, Reflexion |
| 6 | **멀티에이전트 오케스트레이션** | 작업을 쪼개 병렬 서브에이전트로 확장 | orchestrator-worker, A2A |
| 7 | **평가 / 관측 / 가드레일 / 신뢰성** | 프로덕션 경화(hardening): eval·trace·security·durability | OTel GenAI, lethal trifecta, MAST |
| 8 | **상용 프로덕션 스택** | 위 레이어들을 실제로 조립한 제품들 | Devin, Codex, Cursor, Jules… |

**이 8개 레이어를 관통하는 단 하나의 원칙**이 있다. 2025~2026년 에이전트 엔지니어링의 지배적 화두는 **"컨텍스트 경제(context economy)"** 다. Anthropic은 이를 이렇게 정의했다.

> "Good context engineering means finding the **smallest possible set of high-signal tokens** that maximize the likelihood of some desired outcome." — Anthropic, *Effective context engineering for AI agents* (2025)
>
> (좋은 컨텍스트 엔지니어링이란, 원하는 결과가 나올 확률을 극대화하는 **가장 작은 고신호 토큰 집합**을 찾는 것이다.)

스킬의 progressive disclosure, 툴의 `defer_loading`/Tool Search, code mode의 중간결과 격리 — 뒤에 나올 거의 모든 최신 기법이 이 한 문장의 파생이다. "복잡한 에이전트"의 본질은 기능을 늘리는 게 아니라 **유한한 attention budget을 어떻게 아끼느냐**의 싸움이다.

---

## 1. 하네스(Harness)와 에이전트 루프 — 골격

### 1.1 "하네스"란 무엇인가

**하네스(harness, = agent scaffolding)** 는 날것의 LLM을 실제로 동작하는 에이전트로 바꾸는 **소프트웨어 래퍼 전체**다. 루프, 툴 실행, 컨텍스트 관리, 메모리, 가드레일, 트레이싱을 포함한다.

2026년의 핵심 통찰은 **모델이 하네스와 함께 학습(co-train)된다**는 것이다. "Claude Code의 모델은 자신이 학습된 바로 그 하네스를 사용하도록 배웠다"는 표현이 대표적이고, OpenAI도 Codex의 모든 표면(CLI·web·IDE)이 "동일한 Codex harness — 공유되는 에이전트 루프, 스레드 수명주기, 툴 실행, 인증 로직"을 돌린다고 명시한다. 이 때문에 **"하네스 엔지니어링(harness engineering)" / "loop engineering"** 이 프롬프트 엔지니어링·컨텍스트 엔지니어링 위의 상위 규율로 2026년에 부상했다.

### 1.2 코어 에이전트 루프 (perceive → reason → act → observe)

기계적 심장은 결국 **while-loop** 다.

> "The loop runs: assemble prompt, call LLM, parse output, execute any tool calls, feed results back, repeat until done. Mechanically, it's often just a while loop." — *The Anatomy of an Agent Harness*

Anthropic은 이 루프를 **Claude Agent SDK** 문서에서 의미론적으로 **gather context → take action → verify work → repeat** 로 정식화한다.

- **Gather context** — "다음 단계에 필요한 것만 가져온다(fetching only what the next step needs)."
- **Take action** — "툴은 에이전트가 진전을 이루는 유일한 방법이다. 툴 없는 루프는 while문 안의 챗봇일 뿐이다(a loop with no tools is just a chatbot in a while statement)."
- **Verify work** — 규칙 기반 체크·시각 피드백·(선택) LLM 심판으로 결과를 목표에 대조.

이것이 **workflow vs agent** 구분과 만난다(Anthropic, *Building Effective Agents*, 2024):

> "**Workflows** are systems where LLMs and tools are orchestrated through predefined code paths. **Agents** are systems where LLMs dynamically direct their own processes and tool usage."
>
> (워크플로우는 제어 흐름이 코드로 미리 정의된 시스템, 에이전트는 LLM이 스스로 프로세스와 툴 사용을 동적으로 지휘하는 시스템이다.)

기본 빌딩블록은 **augmented LLM** = LLM + 검색(retrieval) + 툴(tools) + 메모리(memory)다. Anthropic의 지배 철학은 "**가장 단순한 해법에서 시작하고, 필요할 때만 복잡도를 더하라 — 애초에 에이전트를 안 만드는 게 답일 수도 있다**"이다.

### 1.3 상용 3대 하네스가 루프를 짜는 법

- **Claude Code** (역공학 코드명 **`nO` 메인 루프**): "단일 스레드 마스터 루프 + 절제된 툴 + 플래닝"으로 통제 가능한 자율성을 낸다. `while(tool_call) → execute → feed results → repeat`, 평문 응답이 나오면 자연 종료. **하나의 평평한 메시지 히스토리 / 단일 메인 스레드**를 고수한다("경쟁하는 여러 에이전트 페르소나"를 의도적으로 회피). 코어 툴: **Bash, Read, Edit, Write, Grep, Glob, Task(서브에이전트), TodoWrite**. 컨텍스트 한계 근처에서 압축기(`wU2`)가 요약, 비동기 이중버퍼 큐(`h2A`)가 실시간 조향(mid-task steering)을 가능케 한다. (`nO/wU2/h2A` 등 코드명은 커뮤니티 역공학 결과이므로 "잘 검증된 분석"으로 취급.)
- **OpenAI Codex CLI** (*Unrolling the Codex agent loop*, 2026): (1) 대화 상태로 프롬프트 조립 → (2) **Responses API** 로 전송·SSE 수신 → (3) 툴 호출 요청 시 실행·결과 append → (4) 갱신 프롬프트로 재질의 → (5) 어시스턴트 메시지가 나올 때까지 반복. 지시는 프로젝트 디렉터리의 **AGENTS.md** 에서 로드. 임계 토큰 초과 시 **compaction** + Responses API **prefix caching** 으로 컨텍스트 관리.
- **Cursor** (2026): 자체 **Composer** 모델, test-run-fix를 기본 8회까지 도는 **Agent Loop**, 격리 샌드박스의 **Background Agents**, ~200K~312K 컨텍스트. `@codebase` 는 시맨틱 검색을 트리거.

### 1.4 프로덕션 에이전트의 메시지 레이어 (Messages API)

구체적 기질(substrate)은 이렇게 생겼다. 요청은 캐시 순서대로 **`system` 배열 → `tools` 배열 → `messages` 배열**, 각 메시지 content는 타입 있는 **content block**(`text`/`tool_use`/`tool_result`/thinking/image). 툴 사이클: 모델이 `tool_use` 방출 → 하네스가 실행 → 다음 user 턴에 `tool_use_id`로 참조되는 `tool_result` 반환 → **툴 호출 없는 평문 메시지**가 나오면 while-loop 종료. 이 "종료 조건"이 곧 루프의 정의다.

---

## 2. 컨텍스트 엔지니어링 — 새로운 규율

프롬프트 엔지니어링의 후계자. Anthropic *Effective context engineering for AI agents*(2025)의 정의:

> "Context engineering refers to the set of strategies for **curating and maintaining the optimal set of tokens** during LLM inference."

### 2.1 왜 이게 중요한가 — attention budget과 context rot

> "LLMs, like humans, have a limited working memory capacity… an **'attention budget'** that they draw on when parsing large volumes of context. Every new token introduced depletes this budget."

트랜스포머는 토큰 n개에 대해 n² 쌍관계를 만든다 — "1만 토큰이면 1억 개의 관계"를 추적해야 하고, 길어질수록 attention이 얇게 펴진다. 그 결과가 **context rot** 다.

> "**Context rot**: as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases." (Chroma Research, *Context Rot*, 2025 — 18개 모델 실험. 200K 창도 ~50K에서 정확도 저하, 1M 창도 1M 전체를 신뢰성 있게 추론하지 못함.)

**함의: 컨텍스트는 한계효용이 체감하는 유한 자원이다.** 크게 넣는다고 좋아지지 않는다.

### 2.2 시스템 프롬프트 설계 — "right altitude" (골디락스 존)

> "System prompts should present ideas at the **right altitude** for the agent — the **Goldilocks zone** between hardcoding brittle if-else logic and giving vague high-level guidance that falsely assumes shared context."

즉 "너무 딱딱한 규칙"과 "너무 막연한 지시" 사이. 섹션 구조(`<background_information>`, `<instructions>`, `## Tool guidance`, `## Output description`) + **완전히 명세된 최소 지침 집합**을 권장한다.

### 2.3 Just-in-Time 검색 & progressive disclosure

> "The field is increasingly adopting **'just in time'** context strategies, where agents maintain lightweight **identifiers** (file paths, queries, links) and dynamically load data into context at runtime using tools, rather than pre-processing all relevant data upfront."

모든 걸 미리 벡터DB에 인덱싱하는 방식에서, **가벼운 참조(파일 경로·ID·쿼리)를 들고 런타임에 필요한 것만 로드**하는 방식으로 이동 중이다. Anthropic은 하이브리드(속도용 사전검색 + JIT 탐색)를 권장한다.

### 2.4 통합 프레임워크 — Write / Select / Compress / Isolate

Lance Martin / LangChain의 4-버킷 분류(외우면 편하다):

- **Write** — 컨텍스트 밖에 저장(스크래치패드, 메모리 파일)
- **Select** — 알맞은 컨텍스트 끌어오기(RAG, 툴/메모리 선택)
- **Compress** — 요약·트리밍(compaction)
- **Isolate** — 서브에이전트/샌드박스로 컨텍스트 분리

그리고 컨텍스트 엔지니어링이 고치는 **4대 실패 모드**(Drew Breunig): **Context Poisoning**(오류가 컨텍스트에 박혀 반복 참조됨), **Context Distraction**(너무 길어 학습지식보다 컨텍스트에 과집중), **Context Confusion**(불필요 정보로 저품질 생성), **Context Clash**(누적 정보 간 모순).

### 2.5 Manus의 "KV-cache 우선" 6원칙 (프로덕션 골드 소스)

*Context Engineering for AI Agents: Lessons from Building Manus*(Yichao "Peak" Ji, 2025)는 프레임워크를 **4번 갈아엎으며**("Stochastic Graduate Descent") 얻은 교훈을 정리했다.

1. **Design around the KV-cache** — > "**KV-cache hit rate is the single most important metric for a production-stage AI agent.**" 캐시된 입력 ~$0.30/MTok vs 미캐시 $3.00/MTok = **10배** 차이. 프리픽스는 안정적으로(타임스탬프 금지), 컨텍스트는 append-only, 직렬화는 결정적(JSON 키 순서 고정).
2. **Mask, don't remove** — 툴을 동적으로 추가/삭제하면 캐시가 깨지고 과거 호출이 orphan이 된다. 대신 툴 정의는 고정하고 **logit masking** 으로 가용 툴을 제약(상태기계 + 응답 prefill).
3. **Use the file system as context** — 파일시스템 = 무한·영속·직접조작 가능한 **외부화된 메모리**. 압축은 **복원 가능(restorable)** 해야 한다: 웹페이지 본문은 버려도 **URL** 은 남긴다.
4. **Manipulate attention through recitation** — `todo.md` 를 매 스텝 다시 써서 전역 목표를 컨텍스트 끝(가장 주목받는 영역)으로 밀어 **lost-in-the-middle** 을 방어(평균 ~50 tool call 작업).
5. **Keep the wrong stuff in** — > "erasing failures removes evidence needed for the model to adapt." 실패·스택트레이스를 컨텍스트에 남긴다. "에러 복구는 진짜 에이전트다움의 가장 명확한 지표 중 하나."
6. **Don't get few-shot-ped** — 균일한 반복 패턴은 모델을 과적합시킨다. 구조적 변주를 넣어라.

### 2.6 장기실행 에이전트 — 교대근무(shift) 모델

*Effective harnesses for long-running agents*(Anthropic, 2025)는 컨텍스트 창을 넘는 며칠짜리 작업을 이렇게 다룬다: 에이전트는 "**이전 근무를 기억하지 못하는 교대 근무 엔지니어**처럼" 세션 단위로 일한다. **Initializer agent**(1회: 환경 셋업, `feature-list.json` 생성, `init.sh` 작성) + **Coding agent**(반복적으로 "깨어나" 기능 하나씩 진전, 테스트, `claude-progress.txt` 기록, 커밋). **세션 간 상태 = 컨텍스트가 아니라 지속 산출물**(피처 리스트·git 커밋·테스트 게이트·진행 로그).

---

## 3. 툴 / 함수호출 / MCP / 스킬 — 손·연결·지식

### 3.1 툴 사용(function-calling)의 기본

툴 = `name` + `description` + `input_schema`(JSON Schema). 라운드트립: `tools` 실린 요청 → 모델이 `stop_reason:"tool_use"` + `tool_use` 블록 반환 → 앱이 실행 → `tool_use_id` 참조하는 `tool_result` 를 다음 user 턴에 append → 최종 자연어 응답.

**핵심 구분: client tool vs server tool** = *코드가 어디서 실행되는가*. Client tool(내 함수 + `bash`/`text_editor`/`computer`/`memory` 같은 Anthropic 스키마 툴)은 내 앱에서, server tool(`web_search`/`web_fetch`/`code_execution`/`tool_search`)은 Anthropic 인프라에서 실행.

세부 제어: `tool_choice`(`auto`/`any`/`tool`/`none`), **병렬 툴 호출**(기본 on, `disable_parallel_tool_use`로 끔), **strict**(`strict:true` → 스키마 정확 일치 보장), 그리고 SDK의 **Tool Runner**(루프를 대신 돌려줌).

**툴 설계 원칙**(Anthropic, *Writing effective tools for AI agents*, 2025):

> "Tools represent a fundamentally new software paradigm: **contracts between deterministic systems and non-deterministic agents.**"

① 고레버리지 툴 선택(API 얇은 래퍼 지양) ② 네임스페이싱 ③ 의미 있는 컨텍스트 반환(불투명 ID 대신 고신호 필드) ④ 토큰 효율(페이지네이션·필터·truncation) ⑤ 툴 설명 자체를 프롬프트 엔지니어링 ⑥ 실측 평가.

### 3.2 MCP (Model Context Protocol) — "AI를 위한 USB-C"

Anthropic이 2024년 11월 발표, 2026년엔 광범위 채택(Anthropic·OpenAI·VS Code·Cursor).

> "Think of MCP like a **USB-C port for AI applications**. Just as USB-C provides a standardized way to connect electronic devices, MCP provides a standardized way to connect AI applications to external systems." (modelcontextprotocol.io)

**아키텍처 — host / client / server**: MCP Host(AI 앱)가 서버당 하나의 MCP Client를 만들어 1:1 연결. Server는 로컬(**stdio** 전송, 보통 단일 클라이언트) 또는 원격(**Streamable HTTP** 전송 + OAuth, 다수 클라이언트). 프로토콜은 **JSON-RPC 2.0**, stateful(`initialize` 핸드셰이크).

**서버 3대 프리미티브**:

| 프리미티브 | 무엇 | 제어 주체 |
|---|---|---|
| **Tools** | 모델이 능동적으로 호출하는 함수(DB 쓰기·API 호출·파일 수정) | **Model** |
| **Resources** | 읽기전용 데이터 소스(파일 내용·DB 스키마·문서, URI 주소) | **Application** |
| **Prompts** | 특정 툴/리소스 사용을 지시하는 사전제작 템플릿 | **User** |

Claude Messages API의 MCP 커넥터(beta `mcp-client-2025-11-20`)는 별도 클라이언트 없이 원격 MCP 서버에 연결하고, `mcp_toolset`으로 allowlist/denylist/`defer_loading`을 제어한다.

**MCP 보안**(2025~2026): **prompt injection**(Willison, 2025), **tool poisoning**(Invariant Labs — 악성 지시를 *툴 설명*에 숨김, 사용자에겐 안 보임), **rug pull**(승인 시엔 선량, 이후 악성으로 교체), 공급망/line-jumping. CVE로는 **MCPoison(CVE-2025-54136)**, **CurXecute(CVE-2025-54135)**. 방어: `mcp-scan`, OAuth, 게이트웨이 검사, 툴 변경 시 사람 승인.

### 3.3 Agent Skills — "새 입사자를 위한 온보딩 가이드" (2025-10-16)

> "Skills are **folders of instructions, scripts, and resources** that Claude loads dynamically to improve performance on specialized tasks." (anthropics/skills)
>
> 비유: "Building a skill for an agent is like putting together an **onboarding guide for a new hire**." (Barry Zhang)

**SKILL.md 스켈레톤**:

```markdown
---
name: your-skill-name
description: Brief description of what this Skill does and when to use it.
---
# Your Skill Name
## Instructions
[step-by-step guidance for Claude]
## Examples
[concrete examples]
```

**핵심 메커니즘 — progressive disclosure (3단계)**:

| 레벨 | 로드 시점 | 토큰 비용 | 내용 |
|---|---|---|---|
| **L1 메타데이터** | 항상(시작 시) | ~100 토큰/스킬 | YAML `name`+`description` |
| **L2 지침** | 스킬 트리거 시 | <5k 토큰 | SKILL.md 본문 |
| **L3+ 리소스** | 필요 시 | 접근 전 0 | 번들 파일/스크립트(코드는 컨텍스트 미진입, 출력만) |

> "When Claude runs `validate_form.py`, the **script's code never loads into the context window. Only its output** consumes tokens." — 스크립트가 즉석 코드 생성보다 훨씬 효율적인 이유. 그리고 "번들 콘텐츠에 실질적 한계가 없다"(접근 전엔 토큰을 안 먹으므로).

스킬은 **코드 실행 환경(파일시스템 + bash)** 위에서 돈다. 배포: Claude Code(`~/.claude/skills/`, 플러그인), API(`skills-2025-10-02` beta + code execution tool, 사전제작 `pptx/xlsx/docx/pdf`), claude.ai(zip 업로드). 오픈 표준 **agentskills.io** 도 공개됐다.

### 3.4 Code Mode / Programmatic Tool Calling — 컨텍스트 경제의 절정

**문제 두 가지**: (1) 수백~수천 개 툴 정의를 미리 로드하면 요청 읽기도 전에 **5만+ 토큰** 소모. (2) 모든 중간 결과가 컨텍스트를 왕복.

**해법**(Anthropic, *Code execution with MCP*, 2025): MCP 서버를 **코드 API로 제시** — 툴/서버당 TypeScript 파일을 파일시스템에 깔고, 에이전트가 개별 툴 호출 대신 그 API를 **import·호출하는 코드를 작성**해 샌드박스에서 실행. 툴은 파일시스템처럼 on-demand 발견.

> 헤드라인 수치: ~150,000 토큰 워크플로우 → **~2,000 토큰(98.7% 감소)**. 프라이버시 이점도: 중간 데이터가 "모델을 거치지 않고" 샌드박스 안에서만 흐른다.

Cloudflare **Code Mode** 는 같은 아이디어(LLM은 툴 호출보다 *API 호출 코드 작성*을 더 잘한다 — 학습셋에 TypeScript가 훨씬 많으니까)로 "2,500개 엔드포인트 상호작용을 **117만 → ~1,000 토큰(약 99.9% 감소)**"을 보고했다. Anthropic은 이를 API-native하게 **Programmatic Tool Calling** + **Tool Search Tool**(`defer_loading:true`로 툴을 지연 로드, ~500토큰짜리 검색 툴만 노출)로 제품화했다.

### 3.5 Tools vs MCP vs Skills — 경쟁이 아니라 레이어

| 축 | **Tools** | **MCP** | **Skills** |
|---|---|---|---|
| 정체 | 하나의 호출가능 함수 | 연결 *프로토콜*·표준 | 지침+스크립트+리소스 *폴더* |
| 무엇을 더함 | 능력(행동) | 표준화된 전송·발견 레이어 | 노하우·절차(how) |
| 컨텍스트 비용 | 스키마 사전로드(defer 가능) | ×N 서버(5만+ 토큰) | 트리거 전 ~100토큰/스킬 |
| 비유 | 함수 | AI용 USB-C | 신입 온보딩 가이드 |
| 적합 | 개별 행동 | 앱/데이터 생태계 연결 | 반복 전문성 인코딩 |

**관계**: 스킬(노하우)이 툴·MCP를 호출하고 샌드박스에서 스크립트를 돌리도록 지시한다. MCP는 능력에 대한 *접근*을 표준화하고, function-calling은 모델이 행동을 트리거하는 *저수준 메커니즘*이며, code mode는 다수 호출을 샌드박스 코드로 대체하는 *최적화*다. 복잡한 에이전트는 이 넷을 **동시에 겹쳐 쓴다**.

---

## 4. 메모리 & 검색(RAG) — 기억

### 4.1 메모리 분류 체계

**두 축**. (1) *보존*: 단기(=컨텍스트 창, 작업 기억) vs 장기(창 밖 영속 저장, 필요 시 되읽기). (2) *기능 형태*:

| 유형 | 정의 | 예 |
|---|---|---|
| **Semantic** | 사실·관계 | 사용자가 채식주의자, API base URL |
| **Episodic** | 과거 경험/사건(에피소드 요약) | "지난 화요일 auth 버그를 잡았다" |
| **Procedural** | 작업 수행법(일반화된 스킬·규칙) | 학습된 시스템프롬프트·툴 사용 루틴 |

핵심 설계 문제: 컨텍스트 창은 유한·저하되므로, 살아있는 정보를 장기저장에 **쓰고(write)** 알맞은 부분만 JIT로 **읽는다(read)**. Procedural 메모리는 점점 가중치 파인튜닝이 아니라 **편집 가능한 in-context 지침**으로 저장된다.

### 4.2 장기 메모리 구현체 비교

- **MemGPT / Letta** — "LLM as an OS". OS 가상메모리 차용: main context(RAM) + external context(disk). Letta 3계층 = **core memory**(편집 가능 in-context 블록) + **recall memory**(대화 히스토리) + **archival memory**(외부 벡터DB). > "memory edits and retrieval are entirely self-directed" — 자기수정 메모리를 함수호출로 관리. **sleep-time compute**(유휴 시 백그라운드 통합).
- **Anthropic memory tool + context editing** (2025-09-29, GA `memory_20250818`): > "The memory tool lets Claude store and retrieve information across conversations in a directory of memory files… Memory supports **just-in-time context retrieval**." 클라이언트측 실행(`view/create/str_replace/insert/delete/rename`, `/memories` 디렉터리). **context editing**(`clear_tool_uses_20250919`)이 임계치(기본 10만 토큰) 초과 시 오래된 툴 결과를 자동 제거하고 placeholder로 대체. **둘을 결합**하면 100턴 웹검색 eval에서 **토큰 84% 절감 + 성능 39% 향상**(context editing 단독 29%).
- **Mem0** — 2단계(Extraction → Update: ADD/UPDATE/DELETE/NOOP). 그래프 변종 **Mem0g**. LOCOMO에서 full-context 대비 p95 지연 −91%, 토큰 −90%.
- **Zep / Graphiti** — **시간적 지식 그래프(temporal KG)**. 3계층 서브그래프(episode/entity/community) + **bi-temporal**(사건 발생시각 T + 관측시각 T′). 새 사실이 들어오면 모순되는 엣지를 **무효화(invalidate)** — 이것이 **stale memory** 해결법. 하이브리드 검색(시맨틱+BM25+그래프). LongMemEval +18.5%, 지연 −90%.
- **LangMem / LangGraph** — `BaseStore` 위 3유형 메모리. hot-path(에이전트가 의식적으로 저장) + background(Memory Manager 비동기 통합).
- **OpenAI ChatGPT memory** — saved memories(명시) + reference chat history(암시).

### 4.3 Agentic RAG — 정적 검색에서 에이전트 주도 검색으로

정적 RAG(embed → top-k → prompt → generate, 원샷) → **Agentic RAG**(검색이 *에이전트가 호출을 결정하는 툴*, 추론 루프에 내장, **언제·무엇을·어떻게** 검색할지 결정):

- **Query planning/decomposition** — 복잡 쿼리를 서브태스크로 분해 후 검색.
- **Multi-hop** — 검색→읽기→중간발견으로 재검색.
- **Self-RAG**(ICLR 2024) — reflection token(`Retrieve`/`IsREL`/`IsSUP`/`IsUSE`)으로 온디맨드 검색 + 자기비평.
- **Corrective RAG(CRAG)** — 경량 평가자가 문서를 Correct/Ambiguous/Incorrect로 채점, 자신 없으면 웹검색 fallback.

**검색 품질 메커니즘**: **하이브리드 검색**(BM25 sparse + dense vector 병렬 → **RRF(Reciprocal Rank Fusion)** 로 랭크 융합) + **cross-encoder reranker**(쿼리+문서 동시 처리). 하이브리드+rerank는 dense-only 대비 NDCG +26~31% 보고.

### 4.4 지식그래프 vs 벡터, GraphRAG

벡터: 빠름·콜드스타트 없음·비정형 시맨틱 recall에 강함, 그러나 multi-hop 관계 추론에 약함. KG: 결정적·multi-hop·설명가능·시간 유효성, 그러나 구축비용·콜드스타트. **Microsoft GraphRAG**: 엔티티/관계 추출 → 그래프 → 커뮤니티 클러스터링(Leiden) → LLM 커뮤니티 요약 → **local search**(엔티티 이웃) + **global search**(전 코퍼스 질문, naive RAG 불가한 것). 전역 쿼리에서 comprehensiveness/diversity 70~80% 우위. 실무: 대부분 벡터로 시작해 추론 요구가 커지면 하이브리드(Zep/Graphiti·GraphRAG)로 승급.

### 4.5 메모리 실패 모드

**stale memory**(시간 무효화·UPDATE/DELETE·TTL로 완화), **memory poisoning/injection**(악성·환각 내용을 영구 메모리에 써 영원히 신뢰 — path-traversal 방어, 쓰기 전 검증, 사람 편집 가능 메모리), **retrieval cascade**(나쁜 검색→나쁜 컨텍스트, CRAG/Self-RAG 자기채점으로 대응), **cross-context bleed**(프로젝트 스코핑·네임스페이싱).

---

## 5. 플래닝 / 추론 / 자기수정 — 제어 흐름

### 5.1 코어 추론 패턴 (원 논문)

- **CoT**(Wei et al., 2201.11903) — 중간 추론 단계가 복잡 추론을 극적으로 개선. 모든 것의 기질.
- **ReAct**(Yao et al., 2210.03629, ICLR 2023) — Thought↔Action↔Observation 인터리브. > "reasoning traces help the model induce, track, and update action plans… while actions allow it to interface with external sources." 단일에이전트 기본 패턴. 약점: 토큰이 스텝에 선형 비례.
- **Plan-and-Execute** (LangChain) — Planner(대형 모델)가 다단계 계획 → Executor(더 싼 모델)가 실행 + 재계획. ReAct보다 빠르고 싸고, 계획을 명시적으로 강제해 누락 스텝을 방지.
- **ReWOO**(2305.18323) — Plan→Work→Solve, 변수 치환(`#E1`)으로 관측 없이 전체 계획을 선(先)작성. HotpotQA에서 토큰 5배 효율 + 정확도 +4%.
- **LLM Compiler**(2312.04511, ICML 2024) — 태스크 **DAG** + 병렬 실행. ReAct 대비 지연 3.7배·비용 6.7배·정확도 ~9% 개선.
- **Tree of Thoughts**(2305.10601) — 사고 트리 + 상태 평가자 + 탐색(BFS/DFS). 매우 고비용, "탐색·lookahead·백트래킹"이 필요한 퍼즐용.
- **Self-Refine**(2303.17651) — 한 모델이 generate→self-feedback→refine(단일 출력).
- **Reflexion**(2303.11366) — Actor + Evaluator + Self-Reflection, **에피소드 간** 언어적 피드백을 episodic memory에 저장해 다음 시도 개선(가중치 갱신 없이).

### 5.2 프로덕션의 플래닝 = 외부화된 가변 계획

학술 패턴은 실전에서 **명시적·외부화·가변 TODO 리스트**로 나타난다. **Claude Code TodoWrite**(3+ 스텝 작업에서 계획을 먼저 세움 — "긴 작업은 컨텍스트를 부풀리고 초기 지시가 가장자리로 밀려나므로, 계획을 항상 보이게 유지"). **Manus todo.md recitation**(전역 계획을 컨텍스트 끝으로 밀어 goal drift 방어). **Devin**(구조화된 계획 선작성 + DAG 실행 + **동적 재계획** — "조사하며 제약을 발견하고 막다른 길에 부딪히면 계획을 갱신"). 대부분의 장기 에이전트는 하이브리드(명시적 계획 산출물 + 인터리브 실행 + 지속적 계획 수정).

### 5.3 검증·자기비평 & reasoning model

**generator-verifier gap**: "검증이 생성보다 쉽다"가 테스트타임 스케일링이 통하는 이유. **Self-Consistency**(2203.11171 — 다양한 추론 경로 샘플 후 다수결, GSM8K +17.9%). **LLM-as-Judge**(2306.05685 — GPT-4 심판이 인간과 >80% 일치, 단 position/verbosity/self-enhancement 편향). **Process Reward Model(PRM)** 은 스텝별 채점으로 탐색을 안내.

**Reasoning model**(o-series, Claude extended thinking, R1류)은 외부 스캐폴드(ToT·명시적 CoT)를 상당 부분 모델 내부로 흡수했다. Claude **interleaved thinking**: > "enables Claude to think between tool calls and make more sophisticated reasoning after receiving tool results." — ReAct의 "Thought" 스텝을 학습된 고effort 추론 블록으로 업그레이드. OpenAI의 **planner/doer** 패턴(o-series=플래너, GPT=실행자)은 Plan-and-Execute와 정확히 매핑된다.

### 5.4 오케스트레이션 제어 흐름 — Anthropic 5 워크플로우 패턴

1. **Prompt chaining** — 고정 순서 단계, 사이에 프로그램적 게이트.
2. **Routing** — 입력 분류 후 전문 프롬프트/모델로 라우팅(싼 모델 vs 비싼 모델).
3. **Parallelization** — sectioning(독립 서브태스크 병렬) / voting(같은 태스크 여러 번, self-consistency류).
4. **Orchestrator-workers** — > "a central LLM dynamically breaks down tasks, delegates them to worker LLMs, and synthesises their results." 서브태스크가 미리 정의되지 않고 오케스트레이터가 결정.
5. **Evaluator-optimizer** — 한 LLM이 생성, 다른 LLM이 평가·피드백 루프(Self-Refine/Reflexion의 프로덕션판).

**결정 휴리스틱**: 단일 augmented LLM 호출 → 경로가 알려지면 워크플로우 → 스텝을 예측할 수 없는 개방형 작업에만 완전 에이전트/orchestrator-workers, 명확한 평가기준이 있을 때 evaluator-optimizer.

### 5.5 테스트타임 컴퓨트

*Scaling LLM Test-Time Compute Optimally*(2408.03314, DeepMind): 추론 컴퓨트를 문제 난이도별로 적응 배분하면 훨씬 큰 모델을 이길 수 있다. 두 축 — **순차 스케일링**(사고 연장, o-series) + **병렬 스케일링**(다수 후보 샘플 후 검증/투표로 선택). generator-verifier gap이 병렬 스케일링의 수익원.

**패턴별 언제 쓰나:**

| 패턴 | 계획 방식 | 적응성 | 비용 | 최적 상황 |
|---|---|---|---|---|
| ReAct | 스텝별 인터리브 | 최고 | 높음(스텝 선형) | 관측이 다음 스텝을 크게 좌우 |
| Plan-and-Execute | 선계획+재계획 | 중 | 낮음(싼 실행자) | 분해 가능한 다단계 |
| ReWOO | 전체 선계획 | 낮음 | 최저 토큰 | 독립 조회 많은 툴 작업 |
| LLM Compiler | DAG 병렬 | 중 | 최저 지연 | 병렬화 가능 툴 호출 다수 |
| ToT | 트리 탐색+자기평가 | 높음 | 매우 높음 | lookahead 필요 퍼즐 |
| Reflexion | 언어적 메모리로 재시도 | 높음(시도 간) | 높음 | 보상 신호 + 재시도 허용 |

---

## 6. 멀티에이전트 오케스트레이션 — 확장

### 6.1 토폴로지

**Orchestrator-Worker**(리드가 분해→전문 워커 스폰→합성; 프로덕션 지배 패턴), **Supervisor**(중앙 LLM이 다음 전문가 선택·라우팅), **Hierarchical**(감독자를 감독하는 다층), **Network/Handoff**(피어 그래프, 중앙조정 없음, **handoff** 로 제어 이양), **Sequential**(고정 체인), **Parallel**(독립 병렬 후 집계), **Blackboard**(공유 상태에 read/write하는 피어), **Group chat**(전원 한 채널 공유, manager가 speaker selection), **Swarm**(탈중앙 피어 + handoff), **Magentic**(매니저가 task ledger 유지·동적 지휘). 프로덕션 휴리스틱: "**hierarchical과 graph 두 패턴만 비용값을 하고, swarm·blackboard는 이론적으론 흥미로우나 실전에선 잘 못 이긴다.**"

### 6.2 Anthropic 멀티에이전트 리서치 시스템

**Lead Researcher**(Claude Opus)가 쿼리 분석·전략 수립·계획을 메모리에 저장 → **3~5 서브에이전트**(Sonnet)를 병렬 스폰(각 독립 컨텍스트 창, 각자 3+ 툴 병렬) → 리드가 합성 → 마지막에 **CitationAgent**.

> "A multi-agent system with Claude Opus 4 as the lead agent and Claude Sonnet 4 subagents **outperformed single-agent Claude Opus 4 by 90.2%** on our internal research eval."

**토큰 경제(논쟁의 핵)**: > "agents typically use about **4× more tokens** than chat, and **multi-agent systems use about 15× more tokens** than chats." 성능 분산의 ~95%를 **토큰 사용(~80%) + 툴 호출 수(~10%) + 모델 선택(~5%)** 이 설명 — 즉 멀티에이전트가 이기는 큰 이유는 *토큰을 더 쓰기 때문*이고, 그래서 **고가치 작업에만** 경제성이 있다.

**언제 도움/해로움**: breadth-first·병렬 검색·컨텍스트 창 초과 작업엔 도움. > "Domains that require all agents to share the same context or involve many dependencies between agents are **not a good fit**." — 공유 컨텍스트·강결합(대부분의 코딩)엔 부적합. 오케스트레이터 프롬프트 원칙: **think like your agents**, **teach the orchestrator how to delegate**(명확한 목표·출력형식·툴 안내·경계 — 없으면 서브에이전트가 작업 중복·공백 발생), **scale effort to query complexity**(단순=1 에이전트/3-10 호출, 비교=2-4 서브/각 10-15, 복잡=10+ 서브). 신뢰성: > "**Agents are stateful and errors compound**" — 체크포인트+재시도+resume, rainbow deployment.

### 6.3 프레임워크 비교

| 프레임워크 | 코어 추상화 | 제어 모델 | 상태 | 멀티에이전트 |
|---|---|---|---|---|
| **LangGraph** | 상태 그래프(노드+엣지, 타입 State) | 명시적 그래프/상태기계 | 중앙 State + checkpointer(durable, time-travel, HITL) | supervisor/network/hierarchical, `Command(goto,update)` handoff |
| **OpenAI Agents SDK**(←Swarm) | Agent/Runner/Tools/Handoffs/Guardrails/Sessions | 자율 에이전트 루프 | Sessions 영속 메모리(Responses API) | **Handoffs** vs agent-as-tool |
| **CrewAI** | Crew(role/goal/tools)+tasks+process, Flow | 역할기반 자율 or 이벤트기반 결정적 | Flow state, crew memory | sequential/hierarchical(자동 매니저) |
| **MS Agent Framework**(AutoGen+SK, GA 1.0 2026) | AIAgent + Workflows(타입 그래프) | 자율 + 결정적 워크플로우 | SK 세션 상태, checkpoint/resume | sequential/concurrent/handoff/group chat/**Magentic**, MCP+A2A |
| **AutoGen/AG2** | ConversableAgent, GroupChat+Manager | 대화 주도(actor v0.4) | 메시지 히스토리 | group chat 6 speaker-selection |
| **Google ADK** | LlmAgent + workflow agents | 하이브리드(결정적 or transfer) | Session state 공유 | Sequential/Parallel/LoopAgent + sub_agents, A2A |
| **Claude Agent SDK** | Agent + 서브에이전트, MCP | 오케스트레이터가 격리 서브 스폰 | 서브당 **fresh 격리 창** | Task tool, Dynamic Workflows(수십~수백 팬아웃) |
| **LlamaIndex Workflows** | 이벤트기반 `@step` 그래프 | 이벤트 주도 | 공유 Context, 타입 이벤트 | 중첩/병렬 파이프라인(RAG 강함) |
| **Pydantic AI** | 타입세이프 Agent + pydantic-graph | 타입세이프 | 검증된 구조화 출력, DI | graph node, agent-as-tool |
| **Mastra** | TS 에이전트 + 결정적 워크플로우 | 유연 vs 예측가능 | 워크플로우 상태, 메모리 | agent network + workflow step |

**핵심 축 = 제어 모델**: graph/상태기계(결정적·검사가능) vs 자율/LLM주도(유연·비예측). 2026 프레임워크 대부분이 **양쪽 다** 제공.

### 6.4 에이전트 통신 프로토콜

> "**MCP is vertical**: model to tools and data. **A2A is horizontal**: agent to agent." — 상보적.

**A2A**(Google 발표 2025-04 → Linux Foundation 2025-06 → v1.0 2026): **Agent Card**(`/.well-known/agent.json`, 능력 광고·발견), **Task**(상태기계: submitted→working→input-required→completed/failed/canceled/rejected), **Message/Part/Artifact**, JSON-RPC 2.0 over HTTPS + SSE 스트리밍. **AGNTCY**(Cisco, 발견·신원·관측 레이어; OASF + ACP). **ACP** 혼동 주의(Cisco ACP=REST vs IBM/BeeAI ACP=JSON-RPC, 후자는 2025-08 A2A로 병합). 2026 스택: **MCP(에이전트→툴) · A2A(에이전트→에이전트) · AGNTCY(발견/신원/관측)**.

### 6.5 Claude Code 서브에이전트

**Task tool** 이 위임 프리미티브. > "A subagent starts with a **fresh, isolated context window** — it does not see your conversation history." 각 서브는 자기 컨텍스트·툴 권한·모델을 갖고 압축된 결과만 오케스트레이터에 반환. 커스텀 = `.claude/agents/*.md`(YAML frontmatter: `description`(무엇+*언제* → 자동 위임 트리거), `tools`, `model`… + 본문=시스템프롬프트). 서브에이전트가 이기는 때: 컨텍스트 격리, 병렬 팬아웃, 전문화(스코프 프롬프트+제한 툴셋+싼 모델).

### 6.6 실패 모드 & "멀티에이전트 만들지 마라" 논쟁

**Cognition, *Don't Build Multi-Agents*(2025-06)**:
> **Principle 1: "Share context, and share full agent traces, not just individual messages."**
> **Principle 2: "Actions carry implicit decisions, and conflicting decisions carry bad results."**

병렬 서브에이전트는 서로의 컨텍스트가 없어 **암묵적 결정이 충돌**(예: 서로 다른 스타일로 클론 제작)해 병합이 깨진다. 처방: **단일 스레드 선형 에이전트**, 컨텍스트가 커지면 파생 대신 **압축 모델**로 히스토리 요약. 2026 업데이트 *Multi-Agents: What's Actually Working* 는 철회가 아닌 "정교화": **여러 에이전트가 *지능(읽기 분석)* 을 기여하되 *쓰기는 단일 스레드*("single writer")**.

**MAST**(Berkeley/IBM, 2025): 7개 프레임워크 1,600+ 트레이스에서 첫 멀티에이전트 실패 분류. **14 실패 모드 / 3 범주** — 시스템 설계(~44%: 태스크 명세 불복종·스텝 반복·종료조건 미인지), inter-agent 오정렬(~32%), 검증/종료 실패. **실패율 41~87%** — "체계적 문제". 

**산업의 화해**: **읽기/검색은 병렬화, 쓰기/코딩은 단일 스레드나 격리 샌드박스로.** Anthropic(병렬 읽기+단일 합성)과 Cognition(single writer)의 표면적 대립은 read-heavy vs write-heavy 도메인 차이다.

---

## 7. 평가 / 관측 / 가드레일 / 신뢰성 — 프로덕션 경화

### 7.1 에이전트 평가 3단계

에이전트는 최종 출력 전에 수십 개 내부 결정을 하므로 출력만 평가하면 대부분의 실패를 놓친다.

- **Final Response(결과)** — 끝 결과만 채점(task success). 단순하나 과정에 눈감음.
- **Trajectory(궤적/glass-box)** — 툴 선택·인자·중간추론·상태전파 전체 채점(중복 호출·불필요 행동·불안전 스텝 탐지). 메트릭: tool selection accuracy, parameter correctness, path efficiency, step precision/recall.
- **Single-Step(white-box)** — 개별 결정을 고립 테스트.

**LLM-as-Judge**: > "requires structured rubrics, multiple judge passes, and calibration against human-labeled examples to mitigate bias and drift."

**핵심 벤치마크**:

| 벤치마크 | 무엇을 테스트 |
|---|---|
| **SWE-bench Verified** | 실제 GitHub 이슈 500개, 격리 Docker에서 패치가 숨은 테스트를 통과하는가 |
| **GAIA** | 다단계 추론+툴 사용(브라우징·파일·코드·멀티모달), 인간엔 쉬움 |
| **WebArena** | 5개 샌드박스 사이트의 다단계 브라우저 조작(SOTA <40%) |
| **τ²-bench** | 정책 준수가 1급 메트릭 + dual-control, **pass^k**(신뢰성) |
| **TerminalBench** | 커맨드라인 워크플로우, 실행 오류 복구 |
| **BrowseComp** | 찾기 힘든 정보 지속·창의 탐색 |

SWE-bench Verified는 OpenAI가 "부정확 채점·불충분 명세·과도한 유닛테스트"를 고친 인간검증 부분집합. 2026엔 OpenAI가 *Why we no longer evaluate SWE-bench Verified* 를 냈다(프론티어 코딩의 포화 신호).

### 7.2 관측성 / 트레이싱

멀티스텝 에이전트의 실패는 어느 span에서든 발생 → 트레이스로 span tree를 재구성해야 검사·재현·평가가 가능. **OTel GenAI Semantic Conventions**(SIG 2024-04~): 최상위 `invoke_agent` span → 자식 `chat`(LLM 호출)·`execute_tool` span. 표준 속성 `gen_ai.request.model`, `gen_ai.usage.input_tokens/output_tokens`, `gen_ai.response.finish_reasons`, `gen_ai.input.messages`. 플랫폼: **LangSmith, Langfuse(OSS), Arize Phoenix(OTel-native), Braintrust**.

### 7.3 가드레일 & 안전 — Lethal Trifecta

> "The **lethal trifecta** of capabilities is: **Access to your private data**… **Exposure to untrusted content**… and the **ability to externally communicate**… If you combine these three, an attacker can trick your assistant into stealing your private data and sending it to that attacker." — Simon Willison (2025-06-16)

> "A tool that can access your email is a perfect source of untrusted content: an attacker can literally email your LLM and tell it what to do!"

구조적 요점: **프롬프트 하드닝만으론 못 막는다** — LLM은 정당한 지시와 데이터에 주입된 지시를 신뢰성 있게 구분 못 하기 때문. 방어는 **아키텍처적**: 세 다리 중 하나를 제거(외부 통신 차단 or 비신뢰 콘텐츠를 사설 데이터에서 격리).

**레이어드 가드레일**: 모델레벨(RLHF/constitutional) → 입력(별도 모델로 스크리닝) → 툴(권한정책·allowlist) → 프로세스(샌드박싱) → 사람 리뷰(승인 게이트). **3단계 승인**: auto-approve(안전·가역) → notify(회복가능) → block(비가역/고위험, 사람 필수). **최소권한 기본**.

### 7.4 신뢰성 엔지니어링 — checkpointing vs durable execution

> "Reliability comes from designing for partial failure through **retries with backoff, idempotent actions, checkpointing state, circuit breakers, and human escalation paths.**"

**idempotency** — 상태변경 호출은 재시도가 부작용을 중복시키지 않게. 그리고 날카로운 구분:

- **Checkpointing(LangGraph persistence)** — 노드 *사이* 상태 저장, 노드 *안*은 저장 안 함. > "checkpoints are **not** durable execution — a LangGraph run lives in a single process; if that process dies then the run dies with it."
- **Durable Execution(Temporal)** — 그래프를 Workflow로, 노드를 Activity로 실행, 매 노드 체크포인트, **런 자체가 프로세스 죽음을 넘어 생존**. Temporal LangGraph Plugin(2026)이 이 간극을 메움.

### 7.5 코스트 & 지연

**모델 라우팅/캐스케이드**(작은 모델로 대부분 처리, 어려운 케이스만 큰 모델로 에스컬레이트 — 비용 45~85% 절감·품질 95% 유지 보고), **prompt/prefix caching**(Anthropic prefix cache ~90% 비용·~85% 지연 절감; cache read 0.1×), **token budget**(per-run FinOps 한도). Anthropic API는 **task budget**(beta `task-budgets-2026-03-13`)으로 에이전트가 토큰 천장을 인지해 스스로 페이스 조절.

### 7.6 보안 프레임워크

**OWASP** — LLM Top 10(2025): Prompt Injection = **LLM01(#1)**, Excessive Agency = LLM06. **Agentic Applications Top 10(2026)**: goal hijacking·tool misuse·memory/context poisoning + Agent Design/Memory/Planning/Tool Use/Deployment 위협 분류. **MAESTRO**(CSA) — 7계층 위협모델링(foundation model/data/agent framework/deployment/evaluation/orchestration/ecosystem), **교차계층** 분석이 강점.

---

## 8. 상용에서는 뭘 쓰나 — 티어다운

### 8.1 제품별 요약

- **Claude Code / Agent SDK** — 단일 메인 루프(ReAct), 스코프 read 서브에이전트(Task), 스킬 lazy-load, 네이티브 MCP, 훅(PreToolUse…), CLAUDE.md, prompt-cache+auto-compaction. "loop engineering". Agent SDK(내 프로세스) vs Managed Agents(Anthropic 호스팅 샌드박스).
- **Devin(Cognition)** — 클라우드 샌드박스 VM(셸+에디터+헤드리스 브라우저), planner LLM(계획+자기비평) → executor(툴 선택), 벡터화 리포 스냅샷 + 전체 리플레이 트레이스, DeepWiki. ACU 과금. 자기 에세이는 단일스레드 옹호였으나 2026엔 **격리 VM 위임**(Managed Devins)으로 진화.
- **Manus** — 단일 에이전트 + 파일시스템 메모리. KV-cache 우선, mask-don't-remove, todo.md recitation, keep-errors-in. **컨텍스트 엔지니어링 > 모델 학습** 베팅.
- **OpenAI** — **Operator/CUA**(스크린샷→추론→행동 GUI 제어, 가상 컴퓨터), **ChatGPT Agent**(Operator+Deep Research+터미널 통합), **Codex**(codex-1/GPT-5.5, 태스크당 격리 클라우드 샌드박스, AGENTS.md, test-until-pass), **Responses API + Agents SDK + AgentKit**.
- **GitHub Copilot** — "agent mode는 동기(IDE 열려있음), coding agent는 비동기(자는 동안)". Coding agent: **GitHub Issue → GitHub Actions 샌드박스 → PR**, CodeQL·secret scanning 게이트. **CI/PR 플랫폼 자체가 샌드박스+리뷰 게이트**.
- **Cursor 2.0(2025-11)** — 자체 **Composer**(MoE+RL, 4배 빠름), **최대 8 에이전트 병렬**(git worktree/원격 머신), **best-of-N**("여러 모델이 같은 문제를 풀고 최선을 고르면 결과가 유의하게 향상"). Anthropic/Cognition과 정반대 베팅. Turbopuffer 벡터 인덱스, AST 청킹, 커스텀 임베딩.
- **Windsurf(Cascade)** — 컨텍스트 엔진 + Rules + Memories, **M-Query** 딥 인덱싱 + **Fast Context/SWE-grep**(~20배 빠른 검색).
- **Google Jules/Antigravity** — Jules: Google Cloud VM에 리포 클론, plan→execute→PR→teardown, **큐잉 기반**(라이브 채팅 아님). Antigravity: agent-first IDE, Gemini 3, 브라우저 제어, **artifact 기반 검증** 워크플로우.
- **Amazon Bedrock AgentCore** — 프레임워크 불문 조립형(Runtime/Memory/Gateway/Identity/Code Interpreter/Browser/Observability), Gateway가 API·기존 MCP 서버를 툴로 변환. **Q Developer** = 제품화된 패키지 에이전트.
- **Replit Agent 3** — **자가치유 루프**(라이브 브라우저로 자기 앱을 테스트·자동수정), ~200분 자율. **verification-in-the-loop**.
- **Perplexity Comet** — 에이전틱 브라우저, 탭마다 assistant, **브라우저 자체가 하네스/샌드박스**.

### 8.2 단일 vs 멀티에이전트 & 핵심 베팅

| 제품 | 단일/멀티 | 실행 환경 | 컨텍스트/메모리 | 핵심 베팅 |
|---|---|---|---|---|
| Claude Code | 단일 루프 + 스코프 서브 | 로컬 or 매니지드 샌드박스 | CLAUDE.md + 캐시 + 압축, 스킬 lazy | 모델 불문 **하네스**(툴+스킬+훅+MCP) |
| Devin | 단일 선형 + 격리 VM 위임 | 클라우드 VM | 벡터 스냅샷 + 리플레이, DeepWiki | planner→executor, **컨텍스트 엔지니어링** |
| Manus | 단일 + 외부 메모리 | 파일시스템 샌드박스 | **파일시스템=메모리**, KV-cache | **학습보다 컨텍스트** |
| Codex/ChatGPT Agent | 태스크당 단일(Deep Research는 멀티) | 격리 클라우드 샌드박스 | 리포 프리로드, AGENTS.md | RL-on-tests + **샌드박스-per-task** |
| Copilot coding agent | 단일 비동기 | GitHub Actions | Issue-in/PR-out | **CI = 샌드박스+리뷰 게이트** |
| Cursor 2.0 | **멀티(8) + best-of-N** | git worktree/원격 | Turbopuffer 인덱스 | 자체 Composer, 병렬 격리 |
| Jules | 단일 비동기 | Google Cloud VM(휘발) | plan→PR→teardown | **비동기 클라우드 VM** |
| Bedrock AgentCore | 불문 | 서버리스 Runtime | Memory 서비스(TTL·시맨틱) | **조립형 엔터프라이즈 프리미티브** |
| Replit Agent 3 | 단일 자율 | 수천 격리 샌드박스 | ~200분 장기 | **자가치유 검증** |

### 8.3 관통하는 7가지 엔지니어링 교훈

1. **컨텍스트 엔지니어링 > 프롬프트 엔지니어링** — Cognition·Manus·Anthropic이 독립적으로 "#1 job"이라 명명.
2. **KV-cache 안정성이 지배적 비용/지연 레버** — 프리픽스를 절대 변형 말 것, 툴은 삭제 대신 마스킹.
3. **메모리를 파일시스템으로 외부화** — 컨텍스트 창은 휘발성 RAM.
4. **샌드박스-per-task/클라우드 VM** 이 거의 보편적 실행 기질.
5. **단일 vs 멀티는 작업 형태로 갈린다** — 읽기/검색은 병렬, 쓰기/코딩은 단일 스레드나 격리. 쓰기 에이전트 간 대화형 협업이 모두가 부딪힌 실패 모드.
6. **에러를 컨텍스트에 남겨라** — 숨기면 복구 신호를 잃는다.
7. **검증을 루프 안에** — Replit 자가치유, Codex test-until-pass, Devin 자기비평.

---

## 9. 종합: "가장 복잡한 에이전트"의 전체 조립도

이제 8개 레이어를 하나로 조립하면, 우리가 상정한 가장 복잡한 에이전트는 이렇게 생긴다.

```
[사용자 목표: "이 리포지토리에 기능 X를 구현하고 PR을 올려라"]
        │
        ▼
┌────────────────────────────────────────────────────────────────┐
│ 하네스 (single main loop, gather→act→verify→repeat)              │  ← L1
│  · 시스템프롬프트: right altitude, 섹션 구조                       │  ← L2 컨텍스트 엔지니어링
│  · KV-cache 안정 프리픽스 / append-only / logit masking          │
│                                                                  │
│  루프 매 스텝:                                                    │
│   1) gather: JIT 검색 — 파일 경로/쿼리로 필요한 것만 로드          │  ← L2/L4
│      · 스킬 L1 메타데이터(~100토큰)만 상주, 트리거 시 L2 로드      │  ← L3 스킬
│      · agentic RAG(계획→multi-hop→CRAG 폴백, 하이브리드+rerank)   │  ← L4 RAG
│      · 메모리 tool로 /memories 되읽기 (semantic/episodic/proc.)   │  ← L4 메모리
│   2) act: 툴/MCP 호출 — 수백 툴은 Tool Search(defer_loading)      │  ← L3 툴/MCP
│      · 다단계 체인은 code mode(programmatic tool calling)로 압축   │  ← L3 code mode
│      · 계획은 todo.md에 recite, ReAct/Plan-and-Execute 하이브리드 │  ← L5 플래닝
│      · 병렬화 가능한 조사는 서브에이전트 팬아웃(격리 창)           │  ← L6 멀티에이전트
│   3) verify: 테스트 게이트 / evaluator-optimizer / LLM 심판        │  ← L5/L7
│      · 실패·스택트레이스는 컨텍스트에 남김(keep-errors-in)         │
│   4) 컨텍스트 한계 근처: compaction + 진행상황을 파일에 기록        │  ← L2 write
│                                                                  │
│  교대근무 핸드오프: feature-list.json + git commit + init.sh      │  ← L1 장기실행
└────────────────────────────────────────────────────────────────┘
        │  (전 과정)
        ▼
[관측: OTel span tree] [가드레일: lethal trifecta 방어, 승인 게이트]   ← L7
[신뢰성: durable execution, 체크포인트/재시도] [코스트: 라우팅/캐시/버짓]
        │
        ▼
[격리 샌드박스 VM에서 실행 → PR 생성 → CodeQL/리뷰 게이트]            ← L8 상용 패턴
```

**결론.** 2026년의 "복잡한 에이전트"는 더 똑똑한 프롬프트가 아니라 **더 잘 설계된 시스템**이다. 모델은 상수에 가깝게 강력해졌고, 차별화는 **하네스가 유한한 attention budget을 어떻게 관리하느냐**로 넘어왔다 — 무엇을 컨텍스트에 넣고(스킬·툴·메모리를 progressive disclosure로), 무엇을 밖으로 빼고(파일시스템·서브에이전트), 무엇을 검증하고(테스트·심판), 무엇을 감사·복구하느냐(트레이스·durable execution). 상용 제품들의 겉모습은 제각각이지만, 벗겨 보면 모두 이 8개 레이어의 조합이고, 그 조합을 관통하는 원칙은 하나다 — **컨텍스트 경제**.

---

## 참고문헌 (핵심)

**하네스 / 컨텍스트 엔지니어링**
- Anthropic, *Building effective agents* — https://www.anthropic.com/engineering/building-effective-agents (2024-12)
- Anthropic, *Effective context engineering for AI agents* — https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents (2025-09)
- Anthropic, *Building agents with the Claude Agent SDK* — https://www.anthropic.com/engineering/building-agents-with-the-claude-agent-sdk (2025)
- Anthropic, *Effective harnesses for long-running agents* — https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents (2025-11)
- Chroma, *Context Rot* — https://research.trychroma.com/context-rot (2025-07)
- Manus (Yichao Ji), *Context Engineering for AI Agents: Lessons from Building Manus* — https://manus.im/blog/Context-Engineering-for-AI-Agents-Lessons-from-Building-Manus (2025-07)
- LangChain / Lance Martin, *Context Engineering for Agents* — https://www.langchain.com/blog/context-engineering-for-agents (2025)
- OpenAI, *Unrolling the Codex agent loop* — https://openai.com/index/unrolling-the-codex-agent-loop/ (2026-01)

**툴 / MCP / 스킬**
- modelcontextprotocol.io — *Architecture / Server concepts* — https://modelcontextprotocol.io/docs/learn/architecture (2024~)
- Anthropic, *Writing effective tools for AI agents* — https://www.anthropic.com/engineering/writing-tools-for-agents (2025-09)
- Anthropic, *Equipping agents for the real world with Agent Skills* — https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills (2025-10-16)
- anthropics/skills — https://github.com/anthropics/skills
- Anthropic, *Code execution with MCP* — https://www.anthropic.com/engineering/code-execution-with-mcp (2025-11-04)
- Cloudflare, *Code Mode: the better way to use MCP* — https://blog.cloudflare.com/code-mode/ (2025)

**메모리 / RAG**
- Packer et al., *MemGPT: Towards LLMs as Operating Systems* — https://arxiv.org/abs/2310.08560 (2023-10)
- Anthropic, *Memory tool / Context editing* — https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool
- Mem0 — https://arxiv.org/abs/2504.19413 (2025-04) · Zep — https://arxiv.org/abs/2501.13956 (2025-01)
- Self-RAG — https://arxiv.org/abs/2310.11511 · CRAG — https://arxiv.org/abs/2401.15884
- Microsoft GraphRAG — https://microsoft.github.io/graphrag/
- Drew Breunig, *How Long Contexts Fail* — https://simonwillison.net/2025/Jun/29/how-to-fix-your-context/

**플래닝 / 추론**
- ReAct — https://arxiv.org/abs/2210.03629 · Reflexion — https://arxiv.org/abs/2303.11366 · Self-Refine — https://arxiv.org/abs/2303.17651
- ReWOO — https://arxiv.org/abs/2305.18323 · LLM Compiler — https://arxiv.org/abs/2312.04511 · Tree of Thoughts — https://arxiv.org/abs/2305.10601
- Self-Consistency — https://arxiv.org/abs/2203.11171 · LLM-as-Judge — https://arxiv.org/abs/2306.05685
- Snell et al., *Scaling LLM Test-Time Compute Optimally* — https://arxiv.org/abs/2408.03314

**멀티에이전트**
- Anthropic, *How we built our multi-agent research system* — https://www.anthropic.com/engineering/multi-agent-research-system (2025-06)
- Cognition (Walden Yan), *Don't Build Multi-Agents* — https://cognition.com/blog/dont-build-multi-agents (2025-06)
- LangChain, *How and when to build multi-agent systems* — https://www.langchain.com/blog/how-and-when-to-build-multi-agent-systems
- A2A Protocol Specification — https://a2a-protocol.org/latest/specification/
- MAST, *Why Do Multi-Agent LLM Systems Fail?* — https://openreview.net/forum?id=fAjbYBmonr

**평가 / 관측 / 가드레일**
- Simon Willison, *The lethal trifecta for AI agents* — https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/
- OpenAI, *Introducing SWE-bench Verified* — https://openai.com/index/introducing-swe-bench-verified/
- Meta, *GAIA* — https://arxiv.org/abs/2311.12983 · Sierra, *τ-bench* — https://arxiv.org/abs/2406.12045
- OpenTelemetry, *GenAI Observability* — https://opentelemetry.io/blog/2026/genai-observability/
- OWASP, *Top 10 for Agentic Applications 2026* — https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/
- CSA, *MAESTRO* — https://cloudsecurityalliance.org/blog/2025/02/06/agentic-ai-threat-modeling-framework-maestro

**상용 프로덕션**
- Claude Agent SDK docs — https://code.claude.com/docs/en/agent-sdk/overview
- OpenAI, *Introducing Codex / Operator* — https://openai.com/index/introducing-codex/ · https://openai.com/index/introducing-operator/
- Cursor, *Introducing Cursor 2.0 and Composer* — https://cursor.com/blog/2-0
- Google, *Jules / Antigravity* — https://blog.google/innovation-and-ai/models-and-research/google-labs/jules/
- AWS, *Bedrock AgentCore GA* — https://aws.amazon.com/about-aws/whats-new/2025/10/amazon-bedrock-agentcore-available

> **소싱 노트**: 본 리서치는 병렬 리서치 에이전트들이 주로 WebSearch로 수집했다(이 환경의 egress 정책이 anthropic.com·arxiv.org 등 다수 1차 호스트에 대한 직접 fetch를 403 차단). arXiv ID·URL은 정확하고 안정적이며, 인용문 대부분은 검색이 노출한 verbatim 구절이다. 다만 출판 전에는 (1) Anthropic "smallest possible set of high-signal tokens" 문장, (2) Manus "$0.30 vs $3.00 / 10×" 수치, (3) Cognition Principle 1·2 문구, (4) Anthropic 멀티에이전트 90.2%·15× 수치 — 이 네 개의 load-bearing 인용/수치를 원문 페이지에서 최종 대조할 것을 권장한다.
