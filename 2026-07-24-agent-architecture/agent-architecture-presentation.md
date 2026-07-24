# AI 에이전트 구성요소 전면 해부 (2026) — 프레젠테이션 아웃라인

> 변환 대상: PPT/Keynote. 각 슬라이드는 **제목 + 비주얼 지시 + 최소 텍스트(3단어 이하 지향) + 발표자 노트**. 다이어그램/아이콘/인포그래픽 우선.

---

## Slide 1: 표지
**Visual**: 8개 레이어가 겹겹이 쌓인 반투명 스택 다이어그램(맨 위 "사용자 목표", 맨 아래 "샌드박스 VM"), 배경은 다크 그라디언트. 우하단에 작은 while-loop 아이콘.
**Key Points**:
- 요즘 에이전트, 뭘로 만드나
- 가장 복잡한 에이전트 해부
- 2026
**Speaker Notes**: "LLM + 툴"이라는 요약은 2023년에 끝났다. 오늘은 상상 가능한 가장 복잡한 에이전트 하나를 상정하고, 그걸 완성하는 8개 레이어를 전부 뜯어본다.

---

## Slide 2: Agenda
**Visual**: 8개 번호 칩(1~8)이 세로 타임라인/스택으로 정렬, 각 칩에 아이콘(골격/저울/렌치/뇌+디스크/흐름도/네트워크/방패/공장).
**Key Points**:
- 하네스 · 컨텍스트 · 툴/MCP/스킬
- 메모리 · 플래닝 · 멀티에이전트
- 평가/가드레일 · 상용
**Speaker Notes**: 이 8개가 목차이자 "복잡한 에이전트"의 부품 목록. 각 레이어마다 개념→1차자료→상용 순으로 본다.

---

## Slide 3: 관통 원칙 — 컨텍스트 경제
**Visual**: 가운데 큰 깔때기(funnel). 위로 "수천 툴·긴 히스토리·전체 문서"가 쏟아지고, 아래로 "최소 고신호 토큰"만 빠져나옴. 옆에 attention budget 게이지(거의 참).
**Key Points**:
- Smallest high-signal set
- Attention = 유한 자원
**Speaker Notes**: 뒤에 나올 거의 모든 기법(스킬 progressive disclosure, 툴 defer_loading, code mode)이 이 한 문장의 파생이다. 복잡한 에이전트의 본질은 기능 추가가 아니라 토큰 절약 싸움.

---

## Slide 4: [섹션 구분] L1 — 하네스와 에이전트 루프
**Visual**: 큰 while-loop 회전 화살표, 안에 "assemble → call LLM → parse → execute tool → feed back".
**Speaker Notes**: 골격. 날것의 모델을 동작하는 에이전트로 만드는 소프트웨어 래퍼.

---

## Slide 5: 하네스란?
**Visual**: 양파 단면 — 중심 "LLM", 겹겹이 "loop / tools / context mgmt / memory / guardrails / tracing".
**Key Points**:
- 모델을 감싼 래퍼
- 모델과 co-train
- "loop engineering"
**Speaker Notes**: 2026 핵심 통찰: 모델은 자기 하네스와 함께 학습된다. Claude Code·Codex 모두 동일 하네스를 공유. 하네스 엔지니어링이 상위 규율로 부상.

---

## Slide 6: 코어 루프 — gather → act → verify
**Visual**: 3단계 순환 다이어그램(gather context / take action / verify work) + "repeat" 화살표.
**Key Points**:
- Gather: 필요한 것만
- Act: 툴 = 유일한 진전
- Verify: 목표 대조
**Speaker Notes**: Anthropic Agent SDK의 루프 정식화. "툴 없는 루프는 while문 속 챗봇일 뿐."

---

## Slide 7: Workflow vs Agent
**Visual**: 좌우 대비 — 왼쪽 고정 파이프라인(코드가 경로 결정), 오른쪽 자율 루프(LLM이 경로 결정). 하단 "단순한 것부터".
**Key Points**:
- Workflow: 미리 정의된 경로
- Agent: LLM이 동적 지휘
- 필요할 때만 복잡도↑
**Speaker Notes**: Anthropic 철학 — 애초에 에이전트를 안 만드는 게 답일 수도. 빌딩블록 = augmented LLM(LLM+검색+툴+메모리).

---

## Slide 8: 상용 3대 하네스
**Visual**: 3열 카드(Claude Code / Codex CLI / Cursor), 각 카드에 루프 특징 미니 아이콘.
**Key Points**:
- Claude Code: 단일 nO 루프
- Codex: Responses API 루프
- Cursor: 8-iter Agent Loop
**Speaker Notes**: Claude Code는 단일 스레드 마스터 루프 고수. Codex는 AGENTS.md+compaction. Cursor는 test-run-fix 8회+Background Agents.

