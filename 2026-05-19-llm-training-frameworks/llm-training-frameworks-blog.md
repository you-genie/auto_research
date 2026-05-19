# 2025~2026 LLM 학습 프레임워크 완전 정복: 어떤 회사가 뭘 쓰는지 다 알려드림

> "The choice of training framework is as important as the model architecture itself." — DeepSpeed 팀 블로그, 2024
>
> 학습 프레임워크 선택은 모델 아키텍처만큼이나 중요한 결정이에요.

솔직히 이 세계 좀 복잡하죠? Megatron-LM, NeMo, DeepSpeed, FSDP, veRL, TorchTitan… 이름만 들어도 현기증이 나는데, 실제로 현업에서 어떤 게 쓰이는지는 더 불투명하고요. 오늘은 이걸 제대로 정리해볼게요.

**포인트는 두 가지예요:**
1. 계층/목적별로 프레임워크를 분류해서 비교할 수 있게 만들기
2. 실제로 어떤 기업이 뭘 쓰는지 구체적으로 알아보기

그리고 마지막에는 "내 팀은 GPU가 몇 개인데 뭘 써야 해?" 실용 가이드까지 드릴게요.

---

## 목차

1. [왜 프레임워크 선택이 중요한가](#1-왜-프레임워크-선택이-중요한가)
2. [계층별 분류: 전체 지도 한눈에 보기](#2-계층별-분류-전체-지도-한눈에-보기)
3. [Layer 1: 저수준 분산 학습 엔진](#3-layer-1-저수준-분산-학습-엔진)
4. [Layer 2: End-to-End 학습 플랫폼](#4-layer-2-end-to-end-학습-플랫폼)
5. [Layer 3: Post-training / RLHF·RL 특화 프레임워크](#5-layer-3-post-training--rlhfrl-특화-프레임워크)
6. [Layer 4: 오케스트레이션 & 실험 관리](#6-layer-4-오케스트레이션--실험-관리)
7. [Layer 5: 데이터 파이프라인](#7-layer-5-데이터-파이프라인)
8. [기업별 채택 현황 총정리](#8-기업별-채택-현황-총정리)
9. [한국 기업들은 뭘 쓸까?](#9-한국-기업들은-뭘-쓸까)
10. [규모별 추천 가이드](#10-규모별-추천-가이드)
11. [2025~2026 주요 트렌드](#11-20252026-주요-트렌드)
12. [의사결정 트리: 나에게 맞는 스택 고르기](#12-의사결정-트리-나에게-맞는-스택-고르기)
13. [결론](#13-결론)
14. [참고문헌](#14-참고문헌)

---

## 1. 왜 프레임워크 선택이 중요한가

LLM 학습은 단순히 "코드 돌리기"가 아니에요. 수천~수만 GPU를 동시에 굴리면서:

- 메모리를 어떻게 쪼갤지 (Tensor Parallelism / Pipeline Parallelism / Data Parallelism)
- 통신 비용을 어떻게 줄일지
- 체크포인트를 어떻게 저장할지
- 실패한 노드를 어떻게 복구할지

이 모든 걸 결정해야 하거든요. 잘못 고르면 GPU 활용률이 30~40%로 떨어지는데, 이게 H100 1000개짜리 클러스터면 엄청난 낭비죠.

> "Through the co-design of algorithms, frameworks, and hardware, we overcome the communication bottleneck in cross-node MoE training, achieving near-full computation-communication overlap." — DeepSeek-V3 Technical Report, 2024
>
> 알고리즘, 프레임워크, 하드웨어를 함께 설계함으로써 크로스-노드 MoE 학습에서의 통신 병목을 극복하고 거의 완전한 연산-통신 오버랩을 달성했습니다.

이게 왜 중요하냐면, DeepSeek이 2048개 H800 GPU로 671B 파라미터 모델(DeepSeek-V3)을 효율적으로 학습할 수 있었던 이유 중 하나가 바로 **자체 제작 HAI-LLM 프레임워크**와 그 안의 DualPipe 알고리즘 덕분이거든요.

---

## 2. 계층별 분류: 전체 지도 한눈에 보기

프레임워크는 크게 5개 계층으로 나눌 수 있어요:

```
┌─────────────────────────────────────────────────────────┐
│  Layer 5: 데이터 파이프라인                                │
│  NeMo Curator / Datatrove / WebDataset / StreamingDataset │
├─────────────────────────────────────────────────────────┤
│  Layer 4: 오케스트레이션 & 실험 관리                        │
│  Ray / Slurm / Kubeflow / W&B / MLflow / Hydra           │
├─────────────────────────────────────────────────────────┤
│  Layer 3: Post-training / RLHF·RL 특화                   │
│  veRL / OpenRLHF / NeMo-RL / TRL / LLaMA-Factory        │
│  Axolotl / Unsloth / Open-Instruct / slime / SkyRL       │
├─────────────────────────────────────────────────────────┤
│  Layer 2: End-to-End 학습 플랫폼                          │
│  NeMo / LLM Foundry / TorchTitan / Levanter / MaxText    │
│  Pax/Praxis / nanotron / picotron / Lingua               │
├─────────────────────────────────────────────────────────┤
│  Layer 1: 저수준 분산 학습 엔진                             │
│  Megatron-Core / DeepSpeed / PyTorch FSDP2               │
│  JAX+GSPMD / ColossalAI / HAI-LLM                       │
└─────────────────────────────────────────────────────────┘
```

계층이 낮을수록 제어권이 많고 복잡도가 높아요. 계층이 높을수록 편의성이 높지만 커스터마이징이 제한되는 트레이드오프가 있죠.

---

## 3. Layer 1: 저수준 분산 학습 엔진

이 계층은 실제 GPU 간 통신, 메모리 분할, 병렬화 전략을 담당해요. 여기서의 선택이 학습 속도와 확장성을 결정합니다.

### 3.1 Megatron-LM / Megatron-Core (NVIDIA)

[GitHub - NVIDIA/Megatron-LM](https://github.com/NVIDIA/Megatron-LM)

수천~수만 GPU 클러스터에서 Transformer 모델을 학습하기 위한 NVIDIA의 핵심 라이브러리예요. 2019년 처음 공개된 이래 지금도 가장 강력한 분산 학습 엔진 중 하나로 꼽히죠.

**핵심 기능:**
- **Tensor Parallelism (TP)**: 행렬 연산을 여러 GPU에 분할
- **Pipeline Parallelism (PP)**: 레이어를 여러 GPU 그룹에 분할
- **Sequence Parallelism (SP)**: 시퀀스 차원 분산
- **Context Parallelism (CP)**: 긴 컨텍스트 처리용
- **Expert Parallelism (EP)**: MoE 아키텍처 지원

Megatron-Core는 Megatron-LM의 핵심 모듈화된 버전으로, NeMo 같은 상위 플랫폼의 백엔드로도 활용돼요. 2025~2026년 로드맵에는 DeepSeek-V3, Qwen3 MoE 지원 및 FP8 최적화, Blackwell(H200/B200) 성능 강화가 포함되어 있어요.

**어디 쓰이나?** NVIDIA(자체), Naver, AI21, 그리고 NeMo를 쓰는 기업들 전반에 백엔드로 사용.

### 3.2 DeepSpeed (Microsoft)

[GitHub - microsoft/DeepSpeed](https://github.com/microsoft/DeepSpeed)

Microsoft Research에서 만든 분산 학습 최적화 라이브러리예요. ZeRO(Zero Redundancy Optimizer) 시리즈가 핵심이에요.

**ZeRO 단계별 비교:**

| 단계 | 분할 대상 | 메모리 절감 | 통신 오버헤드 |
|------|-----------|------------|--------------|
| ZeRO-1 | Optimizer States | ~4x | 낮음 |
| ZeRO-2 | + Gradients | ~8x | 중간 |
| ZeRO-3 | + Parameters | ~64x+ | 높음 |
| ZeRO-Infinity | + CPU/NVMe Offload | 거의 무제한 | 매우 높음 |

**2025년 주목 기능:**
- [DeepSpeed-MoE](https://github.com/microsoft/DeepSpeed): all-to-all 통신 최적화로 MoE 모델 학습 효율 대폭 개선
- Megatron-DeepSpeed: NVIDIA Megatron과 결합한 3D 병렬 학습 (MT-NLG 530B 모델 학습에 사용)

**어디 쓰이나?** Microsoft(Phi 시리즈), LLM 스타트업 전반, HuggingFace Accelerate 백엔드

### 3.3 PyTorch FSDP2 (Meta/PyTorch)

[PyTorch 공식 문서](https://pytorch.org/blog/maximizing-training/)

FSDP(Fully Sharded Data Parallel)는 Meta가 주도하여 PyTorch에 통합된 모델 샤딩 기법이에요. 2024년에 FSDP2가 나오면서 큰 변화가 생겼어요.

**FSDP vs FSDP2 비교:**

| 항목 | FSDP (v1) | FSDP2 |
|------|-----------|-------|
| 샤딩 단위 | 모듈 단위 | 파라미터(텐서) 단위 |
| 기반 | 자체 구현 | DTensor 기반 |
| 모델 병렬 조합 | 어려움 | Tensor Parallel과 쉽게 조합 |
| torch.compile | 제한적 | 완전 지원 |
| 코드 복잡도 | 높음 | 낮음 |

> "Unlike the original FSDP, FSDP2 manages sharding at the tensor level (via DTensor), allowing for granular control over memory layout." — PyTorch 공식 블로그
>
> 원래 FSDP와 달리 FSDP2는 DTensor를 통해 텐서 수준에서 샤딩을 관리하여, 메모리 레이아웃에 대한 세밀한 제어가 가능합니다.

SimpleFSDP(arXiv:2411.00284)라는 컴파일러 기반 변형도 등장했는데, Llama 3.1 405B 모델로도 테스트 완료됐어요.

### 3.4 JAX + GSPMD / XLA (Google)

[JAX GitHub](https://github.com/google/jax)

구글의 수치 계산 라이브러리 JAX와 그 위에 구축된 병렬화 컴파일러예요. TPU 환경에서 최고의 성능을 내고, GPU에서도 잘 작동해요.

**GSPMD (Generalized Sharding Propagation for Model Parallelism)**는 개발자가 샤딩 어노테이션만 달면 컴파일러가 알아서 최적 병렬화를 계산해줘요. 이 방식이 TensorFlow, PyTorch 방식과 근본적으로 달라서 러닝 커브가 있지만, 극도의 확장성을 제공해요.

**어디 쓰이나?** Google DeepMind(내부 모델 전반), Anthropic(추정), Google Brain 출신 연구자들

### 3.5 ColossalAI

[GitHub - hpcaitech/ColossalAI](https://github.com/hpcaitech/ColossalAI)

HPC-AI Tech에서 개발한 통합 대규모 모델 학습 시스템이에요. Megatron-LM, DeepSpeed의 기능을 통합하면서 자체적인 병렬화 전략과 Auto-Parallelism을 제공해요. 초기에는 매우 주목받았지만 2024~2025년에는 FSDP2, NeMo에 밀려 상대적으로 활용이 줄어드는 추세예요.

### 3.6 HAI-LLM (DeepSeek 자체 프레임워크)

DeepSeek-V3 Technical Report에서 공개된 내부 프레임워크예요. DualPipe라는 독자적인 파이프라인 병렬화 알고리즘을 포함하는데, 일반적인 1F1B 스케줄보다 파이프라인 버블을 줄이고 Tensor Parallelism 없이도 효율적인 학습이 가능하도록 설계됐어요. 현재까지는 외부 공개가 제한적이에요.

---

## 4. Layer 2: End-to-End 학습 플랫폼

이 계층은 Layer 1 위에서 "실제로 학습 돌리는" 환경을 제공해요. 데이터 로딩, 학습 레시피, 체크포인팅, 로깅 등을 통합하죠.

### 4.1 NVIDIA NeMo 2.0

[NeMo GitHub](https://github.com/NVIDIA/NeMo)

NVIDIA의 End-to-End 학습 플랫폼이에요. 2024년 NeMo 2.0으로 대규모 리팩토링을 거쳤고, 이제 모듈 구조로 분리됐어요:

- **NeMo**: 주로 음성/멀티모달 모델용 핵심 라이브러리
- **NeMo Automodel**: 허깅페이스 모델 파인튜닝
- **NeMo RL**: RL 포스트 트레이닝 (구 NeMo-Aligner 대체)
- **NeMo Gym**: 환경 평가
- **NeMo Curator**: 데이터 큐레이션

> "NeMo provides complete training recipes for established architectures, following published configurations and primarily targeting practitioners who pre-train models along well-established, low-risk paths." — LLM Engineering Stack Guide, 2026
>
> NeMo는 잘 확립된 아키텍처에 대한 완전한 학습 레시피를 제공하며, 검증된 설정을 따르는 실무자들을 주요 대상으로 합니다.

Megatron-Core를 백엔드로 사용하면서도 더 높은 추상화 수준을 제공해요.

### 4.2 TorchTitan (PyTorch 공식)

[TorchTitan GitHub](https://github.com/pytorch/torchtitan)

Meta/PyTorch 팀이 만든 LLM 사전학습 레퍼런스 구현체예요. ICLR 2025에 논문으로도 발표됐어요.

**핵심 특징:**
- FSDP2 + Tensor Parallel + Pipeline Parallel 조합 (4D 병렬)
- torch.compile 완전 통합
- FP8 혼합 정밀도 지원
- 분산 체크포인팅

Llama 3.1 계열로 테스트했을 때 512 GPU 기준 최적화 베이스라인 대비 최대 30% 성능 향상을 달성했어요.

**어디 쓰이나?** 연구소, 중소 규모 AI 팀, AWS에서 SageMaker 위에서 TorchTitan으로 Llama 사전학습 예제를 공식 제공해요.

### 4.3 LLM Foundry + Composer (Databricks/MosaicML)

[LLM Foundry GitHub](https://github.com/mosaicml/llm-foundry)

Databricks가 인수한 MosaicML의 오픈소스 학습 코드베이스예요. DBRX(MoE LLM)를 3,072개 H100에서 12조 토큰으로 학습하는 데 실제로 사용됐어요.

**구성:**
- **Composer**: PyTorch 기반 학습 라이브러리, 분산 학습 워크플로우 최적화
- **LLM Foundry**: Composer 위에서 LLM 학습/파인튜닝/평가
- **StreamingDataset**: 분산 학습을 위한 스트리밍 데이터셋 라이브러리

**어디 쓰이나?** Databricks 자체(DBRX 학습), Databricks 클라우드를 쓰는 기업들

### 4.4 MaxText / Pax (Praxis) (Google, JAX 기반)

[MaxText GitHub](https://github.com/google/maxtext) | [Pax GitHub](https://github.com/google/paxml)

Google의 JAX 기반 LLM 학습 프레임워크들이에요.

- **MaxText**: 단순하고 고성능인 JAX LLM 구현체. TPU 환경에서 높은 MFU를 달성해요. 오픈소스.
- **Pax (Paxml)**: 대규모 모델 학습을 위한 더 고급 프레임워크. 고급 실험 구성과 완전한 병렬화 지원. Google 내부에서 광범위하게 사용됐지만 외부 공개는 제한적.
- **T5X**: JAX 기반 T5 계열 학습 프레임워크. 2024~2025년 기준으로는 레거시 취급되는 추세.

### 4.5 Levanter (Stanford, JAX 기반)

[Levanter GitHub](https://github.com/stanford-crfm/levanter)

Stanford CRFM에서 만든 JAX 기반 학습 프레임워크예요. Haliax라는 명명된 텐서 라이브러리 위에 구축돼서 연구 친화적이에요. Palmyra, Meerkat 등 Stanford 연구 모델들이 이 프레임워크로 학습됐어요.

### 4.6 nanotron / picotron (HuggingFace)

[nanotron GitHub](https://github.com/huggingface/nanotron) | [picotron GitHub](https://github.com/huggingface/picotron)

HuggingFace의 경량 분산 학습 프레임워크예요.

- **nanotron**: 3D 병렬화 지원하는 미니멀한 LLM 학습 프레임워크. SmolLM 시리즈가 이걸로 학습됐어요.
- **picotron**: nanotron에서 발전한 4D 병렬화 지원 교육용 프레임워크. SmolLM-1.7B를 H100 8개로 학습할 때 MFU ~50% 달성.

HuggingFace 팀은 [Ultrascale Playbook](https://huggingface.co/spaces/nanotron/ultrascale-playbook)도 공개했는데, 대규모 분산 학습의 모든 기법을 정리한 필수 참고 자료예요.

### 4.7 Lingua (Meta, 연구용 공개 코드)

[Lingua GitHub](https://github.com/facebookresearch/lingua)

Meta Research에서 공개한 연구용 LLM 학습 코드예요. 내부 연구 파이프라인의 일부를 공개한 거예요. 프로덕션 학습 스택과는 다를 수 있어요.

---

## 5. Layer 3: Post-training / RLHF·RL 특화 프레임워크

2024~2025년 가장 뜨겁게 달아오른 영역이에요. 추론 모델(o1, R1류)의 부상으로 RL 포스트 트레이닝이 핵심 기술이 됐거든요.

### 5.1 veRL / HybridFlow (ByteDance Seed)

[veRL GitHub](https://github.com/verl-project/verl)

2025년 가장 주목받는 RL 학습 프레임워크예요. ByteDance Seed 팀이 개발했고, EuroSys 2025에 HybridFlow 논문으로 발표됐어요.

> "veRL is a flexible, efficient and production-ready RL training framework designed for large language models." — veRL 공식 README
>
> veRL은 대규모 언어 모델을 위한 유연하고 효율적인 프로덕션 레디 RL 학습 프레임워크입니다.

**지원 알고리즘:** PPO, GRPO, GSPO, DAPO, DrGRPO, REINFORCE++, RLOO, PRIME, KL_Cov & Clip_Cov

**Doubao-1.5-pro** (ByteDance의 최신 모델, AIME에서 70.0 pass@1, OpenAI O1급 수학 성능)이 veRL로 학습됐어요.

**지원 기관/기업:** Anyscale, ByteDance, LMSys.org, Shanghai AI Lab, Tsinghua, UC Berkeley, UCLA, UIUC, HKU

GitHub 스타 10,000+ 돌파, 현재 가장 빠르게 성장하는 RL 프레임워크예요.

**핵심 설계:** Hybrid-controller 모델로 training과 inference(vLLM/SGLang)을 효율적으로 분리/통합해요.

### 5.2 LlamaRL (Meta, 2025년 6월 공개)

[arXiv:2505.24034](https://arxiv.org/abs/2505.24034)

Meta가 2025년 6월에 공개한 비동기 RL 프레임워크예요. **Llama 3 포스트 트레이닝에 실제로 사용된** 프레임워크예요.

- 단일 컨트롤러 아키텍처, 순수 PyTorch 기반
- 비동기(async) RL로 trainer와 generator가 병렬 실행
- DeepSpeed-Chat 대비 405B 모델에서 **최대 10.7배 속도 향상**
- 수천 GPU 스케일에서 검증됨

### 5.3 OpenRLHF

[GitHub - OpenRLHF/OpenRLHF](https://github.com/OpenRLHF/OpenRLHF)

Ray + vLLM + DeepSpeed + HuggingFace Transformers 조합의 오픈소스 RLHF 프레임워크예요. EMNLP 2025 System Demonstrations에 논문으로 발표됐어요.

- 70B+ 모델 스케일까지 지원
- HuggingFace 체크포인트에서 바로 학습 가능 (모델 변환 불필요)
- 기존 SOTA 대비 1.22x~1.68x 속도 향상
- PPO, DAPO, REINFORCE++ 등 지원

멀티모달 버전인 **OpenRLHF-M**도 있어요.

### 5.4 NeMo-RL (NVIDIA)

[NeMo RL GitHub](https://github.com/NVIDIA-NeMo/RL)

NVIDIA의 포스트 트레이닝 RL 라이브러리예요. 구 NeMo-Aligner를 대체합니다. 2025년 5월 기준 v0.2.1 릴리즈, DAPO 알고리즘 지원, NVIDIA-Nemotron-3-Nano-30B-A3B-FP8 모델 학습에 사용됐어요.

### 5.5 slime (Tsinghua THUDM)

[GitHub - THUDM/slime](https://github.com/THUDM/slime)

Megatron-LM과 SGLang을 결합한 RL 포스트 트레이닝 프레임워크예요. 대규모 RL 스케일링에 특화돼 있어요. 2025년 신규 등장한 프레임워크 중 하나예요.

### 5.6 SkyRL (NovaSky-AI, UC Berkeley)

[GitHub - NovaSky-AI/SkyRL](https://github.com/NovaSky-AI/SkyRL)

모듈화된 Full-stack RL 라이브러리예요. 멀티-턴 에이전트 설정에 특화됐고, 동기/비동기 파이프라인, 공배치/분리형 생성 지원 등 다양한 설정을 지원해요.

### 5.7 Open-Instruct (AI2 / AllenAI)

[GitHub - allenai/open-instruct](https://github.com/allenai/open-instruct)

Allen AI의 포스트 트레이닝 코드베이스예요. Instruction Tuning과 RLHF, DPO 등을 지원하며, 연구 재현성을 중시한 설계예요.

### 5.8 파인튜닝 전용 도구 (소규모 파인튜닝·LoRA)

| 프레임워크 | 메인테이너 | 특징 | 최적 사용처 |
|-----------|-----------|------|------------|
| [TRL](https://github.com/huggingface/trl) | HuggingFace | SFT/RLHF/DPO 올인원 | 중소 규모 파인튜닝 |
| [LLaMA-Factory](https://github.com/hiyouga/LLaMA-Factory) | hiyouga | Web UI(LlamaBoard) 포함, 가장 높은 GitHub 스타 | 빠른 프로토타이핑 |
| [Axolotl](https://github.com/OpenAccess-AI-Collective/axolotl) | OpenAccess | 멀티 GPU 지원, Ring FlashAttention 시퀀스 병렬화 | 중소 멀티 GPU |
| [Unsloth](https://github.com/unslothai/unsloth) | unslothai | 단일 GPU 메모리 효율 최강, 2026년 MoE 12x 빠른 학습 | 단일/소수 GPU |
| [TorchTune](https://github.com/pytorch/torchtune) | PyTorch 공식 | PyTorch 공식 파인튜닝 레퍼런스 | 중소 규모 |
| [PEFT](https://github.com/huggingface/peft) | HuggingFace | LoRA, QLoRA 등 PEFT 기법 통합 | LoRA 파인튜닝 |

---

## 6. Layer 4: 오케스트레이션 & 실험 관리

### 6.1 Ray / Ray Train

[Ray 공식 사이트](https://docs.ray.io/)

분산 Python 실행 엔진이에요. Kubernetes와 Slurm 위 모두에서 실행 가능하고, 대부분의 RL 프레임워크(veRL, OpenRLHF)가 Ray를 기반으로 해요.

### 6.2 Slurm

고성능 컴퓨팅(HPC) 환경에서 사실상 표준인 잡 스케줄러예요. 대학 연구실, 국가 슈퍼컴퓨팅 센터, 그리고 많은 기업 GPU 클러스터가 Slurm으로 돌아가요. 포스트 트레이닝 연구자들이 가장 많이 쓰는 환경이기도 해요.

### 6.3 Kubeflow Training Operator

[GitHub - kubeflow/trainer](https://github.com/kubeflow/trainer)

Kubernetes 위에서 분산 학습을 오케스트레이션하는 도구예요. PyTorch, DeepSpeed, JAX, HuggingFace 등 다양한 프레임워크를 지원해요.

### 6.4 실험 관리

| 도구 | 용도 |
|------|------|
| Weights & Biases (W&B) | 학습 지표 추적, 하이퍼파라미터 관리 |
| MLflow | 오픈소스 ML 실험 추적 |
| Hydra / OmegaConf | 복잡한 설정 파일 관리 |
| TensorBoard | 기본 시각화 |

---

## 7. Layer 5: 데이터 파이프라인

좋은 데이터 없이는 좋은 모델도 없죠. 데이터 파이프라인도 중요한 계층이에요.

| 도구 | 메인테이너 | 특징 |
|------|-----------|------|
| [NeMo Curator](https://github.com/NVIDIA-NeMo/Curator) | NVIDIA | GPU 가속, 시맨틱 중복제거, PII 제거, RAPIDS 연동 |
| [Datatrove](https://github.com/huggingface/datatrove) | HuggingFace | 대규모 텍스트 처리, HuggingFace-NVIDIA 협업으로 NeMo Curator와 통합 추진 |
| [Dolma Toolkit](https://github.com/allenai/dolma) | AI2 (AllenAI) | Dolma 데이터셋 구축에 사용된 파이프라인 |
| [WebDataset](https://github.com/webdataset/webdataset) | tmbdev | tar 파일 기반 스트리밍, 범용 |
| [StreamingDataset](https://github.com/mosaicml/streaming) | MosaicML/Databricks | 분산 학습 최적화, MDS 포맷 |
| [Mixtera](https://github.com/eth-easl/mixtera) | ETH Zürich EASL | 데이터 혼합 비율 최적화 |

---

## 8. 기업별 채택 현황 총정리

### 8.1 프론티어 랩 / 빅테크

| 기업 | 사전학습 스택 | 포스트 트레이닝 | 데이터 파이프라인 | 오케스트레이션 | 비고 |
|------|-------------|----------------|-----------------|--------------|------|
| **NVIDIA** | Megatron-Core | NeMo-RL | NeMo Curator | Ray/Slurm | 자사 모든 스택 직접 개발 및 운영 |
| **Meta** | PyTorch 자체 + FSDP2 + 내부 스택 | LlamaRL (공개, 2025년 6월) | 자체 내부 도구 | 자체 | Llama 3 논문에서 FSDP 언급, LlamaRL 공개 |
| **Google DeepMind** | JAX + Pathways + Pax/Praxis + MaxText | 자체 내부 스택 | 자체 | 자체(TPU/Borg) | TPU 중심, GSPMD로 병렬화 |
| **OpenAI** | 비공개 (Triton 기반 커널 추정, 자체 분산 라이브러리) | 비공개 | 비공개 | 비공개 | 내부 정보 거의 없음 |
| **Anthropic** | JAX + 자체 스택 (추정) | 자체 | 자체 | 자체(AWS) | Claude 시리즈, 구체적 정보 없음 |
| **Microsoft** | DeepSpeed + Megatron-DeepSpeed | DeepSpeed-Chat / 자체 | 자체 | Azure ML | Phi 시리즈, MT-NLG 530B 학습에 Megatron-DeepSpeed 사용 |
| **DeepSeek** | HAI-LLM (자체 개발) + DualPipe | 자체 | 자체 | 자체 | 2048 H800로 671B DeepSeek-V3 학습 |
| **Mistral** | PyTorch 기반 추정, 자체 스택 | 자체 | 자체 | 자체 | 구체적 정보 공개 없음 |
| **Cohere** | 자체 학습 스택 | 자체 | 자체 | 자체 | 구체적 공개 정보 없음 |

### 8.2 중견 AI 기업 / 오픈소스 중심 기업

| 기업 | 사전학습 스택 | 포스트 트레이닝 | 비고 |
|------|-------------|----------------|------|
| **Databricks/MosaicML** | Composer + LLM Foundry + Megatron 변형 | LLM Foundry | DBRX 3072 H100에서 학습 |
| **HuggingFace** | nanotron / Megatron-LM 변형 | TRL + Accelerate | SmolLM 시리즈는 nanotron 사용 |
| **ByteDance (Seed)** | 자체 내부 스택 | veRL (오픈소스 공개) | Doubao 시리즈, veRL로 RL 학습 |
| **Qwen/Alibaba** | Megatron 변형 + 자체 | 자체 | Qwen 기술보고서에서 Megatron 기반 언급 추정 |
| **Tencent** | Angel-PTM (자체) + Angel-RL | Angel-RL | 10,000 카드 스케일 지원 |
| **AI21 Labs** | Megatron-LM 기반 추정 | 자체 | 구체적 공개 정보 없음 |
| **Yandex** | 자체 (YaLM 시절 Megatron 변형) | 자체 | 최근 동향 불분명 |

### 8.3 연구 기관 / 학계

| 기관 | 주요 사용 프레임워크 | 대표 모델/프로젝트 |
|------|------------------|-----------------|
| **Allen AI (AI2)** | PyTorch + Open-Instruct + Dolma | OLMo, Tulu |
| **Stanford CRFM** | Levanter (JAX) | Alpaca, Mistral 변형 |
| **UC Berkeley** | veRL, SkyRL, vLLM 생태계 | LMSys, LMSYS Chatbot Arena |
| **Tsinghua THUDM** | slime (Megatron+SGLang) + 자체 | ChatGLM, Qwen 기여 |

---

## 9. 한국 기업들은 뭘 쓸까?

### 9.1 Naver — HyperCLOVA X

[HyperCLOVA X 공식 HuggingFace](https://huggingface.co/naver-hyperclovax)

초기 HyperCLOVA(2021년)는 NVIDIA와 협력하여 **Megatron-LM 기반** 프레임워크로 학습됐어요. 82B 파라미터 모델을 NVIDIA GPU 클러스터에서 학습했고, 당시 GPT-3 수준의 한국어 특화 모델이었어요. HyperCLOVA X(2023년)와 이후 버전들은 내부 학습 인프라를 고도화했지만, 기반 기술은 Megatron 변형으로 추정돼요.

2025년 6월 공개된 **HyperCLOVA X THINK**는 추론 특화 모델로, 3단계 커리큘럼 학습(기초 → 강화 → 정제)을 거쳤어요. Naver는 자신들이 "진정한 AI 풀스택"을 갖춘 한국 유일의 기업이라고 주장해요.

### 9.2 LG AI Research — EXAONE

LG AI Research의 EXAONE 시리즈도 Megatron-LM 계열 기반의 자체 학습 인프라를 활용하는 것으로 알려져 있어요. EXAONE 4.0(2025년 7월)은 30B 파라미터 설계로 글로벌 벤치마크에서 경쟁력 있는 성능을 보여줬어요.

### 9.3 Upstage — SOLAR

Upstage의 SOLAR 시리즈는 HuggingFace 생태계(Transformers + Accelerate + FSDP)를 주로 활용하는 것으로 알려져 있어요. SOLAR 10.7B는 DUS(Depth Up-Scaling) 기법으로 주목받았어요.

### 9.4 KT / Kakao

KT와 Kakao도 자체 LLM을 개발하고 있지만, 학습 스택에 대한 구체적인 정보는 공개되지 않았어요. 대체로 HuggingFace 생태계 + 자체 조정 조합을 쓸 것으로 추정돼요.

---

## 10. 규모별 추천 가이드

### 10.1 대규모 GPU 클러스터 (수천~수만 GPU, 프론티어 랩 수준)

이 규모에서는 통신 효율과 병렬화 전략이 곧 학습 비용이에요.

| 요소 | 추천 |
|------|------|
| **분산 엔진** | Megatron-Core 또는 자체 개발 (DeepSeek식) |
| **병렬화 전략** | TP + PP + DP + EP (MoE용) 조합 |
| **RL 포스트트레이닝** | veRL 또는 자체 (LlamaRL처럼) |
| **데이터** | NeMo Curator 또는 자체 |
| **오케스트레이션** | 자체 스케줄러 또는 Slurm/Kubernetes |

**현실:** 이 규모에서는 대부분 자체 스택이에요. NVIDIA는 Megatron-Core + NeMo, Meta는 자체, Google은 JAX + Pathways, DeepSeek은 HAI-LLM.

### 10.2 중규모 GPU 클러스터 (수백~수천 GPU, 대기업 AI팀, AI 스타트업 시리즈 B+)

| 요소 | 추천 |
|------|------|
| **사전학습** | NeMo 2.0 (NVIDIA GPU) 또는 LLM Foundry |
| **분산 전략** | Megatron-DeepSpeed 또는 FSDP2 + Tensor Parallel |
| **RL 포스트트레이닝** | veRL 또는 OpenRLHF |
| **파인튜닝** | TRL + Accelerate 또는 Axolotl |
| **데이터** | NeMo Curator 또는 Datatrove |
| **오케스트레이션** | Ray + Slurm/Kubernetes |

**팁:** NeMo는 설정 기반으로 빠르게 시작할 수 있고, 검증된 레시피가 많아요. NVIDIA GPU 쓰는 곳이라면 1순위 고려.

### 10.3 소규모 GPU (수십 GPU, 스타트업 초기, 연구실)

| 요소 | 추천 |
|------|------|
| **사전학습/지속학습** | TorchTitan + FSDP2 또는 nanotron |
| **파인튜닝** | Axolotl (멀티 GPU) 또는 LLaMA-Factory |
| **SFT** | TRL + Accelerate |
| **RLHF/RL** | veRL (small scale) 또는 OpenRLHF |
| **실험 관리** | W&B + Hydra |

**팁:** TorchTitan은 ICLR 2025 논문으로 검증된 레퍼런스 구현체고, PyTorch 공식이라 장기 유지보수 걱정이 적어요.

### 10.4 POC / 파인튜닝 전용 (수 GPU, 개인 프로젝트, 검증 단계)

| 목적 | 추천 도구 |
|------|----------|
| **빠른 SFT 시작** | LLaMA-Factory (Web UI 있음) |
| **LoRA 파인튜닝** | Unsloth (단일 GPU 메모리 효율 최고) |
| **멀티 GPU LoRA** | Axolotl 또는 TRL + PEFT |
| **RLHF 실험** | TRL (GRPOTrainer) |
| **설정 관리** | Hydra + W&B |

**팁:** Unsloth는 단일 GPU에서 타 도구 대비 2~3x 빠른 학습이 가능하고, 메모리도 훨씬 적게 써요. 단, 오픈소스 버전에서는 멀티 GPU 지원이 제한적이에요.

### 10.5 규모별 스택 요약표

| 규모 | GPU 수 | 사전학습 | 파인튜닝/SFT | RL/RLHF | 대표 기업 |
|------|--------|---------|------------|---------|---------|
| Frontier | 10K+ | Megatron-Core / JAX / 자체 | 자체 | 자체 (LlamaRL 등) | NVIDIA, Meta, Google, OpenAI |
| Large | 1K~10K | NeMo / LLM Foundry / Megatron-DS | TRL, Axolotl | veRL, OpenRLHF | Databricks, 대형 AI 스타트업 |
| Medium | 100~1K | TorchTitan / nanotron / NeMo | TRL, Axolotl | veRL, OpenRLHF | AI 스타트업, 기업 AI팀 |
| Small | 10~100 | TorchTitan / HF Accelerate+FSDP | LLaMA-Factory, Axolotl | TRL (GRPO) | 연구실, 스타트업 초기 |
| Micro | 1~10 | — | Unsloth, LLaMA-Factory | TRL | 개인, POC |

---

## 11. 2025~2026 주요 트렌드

### 11.1 veRL의 급부상: RL 인프라 표준화 경쟁

추론 모델(o1, R1, QwQ 등)의 폭발적 성장으로 **RL 포스트 트레이닝 인프라**가 핵심 경쟁력이 됐어요. veRL이 EuroSys 2025에 논문 발표, 10K+ 스타, 다양한 기관의 채택으로 빠르게 표준화되는 중이에요.

동시에 slime(Megatron+SGLang), SkyRL, AReaL, LlamaRL 등 경쟁 프레임워크들도 속속 등장하고 있어요. 이 공간은 2025~2026년 가장 빠르게 변화하는 영역이에요.

### 11.2 FSDP2 + torch.compile의 안착

PyTorch 2.x 시대에 FSDP2와 torch.compile의 조합이 사실상 "중소 규모의 기본 스택"이 되어가고 있어요. SimpleFSDP(arXiv:2411.00284) 같은 컴파일러 기반 접근도 405B 규모에서 검증됐어요.

### 11.3 JAX 생태계의 견고함

구글 계열과 Anthropic의 핵심 스택인 JAX는 TPU 환경에서 계속 독보적인 위치를 지켜요. MaxText의 오픈소스 공개, Levanter의 성장으로 JAX 생태계도 확장 중이에요.

### 11.4 MoE 모델 지원 고도화

DeepSeek-V3, Qwen3, Mixtral 등 MoE(Mixture of Experts) 아키텍처가 대세가 되면서, **Expert Parallelism**과 **all-to-all 통신 최적화**가 모든 주요 프레임워크의 핵심 개발 과제가 됐어요. Megatron-LM, DeepSpeed-MoE, veRL 모두 MoE 지원을 강화하고 있어요.

### 11.5 Inference-Training 경계 허물기

RL 학습에서 rollout generation이 병목이 되면서, vLLM과 SGLang 같은 추론 엔진이 학습 파이프라인 안으로 들어왔어요. veRL, OpenRLHF, slime 모두 vLLM/SGLang을 rollout 엔진으로 활용해요.

### 11.6 FP8 학습의 보편화

FP8 혼합 정밀도 학습이 DeepSeek-V3에서 전면 채택되면서 주목받았어요. NVIDIA의 Transformer Engine과 PyTorch의 FP8 지원이 성숙해지면서, FP8이 2025~2026년 대규모 학습의 새로운 기본값이 되어가는 중이에요.

---

## 12. 의사결정 트리: 나에게 맞는 스택 고르기

```
내 상황은?
│
├── GPU 10,000개 이상이고 자체 R&D 역량이 있음
│   └── Megatron-Core 기반 자체 스택 개발 (또는 JAX+Pathways)
│       RL 포스트트레이닝: 자체 (LlamaRL 참고) 또는 veRL
│
├── GPU 수백~수천 개, NVIDIA 하드웨어 사용
│   └── NeMo 2.0 (가장 검증된 End-to-End 플랫폼)
│       RL이 필요하다면: NeMo-RL 또는 veRL
│       데이터: NeMo Curator
│
├── GPU 수십~수백 개, PyTorch 중심 팀
│   ├── 사전학습 필요: TorchTitan + FSDP2 (ICLR 2025 검증)
│   ├── 파인튜닝만: Axolotl (멀티 GPU) 또는 LLaMA-Factory
│   └── RL 실험: veRL (small scale config) 또는 OpenRLHF
│
├── GPU 수 개~수십 개, POC/스타트업 초기
│   ├── SFT 파인튜닝: LLaMA-Factory (Web UI로 빠른 시작)
│   ├── LoRA 파인튜닝: Unsloth (단일 GPU) 또는 Axolotl (멀티)
│   └── RLHF 실험: HuggingFace TRL (GRPOTrainer)
│
└── 단일 GPU, 개인/실험
    └── Unsloth + PEFT (LoRA/QLoRA)
        또는 LLaMA-Factory (설정 쉬움)
```

---

## 13. 결론

LLM 학습 프레임워크의 세계는 빠르게 변하고 있지만, 몇 가지 큰 흐름은 분명해요:

1. **"풀스택 자체 개발"은 프론티어 랩만의 선택**: NVIDIA, Meta, Google, DeepSeek처럼 극단적 규모의 기업들만이 자체 프레임워크를 만들어요. 나머지는 오픈소스 생태계를 잘 활용하는 게 맞아요.

2. **중규모 기업의 사실상 표준은 NeMo + veRL**: NVIDIA GPU 환경에서 검증된 레시피를 빠르게 쓰고 싶다면 NeMo가 최선이에요. RL 포스트트레이닝은 veRL이 빠르게 표준화되는 중이에요.

3. **소규모에서는 TorchTitan + Axolotl + TRL 조합**: PyTorch 공식 지원, 커뮤니티 지원, 검증된 사례가 모두 있어요.

4. **RL 인프라가 모델 경쟁력을 좌우하는 시대**: veRL, LlamaRL, slime 등 RL 프레임워크의 선택이 추론 모델 품질에 직결돼요. 이 영역을 계속 주목해야 해요.

5. **데이터 파이프라인을 무시하지 말 것**: NeMo Curator 같은 GPU 가속 데이터 처리 도구가 학습 품질에 7%+ 영향을 미친다는 연구 결과도 있어요.

프레임워크는 수단이에요. 내 팀의 GPU 수, 엔지니어링 역량, 목표 모델 규모에 맞게 고르는 게 최선이에요.

---

## 14. 참고문헌

1. [NVIDIA Megatron-LM GitHub](https://github.com/NVIDIA/Megatron-LM) — NVIDIA, Ongoing
2. [DeepSeek-V3 Technical Report](https://arxiv.org/html/2412.19437v1) — DeepSeek, 2024.12
3. [veRL: HybridFlow Paper (EuroSys 2025)](https://github.com/verl-project/verl) — ByteDance Seed, 2025
4. [TorchTitan: ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/e6231c5f46598cfd09ff1970524e0436-Paper-Conference.pdf) — Meta/PyTorch, 2025
5. [LlamaRL: arXiv:2505.24034](https://arxiv.org/abs/2505.24034) — Meta, 2025.05
6. [NeMo RL Documentation](https://docs.nvidia.com/nemo/rl/latest/index.html) — NVIDIA, 2025
7. [SimpleFSDP: arXiv:2411.00284](https://arxiv.org/pdf/2411.00284) — Meta, 2024.11
8. [OpenRLHF: ACL Anthology EMNLP 2025](https://aclanthology.org/2025.emnlp-demos.48/) — 2025
9. [LLM Foundry GitHub](https://github.com/mosaicml/llm-foundry) — Databricks/MosaicML
10. [HuggingFace nanotron](https://github.com/huggingface/nanotron) — HuggingFace
11. [HuggingFace picotron](https://github.com/huggingface/picotron) — HuggingFace
12. [Pax GitHub](https://github.com/google/paxml) — Google
13. [Axolotl vs Unsloth vs TorchTune 비교](https://www.spheron.network/blog/axolotl-vs-unsloth-vs-torchtune/) — Spheron, 2026
14. [Fine-tuning Frameworks Comparison](https://modal.com/blog/fine-tuning-llms) — Modal, 2025
15. [Angel-PTM: Tencent Pre-training](https://arxiv.org/abs/2303.02868) — Tencent, 2023
16. [NeMo Curator Developer Page](https://developer.nvidia.com/nemo-curator) — NVIDIA, 2025
17. [slime GitHub (THUDM)](https://github.com/THUDM/slime) — Tsinghua THUDM, 2025
18. [SkyRL GitHub (NovaSky-AI)](https://github.com/NovaSky-AI/SkyRL) — NovaSky-AI/UC Berkeley, 2025
19. [Open-Instruct GitHub (AI2)](https://github.com/allenai/open-instruct) — AllenAI, Ongoing
20. [HyperCLOVA X HuggingFace](https://huggingface.co/naver-hyperclovax) — Naver, 2025
21. [Kubeflow Trainer GitHub](https://github.com/kubeflow/trainer) — Kubeflow, 2025
22. [Ray for ML Infrastructure](https://docs.ray.io/en/latest/ray-air/getting-started.html) — Anyscale/Ray, 2025
23. [Open Source RL Libraries for LLMs - Anyscale](https://www.anyscale.com/blog/open-source-rl-libraries-for-llms) — Anyscale, 2025
24. [The 2026 AI Engineering Stack Guide](https://www.tiptinker.com/llm-frameworks/) — TipTinker, 2026
