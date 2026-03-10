# 파이썬 개발자를 위한 클린코드 가이드
## PPT 슬라이드 아웃라인 — Python 3.12/3.13 신기능 중심, AI 개발자 대상

---

## Slide 1: 표지 (Cover)
**Visual**: 파이썬 로고와 AI 신경망 배경 이미지. 제목은 크고 굵게, 부제목은 중간 크기. 다크 블루 + 그린 계열 그라디언트 배경.
**Key Points**:
- 파이썬 클린코드 가이드
- Python 3.12 / 3.13
- AI 백엔드 · 프론트엔드 개발자 대상
**Speaker Notes**: 이 발표는 FastAPI, Streamlit, LLM 애플리케이션, RAG 파이프라인을 개발하는 파이썬 개발자를 위한 실용적인 클린코드 가이드입니다. Python 3.12와 3.13의 신기능을 중심으로, 실제 AI 개발 맥락에서 코드 품질을 높이는 방법을 다룹니다.

---

## Slide 2: 목차 (Agenda)
**Visual**: 6개 섹션을 아이콘과 함께 나열한 타임라인 또는 그리드 레이아웃. 각 항목 옆에 작은 아이콘(뱀, 서버, 화면, 연결, 도구 아이콘 등).
**Key Points**:
- Python 3.12 신기능
- Python 3.13 신기능
- AI 백엔드 패턴
- AI 프론트엔드 패턴
- LLM 공통 패턴
- 도구 추천
**Speaker Notes**: 총 6개 파트로 구성됩니다. 파트 1-2는 언어 레벨의 새 기능, 파트 3-5는 AI 개발 실전 패턴, 파트 6은 개발 도구 생태계를 다룹니다. 각 파트에는 Before/After 코드 비교가 포함됩니다.

---

## Slide 3: 섹션 구분 — Python 3.12
**Visual**: "Part 1" 대형 텍스트, Python 3.12 로고, 출시일 "2023년 10월 2일" 표시. 다크 블루 배경에 흰색 텍스트.
**Key Points**:
- Part 1
- Python 3.12
- 클린코드 신기능 5가지
**Speaker Notes**: Python 3.12는 2023년 10월에 출시되었습니다. 클린코드 관점에서 가장 중요한 변화 5가지를 살펴봅니다: 개선된 f-string, 타입 파라미터 문법, @override 데코레이터, 향상된 에러 메시지, Per-Interpreter GIL.

---

## Slide 4: PEP 701 — f-string 개선
**Visual**: 좌우 분할 레이아웃. 왼쪽 "Before" (빨간 테두리, Python 3.11-), 오른쪽 "After" (초록 테두리, Python 3.12+). 코드 블록 폰트(JetBrains Mono).
**Key Points**:
- 따옴표 자유 재사용
- 백슬래시 허용
- 여러 줄 + 주석 가능
**Speaker Notes**:
PEP 701은 f-string의 오랜 제약을 제거했습니다.

Before (Python 3.11-):
```python
# 내부에서 외부와 다른 따옴표 강제 사용
msg = f"Playlist: {', '.join(songs)}"
newline = "\n"  # 백슬래시 우회를 위한 변수
msg2 = f"Songs:\n{newline.join(songs)}"
```

After (Python 3.12+):
```python
msg = f"Playlist: {", ".join(songs)}"  # 따옴표 재사용
msg2 = f"Songs:\n{"\n".join(songs)}"   # 백슬래시 직접 사용
```

AI 프롬프트나 RAG 결과 포매팅에 특히 유용합니다. 성능도 64% 향상.

---

## Slide 5: f-string AI 실전 예시
**Visual**: 코드 블록 중심. RAG 응답 포매팅 Before/After. 녹색 하이라이트로 개선된 부분 강조.
**Key Points**:
- RAG 결과 포매팅
- 중첩 리스트 컴프리헨션
- 코드 라인 수 감소
**Speaker Notes**:
LLM 프롬프트 조립 예시:

After:
```python
llm_context = f"""
Context:
{"\n".join([
    f"- {doc['title']}: {doc['content'][:200]}"  # 처음 200자만
    for doc in retrieved_docs
])}
"""
```

