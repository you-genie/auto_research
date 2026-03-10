"""
중급 Chainlit 챗봇 데모
=======================
파일 업로드, 세션 관리, 채팅 프로필, 인증 등의 기능을 활용한 챗봇입니다.

주요 기능:
- 파일 업로드 (이미지, PDF, 텍스트)
- 이미지 비전 분석 (GPT-4o)
- PDF/텍스트 파일 내용 추출 및 Q&A
- 채팅 프로필 선택 (GPT-4o / GPT-4o-mini)
- 사용자 세션 관리 (대화 기록, 업로드된 파일 관리)
- 패스워드 기반 인증
- 채팅 설정 (temperature, max_tokens)
- 단계별 처리 과정 시각화 (Steps)

실행 방법:
    1. pip install -r requirements.txt
    2. cp .env.example .env  (그리고 .env에 API 키 입력)
    3. chainlit run app.py -w
"""

import os
import base64
import asyncio
from pathlib import Path
from dotenv import load_dotenv

import chainlit as cl
from openai import AsyncOpenAI

# .env 파일 로드
load_dotenv()

# OpenAI 클라이언트 초기화
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 어드민 계정 정보 (데모용 - 실제 프로덕션에서는 DB 사용)
ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "changeme123")


# -------------------------------------------------------
# 패스워드 인증 콜백
# -------------------------------------------------------
@cl.password_auth_callback
def auth_callback(username: str, password: str) -> cl.User | None:
    """
    사용자가 로그인할 때 호출됩니다.
    실제 프로덕션에서는 DB에서 사용자 정보를 조회해야 합니다.

    반환값:
        cl.User: 인증 성공 시 사용자 객체
        None: 인증 실패 시
    """
    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        return cl.User(
            identifier=username,
            metadata={
                "role": "admin",
                "provider": "credentials",
                "display_name": "관리자"
            }
        )
    # 일반 사용자 허용 (데모 목적)
    if username and password and len(password) >= 4:
        return cl.User(
            identifier=username,
            metadata={
                "role": "user",
                "provider": "credentials",
                "display_name": username
            }
        )
    return None  # 인증 실패


# -------------------------------------------------------
# 채팅 프로필 설정 (사용자가 시작 전에 선택)
# -------------------------------------------------------
@cl.set_chat_profiles
async def chat_profile(current_user: cl.User) -> list[cl.ChatProfile]:
    """
    사용자가 채팅을 시작하기 전에 AI 모델을 선택할 수 있게 합니다.
    """
    return [
        cl.ChatProfile(
            name="GPT-4o (고성능)",
            markdown_description=(
                "**GPT-4o** 모델을 사용합니다.\n\n"
                "- 이미지 분석 지원\n"
                "- 복잡한 추론 능력\n"
                "- 다국어 처리 우수"
            ),
            icon="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
        ),
        cl.ChatProfile(
            name="GPT-4o-mini (빠름)",
            markdown_description=(
                "**GPT-4o-mini** 모델을 사용합니다.\n\n"
                "- 빠른 응답 속도\n"
                "- 저비용\n"
                "- 간단한 작업에 적합"
            ),
            icon="https://upload.wikimedia.org/wikipedia/commons/0/04/ChatGPT_logo.svg",
        ),
    ]