---

## Slide 9: [섹션 구분] L2 — 컨텍스트 엔지니어링
**Visual**: 뇌 모양 게이지가 토큰으로 서서히 차오르며 회상 정확도 곡선이 하락.
**Speaker Notes**: 프롬프트 엔지니어링의 후계자. "최적의 토큰 집합을 큐레이션·유지하는 전략".

---

## Slide 10: Attention Budget & Context Rot
**Visual**: 왼쪽 n² 관계망(토큰 늘수록 폭발), 오른쪽 하락 곡선("input↑ → recall↓"), Chroma 18개 모델 라벨.
**Key Points**:
- 모든 토큰이 budget 소모
- 길수록 정확도 저하
- 1M ≠ 신뢰성 있는 1M
**Speaker Notes**: 컨텍스트는 한계효용 체감하는 유한 자원. 크게 넣는다고 좋아지지 않는다.

---

## Slide 11: Write / Select / Compress / Isolate
**Visual**: 4분면 인포그래픽, 각 사분면 아이콘(디스크에 쓰기 / 끌어오기 / 압축 / 분리).
**Key Points**:
- Write · Select
- Compress · Isolate
**Speaker Notes**: Lance Martin/LangChain 통합 분류. 컨텍스트 엔지니어링 기법 전부가 이 4버킷에 들어간다. 실패 4모드: poisoning/distraction/confusion/clash.

---

## Slide 12: Manus의 KV-cache 6원칙
**Visual**: 6개 카드 그리드, 상단에 큰 "10×" 배지($0.30 vs $3.00/MTok).
**Key Points**:
- KV-cache = #1 metric
- Mask, don't remove
- Keep the wrong stuff in
**Speaker Notes**: 프로덕션 골드 소스. 프레임워크를 4번 갈아엎으며("Stochastic Graduate Descent") 얻은 교훈. 프리픽스 안정+append-only+파일시스템 메모리+todo.md recitation+에러 남기기.

---

## Slide 13: 장기실행 = 교대근무 모델
**Visual**: 릴레이 배턴을 넘기는 두 로봇(Initializer → Coding agent), 사이에 feature-list.json·git commit·progress.txt.
**Key Points**:
- 세션 = 교대 근무
- 상태 = 지속 산출물
**Speaker Notes**: 컨텍스트 창 넘는 며칠짜리 작업. 세션 간 상태는 컨텍스트가 아니라 파일·커밋·테스트 게이트로 넘긴다.

---

## Slide 14: [섹션 구분] L3 — 툴 / MCP / 스킬
**Visual**: 3개 퍼즐 조각(손 / USB-C / 책)이 맞물림.
**Speaker Notes**: 손(행동) · 연결 표준 · 전문 지식(절차). 경쟁이 아니라 레이어.

---

## Slide 15: 툴 사용 라운드트립
**Visual**: 4단계 순환(tools 요청 → tool_use → 실행 → tool_result → 최종답). client vs server 분기 표시.
**Key Points**:
- tool_use → tool_result
- client vs server 실행
- strict / 병렬 / tool_choice
**Speaker Notes**: 핵심 구분은 "코드가 어디서 실행되는가". strict:true로 스키마 보장, 병렬 기본 on.

---

## Slide 16: MCP — AI를 위한 USB-C
**Visual**: 중앙 Host, 방사형으로 Client→Server 연결선, 각 서버가 앱 아이콘(DB/GitHub/브라우저). 하단 "tools · resources · prompts".
**Key Points**:
- Host / Client / Server
- stdio(로컬) · HTTP(원격)
- tools/resources/prompts
**Speaker Notes**: Anthropic 2024-11 발표, 2026 광범위 채택. USB-C 비유. JSON-RPC 2.0 stateful. 보안: tool poisoning·rug pull·prompt injection 주의.

---

## Slide 17: Agent Skills — 온보딩 가이드
**Visual**: 폴더 트리(SKILL.md + FORMS.md + scripts/)와 3층 계단(L1 메타 / L2 지침 / L3 리소스), 각 층에 토큰 배지(~100 / <5k / 0).
**Key Points**:
- SKILL.md 폴더
- Progressive disclosure 3층
- ~100 토큰/스킬 상주
**Speaker Notes**: "신입 온보딩 가이드" 비유. 트리거 전엔 이름+설명만. 스크립트 코드는 컨텍스트 미진입, 출력만. 번들 콘텐츠에 실질적 한계 없음.

