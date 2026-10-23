> 📊 **발표자료(PPTX)**: [open-intelligent-ui-presentation.pptx](./open-intelligent-ui-presentation.pptx)

# OpenIntelligentUI 서베이 — 발표 슬라이드 아웃라인

본 문서는 [블로그](./open-intelligent-ui-blog.md)의 발표용 슬라이드 구성안이다. 슬라이드 본문은 최소한의 문구와 도식 중심이며, 상세는 스피커 노트에 둔다.

## Slide 1: 표지

**Visual**: 네이비 배경, 큰 제목과 부제, 주황 강조선

**Key Points**:
- OpenIntelligentUI 서베이
- 생성형 UI 포맷 비교

**Speaker Notes**: 안녕하십니까. 오늘은 OpenAI가 ChatGPT에 도입한 Intelligent UI를 오픈소스로 재현한 두 프로젝트, 즉 CopilotKit의 OpenIntelligentUI와 Thesys의 open-intelligent-ui를 비교하고, 그 아래에 놓인 생성형 UI 포맷의 트레이드오프를 정리하겠습니다.

## Slide 2: 아젠다

**Visual**: 세 개의 번호 카드 (01 02 03)

**Key Points**:
- 01 배경과 스펙트럼
- 02 두 구현 해부
- 03 비교와 선택

**Speaker Notes**: 발표는 세 부분으로 구성됩니다. 먼저 배경과 스펙트럼, 다음으로 두 구현의 내부 구조, 마지막으로 비교와 한계, 선택 기준입니다.

## Slide 3: 섹션 01: 배경과 스펙트럼

**Visual**: 연한 파란 배경, 큰 번호

**Key Points**:
- 배경과 스펙트럼
- 원본 · 이름 충돌 · 프로토콜 스택

**Speaker Notes**: 첫 번째 섹션입니다. 왜 오픈 재현이 나왔는지와 생성형 UI의 지도를 먼저 그리겠습니다.

## Slide 4: 원본: ChatGPT Intelligent UI

**Visual**: 3단계 흐름(라이브러리 → 컴파일러 → 점진 렌더링)과 아래에 폐쇄형 경고 띠, 화살표로 오픈 재현 등장

**Key Points**:
- 네이티브 스트리밍 컴포넌트
- 생성 중 UI 처리 컴파일러
- 폐쇄형 · API 미확인

**Speaker Notes**: OpenAI는 2026년 10월 7일 GPT-6와 함께 Intelligent UI를 공개했습니다. 구성은 네이티브 스트리밍 컴포넌트 라이브러리와, 모델이 생성하는 동안 UI를 처리하는 컴파일러입니다. 다만 폐쇄형이고 외부에서 쓸 API가 확인되지 않아, 오픈 재현이 곧바로 등장했습니다. OpenAI 원문은 직접 열람하지 못해 검색 결과와 2차 보도를 근거로 했다는 점을 밝혀 둡니다.

## Slide 5: 이름은 같고 설계는 다른 두 프로젝트

**Visual**: 좌우 두 카드: CK 구현(주황) vs TS 구현(초록), 산출물/격리/스택/라우터/라이선스 비교

**Key Points**:
- CK: HTML·CSS·JS + iframe + Jev
- TS: OpenUI Lang + 선언형
- 둘 다 MIT

**Speaker Notes**: 같은 이름을 쓰지만 서로 다른 두 저장소입니다. CopilotKit 쪽은 모델이 HTML과 CSS, JavaScript를 직접 스트리밍하고 격리 iframe에서 실행합니다. Thesys 쪽은 OpenUI Lang이라는 DSL을 스트리밍하고 컴포넌트 라이브러리로 렌더링합니다. 이후 비교에서는 각각 CK 구현, TS 구현이라 부르겠습니다.

## Slide 6: 생성형 UI 스펙트럼과 프로토콜 스택

