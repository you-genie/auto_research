"""
LangGraph 멀티 에이전트 그래프 정의 모듈
=========================================
여러 전문화된 노드로 구성된 LangGraph 그래프를 정의합니다.

그래프 구조:
                    ┌─────────────┐
                    │   START     │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │  라우터     │  → 어떤 에이전트로 갈지 결정
                    │  (router)   │
                    └──────┬──────┘
                           │
          ┌────────────────┼─────────────────┐
          │                │                 │
   ┌──────▼──────┐  ┌──────▼──────┐  ┌──────▼──────┐
   │ 검색 에이전트│  │ 분석 에이전트│  │ 코드 에이전트│
   │  (search)   │  │  (analyst)  │  │   (coder)   │
   └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
          │                │                 │
          └────────────────┼─────────────────┘
                           │
                    ┌──────▼──────┐
                    │  응답 합성  │
                    │  (synth)    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │    END      │
                    └─────────────┘
"""

import os
from typing import Annotated, Literal, TypedDict
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.checkpoint.memory import MemorySaver
from langgraph.prebuilt import ToolNode

from tools import ALL_TOOLS, TOOL_DESCRIPTIONS

load_dotenv()


# -------------------------------------------------------
# 그래프 상태 정의
# -------------------------------------------------------
class AgentState(TypedDict):
    """
    그래프 전체에서 공유되는 상태입니다.
    각 노드는 이 상태를 읽고 업데이트합니다.
    """
    # 대화 기록 (add_messages: 새 메시지를 기존 목록에 추가하는 리듀서)
    messages: Annotated[list[BaseMessage], add_messages]

    # 현재 활성 에이전트 이름
    current_agent: str

    # 라우터가 결정한 다음 단계
    next_step: str

    # 각 에이전트의 분석 결과 수집
    analysis_results: list[str]

    # 최종 답변 생성 여부
    final_answer_ready: bool


# -------------------------------------------------------
# LLM 초기화
# -------------------------------------------------------
def create_llm(temperature: float = 0.0) -> ChatOpenAI:
    """ChatOpenAI 인스턴스를 생성합니다."""
    return ChatOpenAI(
        model=os.getenv("OPENAI_MODEL", "gpt-4o"),
        temperature=temperature,
        api_key=os.getenv("OPENAI_API_KEY"),
        streaming=True,
    )


# -------------------------------------------------------
# 노드 1: 라우터 (Router)
# -------------------------------------------------------
def router_node(state: AgentState) -> AgentState:
    """
    사용자의 질문을 분석하여 어떤 전문 에이전트에게 작업을 맡길지 결정합니다.
    복잡한 질문의 경우 여러 에이전트를 순서대로 호출합니다.

    라우팅 규칙:
    - 검색이 필요한 질문 → search_agent
    - 데이터 분석/계산 필요 → analysis_agent
    - 코드 작성/실행 필요 → code_agent
    - 단순 대화/설명 → direct_response
    """
    llm = create_llm(temperature=0.0)

    routing_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""당신은 라우팅 전문가입니다.
사용자의 질문을 분석하여 가장 적합한 에이전트를 선택하세요.

선택 가능한 에이전트:
- search: 최신 정보 검색, 뉴스, 날씨 조회가 필요한 경우
- analysis: 수학 계산, 데이터 분석, 단위 변환이 필요한 경우
- code: Python 코드 작성 또는 실행이 필요한 경우
- direct: 일반 대화, 설명, 요약 등 도구 없이 답변 가능한 경우

반드시 다음 중 하나만 답하세요: search, analysis, code, direct"""),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = routing_prompt | llm
    response = chain.invoke({"messages": state["messages"]})

    # 응답에서 라우팅 결정 추출
    content = response.content.strip().lower()

    if "search" in content:
        next_step = "search_agent"
    elif "analysis" in content or "analys" in content:
        next_step = "analysis_agent"
    elif "code" in content:
        next_step = "code_agent"
    else:
        next_step = "direct_response"

    return {
        **state,
        "current_agent": "router",
        "next_step": next_step,
        "analysis_results": [],
        "final_answer_ready": False,
    }


# -------------------------------------------------------
# 노드 2: 검색 에이전트 (Search Agent)
# -------------------------------------------------------
def search_agent_node(state: AgentState) -> AgentState:
    """
    웹 검색 및 날씨 조회 도구를 사용하는 전문 에이전트입니다.
    ReAct(Reasoning + Acting) 패턴으로 작동합니다.
    """
    # 검색 관련 도구만 선택
    search_tools = [t for t in ALL_TOOLS if t.name in ["web_search", "get_weather", "get_current_datetime"]]
    llm = create_llm(temperature=0.1)
    llm_with_tools = llm.bind_tools(search_tools)

    search_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""당신은 정보 검색 전문 에이전트입니다.
웹 검색, 날씨 조회, 날짜/시간 조회 도구를 사용하여 최신 정보를 수집합니다.
반드시 도구를 사용하여 정확한 정보를 수집하고, 수집한 정보를 명확하게 정리하세요."""),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = search_prompt | llm_with_tools

    # 도구 호출이 완료될 때까지 반복 (ReAct 루프)
    current_messages = list(state["messages"])
    max_iterations = 5

    for i in range(max_iterations):
        response = chain.invoke({"messages": current_messages})
        current_messages.append(response)

        # 도구 호출이 없으면 종료
        if not response.tool_calls:
            break

        # 도구 실행
        tool_node = ToolNode(search_tools)
        tool_results = tool_node.invoke({"messages": current_messages})
        tool_messages = tool_results["messages"]
        current_messages.extend(tool_messages)

    # 검색 결과 요약
    search_summary = response.content if hasattr(response, 'content') else str(response)

    return {
        **state,
        "messages": current_messages,
        "current_agent": "search_agent",
        "analysis_results": state.get("analysis_results", []) + [f"[검색 결과] {search_summary}"],
        "next_step": "synthesizer",
    }


