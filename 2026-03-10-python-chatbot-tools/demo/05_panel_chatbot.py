"""
Panel 챗봇 데모
===============
실행 방법: panel serve 05_panel_chatbot.py --show
접속 URL:  http://localhost:5006

이 데모는 Panel의 ChatInterface 컴포넌트를 사용하여
OpenAI GPT-4o와 대화하는 챗봇을 구현합니다.

핵심 컴포넌트:
- pn.chat.ChatInterface: 고수준 채팅 인터페이스
- pn.chat.ChatMessage: 개별 메시지 컴포넌트
- yield 콜백으로 스트리밍 구현
"""

import os
import time
import panel as pn
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# Panel 확장 초기화
pn.extension()

# ─── 설정 ───────────────────────────────────────────────────────────
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"
SYSTEM_PROMPT = "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요."

# ─── OpenAI 클라이언트 초기화 ─────────────────────────────────────
if not USE_MOCK:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY 환경변수를 설정해주세요.")
    client = OpenAI(api_key=api_key)


def get_chat_history(chat_interface: pn.chat.ChatInterface) -> list[dict]:
    """
    Panel ChatInterface 객체에서 OpenAI 형식의 대화 히스토리를 추출합니다.

    Args:
        chat_interface: Panel ChatInterface 인스턴스
    Returns:
        list[dict]: OpenAI 형식의 메시지 리스트
    """
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for chat_msg in chat_interface.objects:
        if hasattr(chat_msg, 'object') and hasattr(chat_msg, 'user'):
            # Panel ChatMessage의 user 필드로 role 결정
            if chat_msg.user == "사용자":
                role = "user"
            elif chat_msg.user == "시스템":
                continue  # 시스템 메시지 건너뜀
            else:
                role = "assistant"

            if isinstance(chat_msg.object, str):
                messages.append({"role": role, "content": chat_msg.object})

    return messages


def chatbot_callback(
    contents: str,
    user: str,
    instance: pn.chat.ChatInterface,
):
    """
    사용자 입력에 대한 챗봇 응답 콜백 함수.

    Panel ChatInterface에서 사용자가 메시지를 전송하면 이 함수가 호출됩니다.
    yield를 사용하면 스트리밍 응답이 가능합니다.

    Args:
        contents: 사용자가 입력한 메시지 텍스트
        user: 메시지를 보낸 사용자 이름
        instance: ChatInterface 인스턴스
    """
    if USE_MOCK:
        # 목 모드: 타이핑 효과 시뮬레이션
        mock_response = (
            f"[목 응답] '{contents}'를 받았습니다! "
            "Panel은 Jupyter 노트북 친화적인 대시보드+챗봇 프레임워크입니다."
        )
        partial = ""
        for char in mock_response:
            partial += char
            time.sleep(0.02)
            yield partial
        return

    # 대화 히스토리 구성
    messages = get_chat_history(instance)
    messages.append({"role": "user", "content": contents})

    # OpenAI API 스트리밍 호출
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )

    # 스트리밍 응답을 점진적으로 yield
    partial = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            partial += content
            yield partial


# ─── ChatInterface 생성 ───────────────────────────────────────────
chat_interface = pn.chat.ChatInterface(
    callback=chatbot_callback,
    callback_user="AI 어시스턴트",        # 응답자 이름
    user="사용자",                         # 사용자 이름
    show_rerun=True,                       # 최근 메시지 재전송 버튼
    show_undo=True,                        # 메시지 취소 버튼
    show_clear=True,                       # 전체 대화 삭제 버튼
    placeholder_text="메시지를 입력하세요...",
    sizing_mode="stretch_width",
    height=600,
)

# 환영 메시지 (respond=False: 콜백 호출 없이 메시지만 추가)
chat_interface.send(
    f"안녕하세요! 저는 {MODEL} 기반 AI 어시스턴트입니다. 목 모드: {'켜짐' if USE_MOCK else '꺼짐'}",
    user="시스템",
    respond=False,
)

# ─── 사이드바 레이아웃 구성 ───────────────────────────────────────
sidebar = pn.Column(
    pn.pane.Markdown("## 설정"),
    pn.pane.Markdown(f"**모델**: {MODEL}"),
    pn.pane.Markdown(f"**목 모드**: {'켜짐' if USE_MOCK else '꺼짐'}"),
    pn.layout.Divider(),
    pn.pane.Markdown("### 사용법"),
    pn.pane.Markdown("- 하단 입력창에 메시지 입력\n- Enter로 전송\n- Shift+Enter로 줄바꿈"),
    width=200,
)

# ─── 전체 레이아웃 구성 ───────────────────────────────────────────
layout = pn.Row(
    sidebar,
    pn.Column(
        pn.pane.Markdown("# Panel 챗봇 데모", sizing_mode="stretch_width"),
        chat_interface,
        sizing_mode="stretch_width",
    ),
    sizing_mode="stretch_width",
)

# servable()을 호출해야 panel serve로 실행 가능
layout.servable()

if __name__ == "__main__":
    # 직접 실행 시 (python 05_panel_chatbot.py)
    # panel serve 명령 없이 간단한 서버 시작
    pn.serve(layout, port=5006, show=True)