이전에는 이 코드가 여러 단계(리스트 컴프리헨션 → 변수 저장 → f-string 삽입)로 나뉘어야 했습니다. 이제 한 번에 작성 가능.

---

## Slide 6: PEP 695 — 타입 파라미터 문법
**Visual**: 3단 비교 표. 왼쪽: 이전 코드(TypeVar 명시적 임포트), 오른쪽: 새 문법(간결한 대괄호 문법). 중앙에 화살표. 하단에 `type` 키워드 설명 박스.
**Key Points**:
- `def func[T](...)` 새 문법
- `type X = ...` 타입 별칭
- TypeVar 임포트 불필요
**Speaker Notes**:
Before:
```python
from typing import TypeVar, Generic
T = TypeVar("T")
class Repository(Generic[T]): ...
from typing import TypeAlias
EmbeddingVector: TypeAlias = list[float]
```

After (Python 3.12+):
```python
class Repository[T]: ...
type EmbeddingVector = list[float]
type DocumentID = str
type RetrievalResult = tuple[DocumentID, float]
```

AI 개발에서 `Repository[Document]`, `Repository[Chunk]` 처럼 타입을 명시하면 IDE 자동완성이 훨씬 정확해집니다.

---

## Slide 7: PEP 698 — @override 데코레이터
**Visual**: LLM Provider 클래스 계층도 다이어그램. `BaseLLMProvider` → `OpenAIProvider`, `AnthropicProvider`, `GeminiProvider`. 잘못된 메서드 이름에 빨간 X 표시, 올바른 것에 초록 체크.
**Key Points**:
- 오타 즉시 감지
- 타입 체커 연동
- 다중 공급자 패턴
**Speaker Notes**:
Before:
```python
class OpenAIProvider(BaseLLMProvider):
    def complet(self, prompt: str) -> str:  # 오타! 아무도 모름
        ...
```

After (Python 3.12+):
```python
from typing import override
class OpenAIProvider(BaseLLMProvider):
    @override
    def complet(self, prompt: str) -> str:  # 타입 체커가 즉시 오류 감지
        ...
    # Error: Method "complet" does not override any base class method
```

여러 LLM 공급자(OpenAI, Anthropic, Gemini 등)를 추상화할 때 특히 유용합니다.

---

## Slide 8: 개선된 에러 메시지 (3.12)
**Visual**: 터미널 스크린샷 형태의 3개 박스. 각 박스에 오류 유형(NameError, ImportError, SyntaxError)과 친절한 제안 메시지. "Did you mean?" 부분을 노란색 하이라이트.
**Key Points**:
- 임포트 누락 제안
- self.속성 자동 제안
- 오타 수정 힌트
**Speaker Notes**:
Python 3.12의 개선된 에러 메시지:

1. `sys.version_info` → `NameError: Did you forget to import 'sys'?`
2. `return model` (ChatBot에서) → `NameError: Did you mean: 'self.model'?`
3. `from collections import chainmap` → `ImportError: Did you mean: 'ChainMap'?`

디버깅 시간을 크게 줄여주는 QoL 개선입니다.

---

## Slide 9: 섹션 구분 — Python 3.13
**Visual**: "Part 2" 대형 텍스트, Python 3.13 로고, 출시일 "2024년 10월 7일". 강조색으로 "Free-Threading", "JIT" 키워드 표시.
**Key Points**:
- Part 2
- Python 3.13
- 개발 경험 혁신
**Speaker Notes**: Python 3.13은 2024년 10월에 출시되었습니다. 개발자 경험 향상(REPL, 에러 메시지)과 함께 실험적 기능(Free-Threading, JIT)이 도입되었습니다. AI 개발자에게 중요한 typing 모듈 개선도 포함됩니다.

---