# -------------------------------------------------------
# 노드 3: 분석 에이전트 (Analysis Agent)
# -------------------------------------------------------
def analysis_agent_node(state: AgentState) -> AgentState:
    """
    수학 계산, 단위 변환, 데이터 분석 전문 에이전트입니다.
    """
    # 분석 관련 도구만 선택
    analysis_tools = [t for t in ALL_TOOLS if t.name in ["calculate", "convert_units", "get_current_datetime"]]
    llm = create_llm(temperature=0.0)
    llm_with_tools = llm.bind_tools(analysis_tools)

    analysis_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""당신은 데이터 분석 및 계산 전문 에이전트입니다.
수학적 계산, 단위 변환, 수치 분석을 정확하게 수행합니다.
계산 도구를 사용하여 정확한 결과를 제공하고, 단계별 풀이 과정을 설명하세요."""),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = analysis_prompt | llm_with_tools

    current_messages = list(state["messages"])
    max_iterations = 5

    for _ in range(max_iterations):
        response = chain.invoke({"messages": current_messages})
        current_messages.append(response)

        if not response.tool_calls:
            break

        tool_node = ToolNode(analysis_tools)
        tool_results = tool_node.invoke({"messages": current_messages})
        current_messages.extend(tool_results["messages"])

    analysis_summary = response.content if hasattr(response, 'content') else str(response)

    return {
        **state,
        "messages": current_messages,
        "current_agent": "analysis_agent",
        "analysis_results": state.get("analysis_results", []) + [f"[분석 결과] {analysis_summary}"],
        "next_step": "synthesizer",
    }


# -------------------------------------------------------
# 노드 4: 코드 에이전트 (Code Agent)
# -------------------------------------------------------
def code_agent_node(state: AgentState) -> AgentState:
    """
    Python 코드 작성 및 실행 전문 에이전트입니다.
    """
    code_tools = [t for t in ALL_TOOLS if t.name in ["execute_python_code", "calculate"]]
    llm = create_llm(temperature=0.2)
    llm_with_tools = llm.bind_tools(code_tools)

    code_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""당신은 Python 프로그래밍 전문 에이전트입니다.
사용자의 요청에 맞는 Python 코드를 작성하고 실행합니다.
코드는 명확하고 잘 주석된 상태로 작성하며, 실행 결과를 설명합니다.
코드 실행 도구를 사용하여 실제로 코드를 실행하고 결과를 확인하세요."""),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = code_prompt | llm_with_tools

    current_messages = list(state["messages"])
    max_iterations = 5

    for _ in range(max_iterations):
        response = chain.invoke({"messages": current_messages})
        current_messages.append(response)

        if not response.tool_calls:
            break

        tool_node = ToolNode(code_tools)
        tool_results = tool_node.invoke({"messages": current_messages})
        current_messages.extend(tool_results["messages"])

    code_summary = response.content if hasattr(response, 'content') else str(response)

    return {
        **state,
        "messages": current_messages,
        "current_agent": "code_agent",
        "analysis_results": state.get("analysis_results", []) + [f"[코드 결과] {code_summary}"],
        "next_step": "synthesizer",
    }


