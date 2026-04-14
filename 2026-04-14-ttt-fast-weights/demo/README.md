# TTT (Test Time Training) 핵심 메커니즘 데모

Yu Sun et al. (2024) "Learning to (Learn at Test Time)" 논문의
TTT-Linear 및 TTT-MLP 레이어 알고리즘을 NumPy로 구현한 교육용 데모입니다.

## 실행 방법

```bash
pip install numpy
python ttt_demo.py
```

## 데모 목록

| 데모 | 내용 |
|------|------|
| 데모 1 | TTT-Linear: 온라인 vs 미니배치 비교 |
| 데모 2 | TTT-Linear vs TTT-MLP 손실 감소 비교 |
| 데모 3 | 컨텍스트 적응 — W_t의 진화 추적 |
| 데모 4 | TTT vs Self-Attention 속도 비교 |
| 데모 5 | Fast Weights 직관 — 패턴 전환 시 적응 |

## 핵심 구현

```python
# TTT-Linear의 핵심: 히든 스테이트 W_t를 경사하강법으로 업데이트
W_t = W_{t-1} - lr * gradient(loss(W_{t-1}, x_t))
output = W_t @ (theta_Q @ x_t)

# 자기지도 손실
loss = ||W @ (theta_K @ x) - theta_V @ x||^2
```

## 참고 문헌

- Yu Sun et al. (2024): https://arxiv.org/abs/2407.04620
- Titans (Google DeepMind): https://arxiv.org/abs/2501.00663
- E2E-TTT: https://arxiv.org/abs/2512.23675
- LaCT: https://arxiv.org/abs/2505.23884
