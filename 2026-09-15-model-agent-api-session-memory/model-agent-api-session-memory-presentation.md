# 누가 대화를 기억하는가 — 발표 아웃라인

> 산출물: [model-agent-api-session-memory-presentation.pptx](./model-agent-api-session-memory-presentation.pptx)

---

## Slide 1: 누가 대화를 기억하는가

**Visual**: 좌우 대비 히어로. 왼쪽에 "무상태" 아이콘(빈 상자, 화살표가 통과), 오른쪽에 "상태 저장" 아이콘(서랍장에 대화 기록이 쌓임). 가운데 물음표.

**Key Points**:
- 상용 모델 API vs 에이전트 API
- 세션·메모리 소유권 전면 비교
- 2026년 9월 기준

**Speaker Notes**: OpenAI Chat Completions는 세션을 서버에서 관리하지 않지만 Responses API는 한다. Claude Messages API는 안 하지만 Managed Agents는 한다. 같은 회사 안에서도 API마다 상태 소유권이 다르다는 점에서 출발한다.

---

## Slide 2: 오늘 답할 세 가지 질문

**Visual**: 번호가 붙은 3개 카드. 각 카드에 아이콘(① 모델 칩, ② 로봇, ③ 두 개가 맞물린 톱니).

**Key Points**:
- 모델 API는 누가 관리?
- 에이전트 API는 누가 관리?
- 같이 쓰면 기억은 어디에?

**Speaker Notes**: 세 번째가 실무에서 가장 자주 사고가 나는 지점이다. 답을 먼저 말하면 "당신이 고르는 것"이고, 고를 수 있다는 사실 자체를 모르는 경우가 많다.

---

## Slide 3: 결론 먼저 — 3줄

**Visual**: 큰 숫자 1/2/3, 각 줄에 한 문장씩. 배경은 옅은 그라데이션.

**Key Points**:
- 모델은 언제나 무상태
- 모든 벤더가 같은 사다리
- 세션과 메모리는 직교

**Speaker Notes**: "서버 세션"은 모델이 기억한다는 뜻이 아니라 누가 로그를 보관하느냐의 문제다. 그래서 토큰은 매 턴 다시 낸다. 그리고 세션(단기)과 메모리(장기)는 별개 제품이라 조합이 자유롭다.

---

## Slide 4: 섹션 — 프레임

**Visual**: 섹션 디바이더. 큰 텍스트 "① 상태 소유권 4단계".

**Key Points**: (없음)

**Speaker Notes**: 벤더별 용어의 홍수를 관통하는 단일 프레임을 먼저 세운다.

---

## Slide 5: 상태 소유권 사다리

**Visual**: 4단 계단 다이어그램. 아래에서 위로 L0 → L1 → L2 → L3. 각 단에 대표 제품 로고/이름. 오른쪽에 "서버가 갖는 양" 화살표가 위로 증가.

**Key Points**:
- L0 완전 무상태
- L1 대화 로그 보관
- L2 실행 상태 보관
- L3 장기 기억 추출

**Speaker Notes**: L0~L2는 "이번 대화"의 축, L3는 "대화들 사이"의 축이라 직교한다. L0 모델 API에 L3 메모리를 붙이는 게 가장 흔한 프로덕션 패턴이다.

---

## Slide 6: 대전제 — 모델은 무상태다

**Visual**: 시퀀스 다이어그램 2단. 위: L0에서 앱이 전체 배열 전송. 아래: L1에서 앱은 새 턴만 보내지만 서버가 저장분을 prepend → 모델에 가는 프롬프트 크기 **동일**. 동일 크기를 빨간 박스로 강조.

**Key Points**:
- 보관 책임만 이동
- 프롬프트 크기 동일
- 토큰 재과금

**Speaker Notes**: OpenAI 문서는 previous_response_id 체인의 모든 이전 입력 토큰이 입력 토큰으로 과금된다고 명시한다. 서버 세션은 네트워크 페이로드를 줄일 뿐 컨텍스트 비용을 줄이지 않는다.

---

## Slide 7: 섹션 — 모델 API

**Visual**: 섹션 디바이더. "② 모델 API 계층".

**Key Points**: (없음)

**Speaker Notes**: 벤더별로 어디까지 올라갔는지 본다.

---

## Slide 8: OpenAI — 한 회사 안에 L0·L1 공존

