"""
Chainlit 챗봇 데모
==================
실행 방법: chainlit run 03_chainlit_chatbot.py
접속 URL:  http://localhost:8000

중요: 'python 03_chainlit_chatbot.py'로는 실행되지 않습니다.
반드시 'chainlit run' 명령어를 사용해야 합니다.

이 데모는 Chainlit 프레임워크를 사용하여 ChatGPT 수준의
채팅 UI를 구현합니다.

핵심 컴포넌트:
- @cl.on_chat_start: 새 세션 시작 이벤트
- @cl.on_message: 사용자 메시지 수신 이벤트
- cl.Message: 메시지 전송 및 스트리밍
- cl.user_session: 사용자별 세션 상태 관리
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

# ─── Anthropic 클라이언트 초기화 ─────────────────────────────────────
if not USE_MOCK:
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY 환경변수를 설정해주세요.")
    client = anthropic.AsyncAnthropic(api_key=api_key)


# ─── 채팅 시작 이벤트 ─────────────────────────────────────────────
@cl.on_chat_start
async def on_chat_start():
    """
    새 채팅 세션이 시작될 때 실행됩니다.
    - 대화 히스토리 초기화
    - 환영 메시지 전송
    """
    # 사용자별 세션에 대화 히스토리 저장 (system 메시지는 별도 관리)
    cl.user_session.set("history", [])

    # 환영 메시지 전송
    await cl.Message(
        content=f"안녕하세요! 저는 {MODEL} 기반 AI 어시스턴트입니다. 무엇이든 물어보세요!\n\n"
                f"목 모드: {'켜짐 (실제 API 미호출)' if USE_MOCK else '꺼짐 (실제 API 사용)'}",
        author="시스템",
    ).send()


# ─── 메시지 수신 이벤트 ─────────────────────────────────────────
@cl.on_message
async def on_message(message: cl.Message):
    """
    사용자 메시지를 받을 때마다 실행됩니다.
    - 히스토리에 사용자 메시지 추가
    - Claude API 호출 (스트리밍)
    - 응답을 히스토리에 추가
    """
    # 세션에서 대화 히스토리 가져오기
    history: list[dict] = cl.user_session.get("history")

    # 사용자 메시지를 히스토리에 추가
    history.append({"role": "user", "content": message.content})

    # 빈 어시스턴트 메시지 생성 (스트리밍용)
    response_msg = cl.Message(content="")

    if USE_MOCK:
        # 목 모드: 타이핑 효과 시뮬레이션
        mock_text = f"[목 응답] '{message.content}'를 받았습니다! Chainlit은 LLM 챗봇에 특화된 프레임워크입니다."
        for char in mock_text:
            await response_msg.stream_token(char)
            time.sleep(0.02)
    else:
        # 실제 Claude API 스트리밍 호출
        async with client.messages.stream(
            model=MODEL,
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=history,
        ) as stream:
            async for text in stream.text_stream:
                await response_msg.stream_token(text)

    # 최종 메시지 업데이트 (스트리밍 완료 후)
    await response_msg.update()

    # 어시스턴트 응답을 히스토리에 추가
    history.append({"role": "assistant", "content": response_msg.content})
    cl.user_session.set("history", history)


# ─── 채팅 종료 이벤트 ─────────────────────────────────────────────
@cl.on_chat_end
async def on_chat_end():
    """채팅 세션이 종료될 때 실행됩니다."""
    history = cl.user_session.get("history", [])
    print(f"세션 종료. 총 {len(history)} 개의 메시지가 있었습니다.")
