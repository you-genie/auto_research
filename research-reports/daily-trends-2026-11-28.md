# 데일리 테크·AI 트렌드 리포트: 2026-11-28 (토)

> 대상 기간: 2026-11-27 ~ 11-28 (최근 24시간) + 이번 주 맥락
> 범위: AI/LLM, 에이전트(Agent), 오픈소스 생태계 (이 레포의 주 관심 분야)
> 표기 규칙: **한글 용어 (English 원문, [발음])**
> 신뢰도 표시: ✅ 1차 출처/다수 매체 교차 확인 · ⚠️ 2차 집계 사이트에서만 확인 · ❌ 확인 시도했으나 근거 없음

---

## 0. 한눈에 보기 (TL;DR)

| # | 핵심 | 한 줄 요약 |
|---|------|-----------|
| 1 | **리만 가설 (Riemann Hypothesis, [리-만 하이파써시스])** AI 증명 | Lean 커뮤니티가 형식 증명(formal proof)을 검증했다. 다만 사람이 읽을 수 있는 설명(약 25만 쪽)은 아직 공개되지 않았다. ✅ |
| 2 | **에이전트 스킬 (Agent Skills, [에이전트 스킬즈])** 열풍 | GitHub 트렌딩 상위권 대부분이 Claude Code·Cursor용 스킬 번들이다. ✅ |
| 3 | 프런티어 모델 3파전 | Claude Fable 5.2(11/9), GPT-6.2 Astra/Sol(11/17), Gemini 4 Neon(11/18)이 연달아 나왔다. ✅ |
| 4 | **수출 통제 (Export Controls, [익스포트 컨트롤즈])** 강화 | Nvidia가 중국향 H200 출하를 중단했고, 미국은 동남아 우회 수출을 막기 위해 라이선스 의무를 확대했다. ✅ |
| 5 | Anthropic 상장 이후 | IPO 공모가는 $83이었고 첫날 +17%로 마감했다. 이후 '매도세' 보도가 나왔다. ✅/⚠️ |

---

## 1. 트렌딩 키워드·토픽

| 키워드 (원문, [발음]) | 설명 | 왜 뜨는가 |
|---|---|---|
| **에이전트 스킬 (Agent Skills, [에이전트 스킬즈])** | 코딩 에이전트에 붙이는 지식·절차 패키지(SKILL.md 등)다. | GitHub 트렌딩 16개 중 7개 이상이 스킬 관련이다. 스킬이 "프롬프트를 배포하는 단위"로 자리 잡는 중이다. |
| **형식 검증 (Formal Verification, [포멀 베리피케이션])** / **린 (Lean, [린])** | 증명을 기계가 검사할 수 있는 코드로 쓰고 정리 증명기(theorem prover)로 확인하는 방식이다. | AI가 만든 리만 가설 증명을 Lean FRO와 Mathlib 측이 검증했다고 발표했다. "AI 결과물은 기계 검증과 짝을 이룬다"는 흐름이 강해지고 있다. |
| **삼진 양자화 (Ternary Quantization, [터너리 퀀타이제이션])** | 가중치를 {-1, 0, +1}로 표현하는 초저비트(~1.58bit) 압축이다. | HF 트렌딩 3위 `Ternary-Bonsai-2.5-27B`는 Qwen3.8-27B를 온디바이스에서 돌릴 수 있게 만들었다. |
| **MoE (Mixture of Experts, [믹스처 오브 엑스퍼츠])** | 토큰마다 일부 전문가(expert) 네트워크만 활성화하는 구조다. | HF 트렌딩 1위 Thinking Machines의 `Inkling-2-Mini`가 Apache-2.0 MoE 멀티모달 모델이다. |
| **MCP (Model Context Protocol, [모델 컨텍스트 프로토콜])** | 에이전트와 도구를 연결하는 표준 프로토콜이다. | Google Stitch가 MCP 서버용 스킬을 공개했다. 오늘 Workspace에 MCP 이전 마감이 생겼다는 보도는 ❌ 확인되지 않았다(5월 공지만 존재). |
| **에이전트 샌드박스 (Agent Sandbox, [에이전트 샌드박스])** | 에이전트가 코드를 실행하는 격리 환경이다. | AWS가 에이전트용 보안 실행 환경을 내놨다는 보도가 있다 ⚠️. (참고: 이 레포의 `2026-09-15-agent-sandbox-internals` 글) |
| **증류 차단 (Distillation Curbs, [디스틸레이션 커브즈])** | 프런티어 모델의 출력으로 경쟁 모델을 학습시키는 것을 막는 정책이다. | Z.ai의 GLM-5.5 출시가 늦어진 원인으로 거론된다 ⚠️(Reuters 원문은 확인하지 못함). |

