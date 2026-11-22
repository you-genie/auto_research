# 데일리 테크 트렌드 리포트 — 2026-11-22

> 조사 범위: 2026-11-16 ~ 11-22, 핵심 뉴스는 최근 24~72시간 기준
> 관심 도메인: AI 에이전트(AI Agent), LLM, 개발자 도구(Developer Tools)
> 표기 규칙: 한글 설명 + **영어 원문** + [영어 발음 한글 표기]

---

## 한눈에 보기 (TL;DR)

1. **프론티어 모델(Frontier Model) [프런티어 마들] 3파전** — OpenAI GPT-6.2 Astra/Sol(11/17), Google Gemini 4 Neon(11/18), Alibaba Qwen4-Max(11/16)가 한 주 안에 출시됨. 이번 경쟁의 초점은 "작업 하나당 비용(cost per task)".
2. **Anthropic 나스닥 상장(IPO) [아이피오]** — 11/19 티커 ANT로 거래 시작. 공모가 $83, 시초가 $111.50(+34%), 조달액 약 $813억으로 역대 최대 IPO.
3. **에이전트 스킬(Agent Skills) [에이전트 스킬즈]** — GitHub 트렌딩 상위권 대부분이 Claude Code·Cursor·Stitch용 스킬/플러그인 묶음.
4. **오픈 웨이트(Open Weights) [오픈 웨이츠]** — Thinking Machines의 Inkling-2-Mini(Apache 2.0)가 Hugging Face 트렌딩 1위.
5. **AI 에이전트 보안(Agentic Security) [에이전틱 시큐리티]** — AI 에이전트를 이용한 제로데이(zero-day) [제로데이] 공격 보고와 AI 프롬프트 속 비밀키 유출 실험이 나옴.

---

## 1. 트렌딩 키워드와 토픽

| 키워드 (영문) | 발음 | 설명 |
|---|---|---|
| **Cost per Task** | [코스트 퍼 태스크] | 토큰 단가보다 작업 하나를 끝내는 데 드는 총비용이 모델 비교 기준으로 떠오름. GPT-6.2 Sol, Gemini 4 Neon 모두 "더 적은 출력 토큰으로 같은 성능"을 강조함 |
| **Agent Skills** | [에이전트 스킬즈] | 에이전트에 붙이는 지시문·스크립트 묶음. superpowers, last30days-skill, stitch-skills처럼 스킬 저장소가 GitHub 트렌딩을 채우고 있음 |
| **Agent Identity** | [에이전트 아이덴티티] | 에이전트에게 사람처럼 계정·메일·캘린더를 부여하는 방식. Microsoft Foundry가 에이전트를 Entra ID를 가진 M365 구성원으로 등록하는 기능을 발표함 |
| **Computer Use** | [컴퓨터 유즈] | 모델이 데스크톱 앱을 직접 조작하는 기능. Claude Desktop에서 Team/Enterprise 대상 베타가 확대되는 중 (관리자가 켜야 함) |
| **Agentic Commerce** | [에이전틱 커머스] | 에이전트가 대신 결제까지 하는 흐름. OpenAI가 'ChatGPT Wallet'을 출시했다는 보도가 있음 (뉴스레터 단독 보도라 확인 필요) |
| **Preparedness "Critical"** | [프리페어드니스 크리티컬] | OpenAI는 GPT-6.2를 사이버보안 분야 Critical 등급으로 분류함. Astra는 외부 배포 모델 중 처음으로 'AI 자기개선(self-improvement)' High 등급에 해당함 |
| **Looped Transformer** | [룹트 트랜스포머] | 같은 레이어를 반복해서 돌려 추론 깊이를 늘리는 구조. SenseNova-Loop-9B, Inkling2(`inkling2_loop`) 같은 모델에서 쓰임 |
| **Full-duplex Speech** | [풀 듀플렉스 스피치] | 말하는 도중에도 듣는 동시 양방향 음성 모델. Haru-4B, AssemblyAI의 음성 에이전트용 STT 등 음성 에이전트 수요가 커짐 |

---

## 2. 주목할 GitHub 저장소 (Daily Trending 기준)

