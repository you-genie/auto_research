"""
Reflex 챗봇 데모
================
실행 방법:
  cd 04_reflex_chatbot
  reflex init    # 최초 1회 초기화
  reflex run     # 개발 서버 시작
접속 URL: http://localhost:3000

이 데모는 Reflex 프레임워크를 사용하여
파이썬만으로 완전한 풀스택 챗봇 웹앱을 구현합니다.

핵심 개념:
- rx.State: 반응형 상태 관리
- 컴포넌트 함수: UI를 Python 함수로 정의
- 이벤트 핸들러: UI 이벤트를 State 메서드로 처리
- yield: 비동기 UI 업데이트 (스트리밍 효과)
"""

import os
import time
import reflex as rx
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# ─── 설정 ───────────────────────────────────────────────────────────
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-haiku-4-5-20251001")
USE_MOCK = os.getenv("USE_MOCK", "false").lower() == "true"
SYSTEM_PROMPT = "당신은 도움이 되는 AI 어시스턴트입니다. 한국어로 답변해주세요."

# ─── Anthropic 클라이언트 ───────────────────────────────────────────
if not USE_MOCK:
    import anthropic
    api_key = os.getenv("ANTHROPIC_API_KEY")
    client = anthropic.Anthropic(api_key=api_key) if api_key else None


# ─── 메시지 데이터 모델 ──────────────────────────────────────────
class Message(rx.Base):
    """채팅 메시지를 나타내는 데이터 클래스"""
    role: str       # "user" 또는 "assistant"
    content: str    # 메시지 내용


# ─── 앱 상태 클래스 ──────────────────────────────────────────────
class ChatState(rx.State):
    """
    앱의 전체 상태를 관리하는 클래스.
    모든 state 변수는 반응형(reactive)으로, 변경 시 UI가 자동 업데이트됩니다.
    """
    messages: list[Message] = []    # 대화 히스토리
    current_input: str = ""          # 현재 입력 텍스트
    is_loading: bool = False         # 응답 생성 중 여부
    error_msg: str = ""              # 오류 메시지

    @rx.var
    def has_messages(self) -> bool:
        """메시지가 있는지 여부를 반환하는 계산된 변수"""
        return len(self.messages) > 0

    async def send_message(self):
        """
        사용자 메시지를 전송하고 AI 응답을 받는 이벤트 핸들러.
        """
        # 빈 입력 무시
        user_text = self.current_input.strip()
        if not user_text:
            return

        # 입력창 초기화 및 로딩 시작
        self.current_input = ""
        self.is_loading = True
        self.error_msg = ""

        # 사용자 메시지를 히스토리에 추가
        self.messages.append(Message(role="user", content=user_text))
        yield  # UI 즉시 업데이트

        try:
            if USE_MOCK:
                mock_response = (
                    f"[목 응답] '{user_text}'를 받았습니다! "
                    "Reflex는 파이썬만으로 풀스택 웹앱을 만들 수 있는 프레임워크입니다."
                )
                self.messages.append(Message(role="assistant", content=""))
                yield

                for char in mock_response:
                    self.messages[-1].content += char
                    time.sleep(0.02)
                    yield
            else:
                if not client:
                    raise ValueError("ANTHROPIC_API_KEY가 설정되지 않았습니다.")

                # API 메시지 구성
                api_messages = []
                for msg in self.messages:
                    api_messages.append({"role": msg.role, "content": msg.content})

                # 어시스턴트 응답 메시지 추가 (빈 내용으로 시작)
                self.messages.append(Message(role="assistant", content=""))
                yield

                # Claude 스트리밍 응답
                with client.messages.stream(
                    model=MODEL,
                    max_tokens=1024,
                    system=SYSTEM_PROMPT,
                    messages=api_messages,
                ) as stream:
                    for text in stream.text_stream:
                        self.messages[-1].content += text
                        yield  # 토큰마다 UI 업데이트

        except Exception as e:
            self.error_msg = f"오류가 발생했습니다: {str(e)}"
            if self.messages and self.messages[-1].role == "assistant":
                self.messages[-1].content = f"[오류] {str(e)}"

        finally:
            self.is_loading = False

    def clear_chat(self):
        """대화를 초기화합니다."""
        self.messages = []
        self.current_input = ""
        self.is_loading = False
        self.error_msg = ""

    def set_input(self, value: str):
        """입력 텍스트를 업데이트합니다."""
        self.current_input = value


