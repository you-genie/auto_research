# 파이썬 챗봇 데모 프레임워크 완전 비교 2025
## PPT 슬라이드 아웃라인

---

## Slide 1: 표지 (Cover)

**Visual**: 어두운 배경에 파이썬 로고와 채팅 버블 아이콘이 떠 있는 그래픽. 각 프레임워크 로고(Streamlit, Gradio, Chainlit, Reflex, Panel, Mesop, Voilà)가 반원형으로 배치.

**Title**: 파이썬 챗봇 프레임워크 대전 2025

**Subtitle**: Streamlit · Gradio · Chainlit · Reflex · Panel · Mesop · Voilà

**Speaker Notes**: 이 발표에서는 파이썬으로 챗봇 데모나 프로토타입을 빠르게 만들 수 있는 7가지 주요 프레임워크를 비교합니다. 각 프레임워크의 특징, 코드 예시, 그리고 어떤 상황에 무엇을 선택해야 하는지를 다룹니다.

---

## Slide 2: 왜 지금 이 주제인가?

**Visual**: LLM 시장 성장 그래프 (2022-2025) + "프로토타입에서 프로덕션까지" 아이콘 흐름도

**Key Points**:
- LLM API 폭발적 성장
- 비개발자도 챗봇 요구
- 프레임워크 춘추전국시대

**Speaker Notes**: GPT-4, Claude, Gemini 등 강력한 LLM API가 등장하면서 "챗봇 하나 빨리 만들어 보여줘"라는 요구가 폭발적으로 증가했습니다. 파이썬 에코시스템에서는 이 수요를 충족하기 위한 다양한 프레임워크가 경쟁하고 있습니다. 선택을 도와드리는 것이 이 발표의 목표입니다.

---

## Slide 3: 오늘의 주인공들

**Visual**: 7개 프레임워크 로고를 격자(3x3)로 배치. 각 로고 아래 GitHub 스타 수를 뱃지로 표시.

**Key Points**:
- Streamlit ~38k ⭐
- Gradio ~35k ⭐
- Reflex ~22k ⭐
- Chainlit ~9k ⭐
- Mesop ~6.5k ⭐
- Panel ~5k ⭐
- Voilà ~5k ⭐

**Speaker Notes**: 커뮤니티 규모 순서로 나열했습니다. GitHub 스타 수는 생태계 크기와 커뮤니티 활성도의 지표입니다. 하지만 스타 수만으로 선택하는 것은 위험합니다. 각 툴의 목적과 강점이 다르기 때문입니다.

---

## Slide 4: 섹션 구분 - 비교 기준 소개

**Visual**: 다음 6개 기준을 아이콘과 함께 원형 다이어그램으로 배치: (1)챗봇 컴포넌트, (2)스트리밍, (3)LLM 연동, (4)배포, (5)인증, (6)학습 난이도

**Key Points**:
- 6가지 기준으로 평가
- 객관적 비교

**Speaker Notes**: 프레임워크를 6가지 핵심 기준으로 평가합니다: ① 채팅 UI 컴포넌트 내장 여부, ② 스트리밍 지원, ③ LLM API 연동 편의성, ④ 배포 옵션, ⑤ 인증 기능, ⑥ 학습 난이도.

---

## Slide 5: 종합 비교 표

**Visual**: 컬러 코딩된 비교 표 (초록=우수, 노랑=보통, 빨강=부족)

| | Streamlit | Gradio | Chainlit | Reflex | Panel | Mesop | Voilà |
|---|---|---|---|---|---|---|---|
| **채팅 컴포넌트** | 내장 | 전용 | 전용 | 직접 구현 | 내장 | 내장 | ipywidgets |
| **스트리밍** | O | O | O | O | O | O | 복잡 |
| **인증 내장** | X | X | O | X | X | X | X |
| **배포 용이성** | 중 | 상 | 중 | 중 | 중 | 중 | 중 |
| **학습 난이도** | 하 | 최하 | 하 | 상 | 중 | 하 | 하 |