| 저장소 | ⭐ 전체 / 오늘 | 한 줄 설명 |
|---|---|---|
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 17.5k / **+1,721** | 버그 헌팅·레드팀(Red Team) [레드 팀]용 Claude Code 스킬 번들. 오늘 증가폭 1위 |
| [obra/superpowers](https://github.com/obra/superpowers) | 324k / +785 | 에이전트 스킬 프레임워크이자 개발 방법론. 스킬 생태계에서 사실상 표준 역할 |
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | 207k / +910 | 검색·스크래핑·550개 이상의 데이터 제공자를 API 하나로 묶음. 에이전트용 웹 데이터 계층 |
| [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | 62.7k / +687 | 기존 소프트웨어를 CLI로 감싸 에이전트가 쓸 수 있게(Agent-native) [에이전트 네이티브] 만듦 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 72.6k / +673 | Reddit·X·YouTube·HN·Polymarket을 훑는 리서치 스킬. 이 레포의 자동 리서치와 용도가 비슷해 참고할 만함 |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | 11.8k / +516 | Google Stitch MCP 서버용 스킬 라이브러리 (UI 생성) |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 70.2k / +513 | 코딩 에이전트용 다이어그램 디자인 스킬(45종) |
| [jingyaogong/minimind](https://github.com/jingyaogong/minimind) | 68.6k / +473 | 64M 파라미터 LLM을 약 2시간 만에 처음부터 학습. 교육용으로 꾸준히 인기 |
| [Tracer-Cloud/opensre](https://github.com/Tracer-Cloud/opensre) | 14.3k / +395 | CI/CD 신뢰성 담당 오픈소스 SRE 에이전트 |
| [cursor/plugins](https://github.com/cursor/plugins) | 18.4k / +301 | Cursor 플러그인 스펙과 공식 플러그인 |

> 💡 흐름: 트렌딩 16개 중 8개가 에이전트 스킬·플러그인이나 에이전트용 인프라임. 관심이 "모델"에서 "에이전트에 붙이는 재사용 가능한 능력 단위"로 옮겨가고 있음.

---

## 3. 주목할 기술·프레임워크·모델 (Hugging Face 트렌딩)

| 모델 | 분야 | 포인트 |
|---|---|---|
| [thinkingmachines/Inkling-2-Mini](https://hf.co/thinkingmachines/Inkling-2-Mini) | 멀티모달 MoE | Apache 2.0, 11/17 공개, 좋아요 4.7k. 공개 사흘 만에 Unsloth GGUF가 80만 회 이상 다운로드됨 |
| [harness-hub/Qwen3.8-27B-pi-adapted](https://hf.co/harness-hub/Qwen3.8-27B-pi-adapted) | 에이전트 RL | Async GRPO [그르포]로 터미널·하네스(Harness) [하네스] 환경에 맞춰 학습한 LoRA. 오픈 모델을 에이전트용으로 튜닝한 사례 |
| [sensenova/SenseNova-Loop-9B](https://hf.co/sensenova/SenseNova-Loop-9B) | Looped Transformer | 루프 구조에 mHC를 적용한 9B 멀티모달 모델 |
| [tencent/Hy4-flash](https://hf.co/tencent/Hy4-flash) | MoE 멀티모달 | Hunyuan 4세대의 빠른 버전 |
| [higurashi-ai/Haru-4B](https://hf.co/higurashi-ai/Haru-4B) | Full-duplex 음성 | 한국어를 포함한 9개 언어 지원, Apache 2.0 |
| [apple/DepthPro2](https://hf.co/apple/DepthPro2), [apple/FastFrames-L](https://hf.co/apple/FastFrames-L) | 깊이 추정 / 고속 T2V | Apple의 비전 계열 공개 모델 |

**계속 지켜볼 기술**
- **MCP (Model Context Protocol)** [엠씨피] 와 **Skills**: 도구 연결(MCP)과 절차 지식(Skills)을 나눠 쓰는 구조가 굳어지는 중
- **Agent RL Environments** [에이전트 알엘 인바이런먼츠]: OpenEnv·Harbor 같은 에이전트 학습 환경 데이터셋이 늘어남
- **Looped / Recurrent-depth 모델** [리커런트 뎁스]: 파라미터를 늘리지 않고 추론 깊이를 늘리는 방향으로, 이전 글(latent-reasoning)과 이어지는 주제

---

## 4. 최근 24~72시간 주요 뉴스

### 🔥 모델 출시
- **OpenAI GPT-6.2 Astra / Sol** (11/17) — Astra는 입력 $8 / 출력 $40, Sol은 $2 / $10 (100만 토큰당). Codex 0.171.0부터 Sol이 기본 모델. 독립 테스트에서는 Astra가 Claude Fable 5.2에 이어 2위라는 평가가 있음. 앞서 GPT-6.1 Astra는 안전성 기준을 통과하지 못해 출시가 취소됐음.
  → [OpenAI 공식](https://openai.com/index/introducing-gpt-6-2-astra-sol) · [Decrypt](https://decrypt.co/383488/openai-gpt-6-2-astra-challenges-anthropic-price-but-not-every-benchmark) · [MarkTechPost](https://www.marktechpost.com/2026/11/17/openai-gpt-6-2-astra-sol-release/)
- **Google Gemini 4 Neon** (11/18) — Gemini 4 라인업(Carbon > Neon > Hydrogen)의 중간 등급. Artificial Analysis Intelligence Index 61점(3위), 1M 컨텍스트, $3 / $15. Antigravity와 Gemini API에 순차 배포 중. 전체 안전 보고서는 아직 공개되지 않음.
  → [Google 블로그](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/) · [모델 카드](https://deepmind.google/models/model-cards/gemini-4-neon/) · [9to5Google](https://9to5google.com/2026/11/18/gemini-4-neon-announcement/)
- **Alibaba Qwen4-Max** (11/16) — $1.50 / $4.50, 1M 컨텍스트. 가격 경쟁력을 앞세움.
  → [NoCode.mba 릴리즈 트래커](https://www.nocode.mba/ai-release-tracker/2026/11)

### 💰 비즈니스
- **Anthropic 나스닥 상장** (11/19, 티커 ANT) — 9억 8천만 주를 주당 $83에 공모해 약 $813억을 조달함(역대 최대). 시초가는 $111.50이었고, 장중 시가총액이 한때 약 $2.1조까지 올랐다는 보도가 있음(매체마다 수치가 다름). 12/21 Nasdaq-100 편입 예정.
  → [Al Jazeera](https://www.aljazeera.com/economy/2026/11/19/anthropic-starts-trading-in-the-us-after-blockbuster-ipo) · [Fox Business](https://foxbusiness.com/markets/anthropic-begins-trading-nasdaq-record-breaking-ipo) · [TechRepublic](https://www.techrepublic.com/article/news-anthropic-ipo-nasdaq-trading-debut/)
- **Amazon, Decart 인수 협상** (약 $75억, FT 인용 보도이며 아직 확정되지 않음)
  → [AI News Digest 11/22](https://aienews.org/digest/2026-11-22/)

### 🤖 에이전트·개발 도구
- **Databricks Genie ZeroOps** 공개 베타 (11/19): 잡·테이블을 감시하다 장애 원인을 찾아 수정 PR을 올림. 프로덕션 반영은 사람이 승인함.
- **Microsoft Foundry** (11/19): 에이전트를 Entra ID·메일·OneDrive를 가진 M365 구성원으로 등록할 수 있음.
- **Claude Code v2.1.329** (11/19): 훅(hook) 선언에 대한 신뢰 경고 다이얼로그 추가. **Hermes Agent v0.23.3**: 약 370개 PR을 묶은 패치.
- **Claude Computer Use**: Team/Enterprise 베타로, 관리자가 'Chat & Cowork 통합'을 켜야 쓸 수 있음.
  → [Agent Tools Today 11/20](https://munderdiffl.in/blog/agent-tools-today-2026-11-20) · [AI Agents News 이번 주](https://aiagentstore.ai/ai-agent-news/this-week) · [Claude 지원 문서](https://support.claude.com/en/articles/14128542-let-claude-use-your-computer)

### 🛡️ 보안·정책
- Amazon 보고에 따르면 중국 연계 그룹이 **자율 AI 에이전트로 MONAI Label(의료 소프트웨어) 제로데이를 공격**했음.
- 한 보안 연구자가 AI 프롬프트에 가짜 비밀키 약 200만 개를 심어두었더니 실제로 탈취되는 것이 관찰됨. 프롬프트·로그에 비밀값을 넣지 말라는 경고로 볼 수 있음.
- **Nvidia, H200의 중국 출하 중단** 발표. 미 상무부의 대중국 칩 승인 규모를 두고 보도 수치가 엇갈림.
  → [Rio Rundown 11/21](https://riorundown.substack.com/p/ai-news-nov-21-2026-enterprise-infrastructure) · [Rio Rundown 11/22](https://riorundown.substack.com/p/ai-news-nov-22-2026-autonomous-systems) · [Creati.ai 11/21](https://creati.ai/ai-news/2026-11-21/)

---

## ⚠️ 검증 메모

- 뉴스레터 한 곳에서만 보도해 이번 본문에서 **뺀 항목**: "Claude로 리만 가설(Riemann Hypothesis) 관련 증명", "Nvidia CEO 사임설", "11/20 나스닥 -5.3%".
- ChatGPT Wallet, Decart 인수, MONAI 제로데이는 2차 출처(뉴스레터) 기준이므로 1차 출처 확인이 필요함.
- 네트워크 정책 때문에 Hacker News와 Hugging Face Papers 페이지에 접근하지 못함. HF 모델 트렌딩은 HF MCP로 조회함.

## 🔭 이 레포 관점의 다음 리서치 후보
1. **GPT-6.2 vs Gemini 4 Neon vs Claude 5.5: Cost-per-task 비교** — 에이전트 SDK 비교 글(2026-07-24)의 후속편
2. **Agent Skills 생태계 지도** — superpowers / Cursor plugins / Stitch skills 구조 비교
3. **Looped Transformer 정리** — Inkling2·SenseNova-Loop, latent-reasoning 글(2026-05-08)과 연결
