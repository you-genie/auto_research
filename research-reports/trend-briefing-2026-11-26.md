# 데일리 트렌드 브리핑 — 2026-11-26 (목)

> 자동 리서치 루틴 산출물입니다. 출처는 대부분 뉴스 애그리게이터·2차 보도라서, 1차 출처로 확인이 안 된 항목은 **⚠️ 미확인**으로 표시했습니다.
> 표기 규칙: **한글 용어 (English 원문, [영어 발음])**

---

## 🔑 한 줄 요약

**이번 주 개발자에게 가장 중요한 소식은 보안 사고입니다.** Microsoft의 공식 **에이전트 프레임워크 (Agent Framework, [에이전트 프레임워크])** PyPI 패키지 1.26.1/1.26.2 버전에 **자격증명 탈취 악성코드 (Credential Stealer, [크리덴셜 스틸러])**가 들어 있었습니다. 모델 쪽에서는 Thinking Machines의 오픈 웨이트 모델 **Inkling 2 Mini ([잉클링 투 미니])**가 Hugging Face 트렌딩 1위를 차지했습니다.

---

## 1. 트렌딩 키워드 & 토픽

| 키워드 (원문, [발음]) | 설명 |
|---|---|
| **공급망 공격 (Supply Chain Attack, [서플라이 체인 어택])** | 공식 패키지 계정이 탈취되어 악성 버전이 배포되는 공격입니다. 이번 주 Microsoft agent-framework 사건으로 AI 에이전트 SDK가 새로운 공격 대상이 되었습니다. |
| **`.pth` 후킹 (.pth Hook, [닷 피티에이치 훅])** | 파이썬 site-packages 안의 `.pth` 파일은 인터프리터가 시작될 때 자동으로 실행됩니다. 따라서 패키지를 **import하지 않아도** 악성코드가 실행됩니다. |
| **비공개 추론 (Private Inference, [프라이빗 인퍼런스])** | 기밀 컴퓨팅 (Confidential Computing, [컨피덴셜 컴퓨팅])을 이용해 모델 제공사도 프롬프트를 볼 수 없게 하는 기술입니다. OpenAI는 이를 "Private Intelligence" 묶음의 프리뷰로 제공하고 있습니다. |
| **루프드 트랜스포머 (Looped Transformer, [룹트 트랜스포머])** | 같은 레이어 블록을 여러 번 반복 통과시켜 파라미터 수 대비 추론 깊이를 늘리는 구조입니다. Inkling 2 Mini가 이 구조를 씁니다. |
| **3진 양자화 (Ternary Quantization, [터너리 퀀타이제이션])** | 가중치를 {-1, 0, +1} 세 값으로만 표현하는 양자화 방식으로, 약 1.58~2비트에 해당합니다. 27B 모델을 기기에서 직접 실행하는 사례가 등장했습니다. |
| **에이전트 메모리 (Agent Memory, [에이전트 메모리])** / **에이전트 스킬 (Agent Skill, [에이전트 스킬])** | GitHub 트렌딩 상위권이 모델보다는 에이전트용 인프라(메모리·스크래핑·스킬)로 채워지는 흐름이 이어지고 있습니다. |
| **AI 수학 연구 (AI for Math, [에이아이 포 매쓰])** | Google·Meta 등이 멀티에이전트로 미해결 수학 문제를 풀고 Lean으로 검증한 결과를 연이어 발표하고 있습니다. |

---

## 2. 주목할 GitHub 저장소 / 프로젝트

출처는 2026-11-25 agents-radar 일일 리포트와 GitHub Explore입니다. 스타 수는 대략적인 값입니다.