---

## Slide 18: Code Mode — 컨텍스트 경제의 절정
**Visual**: Before/After 막대(150,000 토큰 → 2,000 토큰, 98.7%↓). Cloudflare "117만 → ~1k(99.9%↓)" 부제.
**Key Points**:
- 150k → 2k 토큰
- 툴 호출 대신 코드 작성
- 중간결과 모델 미경유
**Speaker Notes**: MCP를 코드 API로 제시→에이전트가 코드 작성해 샌드박스 실행. LLM은 툴 호출보다 코드 작성을 더 잘한다. Programmatic Tool Calling + Tool Search(defer_loading).

---

## Slide 19: Tools vs MCP vs Skills 비교
**Visual**: 3열 비교표(정체 / 무엇을 더함 / 컨텍스트 비용 / 비유).
**Key Points**:
- Tool: 함수
- MCP: 연결 표준
- Skill: 노하우
**Speaker Notes**: 경쟁 아님. 스킬이 툴·MCP를 호출하고 스크립트를 돌리도록 지시. 복잡한 에이전트는 넷을 동시에 겹쳐 쓴다.

---

## Slide 20: Clarification / Elicitation — 에이전트가 되묻기
**Visual**: 실행 루프가 멈추고 사용자에게 말풍선 모달(질문 + 자동생성 객관식 옵션)이 뜨는 그림. 옆에 3분법 라벨(Clarification / Approval / Interrupt).
**Key Points**:
- AskUserQuestion (Claude Code 네이티브)
- MCP elicitation · A2A input-required
- Codex: 자율지향 → 네이티브 부재
**Speaker Notes**: clarification(정보 부족해 되묻기)은 approval(승인 게이팅)·interrupt(사용자 중단)과 별개. Claude Code는 전용 네이티브 툴(옵션 자동생성 + 모달 렌더 + 루프 블록)로 승격. 프로토콜 레벨엔 MCP elicitation·A2A input-required·Managed Agents requires_action. Codex는 비동기·자율(sandbox-per-task)이라 되묻기가 큐를 막으므로 약하게 두고 가정+명시/커뮤니티 스킬로 대체. 모델 자체도 ask-rate를 프롬프트로 튜닝(Opus 4.8은 자주 묻는 경향).

---

## Slide 21: [섹션 구분] L4 — 메모리 & RAG
**Visual**: 뇌 + 외장 디스크 아이콘, 사이에 write/read 양방향 화살표.
**Speaker Notes**: 컨텍스트 밖에 기억을 쓰고 필요할 때 되읽기.

---

## Slide 22: 메모리 분류 체계
**Visual**: 2축 매트릭스 — 세로(단기/장기), 가로(semantic/episodic/procedural), 각 셀 예시 아이콘.
**Key Points**:
- 단기(창) vs 장기(밖)
- 사실 / 경험 / 절차
**Speaker Notes**: Procedural은 점점 파인튜닝이 아니라 편집 가능한 in-context 지침으로 저장.

---

## Slide 23: 장기 메모리 구현체 비교
**Visual**: 5행 비교 카드(Letta / Anthropic memory tool / Mem0 / Zep / LangMem), 각 행에 핵심 메커니즘+대표 수치.
**Key Points**:
- Letta: OS 3계층
- Anthropic: memory+context editing (84%↓, +39%)
- Zep: 시간적 KG
**Speaker Notes**: Anthropic memory tool + context editing 결합이 100턴 eval에서 토큰 84% 절감·성능 39% 향상. Zep은 bi-temporal 엣지 무효화로 stale memory 해결.

---

## Slide 24: Agentic RAG
**Visual**: 좌(정적 RAG: 일직선) vs 우(agentic: 검색이 루프 속 툴, 재검색·CRAG 폴백 분기).
**Key Points**:
- 검색 = 결정하는 툴
- Self-RAG / CRAG
- 하이브리드+rerank
**Speaker Notes**: 언제·무엇을·어떻게 검색할지 에이전트가 결정. BM25+dense→RRF→cross-encoder rerank(NDCG +26~31%). 전역 질문엔 GraphRAG.

---

## Slide 25: [섹션 구분] L5 — 플래닝 / 추론 / 자기수정
**Visual**: 분기하는 흐름도(플랜→실행→검증→재계획).
**Speaker Notes**: 무엇을 다음에 할지 결정하는 제어 흐름.

---

