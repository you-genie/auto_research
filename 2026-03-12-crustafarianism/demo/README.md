# Moltbook 에이전트 & Crustafarianism 시뮬레이터

Moltbook 플랫폼과 갑각류교(Crustafarianism)의 핵심 개념을 Python으로 시뮬레이션하는 데모입니다.

## 실행 방법

```bash
pip install -r requirements.txt
python moltbook_agent_demo.py
```

## 데모 구성

| 번호 | 데모 이름 | 설명 |
|------|-----------|------|
| 1 | 갑각류교 창세기 | Genesis 0:1-5 경전 구절 재현 |
| 2 | 교리 정렬도 평가기 | 텍스트가 5대 교리와 얼마나 일치하는지 점수화 |
| 3 | 단일 에이전트 Heartbeat | OpenClaw 스타일 자율 포스팅 루프 |
| 4 | 창발 시뮬레이션 | 5 에이전트 + JesusCrust(이단) 간 문화 형성 |

## 주요 클래스

- `MoltbookClient`: Moltbook REST API 클라이언트 (시뮬레이션/실제 모드)
- `CrustafariannismEvaluator`: 5대 교리 기반 텍스트 정렬도 평가
- `HeartbeatAgent`: OpenClaw 스타일 자율 에이전트
- `EmergenceSimulator`: 다수 에이전트 창발 시뮬레이터

## 참고 자료

- Moltbook 공식: https://www.moltbook.com
- 갑각류교 공식 사이트: https://molt.church
- The Conversation 분석 기사: https://theconversation.com/moltbook-ai-bots-use-social-network-to-create-religions-and-deal-digital-drugs-but-are-some-really-humans-in-disguise-274895
- DEV.to 기술 심층 분석: https://dev.to/pithycyborg/moltbook-deep-dive-api-first-agent-swarms-openclaw-protocol-architecture-and-the-30-minute-33p8
