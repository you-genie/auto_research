# 데일리 테크 트렌드 리포트 — 2026-11-25

> 자동 생성 리포트 (scheduled routine). 표기법: **한글 용어 (English 원문, [영어 발음])**
> ✅ = 1차/복수 매체로 확인 · ⚠️ = 집계 사이트(aggregator)에만 보도되어 미확인

---

## 한 줄 요약

**이번 주 흐름은 "에이전트(Agent)를 감독하고 검증하는 도구"입니다.** GitHub 트렌딩은 에이전트 리뷰·플래닝·스킬 레포가 장악했고, 시장에서는 Anthropic(ANT) 주가가 상장 4거래일 만에 공모가 아래로 내려갔습니다. 모델 쪽에서는 Google Gemini 4 Neon이 "중간 티어 가성비" 경쟁에 불을 붙였습니다.

---

## 1. 트렌딩 키워드 & 토픽

| 키워드 | 발음 | 설명 |
|---|---|---|
| **에이전트 스킬 (Agent Skills)** | [에이전트 스킬즈] | 코딩 에이전트에 붙이는 재사용 가능한 작업 패키지입니다. 이번 주 GitHub 트렌딩 상위권 절반 이상이 스킬 레포(`last30days-skill`, `stitch-skills`, `ffmpeg-skill`, `claude-trading-skills`)였습니다. "모델"보다 "모델에 무엇을 붙이느냐"로 경쟁 축이 옮겨가고 있다는 신호입니다. |
| **휴먼 인 더 루프 (Human-in-the-loop)** | [휴먼 인 더 룹] | 에이전트가 행동하기 전에 사람이 계획을 검토하고 승인하는 구조입니다. `plannotator`, `n8n-io/nod`("행동 전에 물어보는 에이전트")가 급상승했습니다. |
| **AI 코드 리뷰 (AI Code Review)** | [에이아이 코드 리뷰] | `alibaba/open-code-review`가 주간 +2.6k★를 기록했습니다. 규칙 파이프라인(rule pipeline)에 LLM 에이전트를 결합해 라인 단위 코멘트를 다는 방식입니다. |
| **에이전틱 커머스 (Agentic Commerce)** | [에이전틱 커머스] | AI 에이전트가 사용자를 대신해 쇼핑하는 흐름입니다. Meta의 Muse 에이전트를 Amazon은 차단했고(9월), Walmart·Shopify는 제휴했습니다. 블랙프라이데이를 앞두고 "에이전트 접근권"을 둘러싼 플랫폼 간 대치가 다시 화제가 되고 있습니다. |
| **프런티어 모델 출시 보류 (Frontier Model Withholding)** | [프런티어 모델 위드홀딩] | 위험하다고 판단한 모델은 제한된 파트너에게만 공개하는 관행입니다. Anthropic Mythos, OpenAI GPT-6.1 Astra 사례가 이어졌고, 주가 하락의 배경으로도 다시 거론되고 있습니다. |
| **AI 취약점 스캐너 (AI Vulnerability Scanner)** | [에이아이 벌너러빌리티 스캐너] | Drupal 코어 설치기(installer) RCE 취약점(SA-CORE-2026-017)은 Anthropic OSS Scanner가 발견해 크레딧을 받았습니다. AI가 실제 CVE를 찾아내는 일이 일상이 되고 있습니다. |

---

## 2. 떠오르는 GitHub 레포지토리

### 주간 트렌딩 (github.com/trending?since=weekly)

