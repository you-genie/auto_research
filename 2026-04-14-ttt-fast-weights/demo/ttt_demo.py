"""
Test Time Training (TTT) 핵심 메커니즘 데모
==============================================

Yu Sun et al. (2024) "Learning to (Learn at Test Time)" 논문의
TTT-Linear 레이어 핵심 알고리즘을 NumPy로 구현한 교육용 데모입니다.

실행 방법:
    python ttt_demo.py

참고 논문: https://arxiv.org/abs/2407.04620
"""

import numpy as np
import time


# ─── 유틸리티 함수 ────────────────────────────────────────────────────────────

def set_seed(seed: int = 42):
    """재현성을 위한 난수 시드 고정"""
    np.random.seed(seed)


def layer_norm(x: np.ndarray, eps: float = 1e-5) -> np.ndarray:
    """Layer Normalization 구현"""
    mean = x.mean(axis=-1, keepdims=True)
    std = x.std(axis=-1, keepdims=True)
    return (x - mean) / (std + eps)


def softmax(x: np.ndarray) -> np.ndarray:
    """수치 안정적 Softmax"""
    x = x - x.max(axis=-1, keepdims=True)
    exp_x = np.exp(x)
    return exp_x / exp_x.sum(axis=-1, keepdims=True)


# ─── TTT-Linear 레이어 ────────────────────────────────────────────────────────

class TTTLinearLayer:
    """
    TTT-Linear 레이어: 히든 스테이트 = 선형 모델 W

    핵심 아이디어:
    - 일반 RNN: h_t = σ(W · h_{t-1} + U · x_t)
    - TTT:      W_t = W_{t-1} - η · ∇ℓ(W_{t-1}; x_t)
                output_t = f(x_t; W_t)

    자기지도 손실: ℓ(W; x) = ||f(θ_K · x; W) - θ_V · x||²
    """

    def __init__(self, d_model: int, lr: float = 0.01, chunk_size: int = 4):
        """
        Args:
            d_model: 모델 차원 (임베딩 크기)
            lr: 내부 루프 학습률 (η)
            chunk_size: 미니배치 TTT 청크 크기 (b)
        """
        self.d_model = d_model
        self.lr = lr
        self.chunk_size = chunk_size

        # 외부 루프에서 학습되는 프로젝션 행렬들
        scale = 1.0 / np.sqrt(d_model)
        self.theta_K = np.random.randn(d_model, d_model) * scale  # 키 프로젝션
        self.theta_V = np.random.randn(d_model, d_model) * scale  # 밸류 프로젝션
        self.theta_Q = np.random.randn(d_model, d_model) * scale  # 쿼리 프로젝션

        # 히든 스테이트: 선형 모델의 가중치 행렬 W₀
        self.W_init = np.eye(d_model) * 0.1  # 초기 히든 스테이트

        print(f"[TTT-Linear] 초기화: d_model={d_model}, lr={lr}, chunk_size={chunk_size}")

    def _self_supervised_loss(self, W: np.ndarray, x: np.ndarray) -> tuple[float, np.ndarray]:
        """
        자기지도 손실 계산 및 W에 대한 그래디언트 반환

        ℓ(W; x) = ||f(θ_K · x; W) - θ_V · x||²
                 = ||W · (θ_K · x) - θ_V · x||²

        Args:
            W: 현재 히든 스테이트 가중치 (d_model, d_model)
            x: 입력 토큰 (d_model,)

        Returns:
            (손실값, W에 대한 그래디언트)
        """
        k = self.theta_K @ x        # 키 뷰: θ_K · x
        v = self.theta_V @ x        # 밸류 뷰 (타겟): θ_V · x
        pred = W @ k                # 예측: W · k
        residual = pred - v         # 잔차

        loss = 0.5 * np.sum(residual ** 2)
        # ∂ℓ/∂W = residual · k^T  (외적)
        grad_W = np.outer(residual, k)

        return loss, grad_W

    def forward_online(self, tokens: np.ndarray) -> tuple[np.ndarray, list[float]]:
        """
        온라인 TTT 순전파 (토큰 하나씩 처리 — 느리지만 개념 이해에 명확)

        Args:
            tokens: 입력 시퀀스 (seq_len, d_model)

        Returns:
            (출력 시퀀스, 손실 이력)
        """
        seq_len = tokens.shape[0]
        outputs = np.zeros_like(tokens)
        W = self.W_init.copy()
        losses = []

        for t in range(seq_len):
            x_t = tokens[t]

            # ── 내부 루프: 자기지도 학습으로 W 업데이트 ──
            loss, grad_W = self._self_supervised_loss(W, x_t)
            losses.append(loss)
            W = W - self.lr * grad_W  # 경사하강법 한 스텝

            # ── 출력 생성: W_t를 쿼리로 예측 ──
            q_t = self.theta_Q @ x_t
            out = W @ q_t
            outputs[t] = layer_norm(out + x_t)  # 잔차 연결 + LayerNorm

        return outputs, losses

    def forward_minibatch(self, tokens: np.ndarray) -> tuple[np.ndarray, list[float]]:
        """
        미니배치 TTT 순전파 (chunk_size 토큰씩 묶어 병렬 처리)

        이 방식이 GPU에서 효율적인 이유:
        - chunk 내 토큰들의 그래디언트를 한꺼번에 계산
        - 행렬 곱셈으로 병렬화 가능

        Args:
            tokens: 입력 시퀀스 (seq_len, d_model)

        Returns:
            (출력 시퀀스, 청크별 평균 손실 이력)
        """
        seq_len = tokens.shape[0]
        outputs = np.zeros_like(tokens)
        W = self.W_init.copy()
        chunk_losses = []

        for chunk_start in range(0, seq_len, self.chunk_size):
            chunk_end = min(chunk_start + self.chunk_size, seq_len)
            chunk = tokens[chunk_start:chunk_end]  # (b, d_model)
            b = chunk.shape[0]

            # ── 청크 내 모든 토큰에 대해 그래디언트 누적 ──
            total_loss = 0.0
            grad_accum = np.zeros_like(W)

            for x_t in chunk:
                loss, grad_W = self._self_supervised_loss(W, x_t)
                total_loss += loss
                grad_accum += grad_W  # 그래디언트 누적

            chunk_losses.append(total_loss / b)

            # ── 청크 단위로 W 업데이트 (미니배치 경사하강법) ──
            W = W - self.lr * (grad_accum / b)

            # ── 청크 출력 생성 ──
            for i, x_t in enumerate(chunk):
                q_t = self.theta_Q @ x_t
                out = W @ q_t
                outputs[chunk_start + i] = layer_norm(out + x_t)

        return outputs, chunk_losses


