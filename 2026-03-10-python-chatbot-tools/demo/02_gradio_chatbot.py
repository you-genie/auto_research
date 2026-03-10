"""
Gradio 챗봇 데모
================
실행 방법: python 02_gradio_chatbot.py
접속 URL:  http://localhost:7860

이 데모는 Gradio의 ChatInterface를 사용하여
OpenAI GPT-4o와 대화하는 챗봇을 구현합니다.

핵심 컴포넌트:
- gr.ChatInterface: 고수준 채팅 UI (응답 함수만 정의하면 완성)
- gr.Blocks: 커스텀 레이아웃 구성
- gr.Chatbot: 저수준 챗봇 컴포넌트

주요 특징:
- type="messages"로 OpenAI 형식 히스토리 사용
- yield 제너레이터로 스트리밍 구현
- multimodal=True로 파일 업로드 지원 (고급 예시)
"""

import os
import time
import gradio as gr
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


# ─── 기본 챗봇 응답 함수 ─────────────────────────────────────────
def basic_chat(
    message: str,
    history: list[dict],
) -> str:
    """
    기본 챗봇 응답 함수 (스트리밍 없음)

    Args:
        message: 현재 사용자 입력
        history: OpenAI 형식의 대화 히스토리
                 [{"role": "user", "content": "..."}, ...]
    Returns:
        str: 어시스턴트 응답
    """
    if USE_MOCK:
        time.sleep(0.5)  # API 지연 시뮬레이션
        return f"[목 응답] '{message}'를 받았습니다!"

    messages = history + [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
    )
    return response.choices[0].message.content


# ─── 스트리밍 챗봇 응답 함수 ──────────────────────────────────────
def streaming_chat(
    message: str,
    history: list[dict],
) -> str:
    """
    스트리밍 챗봇 응답 함수 (yield 제너레이터)

    yield를 사용하면 Gradio가 자동으로 스트리밍 UI를 처리합니다.
    전송 버튼은 스트리밍 중에 "정지" 버튼으로 변경됩니다.
    """
    if USE_MOCK:
        # 목 모드: 타이핑 효과 시뮬레이션
        mock_response = f"[목 응답] '{message}'를 받았습니다! 파이썬 챗봇 프레임워크 중 Gradio는 가장 빠르게 시작할 수 있습니다."
        partial = ""
        for char in mock_response:
            partial += char
            time.sleep(0.03)
            yield partial
        return

    # OpenAI API 스트리밍
    messages = history + [{"role": "user", "content": message}]
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )

    partial = ""
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content:
            partial += content
            yield partial  # 부분 응답을 점진적으로 반환


# ─── 기본 ChatInterface 예시 ──────────────────────────────────────
def create_basic_demo() -> gr.ChatInterface:
    """가장 간단한 Gradio 챗봇 - 스트리밍 지원"""
    return gr.ChatInterface(
        fn=streaming_chat,
        type="messages",         # OpenAI 형식 히스토리
        title="Gradio 챗봇 데모",
        description=f"OpenAI {MODEL}을 사용한 스트리밍 챗봇",
        examples=[               # 사전 정의된 예시 질문
            "파이썬이란 무엇인가요?",
            "Gradio와 Streamlit의 차이점은?",
            "LLM 챗봇을 만드는 가장 쉬운 방법은?",
        ],
        cache_examples=False,    # 예시 응답 캐싱 비활성화
    )


# ─── 고급 Blocks 기반 예시 ────────────────────────────────────────
def create_advanced_demo() -> gr.Blocks:
    """
    gr.Blocks를 사용한 커스텀 레이아웃 챗봇
    - 사이드바에 모델 설정 추가
    - 시스템 프롬프트 변경 가능
    - 대화 초기화 버튼
    """
    with gr.Blocks(title="고급 Gradio 챗봇") as demo:
        gr.Markdown("## 고급 Gradio 챗봇")
        gr.Markdown(f"모델: `{MODEL}` | 목 모드: `{'켜짐' if USE_MOCK else '꺼짐'}`")

        with gr.Row():
            # 왼쪽: 채팅 영역
            with gr.Column(scale=3):
                chatbot = gr.Chatbot(
                    type="messages",
                    height=450,
                    show_copy_button=True,  # 메시지 복사 버튼
                    avatar_images=(None, "🤖"),  # 사용자, 어시스턴트 아바타
                )
                with gr.Row():
                    msg = gr.Textbox(
                        placeholder="메시지를 입력하세요...",
                        scale=4,
                        container=False,
                    )
                    send_btn = gr.Button("전송", variant="primary", scale=1)

            # 오른쪽: 설정 패널
            with gr.Column(scale=1):
                gr.Markdown("### 설정")
                system_prompt = gr.Textbox(
                    label="시스템 프롬프트",
                    value="당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
                    lines=4,
                )
                temperature = gr.Slider(
                    label="Temperature",
                    minimum=0.0,
                    maximum=2.0,
                    value=0.7,
                    step=0.1,
                )
                clear_btn = gr.ClearButton([msg, chatbot], value="대화 초기화")

        def respond_with_system(message, chat_history, sys_prompt, temp):
            """시스템 프롬프트와 temperature를 반영한 응답 생성"""
            if not message.strip():
                return "", chat_history

            if USE_MOCK:
                response = f"[목] {sys_prompt[:20]}... | 온도: {temp} | 응답: '{message}'"
                chat_history.append({"role": "user", "content": message})
                chat_history.append({"role": "assistant", "content": response})
                return "", chat_history

            # 시스템 프롬프트 + 히스토리 구성
            api_messages = [{"role": "system", "content": sys_prompt}] + chat_history
            api_messages.append({"role": "user", "content": message})

            stream = client.chat.completions.create(
                model=MODEL,
                messages=api_messages,
                stream=True,
                temperature=temp,
            )

            # 스트리밍 응답 처리
            chat_history.append({"role": "user", "content": message})
            chat_history.append({"role": "assistant", "content": ""})

            partial = ""
            for chunk in stream:
                content = chunk.choices[0].delta.content
                if content:
                    partial += content
                    chat_history[-1]["content"] = partial
                    yield "", chat_history

        # 이벤트 연결
        msg.submit(
            respond_with_system,
            inputs=[msg, chatbot, system_prompt, temperature],
            outputs=[msg, chatbot],
        )
        send_btn.click(
            respond_with_system,
            inputs=[msg, chatbot, system_prompt, temperature],
            outputs=[msg, chatbot],
        )

    return demo


# ─── 메인 실행 ────────────────────────────────────────────────────
if __name__ == "__main__":
    # 기본 ChatInterface 실행 (간단 버전)
    # demo = create_basic_demo()

    # 고급 Blocks 버전 실행
    demo = create_advanced_demo()

    demo.launch(
        server_name="0.0.0.0",  # 로컬 네트워크에서 접근 허용
        server_port=7860,
        share=False,            # True로 변경하면 임시 공개 URL 생성 (7일)
        show_error=True,
    )