**Speaker Notes**: 이 표가 오늘 발표의 핵심입니다. Gradio는 배포와 학습 난이도에서, Chainlit은 인증과 채팅 전문성에서 두드러집니다. 각 항목을 하나씩 살펴보겠습니다.

---

## Slide 6: [1/7] Streamlit 개요

**Visual**: Streamlit 로고 + 챗봇 스크린샷 (어시스턴트 아바타, 채팅 버블, 하단 입력창)

**Key Points**:
- 2018년 출시
- Snowflake 인수 (2022)
- 38k GitHub 스타

**Speaker Notes**: Streamlit은 2018년에 데이터 과학자들이 빠르게 웹앱을 만들 수 있도록 설계됐습니다. 2022년 Snowflake에 인수됐으며, 현재까지 가장 많은 커뮤니티와 생태계를 가진 ML/AI 데모 프레임워크입니다. 2023년 6월 v1.24.0부터 채팅 전용 컴포넌트가 추가됐습니다.

---

## Slide 7: Streamlit - 핵심 채팅 컴포넌트

**Visual**: 코드 스니펫 + 실제 렌더링 결과 스크린샷을 나란히 배치

```python
# 핵심 3가지 API
st.chat_message("user")      # 채팅 버블
st.chat_input("입력...")      # 하단 고정 입력창
st.write_stream(stream)      # 스트리밍 출력
```

**Key Points**:
- `st.chat_message`
- `st.chat_input`
- `st.write_stream`

**Speaker Notes**: Streamlit 챗봇의 핵심은 세 가지 API입니다. `st.chat_message`는 "user" 또는 "assistant" role에 따라 자동으로 아바타와 스타일을 적용합니다. `st.chat_input`은 화면 하단에 항상 고정된 입력창을 생성합니다. `st.write_stream`은 OpenAI 스타일의 스트리밍 응답을 실시간으로 표시합니다.

---

## Slide 8: Streamlit - 배포 & 생태계

**Visual**: Streamlit Community Cloud 로고 + 에코시스템 아이콘 맵 (streamlit-extras, st-chat, pandas, plotly 등)

**Key Points**:
- Community Cloud 무료
- 가장 큰 커뮤니티
- 데이터 시각화 통합

**Speaker Notes**: Streamlit Community Cloud는 GitHub 저장소와 연동하여 무료로 앱을 배포할 수 있습니다. streamlit-extras, st-chat 등 풍부한 서드파티 컴포넌트가 있으며, pandas, plotly, altair 등 데이터 시각화 라이브러리와의 통합이 탁월합니다. 데이터 분석 결과를 챗봇과 결합한 앱에 특히 적합합니다.

---

## Slide 9: [2/7] Gradio 개요

**Visual**: Gradio + Hugging Face 로고 조합 + Spaces 배포 화면 스크린샷

**Key Points**:
- Hugging Face 소속
- ML 데모 표준
- HF Spaces 즉시 배포

**Speaker Notes**: Gradio는 현재 Hugging Face의 일부입니다. 머신러닝 모델을 가장 빠르게 웹 인터페이스로 변환할 수 있는 도구로, 연구자들이 논문과 함께 모델 데모를 공유할 때 사실상 표준이 됐습니다. Hugging Face Spaces와의 통합으로 원클릭 배포가 가능합니다.

---

## Slide 10: Gradio - ChatInterface의 힘

**Visual**: 왼쪽에 3줄 코드, 오른쪽에 완성된 채팅 UI 스크린샷

```python
# 단 이것만으로 완전한 챗봇!
gr.ChatInterface(
    fn=my_response_fn,
    title="My Chatbot",
).launch()
```

**Key Points**:
- 3줄로 완성
- 자동 API 엔드포인트
- 멀티모달 지원

**Speaker Notes**: Gradio의 가장 강력한 기능은 `gr.ChatInterface`입니다. 응답 함수 하나만 정의하면 완전한 채팅 UI가 완성됩니다. 더 나아가, 배포 시 자동으로 REST API 엔드포인트가 생성되어 다른 서비스에서 API로 호출할 수 있습니다. `multimodal=True` 옵션 하나로 이미지/파일 업로드도 지원합니다.