**Visual**: 3개 레인. Chat Completions(L0) / Responses(L1) / Conversations(L1+). 각 레인에 보존 기간 뱃지.

**Key Points**:
- Chat Completions: 무상태
- Responses: `store` 기본 true, 30일
- Conversations: 30일 TTL 미적용

**Speaker Notes**: Responses는 previous_response_id로 체이닝, Conversations는 자체 식별자를 가진 장기 객체다. 데이터를 남기기 싫으면 store:false 또는 Chat Completions.

---

## Slide 9: Anthropic — L0 고정, 대신 서버가 "편집"한다

**Visual**: 클라이언트 쪽에 메시지 배열 아이콘(소유권 표시), 서버 쪽에 가위 아이콘. 가위가 배열 앞부분을 잘라내는 애니메이션 느낌.

**Key Points**:
- Messages API는 상태 저장 없음
- Context editing: 오래된 tool result 제거
- Compaction: 요약 블록 이전 드롭

**Speaker Notes**: 핵심은 "클라이언트가 관리하는 목록 + 서버가 수행하는 컨텍스트 최적화". 저장 주체는 클라이언트에 남기면서 어려운 부분만 서버로 옮긴 절충안이다. ZDR을 유지하면서 장기 실행 에이전트를 돌릴 수 있다.

---

## Slide 10: Gemini — 상태 저장을 기본값으로 삼은 첫 API

**Visual**: generateContent → Interactions API 화살표. Interactions 쪽에 `store=true` 기본값 뱃지, 보존 55일/1일 뱃지.

**Key Points**:
- Interactions API GA (2026-06)
- `previous_interaction_id`
- 함정: tools 승계 안 됨

**Speaker Notes**: tools, system_instruction, generation_config는 interaction 스코프라 매 턴 다시 명시해야 한다. store:false를 주면 무상태가 되지만 체이닝과 백그라운드 실행을 못 쓴다.

---

## Slide 11: Azure — 같은 API 모양, 다른 데이터 경계

**Visual**: 동일한 API 아이콘 두 개, 아래에 서로 다른 색의 "데이터 경계" 원. 왼쪽 OpenAI 클라우드, 오른쪽 고객 Azure 테넌트(자물쇠).

**Key Points**:
- Responses API 동일 표면
- 저장은 고객 테넌트
- 같은 지리 + AES-256

**Speaker Notes**: 규제 산업에서 Azure를 고르는 이유가 여기 압축돼 있다. 실행은 맡기고 저장은 소유하는 구조다.

---

## Slide 12: AWS Bedrock — 상태를 별도 API로 떼어냈다

**Visual**: Converse(L0) 박스 옆에 점선으로 분리된 Session Management API 박스(CreateSession → CreateInvocation → PutInvocationStep 파이프라인).

**Key Points**:
- Converse: 완전 무상태
- Session API는 별도
- 명시적 put/get

**Speaker Notes**: AWS의 L1은 자동 주입형이 아니라 개발자가 명시적으로 쓰고 읽는 체크포인트 스토어다. LangGraph·LlamaIndex의 상태 저장소 용도로 설계됐다. 같은 AWS 안에서도 InvokeAgent는 자동 주입형이라 경로마다 다르다.

---

## Slide 13: 모델 API 종합 비교표

**Visual**: 전체 화면 비교표. 단계(L0/L1) 컬럼을 색으로 구분.

**Key Points**:
- 11개 API 한눈에
- 저장 주체 · 보존 · 무상태 선택 가능 여부

**Speaker Notes**: 표를 훑을 때 "무상태 선택 가능" 컬럼을 주목하게 한다. 거버넌스 제약이 있는 조직은 이 컬럼이 X인 제품을 바로 제외할 수 있다.

---

## Slide 14: 섹션 — 에이전트 API

**Visual**: 섹션 디바이더. "③ 에이전트 API 계층".

**Key Points**: (없음)

**Speaker Notes**: 모델 API는 추론 1회를 팔고, 에이전트 API는 루프 전체를 판다.

---

## Slide 15: Claude Managed Agents — L2+L3를 한 제품으로

**Visual**: 4개 개념 블록(Agent / Environment / Session / Events)이 맞물린 도형. 아래에 Anthropic 클라우드 샌드박스 아이콘.

**Key Points**:
- Agent · Environment · Session · Events
- 이벤트 이력 서버 영속
- 예산 상한 · 볼트 · 버전 고정

