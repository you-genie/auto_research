# KORMo: 합성 데이터로 한국어 LLM을 처음부터 만들 수 있을까?

> "The key question is whether synthetic data can safely dominate pretraining corpora for low-resource languages without triggering model collapse."
> — KORMo 저자진 (KAIST MLP Lab et al., 2025)

한국어 LLM 사전학습에서 가장 큰 고민 중 하나는 데이터 부족이에요. 영어는 수천억 토큰짜리 고품질 코퍼스가 넘쳐나는데, 한국어는 그 규모가 한참 작거든요. LLaMA-2가 사전학습 시 한국어 토큰을 고작 **0.06%** 썼다는 사실만 봐도 얼마나 저자원인지 바로 와닿죠.

그래서 KAIST MLP Lab·NLPCL Lab·U&I Lab과 서울과학기술대학교 공동 연구진이 한 가지 과감한 실험을 했어요. *"합성 데이터를 코퍼스의 68%로 채운 채 10B짜리 모델을 처음부터 학습시켜도, model collapse가 안 일어날 수 있을까?"*

그 결과가 바로 **KORMo(Korean Open Reasoning Model for Everyone)**예요. 데이터, 코드, 학습 레시피, 로그까지 전부 공개한 Fully Open Model(FOM)이고, arXiv에는 2025년 10월에 올라왔어요([arXiv:2510.09426](https://arxiv.org/abs/2510.09426)).

---

## 목차

1. [문제의식: 저자원 언어와 합성 데이터 딜레마](#1-문제의식)
2. [KORMo-10B 아키텍처](#2-kormo-10b-아키텍처)
3. [한국어 합성 데이터 5종](#3-한국어-합성-데이터-5종)
4. [데이터 구성 및 품질 관리](#4-데이터-구성-및-품질-관리)
5. [2-Stage 학습 레시피](#5-2-stage-학습-레시피)
6. [평가 결과](#6-평가-결과)
7. [핵심 발견 RQ1·RQ2·RQ3](#7-핵심-발견)
8. [Instruction Tuning: KORMo-10B-sft](#8-instruction-tuning)
9. [한계와 의의](#9-한계와-의의)
10. [참고 문헌](#참고-문헌)

---

## 1. 문제의식

### 합성 데이터 = model collapse?

지금까지 합성 데이터를 대규모로 사전학습에 쓰는 건 금기에 가까웠어요. Shumailov et al. 등의 연구가 경고한 이유가 있거든요.

합성 데이터로만 학습하면 분포가 점점 좁아지고, 그 데이터로 또 모델을 만들고, 또 그 모델로 데이터를 만들면... 어느 순간 모델이 완전히 제한적인 출력만 내놓게 돼요. 이게 **model collapse**예요.

그런데 저자원 언어 입장에서는 난감한 상황이에요.

- 영어처럼 고품질 실제 데이터가 수천억 토큰씩 있지 않고
- 그렇다고 합성 데이터를 막 쓰자니 collapse가 걱정이고

KORMo는 이 딜레마에 정면 돌파로 답해요.

### KORMo의 핵심 전제

1. **합성 데이터 비율 자체가 문제가 아닐 수 있다** — 어떻게, 누가 만드느냐가 더 중요하다
2. **단일 합성기로 만든 데이터 → collapse / 다양한 합성기 믹스 → stable**
3. 한국어를 제대로 소화하려면 최소 **5% 이상**의 한국어 토큰이 필요하다

LLaMA-2의 한국어 비중 0.06%가 얼마나 부족한지, 그리고 KORMo가 의도적으로 5%를 확보한 이유가 여기서 나오는 거예요.

---

## 2. KORMo-10B 아키텍처

아키텍처 자체는 표준적인 LLaMA-style decoder예요. 특이점이라면 vocab이 **125K**로 매우 커서 한국어 형태소를 훨씬 효율적으로 처리한다는 거예요.

| 항목 | 값 |
|---|---|
| 총 파라미터 | 10.75B (임베딩 1.02B + 비임베딩 9.73B) |
| 레이어 수 | 40 |
| Hidden size | 4096 |
| Attention head / KV head | 32 / 8 (GQA) |
| Vocab size | 125,184 |
| 활성화 함수 | SwiGLU |
| 정규화 | RMSNorm + Pre-LN |
| 위치 임베딩 | RoPE |
| Long-context | 13K 토큰까지 정확도 유지 |

GQA(Grouped Query Attention)를 써서 추론 시 KV 캐시 메모리를 절약하고, Pre-LN 덕분에 합성 데이터로 학습할 때도 훈련이 불안정해지지 않는다는 게 논문의 주장이에요. 실제로 Pre-LN 없이는 합성 데이터 heavy 학습이 쉽게 불안정해진다는 절제 실험 결과도 있어요.

토크나이저는 **EPK-125K**라는 이름으로 한국어 친화적으로 설계됐어요. 기존 32K~64K 수준 토크나이저보다 한국어 형태소를 훨씬 세밀하게 처리하죠.

---

## 3. 한국어 합성 데이터 5종

이게 KORMo 논문의 진짜 기여라고 해도 과언이 아니에요. 합성 데이터를 단순히 "많이 만든다"가 아니라, **시드 다양성 × 합성 모델 다양성**을 의도적으로 설계했거든요.

| 데이터셋 | 시드 소스 | 합성 모델 | 합성 방식 |
|---|---|---|---|
| Synth-FineWeb2 | [FineWeb2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) | Qwen3-30B-A3B | 한국 맥락 기반 커스텀 프롬프트로 rewrite |
| Synth-UltraFineWeb | [UltraFineWeb](https://huggingface.co/datasets/openbmb/UltraFineWeb) | Qwen3-30B-A3B | "한국어로 답변" 지시어 추가해 rewrite |
| Synth-Nemo-HQ | [Nemotron-CC-HQ](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2) | Qwen3-30B-A3B | 영어 시드를 한국어로 번역+재작성 |
| Kosmopedia | Cosmopedia 시드 | GPT-OSS-120B | 한국 맞춤형 textbook-style 생성 |
| Ko-Reasoning | Nemotron-Post | Qwen3-235B | 영어 reasoning chain + 한국어 답변 쌍 |

합성 모델이 세 종류(Qwen3-30B-A3B, GPT-OSS-120B, Qwen3-235B)라는 점에 주목해야 해요. 각 모델이 서로 다른 스타일과 편향을 갖고 있기 때문에, 이 세 모델이 만든 데이터를 섞으면 **단일 모델 분포로 수렴하지 않아요**.

> "Using a single synthesizer for all synthetic data leads to model collapse, while mixing outputs from diverse synthesizers maintains training stability."

이 발견이 논문의 핵심 실험적 기여예요.

### 왜 Ko-Reasoning이 중요한가?

Ko-Reasoning은 단순 번역이 아니에요. 영어로 된 reasoning chain(사고 과정)을 Qwen3-235B로 생성하고, 그에 대한 답변은 한국어로 쓰는 이중 언어 쌍이에요. 이걸 통해 모델이 한국어로 추론하는 능력을 사전학습 단계부터 익히게 되는 거예요.

---

## 4. 데이터 구성 및 품질 관리

### 전체 토큰 구성

사전학습에 사용된 총 토큰은 **3,462.32B (약 3.46T)**이에요.

- 영어: ~2,290B
- 한국어: ~1,172B (전체의 약 5%)
  - 그 중 합성 비율: **68.74%**

5%라는 숫자가 작아 보일 수 있는데, 절대적인 양으로 보면 1,172B 토큰이에요. 그 중 806B 이상이 합성이라는 거죠. 이 규모로 합성 데이터 위주 사전학습을 시도한 사례는 사실상 없었어요.

### 다단계 품질 필터링

데이터를 그냥 모아서 학습시키면 당연히 안 되겠죠. KORMo는 4단계 필터링을 거쳐요.

```
1. 휴리스틱 필터
   - 정규식 기반 오류 제거
   - 문서 길이 필터
   - perplexity 기반 품질 필터

2. 중복 제거 (dedup)
   - Old-both 전략 (가장 엄격한 버전)
   - → 전체 데이터의 70% 감소
   - → 하지만 성능은 오히려 향상!

3. 품질 분류기
   - fastText 분류기 v2가 최고 성능 (Table 11)
   - 여러 분류기 변형 중 ablation으로 선택

4. 추론 데이터 번역 필터 (Algorithm 1)
   - 2단계 필터로 오역/품질 저하 데이터 99% 제거
   - Ko-Reasoning 데이터의 순도 확보
```

특히 dedup 결과가 흥미로워요. 데이터를 70% 날려도 성능이 좋아진다는 건, **데이터 품질이 양보다 훨씬 중요하다**는 걸 실증적으로 보여주는 거예요.

### 토크나이저별 최적 합성 비율 (RQ2)

EPK-125K 토크나이저를 기준으로 실험한 결과:

| 언어 | 최적 합성 비율 |
|---|---|
| 영어 | 약 85% |
| 한국어 | 약 15% |

이게 좀 반직관적이에요. 한국어 데이터가 부족하니까 합성 데이터를 더 많이 쓰면 될 것 같잖아요? 근데 실험 결과는 한국어는 합성 비율을 **너무 높이면 안 된다**고 나와요. 15%가 스위트 스팟이에요.

반면 영어는 85%까지 합성 비율을 높여도 괜찮았어요. 영어 합성 데이터가 더 다양하고 품질이 고르기 때문으로 추정돼요.

---

## 5. 2-Stage 학습 레시피

### Stage 1: Warm-up (~1T 토큰)

저품질 웹 데이터로 베이스 representation을 다지는 단계예요. 여기서는 정제되지 않은 데이터도 많이 포함해서, 모델이 언어의 기본적인 통계 패턴을 익히게 해요.

### Stage 2: 본 학습 (~1.8T 토큰)

고품질 + 합성 데이터 + reasoning 데이터를 집중 투입하는 단계예요.

- Learning rate **7e-4**가 가장 안정적인 수렴을 보였어요 (Figure 6에서 여러 LR 값 비교)
- Ko-Reasoning 데이터를 이 시점에 집중 투입

```
Stage 2 데이터 구성:
- 고품질 웹 데이터 (dedup + 분류기 통과)
- 합성 데이터 5종 (Synth-FineWeb2, Synth-UltraFineWeb, ...)
- Ko-Reasoning 데이터
```

### Mid-training (Stage 2 이후)

Stage 2가 끝난 뒤, 두 가지 특화 학습을 추가해요.

| 목적 | 토큰 수 |
|---|---|
| Long-context 확장 | 10.27B |
| Reasoning 강화 (Ko-Reasoning 포함) | 157.76B |

Long-context mid-training에서는 컨텍스트 길이를 점진적으로 늘려서, 최종적으로 13K 토큰까지 안정적으로 처리하게 해요.

---

## 6. 평가 결과

### 영어 벤치마크 (Stage 2)

평균 **64.60%**로, 비슷한 크기의 오픈소스 모델들과 경쟁력 있는 수준이에요.

| 벤치마크 | 점수 |
|---|---|
| MMLU | 65.35% |
| ARC-Challenge | 59.90% |
| ARC-Easy | 85.65% |
| BoolQ | 83.88% |
| COPA | 95.00% |
| HellaSwag | 59.79% |
| Winogrande | 74.98% |
| **평균** | **64.60%** |

비교 대상: Llama 3, Qwen 2.5, DeepSeek-R1, OLMo/OLMo-E, BLOOM, SmolLM3, Nemotron 4 등

### 한국어 벤치마크 (Stage 2)

평균 **39.01%**로, 절대값은 낮지만 맥락이 중요해요.

| 벤치마크 | 점수 |
|---|---|
| [KMMLU](https://arxiv.org/abs/2402.11548) | 28.03% |
| [CSATQA](https://arxiv.org/abs/2402.11548) | 25.13% |
| [HAERAE](https://arxiv.org/abs/2309.02706) | 18.70% |
| [KoBEST](https://arxiv.org/abs/2204.04541) (avg) | 51.82% |
| **평균** | **39.01%** |

KMMLU나 HAERAE처럼 전문 지식이 필요한 벤치마크에서 점수가 낮은 건, 사전학습 베이스 모델의 한계예요. SFT(Instruction Tuning)를 거친 KORMo-10B-sft는 이보다 훨씬 높은 성능을 보여요.

### Long-context (NIAH, Needle-in-a-Haystack)

| 언어 | 정확도 |
|---|---|
| 영어 | 99.04% |
| 한국어 | 69.04% |

영어는 거의 완벽하지만 한국어는 아직 격차가 있어요. 특히 13K 이후로 한국어 정확도가 급격히 떨어지는 패턴이 있어요. Long-context mid-training이 영어에 더 최적화된 탓으로 보여요.

---

## 7. 핵심 발견

### RQ1: 합성 데이터로 사전학습해도 안전한가?

**결론: 조건부 YES**

Pre-LN + intra-doc masking 조건 하에서는, 합성 데이터 heavy 학습이 비합성 모델과 동등 이상의 성능을 보여요. 하지만 핵심 조건이 있어요.

> "단일 합성기(single synthesizer)로만 만든 데이터 → model collapse 발생"
> "다양한 합성기(diverse synthesizers) 믹스 → 안정적 학습"

이게 Figure 8에서 시각적으로 명확하게 보여요. 단일 합성기 실험에서는 훈련 loss가 발산하거나 수렴이 불안정해지는 반면, 여러 합성기를 섞으면 깨끗하게 수렴해요.

**실용적 가이드라인**: 합성 데이터를 쓸 거라면, 최소 2-3가지 서로 다른 스타일의 합성기를 믹스하세요.

### RQ2: 토크나이저별 최적 합성 비율이 다르다

언어마다, 그리고 토크나이저마다 "합성 데이터를 얼마나 넣는 게 최적인가"가 달라요.

- 영어: 합성 85% OK
- 한국어: 합성 15%가 sweet spot (너무 높이면 안 됨)

이건 한국어 합성 데이터의 다양성이 아직 영어만큼 풍부하지 않아서 생기는 현상으로 해석돼요. 합성 모델들이 영어를 더 잘 알기 때문에, 영어 합성 데이터가 더 다양하고 고른 품질을 보여요.

### RQ3: 한국어 합성 데이터의 편향이 영어보다 낮다

이건 저자들도 흥미롭다고 언급하는 발견이에요.

한국어 합성 데이터가 **영어 합성 데이터보다 편향적 토큰(biased tokens)이 적어요**. 반면 실제 크롤링 데이터를 섞을수록 유해 토큰이 급증하는 패턴이 나와요(Table 9).

이 결과는 한국어 합성 데이터를 고품질 필터로 쓰면 오히려 더 깨끗한 코퍼스를 만들 수 있다는 가능성을 시사해요.

---

## 8. Instruction Tuning

사전학습 베이스 위에 이중언어 Instruction Tuning을 적용한 **KORMo-10B-sft**가 HuggingFace에 공개돼 있어요([KORMo-Team/KORMo-10B-sft](https://huggingface.co/KORMo-Team/KORMo-10B-sft)).

한국어에서 거의 네이티브 수준의 reasoning과 담화 일관성을 보여요. 베이스 모델의 낮은 벤치마크 점수와 달리, SFT 이후에는 실용적인 한국어 대화 품질이 크게 올라가요.

---

## 9. 한계와 의의

### 한계

- **한국어 long-context**: 13K 이후 정확도 급격히 저하 (영어는 99% 유지)
- **한국어 전문 벤치마크**: KMMLU 28.03%, HAERAE 18.70%로 절대값은 아직 낮음
- 사전학습 규모(3.46T)가 크지만, GPT-4/Claude 급 모델과의 격차는 명확

### 의의

KORMo가 진짜로 의미 있는 이유는 결과 수치보다 **"이게 가능하다는 것을 보였다"**는 점이에요.

| 기여 | 내용 |
|---|---|
| 합성 데이터 사전학습 실증 | 저자원 언어에서 합성 68% 사전학습이 가능함을 대규모로 증명 |
| Fully Open Model | 데이터 + 코드 + 학습 레시피 + 로그 전체 공개 |
| 합성 다양성 가이드라인 | "단일 합성기 = collapse, 다중 합성기 = stable" 레시피 제시 |
| 한국어 비중 가이드라인 | LLaMA-2 수준 0.06%로는 부족, 5% 이상 필요 |

특히 Fully Open Model이라는 점은 재현성 측면에서 커요. 학습 로그까지 공개함으로써, 다른 연구자들이 학습 과정 전체를 들여다볼 수 있어요. 저자원 언어 LLM 연구를 위한 레퍼런스 포인트가 될 수 있는 작업이에요.

---

## 참고 문헌

- [KORMo 논문 (arXiv:2510.09426)](https://arxiv.org/abs/2510.09426) — Minjun Kim, Hyeonseok Lim 외 11인, KAIST, 2025
- [KORMo PDF](https://arxiv.org/pdf/2510.09426)
- [KORMo HuggingFace Paper 페이지](https://huggingface.co/papers/2510.09426)
- [KORMo-10B-sft (HuggingFace)](https://huggingface.co/KORMo-Team/KORMo-10B-sft)
- [alphaXiv overview](https://www.alphaxiv.org/overview/2510.09426v1)

**데이터셋**

- [FineWeb2](https://huggingface.co/datasets/HuggingFaceFW/fineweb-2) — HuggingFace FW
- [UltraFineWeb](https://huggingface.co/datasets/openbmb/UltraFineWeb) — OpenBMB
- [Nemotron-CC v2](https://huggingface.co/datasets/nvidia/Nemotron-CC-v2) — NVIDIA
- [Cosmopedia](https://huggingface.co/datasets/HuggingFaceTB/cosmopedia) — HuggingFace TB

**합성 모델**

- [Qwen3-30B-A3B](https://huggingface.co/Qwen/Qwen3-30B-A3B)
- [Qwen3-235B-A22B](https://huggingface.co/Qwen/Qwen3-235B-A22B)
- [GPT-OSS-120B](https://huggingface.co/openai/gpt-oss-120b)

**벤치마크**

- [KMMLU (arXiv:2402.11548)](https://arxiv.org/abs/2402.11548)
- [HAERAE (arXiv:2309.02706)](https://arxiv.org/abs/2309.02706)
- [KoBEST (arXiv:2204.04541)](https://arxiv.org/abs/2204.04541)