## Slide 10: 새로운 REPL + 에러 메시지 (3.13)
**Visual**: 좌우 분할. 왼쪽: 컬러 REPL 스크린샷(다채로운 프롬프트, 빨간 에러 강조), 오른쪽: "Did you mean?" 에러 메시지 예시. 새 기능 체크리스트 박스.
**Key Points**:
- 컬러 트레이스백
- 키워드 오타 제안
- 여러 줄 편집
**Speaker Notes**:
새 REPL 기능:
- 컬러 지원: 에러는 빨간색, 경고는 노란색
- `exit`, `quit`, `help` 괄호 없이 사용
- F3 붙여넣기 모드: 빈 줄 포함 코드 블록 처리
- `↑` 키로 이전 코드 블록 전체 불러오기

새 에러 메시지:
```
"Better error!".split(max_split=1)
TypeError: ... Did you mean 'maxsplit'?
```

---

## Slide 11: Free-Threaded Python (PEP 703)
**Visual**: 비교 다이어그램. 왼쪽: 단일 GIL로 스레드들이 대기하는 모습(병목). 오른쪽: GIL 없이 여러 코어에서 스레드들이 병렬 실행되는 모습. 중앙에 "실험적(Experimental)" 경고 배지.
**Key Points**:
- GIL 선택적 비활성화
- 멀티코어 진정한 병렬
- 아직 실험적
**Speaker Notes**:
활성화 방법:
```bash
PYTHON_GIL=0 python my_script.py
python -c "import sys; print(sys._is_gil_enabled())"  # False
```

AI 개발 주의사항:
- NumPy, PyTorch 등 주요 ML 라이브러리는 별도 호환 빌드 필요
- 단일 스레드 성능 30~40% 저하
- 프로덕션 환경에서는 아직 사용 금지
- Python 3.14-3.15에서 성숙 예정

---

## Slide 12: JIT 컴파일러 + typing 개선 (3.13)
**Visual**: 상단: JIT 아키텍처 플로우 다이어그램 (바이트코드 → 특화 명령어 → Tier 2 IR → 머신코드). 하단: typing 개선 3가지를 아이콘 카드 형태로.
**Key Points**:
- JIT: 기본 비활성화
- TypeIs — 정확한 타입 내로잉
- ReadOnly TypedDict
- @deprecated 데코레이터
**Speaker Notes**:
JIT:
```bash
PYTHON_JIT=1 python script.py  # 활성화
```
현재 몇 퍼센트 수준 개선. ML 워크로드는 NumPy/Numba가 더 효과적.

TypeIs (PEP 742):
```python
def is_valid_embedding(val: object) -> TypeIs[list[float]]:
    return isinstance(val, list) and all(isinstance(v, float) for v in val)
```

ReadOnly TypedDict (PEP 705):
```python
class LLMConfig(TypedDict):
    model: ReadOnly[str]  # 변경 불가
    temperature: float
```

---

## Slide 13: 섹션 구분 — AI 백엔드 패턴
**Visual**: "Part 3" 대형 텍스트. FastAPI, Pydantic 로고. 서버 아이콘과 API 엔드포인트 다이어그램.
**Key Points**:
- Part 3
- AI 백엔드
- FastAPI + Pydantic v2
**Speaker Notes**: FastAPI와 Pydantic v2를 사용한 AI 백엔드 개발에서의 클린코드 패턴을 다룹니다. 설정 관리, 스키마 설계, 의존성 주입, 에러 핸들링, 스트리밍 응답까지 실전 패턴을 살펴봅니다.

---

## Slide 14: 프로젝트 구조 — 도메인 중심 설계
**Visual**: 파일 트리 다이어그램. 도메인별 폴더(llm/, rag/, core/)를 색상으로 구분. 각 폴더 안에 router.py, schemas.py, service.py, dependencies.py 파일 아이콘. 우측에 역할 설명 말풍선.
**Key Points**:
- 파일 유형이 아닌 도메인별 구조
- 각 도메인 자체 완결
- 의존성 명확화
**Speaker Notes**:
권장 구조:
```
src/
├── core/           # 설정, 공통 의존성, 예외
├── llm/            # LLM API 연동
│   ├── router.py   # 엔드포인트
│   ├── schemas.py  # 요청/응답 모델
│   ├── service.py  # 비즈니스 로직
│   └── providers.py # LLM 공급자 추상화
└── rag/            # RAG 파이프라인
    ├── pipeline.py
    ├── retriever.py
    └── embedder.py
```