**Speaker Notes**: POST /v1/sessions로 세션 생성, /events로 이벤트 전송, SSE 스트리밍. budget.max_list_cost는 부동소수점 반올림을 피하려고 센트 단위 문자열로 받는다.

---

## Slide 16: memory_stores — 파일시스템으로서의 장기 기억

**Visual**: 샌드박스 내부에 `/mnt/memory/<slug>/` 디렉터리 트리. 오른쪽에 버전 스택(memver_) 아이콘.

**Key Points**:
- 세션당 최대 8개 store
- 메모리당 100 kB · store당 1만 개
- 불변 버전 + redact

**Speaker Notes**: 에이전트가 평소 쓰던 파일 툴로 읽고 쓴다. 모든 변경이 불변 버전을 만들어 감사 추적이 남고, 규제 대응용 redact 엔드포인트가 따로 있다. 동시 쓰기는 content_sha256 precondition으로 막는다.

---

## Slide 17: 경고 — 메모리는 인젝션의 지속성을 만든다

**Visual**: 경고 색 슬라이드. 세션1(오염된 입력) → memory store(악성 기록) → 세션2·3·4(신뢰된 기억으로 읽음) 흐름도.

**Key Points**:
- 기본값이 `read_write`
- 인젝션이 세션 경계를 넘는다
- 참조용은 `read_only`

**Speaker Notes**: Managed Agents만의 문제가 아니라 L3 장기 메모리 전반의 구조적 위험이다. 메모리는 세션 경계를 넘는 쓰기 채널이기 때문이다.

---

## Slide 18: 같은 회사, 정반대의 소유권 — Claude Agent SDK

**Visual**: Managed Agents(클라우드 아이콘)와 Agent SDK(노트북 아이콘)를 좌우 대비. 아래 각각 "Anthropic 인프라" / "~/.claude/projects/*.jsonl".

**Key Points**:
- 로컬 JSONL, append-only
- resume / fork
- 인프라 소유 vs 무인프라

**Speaker Notes**: Anthropic은 같은 에이전트 개념을 두 가지 상태 소유권으로 동시에 판다. 이력을 내 손에 두고 싶으면 SDK, 인프라를 아예 안 만들고 싶으면 Managed Agents.

---

## Slide 19: OpenAI Agents SDK — 세션 백엔드를 고른다

**Visual**: 중앙에 에이전트 코드 박스, 아래로 6갈래 화살표 → Memory / SQLite / OpenAI Conversations / Redis / SQLAlchemy / Mongo·Dapr.

**Key Points**:
- 한 줄로 소유권 이동
- 로컬 ↔ 자체 DB ↔ OpenAI 서버
- Compaction 세션도 제공

**Speaker Notes**: 상태 소유권이 런타임 설정으로 내려온 첫 사례에 가깝다. 참고로 Agent Builder는 2026년 11월 30일 종료 예정이고, OpenAI는 ChatKit SDK + Agents SDK 기반 자체 서버 구현을 권장한다.

---

## Slide 20: AWS AgentCore — 런타임(L2)과 메모리(L3)를 분리 판매

**Visual**: 좌: microVM 격리 그림(세션별 상자). 우: Memory 계층도(Event → Strategy → Namespace → Memory record).

**Key Points**:
- 세션당 전용 microVM, 최대 8시간
- 15분 유휴 시 회수
- 모델 무관: Bedrock·Claude·Gemini·OpenAI

**Speaker Notes**: 세션 헤더로 같은 microVM에 라우팅하므로 클라이언트가 세션 ID를 이후 요청에 계속 넣어야 어피니티가 유지된다. 모델 무관이라는 점이 크로스오버의 핵심 재료다.

---

## Slide 21: AgentCore Memory — 2026년에 무엇이 바뀌었나

**Visual**: 타임라인. 2026-03 스트리밍 알림 / 2026-05~06 strict metadata / 2026-09 IngestData.

**Key Points**:
- 폴링 제거
- LLM 추론 없는 메타데이터
- 대화 아닌 문서도 직접 주입

**Speaker Notes**: IngestData는 단기 이벤트를 만들지 않고 바로 장기 레코드를 만든다. 대화가 아닌 문서·기록물을 메모리에 넣는 경로가 열린 셈이다.

---

## Slide 22: Azure Foundry — thread/run + BYO 스토리지

**Visual**: thread 아이콘 안에 메시지 스택, 아래 화살표가 고객 Cosmos DB 아이콘으로 내려감. 컨테이너 3개 이름 표기.