# -------------------------------------------------------
# 노드 5: 직접 응답 (Direct Response)
# -------------------------------------------------------
def direct_response_node(state: AgentState) -> AgentState:
    """
    도구 없이 LLM이 직접 답변하는 노드입니다.
    일반 대화, 설명, 요약 등에 사용됩니다.
    """
    llm = create_llm(temperature=0.7)

    direct_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content="""당신은 지식이 풍부하고 친절한 AI 어시스턴트입니다.
한국어로 명확하고 도움이 되는 답변을 제공합니다.
필요하다면 예시를 들어 설명하고, 복잡한 개념은 쉽게 풀어서 설명하세요."""),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = direct_prompt | llm
    response = chain.invoke({"messages": state["messages"]})

    return {
        **state,
        "messages": [*state["messages"], response],
        "current_agent": "direct_response",
        "analysis_results": [response.content],
        "next_step": "end",
        "final_answer_ready": True,
    }


# -------------------------------------------------------
# 노드 6: 응답 합성기 (Synthesizer)
# -------------------------------------------------------
def synthesizer_node(state: AgentState) -> AgentState:
    """
    여러 에이전트의 결과를 통합하여 최종 응답을 생성합니다.
    """
    llm = create_llm(temperature=0.5)

    # 수집된 분석 결과들 통합
    analysis_text = "\n\n".join(state.get("analysis_results", []))

    synthesis_prompt = ChatPromptTemplate.from_messages([
        SystemMessage(content=f"""당신은 응답 합성 전문가입니다.
여러 에이전트가 수집한 정보를 통합하여 사용자에게 명확하고 유용한 최종 답변을 작성합니다.

수집된 정보:
{analysis_text}

위 정보를 바탕으로 사용자의 질문에 대해 구조적이고 완성된 답변을 한국어로 작성하세요.
불필요한 반복을 피하고, 핵심 내용을 명확하게 전달하세요."""),
        MessagesPlaceholder(variable_name="messages"),
    ])

    chain = synthesis_prompt | llm
    response = chain.invoke({"messages": state["messages"]})

    return {
        **state,
        "messages": [*state["messages"], response],
        "current_agent": "synthesizer",
        "next_step": "end",
        "final_answer_ready": True,
    }


# -------------------------------------------------------
# 라우팅 로직 (엣지 조건)
# -------------------------------------------------------
def route_after_router(state: AgentState) -> Literal["search_agent", "analysis_agent", "code_agent", "direct_response"]:
    """라우터 노드 실행 후 다음 노드를 결정합니다."""
    next_step = state.get("next_step", "direct_response")
    if next_step == "search_agent":
        return "search_agent"
    elif next_step == "analysis_agent":
        return "analysis_agent"
    elif next_step == "code_agent":
        return "code_agent"
    else:
        return "direct_response"


def route_after_agent(state: AgentState) -> Literal["synthesizer", END]:
    """에이전트 노드 실행 후 합성기로 이동하거나 종료합니다."""
    if state.get("final_answer_ready", False):
        return END
    return "synthesizer"


# -------------------------------------------------------
# 그래프 빌드 및 컴파일
# -------------------------------------------------------
def build_agent_graph() -> tuple:
    """
    LangGraph 멀티 에이전트 그래프를 빌드하고 컴파일합니다.

    반환값:
        tuple: (compiled_graph, memory_saver)
    """
    # 메모리 기반 체크포인터 (대화 기록 영속성)
    # 프로덕션에서는 PostgreSQL이나 Redis 기반 체크포인터로 교체 가능
    memory = MemorySaver()

    # 그래프 빌드
    workflow = StateGraph(AgentState)

    # 노드 추가
    workflow.add_node("router", router_node)
    workflow.add_node("search_agent", search_agent_node)
    workflow.add_node("analysis_agent", analysis_agent_node)
    workflow.add_node("code_agent", code_agent_node)
    workflow.add_node("direct_response", direct_response_node)
    workflow.add_node("synthesizer", synthesizer_node)

    # 엣지 연결
    workflow.add_edge(START, "router")

    # 라우터에서 조건부 분기
    workflow.add_conditional_edges(
        "router",
        route_after_router,
        {
            "search_agent": "search_agent",
            "analysis_agent": "analysis_agent",
            "code_agent": "code_agent",
            "direct_response": "direct_response",
        }
    )

    # 각 에이전트에서 합성기로 이동 또는 종료
    workflow.add_conditional_edges(
        "search_agent",
        route_after_agent,
        {"synthesizer": "synthesizer", END: END}
    )
    workflow.add_conditional_edges(
        "analysis_agent",
        route_after_agent,
        {"synthesizer": "synthesizer", END: END}
    )
    workflow.add_conditional_edges(
        "code_agent",
        route_after_agent,
        {"synthesizer": "synthesizer", END: END}
    )

    # 직접 응답과 합성기는 종료
    workflow.add_edge("direct_response", END)
    workflow.add_edge("synthesizer", END)

    # 체크포인터와 함께 컴파일
    compiled_graph = workflow.compile(checkpointer=memory)

    return compiled_graph, memory


# 그래프 싱글톤 (모듈 로드 시 한 번만 생성)
agent_graph, memory_saver = build_agent_graph()
