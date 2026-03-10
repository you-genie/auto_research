# Chainlit 데모 코드 모음

이 폴더에는 Chainlit 프레임워크를 활용한 세 가지 수준의 챗봇 데모가 포함되어 있습니다.

---

## 데모 구조

```
demo/
├── README.md          ← 이 파일
├── basic/             ← 기본 챗봇 (Hello World 수준)
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
├── intermediate/      ← 중급 챗봇 (파일 업로드, 세션 관리, 인증)
│   ├── app.py
│   ├── requirements.txt
│   └── .env.example
└── advanced/          ← 고급 챗봇 (LangGraph 멀티 에이전트)
    ├── app.py         ← Chainlit UI 메인
    ├── agent_graph.py ← LangGraph 그래프 정의
    ├── tools.py       ← 에이전트 도구 정의
    ├── requirements.txt
    └── .env.example
```

---

## 데모 1: 기본 챗봇 (basic/)

**무엇을 배울 수 있나요?**
- `@cl.on_chat_start`: 세션 초기화
- `@cl.on_message`: 메시지 처리
- `cl.user_session`: 사용자별 데이터 격리
- 응답 스트리밍 (`stream_token`)

**실행 방법:**
```bash
cd basic
pip install -r requirements.txt
cp .env.example .env
# .env에 OPENAI_API_KEY 입력
chainlit run app.py -w
```

**필요한 API 키:**
- `OPENAI_API_KEY` (필수)

---

## 데모 2: 중급 챗봇 (intermediate/)

**무엇을 배울 수 있나요?**
- 패스워드 기반 인증 (`@cl.password_auth_callback`)
- 채팅 프로필 선택 (`@cl.set_chat_profiles`)
- 파일 업로드 처리 (이미지 비전 분석, PDF 텍스트 추출)
- 채팅 설정 UI (`cl.ChatSettings`)
- 처리 단계 시각화 (`cl.Step`)

**실행 방법:**
```bash
cd intermediate
pip install -r requirements.txt
cp .env.example .env
# .env에 OPENAI_API_KEY 입력 (gpt-4o 권장)
chainlit run app.py -w
```

**로그인 정보 (데모용):**
- 관리자: admin / changeme123
- 일반 사용자: 원하는 아이디 / 4자 이상 비밀번호

**필요한 API 키:**
- `OPENAI_API_KEY` (필수, gpt-4o 권장)

---

## 데모 3: 고급 챗봇 - LangGraph 멀티 에이전트 (advanced/)

**무엇을 배울 수 있나요?**
- LangGraph `StateGraph`로 멀티 에이전트 오케스트레이션
- ReAct 패턴 에이전트 구현
- `MemorySaver`를 통한 대화 기록 영속성
- 조건부 엣지 (`add_conditional_edges`)
- `astream_events`를 통한 에이전트 실행 스트리밍
- Chainlit Steps로 에이전트 과정 시각화
- 다양한 도구 구현 (웹 검색, 날씨, 계산, 코드 실행, 단위 변환)

**그래프 구조:**
```
START
  ↓
[라우터] ─── 질문 유형 분류
  ↓
[검색 에이전트]  → 웹 검색, 날씨 조회
[분석 에이전트]  → 계산, 단위 변환
[코드 에이전트]  → Python 코드 실행
[직접 응답]      → 일반 대화
  ↓
[응답 합성기] ── 결과 통합
  ↓
END
```

**실행 방법:**
```bash
cd advanced
pip install -r requirements.txt
cp .env.example .env
# .env에 API 키 입력:
# - OPENAI_API_KEY (필수)
# - TAVILY_API_KEY (선택 - 웹 검색용)
# - OPENWEATHER_API_KEY (선택 - 날씨용)
chainlit run app.py -w
```

**테스트 쿼리 예시:**
```
# 검색 에이전트 테스트
서울 날씨 알려줘

# 분석 에이전트 테스트
100마일을 킬로미터로 변환해줘
sin(30도) 값은 얼마야?

# 코드 에이전트 테스트
피보나치 수열 10번째까지 출력하는 Python 코드 작성해줘

# 직접 응답 테스트
LangGraph가 뭔지 설명해줘

# 복합 쿼리 (여러 에이전트 협력)
오늘 서울 날씨 확인하고, 현재 온도를 화씨로 변환해줘
```

**필요한 API 키:**
- `OPENAI_API_KEY` (필수) - https://platform.openai.com/api-keys
- `TAVILY_API_KEY` (선택) - https://tavily.com/ (무료 발급)
- `OPENWEATHER_API_KEY` (선택) - https://openweathermap.org/api (무료 발급)

> API 키가 없는 도구는 시뮬레이션 모드로 동작합니다.

---

## 공통 실행 명령어

```bash
# 개발 모드 (파일 변경 시 자동 재시작)
chainlit run app.py -w

# 특정 포트 지정
chainlit run app.py -w --port 8080

# 프로덕션 모드 (브라우저 자동 열기 없음)
chainlit run app.py -h --host 0.0.0.0 --port 8000
```

---

## 트러블슈팅

**Q: `ModuleNotFoundError` 발생**
- `pip install -r requirements.txt` 실행 확인

**Q: OpenAI API 오류**
- `.env` 파일에 올바른 `OPENAI_API_KEY` 입력 확인
- API 크레딧 잔액 확인

**Q: 포트 충돌**
- `--port 8080` 옵션으로 다른 포트 사용

**Q: LangGraph 버전 오류**
- `pip install --upgrade langgraph langchain langchain-openai` 실행