**Key Points**:
- 스레드당 최대 10만 메시지
- 고객 Cosmos DB에 저장
- non-OpenAI 모델 지원

**Speaker Notes**: enterprise_memory DB 안에 thread-message-store, system-thread-message-store, agent-entity-store가 생긴다. 최소 3,000 RU/s 필요. L2 상태를 제공하면서 물리적 저장소 소유권은 고객에게 남기는 유일한 메이저 옵션이다.

---

## Slide 23: Vertex Agent Engine — Sessions + Memory Bank

**Visual**: 두 박스. Sessions(단기, 대화 컨텍스트) / Memory Bank(장기). Memory Bank 쪽에 GenerateMemories · RetrieveMemories 화살표와 scope 키 태그.

**Key Points**:
- `GenerateMemories` / `RetrieveMemories`
- `scope`가 멀티테넌시 경계
- ADK 없이도 사용 가능

**Speaker Notes**: scope를 명시하지 않으면 자동으로 user_id로 키가 매겨지고, 같은 스코프끼리만 통합 대상이 된다. Agent Engine SDK는 ADK가 아닌 프레임워크에서도, 프레임워크 없이 REST로도 쓸 수 있다.

---

## Slide 24: 서드파티 메모리 3파전

**Visual**: 3열 카드. mem0(키-값 아이콘) / Zep(시계+그래프 아이콘) / Letta(OS 창 아이콘). 하단에 공통 MCP 배지.

**Key Points**:
- mem0: 범용 메모리 API
- Zep: 시간 인식 지식 그래프
- Letta: 자기 편집 에이전트 OS

**Speaker Notes**: 메모리를 MCP 툴로 노출하면 모델·프레임워크·클라우드를 전부 갈아치워도 기억이 남는다. 락인 회피 관점에서 가장 강력한 선택지다.

---

## Slide 25: 섹션 — 크로스오버

**Visual**: 섹션 디바이더. "④ 같이 쓰면 기억은 어디에?".

**Key Points**: (없음)

**Speaker Notes**: 가장 중요한 섹션이다.

---

## Slide 26: 세 계층은 직교한다

**Visual**: 3열 선택 매트릭스. ①추론 ②루프 ③기억. 각 열에서 하나씩 고르는 연결선을 여러 색으로 그림.

**Key Points**:
- 추론 · 루프 · 기억
- 각 열에서 자유 선택
- 조합이 곧 아키텍처

**Speaker Notes**: "메모리가 어디 있냐"는 질문에는 단일 답이 없고 세 개의 답이 있다. 이 슬라이드가 그 사실을 시각화한다.

---

## Slide 27: 실제로 성립하는 7가지 조합

**Visual**: 7행 표. 각 행에 추론/세션/메모리 위치를 국기·클라우드 아이콘으로 표기해 "서로 다른 회사에 흩어짐"을 시각화.

**Key Points**:
- OpenAI SDK + Claude 모델 + 내 Redis
- AgentCore + OpenAI 모델 + AWS 메모리
- 아무 모델 + MCP 메모리

**Speaker Notes**: 3번 조합을 강조한다. 추론은 OpenAI, 세션은 AWS microVM, 장기 메모리도 AWS다. 세 개가 다른 회사일 수 있다.

---

## Slide 28: 판별 규칙 — 세 가지 질문

**Visual**: 3단 체크리스트. 각 질문 옆에 "무엇이 결정하는가" 답.

**Key Points**:
- 대화 이력 → 세션 백엔드 설정
- 툴 산출물 → 샌드박스 소유자
- 세션 넘는 사실 → 붙인 L3 제품

**Speaker Notes**: 세 번째 질문의 답이 "안 붙였으면 어디에도 안 쌓인다"라는 점을 강조한다. 많은 팀이 에이전트가 자동으로 기억한다고 착각한다.

---

## Slide 29: 안티패턴 — 이중 기록

**Visual**: 경고 슬라이드. SDK 세션과 모델 API가 각각 이력을 prepend해 프롬프트에 같은 턴이 두 번 들어가는 그림. 토큰 청구서 아이콘이 부풀어 오름.

**Key Points**:
- source of truth는 하나
- 중복 턴 · 과다 과금 · 순서 꼬임
- L3는 예외

