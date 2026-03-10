"""
Mesop 챗봇 데모
===============
실행 방법: mesop 06_mesop_chatbot.py
접속 URL:  http://localhost:32123

이 데모는 Google의 Mesop 프레임워크를 사용하여
챗봇 인터페이스를 구현합니다.

핵심 컴포넌트:
- mesop.labs.chat: 내장 채팅 컴포넌트
- @me.page: 페이지 정의 데코레이터
- 선언형 UI 패턴
"""

import os
import mesop as me
import mesop.labs as mel
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# ─── 설정 ───────────────────────────────────────────────────────────
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

# ─── Anthropic 클라이언트 초기화 ─────────────────────────────────────
if not USE_MOCK:
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY 환경변수를 설정해주세요.")
    client = anthropic.Anthropic(api_key=api_key)


def transform(
    input_text: str,
    history: list[mel.ChatMessage],
) -> str:
    """
    Mesop mel.chat 컴포넌트의 transform 콜백 함수.
    """
    if USE_MOCK:
        response = (
            f"[목 응답] '{input_text}'를 받았습니다! "
            "Mesop은 Google이 내부적으로 사용하는 Python UI 프레임워크입니다."
        )
        return response

    # Claude API 메시지 형식으로 변환
    messages = []
    for msg in history:
        messages.append({
            "role": msg.role,
            "content": msg.content,
        })
    messages.append({"role": "user", "content": input_text})

    # Claude API 호출
    response = client.messages.create(
        model=MODEL,
        max_tokens=1024,
        system="당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
        messages=messages,
    )

    return response.content[0].text


# ─── Mesop 페이지 정의 ───────────────────────────────────────────
@me.page(
    path="/",
    title="Mesop 챗봇 데모",
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
)
def app():
    """메인 앱 페이지."""
    with me.box(
        style=me.Style(
            background="#f0f4f8",
            padding=me.Padding.all(16),
            border_radius=8,
            margin=me.Margin(bottom=16),
        )
    ):
        me.text(
            "Mesop 챗봇 데모",
            style=me.Style(font_size=24, font_weight="bold"),
        )
        me.text(
            f"모델: {MODEL} | 목 모드: {'켜짐' if USE_MOCK else '꺼짐'}",
            style=me.Style(color="#666", font_size=14),
        )

    mel.chat(
        transform=transform,
        title="AI 어시스턴트",
        bot_user="AI",
    )


@me.page(path="/about", title="Mesop 정보")
def about_page():
    """Mesop 프레임워크 소개 페이지"""
    me.text("Mesop 소개", style=me.Style(font_size=24, font_weight="bold"))
    me.text("Google이 만든 Python 기반 UI 프레임워크")
    me.text("• 파이썬만으로 웹앱 개발")
    me.text("• Angular Material 컴포넌트")
    me.text("• 핫 리로드 지원")
    me.text("• Gemini AI 친화적")

    with me.box(style=me.Style(margin=me.Margin(top=16))):
        me.link(text="챗봇으로 돌아가기", url="/")


if __name__ == "__main__":
    print("Mesop 앱은 다음 명령어로 실행해주세요:")
    print("  mesop 06_mesop_chatbot.py")
    print("\n브라우저에서 http://localhost:32123 접속")