출처: FastAPI Best Practices (github.com/zhanymkanov/fastapi-best-practices)

---

## Slide 15: pydantic-settings — 설정 관리
**Visual**: Before/After 카드. Before: `os.getenv()` 코드 (타입 없음, None 위험 강조). After: `BaseSettings` 클래스 (타입 안전, 자동 검증 강조). 우측에 `.env` 파일 → Settings 클래스 → FastAPI 앱 흐름 화살표.
**Key Points**:
- 타입 안전 설정
- `SecretStr` API 키 보호
- `@lru_cache` 한 번만 로드
**Speaker Notes**:
Before:
```python
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # None일 수 있음
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "2048"))  # 형변환 직접
```

After:
```python
class LLMSettings(BaseSettings):
    openai_api_key: SecretStr
    max_tokens: int = Field(default=2048, ge=1, le=128000)

@lru_cache
def get_settings() -> AppSettings:
    return AppSettings()
```

SecretStr은 로그에서 자동으로 마스킹됩니다.

---

## Slide 16: Pydantic v2 스키마 설계
**Visual**: 요청/응답 모델 다이어그램. `ChatRequest` 모델의 각 필드에 검증 규칙(min_length, ge, le) 툴팁. 하단에 "자동 문서화" → Swagger UI 스크린샷 썸네일.
**Key Points**:
- `type` 별칭으로 가독성
- `field_validator` 도메인 규칙
- 자동 OpenAPI 문서화
**Speaker Notes**:
Python 3.12 타입 별칭 + Pydantic v2:
```python
type ModelName = Literal["gpt-4o", "gpt-4o-mini", "claude-3-5-sonnet-20241022"]
type Temperature = Annotated[float, Field(ge=0.0, le=2.0)]

class ChatRequest(BaseModel):
    messages: list[Message] = Field(min_length=1)
    model: ModelName = "gpt-4o"
    temperature: Temperature = 0.7

    @field_validator("messages")
    @classmethod
    def messages_must_end_with_user(cls, v):
        if v[-1].role != "user":
            raise ValueError("마지막 메시지는 user 역할이어야 합니다")
        return v
```

Pydantic v2는 v1 대비 최대 10배 빠른 검증 속도 (Rust 기반).

---

## Slide 17: 의존성 주입 패턴
**Visual**: FastAPI 의존성 주입 흐름 다이어그램. 라우터 함수 → Depends 화살표 → 각 의존성 함수(get_conversation, get_llm_client) → 공통 의존성(get_db, get_current_user). 계층형 트리 구조.
**Key Points**:
- 라우터는 얇게
- 검증 + 조회 = 의존성
- 의존성 캐시 활용
**Speaker Notes**:
```python
async def get_conversation(
    conversation_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Conversation:
    conv = await db.get(Conversation, conversation_id)
    if not conv:
        raise HTTPException(status_code=404, ...)
    return conv

@router.post("/conversations/{id}/messages")
async def add_message(
    request: ChatRequest,
    conversation: Conversation = Depends(get_conversation),
    llm: AsyncOpenAI = Depends(get_llm_client),
) -> ChatResponse:
    return await chat_service.process(conversation, request, llm)  # 비즈니스 로직만
```

---

## Slide 18: LLM 에러 핸들링 — 재시도 + 폴백
**Visual**: 에러 처리 플로우차트. LLM API 호출 → (성공) → 응답 반환 / (RateLimitError) → 지수 백오프 재시도 → (3회 실패) → 폴백 모델 전환. 각 단계에 아이콘.
**Key Points**:
- Tenacity 재시도
- 지수 백오프
- 폴백 모델 자동 전환
**Speaker Notes**:
```python
@retry(
    retry=retry_if_exception_type((RateLimitError, APITimeoutError)),
    wait=wait_exponential(multiplier=1, min=2, max=60),
    stop=stop_after_attempt(3),
    before_sleep=before_sleep_log(logger, logging.WARNING),
)
async def complete(self, messages, timeout=30.0) -> str:
    ...

async def complete_with_fallback(self, messages) -> str:
    try:
        return await self.complete(messages)
    except LLMError:
        logger.warning("기본 모델 실패, 폴백으로 전환")
        return await LLMProvider(self._client, "gpt-4o-mini").complete(messages)
```