# ─── TTT-MLP 레이어 (단순화 버전) ────────────────────────────────────────────

class TTTMLPLayer:
    """
    TTT-MLP 레이어: 히든 스테이트 = 2층 MLP

    TTT-Linear와 동일한 프레임워크이지만
    내부 모델 f를 더 강력한 MLP로 대체합니다.

    f_mlp(x) = W2 · gelu(W1 · x)   (4배 확장 차원)
    """

    def __init__(self, d_model: int, expansion: int = 4, lr: float = 0.01):
        """
        Args:
            d_model: 모델 차원
            expansion: MLP 내부 확장 비율 (보통 4)
            lr: 내부 루프 학습률
        """
        self.d_model = d_model
        self.d_hidden = d_model * expansion
        self.lr = lr

        scale = 1.0 / np.sqrt(d_model)
        self.theta_K = np.random.randn(d_model, d_model) * scale
        self.theta_V = np.random.randn(d_model, d_model) * scale
        self.theta_Q = np.random.randn(d_model, d_model) * scale

        # MLP 히든 스테이트: W1, W2 두 개의 가중치 행렬
        self.W1_init = np.random.randn(self.d_hidden, d_model) * scale
        self.W2_init = np.random.randn(d_model, self.d_hidden) * scale * 0.1

        print(f"[TTT-MLP] 초기화: d_model={d_model}, d_hidden={self.d_hidden}, lr={lr}")

    @staticmethod
    def gelu(x: np.ndarray) -> np.ndarray:
        """GELU 활성화 함수"""
        return 0.5 * x * (1 + np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3)))

    @staticmethod
    def gelu_grad(x: np.ndarray) -> np.ndarray:
        """GELU 그래디언트"""
        tanh_val = np.tanh(np.sqrt(2 / np.pi) * (x + 0.044715 * x**3))
        sech2 = 1 - tanh_val**2
        return 0.5 * (1 + tanh_val) + 0.5 * x * sech2 * np.sqrt(2 / np.pi) * (1 + 3 * 0.044715 * x**2)

    def _mlp_forward(self, x: np.ndarray, W1: np.ndarray, W2: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        """MLP 순전파: f(x; W1, W2) = W2 · gelu(W1 · x)"""
        h = W1 @ x          # (d_hidden,)
        a = self.gelu(h)     # (d_hidden,)
        out = W2 @ a         # (d_model,)
        return out, a        # 출력과 중간 활성화 반환

    def _self_supervised_loss(self, W1, W2, x):
        """MLP 자기지도 손실 및 그래디언트"""
        k = self.theta_K @ x
        v = self.theta_V @ x

        pred, a = self._mlp_forward(k, W1, W2)
        residual = pred - v

        loss = 0.5 * np.sum(residual ** 2)

        # 역전파 (그래디언트 클리핑으로 수치 안정화)
        grad_W2 = np.outer(residual, a)
        delta_h = W2.T @ residual * self.gelu_grad(W1 @ k)
        grad_W1 = np.outer(delta_h, k)

        # NaN/Inf 방지를 위한 클리핑
        grad_W1 = np.clip(grad_W1, -5.0, 5.0)
        grad_W2 = np.clip(grad_W2, -5.0, 5.0)

        return loss, grad_W1, grad_W2

    def forward(self, tokens: np.ndarray) -> tuple[np.ndarray, list[float]]:
        """TTT-MLP 순전파"""
        seq_len = tokens.shape[0]
        outputs = np.zeros_like(tokens)
        W1, W2 = self.W1_init.copy(), self.W2_init.copy()
        losses = []

        for t in range(seq_len):
            x_t = tokens[t]
            loss, gW1, gW2 = self._self_supervised_loss(W1, W2, x_t)
            losses.append(loss)

            # 두 행렬 모두 업데이트
            W1 = W1 - self.lr * gW1
            W2 = W2 - self.lr * gW2

            q_t = self.theta_Q @ x_t
            out, _ = self._mlp_forward(q_t, W1, W2)
            outputs[t] = layer_norm(out + x_t)

        return outputs, losses


# ─── 비교: 표준 Self-Attention ────────────────────────────────────────────────

class StandardSelfAttention:
    """
    비교용 표준 Self-Attention (단일 헤드)
    TTT와의 이론적 연결: Nadaraya-Watson TTT ≈ Self-Attention
    """

    def __init__(self, d_model: int):
        scale = 1.0 / np.sqrt(d_model)
        self.W_Q = np.random.randn(d_model, d_model) * scale
        self.W_K = np.random.randn(d_model, d_model) * scale
        self.W_V = np.random.randn(d_model, d_model) * scale
        self.scale = np.sqrt(d_model)

    def forward(self, tokens: np.ndarray) -> np.ndarray:
        """
        Self-Attention 순전파 (O(n²) 복잡도)
        """
        Q = tokens @ self.W_Q.T  # (seq_len, d_model)
        K = tokens @ self.W_K.T
        V = tokens @ self.W_V.T

        # 어텐션 점수: O(n²)
        scores = (Q @ K.T) / self.scale    # (seq_len, seq_len)
        # 인과 마스크 (causal masking)
        mask = np.triu(np.ones_like(scores) * (-1e9), k=1)
        attn = softmax(scores + mask)

        output = attn @ V
        return np.array([layer_norm(output[t] + tokens[t]) for t in range(len(tokens))])


# ─── 메인 데모 ────────────────────────────────────────────────────────────────

def demo_ttt_linear():
    """TTT-Linear 기본 동작 데모"""
    print("\n" + "="*60)
    print("데모 1: TTT-Linear — 온라인 vs 미니배치")
    print("="*60)

    set_seed(42)
    d_model, seq_len = 16, 32
    tokens = np.random.randn(seq_len, d_model)

    layer = TTTLinearLayer(d_model=d_model, lr=0.01, chunk_size=4)

    # 온라인 TTT
    t0 = time.perf_counter()
    out_online, losses_online = layer.forward_online(tokens)
    t1 = time.perf_counter()

    # 미니배치 TTT
    t2 = time.perf_counter()
    out_minibatch, losses_minibatch = layer.forward_minibatch(tokens)
    t3 = time.perf_counter()

    print(f"\n입력 시퀀스: {seq_len}토큰 × {d_model}차원")
    print(f"\n[온라인 TTT]    시간: {(t1-t0)*1000:.2f}ms   초기 손실: {losses_online[0]:.4f}   최종 손실: {losses_online[-1]:.4f}")
    print(f"[미니배치 TTT]  시간: {(t3-t2)*1000:.2f}ms   초기 손실: {losses_minibatch[0]:.4f}   최종 손실: {losses_minibatch[-1]:.4f}")
    print(f"\n출력 통계 (온라인):    평균={out_online.mean():.4f}, 표준편차={out_online.std():.4f}")
    print(f"출력 통계 (미니배치):  평균={out_minibatch.mean():.4f}, 표준편차={out_minibatch.std():.4f}")


def demo_ttt_mlp():
    """TTT-MLP 데모: 더 강력한 내부 모델"""
    print("\n" + "="*60)
    print("데모 2: TTT-MLP — 2층 MLP 히든 스테이트")
    print("="*60)

    set_seed(42)
    d_model, seq_len = 16, 20
    tokens = np.random.randn(seq_len, d_model)

    layer_linear = TTTLinearLayer(d_model=d_model, lr=0.01)
    layer_mlp = TTTMLPLayer(d_model=d_model, expansion=4, lr=0.005)

    out_linear, losses_linear = layer_linear.forward_online(tokens)
    out_mlp, losses_mlp = layer_mlp.forward(tokens)

    print(f"\n입력 시퀀스: {seq_len}토큰 × {d_model}차원")
    print(f"\n{'모델':<20} {'초기 손실':>12} {'최종 손실':>12} {'손실 감소율':>12}")
    print("-" * 60)

    for name, losses in [("TTT-Linear", losses_linear), ("TTT-MLP", losses_mlp)]:
        init_loss = losses[0]
        final_loss = losses[-1]
        reduction = (init_loss - final_loss) / init_loss * 100
        print(f"{name:<20} {init_loss:>12.4f} {final_loss:>12.4f} {reduction:>11.1f}%")

    print(f"\n히든 스테이트 파라미터 수:")
    print(f"  TTT-Linear: {d_model}×{d_model} = {d_model*d_model} 파라미터")
    print(f"  TTT-MLP:    {d_model}×{d_model*4} + {d_model*4}×{d_model} = {d_model*d_model*4 + d_model*4*d_model} 파라미터")


def demo_context_adaptation():
    """
    TTT의 핵심 특성 데모: 컨텍스트에 적응하는 히든 스테이트

    서로 다른 패턴의 두 시퀀스를 입력하면,
    TTT는 각 시퀀스에 맞게 W_t가 다르게 진화합니다.
    """
    print("\n" + "="*60)
    print("데모 3: 컨텍스트 적응 — W_t의 진화 추적")
    print("="*60)

    set_seed(42)
    d_model = 8

    # 패턴 A: 주기적 시퀀스
    t = np.linspace(0, 2 * np.pi, 16)
    pattern_A = np.stack([np.sin(t + i * 0.5) for i in range(d_model)], axis=1)

    # 패턴 B: 랜덤 시퀀스
    pattern_B = np.random.randn(16, d_model)

    layer = TTTLinearLayer(d_model=d_model, lr=0.05)

    print("\n시퀀스 A (주기적 패턴):")
    _, losses_A = layer.forward_online(pattern_A)
    W_after_A = layer.W_init.copy()  # 참고용 (실제로는 내부에서 추적)

    print(f"  손실 궤적: {' → '.join(f'{l:.3f}' for l in losses_A[::4])}")
    print(f"  손실 감소: {losses_A[0]:.4f} → {losses_A[-1]:.4f} ({(losses_A[0]-losses_A[-1])/losses_A[0]*100:.1f}% 감소)")

    print("\n시퀀스 B (랜덤 패턴):")
    _, losses_B = layer.forward_online(pattern_B)
    print(f"  손실 궤적: {' → '.join(f'{l:.3f}' for l in losses_B[::4])}")
    print(f"  손실 감소: {losses_B[0]:.4f} → {losses_B[-1]:.4f} ({(losses_B[0]-losses_B[-1])/losses_B[0]*100:.1f}% 감소)")

    print("\n핵심 관찰:")
    print("  W_t는 각 시퀀스의 패턴에 맞게 독립적으로 진화합니다.")
    print("  주기적 패턴은 학습이 더 쉬워 손실이 빠르게 감소합니다.")
    print("  이것이 TTT가 '테스트 시점에 배운다'는 의미입니다.")


def demo_ttt_vs_attention():
    """
    TTT vs Self-Attention 비교
    이론적 연결: Nadaraya-Watson TTT ≈ Self-Attention
    """
    print("\n" + "="*60)
    print("데모 4: TTT vs Self-Attention 비교")
    print("="*60)

    set_seed(42)
    d_model = 16
    attention = StandardSelfAttention(d_model=d_model)

    print(f"\n{'컨텍스트 길이':>15} | {'Self-Attention':>16} | {'TTT-Linear':>12} | {'복잡도 비율':>12}")
    print("-" * 62)

    for seq_len in [16, 64, 256, 1024]:
        tokens = np.random.randn(seq_len, d_model)
        layer = TTTLinearLayer(d_model=d_model, lr=0.01, chunk_size=16)

        t0 = time.perf_counter()
        _ = attention.forward(tokens)
        t_attn = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        _, _ = layer.forward_minibatch(tokens)
        t_ttt = (time.perf_counter() - t0) * 1000

        ratio = t_attn / t_ttt if t_ttt > 0 else float('inf')
        print(f"{seq_len:>15} | {t_attn:>13.2f}ms | {t_ttt:>9.2f}ms | {ratio:>10.1f}×")

    print("\n참고: 이 데모는 순수 NumPy로 구현되어 GPU 최적화 효과를 반영하지 않습니다.")
    print("실제 GPU 구현에서 TTT의 장점은 훨씬 명확하게 나타납니다.")
    print("\n이론적 연결 (Yu Sun et al., 2024 Theorem 1):")
    print("  TTT-Linear (배치 경사하강법) ≡ 선형 어텐션 (수학적 동치)")
    print("  Nadaraya-Watson TTT ≡ Self-Attention (수학적 동치)")


def demo_fast_weights_intuition():
    """
    Fast Weights 직관 데모:
    Slow Weights(고정) vs Fast Weights(적응)의 차이
    """
    print("\n" + "="*60)
    print("데모 5: Fast Weights 직관 — 적응적 메모리")
    print("="*60)

    set_seed(42)
    d_model = 8
    seq_len = 24

    # 시나리오: "언어 A" 패턴 12토큰, "언어 B" 패턴 12토큰
    # 언어 A: 양수 위주
    lang_A = np.abs(np.random.randn(seq_len // 2, d_model))
    # 언어 B: 음수 위주
    lang_B = -np.abs(np.random.randn(seq_len // 2, d_model))
    tokens = np.vstack([lang_A, lang_B])

    layer = TTTLinearLayer(d_model=d_model, lr=0.1)
    _, losses = layer.forward_online(tokens)

    print(f"\n시퀀스 구성: 언어A({seq_len//2}토큰) → 언어B({seq_len//2}토큰)")
    print("\n손실 변화 추적:")
    print("  언어A 구간:", end=" ")
    print(" → ".join(f"{l:.3f}" for l in losses[:seq_len//2:3]))
    print("  [언어 전환!]")
    print("  언어B 구간:", end=" ")
    print(" → ".join(f"{l:.3f}" for l in losses[seq_len//2::3]))

    # 언어 전환 직후 손실 급등 여부 확인
    loss_before_switch = np.mean(losses[seq_len//2-3:seq_len//2])
    loss_after_switch = losses[seq_len//2]
    loss_end = losses[-1]

    print(f"\n언어 전환 직전 평균 손실: {loss_before_switch:.4f}")
    print(f"언어 전환 직후 손실:       {loss_after_switch:.4f}  (급등 예상)")
    print(f"언어B 학습 후 최종 손실:   {loss_end:.4f}  (다시 감소)")
    print("\n핵심: Fast Weights(W_t)가 새 패턴에 빠르게 재적응합니다.")
    print("이것이 TTT가 'Fast Weights'의 현대적 실현인 이유입니다.")


# ─── 진입점 ───────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 60)
    print("Test Time Training (TTT) 핵심 메커니즘 데모")
    print("Yu Sun et al. (2024), arXiv:2407.04620")
    print("=" * 60)

    demo_ttt_linear()
    demo_ttt_mlp()
    demo_context_adaptation()
    demo_ttt_vs_attention()
    demo_fast_weights_intuition()

    print("\n" + "="*60)
    print("데모 완료!")
    print("="*60)
    print("\n참고 자료:")
    print("  논문: https://arxiv.org/abs/2407.04620")
    print("  Titans: https://arxiv.org/abs/2501.00663")
    print("  E2E-TTT: https://arxiv.org/abs/2512.23675")
    print("  LaCT: https://arxiv.org/abs/2505.23884")