| 저장소 | 언어 | 지표 | 한 줄 설명 |
|---|---|---|---|
| [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl) | TS | **+991 ⭐/일** | 에이전트용 **웹 스크래핑 (Web Scraping, [웹 스크레이핑])**·검색 API입니다. 550개 이상의 데이터 제공원을 하나의 API로 제공합니다. |
| [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill) | Python | +703 ⭐/일 | 여러 플랫폼에서 최근 30일 동향을 모아 요약하는 에이전트 스킬입니다. 이 루틴과 같은 용도라서 참고할 만합니다. |
| [jingyaogong/minimind](https://github.com/jingyaogong/minimind) | Python | 70.4K ⭐, +727/일 | 64M 파라미터 LLM을 약 2시간 만에 **처음부터 학습 (From Scratch, [프롬 스크래치])**하는 교육용 프레임워크입니다. |
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | Python | 69.4K ⭐ | 에이전트의 **장기 기억 계층 (Memory Layer, [메모리 레이어])**입니다. |
| [infiniflow/ragflow](https://github.com/infiniflow/ragflow) | Go | 94.7K ⭐ | **RAG ([래그], Retrieval-Augmented Generation)** 엔진입니다. |
| [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach) | Python | 114.6K ⭐ | 여러 플랫폼을 탐색하는 범용 수집용 CLI 에이전트입니다. |
| [obra/superpowers](https://github.com/obra/superpowers) | — | Explore 트렌딩 | 코딩 에이전트용 **스킬 프레임워크 (Skills Framework)**입니다. |
| [openvinotoolkit/openvino](https://github.com/openvinotoolkit/openvino) | C++ | +185 ⭐/일 | Intel의 추론 최적화·배포 툴킷입니다. |

**흐름 해석:** 이번 주에도 트렌딩 상위권은 *모델*보다 *에이전트가 쓰는 도구*(데이터 수집, 메모리, 스킬)가 차지했습니다.

---

## 3. 떠오르는 기술 / 모니터링할 프레임워크·모델 (Hugging Face 트렌딩 기준)

| 모델 | 특징 | 왜 볼 만한가 |
|---|---|---|
| [thinkingmachines/Inkling-2-Mini](https://hf.co/thinkingmachines/Inkling-2-Mini) | 이미지+텍스트 입력 **MoE ([엠오이], Mixture of Experts)**에 루프드 트랜스포머 구조, **Apache-2.0** 라이선스. 11/17에 공개됐습니다. | HF 트렌딩 1위(좋아요 약 6.2K)입니다. Unsloth GGUF 변환본 다운로드가 240만 회를 넘었습니다. 미국산 오픈 웨이트 모델의 대표 주자로 자리잡는 중입니다. |
| [prism-ml/Ternary-Bonsai-2.5-27B-GGUF](https://hf.co/prism-ml/Ternary-Bonsai-2.5-27B-GGUF) | Qwen3.8-27B를 **3진(2비트급) 양자화**했고 MTP·투기적 디코딩 (Speculative Decoding, [스펙큘러티브 디코딩])을 지원합니다. 11/24에 공개됐습니다. | 27B급 에이전트·툴 호출 모델을 노트북이나 Mac에서 실행할 수 있습니다. **온디바이스 (On-device, [온디바이스])** 흐름에서 눈여겨볼 모델입니다. |
| [inclusionAI/Ling-3.2-air](https://hf.co/inclusionAI/Ling-3.2-air) | MoE 기반 비전-언어 모델로 FP8, MIT 라이선스입니다. 11/23에 공개됐습니다. | 중국계 오픈 MoE 라인업의 신규 모델입니다. |
| [inworld/voice-isolator](https://hf.co/inworld/voice-isolator) | 48kHz 실시간 **음성 분리 (Voice Isolation, [보이스 아이솔레이션])** 모델로 Apache-2.0 라이선스입니다. | 음성 에이전트 파이프라인의 전처리용으로 바로 쓸 수 있습니다. |
| [apple/DepthPro2](https://hf.co/apple/DepthPro2) | 단안 메트릭·비디오 **깊이 추정 (Depth Estimation, [뎁스 에스티메이션])** 모델입니다. | 3D/AR, 3D 가우시안 스플래팅 쪽 연구와 연결됩니다. |
| [llamaindex/OCRia-nano-1](https://hf.co/llamaindex/OCRia-nano-1) | CPU에서 동작하는 ONNX 기반 문서 OCR로, PDF를 Markdown으로 변환합니다. | RAG 수집 단계의 비용을 줄일 수 있습니다. |

**이번 달 프런티어 모델 흐름 (애그리게이터 기준, ⚠️ 날짜는 개별 확인 필요):** OpenAI GPT-6.2 Astra/Sol (11/17), Google Gemini 4 Carbon·Hydrogen·Neon (11/10~18), Alibaba Qwen4-Max (11/16), Moonshot Kimi K3.1 Pro (11/20), Anthropic Fable 5.2 (11/9).

---

## 4. 지난 24시간 주요 뉴스

### 🚨 보안 — Microsoft `agent-framework` PyPI 패키지 오염 (확인됨, 여러 매체 교차 보도)
- **영향 버전:** `agent-framework` **1.26.1, 1.26.2** (11/17 배포, 약 45분~1시간 뒤 삭제). 마지막 정상 버전은 **1.26.0**입니다.
- **동작:** `.pth` 파일(1.26.2에서는 `af_runtime_diag.pth`)을 이용해 파이썬 시작 시 자동 실행되며, import하지 않아도 동작합니다. Azure 관리 ID, OIDC, CI/CD 토큰과 개발자 비밀값을 탈취합니다.
- **조치:** 해당 버전이 설치됐던 호스트·CI 러너에서 접근 가능한 **모든 자격증명을 교체 (Rotate, [로테이트])**하세요. 버전은 1.26.0으로 고정(pin)하고 환경을 다시 빌드해야 합니다.
- 링크: [BleepingComputer](https://bleepingcomputer.com/news/security/microsofts-agent-framework-pypi-package-compromised-to-steal-credentials) · [CSO Online](https://www.csoonline.com/article/4250156/attackers-hijack-microsofts-agent-framework-package-to-steal-azure-and-ci-credentials.html) · [Corgea 분석](https://corgea.com/research/microsoft-agent-framework-pypi-1-26-1-1-26-2-pth-credential-stealer-november-2026)

### 🤖 AI 기업·제품
- **OpenAI**: ChatGPT의 **Chat + Work 통합 화면**을 일부 Pro 사용자에게 시범 배포하고 있다고 보도됐습니다 (⚠️ 애그리게이터 보도). 엔터프라이즈용 **Private Intelligence**(ZDR + Private Safety Processing, Private Inference 프리뷰)도 함께 소개되고 있습니다. 다만 보안 연구자 Matthew Green은 "에이전트가 데이터를 읽고 메시지도 보낼 수 있다면 비공개 추론만으로는 보호가 안 된다"고 비판했습니다. → [VentureBeat](https://venturebeat.com/ai/openais-new-private-intelligence-targets-a-growing-enterprise-concern-who-can-see-your-ai-data/)
- **Anthropic**: Claude 대화를 라우팅하는 API 계층을 Python에서 **Rust ([러스트])**로 재작성해 한 리전에서 요청당 CPU 사용량을 약 70% 줄였다고 보도됐습니다 (⚠️ 단일 출처). Claude Platform의 OpenTelemetry 내보내기 대상에 Databricks MLflow도 추가됐습니다.
- **Microsoft**: Azure DevOps용 GitHub Advanced Security에 **Agentic Autofix**(에이전트 기반 취약점 자동 수정) 퍼블릭 프리뷰를 공개했습니다 (11/24). → [Microsoft Dev Blogs](https://devblogs.microsoft.com/)
- **Apple**: 모든 개발자가 앱을 Siri AI와 연동할 수 있는 Developer Preview를 시작했습니다 (iOS 27.3 베타, 11/16). → [Apple Developer News](https://developer.apple.com/news/)

### 🔬 연구
- **Google Research "Teamwork"**: 멀티에이전트로 얻은 수학 결과 7건을 발표했습니다(11/13 블로그). Lean으로 검증한 Knuth 증명이 포함됩니다. 일부 뉴스레터에 나온 "하루에 논문 6편"이라는 수치는 확인되지 않았습니다. → [Magica 요약](https://magica.com/news/google-teamwork-seven-math-results-verification-cost)

### ⚖️ 정책·시장 (⚠️ 사실 확인 결과 주의)
- "**FCC가 SpaceX의 100만 기 AI 데이터센터 위성을 승인했다**"는 애그리게이터 보도가 있지만, 확인된 가장 최근 보도(10월)는 *접수(filing accepted)만 됐고 아직 승인되지 않았다*는 내용입니다. FCC 기록(SAT-LOA-20260108-00016)을 직접 확인해야 합니다. → [Decrypt](https://decrypt.co/357024/fcc-review-musk-spacex-plan-orbital-ai-data-centers)
- "**뉴욕주 AI 챗봇 장난감 5년 판매 금지법 서명**" 보도도 있지만 확인되지 않았습니다. 확인된 것은 10/28에 서명된 *미성년자 대상 위험 챗봇 기능 금지법*과 *베이비 모니터 보안법*입니다. 장난감 금지 법안(S9408A)은 서명 대기 중으로 알려져 있습니다. → [NY 주지사실](https://www.governor.ny.gov/news/governor-hochul-signs-nation-leading-legislation-protect-kids-ai-chatbots-and-ensure-baby)
- 시장: "Anthropic 주가가 공모가 아래로 마감", "S&P가 Nvidia 등급 하향을 검토 중"이라는 단신이 있습니다 (⚠️ 단일 출처, 미확인).

---

## 출처
- [The Neuron — Nov 26, 2026](https://www.theneuron.ai/digest/everything-that-happened-in-ai-today-november-26-2026/) · [Sam on AI](https://samonai.substack.com/p/ai-brief-november-26-2026) · [DEV Community 일일 AI 뉴스](https://dev.to/trillioniar_s_14a3c313e14/daily-ai-news-nov-26-ai-solves-math-while-the-bill-comes-due-29l6)
- [agents-radar #530 (2026-11-25)](https://github.com/yaojiejia/agents-radar/issues/530) · [GitHub Explore](https://github.com/explore)
- [LLM Gateway 타임라인](https://llmgateway.io/timeline) · [tecadmin 11월 모델 정리](https://tecadmin.net/november-2026-ai-model-releases/)
- Hugging Face Hub 트렌딩 (2026-11-26 조회)
- 보안: BleepingComputer, CSO Online, Help Net Security, Corgea
- 사실 확인: Decrypt, Bloomberg, NY Governor's Office, VentureBeat, Magica