**Visual**: 상단: Controlled→Declarative→MCP Apps→Open 4단 화살표. 하단: 명세 층 위, 전송 층(AG-UI, MCP) 아래

**Key Points**:
- 통제 ↔ 표현력
- AG-UI는 전송 프로토콜
- A2UI · MCP Apps는 UI 기술

**Speaker Notes**: CopilotKit의 분류에 따르면 생성형 UI는 에이전트가 쥐는 통제권의 스펙트럼입니다. 왼쪽 Controlled에서 오른쪽 Open으로 갈수록 표현력은 커지고 예측 가능성은 낮아집니다. 아래 층은 전송 프로토콜입니다. AG-UI는 UI 명세가 아니라 이벤트 전송 프로토콜이며, A2UI와 MCP Apps 같은 명세가 그 위나 옆에 놓입니다. OpenUI Lang과 json-render를 Declarative에 놓은 것은 본 연구의 분류입니다.

## Slide 7: 섹션 02: 두 구현 해부

**Visual**: 연한 파란 배경, 큰 번호

**Key Points**:
- 두 구현 해부
- CopilotKit · Jev 라우터 · OpenUI Lang

**Speaker Notes**: 두 번째 섹션입니다. 먼저 CopilotKit 구현의 구조와 요청 흐름, 그리고 Jev의 역할을 보겠습니다. 이어서 Thesys 구현과 OpenUI Lang을 살펴봅니다.

## Slide 8: 구현 A: CopilotKit 아키텍처

**Visual**: 좌: 브라우저 박스(채팅/활동 렌더러/A2UI 표), 중: /api/copilotkit, 우: FastAPI Deep Agent와 Jev·chat-latest, 하단 MCP

**Key Points**:
- Next.js ↔ FastAPI (AG-UI 계열)
- Deep Agent + Jev + chat-latest
- 체크포인트: 프로세스 메모리

**Speaker Notes**: CK 구현은 Turborepo 모노레포입니다. 프런트엔드는 Next.js이고, /api/copilotkit 런타임이 LangGraphHttpAgent로 FastAPI의 Deep Agent에 연결됩니다. 에이전트는 답변 모델 chat-latest와 라우터 Jev를 호출합니다. 선택적 MCP 서버는 assemble_document로 HTML을 텍스트로 반환할 뿐이고, 렌더링은 호스트의 몫입니다.

## Slide 9: 요청 한 번의 흐름

**Visual**: 6개 단계 카드(2행×3열), 화살표 연결: Jev 분류 → 렌더러 도출 → 모델 → 툴 스트림 → 렌더링 → 후속 질문

**Key Points**:
- Jev가 모델보다 먼저
- 툴 스트림 → activity 이벤트
- 후속은 새 턴 (패치 API 없음)

**Speaker Notes**: 요청 한 번의 흐름입니다. 사용자가 질문하면 Jev가 최근 메시지 최대 네 개를 보고 시각화 유형을 먼저 고릅니다. 그 선택에서 렌더러가 도출되고, 답변 모델에는 해당 렌더링 계약만 전달됩니다. 모델은 generateSandboxedUi를 스트리밍하고, 미들웨어가 이를 activity 이벤트로 바꿔 프런트에 보냅니다. 사용자가 버튼을 누르면 sendPrompt로 새로운 턴이 시작됩니다.

## Slide 10: 스트리밍 순서가 곧 UX다

**Visual**: 6개 상자를 화살표로 연결: initialHeight → placeholderMessages → css → html → jsFunctions → jsExpressions. css와 jsExpressions 강조

**Key Points**:
- CSS 먼저
- 표현식 마지막
- html은 morph 프리뷰

**Speaker Notes**: generateSandboxedUi의 인자 순서는 곧 사용자 경험 설계입니다. 높이와 플레이스홀더가 먼저 오고, CSS가 HTML보다 앞서야 스타일 없는 화면이 보이지 않습니다. 표현식은 마지막에 도착해 동작이 하나씩 붙는 모습을 사용자가 지켜보게 됩니다. html이 스트리밍되는 동안에는 Idiomorph로 프리뷰 iframe을 깜빡임 없이 갱신합니다.

