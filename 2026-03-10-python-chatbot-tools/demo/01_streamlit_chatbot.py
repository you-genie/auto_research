"""
Streamlit 챗봇 데모
===================
실행 방법: streamlit run 01_streamlit_chatbot.py
접속 URL:  http://localhost:8501

이 데모는 Streamlit의 채팅 컴포넌트를 사용하여
OpenAI GPT-4o와 대화하는 챗봇을 구현합니다.

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
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"

# ─── OpenAI 클라이언트 초기화 ─────────────────────────────────────
if not USE_MOCK:
    from openai import OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        st.error("OPENAI_API_KEY 환경변수를 설정해주세요. .env 파일을 확인하세요.")
        st.stop()
    client = OpenAI(api_key=api_key)


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


def stream_openai_response(messages: list[dict]):
    """OpenAI API 스트리밍 응답 제너레이터"""
    stream = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        stream=True,
    )
    for chunk in stream:
        content = chunk.choices[0].delta.content
        if content is not None:
            yield content


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
    # 초기 시스템 메시지 설정
    st.session_state.messages = [
        {"role": "system", "content": system_prompt}
    ]

# ─── 기존 메시지 렌더링 ───────────────────────────────────────────
for message in st.session_state.messages:
    # 시스템 메시지는 화면에 표시하지 않음
    if message["role"] == "system":
        continue
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
        # API 메시지: 시스템 프롬프트 + 대화 히스토리
        api_messages = [{"role": "system", "content": system_prompt}] + [
            m for m in st.session_state.messages if m["role"] != "system"
        ]

        if USE_MOCK:
            # 목 모드: 에코 응답
            mock_text = get_mock_response(api_messages)
            response = st.write_stream(stream_mock_response(mock_text))
        else:
            # 실제 OpenAI API 스트리밍 응답
            response = st.write_stream(stream_openai_response(api_messages))

    # 어시스턴트 응답을 히스토리에 추가
    st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    # streamlit run 명령어로 실행해야 합니다
    # python 01_streamlit_chatbot.py 로는 실행되지 않습니다
    pass
