"""
Streamlit 챗봇 데모
===================
실행 방법: streamlit run 01_streamlit_chatbot.py
접속 URL:  http://localhost:8501

이 데모는 Streamlit의 채팅 컴포넌트를 사용하여
Claude Haiku와 대화하는 챗봇을 구현합니다.

핵심 컴포넌트:
- st.chat_message(): 채팅 버블 컨테이너
- st.chat_input(): 하단 고정 입력창
- st.write_stream(): 스트리밍 응답 렌더링
"""

import os
import time
import streamlit as st
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
        st.error("ANTHROPIC_API_KEY 환경변수를 설정해주세요. .env 파일을 확인하세요.")
        st.stop()
    client = anthropic.Anthropic(api_key=api_key)


def get_mock_response(messages: list[dict]) -> str:
    """API 키 없이 테스트할 수 있는 목(Mock) 응답 생성기"""
    last_user_msg = next(
        (m["content"] for m in reversed(messages) if m["role"] == "user"),
        "안녕하세요"
    )
    return f"[목 응답] 다음 메시지를 받았습니다: '{last_user_msg}'"


def stream_mock_response(text: str):
    """목 응답을 스트리밍처럼 생성하는 제너레이터"""
    for char in text:
        yield char
        time.sleep(0.03)  # 타이핑 효과를 위한 지연


def stream_claude_response(messages: list[dict], system_prompt: str):
    """Claude API 스트리밍 응답 제너레이터"""
    with client.messages.stream(
        model=MODEL,
        max_tokens=1024,
        system=system_prompt,
        messages=[m for m in messages if m["role"] != "system"],
    ) as stream:
        for text in stream.text_stream:
            yield text


# ─── 페이지 설정 ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Streamlit 챗봇 데모",
    page_icon="💬",
    layout="centered",
)

st.title("💬 Streamlit 챗봇 데모")
st.caption(f"모델: {MODEL} | 목 모드: {'켜짐' if USE_MOCK else '꺼짐'}")

# ─── 사이드바: 설정 패널 ─────────────────────────────────────────
with st.sidebar:
    st.header("설정")

    # 시스템 프롬프트 설정
    system_prompt = st.text_area(
        "시스템 프롬프트",
        value="당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요.",
        height=100,
    )

    # 대화 초기화 버튼
    if st.button("대화 초기화", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.divider()
    st.markdown("**사용법**")
    st.markdown("- 하단 입력창에 메시지 입력 후 Enter")
    st.markdown("- 사이드바에서 시스템 프롬프트 변경 가능")

# ─── 세션 상태 초기화 ────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

# ─── 기존 메시지 렌더링 ───────────────────────────────────────────
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ─── 사용자 입력 처리 ────────────────────────────────────────────
if prompt := st.chat_input("메시지를 입력하세요..."):
    # 사용자 메시지를 히스토리에 추가
    st.session_state.messages.append({"role": "user", "content": prompt})

    # 사용자 메시지 표시
    with st.chat_message("user"):
        st.markdown(prompt)

    # 어시스턴트 응답 생성 및 스트리밍 표시
    with st.chat_message("assistant"):
        if USE_MOCK:
            # 목 모드: 에코 응답
            mock_text = get_mock_response(st.session_state.messages)
            response = st.write_stream(stream_mock_response(mock_text))
        else:
            # 실제 Claude API 스트리밍 응답
            response = st.write_stream(
                stream_claude_response(st.session_state.messages, system_prompt)
            )

    # 어시스턴트 응답을 히스토리에 추가
    st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    # streamlit run 명령어로 실행해야 합니다
    # python 01_streamlit_chatbot.py 로는 실행되지 않습니다
    pass
