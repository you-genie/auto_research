# 3D Gaussian Splatting 개념 시각화 데모

3D Gaussian Splatting의 핵심 개념을 직관적으로 이해할 수 있는 교육용 Python 데모입니다.

## 생성되는 시각화

| 파일 | 내용 |
|------|------|
| `output_1_gaussian_basics.png` | 가우시안 개념: 1D → 2D → 3D 확장 |
| `output_2_gaussian_parameters.png` | 3D 가우시안의 4가지 파라미터 (위치, 공분산, 색상, 불투명도) |
| `output_3_scene_representation.png` | 가우시안 수에 따른 장면 표현 품질 변화 |
| `output_4_alpha_blending.png` | 알파 블렌딩 단계별 누적 과정 |
| `output_5_nerf_vs_3dgs.png` | NeRF vs 3DGS 렌더링 원리와 성능 비교 |

## 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 데모 실행
python gaussian_splatting_demo.py
```

## 주요 개념 요약

- **가우시안(Gaussian)**: 중심(위치), 크기/방향(공분산), 색상(RGB), 불투명도(α)로 정의되는 반투명 타원체
- **스플래팅(Splatting)**: 3D 가우시안을 카메라 방향으로 2D 화면에 투영하는 과정
- **알파 블렌딩**: 앞에서 뒤로 가우시안을 쌓아 최종 픽셀 색상을 계산
- **실시간 렌더링**: 신경망 호출 없이 GPU 래스터화만으로 100+ FPS 달성

## 실제 3DGS 구현체

이 데모는 개념 설명용입니다. 실제 구현체는:
- [graphdeco-inria/gaussian-splatting](https://github.com/graphdeco-inria/gaussian-splatting) — 원논문 공식 구현
- [nerfstudio](https://docs.nerf.studio/) — 사용하기 쉬운 통합 프레임워크