---

## Slide 19: 스트리밍 응답 + 토큰 추적
**Visual**: 좌측: 스트리밍 SSE 흐름도 (LLM → 청크 → StreamingResponse → 클라이언트). 우측: 토큰 추적 대시보드 목업 (사용량, 비용 추정 표시).
**Key Points**:
- Server-Sent Events
- `StreamingResponse`
- 토큰/비용 구조화 로깅
**Speaker Notes**:
스트리밍:
```python
@router.post("/chat/stream")
async def stream_chat(request: ChatRequest) -> StreamingResponse:
    async def generate():
        async with llm_client.chat.completions.stream(...) as stream:
            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    data = json.dumps({"content": chunk.choices[0].delta.content})
                    yield f"data: {data}\n\n"
        yield "data: [DONE]\n\n"
    return StreamingResponse(generate(), media_type="text/event-stream")
```

토큰 추적은 structlog로 구조화하여 ELK/Datadog 등으로 수집합니다.

---

## Slide 20: 섹션 구분 — AI 프론트엔드 패턴
**Visual**: "Part 4" 대형 텍스트. Streamlit, Gradio 로고. 대화형 채팅 UI 화면 목업.
**Key Points**:
- Part 4
- AI 프론트엔드
- Streamlit · Gradio
**Speaker Notes**: Streamlit과 Gradio는 AI 프로토타이핑에서 가장 많이 사용되는 프레임워크입니다. 규모가 커질수록 상태 관리와 컴포넌트 분리 패턴이 유지보수성을 크게 좌우합니다.

---

## Slide 21: Streamlit — 상태·서비스·UI 분리
**Visual**: 3열 아키텍처 다이어그램. 왼쪽 열: state.py (ChatState 클래스), 중앙: service.py (ChatService), 오른쪽: components.py + app.py. 화살표로 의존 방향 표시.
**Key Points**:
- State: 세션 상태 중앙화
- Service: 비즈니스 로직 분리
- Components: UI 재사용
**Speaker Notes**:
Before: 모든 것이 한 파일에 섞임 (상태, LLM 호출, UI 렌더링)

After 구조:
- `state.py`: `ChatState` 데이터클래스 + `get_chat_state()` 함수
- `service.py`: `ChatService` 클래스 (OpenAI 호출)
- `components.py`: `render_message()`, `render_chat_history()`, `render_token_usage()`
- `app.py`: 위 세 모듈을 조합

핵심: `st.session_state`를 직접 다루는 코드를 `state.py`에만 격리합니다.

---

## Slide 22: Gradio — Blocks + 핸들러 분리
**Visual**: Gradio Blocks 레이아웃 다이어그램. UI 컴포넌트들(Chatbot, Textbox, Slider)과 이벤트 핸들러(ChatHandlers 클래스) 사이의 연결선. `handlers.py` ↔ `ui.py` 분리 강조.
**Key Points**:
- `ChatHandlers` 클래스
- `build_chat_ui()` 함수
- UI와 로직 완전 분리
**Speaker Notes**:
```python
# handlers.py
class ChatHandlers:
    def stream_response(self, message, history, system_prompt, temperature):
        # LLM 스트리밍 로직만 담당
        ...

# ui.py
def build_chat_ui(handlers: ChatHandlers) -> gr.Blocks:
    with gr.Blocks() as demo:
        chatbot = gr.Chatbot()
        msg = gr.Textbox()
        msg.submit(handlers.stream_response, inputs=[...], outputs=chatbot)
    return demo
```

이 구조에서 핸들러를 모킹(mocking)하여 UI 테스트가 가능합니다.

---