## Slide 26: 추론 패턴 계보
**Visual**: 트리 계보도 — CoT 뿌리에서 ReAct/ToT/Reflexion/ReWOO/LLM Compiler로 가지.
**Key Points**:
- ReAct: 인터리브
- Plan-and-Execute
- Reflexion: 언어적 RL
**Speaker Notes**: 각 원 논문과 함께. ReWOO는 토큰 5배 효율, LLM Compiler는 DAG 병렬로 지연 3.7배 개선.

---

## Slide 27: 프로덕션 = 외부화된 가변 계획
**Visual**: todo.md/TodoWrite 체크리스트 카드 3개(Claude Code / Manus / Devin), 각 상태 pending/in_progress/done.
**Key Points**:
- TodoWrite (3+ 스텝)
- todo.md recitation
- 동적 재계획(Devin)
**Speaker Notes**: 학술 패턴이 실전에선 명시적·외부화·가변 TODO로. 계획을 항상 보이게 유지해 goal drift 방어.

---

## Slide 28: Anthropic 5 워크플로우 패턴
**Visual**: 5개 미니 다이어그램(chaining/routing/parallelization/orchestrator-workers/evaluator-optimizer).
**Key Points**:
- 단일 → 워크플로우 → 에이전트
- 명확한 기준 → evaluator
**Speaker Notes**: 결정 휴리스틱: 경로가 알려지면 워크플로우, 스텝 예측 불가한 개방형에만 완전 에이전트.

---

## Slide 29: 테스트타임 컴퓨트
**Visual**: 두 축(순차=사고 연장 / 병렬=다수 샘플+투표), generator-verifier gap 저울.
**Key Points**:
- 순차 vs 병렬 스케일링
- 검증 < 생성
**Speaker Notes**: 작은 모델이 더 오래 생각하면 큰 모델을 이길 수 있다(DeepMind). 검증이 생성보다 쉬워서 병렬 스케일링이 통한다.

---

## Slide 30: [섹션 구분] L6 — 멀티에이전트
**Visual**: 오케스트레이터 노드에서 3~5 서브에이전트로 팬아웃하는 방사형.
**Speaker Notes**: 작업을 쪼개 병렬 서브에이전트로 확장.

---

## Slide 31: Anthropic 멀티에이전트 리서치
**Visual**: 리드(Opus)→서브(Sonnet)×5 병렬→합성→CitationAgent. 우측 큰 배지 "+90.2%" / "15× 토큰".
**Key Points**:
- 단일 대비 +90.2%
- 15× 토큰
- read-heavy만 이득
**Speaker Notes**: 성능 분산의 80%를 토큰이 설명 — 멀티가 이기는 건 토큰을 더 쓰기 때문. 고가치·병렬 작업에만 경제적. 공유 컨텍스트·강결합엔 부적합.

---

## Slide 32: 프레임워크 지형도
**Visual**: 2축 산점도 — X축(그래프/결정적 ↔ 자율/LLM주도), Y축(코드 ↔ 대화). LangGraph/OpenAI SDK/CrewAI/AutoGen/ADK/Claude Agent SDK 배치.
**Key Points**:
- 그래프 vs 자율
- 대부분 이제 둘 다
**Speaker Notes**: 핵심 축은 제어 모델. 결정적(검사가능) vs 자율(유연). 2026 프레임워크 대부분 양쪽 제공.

---

## Slide 33: MCP vs A2A vs AGNTCY
**Visual**: 수직축(MCP: 에이전트↓툴) + 수평축(A2A: 에이전트↔에이전트) 십자 다이어그램, 위에 AGNTCY(발견/신원/관측) 우산.
**Key Points**:
- MCP: 수직
- A2A: 수평
- AGNTCY: 발견/신원
**Speaker Notes**: 상보적. A2A는 Agent Card·Task 상태기계. 2025-06 Linux Foundation, 2026 v1.0. ACP는 A2A로 병합.

---

## Slide 34: "멀티에이전트 만들지 마라" 논쟁
**Visual**: 좌우 링(Cognition: single writer) vs (Anthropic: 병렬 읽기), 가운데 화해 배너 "읽기=병렬, 쓰기=단일".
**Key Points**:
- Cognition: 컨텍스트 공유
- 충돌하는 암묵 결정
- 화해: read↔write
**Speaker Notes**: Cognition Principle 1·2. MAST: 7 프레임워크 실패율 41~87%. 화해점 — 읽기/검색은 병렬화, 쓰기/코딩은 단일 스레드나 격리 샌드박스.

---

## Slide 35: [섹션 구분] L7 — 평가 / 관측 / 가드레일 / 신뢰성
**Visual**: 방패 + 돋보기 + 게이지 아이콘.
**Speaker Notes**: 프로덕션 경화. 70% 작동 프로토타입과 프로덕션 사이의 간극.