## Slide 11: Jev의 역할: 포맷을 먼저 고르는 라우터

**Visual**: 좌: 메시지 → Jev → 우: text/table/차트·다이어그램·계산기·지도 → 각 렌더러. 하단 경고 띠

**Key Points**:
- 턴마다 타입 있는 선택 1개
- 선택에서 렌더러 도출
- 실패 시 턴 실패

**Speaker Notes**: Jev는 TypeSafe의 System One 모델입니다. 새 사용자 메시지마다 타입이 있는 시각화 선택 하나를 만듭니다. 선택에서 렌더러가 도출되므로 모순된 조합이 생기지 않습니다. 현재 선언형 경로는 기본 표뿐이고 나머지 시각화는 샌드박스 경로입니다. 인증 실패나 타임아웃은 턴 실패로 드러나며 조용한 폴백은 없습니다. Jev와 결정 모델 자체는 자매 글에서 자세히 다룹니다.

## Slide 12: 구현 B: Thesys 아키텍처

**Visual**: 좌: 브라우저(렌더러/상태), 중: /api/chat, 우: 3개 모델 경로(Gateway=검증, 직접·Ollama=수정 없음)

**Key Points**:
- /api/chat → 3경로
- Gateway만 자동 수정
- 스레드는 localStorage

**Speaker Notes**: TS 구현은 Next.js 단일 앱입니다. /api/chat이 컴포넌트 라이브러리에서 시스템 프롬프트를 만들어 세 가지 경로 중 하나로 보냅니다. OpenUI Gateway는 OpenUI Lang을 검증하고 자동 수정합니다. 직접 OpenAI 호환 엔드포인트나 Ollama를 쓰면 수정 단계가 없어 출력이 쓴 그대로 렌더링됩니다. 스레드는 브라우저 localStorage에 저장됩니다.

## Slide 13: OpenUI Lang: 생성은 한 번, 실행은 런타임

**Visual**: 좌: OpenUI Lang 코드 4줄과 생성/실행 두 칸. 우: 400토큰 vs 60토큰 막대와 벤더 수치 경고

**Key Points**:
- 모델은 배선만 1회 생성
- 클릭·필터는 모델 호출 없음
- 증분 편집 ≈ 60토큰 (대략치)
- 52% 절감은 제작사 측정

**Speaker Notes**: OpenUI Lang의 핵심은 생성과 실행의 분리입니다. 모델은 배선을 한 번 생성하고, 런타임이 Query와 Mutation, 반응형 변수를 실행합니다. 필터와 클릭은 모델 호출 없이 처리됩니다. 후속 요청에서는 바뀐 문장만 출력해 파서가 병합하며, 문서의 대략적 수치로 전체 약 400토큰 대 패치 약 60토큰입니다. 토큰 절감 비율은 제작사 자체 측정이므로 재측정을 권합니다.

## Slide 14: 섹션 03: 비교와 선택

**Visual**: 연한 파란 배경, 큰 번호

**Key Points**:
- 비교와 선택
- 포맷 · 한계 · 선택 기준

**Speaker Notes**: 마지막 섹션입니다. 두 구현을 비교하고, 포맷 간 트레이드오프와 한계, 선택 기준을 정리하겠습니다.

## Slide 15: 두 구현 비교

**Visual**: 3열 표: 축 / CK 구현 / TS 구현 (포맷, 검증, 모델, 라우터, 상호작용, 상태, 샌드박싱, 키)

**Key Points**:
- CK: 가두기(격리)
- TS: 어휘 한정
- 상태는 둘 다 시연 수준

