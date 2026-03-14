# 3D Gaussian Splatting 완전 정복: 사진 몇 장으로 포토리얼한 3D 세계를 만드는 기술

> 작성일: 2026-03-14
> 난이도: 입문 ~ 중급 (컴퓨터 그래픽스 비전공자 환영)

---

솔직히 처음 "3D Gaussian Splatting"이라는 이름을 들었을 때 뭔가 엄청 어렵고 복잡한 수학 얘기 같잖아요. "가우시안"이면 정규분포 곡선 아닌가? "스플래팅"은 또 뭐야? 하는 생각이 드는 게 정상이에요.

근데 이 기술, 알고 나면 진짜 신기하거든요. 스마트폰으로 방 사진 몇 장 찍으면 → 그걸 포토리얼한 3D 공간으로 만들어줘요. 심지어 실시간으로요. 영화 VFX팀이 몇 주 걸려서 하던 걸, 이제 몇 분 만에 할 수 있어요.

오늘은 기초 개념부터 차근차근 풀어볼게요.

---

## 목차

1. [3D 렌더링의 기초: 컴퓨터는 어떻게 3D를 그리나요?](#1-3d-렌더링의-기초)
2. [NeRF: AI가 3D 공간을 배우다](#2-nerf-neural-radiance-fields)
3. [3D Gaussian Splatting의 핵심 원리](#3-3d-gaussian-splatting-핵심-원리)
4. [NeRF vs 3DGS: 어디가 어떻게 다른가?](#4-nerf-vs-3dgs-비교)
5. [최신 발전 동향 (2024-2026)](#5-최신-발전-동향)
6. [실제 활용 사례](#6-실제-활용-사례)
7. [주요 오픈소스 도구들](#7-주요-오픈소스-도구들)
8. [현재 한계점과 미래 전망](#8-한계점과-미래-전망)

---

## 1. 3D 렌더링의 기초

### 컴퓨터는 어떻게 3D 장면을 화면에 그릴까요?

먼저 아주 기본적인 것부터 시작할게요. 우리가 게임을 하거나 3D 애니메이션을 볼 때, 컴퓨터는 어떻게 그 3D 장면을 2D 화면에 표시하는 걸까요?

크게 두 가지 방법이 있어요.

---

### 래스터화 (Rasterization) — "빠른 근사"

래스터화는 지금 게임에서 가장 많이 쓰는 방식이에요.

> "Rasterization is a technique that has long been used in real-time computer graphics to display three-dimensional objects on a two-dimensional screen. With rasterization, objects on the screen are created from a mesh of virtual triangles, or polygons, that create 3D models of objects." — [NVIDIA Blog](https://blogs.nvidia.com/blog/whats-difference-between-ray-tracing-rasterization/)

쉽게 말하면: **3D 물체를 수천 개의 삼각형으로 쪼개서 → 화면에 투영(projection)하는 방법**이에요.

어떻게 동작하냐면:
1. 3D 물체를 작은 삼각형(폴리곤)으로 분해해요
2. 각 삼각형의 꼭짓점을 카메라 시점에서 2D 화면으로 투영해요
3. 삼각형 내부 픽셀을 색상으로 채워요

**장점**: 엄청 빠르다! GPU가 이걸 병렬 처리하기에 최적화되어 있어서, 게임이 초당 60~120프레임으로 돌아가는 거예요.

**단점**: 반사, 굴절, 그림자 같은 빛의 물리적 현상을 정확하게 표현하기 어려워요. 그래서 게임에서 그림자가 좀 어색해 보이는 경우가 있죠.

---

### 레이 트레이싱 (Ray Tracing) — "느리지만 정확한 물리"

레이 트레이싱은 정반대로, **빛의 물리 법칙을 시뮬레이션**하는 방법이에요.

> "Ray tracing is a rendering technique that can realistically simulate the lighting of a scene and its objects by rendering physically accurate reflections, refractions, shadows, and indirect lighting. It generates computer graphics images by tracing the path of light from the view camera through the 2D viewing plane out into the 3D scene, and back to the light sources." — [Scratchapixel](https://www.scratchapixel.com/lessons/3d-basic-rendering/ray-tracing-overview/ray-tracing-rendering-technique-overview.html)

원리:
1. 카메라에서 각 픽셀 방향으로 "광선(ray)"을 쏴요
2. 광선이 어떤 물체에 맞으면, 거기서 또 광선이 반사/굴절돼요
3. 광원까지 추적하면서 최종 색상을 계산해요

**장점**: 유리잔의 굴절, 금속의 반사, 자연스러운 그림자 — 모두 물리적으로 정확해요. 픽사나 드림웍스 애니메이션의 그 사실적인 빛이 이렇게 나오는 거예요.

**단점**: 계산량이 어마어마해요. 영화 한 프레임 렌더링하는 데 몇 분~몇 시간이 걸려서, 농장처럼 서버 수백 대를 묶어놓은 "렌더 팜"이 필요해요.

---

### 전통적 3D 파이프라인의 한계

자, 그러면 전통 방식으로는 이런 과정이 필요해요:

1. 3D 아티스트가 모델링 소프트웨어로 물체를 직접 만들기
2. UV 언래핑 (텍스처 좌표 지정)
3. 텍스처 페인팅
4. 재질(Material) 설정
5. 리깅 & 애니메이션

이 과정이 엄청나게 시간과 돈이 들어요. 게임 하나 만드는 데 수백 명의 아티스트가 몇 년씩 일하는 게 이 과정 때문이에요.

그러면... **현실 세계를 그냥 사진으로 찍어서 3D로 변환할 수는 없을까?** 바로 이 질문에서 NeRF가 탄생해요.

---

## 2. NeRF: Neural Radiance Fields

### "AI야, 이 사진들 보고 3D 공간 이해해봐"

2020년, UC 버클리와 구글 리서치 연구팀이 엄청난 논문을 발표해요. 바로 [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/abs/2003.08934)예요.

> "A neural radiance field (NeRF) is a neural network that can reconstruct complex three-dimensional scenes from a partial set of two-dimensional images. The NeRF algorithm represents a scene as a radiance field parametrized by a deep neural network." — [AWS](https://aws.amazon.com/what-is/neural-radiance-fields/)

핵심 아이디어가 뭐냐면:

**"3D 공간의 모든 점(x, y, z)에서, 특정 방향으로 볼 때의 색상과 불투명도(opacity)를 신경망이 학습하게 하자"**

### NeRF는 어떻게 동작하나요?

1. 같은 물체를 여러 각도에서 찍은 사진 수십~수백 장을 준비해요
2. 신경망(MLP: 다층 퍼셉트론)이 이 사진들을 학습해요
3. 학습이 끝나면, **학습에 없던 새로운 각도에서 본 모습도 생성**할 수 있어요!

이걸 "Novel View Synthesis(새로운 시점 합성)"라고 해요.

### NeRF가 혁신적인 이유

기존 방법들은 3D 모델을 명시적으로(explicitly) 만들어야 했어요. 근데 NeRF는 신경망 가중치 안에 3D 공간 정보를 **암묵적으로(implicitly)** 저장해요.

진짜 재밌는 건, NeRF가 한 번 학습되면 그 신경망 자체가 곧 3D 장면이에요. 모델 파일 하나가 3D 세계 전체예요.

### NeRF의 한계

근데 솔직히 NeRF에는 치명적인 단점이 있었어요:

| 문제점 | 내용 |
|--------|------|
| **느린 학습** | 장면 하나 학습하는 데 수 시간~수십 시간 |
| **느린 렌더링** | 초당 5프레임도 안 나옴 (실시간 불가능) |
| **고정된 장면** | 움직이는 물체 처리 어려움 |
| **조명 변화 취약** | 다른 시간/날씨에 찍은 사진 섞기 어려움 |

2020~2023년 동안 Instant-NGP (NVIDIA), mip-NeRF 360 등 NeRF 변형 모델들이 쏟아졌지만, 근본적인 속도 문제는 해결이 어려웠어요.

그러던 중 2023년 8월, 완전히 다른 접근법이 등장해요.

---

## 3. 3D Gaussian Splatting 핵심 원리

### "가우시안"이 뭔데요?

먼저 "가우시안(Gaussian)"이 뭔지 알아야 해요. 통계 시간에 배운 **정규분포(Normal Distribution)**가 바로 가우시안이에요.

종 모양 곡선, 기억나죠? 가운데가 제일 높고, 양쪽으로 갈수록 부드럽게 낮아지는 그 곡선이요.

3D Gaussian은 이걸 3차원으로 확장한 거예요. 즉:
- 3D 공간에 떠 있는 **부드러운 타원형 물체** 같은 거예요
- 중심에서 멀어질수록 부드럽게 투명해져요
- 방향에 따라 길쭉하게 혹은 납작하게 늘릴 수 있어요

> "Gaussian in 3D Gaussian Splatting is a 3D primitive described by four key parameters: Position (XYZ), Covariance (3×3 matrix), Color (RGB), Alpha (α)" — [Hugging Face Blog](https://huggingface.co/blog/gaussian-splatting)

각 가우시안 하나는 이런 정보를 가져요:

| 속성 | 의미 |
|------|------|
| **위치 (x, y, z)** | 3D 공간에서의 위치 |
| **공분산 행렬 (3×3)** | 크기, 방향, 형태 (길쭉한지, 납작한지) |
| **색상 (RGB + 구면 조화)** | 보는 방향에 따른 색상 |
| **불투명도 (α)** | 얼마나 투명한지 |

### "스플래팅"이 뭔데요?

스플래팅(Splatting)은 이 3D 가우시안들을 화면에 **"찍어내는(stamp)"** 과정이에요.

물감을 붓으로 그리는 대신 도장을 쾅 찍는 느낌이랄까요.

> "Splatting is a rasterization technique that draws Gaussians to the screen. It's analogous to triangle rasterization but uses Gaussians as primitives instead of triangles." — [Hugging Face Blog](https://huggingface.co/blog/gaussian-splatting)

구체적으로 어떻게 동작하냐면:

1. **3D 가우시안 → 2D 투영**: 카메라 시점에서 각 3D 가우시안을 2D 타원형으로 투영(project)해요
2. **깊이 정렬**: 카메라에서 가까운 것부터 멀리 있는 것 순서로 정렬해요
3. **알파 블렌딩**: 픽셀마다 앞에서 뒤 순서로 가우시안들을 반투명하게 겹쳐 그려요

이게 전통 래스터화와 비슷하지만, 삼각형 대신 부드러운 가우시안 덩어리를 쓰는 거예요.

---

### 3DGS는 어떻게 학습하나요?

아주 명쾌한 파이프라인이에요. [원본 논문](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/)을 참고해서 설명할게요.

**Step 1: 사진 수집 + COLMAP**

여러 각도에서 찍은 사진들을 COLMAP이라는 소프트웨어로 처리해요. COLMAP이 각 사진에서 카메라 위치를 추정하고, 희박한 3D 점구름(sparse point cloud)을 만들어요.

**Step 2: 점구름 → 초기 가우시안**

각 점을 초기 가우시안으로 변환해요. 처음에는 작고 둥근 가우시안들이에요.

**Step 3: 반복 최적화**

```
반복:
  1. 현재 가우시안들을 카메라 시점에서 렌더링
  2. 렌더링 결과 vs 실제 사진 비교 (손실 계산)
  3. 가우시안 파라미터 조정 (경사하강법)
  4. 밀도 조절:
     - 에러가 큰 작은 가우시안 → 복제(clone)
     - 에러가 큰 큰 가우시안 → 분할(split)
     - 투명도 낮은 가우시안 → 제거(prune)
```

> "Uses Stochastic Gradient Descent (SGD) without neural network layers — the Gaussians themselves are optimized directly via backpropagation through differentiable rasterization." — [Hugging Face Blog](https://huggingface.co/blog/gaussian-splatting)

흥미로운 점: NeRF와 달리 3DGS는 신경망(Neural Network)을 거의 안 써요. 최적화 과정이 신경망처럼 학습하는 것처럼 보이지만, 실제로는 가우시안 파라미터들을 직접 최적화하는 거예요.

**Step 4: 최종 결과**

학습이 끝나면 수백만 개의 가우시안들이 장면을 표현해요. 보통 한 장면에 약 **700만 개** 정도의 가우시안이 사용돼요.

---

### 구면 조화 함수 (Spherical Harmonics): 색상이 방향에 따라 달라지는 이유

가우시안의 색상이 단순 RGB로 저장되지 않는다는 사실, 알고 계셨나요?

실제 세계에서 물체의 색상은 보는 방향에 따라 달라져요. 금속 공을 생각해봐요 — 각도에 따라 하이라이트가 달라지잖아요. 이런 현상을 **뷰 의존적 색상(View-Dependent Color)**이라고 해요.

3DGS는 이를 **구면 조화 함수(Spherical Harmonics)**라는 수학적 도구로 표현해요. 쉽게 생각하면, "보는 방향마다 다른 색상 값"을 저장하는 함수예요. 덕분에 금속이나 유리 같은 재질의 하이라이트도 어느 정도 표현 가능해요.

---

## 4. NeRF vs 3DGS 비교

자, 이제 두 방법을 비교해볼게요. 솔직히 이게 핵심이거든요.

### 철학의 차이

| 관점 | NeRF | 3D Gaussian Splatting |
|------|------|----------------------|
| **표현 방식** | 암묵적(Implicit) — 신경망 가중치 | 명시적(Explicit) — 가우시안 집합 |
| **렌더링** | 볼류메트릭 레이 마칭 (느림) | 래스터화 (빠름) |
| **학습 시간** | 수 시간 ~ 하루 | 수십 분 |
| **렌더링 속도** | ~5 FPS | 100+ FPS |
| **수정 가능성** | 어려움 | 가우시안 직접 편집 가능 |
| **저장 공간** | 신경망 가중치 (비교적 작음) | 수백만 가우시안 (수 GB) |

### 속도 혁명

> "3DGS uses explicit Gaussians that can be rendered using GPU rasterization — a much faster operation that enables 100+ FPS on consumer hardware. 3DGS completed the reconstruction in just over 42 minutes, while NeRF required more than 74 minutes." — [PyImageSearch](https://pyimagesearch.com/2024/12/09/3d-gaussian-splatting-vs-nerf-the-end-game-of-3d-reconstruction/)

이 차이가 얼마나 큰지 감이 오시나요?
- NeRF: 초당 5프레임 → 영상이 뚝뚝 끊겨요
- 3DGS: 초당 100프레임 이상 → 부드러운 실시간 렌더링!

VR 기기는 최소 90FPS가 필요해요. NeRF로는 VR이 사실상 불가능했지만, 3DGS로는 가능해졌어요.

### 화질은?

> "Gaussian Splatting combines strengths from both approaches: the best of both photogrammetry and NeRFs by using a differentiable process while having the explicit 3D Gaussians." — [PyImageSearch](https://pyimagesearch.com/2024/12/09/3d-gaussian-splatting-vs-nerf-the-end-game-of-3d-reconstruction/)

화질 면에서도 3DGS가 NeRF에 뒤지지 않아요. 심지어 어떤 장면에서는 더 좋기도 해요.

---

## 5. 최신 발전 동향 (2024-2026)

3DGS는 2023년 등장 이후 폭발적으로 발전하고 있어요. 2024-2026년 사이에 어떤 혁신들이 있었는지 살펴볼게요.

### 5.1 4D Gaussian Splatting: 움직임을 더하다

3DGS의 큰 한계 중 하나가 "정적인 장면"만 다룬다는 거였어요. 사람이 걸어다니거나, 나뭇잎이 흔들리거나, 물이 흐르는 장면은 어떻게 할까요?

여기서 등장한 게 **4D Gaussian Splatting**이에요.

> "4D Gaussian Splatting for Real-Time Dynamic Scene Rendering proposes 4D-GS as a holistic representation for dynamic scenes rather than applying 3D-GS for each individual frame. The method achieves real-time rendering at 82 FPS with 800×800 resolution on an RTX 3090 GPU." — [CVPR 2024, arXiv:2310.08528](https://arxiv.org/abs/2310.08528)

4D = 공간(X, Y, Z) + 시간(T). 가우시안에 시간 차원을 더해서, 각 가우시안이 시간에 따라 어떻게 움직이는지 학습해요.

| 방법 | 렌더링 속도 |
|------|-----------|
| 4D-GS (CVPR 2024) | 82 FPS (RTX 3090) |
| 4D-Rotor GS (NVIDIA) | 277 FPS (RTX 3090), 583 FPS (RTX 4090) |
| MEGA (ICCV 2025) | 0.91M 가우시안으로 처리 (기존 13M 대비 93% 감소) |

특히 [MEGA](https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_MEGA_Memory-Efficient_4D_Gaussian_Splatting_for_Dynamic_Scenes_ICCV_2025_paper.pdf)는 가우시안 수를 획기적으로 줄이면서 메모리 문제를 해결했어요.

### 5.2 대규모 장면: 도시 전체를 3DGS로

초기 3DGS는 작은 물체나 좁은 실내 공간에 적합했어요. 근데 이제는 도시 전체를 렌더링하는 연구도 나왔어요!

- **[CityGaussian](https://arxiv.org/abs/2404.01133)**: "분할 후 정복(Divide-and-Conquer)" 전략 + Level-of-Detail로 대규모 야외 장면 실시간 렌더링
- **[LODGE](https://arxiv.org/html/2505.23158v2)**: 메모리 제한 기기에서도 대규모 장면 실시간 렌더링 가능
- **[GaussianCity (CVPR 2025)](https://openaccess.thecvf.com/content/CVPR2025/papers/Xie_Generative_Gaussian_Splatting_for_Unbounded_3D_City_Generation_CVPR_2025_paper.pdf)**: 무한한 3D 도시 생성

### 5.3 생성형 AI와의 결합

Text-to-3D, Image-to-3D 분야에서도 3DGS가 핵심 역할을 해요.

- **DreamGaussian**: 텍스트 프롬프트 → 3D Gaussian 장면 생성
- **GaussianEditor**: 텍스트로 3D 장면 편집 ("나무를 금으로 바꿔줘")
- **Splatt3R**: 단 2장의 사진만으로 3D 재구성

### 5.4 표준화의 시작

> "August 2025 brought a watershed: Khronos + OGC announced adding 3D Gaussian Splats to the glTF ecosystem, with SPZ as a compact container." — [Medium](https://medium.com/@qsibmini123/gaussian-splats-are-becoming-the-jpeg-of-3d-why-2025-is-the-breakout-year-ac841ed39440)

Niantic이 개발한 `.SPZ` 포맷은 3D Gaussian Splat의 JPEG처럼, 고압축 표준 포맷이 되어가고 있어요. 2025년 8월, Khronos 그룹(OpenGL, Vulkan 표준 기관)이 glTF 생태계에 3DGS를 통합하기로 발표하면서 표준화에 박차가 가해지고 있어요.

---

## 6. 실제 활용 사례

### 6.1 영화 & VFX 산업

> "Gracia AI secured $1.7M to scale its 4D Gaussian Splatting tools, bringing photorealistic volumetric video to standalone VR and Hollywood production." — [StartupHub.ai](https://www.startuphub.ai/ai-news/funding-round/2025/4d-gaussian-splatting-tools-just-got-1-7m-for-hollywood-scale/)

영화 촬영지를 스캔해서 → 가상 세트로 활용할 수 있어요.

> "In film or television production where location environments are recreated digitally, every surface, shadow, and reflection can be rendered with the realism of live footage, yet adjustable in real time." — [Global Film Industry News](https://www.globalfilmindustry.news/gaussian-splatting-the-breakthrough-making-photorealistic-3d-mainstream/)

Gracia AI는 초당 50프레임으로 촬영한 영상을 처리해서 슬로우 모션으로도 아티팩트 없이 재생 가능한 기술을 개발했어요. 스포츠 중계나 액션 영화에 딱이죠.

### 6.2 게임 개발

> "3D Gaussian Splatting transforms real-world light into real-time game assets. Key advantages: Topology-Free (no retopology or UV unwrapping needed), Photorealistic Lighting, Real-Time Rendering." — [KIRI Engine](https://www.kiriengine.app/blog/3DGaussianSplatting_GameDevelopment)

3DGS를 쓰면:
- 실제 물체를 사진 찍어 → 게임 에셋으로 바로 변환
- UV 언래핑, 리토폴로지 작업이 필요 없음
- 현실 조명이 그대로 캡처되어 자연스러운 PBR 재질 효과

포켓몬 GO 개발사 Niantic은 ["Splats Change Everything"](https://nianticlabs.com/news/splats-change-everything?hl=en) 블로그에서 AR 게임 개발에 이 기술을 활발히 활용하고 있다고 밝혔어요.

### 6.3 자율주행

> "SplatAD enables real-time, high-quality rendering for both camera and lidar, achieving competitive performance within minutes. Dynamic driving scene reconstruction is of great importance in digital twin systems and autonomous driving simulation." — [SplatAD, arXiv](https://arxiv.org/html/2411.16816v3)

자율주행 개발에서 가장 비싸고 위험한 부분이 실제 도로 주행 테스트예요. 3DGS를 쓰면:

- 실제 도로를 스캔해서 → 완전히 사실적인 시뮬레이션 환경 구축
- 카메라 + LiDAR 센서 데이터를 동시에 렌더링
- 다양한 날씨/조명 조건 시뮬레이션

[VR-Drive (arXiv 2025)](https://arxiv.org/abs/2510.23205)는 3DGS 기반 시뮬레이션으로 자율주행 모델을 end-to-end로 학습시키는 연구예요.

### 6.4 VR/AR 및 디지털 트윈

> "Material-informed Gaussian Splatting for 3D World Reconstruction in a Digital Twin — a camera-only pipeline reconstructs scenes using 3D Gaussian Splatting from multi-view images, extracts semantic material masks via vision models, and converts Gaussian representations to mesh surfaces with projected material labels." — [arXiv 2511.20348](https://arxiv.org/abs/2511.20348)

제조업 디지털 트윈에서는:
- 공장 내부를 3DGS로 스캔
- 실시간으로 설비 배치 변경 시뮬레이션
- 재질 정보까지 포함한 정밀 디지털 모델 구축

[GSAVS](https://arxiv.org/html/2412.18816v1)는 도로, 건물, 차량까지 모든 에셋을 3DGS로 구성한 자율주행 시뮬레이터예요.

### 6.5 문화유산 디지털 보존

> "Beyond Digital Twins: 3D Gaussian Splatting, Game Engines and Crossmedia Cultural Heritage Representations" — [ACM SIGGRAPH 2025](https://dl.acm.org/doi/10.1145/3721239.3734094)

고대 유적이나 예술 작품을 3DGS로 스캔해서 디지털로 보존하는 연구도 활발해요. 파손되거나 분실 위험이 있는 유물을 사진 몇 장으로 완벽하게 디지털 보존할 수 있어요.

---

## 7. 주요 오픈소스 도구들

직접 써보고 싶다면 이런 도구들이 있어요!

### 학습/훈련 도구

| 도구 | 설명 | 링크 |
|------|------|------|
| **gaussian-splatting** | INRIA에서 만든 오리지널 구현체 | [GitHub](https://github.com/graphdeco-inria/gaussian-splatting) |
| **gsplat** | CUDA 가속 래스터라이제이션, Python 바인딩 | [GitHub](https://github.com/nerfstudio-project/gsplat) |
| **OpenSplat** | C++로 만든 경량 구현체, CPU/GPU 모두 지원 | [GitHub](https://github.com/pierotofy/OpenSplat) |
| **LichtFeld Studio** | 최신 C++23 + CUDA 12.8 기반 고성능 구현체 | [GitHub](https://github.com/MrNeRF/LichtFeld-Studio) |

### 뷰어/편집 도구

| 도구 | 설명 | 링크 |
|------|------|------|
| **SuperSplat** | 브라우저에서 바로 쓰는 온라인 뷰어+편집기 | [superspl.at](https://superspl.at/) |
| **Luma AI** | 스마트폰으로 촬영 → 3DGS 자동 생성 | [lumalabs.ai](https://lumalabs.ai/) |
| **Scaniverse** | Niantic의 모바일 3DGS 앱 | [scaniverse.com](https://scaniverse.com/) |

### 파일 형식

- **`.ply`**: 원래 포인트 클라우드 형식, 3DGS의 기본 저장 포맷
- **`.splat`**: 최적화된 바이너리 형식
- **`.spz`**: Niantic/Scaniverse가 개발한 압축 형식 ([오픈소스 공개](https://scaniverse.com/news/spz-gaussian-splat-open-source-file-format))
- **glTF 확장**: Khronos 그룹이 표준화 작업 중 (2025년 발표)

### 정보 모음

- [awesome-3D-gaussian-splatting](https://github.com/MrNeRF/awesome-3D-gaussian-splatting): 논문과 리소스 총정리
- [2025 Arxiv Paper List](https://github.com/Lee-JaeWon/2025-Arxiv-Paper-List-Gaussian-Splatting): 매일 업데이트되는 최신 논문 목록
- [Radiance Fields](https://radiancefields.com/): NeRF/3DGS 관련 뉴스와 정보

---

## 8. 한계점과 미래 전망

### 현재 한계점

아무리 혁신적이어도 아직 해결 안 된 문제들이 있어요.

**1. 메모리 & 저장 공간**

> "3DGS suffers from substantial memory and storage requirements, posing challenges for deployment on resource-constrained devices." — [arXiv Survey 2407.17418](https://arxiv.org/html/2407.17418v2)

장면 하나에 수 GB가 필요해요. 모바일 기기에서 실시간으로 돌리기엔 아직 무거워요.

**2. 반사/투명 물체의 어려움**

가우시안 표현은 유리나 금속 표면처럼 복잡한 반사를 처리하기 어려워요. 레이 트레이싱 방식이 아니라 래스터화 기반이라 근본적인 한계가 있어요.

**3. 기존 렌더링 파이프라인과의 호환성**

> "Compatibility issues: existing rendering pipelines are mainly optimized for meshes. 3DGS struggles to support complex effects like transparency and depth of field." — [arXiv Survey](https://arxiv.org/html/2407.17418v2)

게임 엔진(Unreal, Unity)은 기본적으로 폴리곤 메시 기반이에요. 3DGS를 기존 파이프라인에 통합하려면 추가 작업이 필요해요.

**4. 팝핑 아티팩트 (Popping Artifacts)**

카메라를 아주 빠르게 움직일 때, 가우시안의 깊이 정렬 순서가 갑자기 바뀌면서 팝핑(popping) 현상이 발생해요.

**5. 실외 대규모 장면의 품질**

반사 표면, 식생(나무 잎사귀 같은 것들), 희박한 시점 등을 가진 복잡한 야외 장면에서는 아직 재구성 품질이 떨어져요.

---

### 미래 전망

그럼에도 불구하고, 전망은 매우 밝아요.

**단기 전망 (2026~2027)**
- 모바일 실시간 3DGS 렌더링 (스마트폰에서도 가능)
- glTF 표준화 완료로 3DGS가 웹의 보편적 3D 포맷으로
- 생성형 AI와의 완전한 통합 (텍스트 → 3D 장면)

**중기 전망 (2027~2030)**
- 게임 엔진의 기본 에셋 포맷으로 채택
- 자율주행 시뮬레이션의 표준 플랫폼
- AR 글래스에서 실시간 3DGS 렌더링으로 현실-디지털 경계 흐려지기

**장기 전망**
- 3DGS가 "3D의 JPEG"가 되는 세상
  - 지금 웹에서 사진을 JPEG로 보여주듯, 3D 공간을 3DGS로 전달
- 메타버스와 디지털 트윈의 핵심 기반 기술

> "Gaussian splats moved from research curiosity to production reality in 18 months. We now have real-time 3D on consumer devices, 90% smaller files, city-scale mobile streaming, and even early standardization in glTF." — [Medium](https://medium.com/@qsibmini123/gaussian-splats-are-becoming-the-jpeg-of-3d-why-2025-is-the-breakout-year-ac841ed39440)

---

## 마치며

3D Gaussian Splatting은 등장한 지 불과 2~3년 만에 3D 컴퓨터 그래픽스 분야를 완전히 바꿔놓고 있어요. 전통적으로 수십 명의 아티스트가 몇 달 걸려서 만들던 3D 환경을, 이제 스마트폰 사진 몇 장과 몇 분의 학습으로 만들어낼 수 있게 됐어요.

물론 아직 해결해야 할 문제들이 있어요. 메모리, 반사 처리, 동적 장면... 하지만 연구자들이 미친 속도로 이 문제들을 해결해나가고 있어요. 2025년에만 수백 편의 관련 논문이 발표됐으니까요.

앞으로 몇 년 안에 우리가 일상에서 쓰는 앱, 게임, VR 기기에 이 기술이 자연스럽게 녹아들 거예요. "3D Gaussian Splatting"이라는 이름을 기억해두세요. 3D 세계의 판도를 바꾸는 기술이에요.

---

## 참고 문헌

1. Kerbl, B., et al. (2023). [3D Gaussian Splatting for Real-Time Radiance Field Rendering](https://repo-sam.inria.fr/fungraph/3d-gaussian-splatting/). SIGGRAPH 2023.
2. Mildenhall, B., et al. (2020). [NeRF: Representing Scenes as Neural Radiance Fields for View Synthesis](https://arxiv.org/abs/2003.08934). ECCV 2020.
3. Wu, G., et al. (2024). [4D Gaussian Splatting for Real-Time Dynamic Scene Rendering](https://arxiv.org/abs/2310.08528). CVPR 2024.
4. [Introduction to 3D Gaussian Splatting](https://huggingface.co/blog/gaussian-splatting). Hugging Face Blog.
5. [3D Gaussian Splatting vs NeRF: The End Game?](https://pyimagesearch.com/2024/12/09/3d-gaussian-splatting-vs-nerf-the-end-game-of-3d-reconstruction/). PyImageSearch, 2024.
6. [3D Gaussian Splatting: Survey, Technologies, Challenges](https://arxiv.org/html/2407.17418v2). arXiv 2407.17418.
7. [NVIDIA Blog: Ray Tracing vs Rasterization](https://blogs.nvidia.com/blog/whats-difference-between-ray-tracing-rasterization/).
8. [AWS: What is NeRF?](https://aws.amazon.com/what-is/neural-radiance-fields/)
9. [CityGaussian](https://arxiv.org/abs/2404.01133). arXiv 2024.
10. [SplatAD: Gaussian Splatting for Autonomous Driving](https://arxiv.org/html/2411.16816v3). arXiv 2024.
11. [Gaussian Splats: The JPEG of 3D](https://medium.com/@qsibmini123/gaussian-splats-are-becoming-the-jpeg-of-3d-why-2025-is-the-breakout-year-ac841ed39440). Medium 2025.
12. [SPZ: Open-Source Gaussian Splat Format](https://scaniverse.com/news/spz-gaussian-splat-open-source-file-format). Niantic/Scaniverse 2025.
13. [MEGA: Memory-Efficient 4D Gaussian Splatting](https://openaccess.thecvf.com/content/ICCV2025/papers/Zhang_MEGA_Memory-Efficient_4D_Gaussian_Splatting_for_Dynamic_Scenes_ICCV_2025_paper.pdf). ICCV 2025.
14. [Material-informed Gaussian Splatting for Digital Twin](https://arxiv.org/abs/2511.20348). arXiv 2025.
15. [VR-Drive: Feed-Forward 3D Gaussian Splatting for Autonomous Driving](https://arxiv.org/abs/2510.23205). arXiv 2025.
