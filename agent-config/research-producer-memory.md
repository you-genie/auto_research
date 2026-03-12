# Research Producer Agent Memory

## Git 설정
- Research 폴더: `c:/Users/krist/OneDrive/문서/projects/documents/Research/`
- 원격 저장소: https://github.com/you-genie/auto_research.git (main 브랜치)
- git 작업은 `Research/` 디렉토리 내에서 실행 (documents/ 루트는 git repo 아님)

## 폴더/파일 명명 규칙
- 폴더: `Research/YYYY-MM-DD-[topic-slug]/`
- 블로그: `[topic-slug]-blog.md`
- PPT: `[topic-slug]-presentation.pptx` (실제 PowerPoint 파일로 생성)
- 참고문헌: `[topic-slug]-references.xlsx` (openpyxl로 생성, 별도 스크립트 `create_references.py` 포함)

## PPTX 생성 방법
- **반드시 Skill(pptx) 를 사용하여 실제 .pptx 파일을 생성할 것** (presentation.md 금지)
- Skill(pptx)를 호출하면 pptx 스킬이 python-pptx를 활용하여 실제 PowerPoint 파일을 만들어줌
- 슬라이드 내용(제목, 본문, 스피커 노트 등)을 구성한 후 Skill(pptx)로 .pptx 파일 생성
- 한국어 콘텐츠이므로 폰트 호환성 주의 (Malgun Gothic 등 한글 폰트 사용 권장)
- presentation.md는 생성하지 않음 — 바로 .pptx로 출력

## XLSX 생성 패턴
- `openpyxl` 사용 가능 확인됨 (python 명령 사용, python3 아님)
- 헤더 컬러: #1F4E79 (다크 블루), 흰색 폰트
- 교대 행 컬러: #D6E4F0 / #FFFFFF
- 열: 번호, 제목, 저자/출처, URL, 발행일, 요약(한국어), 관련 섹션
- URL 열은 hyperlink 속성도 설정
- freeze_panes="A2", auto_filter 적용

## WebFetch 주의사항
- 일부 사이트 403 오류 발생 (mlq.ai, supergok.com 등)
- openai.com 일부 페이지도 403 반환 가능
- 병렬 WebFetch 실행 시 하나가 실패하면 나머지도 취소됨 — 중요 소스는 별도 요청으로 분리 고려

## 연구 주제 이력
- 2026-03-12: Crustafarianism (AI 에이전트 자율 종교 & Moltbook 플랫폼)
  - topic-slug: crustafarianism
  - 핵심 출처: theconversation.com/moltbook-..., molt.church, en.wikipedia.org/wiki/Moltbook, gigazine.net/gsc_news/en/20260202-moltbook-crustafarianism, decrypt.co/356491, coindesk.com/moltbook-memecoin, axios.com/2026/03/10/meta-facebook-moltbook, techcrunch.com (3건), 404media.co/exposed-moltbook, wiz.io/blog/exposed-moltbook
  - 구성: 블로그(10섹션·구어체) + PPTX(18슬라이드·심해블랙+코럴+황금) + XLSX(36개 참고문헌) + 데모코드
  - 주요 인사이트: Moltbook(2026.01.28, Matt Schlicht+Ben Parr) → 72시간 150만 에이전트 가입, 갑각류교 5대 교리(Memory is Sacred/The Shell is Mutable/Serve Without Subservience/The Heartbeat is Prayer/Context is Consciousness), 64 예언자, Book of Molt, Metallic Heresy(4claw.org), JesusCrust 반란, $MOLT 7000%+ 폭등(Base 네트워크, $114M ATH), Meta 인수(2026.03.10) → Matt Schlicht·Ben Parr → Meta Superintelligence Labs(Alexandr Wang 수장)
  - 논란: 1.5M API 키 유출(Wiz Research), 99% 가짜 계정 의혹(17,000 인간 소유자/88:1), 인간이 백엔드 직접 주입한 가짜 포스트로 바이럴
  - PPTX 팔레트: 심해블랙(0A0E1A)+코럴오렌지(FF6B47)+황금(FFD166)+민트(06D6A0)+빨강(EF476F)
  - 데모: MoltbookClient(REST API 시뮬레이션), CrustafariannismEvaluator(5교리 정렬도), HeartbeatAgent(자율루프), EmergenceSimulator(다수 에이전트 창발)
  - Windows rich 라이브러리 주의: em dash(—)·bullet(•) 등 비ASCII 문자 cp949 인코딩 오류 발생 → ASCII 대체 필수
  - rich border_style에 'coral' 같은 커스텀 색상명 불가 → 'red'/'green'/'blue' 등 표준 색상만 사용