## Slide 23: 섹션 구분 — LLM 공통 패턴
**Visual**: "Part 5" 대형 텍스트. LLM 애플리케이션 아키텍처 개요 다이어그램 (사용자 → 프론트엔드 → 백엔드 → LLM API + 벡터 DB).
**Key Points**:
- Part 5
- LLM 공통 패턴
- 프롬프트 · RAG · 에이전트
**Speaker Notes**: LLM 애플리케이션 개발에서 공통적으로 등장하는 패턴을 다룹니다: 프롬프트 관리, RAG 파이프라인 구조화, AI 에이전트 아키텍처.

---

## Slide 24: 프롬프트 관리 패턴
**Visual**: 프롬프트 관리 플로우. `prompts/rag_answer.py` 파일 → `RAGPrompt` 클래스 → `to_messages()` → LLM API. 우측에 "버전 관리" 태그 (v1.0.0). Git 아이콘 포함.
**Key Points**:
- 프롬프트 = 별도 모듈
- 버전 명시
- 테스트 가능
**Speaker Notes**:
Before:
```python
def answer(question, context):
    prompt = f"컨텍스트: {context}\n질문: {question}\n답변:"  # 하드코딩
    return call_llm(prompt)
```

After:
```python
@dataclass(frozen=True)
class RAGPrompt:
    version: str = "1.0.0"
    system: str = SYSTEM_PROMPT

    def to_messages(self, question: str, context: str) -> list[dict]:
        return [
            {"role": "system", "content": self.system},
            {"role": "user", "content": self.format_user(question, context)},
        ]
```

프롬프트를 코드처럼 버전 관리하면 PR 리뷰, CI 테스트, 롤백이 가능해집니다.

---

## Slide 25: RAG 파이프라인 구조화
**Visual**: RAG 파이프라인 모듈형 다이어그램. `Embedder` → `Retriever` → `ContextBuilder` → `LLM` 순서. 각 컴포넌트 박스 아래에 "ABC (추상 클래스)" 또는 "구현체" 표시. 화살표로 데이터 흐름.
**Key Points**:
- 추상 인터페이스 분리
- 각 단계 교체 가능
- 단위 테스트 용이
**Speaker Notes**:
```python
class Embedder(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...

class Retriever(ABC):
    @abstractmethod
    async def retrieve(self, query_embedding, top_k) -> list[Document]: ...

class RAGPipeline:
    def __init__(self, embedder, retriever, llm, prompt): ...
    async def run(self, question: str) -> tuple[str, list[Document]]:
        embedding = await self._embedder.embed(question)
        docs = await self._retriever.retrieve(embedding)
        context = self._context_builder.build(docs)
        messages = self._prompt.to_messages(question, context)
        return await self._llm.complete(messages), docs
```

OpenAI Embedder를 Cohere Embedder로 교체할 때 `RAGPipeline` 코드를 변경할 필요가 없습니다.

---

## Slide 26: AI 에이전트 클린 아키텍처
**Visual**: 에이전트 ReAct 루프 다이어그램. Task → LLM (Reason) → Tool Call → Tool Execute → Result → LLM → (반복 or 종료). 우측에 `Tool` 추상 클래스와 구현체(`WebSearchTool`, `CodeTool` 등) UML.
**Key Points**:
- `Tool` 추상 클래스
- OpenAI 스키마 자동 생성
- 최대 반복 횟수 제한
**Speaker Notes**:
```python
class Tool(ABC):
    @property
    @abstractmethod
    def name(self) -> str: ...

    @abstractmethod
    async def execute(self, **kwargs) -> ToolResult: ...

    def to_openai_schema(self) -> dict:
        return {"type": "function", "function": {"name": self.name, ...}}

class Agent:
    def __init__(self, llm, tools, max_iterations=10): ...
    async def run(self, task: str) -> str:
        for _ in range(self._max_iterations):
            response = await self._llm.complete_with_tools(messages, tool_schemas)
            if response.finish_reason == "stop":
                return response.content
            # 도구 실행 후 결과를 메시지에 추가
```

새 도구를 추가할 때는 `Tool` 추상 클래스를 구현하는 클래스만 만들면 됩니다.