---

## Slide 11: Gradio - 고급 기능

**Visual**: Chain-of-Thought 시각화 스크린샷 + Tool Calling 아코디언 UI 스크린샷

**Key Points**:
- CoT 시각화 내장
- Tool Usage 표시
- 인용구(Citations) 표시

**Speaker Notes**: Gradio의 숨겨진 강점은 LLM 에이전트 UI 지원입니다. Chain-of-Thought 추론 과정을 접이식 아코디언으로 표시하거나, Tool Calling 과정을 시각화하거나, RAG 챗봇에서 인용 출처를 표시하는 기능이 내장되어 있습니다. LLM 에이전트 연구 데모에 매우 적합합니다.

---

## Slide 12: [3/7] Chainlit 개요

**Visual**: Chainlit 로고 + ChatGPT와 유사한 UI 스크린샷 + "Purpose-built for LLM" 뱃지

**Key Points**:
- LLM 챗봇 전문
- 인증 내장 (OAuth)
- 관찰 가능성 (Literal AI)

**Speaker Notes**: Chainlit은 다른 프레임워크들과 달리 처음부터 LLM 챗봇만을 위해 설계됐습니다. ChatGPT와 거의 동일한 수준의 UI를 제공하며, OAuth 인증, 대화 추적, 파일 업로드, 사용자 피드백 버튼이 모두 내장되어 있습니다. 중요한 주의사항: 2025년 5월부터 원 개발팀이 물러나고 커뮤니티 유지로 전환됐습니다.

---

## Slide 13: Chainlit - 데코레이터 아키텍처

**Visual**: 데코레이터 → 이벤트 → UI 흐름을 화살표로 표시한 다이어그램

```python
@cl.on_chat_start  # 채팅 시작
async def start(): ...

@cl.on_message    # 메시지 수신
async def main(msg: cl.Message): ...
```

**Key Points**:
- 데코레이터 기반
- 비동기(async) 우선
- 이벤트 드리븐

**Speaker Notes**: Chainlit은 파이썬 데코레이터로 이벤트를 정의하는 방식을 사용합니다. `@cl.on_chat_start`는 새 채팅 세션이 시작될 때, `@cl.on_message`는 사용자 메시지가 도착할 때 실행됩니다. 전체가 비동기 기반으로 설계되어 동시 접속 처리에 유리합니다.

---

## Slide 14: Chainlit - 차별화 기능

**Visual**: 3개 기능을 아이콘과 함께 나열: (1) 자물쇠 아이콘 = 인증, (2) 눈 아이콘 = 관찰 가능성, (3) 슬랙/디스코드 아이콘 = 플랫폼 통합

**Key Points**:
- OAuth / 비밀번호 인증
- Literal AI 모니터링
- Slack, Teams 배포

**Speaker Notes**: Chainlit이 다른 프레임워크와 가장 크게 차별화되는 세 가지 기능입니다. 첫째, OAuth와 비밀번호 기반 인증이 내장되어 있어 사내 도구나 유료 서비스 구축이 가능합니다. 둘째, Literal AI와 연동하여 대화 로그, 성능 모니터링이 가능합니다. 셋째, Slack, Teams, Discord에 직접 배포할 수 있습니다.

---

## Slide 15: [4/7] Reflex 개요

**Visual**: Reflex 로고 + Python → React 변환을 나타내는 화살표 다이어그램. 왼쪽에 파이썬 코드, 오른쪽에 완성된 웹앱 스크린샷.

**Key Points**:
- 구 Pynecone
- 100% 파이썬
- React 기반 컴파일

**Speaker Notes**: Reflex는 구 Pynecone에서 이름을 바꾼 프레임워크입니다. 파이썬 코드를 작성하면 내부적으로 React + FastAPI 코드로 자동 컴파일됩니다. 단순 데모를 넘어 실제 프로덕션급 SPA(Single Page Application)를 파이썬만으로 만들 수 있다는 것이 핵심 차별점입니다.

---

## Slide 16: Reflex - State 기반 아키텍처