| 레포 | 언어 | 총 ★ / 주간 ★ | 설명 |
|---|---|---|---|
| [backnotprop/plannotator](https://github.com/backnotprop/plannotator) | TS | 15.1k / +2.0k | 에이전트의 계획을 사람이 주석(annotate)하고 리뷰한 뒤 피드백을 돌려보내는 워크스페이스입니다. |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | Python | 75.0k / **+5.4k** | Reddit·X·YouTube·HN·Polymarket을 훑어 최근 30일 동향을 요약하는 에이전트 스킬입니다. 이번 주 최대 상승 레포입니다. |
| [dream-num/univer](https://github.com/dream-num/univer) | TS | 31.8k / +3.3k | AI를 붙일 수 있는 오피스(스프레드시트·문서) SDK입니다. |
| [kajisho5/ffmpeg-skill](https://github.com/kajisho5/ffmpeg-skill) | Python | 11.0k / +3.0k | FFmpeg 도구 42개와 MCP(Model Context Protocol, [엠씨피]) 서버를 묶은 로컬 영상 편집 키트입니다. |
| [meta/astryx](https://github.com/meta/astryx) | TS | 33.1k / +2.9k | Meta가 공개한 "에이전트 친화적(agent-ready)" 디자인 시스템입니다. |
| [alibaba/open-code-review](https://github.com/alibaba/open-code-review) | Go | 56.3k / +2.6k | 규칙과 LLM을 결합한 하이브리드 코드 리뷰 도구입니다. |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | TS | 12.9k / +2.6k | Google Stitch MCP 서버용 스킬 라이브러리입니다. |
| [GoogleChrome/modern-web-guidance-src](https://github.com/GoogleChrome/modern-web-guidance-src) | TS | 11.0k / +2.5k | 코딩 에이전트에 최신 웹 베스트 프랙티스를 주입하는 가이드입니다. |
| [ag-ui-protocol/ag-ui](https://github.com/ag-ui-protocol/ag-ui) | TS | 21.7k / +1.8k | 에이전트를 프런트엔드 UI에 연결하는 프로토콜입니다. 생성형 UI(Generative UI) 흐름과 이어집니다. |
| [n8n-io/nod](https://github.com/n8n-io/nod) | TS | 3.5k / +1.0k | n8n이 공개한 로컬 퍼스널 에이전트입니다. 모델을 직접 고르고, 행동하기 전에 확인을 받습니다. **신규라 주목할 만합니다.** |

### 일간 트렌딩 하이라이트
- [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter): 버그 헌팅·레드팀(red-team, [레드 팀])용 Claude Code 스킬 번들입니다. 하루 +1.6k★.
- [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything): 아무 소프트웨어나 CLI로 감싸서 에이전트가 쓸 수 있게(agent-native) 만듭니다. 하루 +1.1k★.
- [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design): 코딩 에이전트용 다이어그램 디자인 스킬로, 52가지 유형을 지원합니다.
- [jingyaogong/minimind](https://github.com/jingyaogong/minimind): 64M 파라미터 LLM을 약 2시간 만에 처음부터 학습하는 교육용 프로젝트입니다.

---

## 3. 주목할 기술 / 프레임워크

1. **Gemini 4 Neon** [제미나이 포 네온] ✅: Google이 11/18에 출시했습니다. Carbon(최상위)과 Hydrogen(경량) 사이의 중간 티어입니다. Carbon과 비슷한 품질에 작업 속도는 약 3배, 작업당 비용은 약 25~32% 낮다고 주장합니다. 1M 토큰 컨텍스트에 사고 단계(thinking level) 4개를 지원하고, AI Studio·Antigravity에서 쓸 수 있습니다. 경쟁 상대로는 Claude Opus 5.5와 GPT-6.2 Sol이 거론됩니다.
2. **AG-UI 프로토콜 (Agent-User Interaction Protocol)** [에이지-유아이]: MCP(도구 연결)와 A2A(에이전트 간 통신)에 이어 "에이전트↔UI" 계층의 표준 후보입니다. 지난 10월 리포트의 [OpenIntelligentUI](../2026-10-23-open-intelligent-ui/) 주제와 직접 맞닿아 있습니다.
3. **Enterprise Frontier Safeguards (EFS)** [엔터프라이즈 프런티어 세이프가드] ✅: Anthropic의 제로 데이터 보존(ZDR)과 오용 탐지를 결합한 기능으로, 로그가 고객 소유 클라우드에 남습니다. 9월에 발표되어 단계적으로 배포 중이며, "가을 중 광범위 제공"을 목표로 하고 있습니다.
4. **Claude Code Code Review** [코드 리뷰] ✅: 여러 에이전트가 PR을 병렬로 검토하고, 오탐(false positive)을 검증한 뒤 심각도 순으로 정리합니다. **승인(approve)은 하지 않습니다.** 집계 사이트에서 "Claude Ship"이라는 이름으로 "자동 승인까지 한다"고 보도됐지만, 공식 출처에서는 확인되지 않습니다.

---

## 4. 지난 24시간 주요 뉴스

| | 뉴스 | 상태 |
|---|---|---|
| 📉 | **Anthropic(ANT) 주가가 공모가($83) 아래로 하락**했습니다. 11/24 종가는 $81.91(−6.5%)이며 장중 한때 $76 미만까지 내려갔습니다. 상장 4거래일 만으로, SpaceX(21일)보다 빠릅니다. 원인으로는 S-1에 공개된 약 $9,000억의 컴퓨트 약정과 "신규 모델이 너무 위험하다"는 보도가 거론됩니다. Dario·Daniela Amodei는 IPO 때 각각 약 $2.8억어치를 매도했습니다. Canaccord는 매수 의견(목표가 $135)으로 커버리지를 시작했습니다. 12월에 최대 3억 주 규모의 보호예수(lock-up) 해제 물량이 리스크입니다. | ✅ [CNBC](https://www.cnbc.com/2026/11/24/anthropic-stock-ipo-price.html) · [Bloomberg](https://www.bloomberg.com/news/articles/2026-11-24/anthropic-breaks-below-83-ipo-price-in-premarket-trading) · [Forbes](https://www.forbes.com/sites/eriksherman/2026/11/24/anthropic-shares-fall-under-the-ipo-price-heres-what-it-means/) |
| 🛡️ | **Anthropic·OpenAI 직원들이 "미공개 모델이 출시하기엔 너무 위험하다"고 우려**한다는 보도가 나왔습니다. 새 학습 중단이나 내부 전용 운영까지 검토 중이라고 합니다. 8~9월의 Mythos 보류, GPT-6.1 Astra 출시 취소에서 이어지는 흐름입니다. | ⚠️ 11/24 원문 기사는 미확인. 배경: [Axios](https://axios.com/2026/08/14/anthropic-model-2-ai-risk) · [Al Jazeera](https://aljazeera.com/economy/2026/9/29/openai-scraps-release-of-latest-ai-model-over-safety-concerns) |
| 🔐 | **Drupal 코어 치명적 RCE (SA-CORE-2026-017)**: 특정 조건에서 설치기를 다시 실행해 사이트를 탈취할 수 있습니다. Anthropic OSS Scanner가 발견했습니다. "실제 공격(in-the-wild)에 악용 중"이라는 보도는 확인되지 않았지만, Drupal 측은 빠른 익스플로잇 등장을 경고했습니다. **Drupal을 운영 중이라면 바로 패치하세요.** | ✅ 패치 / ⚠️ 악용 여부. [Drupal 공지](https://drupal.org/sa-core-2026-017) · [BleepingComputer](https://bleepingcomputer.com/news/security/drupal-patches-critical-rce-flaw-warns-exploits-may-surface-quickly) |
| 🛒 | **Walmart가 블랙프라이데이 딜을 Meta Muse 에이전트에 개방**했고, Amazon과 Meta가 Muse 차단 문제로 협상 중이라는 보도가 나왔습니다. | ⚠️ 블프 관련 내용은 미확인. 배경: [Axios(9월)](https://www.axios.com/2026/09/21/amazon-meta-muse-ai-agentic-shopping) |
| 🇺🇸 | **미 상무부가 Alibaba 싱가포르 법인 "Apex"를 Entity List에 추가**했다는 보도와, Schumer 의원이 Jensen Huang의 수출통제 위반을 주장했다는 보도가 있습니다. | ⚠️ 공식 BIS 발표 미확인 |
| 🇦🇺 | **호주 디지털 주의의무법 (Digital Duty of Care)**: "매출 5% 벌금으로 통과"라는 보도가 있으나, 확인된 사실은 10/28 하원 통과와 최대 A$1.09억 정액 벌금(AI 챗봇 포함)까지입니다. 상원 통과는 미확인입니다. | ⚠️ [MinterEllison](https://www.minterellison.com/articles/australias-new-digital-duty-of-care-what-it-means) |
| 💹 | AI 매도세로 **SoftBank가 2년 만에 최악의 하루**를 보냈다는 보도가 있습니다. | ⚠️ 11/25 원문 미확인 |

---

## 이번 주 체크포인트

- **Anthropic 보호예수 해제(12월)**와 **Gemini 4 Carbon 프로모션 가격 종료(12/1)**: 가격과 시장의 변곡점입니다.
- 에이전트 스킬 생태계가 폭발적으로 커지고 있습니다. 인기 스킬 레포가 주당 수천 ★씩 오릅니다. 블로그 후속 주제로 **"2026 에이전트 스킬 생태계 지도"**를 추천합니다.
- AG-UI처럼 에이전트를 UI에 연결하는 프로토콜이 계속 성장하고 있습니다. 10/23 GenUI 글의 후속편 소재가 될 수 있습니다.

---

### 조사 한계
- `aiweekly.co`, `trendshift.io`는 세션 네트워크 정책 때문에 직접 열람하지 못했습니다(검색 스니펫만 활용). ⚠️ 항목은 대부분 이 집계 사이트에서 나온 것이라 원문 확인이 필요합니다.
- GitHub 트렌딩 수치는 2026-11-25 조회 시점 기준입니다.
