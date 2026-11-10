---
layout: default
title: "데일리 트렌드 리포트 (2026-11-10): Claude Fable 5.2 출시 · Anthropic IPO 로드쇼 · DeepMind RSA-1024 · 오픈웨이트 동향"
date: 2026-11-10
categories: [research, trend-report]
tags: [daily-trends, anthropic, ipo, claude-fable, mythos, deepmind, rsa, github-trending, huggingface, agents]
---

# 데일리 트렌드 리포트 — 2026년 11월 10일

<div class="doc-hero" markdown="1">
**3줄 요약**
1. **Anthropic(앤트로픽)**이 11/9 **Claude Fable 5.2(페이블)** / **Mythos 5.2(미토스)**를 공개했고, 11/10 **IPO 로드쇼(로드쇼, roadshow)**를 시작했습니다. 공모가 범위는 주당 $70~78, Nasdaq 티커는 `ANT`이며 11/19 상장이 예상됩니다(보도 기준).
2. **Google DeepMind(구글 딥마인드)**는 AI 에이전트가 사람의 감독 아래 **레거시 1024비트 RSA**의 약점 두 가지를 찾았다고 발표했습니다(11/6). 2048비트 이상 키는 여전히 안전합니다.
3. 오픈소스에서는 **에이전트를 백그라운드에서 돌리는 도구**, **AI가 휴대폰을 조작하는 도구**, **LLM용 3D 모델링 도구**가 GitHub 트렌딩에 올랐습니다. Hugging Face에서는 **Gaussian Splatting(가우시안 스플래팅)** 기반 image-to-3D 모델과 **Kimi K3.1 Pro**가 상위권입니다.
</div>

> ⚠️ 출처 신뢰도 안내: Anthropic 공식 뉴스, GitHub, Hugging Face 데이터는 직접 확인했습니다. IPO 수치와 일부 뉴스는 2차 매체(검색 결과 요약) 기준이라 공식 S-1 문서와 대조가 필요합니다. 이번 실행 환경에서는 cnbc.com과 theneuron.ai에 직접 접속할 수 없었습니다.

---

## 1. 트렌딩 키워드 & 토픽

| 키워드 (영문 / 발음) | 설명 |
|---|---|
| **AI IPO** (에이아이 아이피오) | Anthropic 상장 절차가 본격화되었습니다. 동시에 미국 중간선거 이후 데이터센터 반대 여론(**data center backlash**, 데이터 센터 백래시)이 투자 심리의 변수로 거론됩니다. |
| **Gated Model Access** (게이티드 모델 액세스) | 같은 모델을 일반용(안전장치 적용)과 검증된 기관용(사이버·생명과학 분야에서 제한 완화) 두 갈래로 배포하는 방식입니다. Fable 5.2와 Mythos 5.2의 관계가 대표 사례입니다. |
| **AI-assisted Cryptanalysis** (에이아이 어시스티드 크립타날리시스) | 에이전트가 암호 공격 알고리즘을 개선하는 연구입니다. 레거시 키를 서둘러 **migration(마이그레이션)**해야 한다는 메시지와 함께 나왔습니다. |
| **Background Agents** (백그라운드 에이전츠) | CLI 에이전트가 사용자 개입 없이 오래 작업하고, 확신이 없을 때만 사람에게 묻는 패턴입니다. |
| **Agent Skills** (에이전트 스킬즈) | `anthropics/skills`, `google/skills` 같은 스킬 저장소가 꾸준히 인기입니다. 에이전트 경쟁의 초점이 모델에서 "스킬 레이어"로 옮겨가고 있습니다. |
| **Super Intelligence Task Force** (슈퍼 인텔리전스 태스크 포스) | 미국 행정부 조직으로, AI 관련 기소를 조율하고 일부 주(州) AI 법에 이의를 제기하는 역할을 맡았다고 보도되었습니다. |
| **AI Training Opt-out Token** (옵트아웃 토큰) | OpenAI, Google, Microsoft, Anthropic이 robots.txt에 공통 토큰을 지원해, 퍼블리셔가 AI 학습 사용을 거부할 수 있게 한다는 보도가 있습니다. |