# ─── UI 컴포넌트 ─────────────────────────────────────────────────
def message_bubble(message: Message) -> rx.Component:
    """개별 채팅 메시지 버블 컴포넌트."""
    is_user = message.role == "user"

    return rx.box(
        rx.hstack(
            rx.box(
                rx.text("👤" if is_user else "🤖"),
                min_width="40px",
                text_align="center",
            ),
            rx.box(
                rx.markdown(message.content),
                background_color="#DCF8C6" if is_user else "#FFFFFF",
                border_radius="12px",
                padding="12px 16px",
                box_shadow="0 1px 2px rgba(0,0,0,0.1)",
                max_width="75%",
            ),
            justify="end" if is_user else "start",
            align_items="flex-start",
        ),
        width="100%",
        padding="4px 8px",
    )


def chat_area() -> rx.Component:
    """채팅 메시지 영역 컴포넌트"""
    return rx.vstack(
        rx.cond(
            ~ChatState.has_messages,
            rx.center(
                rx.vstack(
                    rx.text("💬", font_size="48px"),
                    rx.text(
                        "대화를 시작해보세요!",
                        color="#999",
                        font_size="18px",
                    ),
                    align="center",
                    spacing="2",
                ),
                height="300px",
            ),
        ),
        rx.foreach(ChatState.messages, message_bubble),
        rx.cond(
            ChatState.is_loading,
            rx.hstack(
                rx.spinner(size="3"),
                rx.text("응답 생성 중...", color="#666"),
                padding="8px",
            ),
        ),
        width="100%",
        spacing="2",
        padding="16px",
        min_height="400px",
    )


def input_area() -> rx.Component:
    """메시지 입력 영역 컴포넌트"""
    return rx.hstack(
        rx.text_area(
            placeholder="메시지를 입력하세요... (Shift+Enter: 줄바꿈, Enter: 전송)",
            value=ChatState.current_input,
            on_change=ChatState.set_input,
            on_key_down=rx.cond(
                rx.Var.create("event.key === 'Enter' && !event.shiftKey"),
                ChatState.send_message,
                rx.noop(),
            ),
            flex="1",
            resize="none",
            rows="3",
            disabled=ChatState.is_loading,
        ),
        rx.button(
            rx.cond(
                ChatState.is_loading,
                rx.spinner(size="2"),
                rx.text("전송"),
            ),
            on_click=ChatState.send_message,
            disabled=ChatState.is_loading,
            color_scheme="blue",
            size="3",
            height="72px",
        ),
        width="100%",
        align_items="flex-end",
        spacing="2",
    )


def chat_app() -> rx.Component:
    """메인 앱 컴포넌트"""
    return rx.center(
        rx.vstack(
            rx.hstack(
                rx.heading("Reflex 챗봇 데모", size="6"),
                rx.spacer(),
                rx.badge(
                    f"{'목 모드' if USE_MOCK else MODEL}",
                    color_scheme="green" if USE_MOCK else "blue",
                ),
                rx.button(
                    "대화 초기화",
                    on_click=ChatState.clear_chat,
                    variant="outline",
                    size="2",
                ),
                width="100%",
                align_items="center",
            ),
            rx.divider(),
            rx.cond(
                ChatState.error_msg != "",
                rx.callout(
                    ChatState.error_msg,
                    color="red",
                    variant="surface",
                    width="100%",
                ),
            ),
            rx.scroll_area(
                chat_area(),
                height="500px",
                type="auto",
                width="100%",
                id="chat-scroll",
            ),
            rx.divider(),
            input_area(),
            rx.text(
                "Enter: 전송 | Shift+Enter: 줄바꿈",
                color="#999",
                font_size="12px",
            ),
            width="100%",
            max_width="800px",
            padding="24px",
            spacing="3",
        ),
        width="100%",
        min_height="100vh",
        background_color="#f5f5f5",
    )


# ─── 앱 초기화 ───────────────────────────────────────────────────
app = rx.App(
    theme=rx.theme(
        appearance="light",
        accent_color="blue",
    )
)
app.add_page(chat_app, route="/", title="Reflex 챗봇")
