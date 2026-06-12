# DiffusionGemma: 구글이 꺼낸 비밀 병기 — 텍스트도 이제 "뿌려서" 만든다

> 📊 **발표자료**: [diffusion-gemma-presentation.pptx](./diffusion-gemma-presentation.pptx)

> "DiffusionGemma prioritizes speed and parallel layout generation. Its overall output quality is lower than standard Gemma 4."  
> — Google DeepMind, DiffusionGemma 모델 카드, 2026년 6월

네, 구글이 직접 "우리 모델이 느리다"는 걸 인정하면서도 새 모델을 냈어요. 그 이유가 뭔지, 오늘 같이 파헤쳐 보죠.

---

## 1. 잠깐, "Diffusion Gemma"가 뭐야? — 사실 확인부터

이 글을 읽기 전에 아마 이런 질문이 생겼을 거예요. "Diffusion Gemma? 이미지 생성 모델이야? Gemma 4랑 다른 거야?"

결론부터 말하자면:
- **DiffusionGemma**는 **텍스트 생성** 모델이에요. 이미지/영상은 입력으로 받을 수 있지만, 출력은 오직 텍스트입니다.
- **Gemma 4 기반** Mixture-of-Experts 아키텍처 위에 올려진 확장 모델이에요.
- **2026년 6월 10일** 구글 AI가 공식 발표하고 오픈소스로 공개했어요.
- "Gemma Diffusion"이 아니라 "[DiffusionGemma](https://ai.google.dev/gemma/docs/diffusiongemma)"가 공식 명칭이에요.

그리고 이거랑 혼동하기 쉬운 **Gemini Diffusion**이 따로 있는데요. 이건 2025년 5월 Google I/O에서 발표된 **리서치 데모** 수준의 프로젝트로, 아직 일반 공개는 되지 않았어요. DiffusionGemma는 그 기술 계보를 이어받아 **실제로 쓸 수 있는 오픈 모델**로 만든 거죠.

| 구분 | Gemini Diffusion | DiffusionGemma |
|------|-----------------|---------------|
| 발표 시기 | 2025년 5월 (Google I/O) | 2026년 6월 10일 |
| 공개 여부 | 대기자 명단 (실험적) | 오픈소스 (Apache 2.0) |
| 기반 모델 | Gemini 계열 | Gemma 4 26B MoE |
| 주요 용도 | 연구 데모 | 로컬/클라우드 배포 |

---

## 2. 배경: AR 모델의 "한 글자씩 쓰기" 문제

기존 LLM이 텍스트를 만드는 방식을 상상해 볼게요. ChatGPT든 Gemma든 다 똑같아요.

```
"안" → "안녕" → "안녕하" → "안녕하세" → "안녕하세요"
```

이걸 **Autoregressive(AR, 자기회귀)** 방식이라고 해요. 토큰 하나 예측 → 다음 토큰 예측... 이 과정을 끝날 때까지 반복하는 거죠.

### AR 방식의 고질적 문제: "메모리 병목"