**Speaker Notes**: 두 구현을 여덟 축으로 비교했습니다. CK 구현은 모델에게 화면을 통째로 맡기고 가두는 방식이고, TS 구현은 모델에게 화면을 기술하게 하고 런타임이 실행하는 방식입니다. 그래서 보안의 중심이 전자는 격리, 후자는 어휘 한정입니다. 상태 측면에서는 CK의 체크포인트가 프로세스 메모리이고 TS는 브라우저 localStorage라는 점이 모두 운영상의 제약입니다.

## Slide 16: 포맷 트레이드오프

**Visual**: 5열 표: 항목 / OpenUI Lang / A2UI / json-render / 원시 HTML. 하단에 벤더 수치 경고

**Key Points**:
- 선언형 3종 = 어휘 한정
- 원시 HTML = 격리 필수
- 토큰 수치는 제작사 측정

**Speaker Notes**: 네 가지 포맷을 비교한 표입니다. 선언형 세 가지는 카탈로그에 있는 것만 말할 수 있다는 점에서 같고, 원시 HTML은 무엇이든 말할 수 있어 격리가 필수입니다. 토큰 수치는 OpenUI 제작사의 자체 측정이며 경쟁 구현을 평가하는 비교표와 같은 문서에 있어 편향 가능성이 있습니다. 방향은 납득되지만 배율은 직접 재측정하시기 바랍니다.

## Slide 17: 한계와 리스크

**Visual**: 6개 카드(3×2): 환각 · 비용 · 탈출 표면 · 상태 · 라우팅 의존 · 검증 공백

**Key Points**:
- 그럴듯한 환각
- sendPrompt = 주입 통로(분석)
- 벤치마크 미공개

**Speaker Notes**: 한계는 여섯 가지로 정리됩니다. 첫째 그럴듯한 환각, 둘째 비용, 셋째 샌드박스 탈출 표면, 넷째 상태, 다섯째 라우팅과 가용성, 여섯째 검증 공백입니다. 특히 sendPrompt는 생성된 코드가 에이전트에게 말을 거는 통로이므로 프롬프트 인젝션 관점의 검토가 필요하다고 판단합니다. 이는 본 연구의 분석이며 문서가 직접 위험으로 규정한 것은 아닙니다.

## Slide 18: 무엇을 고를 것인가

**Visual**: 상단 '무엇을 만드는가' 에서 4갈래 분기: Controlled / OpenUI Lang / A2UI / Open+격리, 하단에 json-render 주석

**Key Points**:
- 정형 + 모델 없는 상호작용 → OpenUI Lang
- 멀티 클라이언트 → A2UI
- 자유 형식 → Open + 격리
- 구간을 섞어라

**Speaker Notes**: 선택 기준입니다. 고정된 브랜드 화면은 Controlled로, 정형 UI가 많고 모델 없이 계산과 재조회가 필요하면 OpenUI Lang, 여러 클라이언트가 필요하면 A2UI, React 중심이면 json-render가 후보입니다. 3D나 게임 같은 자유 형식은 강한 격리를 전제로 한 샌드박스 HTML입니다. 가장 중요한 권고는 한 포맷으로 통일하지 말고 구간을 섞으라는 것입니다.

## Slide 19: 결론 / Q&A

**Visual**: 3개 요약 카드와 하단 Q&A 버튼

**Key Points**:
- 스펙트럼의 양 끝
- 포맷 = 신뢰 경계
- 시연 수준 레퍼런스

**Speaker Notes**: 정리하겠습니다. 첫째, 두 구현은 스펙트럼의 반대편에 있습니다. 둘째, 포맷은 곧 신뢰 경계이므로 격리와 어휘 검증 중 무엇이 보안의 중심인지 먼저 정해야 합니다. 셋째, 두 프로젝트 모두 시연 수준의 상태 관리와 공개 벤치마크 부재라는 한계가 있습니다. Jev와 결정 모델은 자매 글에서 다룹니다. 질문 받겠습니다.