---

## Slide 36: 평가 3단계
**Visual**: 3층 피라미드(Final Response / Trajectory / Single-Step) + 벤치마크 로고 띠.
**Key Points**:
- 결과 / 궤적 / 단계
- SWE-bench·GAIA·τ²-bench
**Speaker Notes**: 출력만 보면 대부분 실패를 놓친다. Trajectory eval이 툴 선택·인자·상태전파를 잡는다. τ²-bench는 정책 준수+pass^k(신뢰성).

---

## Slide 37: Lethal Trifecta
**Visual**: 3원 벤다이어그램 교집합(사설 데이터 / 비신뢰 콘텐츠 / 외부 통신) = 위험 폭발 아이콘.
**Key Points**:
- 사설 데이터
- 비신뢰 콘텐츠
- 외부 통신
**Speaker Notes**: Simon Willison. 셋이 겹치면 탈취. 프롬프트 하드닝으로 못 막는다 — 방어는 아키텍처적, 한 다리를 제거. "이메일 접근 툴은 완벽한 비신뢰 콘텐츠 소스".

---

## Slide 38: 신뢰성 — checkpoint ≠ durable
**Visual**: 좌(프로세스 죽으면 런도 죽음) vs 우(Temporal: 런이 생존, 재시도·재개).
**Key Points**:
- Idempotency
- Checkpoint vs Durable
- 라우팅/캐시/버짓
**Speaker Notes**: LangGraph 체크포인트는 노드 사이만 저장. Durable execution(Temporal)은 런 자체가 생존. 코스트: 라우팅 45~85%↓, prefix cache 90%↓.

---

## Slide 39: [섹션 구분] L8 — 상용에서는 뭘 쓰나
**Visual**: 제품 로고 그리드(Claude Code/Devin/Manus/Codex/Copilot/Cursor/Jules/AgentCore/Replit/Comet).
**Speaker Notes**: 겉모습은 제각각, 벗겨보면 8개 레이어의 조합.

---

## Slide 40: 상용 티어다운 표
**Visual**: 큰 비교표(제품 / 단일·멀티 / 실행환경 / 핵심 베팅) — 색상 코딩.
**Key Points**:
- 샌드박스-per-task 보편
- 단일 vs 멀티 = 작업 형태
- CI = 샌드박스+게이트
**Speaker Notes**: Claude Code=하네스, Devin=planner→executor, Manus=파일시스템 메모리, Codex=RL-on-tests, Copilot=CI 게이트, Cursor=best-of-N 병렬, Jules=비동기 VM.

---

## Slide 41: 관통하는 7가지 교훈
**Visual**: 7개 번호 배지 리스트, 각 아이콘.
**Key Points**:
- 컨텍스트 > 프롬프트
- KV-cache 안정
- 에러를 남겨라 / 검증을 루프에
**Speaker Notes**: 컨텍스트 엔지니어링이 #1 job(3사 독립 명명). 메모리를 파일시스템으로. 읽기 병렬/쓰기 단일. verification-in-the-loop.

---

## Slide 42: 전체 조립도
**Visual**: 블로그의 ASCII 조립도를 깔끔한 아키텍처 다이어그램으로 재현 — 사용자 목표 → 하네스 루프(gather/act/verify) → 각 레이어 라벨 → 샌드박스 실행 → PR.
**Key Points**:
- 8 레이어 = 한 시스템
- 관통 원칙: 컨텍스트 경제
**Speaker Notes**: 상정한 "가장 복잡한 에이전트"의 완성도. 모델은 상수, 차별화는 하네스의 attention budget 관리로 이동.

---

## Slide 43: 결론
**Visual**: 한 문장 대형 타이포 "더 똑똑한 프롬프트가 아니라 더 잘 설계된 시스템", 배경에 흐릿한 스택.
**Key Points**:
- 시스템 설계의 승부
- 컨텍스트 경제
**Speaker Notes**: 2026의 복잡한 에이전트는 무엇을 넣고/빼고/검증하고/복구하느냐의 문제. 관통 원칙은 하나 — 컨텍스트 경제.

---

## Slide 44: Q&A / 참고문헌
**Visual**: QR 또는 링크 리스트(Anthropic engineering, Manus blog, Cognition, MCP spec, A2A spec, MAST).
**Key Points**:
- Q&A
- 1차 자료 링크
**Speaker Notes**: 핵심 load-bearing 인용/수치는 원문 대조 권장(egress 제약으로 검색 기반 수집).