**Visual**: State 클래스 → UI 컴포넌트 → 이벤트 핸들러의 삼각형 관계 다이어그램

```python
class ChatState(rx.State):
    messages: list[dict] = []  # 반응형 상태

    async def send_message(self):
        yield  # UI 즉시 업데이트
```

**Key Points**:
- 중앙 State 클래스
- 반응형 렌더링
- `yield`로 스트리밍

**Speaker Notes**: Reflex의 핵심은 `rx.State` 클래스입니다. 모든 UI 상태를 이 클래스에서 관리하며, 상태가 변경되면 UI가 자동으로 업데이트됩니다. 비동기 이벤트 핸들러에서 `yield`를 사용하면 응답을 점진적으로 스트리밍할 수 있습니다. 학습 곡선이 있지만, 습득 후에는 가장 강력한 UI를 만들 수 있습니다.

---

## Slide 17: Reflex - 적합한 사용 사례

**Visual**: 두 갈래 화살표: "단순 데모 → 다른 툴 권장" vs "프로덕션 앱 → Reflex 권장"

**Key Points**:
- 프로덕션 수준 앱
- 복잡한 라우팅
- 커스텀 UI 필요 시

**Speaker Notes**: Reflex는 모든 프레임워크 중 가장 강력하지만, 그만큼 복잡합니다. 간단한 데모나 프로토타입에는 오버엔지니어링입니다. 반면 다중 페이지, 복잡한 상태 관리, 커스텀 디자인이 필요한 실제 제품을 파이썬으로 만들고 싶다면 최적의 선택입니다.

---

## Slide 18: [5/7] Panel 개요

**Visual**: Panel + HoloViz 로고 + 챗봇과 데이터 시각화가 결합된 대시보드 스크린샷

**Key Points**:
- HoloViz 생태계
- Jupyter 친화적
- 대시보드 + 챗봇

**Speaker Notes**: Panel은 HoloViz 생태계의 일부로, Bokeh, Matplotlib, Plotly 등 다양한 시각화 라이브러리와 완벽하게 통합됩니다. Panel 1.3.0부터 `panel.chat` 서브패키지가 추가되어 LLM 챗봇을 직접 지원합니다. Jupyter 노트북에서 바로 실행하고 서버로 배포할 수 있어 데이터 과학 팀에 인기입니다.

---

## Slide 19: Panel - ChatInterface 특징

**Visual**: Panel ChatInterface 스크린샷 + 무한 스크롤 아이콘 + "1000+ 메시지 처리" 뱃지

**Key Points**:
- 무한 스크롤 피드
- 타임스탬프 내장
- 반응 아이콘 지원

**Speaker Notes**: Panel ChatFeed 컴포넌트는 가상 스크롤링을 지원하여 수천 개의 메시지도 성능 저하 없이 렌더링합니다. 각 메시지에는 타임스탬프, 아바타, 반응 아이콘(좋아요 등)이 자동으로 포함됩니다. 긴 대화 히스토리가 필요한 연구용 챗봇이나 고객 서비스 시뮬레이터에 적합합니다.

---

## Slide 20: [6/7] Mesop 개요

**Visual**: Google 로고 + Mesop 로고 + "Python only, no JS/CSS/HTML" 배너

**Key Points**:
- Google 내부 사용
- Angular 기반
- Gemini 친화적

**Speaker Notes**: Mesop은 구글이 내부적으로 AI 데모와 도구 개발에 사용하기 위해 만든 프레임워크입니다. 2023년 12월 오픈소스로 공개됐으며, Angular와 Angular Material을 기반으로 하지만 개발자는 파이썬만 작성합니다. "공식 구글 제품은 아니다"라는 면책 조항이 있지만, 구글 내부 검증을 받은 도구입니다.

---

## Slide 21: Mesop - mel.chat으로 즉시 챗봇

**Visual**: 왼쪽에 10줄 미만의 코드, 오른쪽에 완성된 Gemini 챗봇 UI

```python
@me.page(path="/")
def app():
    mel.chat(
        transform=chat_fn,
        title="Gemini Bot",
    )
```