---

## 2. 주목받는 GitHub 저장소

**GitHub Trending(깃허브 트렌딩)** 일일 스냅샷(11/9~11/10) 기준입니다. 에뮬레이션, 탈옥, 무료 계정 우회처럼 성격이 모호한 저장소는 제외했습니다.

| 저장소 | 언어 | ⭐ (트렌딩 시점) | 한 줄 설명 |
|---|---|---|---|
| [KKKKhazix/agent-autoloop](https://github.com/KKKKhazix/agent-autoloop) | TypeScript | ~4.2K | CLI 에이전트가 작업을 받아 **백그라운드에서 끝까지 수행**하고, 불확실할 때만 사람에게 질문합니다. *Human-in-the-loop(휴먼 인 더 루프)* 자동화 도구입니다. |
| pinky | Go | ~1.6K | AI 에이전트가 **사용자 휴대폰을 조작**하되, 사람이 계속 상황을 확인할 수 있게 해 줍니다. 모바일 **Computer Use(컴퓨터 유즈)**의 흐름에 있습니다. |
| [Sandflow-ai/sand3d](https://github.com/Sandflow-ai/sand3d) | Python/HTML | ~1.5K | **LLM이 다루기 쉽게 설계된 3D 모델링** 라이브러리입니다. |
| [sarpstar/cinecode](https://github.com/sarpstar/cinecode) | Python | ~1.7K | 코딩 에이전트가 각본, 프레임, 사운드를 코드로 만들어 **단편 영상이나 광고를 생성**합니다. |
| [livliv-dev/player](https://github.com/livliv-dev/player) | TypeScript | ~1.4K | 립싱크와 웹캠 얼굴 추적을 지원하는 경량 2.5D 웹 캐릭터 플레이어입니다(AI 아바타용). |
| chimera-vocal-synth | Rust | ~1.4K | 노래, 말하기, 비트박스를 할 수 있는 보컬 신시사이저입니다. |
| [govijr/terminal-mac](https://github.com/govijr/terminal-mac) | Swift | ~2.4K | macOS 환경 전체를 터미널 안에서 실행하는 실험적 프로젝트입니다. |

GitHub Explore에서 꾸준히 보이는 저장소는 [anthropics/skills](https://github.com/anthropics/skills), [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)(Rust 기반, 에이전트용 헤드리스 브라우저 CLI), [google-deepmind/mujoco](https://github.com/google-deepmind/mujoco)(물리 시뮬레이터)입니다.

출처: [daily-trending-repo #605 (11/10)](https://github.com/marc-ko/daily-trending-repo/issues/605), [#604 (11/9)](https://github.com/marc-ko/daily-trending-repo/issues/604), [GitHub Explore](https://github.com/explore)

---

## 3. 주목할 기술 & 프레임워크

### 🤗 Hugging Face 트렌딩 모델 (직접 조회, trendingScore 기준)

| 모델 | 태스크 | 포인트 |
|---|---|---|
| [speridlabs/idol](https://hf.co/speridlabs/idol) | image-to-3D | 이미지 한 장을 **3D Gaussian Splatting(가우시안 스플래팅)** 장면으로 변환하는 오픈웨이트 파이프라인입니다(Apache-2.0, 10/28 공개). |
| [moonshotai/Kimi-K3.1-Pro](https://hf.co/moonshotai/Kimi-K3.1-Pro) | image-text-to-text | Moonshot(문샷)의 새 멀티모달 모델로, 11/2에 공개되었습니다. |
| [ricursiveAI/Ripple-65B-Preview](https://hf.co/ricursiveAI/Ripple-65B-Preview) | — | 커스텀 아키텍처 65B 프리뷰 모델입니다(Apache-2.0, 11/4). |
| [NousResearch/Arete-27B](https://hf.co/NousResearch/Arete-27B) | text-generation | Qwen3.8-27B를 기반으로 **value alignment(밸류 얼라인먼트)** SFT를 적용했습니다(11/6). |
| [Lightricks/LTX-2.5](https://hf.co/Lightricks/LTX-2.5) | video/audio 생성 | 오디오와 비디오를 함께 생성하는 오픈 모델입니다. 다운로드 약 280만 회로 꾸준히 강세입니다. |
| [MiniMaxAI/MiniMax-H3-Image](https://hf.co/MiniMaxAI/MiniMax-H3-Image) | text-to-image | MiniMax H3 기반 이미지 생성 및 편집 모델입니다(11/3). |
| [Qwen/Qwen3.8-27B](https://hf.co/Qwen/Qwen3.8-27B) | 멀티모달 | 좋아요 약 1.96만 개로 **파인튜닝 베이스의 사실상 표준**입니다. 트렌딩 목록의 상당수가 이 모델의 파생입니다. |

### 🔭 모니터링 포인트
- **Gaussian Splatting → 생성형 3D**: idol, sand3d, Qwen3.5-4B-3D-Coder(Three.js 코드 생성)가 함께 떠오르고 있습니다. "LLM이 3D를 만든다"는 흐름이 굳어지는 중입니다.
- **.NET 11** (닷넷 일레븐): 11월 출시가 예정되어 있습니다(projected). **.NET 8과 9는 오늘(11/10) 지원이 종료**되므로 해당 버전을 쓰는 팀은 업그레이드를 점검해야 합니다. ([endoflife.date](https://endoflife.date/dotnet))
- **Microsoft Agent Framework (Python) 1.25.0**: Python 3.10 지원을 중단하고 3.11 이상을 요구하는 *breaking change(브레이킹 체인지)*가 포함됩니다. ([Releasebot](https://releasebot.io/updates/microsoft))

---

## 4. 최근 24~72시간 주요 뉴스

### 🟣 Anthropic — Claude Fable 5.2 & Mythos 5.2 출시 (11/9)
- Anthropic은 두 모델을 "가장 뛰어난 모델"로 소개하며, 코딩, 금융, 과학 분야의 고난도 기술 작업을 겨냥한다고 밝혔습니다. ([Anthropic News](https://www.anthropic.com/news))
- **Mythos 5.2**는 Fable 5.2와 같은 모델이지만, 검증된 사이버보안·생명과학 기관(**Verification Program**, 베리피케이션 프로그램)에는 안전장치를 완화해 제공합니다.
- 가격(보도 기준): 입력 100만 토큰당 $8, 출력 100만 토큰당 $40로 5.1 세대보다 약 20% 저렴합니다. **Fast mode(패스트 모드)**는 $16/$80입니다. ([Anthropic Mythos 페이지](https://www.anthropic.com/claude/mythos), [DataCamp](https://www.datacamp.com/blog/claude-fable-5-2-and-mythos-5-2))
- 벤치마크(자체 발표): CyScenarioBench 76.3%(5.1은 61.7%), CVE Rediscovery 89.6%. 사전 테스트에서 Fable 5.2 에이전트 1,000개가 **페르마의 마지막 정리(Fermat's Last Theorem)**를 30시간 만에 완전히 **formalization(포멀라이제이션, 형식화)**했다는 주장도 있습니다. 모두 자체 보고이므로 독립 검증을 지켜봐야 합니다.

### 💰 Anthropic — IPO 로드쇼 시작 (11/10)
- Anthropic은 Class A 보통주 IPO 로드쇼를 시작한다고 공식 발표했습니다. ([Anthropic News](https://www.anthropic.com/news))
- 보도에 따르면 공모가 범위는 **$70~78**, 티커는 **`ANT`**(Nasdaq), 거래 시작은 **11/19 예정**입니다. 기업가치는 $1.5조~1.6조 수준으로 거론되며, 초기 목표였던 $2조에서 낮아졌습니다. ([CNBC](https://www.cnbc.com/2026/11/10/anthropic-sets-price-range-of-70-to-78-in-upcoming-ipo.html), [CNBC: 데이터센터 반발](https://www.cnbc.com/2026/11/07/anthropic-ipo-ai-data-center-backlash.html))
- 수정된 S-1에는 약 **$8,954억** 규모의 컴퓨트·인프라 구매 약정이 적혀 있다고 보도되었습니다. Google·Nvidia·Microsoft 등 7개사가 공모가로 $260억을 투자한다는 보도도 있지만, S-1에서 확인되는 것은 Google의 최대 $100억 옵션뿐입니다. ([Yahoo Finance](https://finance.yahoo.com/technology/articles/google-nvidia-microsoft-among-7-140216121.html))

### 🔐 Google DeepMind — AI 에이전트가 레거시 RSA-1024 약점 2건 발견 (11/6)
- **서명 패딩(signature padding)**: 공격자가 서명 블록의 약 절반 이상을 통제하면 패딩이 사실상 보호 효과를 잃습니다. 이론상 기존 최고 공격보다 약 1,600배 개선되었으며, 실제 벤치마크 키에서는 CPU 시간이 3.5배 줄었습니다.
- **배치 인수분해(batch factoring)**: 키를 하나 더 인수분해할 때 드는 평균 비용이 약 30배 감소했습니다.
- **2048비트 이상 키는 안전합니다.** NIST는 2013년부터 1024비트 키로 새 서명을 만드는 것을 허용하지 않고 있습니다. 시사점은 공포가 아니라 레거시 키 마이그레이션입니다. ([Interesting Engineering](https://interestingengineering.com/ai-robotics/google-deepmind-agents-expose-older-encryption-flaws), [Let's Data Science](https://letsdatascience.com/news/google-deepmind-ai-agents-find-faster-attacks-on-legacy-rsa-5d679013))

### 📰 기타 (2차 매체 기준, 미검증 항목 포함)
- **Gemini Omni 1.2 Flash** 정식 출시(GA, 11/5), 15초 비디오 클립 생성 지원. ([Crypto Briefing 주간 정리](https://cryptobriefing.com/openai-anthropic-reveal-new-ai-models-products-in-week-45-of-2026/))
- **OpenAI**: Cursor에 커스텀 모델을 직접 공급하던 계약을 11/12에 종료할 예정이라는 보도가 있습니다. GPT-6 Cyber를 검증된 테스터에게만 제한 공개했다는 보도도 있지만 출처가 하나뿐입니다. ([ThursdAI 11월 릴리스](https://thursdai.news/releases/2026-11))
- **Nvidia(엔비디아)**: CEO 관련 스캔들 보도 후 장전 거래에서 주가가 5% 이상 하락했다고 전해집니다. ([AI Weekly](https://aiweekly.co/ai-news-today))
- **실적**: AMD와 Palantir가 AI 수요에 힘입어 시장 예상치를 넘었습니다. PubMatic은 **agentic buying(에이전틱 바잉)**이 실제 운영 규모로 돌아가고 있다고 밝혔습니다. ([The Agile Brand Guide](https://agilebrandguide.com/yesterdays-marketing-technology-ai-news-november-10-2026))
- **연구**: MIT는 가정용·보조 로봇의 직관적 상호작용 기법 **FLEX(플렉스)**를 발표했습니다. 실제 업무에서 코딩 에이전트가 자주 실패한다는 새 벤치마크도 화제입니다. ([Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-09-2026-ai-agents-and))

---

## 📌 한 줄 결론
이번 주의 축은 **Anthropic(신모델 + IPO)**입니다. 기술적으로는 **"에이전트가 연구한다"(암호해독·수학 형식화)**와 **"에이전트가 혼자 오래 일한다"(백그라운드 에이전트·휴대폰 조작)**라는 두 흐름이 동시에 커지고 있습니다. 오픈웨이트 쪽은 Qwen3.8 파생 모델과 3D/비디오 생성이 강세입니다.
