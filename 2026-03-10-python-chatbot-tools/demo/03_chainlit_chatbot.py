"""
Chainlit + LangChain 챗봇 데모
==============================
실행 방법: chainlit run 03_chainlit_chatbot.py
접속 URL:  http://localhost:8000

중요: 'python 03_chainlit_chatbot.py'로는 실행되지 않습니다.
반드시 'chainlit run' 명령어를 사용해야 합니다.

이 데모는 Chainlit + LangChain을 사용하여 ChatGPT 수준의
채팅 UI를 구현합니다.

핵심 컴포넌트:
- ChatAnthropic: LangChain의 Claude 모델 래퍼
- ChatPromptTemplate: 시스템/사용자 프롬프트 구성
- RunnableWithMessageHistory: 대화 히스토리 자동 관리
- ChatMessageHistory: 인메모리 히스토리 저장소
"""

import os
import time
import chainlit as cl
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# ─── 설정 ───────────────────────────────────────────────────────────
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"
SYSTEM_PROMPT = "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요."

# ─── LangChain 초기화 ───────────────────────────────────────────────
if not USE_MOCK:
    from langchain_anthropic import ChatAnthropic
    from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
    from langchain_core.runnables.history import RunnableWithMessageHistory
    from langchain_community.chat_message_histories import ChatMessageHistory

    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY 환경변수를 설정해주세요.")

    # LLM 모델 생성
    llm = ChatAnthropic(
        model=MODEL,
        max_tokens=1024,
        api_key=api_key,
        streaming=True,
    )

    # 프롬프트 템플릿 (시스템 + 히스토리 + 사용자 입력)
    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        MessagesPlaceholder(variable_name="history"),
        ("human", "{input}"),
    ])

    chain = prompt | llm

    # 세션별 히스토리 저장소
    session_histories: dict[str, ChatMessageHistory] = {}

    def get_session_history(session_id: str) -> ChatMessageHistory:
        if session_id not in session_histories:
            session_histories[session_id] = ChatMessageHistory()
        return session_histories[session_id]

    # 히스토리 자동 관리 체인
    chain_with_history = RunnableWithMessageHistory(
        chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="history",
    )


# ─── 채팅 시작 이벤트 ─────────────────────────────────────────────
@cl.on_chat_start
async def on_chat_start():
    """
    새 채팅 세션이 시작될 때 실행됩니다.
    - 세션 ID 저장
    - 환영 메시지 전송
    """
    session_id = cl.user_session.get("id")
    cl.user_session.set("session_id", session_id)

    await cl.Message(
        content=f"안녕하세요! 저는 LangChain + {MODEL} 기반 AI 어시스턴트입니다. 무엇이든 물어보세요!\n\n"
                f"목 모드: {'켜짐 (실제 API 미호출)' if USE_MOCK else '꺼짐 (실제 API 사용)'}",
        author="시스템",
    ).send()


# ─── 메시지 수신 이벤트 ─────────────────────────────────────────
@cl.on_message
async def on_message(message: cl.Message):
    """
    사용자 메시지를 받을 때마다 실행됩니다.
    - LangChain 체인 호출 (스트리밍)
    - 히스토리는 RunnableWithMessageHistory가 자동 관리
    """
    response_msg = cl.Message(content="")

    if USE_MOCK:
        mock_text = f"[목 응답] '{message.content}'를 받았습니다! LangChain + Chainlit 챗봇입니다."
        for char in mock_text:
            await response_msg.stream_token(char)
            time.sleep(0.02)
    else:
        session_id = cl.user_session.get("session_id")

        # LangChain 스트리밍 호출
        async for chunk in chain_with_history.astream(
            {"input": message.content},
            config={"configurable": {"session_id": session_id}},
        ):
            if hasattr(chunk, "content") and chunk.content:
                await response_msg.stream_token(chunk.content)

    await response_msg.update()


# ─── 채팅 종료 이벤트 ─────────────────────────────────────────────
@cl.on_chat_end
async def on_chat_end():
    """채팅 세션이 종료될 때 실행됩니다."""
    session_id = cl.user_session.get("session_id")
    if not USE_MOCK and session_id in session_histories:
        history = session_histories[session_id]
        print(f"세션 종료. 총 {len(history.messages)} 개의 메시지가 있었습니다.")
        del session_histories[session_id]
