"""
고급 Chainlit + LangGraph 멀티 에이전트 챗봇
============================================
LangGraph로 구현한 복잡한 멀티 에이전트 시스템을 Chainlit UI로 제공합니다.

주요 기능:
- LangGraph 기반 멀티 에이전트 오케스트레이션
  * 라우터 에이전트: 질문 유형별 전문 에이전트 라우팅
  * 검색 에이전트: 웹 검색, 날씨 조회 (도구 호출)
  * 분석 에이전트: 수학 계산, 단위 변환 (도구 호출)
  * 코드 에이전트: Python 코드 작성 및 실행 (도구 호출)
  * 응답 합성기: 여러 에이전트 결과 통합
- MemorySaver를 통한 대화 기록 영속성 (세션 간)
- Chainlit Steps를 통한 에이전트 실행 과정 시각화
- 채팅 프로필 선택
- 처리 과정 단계별 표시

실행 방법:
    1. pip install -r requirements.txt
    2. cp .env.example .env  (그리고 .env에 API 키 입력)
    3. chainlit run app.py -w

그래프 구조:
    START → Router → [Search|Analysis|Code|Direct] → [Synthesizer] → END

참고:
    agent_graph.py: LangGraph 그래프 정의
    tools.py: 에이전트가 사용하는 도구 정의
"""

import os
import uuid
from dotenv import load_dotenv

import chainlit as cl
from langchain_core.messages import HumanMessage, AIMessage

from agent_graph import agent_graph, TOOL_DESCRIPTIONS
from tools import ALL_TOOLS

# .env 로드
load_dotenv()

# 에이전트 이름 한국어 매핑
AGENT_NAMES = {
    "router": "라우터",
    "search_agent": "검색 에이전트",
    "analysis_agent": "분석 에이전트",
    "code_agent": "코드 에이전트",
    "direct_response": "직접 응답",
    "synthesizer": "응답 합성기",
}

# 에이전트별 이모지
AGENT_ICONS = {
    "router": "🔀",
    "search_agent": "🔍",
    "analysis_agent": "📊",
    "code_agent": "💻",
    "direct_response": "💬",
    "synthesizer": "🔧",
}


# -------------------------------------------------------
# 채팅 프로필 설정
# -------------------------------------------------------
@cl.set_chat_profiles
async def chat_profile():
    """사용자가 선택할 수 있는 채팅 모드를 정의합니다."""
    return [
        cl.ChatProfile(
            name="멀티 에이전트 (전체 기능)",
            markdown_description=(
                "**멀티 에이전트 모드**\n\n"
                "LangGraph 기반 오케스트레이션:\n"
                "- 🔀 라우터가 질문을 분류\n"
                "- 🔍 검색 에이전트 (웹 검색, 날씨)\n"
                "- 📊 분석 에이전트 (계산, 단위 변환)\n"
                "- 💻 코드 에이전트 (Python 실행)\n"
                "- 🔧 응답 합성기"
            ),
        ),
        cl.ChatProfile(
            name="단일 에이전트 (빠른 응답)",
            markdown_description=(
                "**단일 에이전트 모드**\n\n"
                "하나의 에이전트가 모든 도구에 접근:\n"
                "- 모든 도구 동시 사용 가능\n"
                "- 더 빠른 응답 속도\n"
                "- 간단한 작업에 적합"
            ),
        ),
    ]


# -------------------------------------------------------
# 채팅 시작 핸들러
# -------------------------------------------------------
@cl.on_chat_start
async def on_chat_start():
    """
    채팅 세션이 시작될 때 초기화합니다.
    각 사용자마다 고유한 thread_id를 생성하여
    LangGraph의 MemorySaver가 대화 기록을 분리 관리합니다.
    """
    chat_profile = cl.user_session.get("chat_profile", "멀티 에이전트 (전체 기능)")

    # LangGraph 스레드 ID 생성 (대화 기록 격리를 위한 고유 ID)
    thread_id = str(uuid.uuid4())
    cl.user_session.set("thread_id", thread_id)
    cl.user_session.set("chat_profile", chat_profile)
    cl.user_session.set("message_count", 0)

    # 사용 가능한 도구 목록 표시
    tool_list = "\n".join([
        f"  - **{TOOL_DESCRIPTIONS.get(t.name, t.name)}** (`{t.name}`)"
        for t in ALL_TOOLS
    ])

    mode_info = ""
    if "멀티" in chat_profile:
        mode_info = (
            "\n**에이전트 구조:**\n"
            "```\n"
            "START → 라우터 → [검색|분석|코드|직접] → 합성기 → END\n"
            "```\n"
        )

    await cl.Message(
        content=(
            f"# 멀티 에이전트 AI 어시스턴트 🤖\n\n"
            f"**모드:** {chat_profile}\n"
            f"**세션 ID:** `{thread_id[:8]}...`\n\n"
            f"{mode_info}"
            f"**사용 가능한 도구:**\n{tool_list}\n\n"
            f"---\n"
            f"무엇이든 물어보세요! 예시:\n"
            f"- \"서울 날씨 알려줘\"\n"
            f"- \"피보나치 수열 10번째까지 계산하는 Python 코드 만들어줘\"\n"
            f"- \"100km를 마일로 변환해줘\"\n"
            f"- \"최신 AI 뉴스 검색해줘\"\n"
            f"- \"sin(30도) 값은?\""
        )
    ).send()