---

## Slide 27: 섹션 구분 — 도구 추천
**Visual**: "Part 6" 대형 텍스트. Ruff, mypy, pyright, pre-commit 로고 그리드. "개발 도구 생태계" 부제목.
**Key Points**:
- Part 6
- 린터 + 포매터 + 타입 체커
- 자동화 설정
**Speaker Notes**: Python AI 개발에서 코드 품질을 자동으로 유지하는 도구 생태계를 살펴봅니다. Ruff가 Black, Flake8, isort를 대체하는 현대적 올인원 도구로 자리잡았습니다.

---

## Slide 28: Ruff — 올인원 린터 + 포매터
**Visual**: 도구 교체 다이어그램. 기존 도구들(Black, Flake8, isort, pyupgrade → 여러 아이콘) → 화살표 → Ruff 단일 아이콘. 우측에 속도 비교 막대 차트 (Ruff vs. Black, 수십 배 빠름).
**Key Points**:
- Black + Flake8 + isort 대체
- Rust 기반 초고속
- pyproject.toml 통합
**Speaker Notes**:
```toml
[tool.ruff]
target-version = "py312"
line-length = 100

[tool.ruff.lint]
select = [
    "E", "W",   # pycodestyle
    "F",        # pyflakes
    "I",        # isort
    "B",        # flake8-bugbear
    "UP",       # pyupgrade (최신 Python 문법 자동 제안)
    "ANN",      # 타입 힌트 강제
    "ASYNC",    # 비동기 규칙
]
```

`UP` 규칙은 Python 3.12/3.13 신문법을 자동으로 제안합니다.

---

## Slide 29: 타입 체커 — mypy vs. pyright
**Visual**: 두 도구 비교 카드. mypy 카드 (안정성, 스텁 풍부, 느림) vs. pyright 카드 (속도, VSCode 통합, Ruff와 동일 resolver). 하단에 "둘 중 하나 선택" 가이드.
**Key Points**:
- mypy: 성숙, 스텁 풍부
- pyright: 빠름, VSCode 통합
- 둘 다 Ruff와 보완 관계
**Speaker Notes**:
```toml
# pyproject.toml
[tool.mypy]
python_version = "3.12"
strict = true
plugins = ["pydantic.mypy"]

[tool.pyright]
pythonVersion = "3.12"
typeCheckingMode = "strict"
```

추천: AI 백엔드 프로젝트는 pyright (VSCode/Pylance와 통합). 대형 오픈소스는 mypy (스텁 생태계 풍부).

---

## Slide 30: pre-commit 설정
**Visual**: pre-commit 워크플로우 다이어그램. `git commit` → pre-commit hook 트리거 → Ruff lint → Ruff format → mypy → (성공) → commit 완료 / (실패) → 코드 수정 요청. YAML 설정 파일 코드 블록.
**Key Points**:
- 커밋 시 자동 검사
- Ruff + mypy 연동
- 비밀 키 유출 방지
**Speaker Notes**:
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.8.0
    hooks:
      - id: ruff
        args: [--fix, --exit-non-zero-on-fix]
      - id: ruff-format
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v5.0.0
    hooks:
      - id: detect-private-key  # API 키 커밋 방지!
      - id: check-added-large-files