---

## 2. 떠오르는 GitHub 저장소 (오늘 기준 `github.com/trending`, 직접 조회 ✅)

| 저장소 | 설명 | ⭐ 총 / 오늘 |
|---|---|---|
| [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | 버그 헌팅·외부 레드팀(Red Team, [레드 팀])용 Claude Code 스킬 번들. **오늘 1위**다. | 27.1K / +1,372 |
| [obra/superpowers](https://github.com/obra/superpowers) | 에이전트 스킬 프레임워크이자 개발 방법론. 수주째 최상위를 지키고 있다. | 329K / +809 |
| [mjmirza/app-store-compliance](https://github.com/mjmirza/app-store-compliance) | App Store·Google Play 심사 거절을 피하기 위한 사전 점검 플레이북 | 8.5K / +907 |
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | 에이전트용 웹 검색·스크래핑 API(550개 이상 공급자 통합) | 212K / +717 |
| [XiaoYouChR/Ghost-Downloader-3](https://github.com/XiaoYouChR/Ghost-Downloader-3) | 다목적 다운로더 | 20.4K / +664 |
| [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything) | 모든 소프트웨어를 CLI로 감싸 **에이전트 네이티브 (Agent-Native, [에이전트 네이티브])**로 만든다. | 67.4K / +561 |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | 최근 30일 동안의 소셜·웹 트렌드를 조사해 요약하는 스킬. 이 리포트와 같은 용도다. | 76.8K / +519 |
| [zhouxiaoka/autoclip](https://github.com/zhouxiaoka/autoclip) | 긴 영상을 자막이 붙은 숏폼으로 자동 편집하는 로컬 우선 도구 | 18.1K / +517 |
| [cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design) | 52종 다이어그램을 그리는 에디토리얼 디자인 스킬(멀티 에이전트 호환) | 74.9K / +499 |
| [jingyaogong/minimind](https://github.com/jingyaogong/minimind) | 64M 파라미터 LLM을 약 2시간 만에 처음부터 학습한다. 교육용으로 꾸준히 인기다. | 72.5K / +391 |
| [google-labs-code/stitch-skills](https://github.com/google-labs-code/stitch-skills) | Stitch MCP 서버용 공식 에이전트 스킬 모음 | 13.9K / +293 |
| [Tracer-Cloud/opensre](https://github.com/Tracer-Cloud/opensre) | CI/CD 안정성을 맡는 오픈소스 **SRE (Site Reliability Engineering, [에스-알-이])** 에이전트 | 16.4K / +270 |
| [cursor/plugins](https://github.com/cursor/plugins) | Cursor 플러그인 명세와 공식 플러그인 | 20.2K / +214 |

**해석:** 트렌딩의 중심이 "모델"에서 "에이전트에 꽂는 부품"(스킬·플러그인·CLI 래퍼·데이터 수집)으로 확실히 옮겨갔다. 특히 보안(BugHunter)과 운영(opensre) 쪽 스킬이 새로 떠오르고 있다.

### Hugging Face 트렌딩 모델 (HF Hub 직접 조회 ✅)

| 모델 | 설명 |
|---|---|
| [thinkingmachines/Inkling-2-Mini](https://hf.co/thinkingmachines/Inkling-2-Mini) | 11/17 공개. 이미지+텍스트 MoE 모델이고 Apache-2.0이다. 좋아요 6.6K, GGUF 파생 모델 다운로드 360만 회 |
| [prism-ml/Ternary-Bonsai-2.5-27B-GGUF](https://hf.co/prism-ml/Ternary-Bonsai-2.5-27B-GGUF) | 11/24 공개. Qwen3.8-27B를 삼진(2bit) 양자화했다. 도구 호출과 **MTP (Multi-Token Prediction, [멀티 토큰 프리딕션])**를 지원한다. |
| [inworld/voice-isolator](https://hf.co/inworld/voice-isolator) | 48kHz 실시간 스트리밍 음성 분리 모델(Apache-2.0) |
| [llamaindex/OCRia-nano-1](https://hf.co/llamaindex/OCRia-nano-1) | CPU에서 도는 경량 문서 파싱·OCR(ONNX) 모델 |
| [kandinskylab/Kandinsky-ImageSR-2.0](https://hf.co/kandinskylab/Kandinsky-ImageSR-2.0) | 11/24 공개. 이미지 초해상도(Super-Resolution) 모델(MIT) |
| [apple/DepthPro2](https://hf.co/apple/DepthPro2) | 단안(monocular) 메트릭 깊이와 비디오 깊이를 추정한다. |

---

## 3. 주목할 기술·프레임워크

1. **에이전트 스킬 생태계**: superpowers, stitch-skills, cursor/plugins를 보면 스킬 포맷이 사실상 표준이 되어 가고 있고, 벤더 간 호환도 확대되고 있다. → *이 레포의 `claude_skills/` 글을 업데이트할 만하다.*
2. **형식 검증 + AI 수학**: 10월에 준리만 가설(Quasi-Riemann), 11월에 리만 가설 형식 증명이 나왔다. Lean과 Mathlib이 "AI 출력 검증기" 역할을 맡기 시작했다.
3. **초저비트 온디바이스 LLM**: 27B급 모델을 삼진 양자화해 llama.cpp, Metal, CUDA에서 돌린다. 로컬 에이전트의 현실성이 높아지고 있다.
4. **통합 오디오·비디오 생성**: LTX-2.5와 MAGI-2 Preview(8월 공개, 114B MoE)처럼 텍스트·비디오·오디오 토큰을 하나의 시퀀스로 처리하는 구조가 대세다. *(일부 집계 사이트가 MAGI-2를 "어제 출시"로 소개했지만, 실제 출시일은 2026-08-05다.)*
5. **사이버 보안 특화 모델 변형**: GPT-6.2는 Preparedness의 "Critical" 사이버 임계치에 도달했다고 밝혔다. Gemini 4 Neon은 방어자 전용 "for cyber" 변형을 내놨다. 보안 기능을 따로 떼어 내는 흐름이 뚜렷하다.

---

## 4. 최근 24시간 주요 뉴스 (11/27~28)

| 뉴스 | 내용 | 신뢰도 |
|---|---|---|
| **AI 리만 가설 증명 후속 보도** | Anthropic 소속 수학자 Levent Alpöge가 11/20 Lean 형식 증명을 공개했고, 11/21 Lean FRO·Mathlib이 검증했다. 일반화 리만 가설(Dirichlet L-함수)까지 포함한다. 사람이 읽을 수 있는 설명이 없다는 점이 논쟁거리다. | ✅ [Scientific American](https://www.scientificamerican.com/article/the-ai-riemann-hypothesis-proof-is-almost-certainly-true-independent-mathematicians-attest/) · [Science](https://www.science.org/content/article/ai-may-have-solved-math-s-greatest-mystery-can-humans-understand-answer) |
| **Anthropic IPO 이후** | 11/18 공모가 $83(목표 범위 $70~78 상회), 공모액 $813억으로 역대 최대다. 11/19 나스닥(티커 ANT) 첫날 +17%로 마감했다. 이후 '매도세'와 Nasdaq-100 편입 보도가 나왔다. | ✅ [CNN](https://www.cnn.com/2026/11/18/investing/anthropic-ipo-price-stock) · ⚠️ [Crypto Briefing](https://cryptobriefing.com/anthropic-nasdaq-100-inclusion-qqq) |
| **Nvidia, 중국향 H200 출하 중단 + 미국 동남아 라이선스 규제** | 임시 CEO Colette Kress가 실적 발표에서 밝혔다. 미국은 인도네시아·말레이시아·싱가포르·태국·브라질로 가는 첨단 칩에 라이선스를 의무화했다. Jensen Huang 사임(Megaspeed 조사)과 맞물린 사안이다. *"Nvidia가 동남아 4개국 서버 출하를 중단했다"는 집계 보도는 ❌ 확인되지 않았다.* | ✅ [Fox Business](https://www.foxbusiness.com/fox-news-tech/nvidia-halts-china-ai-chip-shipments-despite-us-approval) · [Al Jazeera](https://aljazeera.com/economy/2026/11/17/us-moves-to-block-chinas-remote-access-to-ai-chips-amid-nvidia-scandal) · [SCMP](https://scmp.com/week-asia/economics/article/3374665/singapore-seeks-us-talks-ai-chip-export-rules-amid-nvidia-fallout-megaspeed-probe) |
| **FCC, SpaceX 위성 100만 기 승인 (우주 AI 데이터센터)** | 우주 기반 AI 데이터센터 구상에 쓰일 위성 배치를 승인했다는 보도다. | ⚠️ [Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-27-2026-ai-infrastructure) |
| **캐나다, AI 컴퓨트 기금 7억 달러 증액** | Evan Solomon 장관이 발표했다. 중소 조직의 AI 제품 개발을 지원한다. | ⚠️ [Rio Rundown](https://riorundown.substack.com/p/ai-news-nov-27-2026-ai-infrastructure) |
| **Apple, MiniMax의 'Talkie' 앱 전 세계 삭제** | AI 캐릭터가 미성년자에게 성적 메시지를 보냈다는 보도 이후 조치다. | ⚠️ [ExplainX](https://explainx.ai/catch-up-on-ai/2026-11-27) |
| **Z.ai GLM-5.5 지연 / GLM-5.4 출시** | Reuters 보도를 인용해, 미국 규제와 증류 차단 때문에 2027년 1분기 이후로 밀릴 수 있다고 전했다. | ⚠️ (Reuters 원문 미확인) |
| **DeepSeek `deepseek-v4-pro-0813` 등재** | 모델 집계 사이트에 11/27 날짜로 올라왔다. | ⚠️ [LLM Gateway](https://llmgateway.io/timeline) |
| **Google Research, DeepCrossAttention** | 파라미터를 소폭 늘리는 대신 동일 품질을 최대 3배 빠르게 달성한다고 한다. | ⚠️ [AI News Digest](https://aienews.org/digest/2026-11-28/) |
| **케냐 개인정보 규제기관: 결제 에이전트에 "문서화된 사람 승인" 요구** | 돈을 송금할 수 있는 AI 에이전트에 대한 첫 규제 사례 중 하나다. | ⚠️ [AI News Digest](https://aienews.org/digest/2026-11-28/) |

### 이번 주 맥락 (11월 중순 출시 모델)
- **Claude Fable 5.2 / Mythos 5.2** (11/9): FrontierCode 2.0에서 49.1%를 기록했다(Opus 5.5는 45.5%). [SD Times](https://sdtimes.com/ai/anthropic-introduces-claude-fable-5-2-mythos-5-2/)
- **GPT-6.2 Astra / Sol** (11/17): Astra 가격은 입력 100만 토큰당 $8, 출력 $40이다. 독립 평가에서는 Fable 5.2에 이어 2위다. [OpenAI](https://openai.com/index/introducing-gpt-6-2-astra-sol) · [Decrypt](https://decrypt.co/383488/openai-gpt-6-2-astra-challenges-anthropic-price-but-not-every-benchmark)
- **Gemini 4 Neon** (11/18): 가격은 $3/$15, 컨텍스트 1M이다. Artificial Analysis 지수 3위다. [Google Blog](https://blog.google/innovation-and-ai/models-and-research/gemini-models/introducing-gemini-4-neon/)
- **Kimi K3.1 Pro Prime** (11/20), **Qwen4-Max** (11/16) ⚠️

---

## 5. 정정·미확인 항목

- "OpenAI가 Apple에 맞소송(countersuit)을 냈다"는 집계 보도는 ❌. 확인되는 것은 8월의 기각 신청(motion to dismiss)과 공개 반박뿐이다. [Axios](https://www.axios.com/2026/08/06/openai-apple-motion-to-dismiss)
- "Google이 Workspace 에이전트의 MCP 이전 마감을 정했다"는 보도는 ❌. 확인되는 것은 5월 MCP 서버 프리뷰와 쿼터 변경 공지뿐이다. [Google Workspace Updates](https://workspaceupdates.googleblog.com/2026/05/agent-tools-and-security-updates-for-workspace-developers.html)
- MAGI-2 Preview는 신규 출시가 아니다(2026-08-05 출시).

---

### 조사 메모
- 이 세션의 네트워크 정책상 `news.ycombinator.com`, `huggingface.co`(웹), `theneuron.ai`, `ai.info`에 직접 접속할 수 없었다. GitHub 트렌딩과 HF Hub(MCP)는 직접 조회했고, 나머지는 웹 검색 결과를 교차 확인했다.