**Key Points**:
- `mel.chat` 4줄
- Gemini 즉시 연동
- 핫 리로드

**Speaker Notes**: Mesop의 `mesop.labs.chat` 컴포넌트를 사용하면 응답 함수 하나와 `mel.chat()` 호출만으로 완전한 채팅 UI가 완성됩니다. 핫 리로드 기능으로 코드를 저장하면 브라우저가 즉시 새로고침됩니다. Gemini API와의 통합이 특히 자연스럽습니다.

---

## Slide 22: [7/7] Voilà 개요

**Visual**: Jupyter 노트북 아이콘 → 화살표 → 웹앱 아이콘 변환 그래픽. "코드 셀 숨김, 위젯만 표시" 설명.

**Key Points**:
- Jupyter → 웹앱
- 코드 셀 자동 숨김
- ipywidgets 기반

**Speaker Notes**: Voilà는 기존 Jupyter 노트북을 그대로 웹 애플리케이션으로 변환해주는 도구입니다. 코드 셀은 숨기고 출력 결과와 ipywidgets만 표시합니다. 이미 Jupyter 노트북으로 분석 작업을 하고 있다면, 별도의 재개발 없이 그 노트북을 그대로 데모로 배포할 수 있습니다.

---

## Slide 23: Voilà - 챗봇 구현의 한계

**Visual**: 비교 이미지: Chainlit/Gradio의 세련된 채팅 UI vs Voilà의 ipywidgets 기반 단순 UI

**Key Points**:
- ipywidgets 의존
- 스트리밍 복잡
- 리소스 소모 큼

**Speaker Notes**: Voilà로도 채팅 인터페이스를 만들 수 있지만, ipywidgets의 한계로 인해 다른 툴에 비해 UI가 원시적입니다. 또한 각 사용자마다 별도의 Jupyter 커널이 필요하여 서버 리소스 소모가 큽니다. 2024-2025년 트렌드를 보면 챗봇 데모 용도로는 Streamlit/Gradio로 대체되는 추세입니다.

---

## Slide 24: 섹션 구분 - 선택 가이드

**Visual**: "Which one should I use?" 대형 텍스트 + 분기 화살표 그래픽

**Speaker Notes**: 지금까지 7개 프레임워크를 살펴봤습니다. 이제 실제로 어떤 상황에서 무엇을 선택해야 하는지 정리합니다.

---

## Slide 25: 결정 트리 (Decision Tree)

**Visual**: 플로우차트 형식의 결정 트리 다이어그램

```
목표는?
├── 빠른 데모
│   ├── ML 모델 → Gradio
│   └── 일반 챗봇 → Streamlit
├── 프로덕션 배포
│   ├── 인증 필요 → Chainlit
│   └── 커스텀 UI → Reflex
├── 기존 Jupyter 활용
│   ├── 단순 → Voilà
│   └── 복잡 → Panel
└── Google 생태계
    └── Mesop
```

**Key Points**:
- 목적 먼저 결정
- 배포 환경 고려
- 팀 스킬 반영

**Speaker Notes**: 이 결정 트리를 사용하세요. 가장 중요한 질문은 "무엇을 만들고 싶은가"가 아니라 "누가, 어디서, 얼마나 오래 사용할 것인가"입니다. 5분짜리 데모라면 Gradio, 사내 상시 운영 서비스라면 Chainlit이나 Reflex를 고려하세요.

---

## Slide 26: 학습 비용 vs 유연성 매트릭스

**Visual**: 2x2 사분면 그래프. X축: 낮은 학습 비용 → 높은 학습 비용. Y축: 낮은 유연성 → 높은 유연성.

```
높은 유연성
        ^
Reflex  |    Panel
        |         Streamlit
Mesop   |    Gradio    Voilà
        +---------------------→
   낮은 난이도        높은 난이도
```

**Key Points**:
- Gradio: 쉽고 빠름
- Reflex: 어렵지만 강력
- Streamlit: 균형점

