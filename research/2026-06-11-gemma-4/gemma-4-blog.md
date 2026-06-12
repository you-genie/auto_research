# Gemma 4 완전 정복: 31B로 400B를 이긴 구글의 오픈 웨이트 모델

> 📊 **발표자료**: [gemma-4-presentation.pptx](./gemma-4-presentation.pptx)

> **TL;DR**: 구글 딥마인드가 2026년 4월 2일 Gemma 4를 공식 출시했어요. 5가지 모델 크기, 최대 256K 컨텍스트, 멀티모달(이미지+오디오+비디오) 지원, 그리고 Apache 2.0 라이선스까지. 31B 모델이 AIME 2026 수학 벤치마크에서 89.2%를 기록하며 훨씬 큰 모델들을 제쳤거든요.

---

## 목차

1. [이게 뭐예요? — Gemma 시리즈 간단 정리](#gemma-시리즈-간단-정리)
2. [Gemma 4, 언제 어떻게 나왔나요?](#gemma-4-출시-배경)
3. [세대별 비교 — 1 → 2 → 3 → 4](#세대별-진화)
4. [핵심 기술 파헤치기](#핵심-기술-특징)
5. [모델 라인업 한눈에 보기](#모델-라인업)
6. [벤치마크: 진짜 얼마나 잘해요?](#벤치마크-성능)
7. [생태계 & 어디서 쓸 수 있나요?](#생태계와-활용)
8. [한계점과 주의사항](#한계점과-주의사항)
9. [앞으로 어떻게 될까?](#향후-전망)
10. [참고문헌](#참고문헌)

---

## Gemma 시리즈 간단 정리

[구글 딥마인드](https://deepmind.google/)가 만드는 **Gemma 시리즈**는 쉽게 말하면 "Gemini의 오픈소스 사촌"이에요. 거대한 Gemini 모델을 만들 때 쌓은 연구 결과를 활용해서, 누구나 다운로드하고 파인튜닝하고 상업적으로도 쓸 수 있게 공개하는 거죠.

"오픈 웨이트(open weights)"라는 표현을 쓰는 이유가 있는데요 — 모델 가중치는 공개하지만, 학습 데이터나 전체 학습 파이프라인까지 공개하는 건 아니라서 "완전한 오픈소스"와는 구분돼요. 그래도 실용적인 관점에서는 자유롭게 쓸 수 있으니 오픈소스 생태계의 핵심 플레이어 중 하나예요.

---

## Gemma 4 출시 배경

[Google AI for Developers](https://ai.google.dev/gemma/docs/core/model_card_4)에 따르면 Gemma 4는 **2026년 4월 2일** 공식 출시됐어요. 구글 딥마인드가 "지금까지 만든 가장 지능적인 오픈 모델 패밀리"라고 소개했고요.

> "Gemma 4 is Google's most capable open model family, built from the same research and technology used to create Gemini 3, released with open weights so you can download, inspect, fine-tune, and deploy the models on your own infrastructure."  
> — [Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/gemma-4-available-on-google-cloud), 2026

즉 Gemini 3를 만들면서 개발한 연구 결과를 그대로 가져와서 오픈 웨이트로 공개한 거예요. Meta의 Llama 4, Alibaba의 Qwen 시리즈와 치열하게 경쟁하면서 구글이 오픈소스 AI 레이스에서 포지션을 확보하려는 전략이기도 하고요.

같은 해 6월에는 **Gemma 4 12B** 추가 모델과 **QAT(양자화 인식 학습) 체크포인트**까지 릴리즈됐어요.

---

## 세대별 진화

Gemma 시리즈가 어떻게 발전해왔는지 한번 정리해볼게요. [Wikipedia - Gemma (language model)](https://en.wikipedia.org/wiki/Gemma_(language_model)) 참고했어요.

### 세대별 핵심 스펙 비교

| 항목 | Gemma 1 (2024.02) | Gemma 2 (2024.06) | Gemma 3 (2025.03) | Gemma 4 (2026.04) |
|------|------------------|------------------|------------------|------------------|
| **최대 파라미터** | 7B | 27B | 27B | 31B (Dense) |
| **컨텍스트 길이** | 8K | 8K | 128K | 256K |
| **비전(이미지) 지원** | 없음 | 없음 | 있음 | 있음 |
| **오디오 지원** | 없음 | 없음 | 없음 | 있음 |
| **멀티모달** | 텍스트만 | 텍스트만 | 텍스트+이미지 | 텍스트+이미지+오디오+비디오 |
| **지원 언어** | 다국어 | 다국어 | 140+개 | 140+개 |
| **라이선스** | Gemma ToU | Gemma ToU | Gemma ToU | **Apache 2.0** |
| **주요 아키텍처** | MHA/MQA | GQA | GQA + SigLIP | Hybrid Attn + MoE |

뭐가 제일 눈에 띄냐면요:

1. **컨텍스트 길이 폭발**: 8K → 8K → 128K → 256K. Gemma 3에서 이미 엄청 늘었는데 Gemma 4에서 또 2배가 됐어요.
2. **멀티모달의 완성**: 1, 2세대는 텍스트 전용이었고, 3세대에서 이미지가 추가됐고, 4세대에서 오디오까지 들어왔어요.
3. **라이선스 변화**: 기존 "Gemma 이용 약관"에서 **Apache 2.0**으로 바뀐 게 큰 변화예요. 상업적 사용, 수정, 재배포 모두 자유롭게 가능해졌거든요.

### Gemma 1 (2024년 2월)

> 출시 당시 "경량 Gemini"로 포지셔닝됐고, 2B와 7B 두 가지 크기만 있었어요.

- 2B: Multi-Query Attention(MQA)
- 7B: Multi-Head Attention(MHA)
- 컨텍스트: 8,192 토큰
- 웹 문서, 코드 데이터로 학습

### Gemma 2 (2024년 6월)

- 2B, 9B, 27B 세 가지 크기
- **Grouped-Query Attention(GQA)** 도입
- 9B 모델은 27B에서 **지식 증류(distillation)**로 학습
- 그래도 여전히 8K 컨텍스트, 텍스트 전용

### Gemma 3 (2025년 3월)

- 1B, 4B, 12B, 27B로 라인업 다양화
- **비전 지원** 첫 도입 (SigLIP 인코더)
- 컨텍스트 128K로 대폭 확장
- 140개 이상 언어 지원
- Gemma 3n: 스마트폰/노트북 최적화 서브 라인

### Gemma 4 (2026년 4월)

- E2B, E4B, 12B, 26B MoE, 31B Dense
- **오디오 입력** 추가
- 컨텍스트 최대 256K
- MoE 아키텍처 도입 (26B A4B)
- Per-Layer Embeddings 등 효율화 기법
- **Apache 2.0** 라이선스

---

## 핵심 기술 특징

이 부분이 진짜 재미있는 부분이에요. [Maarten Grootendorst의 Visual Guide to Gemma 4](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-gemma-4)를 많이 참고했어요.

### 1. 하이브리드 어텐션 메커니즘

Gemma 4의 핵심 아키텍처 혁신 중 하나는 **로컬 슬라이딩 윈도우 어텐션**과 **글로벌 풀 어텐션**을 교대로 쌓는 방식이에요.

- **E2B**: 4:1 비율 (로컬 4개 레이어 : 글로벌 1개 레이어)
- **E4B, 31B, 26B A4B**: 5:1 비율
- **핵심 규칙**: 마지막 레이어는 항상 글로벌 어텐션

왜 이게 중요하냐면 — 풀 어텐션은 모든 토큰을 서로 비교하니까 메모리와 연산이 O(n²)으로 늘어요. 슬라이딩 윈도우는 가까운 토큰만 보니까 훨씬 효율적이고요. 둘을 섞으면 효율성과 성능을 같이 잡을 수 있는 거죠.

슬라이딩 윈도우 크기는:
- 소형 모델(E2B/E4B): 512 토큰
- 대형 모델(31B/26B A4B): 1024 토큰

그리고 글로벌 어텐션 레이어에서는 KV 쌍에서 K=V 최적화를 적용해서 KV 캐시 메모리를 더 줄였어요.

### 2. Per-Layer Embeddings (PLE) — E2B/E4B 전용

소형 모델들에만 적용된 재미있는 기법인데요, 토큰 임베딩을 입력 레이어에만 저장하는 게 아니라 **모든 레이어마다** 따로 저장해요.

각 레이어에서 256차원 임베딩(vs. 입력 1536차원)을 플래시 메모리에서 불러와서 게이팅 메커니즘으로 가중치를 조절하고, 이전 레이어 출력과 결합해요. RAM은 아끼면서 모델 표현력을 높이는 거죠 — 모바일/엣지 기기에 딱 맞는 설계예요.

### 3. MoE 아키텍처 (26B A4B)

> "Gemma 4's MoE model has 128 experts with 8 active per token, plus one shared expert per token, activating only 3.8B active parameters."  
> — [MindStudio Blog](https://www.mindstudio.ai/blog/gemma-4-mixture-of-experts-architecture-explained)

26B A4B 모델이 어떻게 26B의 지식을 갖고 있으면서도 추론 비용은 4B 수준인지 — 그 비결이 MoE예요.

- **전체 파라미터**: 25.2B (임베딩 포함)
- **활성 파라미터**: 추론 시 3.8B만 사용
- **전문가 구성**: 128개 전문가 + 1개 공유 전문가
- **라우팅**: 각 토큰마다 128개 중 8개 전문가 선택

공유 전문가는 항상 활성화되고, 나머지 8개는 라우터가 토큰에 따라 동적으로 선택해요. 학습 중에는 전문가들이 고르게 사용되도록 보조 손실(auxiliary loss)을 추가해요.

### 4. p-RoPE (부분 회전 위치 인코딩)

기존 RoPE는 모든 차원에 회전 위치 정보를 적용하는데, Gemma 4는 `p=0.25`로 전체 차원의 25%에만 적용해요. 이렇게 하면 긴 컨텍스트에서 작은 회전이 누적되어 발생하는 성능 저하를 줄일 수 있어요. 글로벌 어텐션 레이어에서 특히 중요해요.

### 5. 비전 인코더 (ViT 기반)

이미지를 16×16 픽셀 패치로 나눠서 Vision Transformer로 처리해요.

- 소형 모델(E2B/E4B): 150M 파라미터 인코더
- 대형 모델(31B/26B MoE): 550M 파라미터 인코더
- **12B 유니파이드 모델**: 인코더 없음! 이미지/오디오 데이터를 직접 LLM 임베딩 공간으로 선형 투영

2D RoPE로 가변 종횡비 이미지를 처리하고, 소프트 토큰 버짓(70~1120 토큰)으로 이미지 복잡도를 조절해요.

### 6. 오디오 인코더 (E2B/E4B/12B)

**Conformer 인코더**를 사용해서:
1. 멜-스펙트로그램(mel-spectrogram) 특징 추출
2. 청킹 및 2D 합성곱 다운샘플링
3. 소프트 토큰으로 변환 후 언어 모델 차원으로 투영

최대 30초 오디오를 처리할 수 있어요.

### 7. Multi-Token Prediction (MTP) 드래프터

추론 속도를 높이기 위한 투기적 디코딩(speculative decoding)이에요.

- E2B용 드래프터: 76M 파라미터
- 여러 토큰을 병렬로 예측하고, 메인 모델이 한꺼번에 검증
- **최대 3배** 추론 속도 향상 (품질 손실 없이!)

### 8. 생각 모드 (Thinking Mode)

[공식 문서](https://ai.google.dev/gemma/docs/capabilities/thinking)에 따르면 모든 Gemma 4 모델은 "생각 모드"를 지원해요.

```python
text = processor.apply_chat_template(
    message, 
    tokenize=False, 
    add_generation_prompt=True, 
    enable_thinking=True  # 생각 모드 활성화
)
```

활성화하면 모델이 최종 답변 전에 내부 추론 과정을 먼저 생성해요. 수학, 코딩, 복잡한 다단계 추론에 특히 효과적이에요. 멀티턴 대화에서는 이전 턴의 생각 토큰을 제거하고 넘겨줘야 성능이 유지된다는 점 주의!

### 9. 학습 데이터

- **데이터 종류**: 웹 문서, 코드, 이미지, 오디오
- **데이터 컷오프**: 2025년 1월
- **언어**: 140개 이상
- **안전 처리**: CSAM 필터링, 민감 데이터 제거

---

## 모델 라인업

[공식 모델 카드](https://ai.google.dev/gemma/docs/core/model_card_4)와 [Google AI 개요 페이지](https://ai.google.dev/gemma/docs/core)에서 확인한 내용이에요.

### 모델 스펙 상세

| 모델 | 전체 파라미터 | 활성 파라미터 | 레이어 수 | 컨텍스트 | 메모리(BF16) | 특징 |
|------|-------------|-------------|---------|---------|-------------|------|
| **E2B** | 5.1B (임베딩 포함) | 2.3B | 35 | 128K | 11.4 GB | 엣지/모바일, PLE |
| **E4B** | 8B (임베딩 포함) | 4.5B | 42 | 128K | 17.9 GB | 엣지/모바일, PLE |
| **12B** | 11.95B | 11.95B | 48 | 256K | 26.7 GB | 인코더-프리 유니파이드 |
| **26B A4B** | 25.2B | 3.8B (추론 시) | 30 | 256K | 57.7 GB | MoE, 128전문가 |
| **31B Dense** | 30.7B | 30.7B | 60 | 256K | 69.9 GB | 최고 성능 |

**어떤 모델을 써야 하냐고요?**

- **스마트폰/IoT**: E2B — 11GB VRAM (QAT 적용 시 더 줄어요)
- **일반 노트북**: E4B 또는 12B
- **고성능 워크스테이션**: 26B A4B (MoE라 추론 빠름)
- **최고 품질 필요**: 31B Dense

### 인스트럭션 튜닝(IT) 버전

각 모델에는 `-it` 접미사가 붙은 인스트럭션 튜닝 버전도 있어요:
- `gemma-4-31B-it`
- `gemma-4-26B-A4B-it`
- `gemma-4-12B-it`
- `gemma-4-E4B-it`
- `gemma-4-E2B-it`

대화형 어시스턴트, 코딩 도우미 등 실제 사용 목적이라면 IT 버전을 쓰는 게 좋아요.

---

## 벤치마크 성능

### Gemma 4 31B vs 경쟁 모델

[Lushbinary 비교 가이드](https://lushbinary.com/blog/gemma-4-vs-llama-4-vs-qwen-3-5-open-weight-model-comparison/)에서 정리된 데이터예요:

| 벤치마크 | Gemma 4 31B | Qwen 3.5 27B | Llama 4 Scout | 비고 |
|---------|------------|-------------|--------------|------|
| **MMLU Pro** | 85.2% | **86.1%** | ~80% | 일반 지식 |
| **GPQA Diamond** | 84.3% | **85.5%** | ~74% | 박사급 추론 |
| **AIME 2026** | **89.2%** | ~85% | N/A | 수학 경시 |
| **LiveCodeBench v6** | 80.0% | **83.6%** | ~68% | 코딩 |
| **Codeforces ELO** | **2150** | ~1900 | ~1400 | 경쟁 프로그래밍 |
| **MMMU Pro (비전)** | **76.9%** | ~72% | ~65% | 멀티모달 추론 |
| **Arena Text 순위** | **#3** (1452) | #2 (est.) | ~#10 | LM Arena |
| **Arena Text (26B MoE)** | **#6** (1441) | — | — | 4B 활성만으로! |

> **핵심 정리**: Gemma 4 31B는 수학과 경쟁 프로그래밍에서 압도적이에요. 일반 지식(MMLU Pro)과 GPQA에서는 Qwen 3.5 27B에 살짝 밀려요. Llama 4 Scout는 전반적으로 뒤처지고요.

가장 인상적인 수치는 **26B A4B MoE 모델의 Arena 6위**예요. 추론 시 4B 파라미터만 활성화하면서 Arena 6위에 오른다는 건, 파라미터 당 효율로 보면 압도적이에요.

### Gemma 3 vs Gemma 4 비교

한 세대 전과 비교하면 얼마나 발전했는지 체감이 되죠:

| 벤치마크 | Gemma 3 27B | Gemma 4 31B | 향상폭 |
|---------|------------|------------|-------|
| AIME | ~50-60% | **89.2%** | +30%p 이상 |
| LiveCodeBench | ~50% | **80.0%** | +30%p |
| GPQA Diamond | ~65% | **84.3%** | +20%p |

한 마디로 — 엄청난 도약이에요.

---

## 생태계와 활용

### 접근 방법

[HuggingFace Gemma 4 블로그](https://huggingface.co/blog/gemma4)와 [구글 공식 발표](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)에 따르면 다양한 경로로 이용 가능해요.

**모델 다운로드**:
- [Hugging Face](https://huggingface.co/google) — SafeTensors 포맷
- [Kaggle](https://www.kaggle.com/models/google/gemma) — 구글 계정으로 접근
- [Ollama](https://ollama.com/library/gemma4) — `ollama run gemma4:31b`
- [LM Studio](https://lmstudio.ai/models/gemma-4) — GUI 인터페이스

### 추론 프레임워크 지원

| 도구 | 지원 | 특징 |
|-----|------|------|
| **vLLM** | ✅ | compressed-tensors QAT 지원 |
| **llama.cpp** | ✅ | GGUF 포맷, CPU도 가능 |
| **Ollama** | ✅ | 한 줄 설치 |
| **MLX** | ✅ | Apple Silicon 최적화 |
| **transformers.js** | ✅ | 브라우저에서도 실행 |
| **mistral.rs** | ✅ | Rust 네이티브 추론 |
| **TensorRT-LLM** | ✅ | NVIDIA GPU 최적화 |

### 클라우드 배포

- **Google Cloud Vertex AI**: 완전 관리형 배포, 파인튜닝
- **Google Cloud Run**: 서버리스 GPU (NVIDIA RTX PRO 6000)
- **GKE**: 쿠버네티스 기반 추론 서빙
- **Google Cloud TPU**: 사전 학습/추론 최적화

### 양자화 (QAT 체크포인트)

[구글 QAT 발표](https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/) (2026년 6월 5일)에 따르면:

> QAT 방식은 모델 학습 과정에 양자화를 통합해서, 학습 후 적용하는 일반 PTQ보다 품질이 더 높아요.

- **Q4_0 포맷**: 모든 모델에 범용 적용 가능
- **모바일 포맷**: 정적 활성화, 채널별 양자화, 2비트 압축
- **결과**: 26B A4B가 16GB 노트북에서, E2B가 모바일에서 1GB 수준으로 실행!

QAT GGUF는 Unsloth가 Hugging Face에 올린 버전이 가장 많이 다운로드되고 있어요.

### NVIDIA 생태계

[nvidia/Gemma-4-31B-IT-NVFP4](https://huggingface.co/nvidia/Gemma-4-31B-IT-NVFP4)처럼 NVIDIA가 FP4 양자화 버전도 제공해요. NVIDIA NIM 플랫폼과도 통합됐어요.

---

## 한계점과 주의사항

좋은 점만 얘기하면 안 되죠. [gemmai4.com 한계점 분석](https://gemmai4.com/limitations/)을 참고했어요.

### 기술적 한계

1. **비디오 처리 제한**: 최대 60초, 1fps(초당 1프레임). 실시간 비디오나 빠른 동작 분석에는 부적합해요.
2. **오디오 한계**: 오디오 입력은 E2B/E4B/12B에만 있고, **오디오 출력(TTS)은 지원 안 해요**.
3. **복잡한 수학적 추론**: 비선형 추론, 고급 기호 조작은 명시적 단계별 프롬프팅 없이는 어려울 수 있어요.
4. **결정론적 출력 불가**: 암호화 연산이나 정확한 수치 계산은 검증 레이어가 필요해요.
5. **SWE-bench**: Qwen 3.5 27B에 비해 실제 소프트웨어 엔지니어링 태스크에서는 다소 밀려요.

### 안전 및 윤리 이슈

- **할루시네이션**: 그럴듯하게 들리지만 틀린 정보를 생성할 수 있어요. 중요한 정보는 반드시 검증 필요!
- **학습 데이터 편향**: 사회적 편향이 모델에 내재될 수 있어요.
- **언세이프 파인튜닝**: "abliteration" 기법 등으로 안전 장치를 우회한 버전이 커뮤니티에 돌아다녀요.
- **의료/법률/금융 분야 배포 시 주의**: 자율 의사결정 시스템에는 반드시 인간 감독이 필요해요.

### 데이터 컷오프

학습 데이터 컷오프가 **2025년 1월**이에요. 그 이후 사건이나 정보는 모르거나 잘못 알 수 있어요.

---

## 향후 전망

Gemma 4 이후를 어떻게 볼 수 있을까요?

**단기 트렌드** (2026년 하반기):
- QAT 최적화 지속 — 엣지 기기 성능 개선
- 파인튜닝 생태계 성숙 (Unsloth, Vertex AI 등)
- 에이전트 프레임워크 통합 심화 (ADK, LangChain 등)

**중기 트렌드**:
- DiffusionGemma(이산 확산 기반 텍스트 생성, H100에서 1100+ 토큰/초)처럼 새 아키텍처 변형 등장
- 멀티모달 범위 확장 (오디오 출력, 3D 등)
- 더 작고 효율적인 엣지 모델 (PLE 기법 심화)

**경쟁 구도**:

| 진영 | 주요 모델 | 강점 |
|-----|---------|------|
| **Google** | Gemma 4 | 멀티모달, Apache 2.0, 엣지 지원 |
| **Meta** | Llama 4 | 초장문 컨텍스트(10M), 생태계 |
| **Alibaba** | Qwen 3.5/3.6 | 일반 지식, 코딩 |
| **Mistral** | Mistral/Mixtral | 유럽, 경량 |

구글이 Gemma 시리즈를 통해 Gemini 연구를 빠르게 오픈 생태계로 가져오는 전략을 유지하는 한, Gemma 5도 멀지 않았을 거예요.

---

## 마무리

Gemma 4는 그냥 "구글이 오픈소스 AI 하나 더 냈네" 수준이 아니에요. 31B로 자기보다 훨씬 큰 모델들과 대등하거나 더 나은 성능을 보여주고, Apache 2.0으로 진정한 상업적 자유를 줬고, 엣지부터 클라우드까지 모든 환경을 커버하는 라인업을 갖췄거든요.

특히 **26B MoE 모델이 추론 시 4B만 쓰면서 Arena 6위**에 오른 건 — 파라미터 당 효율이라는 관점에서 오픈 웨이트 모델의 새 지평을 열었다고 봐요.

직접 써보고 싶다면? Ollama로 시작하는 게 가장 쉬워요:

```bash
ollama run gemma4:31b
```

또는 Hugging Face에서 IT 버전 받아서 `transformers`로 돌려보세요. 생각 모드 켜놓고 수학 문제 몇 개 던져보면 진짜 놀랄 거예요.

---

## 참고문헌

1. [Gemma 4 model card | Google AI for Developers](https://ai.google.dev/gemma/docs/core/model_card_4)
2. [Gemma 4: Byte for byte, the most capable open models — Google Blog](https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/)
3. [Gemma 4 available on Google Cloud | Google Cloud Blog](https://cloud.google.com/blog/products/ai-machine-learning/gemma-4-available-on-google-cloud)
4. [Gemma 4 model overview | Google AI for Developers](https://ai.google.dev/gemma/docs/core)
5. [Thinking mode in Gemma | Google AI for Developers](https://ai.google.dev/gemma/docs/capabilities/thinking)
6. [Welcome Gemma 4: Frontier multimodal intelligence on device — HuggingFace Blog](https://huggingface.co/blog/gemma4)
7. [A Visual Guide to Gemma 4 — Maarten Grootendorst](https://newsletter.maartengrootendorst.com/p/a-visual-guide-to-gemma-4)
8. [Gemma (language model) — Wikipedia](https://en.wikipedia.org/wiki/Gemma_(language_model))
9. [Gemma 4 vs Llama 4 vs Qwen 3.5: 2026 Comparison Guide — Lushbinary](https://lushbinary.com/blog/gemma-4-vs-llama-4-vs-qwen-3-5-open-weight-model-comparison/)
10. [Gemma 4 with quantization-aware training — Google Blog](https://blog.google/innovation-and-ai/technology/developers-tools/quantization-aware-training-gemma-4/)
11. [Gemma 4 Limitations: Key Drawbacks, Challenges & Tradeoffs](https://gemmai4.com/limitations/)
12. [Gemma 4 Architecture Deep Dive: MoE, Dual RoPE, and 256K Context Explained — CloudInsight](https://cloudinsight.cc/en/blog/gemma-4-architecture)
13. [What Is Gemma 4's Mixture of Experts Architecture? — MindStudio](https://www.mindstudio.ai/blog/gemma-4-mixture-of-experts-architecture-explained)
14. [gemma4 — Ollama Library](https://ollama.com/library/gemma4)
15. [unsloth/gemma-4-31B-it-GGUF — Hugging Face](https://huggingface.co/unsloth/gemma-4-31B-it-GGUF)

---

## 📝 학습 퀴즈

지금까지 읽은 내용, 얼마나 기억나는지 가볍게 점검해 보세요. 답을 먼저 생각해 본 다음 "정답 보기"를 눌러 확인하면 돼요.

**Q1. "오픈 웨이트(open weights)"와 "완전한 오픈소스"는 뭐가 다른가요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 오픈 웨이트는 모델 가중치만 공개하는 것이고, 학습 데이터나 전체 학습 파이프라인까지 공개하는 건 아니에요.

**해설**: Gemma 시리즈는 누구나 가중치를 다운로드해서 파인튜닝하고 상업적으로 쓸 수 있지만, 무엇으로 어떻게 학습했는지는 전부 공개하지 않아요. 그래서 "완전한 오픈소스"와는 구분해서 부르는 거죠. 실용적인 관점에서는 자유롭게 쓸 수 있어서 오픈 생태계의 핵심 플레이어로 꼽혀요.

</details>

**Q2. OX 퀴즈: Gemma 4의 26B A4B 모델은 추론할 때 26B 파라미터를 전부 사용한다. (O/X)**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X

**해설**: 26B A4B는 MoE(Mixture of Experts) 아키텍처라서 추론 시에는 3.8B 활성 파라미터만 사용해요. 128개 전문가 중 토큰마다 8개를 라우터가 골라 쓰고, 공유 전문가 1개는 항상 활성화되는 구조죠. 그래서 26B급 지식을 갖고 있으면서도 추론 비용은 4B 수준인 거예요.

</details>

**Q3. Gemma 4가 로컬 슬라이딩 윈도우 어텐션과 글로벌 풀 어텐션을 교대로 쌓는 하이브리드 구조를 쓰는 이유는 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 효율성과 성능을 동시에 잡기 위해서예요. 풀 어텐션은 O(n²)로 비용이 커지니까, 가까운 토큰만 보는 슬라이딩 윈도우를 섞어서 메모리와 연산을 아끼는 거죠.

**해설**: 풀 어텐션은 모든 토큰을 서로 비교해서 메모리·연산이 제곱으로 늘어나는데, 슬라이딩 윈도우는 근처 토큰만 봐서 훨씬 가벼워요. Gemma 4는 로컬 레이어 4~5개당 글로벌 레이어 1개를 끼워 넣고, 마지막 레이어는 항상 글로벌로 두는 규칙을 지켜요. 덕분에 256K라는 긴 컨텍스트도 감당할 수 있는 거예요.

</details>

**Q4. Gemma 3에서 Gemma 4로 넘어오면서 생긴 변화가 아닌 것은 뭘까요?**

(a) 오디오 입력 지원 추가
(b) 컨텍스트 128K → 256K 확장
(c) Apache 2.0 라이선스 전환
(d) 비전(이미지) 지원 첫 도입

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: (d) 비전(이미지) 지원 첫 도입

**해설**: 이미지 지원은 이미 Gemma 3에서 SigLIP 인코더로 처음 들어왔어요. Gemma 4에서 새로 생긴 건 오디오 입력, 256K 컨텍스트, MoE 아키텍처, 그리고 기존 Gemma 이용 약관에서 Apache 2.0으로 바뀐 라이선스죠. 특히 라이선스 변화 덕분에 상업적 사용·수정·재배포가 모두 자유로워졌어요.

</details>

**Q5. 응용 시나리오: 스마트폰이나 IoT 기기처럼 메모리가 빠듯한 엣지 환경에 모델을 올려야 해요. 어떤 모델을 고르는 게 좋고, 이 모델에만 적용된 효율화 기법은 뭘까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: E2B(또는 E4B)를 고르면 되고, 이 소형 모델들에는 Per-Layer Embeddings(PLE)가 적용돼 있어요.

**해설**: PLE는 토큰 임베딩을 모든 레이어마다 따로 저장하고, 작은 256차원 임베딩을 플래시 메모리에서 불러와 게이팅으로 결합하는 기법이에요. RAM은 아끼면서 표현력은 높이니까 모바일·엣지에 딱 맞죠. 여기에 QAT 체크포인트까지 쓰면 E2B는 모바일에서 1GB 수준으로도 돌아가요.

</details>

**Q6. "생각 모드(Thinking Mode)"를 멀티턴 대화에서 쓸 때 주의해야 할 점은 뭐였죠?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 이전 턴의 생각 토큰을 제거하고 넘겨줘야 성능이 유지돼요.

**해설**: 생각 모드를 켜면 모델이 최종 답변 전에 내부 추론 과정을 먼저 생성하는데, 수학·코딩·다단계 추론에 특히 효과적이에요. 다만 멀티턴 대화에서 이전 턴의 생각 토큰까지 그대로 컨텍스트에 넣으면 성능이 떨어질 수 있어서, 제거하고 넘기는 게 권장돼요.

</details>

**Q7. OX 퀴즈: Gemma 4는 오디오를 입력으로 받을 수 있을 뿐 아니라 음성(TTS)으로 출력할 수도 있다. (O/X)**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: X

**해설**: 오디오는 입력만 지원하고, 그것도 E2B/E4B/12B 모델에만 있어요. 오디오 출력(TTS)은 지원하지 않죠. 입력도 Conformer 인코더로 멜-스펙트로그램을 처리하는 방식이라 최대 30초까지만 다룰 수 있다는 한계가 있어요.

</details>

**Q8. 벤치마크 결과를 보면 Gemma 4 31B가 특히 강한 영역과 상대적으로 밀리는 영역이 갈렸는데요. 각각 어디였을까요?**

<details markdown="1">
<summary>✅ 정답 보기</summary>

**정답**: 수학(AIME)과 경쟁 프로그래밍(Codeforces), 멀티모달 추론에서는 압도적이고, 일반 지식(MMLU Pro)·GPQA·실제 코딩(LiveCodeBench, SWE-bench)에서는 Qwen 3.5 27B에 살짝 밀려요.

**해설**: 수학 경시와 경쟁 프로그래밍, 비전 추론에서는 경쟁 모델들을 크게 앞섰지만, 일반 지식과 박사급 추론, 실제 소프트웨어 엔지니어링 태스크에서는 Qwen 3.5가 조금 더 나았어요. 모델마다 강점 영역이 다르니 용도에 맞게 고르는 게 중요하다는 얘기죠.

</details>
