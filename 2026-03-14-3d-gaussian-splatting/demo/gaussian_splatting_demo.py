"""
3D Gaussian Splatting 개념 시각화 데모
======================================
이 코드는 3D Gaussian Splatting의 핵심 개념을 직관적으로 이해할 수 있도록
단계별로 시각화하는 교육용 데모입니다.

실제 3DGS 구현은 CUDA 기반 고성능 코드이지만,
이 데모는 numpy와 matplotlib만으로 개념을 설명합니다.

필요 패키지: numpy, matplotlib, scipy
설치: pip install -r requirements.txt
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Ellipse
from mpl_toolkits.mplot3d import Axes3D
from scipy.stats import multivariate_normal
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# 1. 가우시안(Gaussian) 기본 개념 시각화
# =============================================================================

def demo_gaussian_basics():
    """
    가우시안 분포의 1D → 2D → 3D 확장을 시각화합니다.
    "종 모양 곡선"이 어떻게 3D 공간의 '반투명 구름'이 되는지 보여줍니다.
    """
    fig = plt.figure(figsize=(16, 5))
    fig.suptitle("가우시안(Gaussian)의 개념: 1D → 2D → 3D", fontsize=14, fontweight='bold')

    # --- 1D 가우시안 ---
    ax1 = fig.add_subplot(131)
    x = np.linspace(-3, 3, 300)
    # 평균 0, 표준편차 1인 가우시안 = exp(-x²/2) / sqrt(2π)
    y = np.exp(-0.5 * x**2) / np.sqrt(2 * np.pi)
    ax1.plot(x, y, 'b-', linewidth=2)
    ax1.fill_between(x, y, alpha=0.3, color='blue')
    ax1.set_title("1D 가우시안\n(종 모양 곡선)")
    ax1.set_xlabel("x")
    ax1.set_ylabel("밀도")
    ax1.axvline(0, color='red', linestyle='--', alpha=0.5, label='평균(μ)')
    ax1.legend()

    # --- 2D 가우시안 ---
    ax2 = fig.add_subplot(132)
    x2 = np.linspace(-3, 3, 100)
    y2 = np.linspace(-3, 3, 100)
    X, Y = np.meshgrid(x2, y2)

    # 비등방성(anisotropic) 가우시안: 타원형 모양
    # 공분산 행렬 = [[1.5, 0.8], [0.8, 0.6]] → 기울어진 타원
    mean_2d = [0, 0]
    cov_2d = [[1.5, 0.8], [0.8, 0.6]]
    pos = np.dstack((X, Y))
    rv = multivariate_normal(mean_2d, cov_2d)
    Z = rv.pdf(pos)

    # 등고선으로 표현
    contour = ax2.contourf(X, Y, Z, levels=20, cmap='Blues')
    ax2.contour(X, Y, Z, levels=5, colors='darkblue', alpha=0.5, linewidths=0.5)
    plt.colorbar(contour, ax=ax2)
    ax2.set_title("2D 가우시안\n(비등방성 타원형)")
    ax2.set_xlabel("x")
    ax2.set_ylabel("y")
    ax2.plot(0, 0, 'r*', markersize=10, label='중심(μ)')
    ax2.legend()

    # --- 3D 가우시안 (표면 플롯) ---
    ax3 = fig.add_subplot(133, projection='3d')
    ax3.plot_surface(X, Y, Z, cmap='Blues', alpha=0.8, edgecolor='none')
    ax3.set_title("3D 가우시안\n(산 모양 표면)")
    ax3.set_xlabel("x")
    ax3.set_ylabel("y")
    ax3.set_zlabel("밀도")

    plt.tight_layout()
    plt.savefig("output_1_gaussian_basics.png", dpi=150, bbox_inches='tight')
    print("[1/5] 가우시안 기본 개념 시각화 저장: output_1_gaussian_basics.png")
    plt.close()


# =============================================================================
# 2. 3D 가우시안의 핵심 파라미터 시각화
# =============================================================================

def demo_gaussian_parameters():
    """
    각 3D 가우시안이 가진 4가지 핵심 파라미터를 시각화합니다:
    위치(Position), 크기/방향(Covariance), 색상(Color), 불투명도(Opacity)
    """
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    fig.suptitle("3D 가우시안의 4가지 핵심 파라미터", fontsize=14, fontweight='bold')

    # 공통 배경
    for ax in axes:
        ax.set_xlim(-5, 5)
        ax.set_ylim(-5, 5)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)

    # --- 파라미터 1: 위치(Position) ---
    ax = axes[0]
    ax.set_title("① 위치 (Position)\n각 가우시안의 중심 좌표")
    # 서로 다른 위치에 가우시안 배치
    positions = [(-2, 2), (1, -1), (3, 3), (-1, -3), (0, 1)]
    for pos in positions:
        ellipse = Ellipse(pos, width=1.5, height=1.5,
                         angle=0, alpha=0.5, color='steelblue')
        ax.add_patch(ellipse)
        ax.plot(*pos, 'r.', markersize=6)  # 중심점 표시
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # --- 파라미터 2: 공분산(Covariance) = 크기와 방향 ---
    ax = axes[1]
    ax.set_title("② 공분산 (Covariance)\n크기와 방향 결정")
    # 다양한 모양의 가우시안 (모두 원점에)
    shapes = [
        # (width, height, angle, label)
        (3.0, 1.0, 0,   '납작하고 수평'),
        (1.5, 2.5, 45,  '기울어진'),
        (2.0, 2.0, 0,   '구형'),
    ]
    colors = ['steelblue', 'coral', 'green']
    offsets = [(-3, 1), (1, -2), (3, 2)]
    for (w, h, angle, label), color, offset in zip(shapes, colors, offsets):
        ellipse = Ellipse(offset, width=w, height=h,
                         angle=angle, alpha=0.5, color=color, label=label)
        ax.add_patch(ellipse)
    ax.legend(fontsize=7, loc='upper left')
    ax.set_xlabel("x")
    ax.set_ylabel("y")

    # --- 파라미터 3: 색상(Color) ---
    ax = axes[2]
    ax.set_title("③ 색상 (Color)\nRGB 값으로 표현")
    color_gaussians = [
        ((-2, 2), 'red',    'R=1.0 G=0.0 B=0.0'),
        ((2, 2),  'green',  'R=0.0 G=1.0 B=0.0'),
        ((-2, -2),'blue',   'R=0.0 G=0.0 B=1.0'),
        ((2, -2), 'orange', 'R=1.0 G=0.5 B=0.0'),
        ((0, 0),  'purple', 'R=0.5 G=0.0 B=0.5'),
    ]
    for pos, color, label in color_gaussians:
        ellipse = Ellipse(pos, width=2.0, height=2.0,
                         angle=0, alpha=0.6, color=color)
        ax.add_patch(ellipse)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.text(0, -4.5, "각 가우시안은 자신만의 RGB 색상 보유",
            ha='center', fontsize=8, style='italic')

    # --- 파라미터 4: 불투명도(Opacity/Alpha) ---
    ax = axes[3]
    ax.set_title("④ 불투명도 (Alpha)\n투명~불투명 사이")
    alphas = [0.1, 0.3, 0.5, 0.7, 0.95]
    x_positions = np.linspace(-4, 4, 5)
    for alpha, x_pos in zip(alphas, x_positions):
        ellipse = Ellipse((x_pos, 0), width=1.5, height=1.5,
                         angle=0, alpha=alpha, color='steelblue')
        ax.add_patch(ellipse)
        ax.text(x_pos, -1.5, f'α={alpha}', ha='center', fontsize=7)
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.text(-4, 2.5, "←── 투명", fontsize=9)
    ax.text(2.5, 2.5, "불투명 ──→", fontsize=9)

    plt.tight_layout()
    plt.savefig("output_2_gaussian_parameters.png", dpi=150, bbox_inches='tight')
    print("[2/5] 가우시안 파라미터 시각화 저장: output_2_gaussian_parameters.png")
    plt.close()


# =============================================================================
# 3. 장면을 가우시안으로 표현하기
# =============================================================================

def demo_scene_representation():
    """
    실제 장면을 수많은 가우시안으로 표현하는 방식을 시뮬레이션합니다.
    간단한 2D '장면'(원과 사각형)을 점점 더 많은 가우시안으로 근사합니다.
    """
    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    fig.suptitle("장면을 가우시안으로 표현: 개수가 늘수록 정확해져요!",
                 fontsize=13, fontweight='bold')

    # 목표 장면: 원 하나 + 사각형 느낌의 점군
    # 원 위의 점들 생성
    theta = np.linspace(0, 2*np.pi, 200)
    circle_x = 2 * np.cos(theta)
    circle_y = 2 * np.sin(theta)

    # 사각형 외곽 점들
    rect_x = np.concatenate([
        np.linspace(-4, -2, 50),  # 하단
        np.ones(50) * -2,          # 우측
        np.linspace(-2, -4, 50),  # 상단
        np.ones(50) * -4,          # 좌측
    ])
    rect_y = np.concatenate([
        np.ones(50) * -2,
        np.linspace(-2, 1, 50),
        np.ones(50) * 1,
        np.linspace(1, -2, 50),
    ])

    all_x = np.concatenate([circle_x, rect_x])
    all_y = np.concatenate([circle_y, rect_y])
    all_colors = ['steelblue'] * len(circle_x) + ['coral'] * len(rect_x)

    n_gaussians_list = [5, 20, 50, 200]
    titles = [
        "5개의 가우시안\n(매우 부정확)",
        "20개의 가우시안\n(대략적 형태)",
        "50개의 가우시안\n(꽤 비슷해졌어요)",
        "200개의 가우시안\n(꽤 정확!)"
    ]

    for ax, n_gaussians, title in zip(axes, n_gaussians_list, titles):
        ax.set_xlim(-6, 4)
        ax.set_ylim(-4, 4)
        ax.set_aspect('equal')
        ax.set_facecolor('#f8f9fa')
        ax.set_title(title)

        # n_gaussians 개수만큼 원래 점들 중에서 샘플링
        np.random.seed(42)
        indices = np.random.choice(len(all_x), min(n_gaussians, len(all_x)), replace=False)

        for idx in indices:
            x_pos = all_x[idx] + np.random.normal(0, 0.1)
            y_pos = all_y[idx] + np.random.normal(0, 0.1)
            color = all_colors[idx]

            # 가우시안 크기: 개수가 많을수록 작게
            size = max(0.3, 2.0 / (n_gaussians ** 0.3))
            alpha = 0.6

            ellipse = Ellipse(
                (x_pos, y_pos),
                width=size * np.random.uniform(0.8, 1.2),
                height=size * np.random.uniform(0.8, 1.2),
                angle=np.random.uniform(0, 180),
                alpha=alpha, color=color
            )
            ax.add_patch(ellipse)

        ax.text(0, -3.5, f"가우시안 {n_gaussians}개", ha='center', fontsize=9)
        ax.set_xlabel("x")
        ax.set_ylabel("y")

    plt.tight_layout()
    plt.savefig("output_3_scene_representation.png", dpi=150, bbox_inches='tight')
    print("[3/5] 장면 표현 시각화 저장: output_3_scene_representation.png")
    plt.close()


# =============================================================================
# 4. 알파 블렌딩 (Alpha Blending) 시뮬레이션
# =============================================================================

def demo_alpha_blending():
    """
    3DGS 렌더링의 핵심인 알파 블렌딩 과정을 시뮬레이션합니다.
    앞에서 뒤로 가우시안들을 쌓는 방식으로 최종 이미지가 만들어집니다.
    """
    fig, axes = plt.subplots(1, 5, figsize=(18, 4))
    fig.suptitle("알파 블렌딩 (Alpha Blending): 가우시안을 앞에서 뒤로 겹쳐 쌓기",
                 fontsize=13, fontweight='bold')

    # 4개의 가우시안 (앞에서 뒤 순서로)
    # 각각: 위치, 크기, 색상(RGB), 알파
    gaussians = [
        # (center_x, center_y, sigma_x, sigma_y, angle, color, alpha, depth_label)
        (2.5, 2.5, 0.8, 0.5, 30,  np.array([0.9, 0.2, 0.2]), 0.7, "가장 앞 (깊이=1)"),  # 빨강
        (2.0, 2.0, 1.0, 0.7, -20, np.array([0.2, 0.7, 0.2]), 0.6, "두 번째 (깊이=2)"),  # 초록
        (1.5, 1.5, 1.2, 0.9, 45,  np.array([0.2, 0.2, 0.9]), 0.5, "세 번째 (깊이=3)"),  # 파랑
        (1.0, 1.0, 1.4, 1.1, -10, np.array([0.9, 0.7, 0.2]), 0.8, "가장 뒤 (깊이=4)"),  # 노랑
    ]

    # 이미지 크기
    H, W = 200, 200
    x_grid = np.linspace(0, 5, W)
    y_grid = np.linspace(0, 5, H)
    X_grid, Y_grid = np.meshgrid(x_grid, y_grid)

    # 각 가우시안의 2D 마스크 계산 함수
    def gaussian_2d(cx, cy, sx, sy, angle_deg, X, Y):
        """2D 가우시안 밀도 계산 (회전 포함)"""
        angle = np.radians(angle_deg)
        cos_a, sin_a = np.cos(angle), np.sin(angle)

        # 회전된 좌표
        dx = X - cx
        dy = Y - cy
        xr = cos_a * dx + sin_a * dy
        yr = -sin_a * dx + cos_a * dy

        # 가우시안 공식: exp(-0.5 * (xr²/sx² + yr²/sy²))
        g = np.exp(-0.5 * (xr**2 / sx**2 + yr**2 / sy**2))
        return g

    # 누적 블렌딩 이미지와 투과율(transmittance) 초기화
    blended = np.zeros((H, W, 3))       # 최종 색상 누적
    transmittance = np.ones((H, W))     # 초기 투과율 = 1.0 (완전 투명)

    for i, (cx, cy, sx, sy, angle, color, alpha, depth_label) in enumerate(gaussians):
        # 개별 가우시안 마스크 (0~1 범위)
        g_mask = gaussian_2d(cx, cy, sx, sy, angle, X_grid, Y_grid)

        # 실제 불투명도 = alpha × gaussian_mask
        actual_alpha = alpha * g_mask

        # 이 가우시안의 기여도 = color × actual_alpha × transmittance
        ax = axes[i]
        contribution = color[np.newaxis, np.newaxis, :] * actual_alpha[:, :, np.newaxis] \
                      * transmittance[:, :, np.newaxis]
        blended += contribution

        # 투과율 업데이트: T(i+1) = T(i) × (1 - actual_alpha)
        transmittance *= (1 - actual_alpha)

        # 현재까지의 블렌딩 결과 표시
        display_img = np.clip(blended.copy(), 0, 1)
        ax.imshow(display_img, origin='lower', extent=[0, 5, 0, 5])
        ax.set_title(f"단계 {i+1}: {depth_label}\n추가 후 누적 결과")
        ax.set_xlabel("x")
        if i == 0:
            ax.set_ylabel("y")

    # 최종 결과
    axes[-1].set_title(f"최종 결과\n(4개 가우시안 블렌딩)")

    # 마지막 패널에 최종 이미지 표시
    axes[-1].imshow(np.clip(blended, 0, 1), origin='lower', extent=[0, 5, 0, 5])

    plt.tight_layout()
    plt.savefig("output_4_alpha_blending.png", dpi=150, bbox_inches='tight')
    print("[4/5] 알파 블렌딩 시뮬레이션 저장: output_4_alpha_blending.png")
    plt.close()


# =============================================================================
# 5. NeRF vs 3DGS 렌더링 속도 비교 시뮬레이션
# =============================================================================

def demo_nerf_vs_3dgs():
    """
    NeRF와 3DGS의 렌더링 원리와 속도 차이를 시각화합니다.
    """
    fig, axes = plt.subplots(1, 3, figsize=(16, 5))
    fig.suptitle("NeRF vs 3D Gaussian Splatting: 렌더링 원리 비교",
                 fontsize=13, fontweight='bold')

    # --- 그래프 1: NeRF 렌더링 방식 ---
    ax1 = axes[0]
    ax1.set_xlim(-1, 10)
    ax1.set_ylim(-1, 8)
    ax1.set_facecolor('#1a1a2e')
    ax1.set_title("NeRF 렌더링\n(광선 마칭 + 신경망 호출)", color='white')
    ax1.tick_params(colors='white')
    for spine in ax1.spines.values():
        spine.set_color('white')

    # 카메라
    camera_x, camera_y = 0, 4
    ax1.plot(camera_x, camera_y, 's', color='yellow', markersize=15, zorder=5)
    ax1.text(0.2, 4.3, "카메라", color='yellow', fontsize=9)

    # 여러 픽셀 방향으로 광선 쏘기
    ray_targets = [(9, 1), (9, 3), (9, 5), (9, 7)]
    colors_ray = ['cyan', 'magenta', 'lime', 'orange']

    for (tx, ty), rc in zip(ray_targets, colors_ray):
        # 광선 그리기
        ax1.annotate('', xy=(tx, ty), xytext=(camera_x, camera_y),
                    arrowprops=dict(arrowstyle='->', color=rc, lw=1.5))

        # 광선 위의 샘플 포인트들
        n_samples = 6
        sample_xs = np.linspace(camera_x + 1, tx - 0.5, n_samples)
        sample_ys = np.linspace(camera_y + (ty - camera_y) * 0.1,
                                ty - (ty - camera_y) * 0.1, n_samples)
        ax1.scatter(sample_xs, sample_ys, c=rc, s=30, zorder=6, marker='o')

        # 신경망 호출 표시
        for sx, sy in zip(sample_xs, sample_ys):
            ax1.annotate('f(x,y,z)', xy=(sx, sy), fontsize=5,
                        color='white', alpha=0.5,
                        xytext=(sx + 0.1, sy + 0.2))

    ax1.text(5, 0, f"픽셀 1개당 신경망 {n_samples}회 호출\n"
             f"→ 1080p = {1920*1080*n_samples//1_000_000}백만 회 호출\n"
             f"→ 수 초 걸림 = 5 FPS",
             color='red', fontsize=8, ha='center',
             bbox=dict(boxstyle='round', facecolor='#2d0000', alpha=0.8))

    # --- 그래프 2: 3DGS 렌더링 방식 ---
    ax2 = axes[1]
    ax2.set_xlim(-1, 10)
    ax2.set_ylim(-1, 8)
    ax2.set_facecolor('#0d2818')
    ax2.set_title("3DGS 렌더링\n(래스터화 = 가우시안 → 화면 투영)", color='white')
    ax2.tick_params(colors='white')
    for spine in ax2.spines.values():
        spine.set_color('white')

    # 가우시안들 배치
    np.random.seed(123)
    n_gaussians = 30
    gx = np.random.uniform(2, 8, n_gaussians)
    gy = np.random.uniform(1, 7, n_gaussians)
    g_colors = plt.cm.Set3(np.random.rand(n_gaussians))
    g_alphas = np.random.uniform(0.4, 0.9, n_gaussians)

    for i in range(n_gaussians):
        w = np.random.uniform(0.3, 1.2)
        h = np.random.uniform(0.2, 0.8)
        angle = np.random.uniform(0, 180)
        ellipse = Ellipse((gx[i], gy[i]), width=w, height=h,
                         angle=angle, alpha=g_alphas[i], color=g_colors[i])
        ax2.add_patch(ellipse)

    # 카메라와 투영 방향 표시
    ax2.plot(0, 4, 's', color='yellow', markersize=15, zorder=5)
    ax2.text(0.2, 4.3, "카메라", color='yellow', fontsize=9)

    # 투영 화살표 (가우시안 → 화면)
    ax2.annotate('', xy=(9.5, 4), xytext=(5, 4),
                arrowprops=dict(arrowstyle='->', color='yellow', lw=2))
    ax2.text(7, 4.3, "GPU\n투영", color='yellow', fontsize=8, ha='center')

    ax2.text(5, 0, "신경망 호출 없음!\n가우시안을 한번에 GPU에서 투영\n→ 100+ FPS",
            color='lime', fontsize=8, ha='center',
            bbox=dict(boxstyle='round', facecolor='#002d00', alpha=0.8))

    # --- 그래프 3: 성능 비교 바 차트 ---
    ax3 = axes[2]
    ax3.set_title("성능 비교 (로그 스케일)")

    categories = ['렌더링\n(FPS)', '학습 시간\n(분)', '파일 크기\n(MB)']
    nerf_values = [5, 600, 10]          # FPS, 학습시간(분), 파일크기(MB)
    gs_values = [120, 45, 500]          # 3DGS 값

    x = np.arange(len(categories))
    width = 0.35

    bars_nerf = ax3.bar(x - width/2, nerf_values, width,
                        label='NeRF', color='coral', alpha=0.8)
    bars_gs = ax3.bar(x + width/2, gs_values, width,
                      label='3D Gaussian Splatting', color='steelblue', alpha=0.8)

    ax3.set_yscale('log')
    ax3.set_ylabel('값 (로그 스케일)')
    ax3.set_xticks(x)
    ax3.set_xticklabels(categories)
    ax3.legend()
    ax3.grid(True, alpha=0.3, axis='y')

    # 값 레이블 추가
    for bar in bars_nerf:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{height}', ha='center', va='bottom', fontsize=9, color='coral')

    for bar in bars_gs:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height * 1.1,
                f'{height}', ha='center', va='bottom', fontsize=9, color='steelblue')

    # 주석 추가
    ax3.text(0, 200, "24배 빠름!", ha='center', fontsize=9,
            color='green', fontweight='bold')
    ax3.text(1, 50, "13배 빠른\n학습!", ha='center', fontsize=8,
            color='green', fontweight='bold')

    plt.tight_layout()
    plt.savefig("output_5_nerf_vs_3dgs.png", dpi=150, bbox_inches='tight')
    print("[5/5] NeRF vs 3DGS 비교 시각화 저장: output_5_nerf_vs_3dgs.png")
    plt.close()


# =============================================================================
# 메인 실행
# =============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("3D Gaussian Splatting 개념 시각화 데모")
    print("=" * 60)
    print()
    print("5가지 시각화를 생성합니다:")
    print("  1. 가우시안 기본 개념 (1D → 2D → 3D)")
    print("  2. 3D 가우시안의 4가지 파라미터")
    print("  3. 장면을 가우시안으로 표현하기")
    print("  4. 알파 블렌딩 시뮬레이션")
    print("  5. NeRF vs 3DGS 비교")
    print()

    demo_gaussian_basics()
    demo_gaussian_parameters()
    demo_scene_representation()
    demo_alpha_blending()
    demo_nerf_vs_3dgs()

    print()
    print("=" * 60)
    print("완료! 생성된 파일:")
    print("  - output_1_gaussian_basics.png")
    print("  - output_2_gaussian_parameters.png")
    print("  - output_3_scene_representation.png")
    print("  - output_4_alpha_blending.png")
    print("  - output_5_nerf_vs_3dgs.png")
    print()
    print("핵심 개념 요약:")
    print("  - 가우시안: 중심, 크기/방향, 색상, 불투명도로 정의되는 반투명 타원체")
    print("  - 스플래팅: 3D 가우시안을 2D 화면에 투영하는 과정")
    print("  - 알파 블렌딩: 앞에서 뒤로 가우시안을 쌓아 최종 색상 계산")
    print("  - 실시간 렌더링: 신경망 없이 GPU 래스터화만으로 100+ FPS 달성")
    print("=" * 60)