# -------------------------------------------------------
# 채팅 세션 시작 핸들러
# -------------------------------------------------------
@cl.on_chat_start
async def on_chat_start():
    """
    채팅 세션이 시작될 때 호출됩니다.
    - 선택된 채팅 프로필에 따라 모델을 설정합니다.
    - 채팅 설정 UI를 초기화합니다.
    - 사용자 세션을 설정합니다.
    """
    # 선택된 채팅 프로필 가져오기
    chat_profile = cl.user_session.get("chat_profile")
    if chat_profile == "GPT-4o (고성능)":
        model = "gpt-4o"
    else:
        model = "gpt-4o-mini"

    # 현재 로그인된 사용자 정보
    current_user = cl.user_session.get("user")
    display_name = current_user.metadata.get("display_name", "사용자") if current_user else "사용자"

    # 세션 초기화
    cl.user_session.set("model", model)
    cl.user_session.set("message_history", [
        {
            "role": "system",
            "content": (
                "당신은 친절하고 전문적인 AI 어시스턴트입니다. "
                "이미지, PDF, 텍스트 파일을 분석하고 질문에 답할 수 있습니다. "
                "한국어로 대화하며, 파일이 첨부되면 내용을 분석하여 답변합니다."
            )
        }
    ])
    cl.user_session.set("uploaded_files", {})  # 업로드된 파일 캐시
    cl.user_session.set("conversation_count", 0)

    # 채팅 설정 UI (온도, 최대 토큰)
    settings = await cl.ChatSettings([
        cl.input_widget.Slider(
            id="temperature",
            label="Temperature (창의성)",
            initial=0.7,
            min=0.0,
            max=2.0,
            step=0.1,
            tooltip="높을수록 더 창의적이고 다양한 답변을 생성합니다"
        ),
        cl.input_widget.Slider(
            id="max_tokens",
            label="최대 응답 길이",
            initial=1000,
            min=100,
            max=4000,
            step=100,
            tooltip="응답의 최대 토큰 수를 설정합니다"
        ),
        cl.input_widget.Switch(
            id="show_steps",
            label="처리 과정 표시",
            initial=True,
            tooltip="파일 분석 등의 처리 과정을 단계별로 표시합니다"
        ),
    ]).send()

    # 설정 값 저장
    cl.user_session.set("settings", {
        "temperature": settings["temperature"],
        "max_tokens": int(settings["max_tokens"]),
        "show_steps": settings["show_steps"],
    })

    # 환영 메시지
    await cl.Message(
        content=(
            f"안녕하세요, **{display_name}**님! 👋\n\n"
            f"**{chat_profile}** 프로필로 시작합니다.\n\n"
            "다음 기능을 사용할 수 있습니다:\n"
            "- 💬 일반 대화 및 질문\n"
            "- 🖼️ 이미지 첨부 및 분석 (드래그&드롭 또는 클립 버튼)\n"
            "- 📄 PDF/텍스트 파일 업로드 및 Q&A\n"
            "- ⚙️ 좌측 설정 패널에서 모델 파라미터 조정 가능\n\n"
            "무엇이든 물어보세요!"
        )
    ).send()


# -------------------------------------------------------
# 채팅 설정 변경 핸들러
# -------------------------------------------------------
@cl.on_settings_update
async def on_settings_update(settings: dict):
    """
    사용자가 채팅 설정을 변경할 때 호출됩니다.
    """
    cl.user_session.set("settings", {
        "temperature": settings["temperature"],
        "max_tokens": int(settings["max_tokens"]),
        "show_steps": settings["show_steps"],
    })
    await cl.Message(
        content=f"설정이 업데이트되었습니다: temperature={settings['temperature']:.1f}, max_tokens={int(settings['max_tokens'])}",
        author="System"
    ).send()