# -------------------------------------------------------
# 단일 에이전트 실행 함수
# -------------------------------------------------------
async def run_single_agent(message_content: str, thread_id: str, response_msg: cl.Message):
    """
    단일 에이전트 모드로 실행합니다.
    모든 도구에 접근 가능한 ReAct 에이전트를 사용합니다.
    """
    from langchain_openai import ChatOpenAI
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langgraph.prebuilt import create_react_agent
    from langgraph.checkpoint.memory import MemorySaver

    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        temperature=0.5,
        streaming=True,
    )

    # ReAct 에이전트 생성 (모든 도구 사용 가능)
    memory = MemorySaver()
    react_agent = create_react_agent(
        model=llm,
        tools=ALL_TOOLS,
        checkpointer=memory,
        state_modifier=(
            "당신은 다양한 도구를 활용하는 AI 어시스턴트입니다. "
            "웹 검색, 날씨 조회, 계산, 코드 실행, 단위 변환 등의 도구를 사용할 수 있습니다. "
            "한국어로 답변하며, 도구를 적극적으로 활용하여 정확한 정보를 제공하세요."
        )
    )

    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 20
    }

    full_response = ""

    async for event in react_agent.astream_events(
        {"messages": [HumanMessage(content=message_content)]},
        config=config,
        version="v2"
    ):
        kind = event["event"]

        if kind == "on_chat_model_stream":
            chunk = event["data"]["chunk"]
            if hasattr(chunk, "content") and chunk.content:
                token = chunk.content
                full_response += token
                await response_msg.stream_token(token)

    await response_msg.update()
    return full_response


