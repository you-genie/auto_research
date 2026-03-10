# Chainlit 완전 정복: LLM 챗봇 UI를 분 단위로 만드는 프레임워크

> 작성일: 2026-03-10
> 키워드: Chainlit, LLM, 챗봇, LangGraph, LangChain, 대화형 AI, Python

---

## 목차

1. [Chainlit이란 무엇인가?](#1-chainlit이란-무엇인가)
2. [설치 및 첫 번째 앱 실행](#2-설치-및-첫-번째-앱-실행)
3. [핵심 아키텍처 및 개념](#3-핵심-아키텍처-및-개념)
4. [핵심 기능 상세](#4-핵심-기능-상세)
5. [다른 프레임워크와 비교](#5-다른-프레임워크와-비교)
6. [LangChain / LangGraph 통합](#6-langchain--langgraph-통합)
7. [실제 활용 사례 및 베스트 프랙티스](#7-실제-활용-사례-및-베스트-프랙티스)
8. [프로덕션 배포 가이드](#8-프로덕션-배포-가이드)
9. [최신 트렌드 및 커뮤니티 동향](#9-최신-트렌드-및-커뮤니티-동향)
10. [마치며](#10-마치며)

---

## 1. Chainlit이란 무엇인가?

솔직히 LLM 앱 만들 때 제일 귀찮은 게 뭔지 알아요? 백엔드 로직은 금방 짰는데, UI 만드는 데 시간을 다 써버리는 거거든요. 채팅 버블, 스트리밍 응답, 파일 업로드, 인증... 이걸 다 직접 만들려면 며칠은 각오해야 해요.

그래서 [Chainlit](https://chainlit.io/)이 나왔습니다.

> "Build production ready Conversational AI in minutes, not weeks."
> — Chainlit 공식 홈페이지

한국말로 하면 "몇 주 걸릴 일을 몇 분 안에"인데, 이게 그냥 마케팅 멘트가 아니에요. 실제로 `pip install chainlit` 하고 파이썬 파일 5줄 적으면 완성된 채팅 UI가 뜨거든요.

### 1.1 역사와 배경

Chainlit은 [GitHub](https://github.com/Chainlit/chainlit)에서 오픈소스로 개발된 Python 기반 프레임워크예요. 현재 기준(2026년 3월)으로:

- **스타**: 11,700+
- **포크**: 1,700+
- **의존 프로젝트**: 11,400+
- **총 릴리스**: 163개
- **라이선스**: Apache 2.0

2025년 5월 1일부터는 원래 팀이 개발을 중단하고, `@Chainlit/chainlit-maintainers`라는 커뮤니티 유지보수 그룹이 공식 관리를 맡고 있어요. 그래도 개발은 계속 되고 있고, 2026년 3월 5일에 버전 2.10.0이 릴리스됐을 정도니까 걱정 안 해도 돼요.

### 1.2 Chainlit의 목적

Chainlit은 **AI/LLM 개발자를 위한 전용 UI 프레임워크**예요. 범용 대시보드 도구가 아니라, 처음부터 "대화형 AI 인터페이스"를 만들기 위해 설계됐죠. 그래서:

- 채팅 메시지 버블, 타이핑 인디케이터 등이 기본 내장
- LLM 응답 스트리밍이 기본 지원
- LangChain, LlamaIndex 등 AI 프레임워크와 네이티브 통합
- 엔터프라이즈급 인증, 모니터링, 데이터 영속성 지원

이런 것들이 다 기본으로 들어있어요. 직접 만들 필요가 없는 거죠.

---

## 2. 설치 및 첫 번째 앱 실행

### 2.1 설치

```bash
pip install chainlit
```

그게 전부예요. 추가로 OpenAI나 다른 LLM 라이브러리가 필요하면 같이 설치하면 됩니다.

```bash
pip install chainlit openai python-dotenv
```

### 2.2 Hello World

`app.py` 파일을 만들고:

```python
import chainlit as cl

@cl.on_message
async def main(message: cl.Message):
    # 사용자 메시지를 그대로 돌려주는 에코 봇
    await cl.Message(
        content=f"받은 메시지: {message.content}",
    ).send()
```

그리고 실행:

```bash
chainlit run app.py -w
```

`-w`는 파일 변경 시 자동 재시작 옵션이에요. 브라우저에서 `http://localhost:8000`으로 접속하면 완성된 채팅 UI가 딱 뜹니다. 진짜로요.

---

## 3. 핵심 아키텍처 및 개념

[공식 문서](https://docs.chainlit.io/get-started/overview)에 따르면 Chainlit은 하이브리드 아키텍처를 사용해요.

### 3.1 전체 구조

```
┌─────────────────────────────────────────────┐
│              사용자 브라우저                   │
│  ┌─────────────────────────────────────────┐ │
│  │     React 기반 프론트엔드 (TypeScript)    │ │
│  │  - 채팅 UI 컴포넌트                      │ │
│  │  - Shadcn/Tailwind (v2.0+ 완전 재작성)   │ │
│  └──────────────────┬──────────────────────┘ │
└─────────────────────┼───────────────────────┘
                      │ WebSocket / HTTP
┌─────────────────────┼───────────────────────┐
│              Python 백엔드                   │
│  ┌──────────────────┴──────────────────────┐ │
│  │         Chainlit 런타임                  │ │
│  │  @cl.on_chat_start                      │ │
│  │  @cl.on_message                         │ │
│  │  @cl.on_stop                            │ │
│  └──────────────────┬──────────────────────┘ │
│                     │                        │
│  ┌──────────────────┴──────────────────────┐ │
│  │      LLM / AI 통합 레이어               │ │
│  │  LangChain, LangGraph, OpenAI, ...      │ │
│  └─────────────────────────────────────────┘ │
└─────────────────────────────────────────────┘
```

### 3.2 핵심 데코레이터

Chainlit의 핵심은 이 데코레이터들이에요. Flask처럼 간단해서 금방 익힐 수 있거든요.

| 데코레이터 | 역할 | 언제 호출되나 |
|-----------|------|--------------|
| `@cl.on_chat_start` | 초기화 | 채팅 세션이 시작될 때 |
| `@cl.on_message` | 메시지 처리 | 사용자가 메시지를 보낼 때 |
| `@cl.on_stop` | 정지 처리 | 사용자가 응답 생성을 중단할 때 |
| `@cl.on_chat_end` | 종료 처리 | 채팅 세션이 끝날 때 |
| `@cl.on_chat_resume` | 재개 처리 | 이전 세션을 재개할 때 |
| `@cl.password_auth_callback` | 인증 처리 | 패스워드 인증 시 |
| `@cl.oauth_callback` | OAuth 처리 | OAuth 로그인 시 |

### 3.3 cl.user_session - 사용자 세션의 핵심

[공식 세션 문서](https://docs.chainlit.io/concepts/user-session)를 보면, Chainlit은 멀티유저 환경에서 **각 사용자마다 독립된 세션 공간**을 제공해요.

> "The user session is designed to persist data in memory through the life cycle of a chat session. It is unique per user and per session."
> — Chainlit 공식 문서

이게 왜 중요하냐면, 전역 변수 쓰면 사용자 A의 데이터가 사용자 B한테 섞이는 참사가 벌어지거든요.

```python
# 위험한 방법 (전역 변수)
chat_history = []  # 모든 사용자가 공유!

# 올바른 방법 (user_session)
@cl.on_chat_start
def on_chat_start():
    cl.user_session.set("chat_history", [])

@cl.on_message
async def on_message(message: cl.Message):
    history = cl.user_session.get("chat_history")
    history.append(message.content)
    cl.user_session.set("chat_history", history)
```

예약된 기본 키들도 있어요:
- `id`: 세션 고유 ID
- `user`: 인증된 사용자 객체
- `chat_profile`: 선택된 채팅 프로필
- `chat_settings`: 사용자 설정값
- `env`: 환경 변수

---

## 4. 핵심 기능 상세

### 4.1 메시지 스트리밍

LLM 응답을 실시간으로 스트리밍하는 건 현대 챗봇의 기본이죠. Chainlit은 이걸 아주 깔끔하게 처리해요.

```python
@cl.on_message
async def on_message(message: cl.Message):
    msg = cl.Message(content="")
    await msg.send()

    # 스트리밍 방식으로 토큰 하나씩 추가
    async for token in some_streaming_llm():
        await msg.stream_token(token)

    await msg.update()
```

### 4.2 멀티모달 지원

[공식 멀티모달 문서](https://docs.chainlit.io/advanced-features/multi-modal)에 따르면 Chainlit은 텍스트 외에도 다양한 미디어 타입을 지원해요.

#### 파일 업로드

사용자가 드래그&드롭이나 버튼으로 파일을 첨부할 수 있어요:

```python
@cl.on_message
async def on_message(msg: cl.Message):
    if not msg.elements:
        await cl.Message(content="파일이 없어요!").send()
        return

    # 이미지 파일만 필터링
    images = [file for file in msg.elements if "image" in file.mime]

    for image in images:
        # image.path에서 파일 경로 접근
        # image.content에서 바이트 데이터 접근
        pass

    await cl.Message(content=f"{len(images)}개 이미지를 받았어요!").send()
```

파일 업로드 비활성화가 필요하면 `.chainlit/config.toml`에서:

```toml
[features.spontaneous_file_upload]
enabled = false
```

#### 음성 지원

`@cl.on_audio_chunk` 데코레이터로 실시간 오디오 스트림에 접근 가능해요. OpenAI Realtime API와 통합하면 음성 어시스턴트도 만들 수 있죠.

#### 다양한 요소 표시

```python
# 이미지 표시
image = cl.Image(path="./image.png", name="샘플 이미지", display="inline")
await cl.Message(content="이미지예요:", elements=[image]).send()

# PDF 표시
pdf = cl.Pdf(path="./doc.pdf", display="side")
await cl.Message(content="문서 확인해주세요:", elements=[pdf]).send()

# 플롯 표시
fig = go.Figure(...)  # plotly
chart = cl.Plotly(figure=fig, display="inline")
await cl.Message(content="차트:", elements=[chart]).send()
```

### 4.3 인증 시스템

엔터프라이즈 환경에서 인증은 필수죠. Chainlit은 여러 방식을 지원해요.

#### 패스워드 기반 인증

```python
import chainlit as cl
from chainlit.types import ThreadDict

@cl.password_auth_callback
def auth_callback(username: str, password: str):
    # 실제 환경에서는 DB 조회 필요
    if (username, password) == ("admin", "secret"):
        return cl.User(identifier="admin", metadata={"role": "admin"})
    return None
```

#### OAuth 인증

Google, GitHub, Azure AD 등 OAuth 제공자 지원:

```python
@cl.oauth_callback
def oauth_callback(
    provider_id: str,
    token: str,
    raw_user_data: dict,
    default_user: cl.User,
) -> cl.User | None:
    if provider_id == "google":
        if raw_user_data.get("hd") == "mycompany.com":  # 도메인 제한
            return default_user
    return None
```

`config.toml` 설정:

```toml
[auth]
[auth.oauth]
providers = ["google", "github"]
```

#### JWT 토큰 인증

API 기반 접근이 필요하면 JWT 인증도 사용 가능해요.

### 4.4 데이터 영속성 (Data Layer)

[DeepWiki 문서](https://deepwiki.com/Chainlit/chainlit/3.4-session-management)에 따르면, Chainlit은 기본 인메모리 저장 외에도 다양한 데이터 레이어를 제공해요.

```python
from chainlit.data import BaseDataLayer
import chainlit as cl

class CustomDataLayer(BaseDataLayer):
    async def get_user(self, identifier: str):
        # DB에서 사용자 조회
        ...

    async def create_user(self, user: cl.User):
        # DB에 사용자 저장
        ...

    async def upsert_feedback(self, feedback: cl.Feedback):
        # 피드백 저장
        ...

# 데이터 레이어 등록 (v2.0+ 새로운 방식)
@cl.data_layer
def get_data_layer():
    return CustomDataLayer()
```

Literal AI(Chainlit 팀의 관찰 가능성 플랫폼)와 통합하면 모든 대화를 자동으로 저장하고 분석할 수 있어요.

### 4.5 단계별 추론 시각화 (Steps)

LLM이 어떤 과정을 거쳐 답을 냈는지 사용자에게 보여줄 수 있어요:

```python
@cl.on_message
async def on_message(message: cl.Message):
    async with cl.Step(name="검색") as step:
        step.input = message.content
        results = await search_documents(message.content)
        step.output = f"{len(results)}개 문서 발견"

    async with cl.Step(name="분석") as step:
        analysis = await analyze(results)
        step.output = analysis

    await cl.Message(content=analysis).send()
```

사용자 화면에 각 단계가 접을 수 있는 UI로 표시돼요. 디버깅할 때도 유용하고, 사용자 신뢰도 높아지거든요.

### 4.6 채팅 프로필

여러 AI 페르소나나 모드를 제공할 수 있어요:

```python
@cl.set_chat_profiles
async def chat_profile():
    return [
        cl.ChatProfile(
            name="GPT-4o",
            markdown_description="**GPT-4o** 모델을 사용합니다.",
            icon="https://openai.com/favicon.ico",
        ),
        cl.ChatProfile(
            name="Claude",
            markdown_description="**Claude** 모델을 사용합니다.",
        ),
    ]
```

### 4.7 실시간 설정 (Chat Settings)

채팅 중에도 사용자가 설정을 바꿀 수 있어요:

```python
@cl.on_chat_start
async def on_chat_start():
    settings = await cl.ChatSettings(
        [
            cl.input_widget.Select(
                id="model",
                label="AI 모델",
                values=["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet"],
                initial_index=0,
            ),
            cl.input_widget.Slider(
                id="temperature",
                label="Temperature",
                initial=0.7,
                min=0,
                max=2,
                step=0.1,
            ),
        ]
    ).send()
```

---

## 5. 다른 프레임워크와 비교

[getstream.io 비교 가이드](https://getstream.io/blog/ai-chat-ui-tools/)와 [markaicode 비교](https://markaicode.com/streamlit-vs-gradio-vs-chainlit-llm-ui-framework/)를 바탕으로 정리했어요.

### 5.1 전체 비교표

| 항목 | Chainlit | Streamlit | Gradio |
|------|----------|-----------|--------|
| **주요 용도** | 대화형 AI 전용 | 데이터 앱/대시보드 | ML 모델 데모 |
| **학습 곡선** | 낮음 (AI 개발자 친화적) | 낮음 | 매우 낮음 |
| **채팅 UI 품질** | 최상 (네이티브) | 보통 (추가 코드 필요) | 보통 |
| **스트리밍** | 네이티브 지원 | 지원 | 지원 |
| **파일 업로드** | 네이티브 지원 | 지원 | 지원 |
| **인증** | 내장 (OAuth, Password, JWT) | 제한적 | 제한적 |
| **모니터링** | Literal AI 통합 | 제한적 | 없음 |
| **멀티모달** | 내장 지원 | 제한적 | 우수 |
| **커스터마이징** | 높음 | 높음 | 중간 |
| **멀티플랫폼** | Slack/Discord/Teams | 웹 전용 | 웹/HuggingFace |
| **프로덕션 준비도** | 높음 | 중간 | 낮음 |
| **LangChain 통합** | 네이티브 콜백 | 직접 구현 | 직접 구현 |

### 5.2 언제 뭘 써야 하나

**Chainlit을 선택하세요:**
- 챗봇이나 대화형 AI 에이전트를 만들 때
- 프로덕션 레벨의 인증과 보안이 필요할 때
- LangChain/LangGraph 기반 앱을 빠르게 프로토타이핑할 때
- 사용자 대화를 모니터링하고 분석해야 할 때
- Slack, Discord, Teams 등에 배포해야 할 때

**Streamlit을 선택하세요:**
- 데이터 시각화와 대시보드가 주 목적일 때
- 다양한 입력 위젯(슬라이더, 선택박스 등)이 많이 필요할 때
- 채팅이 아닌 범용 데이터 앱을 만들 때

**Gradio를 선택하세요:**
- 빠른 ML 모델 데모가 필요할 때
- HuggingFace Spaces에 배포할 때
- 이미지 생성, 음성 인식 같은 특화 AI 태스크 UI가 필요할 때

> "Chainlit delivers the best experience for conversational AI and is ideal for chatbots, LangChain applications, and real-time chat interfaces."
> — getstream.io, 2025

---

## 6. LangChain / LangGraph 통합

이게 Chainlit의 진짜 강점 중 하나예요. [공식 통합 문서](https://docs.chainlit.io/integrations/langchain)에 따르면 네이티브 콜백 핸들러를 제공해서 LangChain의 중간 단계를 자동으로 UI에 표시해줘요.

### 6.1 LangChain LCEL 통합

```python
import chainlit as cl
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain.schema.runnable.config import RunnableConfig

@cl.on_chat_start
async def on_chat_start():
    model = ChatOpenAI(streaming=True)
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 도움이 되는 AI 어시스턴트입니다."),
        ("human", "{question}")
    ])

    runnable = prompt | model | StrOutputParser()
    cl.user_session.set("runnable", runnable)

@cl.on_message
async def on_message(message: cl.Message):
    runnable = cl.user_session.get("runnable")

    msg = cl.Message(content="")
    await msg.send()

    async for chunk in runnable.astream(
        {"question": message.content},
        config=RunnableConfig(
            callbacks=[cl.LangchainCallbackHandler()]
        )
    ):
        await msg.stream_token(chunk)

    await msg.update()
```

> "콜백 핸들러는 체인의 중간 단계를 감지하고 UI로 전달하는 역할을 담당하여 실시간 응답 스트리밍을 가능하게 합니다."
> — Chainlit 공식 문서

### 6.2 LangGraph 통합

[brucechou1983/chainlit_langgraph](https://github.com/brucechou1983/chainlit_langgraph) 등의 커뮤니티 프로젝트에서 LangGraph 통합 패턴이 잘 정리되어 있어요.

```python
import chainlit as cl
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI

# LangGraph 그래프 정의
model = ChatOpenAI(model="gpt-4o", streaming=True)
memory = MemorySaver()

def call_model(state: MessagesState):
    response = model.invoke(state["messages"])
    return {"messages": [response]}

workflow = StateGraph(MessagesState)
workflow.add_node("model", call_model)
workflow.add_edge(START, "model")
workflow.add_edge("model", END)
graph = workflow.compile(checkpointer=memory)

@cl.on_chat_start
async def on_chat_start():
    thread_id = cl.user_session.get("id")
    cl.user_session.set("thread_id", thread_id)

@cl.on_message
async def on_message(message: cl.Message):
    thread_id = cl.user_session.get("thread_id")
    config = {"configurable": {"thread_id": thread_id}}

    msg = cl.Message(content="")
    await msg.send()

    # LangGraph 스트리밍 실행
    async for event in graph.astream_events(
        {"messages": [("human", message.content)]},
        config=config,
        version="v2"
    ):
        kind = event["event"]
        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if chunk.content:
                await msg.stream_token(chunk.content)

    await msg.update()
```

[DEV 커뮤니티 튜토리얼](https://dev.to/jamesbmour/building-a-simple-chatbot-with-langgraph-and-chainlit-a-step-by-step-tutorial-4k6h)에 의하면 MemorySaver를 사용하면 대화 기록이 자동으로 유지되어 멀티턴 대화가 가능해요.

> "MemorySaver is LangGraph's way of checkpointing the state—it's in-memory here, but you could swap it for something persistent like a database for production."
> — James B Mour, DEV Community, 2025

### 6.3 LangGraph 멀티 에이전트 패턴

여러 전문화된 에이전트를 연결하는 패턴:

```python
from langgraph.graph import StateGraph, END
from langgraph_supervisor import create_supervisor
from langgraph.prebuilt import create_react_agent

# 전문 에이전트 정의
search_agent = create_react_agent(model, tools=[search_tool])
code_agent = create_react_agent(model, tools=[python_repl_tool])

# 슈퍼바이저가 라우팅 결정
supervisor = create_supervisor(
    agents=[search_agent, code_agent],
    model=model
)
```

---

## 7. 실제 활용 사례 및 베스트 프랙티스

### 7.1 주요 활용 사례

1. **RAG(검색 증강 생성) 챗봇** - 기업 문서 검색 + 대화
   - [Medium: RAG in Production with LangChain and Chainlit](https://medium.com/@justinduy/rag-in-production-with-langchain-and-chainlit-86c2dea0ca40)

2. **고객 지원 자동화** - 인증된 사용자별 맞춤 응답

3. **코드 어시스턴트** - Python REPL 도구와 통합

4. **문서 분석 챗봇** - PDF/Excel 파일 업로드 후 Q&A

5. **멀티모달 에이전트** - 이미지 분석 + 텍스트 응답

6. **음성 어시스턴트** - OpenAI Realtime API 통합

### 7.2 베스트 프랙티스

#### 상태 관리

```python
# 복잡한 상태는 Pydantic 모델로 정의
from pydantic import BaseModel

class ChatState(BaseModel):
    history: list = []
    user_preferences: dict = {}
    session_start: str = ""

@cl.on_chat_start
async def on_chat_start():
    state = ChatState()
    cl.user_session.set("state", state)
```

#### 에러 처리

```python
@cl.on_message
async def on_message(message: cl.Message):
    try:
        # 처리 로직
        ...
    except Exception as e:
        await cl.Message(
            content=f"오류가 발생했어요: {str(e)}",
            author="System"
        ).send()
```

#### 로딩 상태 표시

```python
@cl.on_message
async def on_message(message: cl.Message):
    # 처리 중 메시지 표시
    async with cl.Step(name="처리 중...") as step:
        result = await heavy_processing()
        step.output = "완료"

    await cl.Message(content=result).send()
```

#### 환경 변수 관리

```python
# .env 파일 사용
from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
```

---

## 8. 프로덕션 배포 가이드

[공식 배포 문서](https://docs.chainlit.io/deploy/overview)에 따르면 다양한 배포 옵션을 제공해요.

### 8.1 기본 실행 명령

```bash
# 개발 환경
chainlit run app.py -w

# 프로덕션 환경 (브라우저 자동 열기 방지)
chainlit run app.py -h --host 0.0.0.0 --port 8000
```

### 8.2 Docker 배포

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000
CMD ["chainlit", "run", "app.py", "-h", "--host", "0.0.0.0", "--port", "8000"]
```

### 8.3 지원하는 클라우드 플랫폼

| 플랫폼 | 특징 |
|--------|------|
| Ploomber Cloud | Chainlit 공식 파트너 |
| AWS ECS | 컨테이너 기반, 쿡북 예제 있음 |
| Google Cloud Run | 서버리스 |
| Azure Container | 엔터프라이즈 |
| HuggingFace Spaces | 무료 배포 |
| Render, Fly.io | 간단한 PaaS |

### 8.4 주요 프로덕션 고려사항

- **WebSocket 지원**: 로드밸런서에서 sticky session(세션 어피니티) 활성화 필수
- **서브경로 배포**: `--root-path /chatbot` 플래그 사용
- **CORS 설정**: `config.toml`의 `allow_origins` 수정
- **확장성**: 다중 인스턴스 시 Redis 기반 세션 공유 고려

---

## 9. 최신 트렌드 및 커뮤니티 동향

### 9.1 버전 2.0의 주요 변화

[PyPI 기록](https://pypi.org/project/chainlit/)에 따르면 버전 2.0에서 큰 변화가 있었어요:

- **UI 완전 재작성**: Shadcn/Tailwind 기반으로 새로운 디자인 시스템
- **`@data_layer` 데코레이터**: 커스텀 데이터 레이어를 선언적으로 설정
- **모드 선택**: LLM 모델, 플래닝 모드, 추론 모드 선택 UI 추가
- **멀티 에이전트 지원 강화**: 중첩 단계(nested steps) 개선
- **마이그레이션 가이드**: v1.x에서 v2.0으로 마이그레이션 가이드 제공

### 9.2 커뮤니티 생태계

[GitHub](https://github.com/Chainlit/chainlit)의 11,700+ 스타가 보여주듯, 커뮤니티가 활발해요:

- **Chainlit Cookbook**: 공식 예제 모음 저장소
- **Discord**: 개발자 커뮤니티 (문서에서 링크 제공)
- **DeepWiki**: 아키텍처 심층 문서
- **커뮤니티 통합 라이브러리**: chainlit_langgraph, LlamaIndex 통합 등

### 9.3 2025-2026 주요 트렌드

1. **MCP(Model Context Protocol) 통합**: LangGraph + Chainlit + MCP 조합
   - [Medium: Building a Weather Agent with LangGraph, Chainlit & MCP](https://medium.com/@dominicschneider_7223/%EF%B8%8F-building-a-weather-agent-with-langgraph-chainlit-mcp-your-first-modular-ai-tool-6208bbb3d693)

2. **멀티 에이전트 시스템**: 여러 전문화된 에이전트를 오케스트레이션

3. **음성 인터페이스**: OpenAI Realtime API와의 결합으로 음성 지원 강화

4. **AWS Bedrock 통합**: 기업 환경의 AWS 생태계와 결합
   - [Gonzalo123: Chat with your Data with AWS Bedrock and Chainlit](https://gonzalo123.com/2025/12/09/chat-with-your-data-building-a-file-aware-ai-agent-with-aws-bedrock-and-chainlit/)

5. **보안 취약점 대응**: 2026년 1월 파일 읽기/SSRF 취약점 패치
   - [The Hacker News: Chainlit AI Framework Flaws Enable Data Theft](https://thehackernews.com/2026/01/chainlit-ai-framework-flaws-enable-data.html)
   - 최신 버전으로 업데이트 필수!

---

## 10. 마치며

Chainlit은 "LLM 앱을 빠르게 만들고 싶은 개발자"에게 정말 잘 맞는 도구예요. Streamlit이나 Gradio처럼 범용으로 쓰기보다는, 대화형 AI에 특화되어 있어서 그 분야에선 타의 추종을 불허하거든요.

특히 이런 분들한테 적극 추천해요:

- **LangChain/LangGraph 쓰는 분들**: 네이티브 통합이라 진짜 편함
- **프로덕션 배포까지 생각하는 분들**: 인증, 모니터링, 데이터 레이어 다 준비됨
- **AI 에이전트 프로토타입이 필요한 분들**: 아이디어를 빠르게 검증 가능

물론 단점도 있어요. 2025년 5월부터 원래 팀이 빠지고 커뮤니티 유지보수로 전환됐다는 게 리스크요. 그래도 11,700+ 스타와 활발한 커뮤니티, 꾸준한 릴리스를 보면 당분간은 걱정 없을 것 같아요.

다음 챗봇 프로젝트에 Chainlit 한번 써보세요. 진짜 빠릅니다 ㅎㅎ

---

## 참고문헌

1. [Chainlit 공식 문서 - 개요](https://docs.chainlit.io/get-started/overview)
2. [Chainlit GitHub 리포지토리](https://github.com/Chainlit/chainlit)
3. [Chainlit 공식 홈페이지](https://chainlit.io/)
4. [Chainlit PyPI](https://pypi.org/project/chainlit/)
5. [Chainlit 사용자 세션 문서](https://docs.chainlit.io/concepts/user-session)
6. [Chainlit 멀티모달 문서](https://docs.chainlit.io/advanced-features/multi-modal)
7. [Chainlit LangChain 통합 문서](https://docs.chainlit.io/integrations/langchain)
8. [Chainlit 배포 문서](https://docs.chainlit.io/deploy/overview)
9. [DeepWiki - Chainlit 세션 관리](https://deepwiki.com/Chainlit/chainlit/3.4-session-management)
10. [DeepWiki - Chainlit 인증](https://deepwiki.com/Chainlit/chainlit/8-authentication)
11. [getstream.io - Python AI 챗 UI 비교](https://getstream.io/blog/ai-chat-ui-tools/)
12. [markaicode - Streamlit vs Gradio vs Chainlit](https://markaicode.com/streamlit-vs-gradio-vs-chainlit-llm-ui-framework/)
13. [DEV Community - LangGraph + Chainlit 튜토리얼](https://dev.to/jamesbmour/building-a-simple-chatbot-with-langgraph-and-chainlit-a-step-by-step-tutorial-4k6h)
14. [brucechou1983/chainlit_langgraph GitHub](https://github.com/brucechou1983/chainlit_langgraph)
15. [Medium - RAG in Production with LangChain and Chainlit](https://medium.com/@justinduy/rag-in-production-with-langchain-and-chainlit-86c2dea0ca40)
16. [Medium - Chainlit for LLM Apps 2025](https://medium.com/mitb-for-all/its-2025-start-using-chainlit-for-your-llm-apps-558db1a46315)
17. [The Hacker News - Chainlit 보안 취약점](https://thehackernews.com/2026/01/chainlit-ai-framework-flaws-enable-data.html)
18. [Medium - Building a Weather Agent with LangGraph, Chainlit & MCP](https://medium.com/@dominicschneider_7223/%EF%B8%8F-building-a-weather-agent-with-langgraph-chainlit-mcp-your-first-modular-ai-tool-6208bbb3d693)
19. [gonzalo123.com - Chat with Data using AWS Bedrock and Chainlit](https://gonzalo123.com/2025/12/09/chat-with-your-data-building-a-file-aware-ai-agent-with-aws-bedrock-and-chainlit/)
20. [DEV Community - Building News and Stock Assistant with LangGraph and Chainlit](https://dev.to/jamesbmour/building-a-news-and-stock-assistant-with-langgraph-and-chainlit-1bkk)