# -------------------------------------------------------
# 파일 처리 함수들
# -------------------------------------------------------
async def process_image(file: cl.File) -> str:
    """
    이미지 파일을 base64로 인코딩하여 GPT-4o에 전달할 수 있는 형식으로 변환합니다.
    """
    with open(file.path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")
    return image_data


async def extract_text_from_file(file: cl.File) -> str:
    """
    텍스트 파일 또는 PDF에서 텍스트를 추출합니다.
    """
    suffix = Path(file.path).suffix.lower()

    if suffix == ".pdf":
        # PDF 텍스트 추출
        try:
            import PyPDF2
            text_content = []
            with open(file.path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                for page_num, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text:
                        text_content.append(f"[페이지 {page_num}]\n{page_text}")
            return "\n\n".join(text_content)
        except Exception as e:
            return f"PDF 추출 실패: {str(e)}"

    elif suffix in [".txt", ".md", ".csv", ".json", ".py", ".js", ".html", ".xml"]:
        # 텍스트 파일 직접 읽기
        with open(file.path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    else:
        return f"지원하지 않는 파일 형식입니다: {suffix}"


# -------------------------------------------------------
# 메시지 수신 핸들러
# -------------------------------------------------------
@cl.on_message
async def on_message(message: cl.Message):
    """
    사용자 메시지를 처리합니다.
    - 첨부된 파일을 분석합니다.
    - OpenAI API를 호출합니다.
    - 결과를 스트리밍으로 전달합니다.
    """
    # 세션 데이터 가져오기
    model = cl.user_session.get("model", "gpt-4o-mini")
    settings = cl.user_session.get("settings", {
        "temperature": 0.7,
        "max_tokens": 1000,
        "show_steps": True
    })
    message_history = cl.user_session.get("message_history", [])
    uploaded_files_cache = cl.user_session.get("uploaded_files", {})

    # 대화 카운터 증가
    count = cl.user_session.get("conversation_count", 0) + 1
    cl.user_session.set("conversation_count", count)

    show_steps = settings.get("show_steps", True)

    # 현재 메시지의 내용 (텍스트 + 파일)
    current_content = []

    # 파일 처리
    if message.elements:
        for element in message.elements:
            if not isinstance(element, cl.File):
                continue

            file_name = element.name
            mime = getattr(element, "mime", "") or ""

            if show_steps:
                async with cl.Step(name=f"파일 분석: {file_name}") as step:
                    step.input = f"파일: {file_name} (형식: {mime})"

                    if "image" in mime:
                        # 이미지 처리
                        image_data = await process_image(element)
                        uploaded_files_cache[file_name] = {
                            "type": "image",
                            "data": image_data,
                            "mime": mime
                        }
                        # 이미지를 메시지 컨텐츠에 추가
                        current_content.append({
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:{mime};base64,{image_data}"
                            }
                        })
                        step.output = f"이미지 로드 완료 ({mime})"

                    else:
                        # 텍스트/PDF 처리
                        extracted_text = await extract_text_from_file(element)
                        uploaded_files_cache[file_name] = {
                            "type": "text",
                            "content": extracted_text[:5000]  # 최대 5000자
                        }
                        step.output = f"텍스트 추출 완료 ({len(extracted_text)}자)"
            else:
                # 단계 표시 없이 처리
                if "image" in mime:
                    image_data = await process_image(element)
                    current_content.append({
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime};base64,{image_data}"}
                    })

        # 업로드된 파일 캐시 저장
        cl.user_session.set("uploaded_files", uploaded_files_cache)

        # 텍스트 파일 내용을 사용자 메시지에 포함
        text_files_context = []
        for fname, fdata in uploaded_files_cache.items():
            if fdata["type"] == "text":
                text_files_context.append(
                    f"=== {fname} 파일 내용 ===\n{fdata['content']}"
                )

        # 사용자 메시지 텍스트 구성
        user_text = message.content
        if text_files_context:
            user_text += "\n\n" + "\n\n".join(text_files_context)

        current_content.insert(0, {"type": "text", "text": user_text})
    else:
        # 파일 없는 일반 텍스트 메시지
        current_content = message.content

    # 사용자 메시지를 대화 기록에 추가
    message_history.append({
        "role": "user",
        "content": current_content
    })

    # 응답 메시지 생성 (스트리밍용)
    response_msg = cl.Message(content="")
    await response_msg.send()

    # OpenAI API 호출 (스트리밍)
    full_response = ""
    try:
        stream = await client.chat.completions.create(
            model=model,
            messages=message_history,
            stream=True,
            temperature=settings["temperature"],
            max_tokens=settings["max_tokens"],
        )

        async for chunk in stream:
            if chunk.choices[0].delta.content is not None:
                token = chunk.choices[0].delta.content
                full_response += token
                await response_msg.stream_token(token)

    except Exception as e:
        error_msg = f"API 호출 오류: {str(e)}"
        full_response = error_msg
        await response_msg.stream_token(error_msg)

    await response_msg.update()

    # AI 응답을 대화 기록에 추가
    message_history.append({
        "role": "assistant",
        "content": full_response
    })

    # 업데이트된 대화 기록 저장 (최근 20턴만 유지 - 토큰 절약)
    if len(message_history) > 41:  # 시스템 메시지 1개 + 최근 40개
        message_history = [message_history[0]] + message_history[-40:]

    cl.user_session.set("message_history", message_history)


# -------------------------------------------------------
# 채팅 종료 핸들러
# -------------------------------------------------------
@cl.on_chat_end
async def on_chat_end():
    """
    채팅 세션이 종료될 때 호출됩니다.
    실제 프로덕션에서는 대화 기록을 DB에 저장할 수 있습니다.
    """
    user = cl.user_session.get("user")
    count = cl.user_session.get("conversation_count", 0)
    username = user.identifier if user else "anonymous"
    print(f"[INFO] 사용자 '{username}' 채팅 종료 - 총 {count}번 대화")