[Google AI 공식 문서](https://ai.google.dev/gemma/docs/diffusiongemma/explained)에서는 이렇게 설명해요:

> "Most of the generation time is spent loading model weights from hardware memory into the processing units, rather than performing the actual mathematical calculations."
> 
> 생성 시간의 대부분이 실제 계산이 아니라 **모델 가중치를 메모리에서 불러오는 데** 쓰인다.

즉, GPU가 "연산을 못 해서" 느린 게 아니라, "매 스텝마다 수십 GB짜리 가중치를 다시 불러야 해서" 느린 거예요. 이게 바로 AR 모델의 **메모리 바운드(memory-bound)** 문제입니다.

해결책은 뭘까요? **한 번에 여러 토큰을 동시에 처리하면** 가중치 로딩 횟수를 줄일 수 있겠죠. 그래서 등장한 게 **Diffusion LLM**이에요.

---

## 3. 디퓨전 LLM 생태계 — DiffusionGemma 이전에 뭐가 있었나

사실 DiffusionGemma가 처음은 아니에요. 텍스트 디퓨전 모델은 꽤 오래 연구돼 왔거든요.

### 선행 연구들

**MDLM (Masked Diffusion Language Model)**  
마스크 토큰(`[MASK]`)으로 텍스트를 오염시키고, 이걸 복원하는 방식을 학습해요. BERT의 MLM 방식과 비슷하지만 생성 모델로 확장한 거죠. 이 방식이 나중에 나올 LLaDA의 기반이 돼요.

**SEDD (Score Entropy Discrete Diffusion)**  
이산 공간(discrete space)에서의 디퓨전에 수학적으로 올바른 스코어 함수를 정의했어요. 연속 이미지 디퓨전의 "score matching"을 텍스트에 맞게 가져온 거죠.

**[LLaDA (Large Language Diffusion with mAsking)](https://arxiv.org/abs/2502.09992)**  
2025년 발표된 8B 규모의 마스크 디퓨전 모델이에요. LLaMA 3 8B와 비슷한 성능을 보여주면서 "디퓨전 LLM도 스케일 업되면 AR 모델이랑 경쟁할 수 있다"는 걸 처음으로 증명했어요. 학습 데이터는 2.3조 토큰인데, LLaMA 3의 15조 토큰의 약 15% 수준이에요. 놀랍죠?

**[Mercury (Inception Labs)](https://www.inceptionlabs.ai/blog/introducing-mercury)**  
2025년 초 세계 최초 **상업용** 디퓨전 LLM으로 출시됐어요. Mercury 2는 2026년 2월 발표됐는데, NVIDIA H100 단일 GPU에서 초당 1,000+ 토큰을 달성하며 Claude 4.5 Haiku Reasoning(~89 tok/s)보다 **10배 이상 빠른** 속도를 보였어요.

**[Gemini Diffusion (Google DeepMind)](https://deepmind.google/models/gemini-diffusion/)**  
2025년 5월 Google I/O에서 공개된 연구 프로토타입이에요. 초당 1,479 토큰이라는 속도를 데모로 보여줬지만, 여전히 실험적 상태예요.

그리고 이 모든 흐름의 결실이 바로 **DiffusionGemma**인 거죠.

---

## 4. DiffusionGemma의 핵심 기술 — "뿌리고 정제한다"

### 4.1 Uniform State Diffusion (USD)

DiffusionGemma가 사용하는 방식은 **Uniform State Diffusion**이에요. 기존의 마스크 디퓨전이 `[MASK]` 토큰만 쓰는 것과 달리, USD는 **랜덤한 실제 토큰**으로 노이즈를 만들어요.

과정을 그림으로 상상해 볼게요:

```
[초기 상태]  →  와/뇨/믒/를/킫/아/툽/니  (256개 랜덤 토큰)
[스텝 10]   →  안녕/뇨/하세요/를/킫/아/합니다  (일부 확정)
[스텝 30]   →  안녕하세요/저는/킫/AI/입니다  (많이 확정)
[최종]       →  안녕하세요 저는 AI입니다  (완성)
```

핵심은 **낮은 확률 토큰을 "재노이징(re-noising)"** 할 수 있다는 점이에요:

> "If a token's probability drops below a threshold due to new context emerging in later steps, it is re-noised with a fresh random token."
> — [Google AI Developer Docs](https://ai.google.dev/gemma/docs/diffusiongemma/explained)

쉽게 말하면, 이미 "잠정 확정"된 토큰도 나중에 더 나은 맥락이 생기면 다시 바꿀 수 있어요. AR 모델은 한번 내뱉은 토큰을 돌릴 수 없는데, 이게 큰 차이죠.

### 4.2 블록-자기회귀 멀티-캔버스 샘플링

[vLLM 블로그](https://vllm.ai/blog/2026-06-10-diffusion-gemma)에서 설명하는 이 메커니즘, 이름이 좀 무겁지만 개념은 단순해요:

1. **캔버스(Canvas)** = 256개 토큰짜리 "작업판"
2. 256개 토큰을 **동시에** 처리해서 한 캔버스를 완성
3. 완성된 캔버스는 KV 캐시에 저장
4. 다음 캔버스를 새로 처리
5. 1,000토큰짜리 응답 = 4번의 캔버스 처리

이게 왜 빠르냐면, 256개 토큰을 한 번에 처리할 때 **GPU가 병렬 연산**을 풀로 쓸 수 있거든요. AR은 토큰 하나 처리할 때마다 가중치를 다시 불러야 하지만, USD는 256개를 한꺼번에 처리하니 가중치 로딩 횟수가 1/256로 줄어드는 거예요.

### 4.3 이중 어텐션 모드

[Hugging Face 모델 카드](https://huggingface.co/google/diffusiongemma-26B-A4B-it)에 따르면, 같은 Gemma 4 백본을 두 가지 모드로 사용해요:

| 모드 | 어텐션 유형 | 사용 시점 |
|------|-----------|---------|
| 인코더 모드 | 인과적 어텐션 (Causal) | 프롬프트 처리, 완성된 캔버스 저장 |
| 디노이저 모드 | 양방향 어텐션 (Bidirectional) | 캔버스 내 토큰 병렬 디노이징 |

이 양방향 어텐션이 핵심이에요. AR 모델은 왼쪽→오른쪽만 볼 수 있지만, 디노이저는 캔버스 내 **모든 위치를 동시에 참조**할 수 있어요. 덕분에 더 일관성 있는 텍스트 블록을 만들 수 있죠.

### 4.4 자기 컨디셔닝 (Self-Conditioning)

디노이징의 각 스텝에서 이전 스텝의 예측 확률 분포를 다음 스텝에 넘겨줘요. 즉, 이전에 "이 위치엔 '안녕'이 적절할 것 같았어"라는 기억을 갖고 다음 스텝을 수행해요. 이게 수렴 속도를 높여주는 역할을 해요.

---

## 5. 스펙 정리 — DiffusionGemma가 뭘 갖고 있나

[공식 모델 카드](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)에서 확인한 스펙이에요:

| 항목 | 사양 |
|------|------|
| 총 파라미터 수 | 25.2B |
| 활성 파라미터 수 | 3.8B |
| 아키텍처 | MoE (전문가 128개, 활성 8개 + 공유 1개) |
| 레이어 수 | 30 |
| 컨텍스트 길이 | 최대 256K 토큰 |
| 캔버스 크기 | 256 토큰 |
| 어휘 크기 | 262K |
| 비전 인코더 | ~550M 파라미터 |
| 지원 언어 | 35개 이상 |
| 라이선스 | Apache 2.0 |

**지원 입력 모달리티:** 텍스트, 이미지 (가변 해상도), 영상 (최대 60초)  
**출력:** 텍스트 전용

**배포 플랫폼:** Hugging Face, Kaggle, Google Vertex AI, vLLM, SGLang, MLX, Unsloth, NVIDIA NIM

---

## 6. 성능 벤치마크 — 얼마나 빠르고, 얼마나 잘 하나

### 6.1 속도: 정말 4배 빠른가?

[MarkTechPost 리뷰](https://www.marktechpost.com/2026/06/10/google-ai-releases-diffusiongemma-a-26b-moe-open-model-using-text-diffusion-for-up-to-4x-faster-generation/)에서 확인한 속도 수치예요:

| 하드웨어 | 속도 |
|---------|------|
| NVIDIA H200 (FP8 양자화) | 1,288 tokens/sec |
| NVIDIA H100 | 1,000+ tokens/sec |
| NVIDIA GeForce RTX 5090 | 700+ tokens/sec |

[vLLM 블로그](https://vllm-project.github.io/2026/06/10/diffusion-gemma)에서는 AR 베이스라인 대비 **5~6배** 빠르고, Multi-Token Prediction 방식 대비 **2.6~3배** 빠르다고 밝혔어요.

"4배 빠르다"는 공식 수치는 단일 유저 로컬 환경에서의 측정이에요. 다수 유저가 동시에 요청하는 서빙 환경에서는 이 이점이 줄어들 수 있어요. 이 부분은 솔직히 아직 검증이 더 필요한 영역이에요.

### 6.2 품질: 기존 Gemma 4 대비 어떤가?

이게 핵심 트레이드오프예요. 구글이 직접 밝힌 벤치마크를 보면:

| 벤치마크 | DiffusionGemma | Gemma 4 26B |
|---------|---------------|------------|
| MMLU Pro | 77.6% | 82.6% |
| GPQA Diamond | 73.2% | 82.3% |
| AIME 2026 | 69.1% | 88.3% |
| LiveCodeBench v6 | 69.1% | 77.1% |
| BigBench Extra Hard | 47.6% | 64.8% |
| MATH-Vision | 70.5% | 82.4% |
| MMMU Pro (Vision) | 54.3% | 73.8% |

수학/추론 중심 태스크에서 약 10~20% 포인트 뒤처지는 모습이에요. 특히 AIME 같은 하드 추론 벤치마크에서 차이가 크게 나죠.

반면 코딩이나 구조화된 작업은 상대적으로 격차가 작아요. 이건 "연속적 추론 체인"이 필요 없는 태스크에서 디퓨전 방식이 더 잘 버틴다는 걸 보여주는 거예요.

### 6.3 디퓨전 LLM 전체 비교

| 모델 | 속도 (tok/s, H100) | 공개 여부 | 기반 |
|------|-------------------|----------|------|
| **DiffusionGemma** | 1,000+ | 오픈소스 (Apache 2.0) | Gemma 4 26B MoE |
| Mercury 2 | 1,009 | 상업 API | 독자 아키텍처 |
| Gemini Diffusion | ~1,479 (데모) | 실험적 (비공개) | Gemini 계열 |
| LLaDA 8B | ~5× AR 대비 빠름 | 연구 오픈소스 | 처음부터 학습 |

---

## 7. 실제로 어떻게 쓸 수 있나

### 하드웨어 요구사항

[공식 문서](https://ai.google.dev/gemma/docs/diffusiongemma)에 따르면, 양자화 시 **18GB VRAM**으로 구동 가능해요. RTX 4090(24GB), RTX 3090(24GB) 같은 고사양 컨슈머 GPU에서도 돌아가는 거죠.

### vLLM으로 서빙하기

```bash
vllm serve google/diffusiongemma-26B-A4B-it \
  --max-model-len 262144 \
  --max-num-seqs 4 \
  --gpu-memory-utilization 0.85 \
  --attention-backend TRITON_ATTN \
  --hf-overrides '{"diffusion_sampler": "entropy_bound", "diffusion_entropy_bound": 0.1}' \
  --diffusion-config '{"canvas_length": 256}'
```

### Hugging Face Transformers로 로컬 사용

```python
from transformers import AutoProcessor, DiffusionGemmaForBlockDiffusion

model = DiffusionGemmaForBlockDiffusion.from_pretrained(
    "google/diffusiongemma-26B-A4B-it"
)
processor = AutoProcessor.from_pretrained(
    "google/diffusiongemma-26B-A4B-it"
)
```

### 주요 추론 파라미터

| 파라미터 | 기본값 | 의미 |
|---------|-------|------|
| `canvas_length` | 256 | 병렬 처리 토큰 블록 크기 |
| `max_denoising_steps` | 48 | 캔버스당 최대 디노이징 스텝 |
| `temperature_schedule` | 0.8 → 0.4 | 초기(탐색) → 후기(확정) 온도 |
| `entropy_threshold` | 0.005 | 조기 종료 엔트로피 기준 |
| `entropy_bound` | 0.1 | 토큰 확정 엔트로피 한계 |

---

## 8. 한계점 — 솔직히 아직 이런 게 아쉬워요

1. **추론 집약적 태스크에서 품질 격차**: 수학, 다단계 논리 추론에서 AR 모델 대비 10~20%p 뒤처져요. "빠르지만 덜 똑똑한" 모델이에요.

2. **다중 사용자 서빙 환경에서의 한계**: DiffusionGemma는 단일 사용자 환경에서 compute-bound로 빠르지만, 많은 요청이 동시에 들어오는 클라우드 서빙 환경에서는 이 속도 이점이 줄어들어요. ([공식 문서](https://ai.google.dev/gemma/docs/diffusiongemma/explained))

3. **미묘한 언어 표현 취약**: 사르카즘, 비유적 표현, 문화적 뉘앙스 처리에 어려움이 있어요.

4. **오디오 미지원**: 텍스트/이미지/영상 입력은 되지만, 오디오는 아직 미지원이에요.

5. **파인튜닝 도구 체인 미성숙**: 공식 파인튜닝은 JAX 기반 Hackable Diffusion 툴박스로 가능하지만, LoRA 같은 경량 파인튜닝 생태계는 아직 초기 단계예요.

6. **순차 캔버스의 긴 컨텍스트 제한**: 256토큰씩 블록 처리하기 때문에 매우 긴 텍스트에서는 블록 간 일관성 유지가 어려울 수 있어요.

---

## 9. 향후 전망 — 디퓨전 LLM은 어디로 가나

디퓨전 LLM 생태계는 지금 굉장히 빠르게 발전 중이에요. 몇 가지 주목할 방향이 있어요:

### 하이브리드 접근법
[Gemini Diffusion](https://deepmind.google/models/gemini-diffusion/) 방식처럼, 디퓨전 초안을 AR이 교정하는 하이브리드 모델이 품질과 속도의 최적 균형을 찾을 수 있어요.

### 에이전틱 AI에서의 활용
초당 1,000+ 토큰 속도는 AI 에이전트가 여러 LLM 호출을 연속으로 수행하는 시나리오에서 엄청난 이점이 돼요. 코드 완성, 다단계 추론 에이전트 등에서 디퓨전 LLM의 역할이 커질 거예요.

### 추론 성능 개선
[Mercury 2](https://www.businesswire.com/news/home/20260224034496/en/Inception-Launches-Mercury-2-the-Fastest-Reasoning-LLM-5x-Faster-Than-Leading-Speed-Optimized-LLMs-with-Dramatically-Lower-Inference-Cost)가 AIME 91.1점을 달성한 것처럼, 디퓨전 LLM의 추론 능력도 빠르게 따라잡고 있어요. DiffusionGemma도 이 부분에서 개선이 이뤄질 것으로 기대돼요.

### 더 큰 캔버스, 더 스마트한 스케줄링
256토큰 캔버스 크기를 늘리거나, 태스크에 따라 최적의 디노이징 스텝 수를 동적으로 조절하는 연구가 진행 중이에요. 단순한 코딩 태스크에서는 스텝 수를 확 줄여 더 빠른 속도를 낼 수 있거든요.

---

## 마무리: "이미지 디퓨전이 텍스트에도 온다"

Stable Diffusion이 이미지 생성을 바꿔놓은 것처럼, 텍스트 디퓨전이 LLM 추론 방식을 바꾸려 하고 있어요. DiffusionGemma는 그 첫 번째 "실제로 쓸 수 있는 오픈소스" 모델이에요.

아직 품질 격차가 있고 생태계도 초기 단계지만, "속도가 필요한 곳"에서는 지금 당장 의미 있는 선택지가 됐어요. 특히 Apache 2.0 라이선스로 완전 오픈되어 있으니, 로컬 배포나 커스텀 파인튜닝을 고려 중이라면 지금 바로 시도해볼 만하죠.

다음 세대 LLM은 "한 글자씩 말하는 모델"이 아니라 "생각을 한꺼번에 뿌려서 정제하는 모델"이 될 수도 있어요. 그 변화의 한 챕터가 지금 열리고 있어요.

---

## 참고문헌

1. [DiffusionGemma 공식 문서 — Google AI for Developers](https://ai.google.dev/gemma/docs/diffusiongemma)
2. [Diffusion in Text Generation Explained — Google AI for Developers](https://ai.google.dev/gemma/docs/diffusiongemma/explained)
3. [DiffusionGemma Model Card — Google AI for Developers](https://ai.google.dev/gemma/docs/diffusiongemma/model_card)
4. [DiffusionGemma 26B-A4B-it — Hugging Face](https://huggingface.co/google/diffusiongemma-26B-A4B-it)
5. [DiffusionGemma: The Developer Guide — Google Developers Blog](https://developers.googleblog.com/diffusiongemma-the-developer-guide/)
6. [DiffusionGemma: The First Diffusion LLM Natively Supported in vLLM — vLLM Blog](https://vllm.ai/blog/2026-06-10-diffusion-gemma)
7. [Google AI Releases DiffusionGemma — MarkTechPost](https://www.marktechpost.com/2026/06/10/google-ai-releases-diffusiongemma-a-26b-moe-open-model-using-text-diffusion-for-up-to-4x-faster-generation/)
8. [A Visual Guide to DiffusionGemma — Maarten Grootendorst Newsletter](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-diffusiongemma)
9. [Gemini Diffusion — Google DeepMind](https://deepmind.google/models/gemini-diffusion/)
10. [Gemini Diffusion Blog Post — Google DeepMind](https://blog.google/technology/google-deepmind/gemini-diffusion/)
11. [Large Language Diffusion Models (LLaDA) — arXiv:2502.09992](https://arxiv.org/abs/2502.09992)
12. [Introducing Mercury — Inception Labs](https://www.inceptionlabs.ai/blog/introducing-mercury)
13. [Mercury 2 Launch — BusinessWire](https://www.businesswire.com/news/home/20260224034496/en/Inception-Launches-Mercury-2-the-Fastest-Reasoning-LLM-5x-Faster-Than-Leading-Speed-Optimized-LLMs-with-Dramatically-Lower-Inference-Cost)
14. [Diffusion LLMs in 2026 — Masturbyte](https://masturbyte.com/diffusion-llms.html)

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. 기존 AR(자기회귀) 모델이 느린 진짜 이유는 뭘까요? GPU의 연산 능력이 부족해서일까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 아니에요. 연산이 아니라 매 토큰마다 모델 가중치를 메모리에서 불러오는 데 대부분의 시간이 쓰이는 "메모리 바운드(memory-bound)" 문제 때문이에요.

**해설**: AR 모델은 토큰 하나를 예측할 때마다 수십 GB짜리 가중치를 다시 로딩해야 하죠. 그래서 GPU가 계산을 못 해서가 아니라 데이터를 나르느라 느린 거예요. 디퓨전 방식은 256개 토큰을 한 번에 처리해서 가중치 로딩 횟수를 확 줄이는 게 핵심이에요.

</details>

**Q2. OX 퀴즈! DiffusionGemma는 텍스트뿐 아니라 이미지도 생성할 수 있다. (O/X)**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X

**해설**: 이름에 "Diffusion"이 들어가서 이미지 생성 모델로 오해하기 쉬운데, DiffusionGemma는 텍스트 생성 모델이에요. 이미지나 영상(최대 60초)을 입력으로 받을 수는 있지만, 출력은 오직 텍스트뿐이죠. 오디오는 입력도 아직 미지원이에요.

</details>

**Q3. Gemini Diffusion과 DiffusionGemma, 둘은 뭐가 다를까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: Gemini Diffusion은 2025년 5월 Google I/O에서 공개된 비공개 리서치 데모이고, DiffusionGemma는 그 기술 계보를 이어받아 Apache 2.0 라이선스로 누구나 쓸 수 있게 공개한 오픈소스 모델이에요.

**해설**: Gemini Diffusion은 대기자 명단으로만 접근 가능한 실험적 프로젝트였죠. 반면 DiffusionGemma는 Gemma 4 26B MoE를 기반으로 만들어져 Hugging Face, vLLM 등에서 바로 받아 로컬이나 클라우드에 배포할 수 있어요. "실제로 쓸 수 있는 첫 오픈 디퓨전 LLM"이라는 게 핵심 차이예요.

</details>

**Q4. DiffusionGemma의 Uniform State Diffusion(USD)이 기존 마스크 디퓨전(MDLM, LLaDA 등)과 다른 점은 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 마스크 디퓨전은 `[MASK]` 토큰으로 텍스트를 오염시키지만, USD는 랜덤한 실제 토큰으로 노이즈를 만들어요. 게다가 한번 잠정 확정된 토큰도 확률이 낮아지면 다시 "재노이징(re-noising)"해서 바꿀 수 있죠.

**해설**: 이 재노이징 능력이 AR 모델과의 결정적 차이이기도 해요. AR 모델은 한번 내뱉은 토큰을 절대 되돌릴 수 없는데, USD는 나중 스텝에서 더 나은 맥락이 생기면 이미 정한 토큰도 고칠 수 있거든요. 덕분에 전체적으로 더 일관성 있는 텍스트를 만들 수 있어요.

</details>

**Q5. DiffusionGemma의 "캔버스(Canvas)"는 어떤 역할을 하고, 왜 속도 향상으로 이어질까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 캔버스는 256개 토큰짜리 작업판이에요. 캔버스 안의 토큰들을 동시에 디노이징하니까 가중치 로딩 횟수가 1/256로 줄어들고, GPU 병렬 연산을 풀로 활용할 수 있어 빨라지는 거예요.

**해설**: 완성된 캔버스는 KV 캐시에 저장하고 다음 캔버스로 넘어가는 "블록-자기회귀" 방식이죠. 그래서 1,000토큰짜리 응답이면 캔버스를 4번 처리하면 돼요. 다만 256토큰 블록 단위로 처리하다 보니 매우 긴 텍스트에서는 블록 간 일관성 유지가 어려울 수 있다는 한계도 있어요.

</details>

**Q6. DiffusionGemma는 인코더 모드와 디노이저 모드에서 서로 다른 어텐션을 써요. 각각 어떤 어텐션이고, 디노이저 쪽이 중요한 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 인코더 모드는 인과적(Causal) 어텐션, 디노이저 모드는 양방향(Bidirectional) 어텐션을 써요. 양방향 어텐션 덕분에 캔버스 내 모든 위치를 동시에 참조할 수 있어요.

**해설**: AR 모델은 왼쪽에서 오른쪽으로만 볼 수 있지만, 디노이저는 캔버스 안의 앞뒤 토큰을 전부 보면서 디노이징하죠. 같은 Gemma 4 백본 하나를 두 가지 모드로 돌려쓰는 구조인데, 프롬프트 처리와 완성된 캔버스 저장은 인코더 모드가, 토큰 병렬 디노이징은 디노이저 모드가 맡아요.

</details>

**Q7. 응용 문제! 여러분이 두 가지 서비스를 만든다고 해봐요. (A) 수학 올림피아드 문제 풀이 튜터, (B) 초당 수천 토큰을 쏟아내야 하는 코드 자동완성 에이전트. 각각 DiffusionGemma와 Gemma 4 중 어느 쪽이 더 적합할까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: (A) 수학 튜터에는 Gemma 4, (B) 코드 자동완성 에이전트에는 DiffusionGemma가 더 적합해요.

**해설**: DiffusionGemma는 AIME 같은 다단계 수학 추론에서 AR 모델 대비 10~20%p 뒤처지는 "빠르지만 덜 똑똑한" 모델이거든요. 반면 코딩이나 구조화된 작업은 격차가 상대적으로 작고, 초당 1,000+ 토큰 속도는 LLM 호출을 연속으로 수행하는 에이전트 시나리오에서 큰 이점이 되죠. 태스크 성격에 따라 속도와 품질의 트레이드오프를 고르는 게 포인트예요.

</details>

**Q8. OX 퀴즈! DiffusionGemma의 "최대 4배 빠르다"는 속도 이점은 다수 사용자가 동시에 요청하는 클라우드 서빙 환경에서도 그대로 유지된다. (O/X)**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X

**해설**: 공식 속도 수치는 단일 유저 로컬 환경 기준이에요. 다수 요청이 동시에 들어오는 서빙 환경에서는 이미 GPU가 배칭으로 병렬성을 확보하고 있어서 디퓨전의 속도 이점이 줄어들죠. 구글도 공식 문서에서 이 한계를 직접 인정했고, 그래서 DiffusionGemma는 로컬 배포나 단일 사용자 시나리오에서 특히 빛나는 모델이에요.

</details>
