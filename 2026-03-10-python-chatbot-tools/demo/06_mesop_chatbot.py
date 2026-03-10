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

주요 특징:
- 핫 리로드: 코드 저장 시 브라우저 자동 새로고침
- Angular Material 기반 컴포넌트
- Google Gemini와의 자연스러운 통합
"""

import os
import time
import mesop as me
import mesop.labs as mel
from dotenv import load_dotenv

# .env 파일에서 환경변수 로드
load_dotenv()

# ─── 설정 ───────────────────────────────────────────────────────────
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

# ─── OpenAI 클라이언트 초기화 ─────────────────────────────────────
if not USE_MOCK:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY 환경변수를 설정해주세요.")
    client = OpenAI(api_key=api_key)


def transform(
    input_text: str,
    history: list[mel.ChatMessage],
) -> str:
    """
    Mesop mel.chat 컴포넌트의 transform 콜백 함수.

    사용자 입력과 대화 히스토리를 받아 AI 응답을 반환합니다.
    제너레이터(yield)를 사용하면 스트리밍이 가능합니다.

    Args:
        input_text: 사용자가 입력한 텍스트
        history: mel.ChatMessage 객체 리스트
                 (각 객체는 .role, .content 속성 보유)
    Returns:
        str 또는 제너레이터: AI 응답
    """
    if USE_MOCK:
        # 목 모드: 타이핑 효과 시뮬레이션
        response = (
            f"[목 응답] '{input_text}'를 받았습니다! "
            "Mesop은 Google이 내부적으로 사용하는 Python UI 프레임워크입니다."
        )
        return response

    # OpenAI API 메시지 형식으로 변환
    messages = [
        {"role": "system", "content": "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요."}
    ]

    # 대화 히스토리 변환
    for msg in history:
        messages.append({
            "role": msg.role,
            "content": msg.content,
        })

    # 현재 사용자 입력 추가
    messages.append({"role": "user", "content": input_text})

    # OpenAI API 호출 (스트리밍)
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )

    # 스트리밍 응답 처리
    response = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            response += content

    return response


# ─── Mesop 페이지 정의 ───────────────────────────────────────────
@me.page(
    path="/",
    title="Mesop 챗봇 데모",
    security_policy=me.SecurityPolicy(
        allowed_iframe_parents=["https://google.github.io"]
    ),
)
def app():
    """
    메인 앱 페이지.
    mel.chat 컴포넌트가 모든 채팅 UI를 자동으로 처리합니다.
    """
    # 상단 헤더
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

    # mel.chat: 완전한 채팅 UI를 단 한 줄로 생성
    mel.chat(
        transform=transform,
        title="AI 어시스턴트",
        bot_user="AI",
    )


# ─── 추가 페이지: 정보 페이지 ────────────────────────────────────
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
    # mesop 06_mesop_chatbot.py 명령으로 실행하세요
    # python으로 직접 실행 시 아래와 같이 안내
    print("Mesop 앱은 다음 명령어로 실행해주세요:")
    print("  mesop 06_mesop_chatbot.py")
    print("\n브라우저에서 http://localhost:32123 접속")