# -------------------------------------------------------
# 멀티 에이전트 실행 함수
# -------------------------------------------------------
async def run_multi_agent(message_content: str, thread_id: str, response_msg: cl.Message):
    """
    멀티 에이전트 모드로 실행합니다.
    LangGraph 그래프를 통해 전문화된 에이전트들을 오케스트레이션합니다.
    각 에이전트의 실행 과정을 Chainlit Steps로 시각화합니다.
    """
    config = {
        "configurable": {"thread_id": thread_id},
        "recursion_limit": 25
    }

    # 현재 활성 에이전트와 Step 추적
    current_step = None
    current_agent = None
    full_response = ""

    # 에이전트 실행 추적용 변수
    active_steps = {}

    async for event in agent_graph.astream_events(
        {
            "messages": [HumanMessage(content=message_content)],
            "current_agent": "",
            "next_step": "",
            "analysis_results": [],
            "final_answer_ready": False,
        },
        config=config,
        version="v2"
    ):
        kind = event["event"]
        name = event.get("name", "")
        tags = event.get("tags", [])

        # 노드 시작 이벤트 감지
        if kind == "on_chain_start" and name in AGENT_NAMES:
            agent_display = AGENT_NAMES.get(name, name)
            icon = AGENT_ICONS.get(name, "🤖")

            # 이전 Step 닫기
            if current_agent and current_agent in active_steps:
                pass  # Step은 context manager로 자동 닫힘

            # 새 Step 생성
            step = cl.Step(
                name=f"{icon} {agent_display}",
                type="tool" if "agent" in name else "run",
                show_input=True,
            )
            await step.__aenter__()
            step.input = f"에이전트 시작: {agent_display}"
            active_steps[name] = step
            current_agent = name

        # 노드 종료 이벤트 감지
        elif kind == "on_chain_end" and name in AGENT_NAMES:
            if name in active_steps:
                step = active_steps.pop(name)
                # 결과 가져오기
                output = event.get("data", {}).get("output", {})
                if isinstance(output, dict):
                    agent_used = output.get("current_agent", name)
                    results = output.get("analysis_results", [])
                    step.output = f"완료 (에이전트: {AGENT_NAMES.get(agent_used, agent_used)})"
                await step.__aexit__(None, None, None)

        # 도구 호출 시작
        elif kind == "on_tool_start":
            tool_name = name
            tool_display = TOOL_DESCRIPTIONS.get(tool_name, tool_name)
            tool_input = event.get("data", {}).get("input", {})

            tool_step = cl.Step(
                name=f"  └─ 도구: {tool_display}",
                type="tool",
                show_input=True,
            )
            await tool_step.__aenter__()
            tool_step.input = str(tool_input)[:200]
            active_steps[f"tool_{tool_name}"] = tool_step

        # 도구 호출 완료
        elif kind == "on_tool_end":
            tool_name = name
            step_key = f"tool_{tool_name}"
            if step_key in active_steps:
                tool_step = active_steps.pop(step_key)
                output = event.get("data", {}).get("output", "")
                tool_step.output = str(output)[:300]
                await tool_step.__aexit__(None, None, None)

        # LLM 스트리밍 토큰 (최종 응답용)
        elif kind == "on_chat_model_stream":
            chunk = event.get("data", {}).get("chunk")
            if chunk and hasattr(chunk, "content") and chunk.content:
                # 합성기나 직접 응답의 최종 출력만 표시
                if current_agent in ["synthesizer", "direct_response"]:
                    token = chunk.content
                    full_response += token
                    await response_msg.stream_token(token)

    # 아직 열려있는 Step들 닫기
    for step in active_steps.values():
        try:
            await step.__aexit__(None, None, None)
        except Exception:
            pass

    await response_msg.update()
    return full_response


# -------------------------------------------------------
# 메시지 수신 핸들러
# -------------------------------------------------------
@cl.on_message
async def on_message(message: cl.Message):
    """
    사용자 메시지를 처리합니다.
    선택된 채팅 프로필에 따라 단일 에이전트 또는 멀티 에이전트 모드로 실행합니다.

    LangGraph의 MemorySaver 덕분에 이전 대화 기록이 자동으로 유지됩니다.
    thread_id가 동일한 경우 이전 대화 컨텍스트를 기억합니다.
    """
    thread_id = cl.user_session.get("thread_id")
    chat_profile = cl.user_session.get("chat_profile", "멀티 에이전트 (전체 기능)")

    # 메시지 카운터 증가
    count = cl.user_session.get("message_count", 0) + 1
    cl.user_session.set("message_count", count)

    # 응답 메시지 초기화 (스트리밍용)
    response_msg = cl.Message(content="")
    await response_msg.send()

    try:
        if "멀티" in chat_profile:
            # 멀티 에이전트 모드
            await run_multi_agent(message.content, thread_id, response_msg)
        else:
            # 단일 에이전트 모드
            await run_single_agent(message.content, thread_id, response_msg)

    except Exception as e:
        error_text = f"\n\n---\n**오류 발생:** {str(e)}\n\nAPI 키 설정을 확인해주세요."
        await response_msg.stream_token(error_text)
        await response_msg.update()
        print(f"[ERROR] {type(e).__name__}: {e}")


# -------------------------------------------------------
# 채팅 재개 핸들러 (이전 세션 복구)
# -------------------------------------------------------
@cl.on_chat_resume
async def on_chat_resume(thread):
    """
    사용자가 이전 채팅 세션을 재개할 때 호출됩니다.
    LangGraph의 MemorySaver를 통해 대화 기록이 자동 복구됩니다.
    """
    await cl.Message(
        content=(
            "이전 대화를 재개합니다. "
            "MemorySaver를 통해 대화 기록이 유지되어 있습니다!"
        ),
        author="System"
    ).send()


# -------------------------------------------------------
# 채팅 종료 핸들러
# -------------------------------------------------------
@cl.on_chat_end
async def on_chat_end():
    """채팅 세션 종료 시 정리 작업을 수행합니다."""
    thread_id = cl.user_session.get("thread_id", "unknown")
    count = cl.user_session.get("message_count", 0)
    print(f"[INFO] 세션 {thread_id[:8]}... 종료 - 총 {count}개 메시지 처리")