**Speaker Notes**: 이 매트릭스는 각 프레임워크의 포지셔닝을 직관적으로 보여줍니다. Gradio는 가장 쉽게 시작할 수 있지만 유연성이 제한적입니다. Reflex는 배우기 어렵지만 가장 유연합니다. 대부분의 챗봇 데모 사용 사례에서는 Streamlit이나 Chainlit이 최적의 균형점을 제공합니다.

---

## Slide 27: 프레임워크별 추천 사용 사례

**Visual**: 6개 카드 레이아웃, 각 카드에 아이콘 + 프레임워크명 + 한 줄 사용 사례

| 프레임워크 | 최적 사용 사례 |
|-----------|-------------|
| Gradio | ML 모델 데모, 논문 재현 |
| Streamlit | 데이터+AI 통합 대시보드 |
| Chainlit | 사내 LLM 챗봇, 프로덕션 |
| Reflex | 커스텀 챗봇 웹서비스 |
| Panel | Jupyter 기반 연구 도구 |
| Mesop | Google/Gemini 생태계 데모 |
| Voilà | 기존 노트북 즉시 배포 |

**Key Points**:
- 목적에 맞는 선택
- 중복 사용 가능
- 팀 친숙도 고려

**Speaker Notes**: 각 프레임워크가 빛나는 고유한 사용 사례가 있습니다. 하나를 완전히 익히고 상황에 따라 다른 것을 추가하는 전략을 권장합니다. 초보자라면 Gradio로 시작해서 Streamlit으로 넘어가는 경로가 가장 자연스럽습니다.

---

## Slide 28: 섹션 구분 - 코드 예시

**Visual**: 코드 아이콘 + "Live Demo" 배너

**Speaker Notes**: 이제 각 프레임워크로 동일한 챗봇을 구현하는 핵심 코드를 비교해보겠습니다. 모든 예시는 OpenAI API를 사용합니다.

---

## Slide 29: 코드 비교 - Gradio vs Streamlit

**Visual**: 좌우 분할 화면. 왼쪽 Gradio 코드, 오른쪽 Streamlit 코드. 라인 수 뱃지 표시 (Gradio: 8줄, Streamlit: ~30줄)

```python
# Gradio (8줄)
def respond(msg, history):
    stream = client.chat.completions.create(
        model="gpt-4o",
        messages=history + [{"role":"user","content":msg}],
        stream=True)
    partial = ""
    for chunk in stream:
        partial += chunk.choices[0].delta.content or ""
        yield partial
gr.ChatInterface(respond).launch()
```

**Key Points**:
- Gradio: 최소 코드
- Streamlit: 더 많은 제어
- 둘 다 스트리밍 O

**Speaker Notes**: 동일한 챗봇 기능을 구현할 때 Gradio는 8줄, Streamlit은 약 30줄이 필요합니다. 코드가 적다고 무조건 좋은 것은 아닙니다. Streamlit의 추가 코드는 더 세밀한 제어와 커스터마이징을 가능하게 합니다.

---

## Slide 30: 코드 비교 - Chainlit

**Visual**: Chainlit 코드 스니펫 + "Production-Ready" 뱃지. 인증, 스트리밍, 세션 관리 코드 하이라이트.

```python
# Chainlit - 프로덕션 수준
@cl.on_chat_start
async def start():
    cl.user_session.set("history", [])

@cl.on_message
async def main(message: cl.Message):
    history = cl.user_session.get("history")
    msg = cl.Message(content="")
    async for chunk in await client.chat.completions.create(..., stream=True):
        await msg.stream_token(chunk.choices[0].delta.content or "")
    await msg.update()
```

**Key Points**:
- 세션 관리 내장
- 비동기 스트리밍
- 데코레이터 패턴

**Speaker Notes**: Chainlit 코드에서 주목할 점은 세션 관리입니다. `cl.user_session`을 통해 각 사용자의 대화 히스토리를 독립적으로 관리합니다. 또한 `msg.stream_token()`으로 토큰 단위 스트리밍을 구현합니다. 비동기 패턴이 기본이어서 동시 접속 처리에 효율적입니다.

---

## Slide 31: 커뮤니티 & 생태계

**Visual**: 막대 그래프: GitHub 스타 수, PyPI 다운로드 수, Stack Overflow 질문 수 비교

