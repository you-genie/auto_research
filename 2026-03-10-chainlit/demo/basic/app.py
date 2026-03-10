"""
기본 Chainlit 챗봇 데모 (Hello World 수준)
========================================
OpenAI API를 이용한 가장 단순한 형태의 Chainlit 챗봇입니다.
- 스트리밍 응답
- 기본 메시지 핸들링
- 대화 기록 유지 (세션 내)

실행 방법:
    1. pip install -r requirements.txt
    2. cp .env.example .env  (그리고 .env에 API 키 입력)
    3. chainlit run app.py -w
"""

import os
from dotenv import load_dotenv
import chainlit as cl
from openai import AsyncOpenAI

# .env 파일에서 환경 변수 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")

# -------------------------------------------------------
# 채팅 세션 시작 시 실행되는 핸들러
# -------------------------------------------------------
@cl.on_chat_start
async def on_chat_start():
    """
    사용자가 채팅을 시작할 때 한 번 호출됩니다.
    - 대화 기록을 세션에 초기화합니다.
    - 환영 메시지를 보냅니다.
    """
    # 각 사용자마다 독립된 대화 기록 초기화
    # cl.user_session을 쓰면 사용자 간 데이터 충돌을 방지할 수 있어요!
    cl.user_session.set("message_history", [
        {
            "role": "system",
            "content": (
                "당신은 친절하고 도움이 되는 AI 어시스턴트입니다. "
                "한국어로 대화하며, 명확하고 간결하게 답변합니다."
            )
        }
    ])

    # 환영 메시지 전송
    await cl.Message(
        content=(
            "안녕하세요! 저는 AI 어시스턴트입니다.\n\n"
            "무엇이든 물어보세요! 도와드릴게요 😊"
        )
    ).send()


# -------------------------------------------------------
# 사용자 메시지 수신 시 실행되는 핸들러
# -------------------------------------------------------
@cl.on_message
async def on_message(message: cl.Message):
    """
    사용자가 메시지를 보낼 때마다 호출됩니다.
    - 대화 기록에 사용자 메시지를 추가합니다.
    - OpenAI API를 스트리밍 방식으로 호출합니다.
    - 응답을 실시간으로 UI에 표시합니다.
    """
    # 현재 세션의 대화 기록 가져오기
    message_history = cl.user_session.get("message_history")

    # 사용자 메시지를 대화 기록에 추가
    message_history.append({
        "role": "user",
        "content": message.content
    })

    # 빈 응답 메시지 생성 (스트리밍용)
    response_message = cl.Message(content="")
    await response_message.send()

    # OpenAI API 스트리밍 호출
    full_response = ""
    stream = await client.chat.completions.create(
        model=MODEL,
        messages=message_history,
        stream=True,  # 스트리밍 활성화
        temperature=0.7,
    )

    # 스트리밍 토큰을 하나씩 UI에 전송
    async for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            token = chunk.choices[0].delta.content
            full_response += token
            await response_message.stream_token(token)

    # 스트리밍 완료 후 메시지 확정
    await response_message.update()

    # AI 응답을 대화 기록에 추가 (다음 대화에서 컨텍스트로 활용)
    message_history.append({
        "role": "assistant",
        "content": full_response
    })

    # 업데이트된 대화 기록 저장
    cl.user_session.set("message_history", message_history)


# -------------------------------------------------------
# 채팅 세션 종료 시 실행되는 핸들러 (선택사항)
# -------------------------------------------------------
@cl.on_chat_end
async def on_chat_end():
    """
    사용자가 채팅을 종료할 때 호출됩니다.
    실제 프로덕션에서는 여기서 대화 기록을 DB에 저장하거나
    정리 작업을 수행할 수 있습니다.
    """
    message_history = cl.user_session.get("message_history", [])
    # 시스템 메시지 제외한 실제 대화 수 계산
    conversation_count = len([m for m in message_history if m["role"] != "system"])
    print(f"[INFO] 채팅 세션 종료 - 총 {conversation_count}개의 메시지 교환")