**Speaker Notes**: SDK 세션을 쓰면 모델 API는 무상태 모드로. 모델 API 서버 세션을 쓰면 SDK는 그걸 래핑하는 구현만. 장기 메모리는 이력이 아니라 추출된 사실이므로 이중이 아니다.

---

## Slide 30: 이식성 스펙트럼

**Visual**: 좌→우 그라데이션 바. 왼쪽 "이식성 높음 / 운영 부담 높음", 오른쪽 "락인 강함 / 운영 부담 낮음". 제품들을 바 위에 배치.

**Key Points**:
- 좋고 나쁨 아님
- 교환의 축
- 조직 상황이 결정

**Speaker Notes**: 락인이 강한 쪽은 그만큼 인프라를 안 만들어도 된다. 자체 구현 쪽은 자유롭지만 샌드박스·재개·감사 로그를 전부 직접 만들어야 한다.

---

## Slide 31: 섹션 — 결정 가이드

**Visual**: 섹션 디바이더. "⑤ 실무에서 어떻게 고를 것인가".

**Key Points**: (없음)

**Speaker Notes**: 거버넌스 → 비용 → 락인 순으로 자른다.

---

## Slide 32: 거버넌스가 가장 많이 자른다

**Visual**: 필터 깔때기. 위에서 모든 선택지가 들어가고, "ZDR" / "테넌트 내 저장" / "지리 고정" / "감사 추적" 필터를 통과하며 줄어듦.

**Key Points**:
- ZDR 필수 → L0 + compaction
- 테넌트 내 → Azure BYO / AgentCore
- 감사 필요 → 버전·불변 이벤트

**Speaker Notes**: Managed Agents가 ZDR·HIPAA BAA 비적용이라는 공식 고지는 예외가 아니라 L2 계층의 일반 법칙이다. 툴 실행이 서버로 가면 상태도 서버로 간다.

---

## Slide 33: 비용은 저장이 아니라 재전송에서 나온다

**Visual**: 3개 레버 아이콘. 캐싱 / compaction / 장기 메모리로 옮기기. 각각 토큰 그래프가 내려가는 미니 차트.

**Key Points**:
- Prompt caching
- Compaction · context editing
- 사실만 조회하기

**Speaker Notes**: 여기에 에이전트 계층 고유의 통제 장치도 있다. Managed Agents의 예산 상한, AgentCore의 15분 유휴 회수와 8시간 상한.

---

## Slide 34: 상황별 권장 조합

**Visual**: 7행 결정표. 왼쪽 상황 아이콘, 오른쪽 권장 스택 뱃지.

**Key Points**:
- 단순 챗봇 → L0 + 앱 DB
- 규제 산업 → BYO 스토리지
- 수 시간 자율 작업 → Managed Agents

**Speaker Notes**: 모델을 자주 갈아탈 예정이라면 AgentCore Runtime이나 자체 루프 + MCP 메모리. 개인화가 제품 핵심이면 전용 L3가 반드시 필요하다.

---

## Slide 35: 의사결정 플로차트

**Visual**: 전체 화면 플로차트. "서버가 보관하나?" → "툴도 서버가?" → "저장소를 소유해야?" → "세션을 넘어 기억?" 네 갈래.

**Key Points**:
- 4개 질문으로 스택 결정
- 마지막 질문이 L3 여부

**Speaker Notes**: 이 한 장만 사진 찍어가도 된다고 말한다.

---

## Slide 36: 기억할 다섯 문장

**Visual**: 번호가 붙은 5줄. 각 줄 왼쪽에 작은 아이콘.

**Key Points**:
- 모델은 무상태다
- 한 벤더 안에 여러 단계
- 툴이 가면 상태도 간다
- 세션과 메모리는 직교
- 이력 소유자는 하나

**Speaker Notes**: 다섯 문장으로 전체를 회수한다. 특히 마지막이 실무 사고를 가장 많이 막아준다.

---

## Slide 37: Q&A

**Visual**: 심플한 마무리. 참고문헌 QR 또는 블로그 링크.

**Key Points**:
- 질문 환영
- 상세 문서 · 참고문헌 링크

**Speaker Notes**: 예상 질문 — "우리는 이미 Chat Completions로 만들었는데 옮겨야 하나?" → 이력 관리가 잘 돌고 있다면 급하지 않다. 옮길 이유는 멀티 디바이스 동기화, 서버측 compaction, 새 기능 접근성 셋 중 하나가 필요할 때다.
