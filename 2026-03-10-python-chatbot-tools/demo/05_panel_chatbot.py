"""
Panel 챗봇 데모
===============
실행 방법: panel serve 05_panel_chatbot.py --show
접속 URL:  http://localhost:5006

이 데모는 Panel의 ChatInterface 컴포넌트를 사용하여
Claude Haiku와 대화하는 챗봇을 구현합니다.

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
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"
SYSTEM_PROMPT = "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요."

# ─── Anthropic 클라이언트 초기화 ─────────────────────────────────────
if not USE_MOCK:
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY 환경변수를 설정해주세요.")
    client = anthropic.Anthropic(api_key=api_key)


def get_chat_history(chat_interface: pn.chat.ChatInterface) -> list[dict]:
    """
    Panel ChatInterface 객체에서 Claude API 형식의 대화 히스토리를 추출합니다.
    """
    messages = []

    for chat_msg in chat_interface.objects:
        if hasattr(chat_msg, 'object') and hasattr(chat_msg, 'user'):
            if chat_msg.user == "사용자":
                role = "user"
            elif chat_msg.user == "시스템":
                continue
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
    yield를 사용하면 스트리밍 응답이 가능합니다.
    """
    if USE_MOCK:
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

    # Claude API 스트리밍 호출
    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=messages,
    ) as stream:
        partial = ""
        for text in stream.text_stream:
            partial += text
            yield partial


# ─── ChatInterface 생성 ───────────────────────────────────────────
chat_interface = pn.chat.ChatInterface(
    callback=chatbot_callback,
    callback_user="AI 어시스턴트",
    user="사용자",
    show_rerun=True,
    show_undo=True,
    show_clear=True,
    placeholder_text="메시지를 입력하세요...",
    sizing_mode="stretch_width",
    height=600,
)

# 환영 메시지
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
    pn.serve(layout, port=5006, show=True)