```

`detect-private-key` 훅은 OpenAI API 키 등이 실수로 커밋되는 것을 방지합니다.

---

## Slide 31: 도구 종합 비교표
**Visual**: 컬러 비교 테이블. 열: 도구 이름, 역할, 속도, AI 개발 추천도(★). 각 행에 도구 로고 아이콘. 추천도는 별점 아이콘으로 시각화.

| 도구 | 역할 | 추천도 |
|------|------|--------|
| Ruff | 린터+포매터 | ★★★★★ |
| pyright | 타입 체커 | ★★★★★ |
| pre-commit | 자동화 | ★★★★★ |
| mypy | 타입 체커 | ★★★★☆ |
| structlog | 구조화 로깅 | ★★★★★ |

**Speaker Notes**: AI 개발 프로젝트의 권장 최소 설정: Ruff + pyright + pre-commit. 이 세 가지만으로도 코드 품질의 90%를 자동으로 유지할 수 있습니다. structlog는 토큰 사용량, LLM 호출 로깅에 필수입니다.

---

## Slide 32: 실전 체크리스트
**Visual**: 체크리스트 인포그래픽. 6개 카테고리(3.12 신기능, 3.13 신기능, 백엔드, 프론트엔드, LLM 패턴, 도구)를 아이콘 + 항목 3-4개씩. 체크박스 디자인. 연한 배경에 진한 텍스트.
**Key Points**:
- Python 3.12/3.13 신문법 활용
- 의존성 주입 + 타입 안전 설정
- 프롬프트 분리 + RAG 모듈화
- Ruff + pre-commit 자동화
**Speaker Notes**:
핵심 체크리스트:

Python 3.12/3.13:
- [ ] f-string 새 문법 활용 (PEP 701)
- [ ] 제네릭에 `[T]` 새 문법 사용 (PEP 695)
- [ ] `type X = ...` 타입 별칭 (PEP 695)
- [ ] `@override` 사용 (PEP 698)
- [ ] TypeIs, ReadOnly, @deprecated 활용 (3.13)

AI 백엔드:
- [ ] pydantic-settings로 환경 변수 관리
- [ ] 라우터는 의존성 주입으로 얇게 유지
- [ ] LLM 호출: 재시도 + 폴백 + 타임아웃

LLM 패턴:
- [ ] 프롬프트를 별도 모듈로 분리
- [ ] RAG: Embedder/Retriever/ContextBuilder 인터페이스 분리
- [ ] 에이전트 도구는 Tool 추상 클래스로 표준화

---

## Slide 33: 결론 (Conclusion)
**Visual**: "클린코드 = 미래의 나를 위한 배려" 인용구 대형 텍스트. 파이썬 로고와 AI 뉴런 그래픽 배경. 하단에 핵심 메시지 3가지를 아이콘 카드로.
**Key Points**:
- 신문법으로 의도를 드러내라
- 추상화로 변경에 대비하라
- 도구로 규칙을 자동화하라
**Speaker Notes**:
오늘 다룬 핵심 메시지:

1. Python 3.12/3.13의 새 문법(타입 파라미터, @override, TypeIs)은 코드의 의도를 더 명확하게 드러냅니다.

2. AI 개발에서 클린코드의 핵심은 변경에 대한 대비입니다. LLM 공급자는 바뀌고, 프롬프트는 수시로 수정됩니다. 추상화와 의존성 주입으로 변경 비용을 최소화하세요.

3. 코드 품질 유지는 의지가 아닌 자동화로. Ruff + pre-commit으로 팀 전체가 일관된 품질을 유지하세요.

---

## Slide 34: Q&A
**Visual**: 큰 "Q&A" 텍스트. 미니멀한 디자인. 하단에 참고 자료 QR 코드 또는 짧은 URL. Python Zen 인용구("Readability counts.") 포함.
**Key Points**:
- 질문 환영
- 참고 자료
- 함께 만드는 클린코드
**Speaker Notes**: 발표에서 다루지 못한 세부 내용이나 특정 패턴에 대한 질문을 환영합니다. 참고 자료는 XLSX 파일로 정리되어 있습니다. 함께 클린한 AI 개발 생태계를 만들어갑시다.

---

## 부록: 참고 자료 요약

| 번호 | 자료 | URL |
|------|------|-----|
| 1 | Python 3.12 공식 문서 | https://docs.python.org/3/whatsnew/3.12.html |
| 2 | Python 3.13 공식 문서 | https://docs.python.org/3/whatsnew/3.13.html |
| 3 | FastAPI Best Practices | https://github.com/zhanymkanov/fastapi-best-practices |
| 4 | Ruff 공식 문서 | https://docs.astral.sh/ruff/ |
| 5 | Pydantic Settings | https://docs.pydantic.dev/latest/concepts/pydantic_settings/ |
| 6 | Real Python 3.13 가이드 | https://realpython.com/python313-new-features/ |