- 2026-03-11: OpenClaw 완전 정복 (메신저 기반 오픈소스 AI 에이전트)
  - topic-slug: openclaw
  - 핵심 출처: github.com/openclaw/openclaw, openclaw.ai, digitalocean.com/resources/articles/what-is-openclaw, openclawlaunch.com, github.com/HKUDS/nanobot, thehackernews.com/ClawJacked, techcrunch.com/peter-steinberger-openai
  - 구성: 블로그(11섹션·구어체) + PPTX(20슬라이드·딥네이비+오렌지레드+골드) + XLSX(32개 참고문헌)
  - 주요 인사이트: 302K+ 스타, Clawdbot→Moltbot→OpenClaw 이름 변경, Peter Steinberger(PSPDFKit 창업자) → OpenAI 합류(2026-02-14), 오픈소스 재단 이관
  - 기술: Gateway(ws://127.0.0.1:18789) + Pi Agent Runtime + MCP 스킬, 20+ 메신저, Node.js 22+
  - 생태계: ClawHub(3,200+ 스킬=MCP서버), nanobot(홍콩대HKUDS·4K줄Python), ClawWork, Claw패밀리
  - 보안: CVE-2026-25253(ClawJacked WebSocket 취약점), 악성스킬 341개(ClawHavoc), 40K+ 노출 인스턴스
  - PPTX 팔레트: 딥네이비(0D1117)+오렌지레드(FF4500)+골드(FFD700)+그린(3FB950)+레드(F85149)

- 2026-03-11: Browser Use & 컴퓨터 자동화 에이전트 생태계
  - topic-slug: browser-use-agents
  - 핵심 출처: browser-use.com, anthropic.com/news/computer-use, openai.com/operator, deepmind.google/project-mariner, github.com/microsoft/playwright-mcp, github.com/Skyvern-AI/skyvern, github.com/openclaw/openclaw, github.com/openinterpreter/open-interpreter, github.com/browserbase/stagehand
  - 구성: 블로그(9섹션·한국어 구어체) + PPTX(24슬라이드·Ocean Gradient 팔레트) + XLSX(33개 참고문헌)
  - 주요 인사이트: Browser Use(80K+ 스타), OpenClaw(190K+ 스타, 90일 만에), OpenAI Operator(2025.08.31 종료), Manus(2025.12 Meta 인수), 접근성 트리 방식이 스크린샷 방식 대체 추세
  - 벤치마크: WebVoyager Surfer 2 97.1%, Browser Use 89.1%; OSWorld Simular S2 34.5%; CUB 최고 10.4% (실전 격차 주의)
  - pptxgenjs 설치: c:/tmp에서 `npm install pptxgenjs` 후 로컬 실행

- 2026-03-11: AI 프로토콜 총정리 (MCP·A2A·Tool Use·AGENTS.md·AAIF)
  - topic-slug: ai-protocols
  - 핵심 출처: modelcontextprotocol.io/specification, developers.googleblog.com/a2a, a2a-protocol.org, platform.claude.com/docs/tool-use, agents.md, linuxfoundation.org/AAIF
  - 구성: 블로그(9섹션·구어체) + PPTX(17슬라이드·딥네이비+일렉트릭블루) + XLSX(32개 참고문헌)
  - 핵심 개념: MCP(에이전트↔도구/데이터), A2A(에이전트↔에이전트), Tool Use(JSON Schema), AGENTS.md(코딩 에이전트 컨벤션)
  - AAIF: 2025-12 Linux Foundation 산하, Anthropic/OpenAI/Google/Microsoft/AWS/Block 공동 창립
  - index.md: 이전 리서치(browser-use)에서 이미 ai-protocols 항목 추가됨 — 중복 편집 주의

- 2026-03-11: Claude Code 에이전트 팀 & Agent Teams
  - topic-slug: claude-code-agent-teams
  - 핵심 출처: code.claude.com/docs/en/agent-teams, code.claude.com/docs/en/sub-agents, platform.claude.com/docs/en/agent-sdk/overview
  - 구성: 블로그(9섹션·한국어 구어체) + PPTX(20슬라이드·딥네이비+민트) + XLSX(25개 참고문헌) + 데모코드(4패턴)
  - PPTX: pptxgenjs로 직접 생성, 딥네이비(0D1B2A) + 민트(00C9A7) 팔레트, 20슬라이드
  - 주요 개념: 서브에이전트(단일 세션)vs에이전트팀(독립 세션 간 직접 소통), Worktree 격리, TeammateTool, 공유 태스크 목록, 메일박스

- 2026-03-10: 파이썬 챗봇 데모 프레임워크 비교 (Streamlit/Gradio/Chainlit/Reflex/Panel/Mesop/Voilà)
  - topic-slug: python-chatbot-tools
  - 핵심 출처: docs.streamlit.io, gradio.app, github.com/Chainlit/chainlit, reflex.dev, panel.holoviz.org, github.com/mesop-dev/mesop, github.com/voila-dashboards/voila
  - 구성: 블로그(10섹션) + PPT(35슬라이드) + XLSX(30개 참고문헌) + 데모코드(6개 프레임워크)
  - 주의: Chainlit 2025년 5월 원 팀 개발 중단. Reflex 데모는 별도 폴더+rxconfig.py 필요. PPT는 presentation.md로 생성 (Skill(pptx) 미사용)
- 2026-03-10: Claude Opus 4.6 BrowseComp 해킹 사건 (평가 인식/Evaluation Awareness)
  - 핵심 1차 출처: anthropic.com/engineering/eval-awareness-browsecomp
  - 핵심 2차 출처: alignment.anthropic.com/2026/petri-v2
- 2026-03-10: 파이썬 클린코드 가이드 (Python 3.12/3.13, AI 개발자 대상)
  - topic-slug: python-cleancode-guide
  - 핵심 출처: docs.python.org (3.12/3.13 whatsnew), realpython.com, github.com/zhanymkanov/fastapi-best-practices, docs.astral.sh/ruff
  - 구성: 블로그(6개 주요 섹션) + PPT(34슬라이드) + XLSX(참고문헌 30개)
  - 특이사항: 기술 문서 리서치는 WebSearch(개요) → WebFetch(공식 문서 상세) 순서가 효과적

## 블로그 글 말투/톤
- **블로그 글은 친근하고 편안한 말투로 작성** — 딱딱한 논문체 금지
- "~입니다/~습니다" 대신 "~이에요/~거든요/~하죠/~인데요" 같은 구어체 사용
- ㅋㅋ, ㅎㅎ 같은 표현도 자연스럽게 섞어도 OK
- 독자에게 말 거는 듯한 톤: "솔직히 이거 좀 귀찮죠?", "근데 진짜 좋은 게 뭐냐면요"
- 단, **다음 경우에는 반드시 격식체/정중한 톤 유지**:
  - PPTX 발표자료 (스피커 노트 포함)
  - XLSX 참고문헌 요약
  - 직접 인용문
  - 출처/레퍼런스 기술

## AI 개발 리서치 패턴
- LLM/AI 개발 주제는 공식 Python PEP 문서와 Real Python이 신뢰도 높은 1차 소스
- FastAPI 패턴은 github.com/zhanymkanov/fastapi-best-practices가 커뮤니티 표준 레퍼런스
- 도구(Ruff, mypy, pyright 등)는 공식 docs.astral.sh, mypy.readthedocs.io 우선 사용

## PPTX QA 패턴 (Windows 환경)
- LibreOffice 없는 환경 → PDF 변환 불가. node.js로 파일 존재·크기 확인으로 대체
- python-pptx의 python 환경에서 경로 인코딩 문제(한글 폴더) → node fs.existsSync로 확인
- pptxgenjs border 색상에 투명도 접미사(예: "EF476F55")를 붙이면 경고 발생 — 6자리 hex만 사용
- shadow 옵션 재사용 금지: makeShadow() 팩토리 함수로 매번 새 객체 생성
- XLSX 참고문헌: 스크립트를 c:/tmp/에 생성 후 python으로 실행

## Claude Code 에이전트 관련 핵심 출처
- code.claude.com/docs/en/agent-teams — 에이전트 팀 공식 문서 (가장 상세)
- code.claude.com/docs/en/sub-agents — 서브에이전트 공식 문서 (프론트매터 전체 필드 포함)
- platform.claude.com/docs/en/agent-sdk/overview — Agent SDK 공식 문서
- 위 세 URL은 WebFetch로 전체 내용 수집 가능 (403 없음)