**Key Points**:
- Streamlit 압도적 1위
- Gradio 빠른 성장
- Chainlit 틈새 강자

**Speaker Notes**: 커뮤니티 규모에서는 Streamlit이 압도적입니다. GitHub 스타 약 38k, Stack Overflow 질문도 가장 많습니다. Gradio는 Hugging Face 생태계에서 빠르게 성장 중이며, Chainlit은 LLM 특화 커뮤니티에서 영향력이 큽니다. Mesop과 Panel은 상대적으로 작지만 활발한 커뮤니티를 유지하고 있습니다.

---

## Slide 32: 2025년 트렌드 & 전망

**Visual**: 타임라인 그래픽 (2023 → 2024 → 2025 → 미래) + 각 연도별 주요 사건

**Key Points**:
- LLM 에이전트 UI 증가
- 멀티모달 챗봇 표준화
- 프레임워크 통합/재편 예상

**Speaker Notes**: 2025년의 주요 트렌드입니다. 첫째, 단순 Q&A를 넘어 Tool Calling과 Multi-step Reasoning을 시각화하는 에이전트 UI 수요가 증가하고 있습니다. 둘째, 이미지, 오디오, 비디오를 처리하는 멀티모달 챗봇이 표준이 되고 있습니다. 셋째, Chainlit처럼 단일 목적 프레임워크는 더 큰 플랫폼에 통합되거나 재편될 가능성이 있습니다.

---

## Slide 33: 핵심 정리

**Visual**: 6개 아이콘을 사용한 인포그래픽 카드

**Key Points**:
- 최속: Gradio
- 생태계: Streamlit
- 채팅 전문: Chainlit
- 풀스택: Reflex
- 데이터+채팅: Panel
- Jupyter: Voilà

**Speaker Notes**: 오늘의 핵심 메시지입니다. 모든 상황에 최적인 프레임워크는 없습니다. 가장 빠른 데모는 Gradio, 가장 큰 생태계는 Streamlit, 채팅 전문성은 Chainlit, 프로덕션 풀스택은 Reflex, 데이터 과학+채팅 결합은 Panel, 기존 Jupyter 자산 활용은 Voilà를 선택하세요.

---

## Slide 34: Q&A

**Visual**: 대형 "?" 아이콘 + 리소스 QR코드 2개 (GitHub 레포, 이 발표 자료)

**Key Points**:
- 질문 환영
- 코드 샘플 제공
- 추가 리소스 QR

**Speaker Notes**: 질문이 있으신가요? 오늘 발표에서 다룬 모든 코드 예시는 GitHub에서 확인하실 수 있습니다. 각 프레임워크로 동일한 GPT-4o 챗봇을 구현한 데모 코드를 제공합니다. 실제로 실행해보고 직접 비교해보시길 권장합니다.

---

## Slide 35: 참고 자료

**Visual**: 링크 목록을 QR코드와 함께 표시

**Key Points**:
- 공식 문서 링크
- GitHub 예제 코드
- 비교 블로그 포스트

**Speaker Notes**:
1. [Streamlit 채팅 튜토리얼](https://docs.streamlit.io/develop/tutorials/chat-and-llm-apps)
2. [Gradio ChatInterface 가이드](https://www.gradio.app/guides/creating-a-chatbot-fast)
3. [Chainlit GitHub](https://github.com/Chainlit/chainlit)
4. [Reflex 챗앱 튜토리얼](https://reflex.dev/docs/getting-started/chatapp-tutorial/)
5. [Panel 챗봇 예제](https://github.com/holoviz-topics/panel-chat-examples)
6. [Mesop GitHub](https://github.com/mesop-dev/mesop)
7. [Voilà GitHub](https://github.com/voila-dashboards/voila)
8. [Streamlit vs Gradio 2025](https://www.squadbase.dev/en/blog/streamlit-vs-gradio-in-2025-a-framework-comparison-for-ai-apps)
9. [AI 앱 UI 툴 비교 - GetStream](https://getstream.io/blog/ai-chat-ui-tools/)
