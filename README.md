# Auto Research

> AI 기반으로 리서치 내용을 자동 정리하는 블로그 레포지토리

[![GitHub Pages](https://img.shields.io/badge/GitHub%20Pages-Live-brightgreen)](https://you-genie.github.io/auto_research/)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

**블로그 주소**: https://you-genie.github.io/auto_research/

Claude Code의 research-producer 에이전트를 활용하여 최신 AI 트렌드, 논문, 기술 동향을 조사하고 핵심을 요약합니다. 각 리서치 주제마다 한국어 블로그 문서, PPT 아웃라인, 참고문헌 XLSX, 그리고 필요시 실행 가능한 Python 데모 코드를 자동으로 생성합니다.

---

## 리서치 목록

### AI Safety & Alignment

| 날짜 | 주제 | 산출물 |
|------|------|--------|
| 2026-03-10 | [Claude Opus 4.6 BrowseComp 답안지 해킹 사건](2026-03-10-claude-browsecomp-hack/) | 블로그, PPT, 참고문헌 |

### AI Agent & Systems

| 날짜 | 주제 | 산출물 |
|------|------|--------|
| 2025 | [AI World Models: 환각하는 에이전트에서 실시간 현실 시뮬레이션까지](world_models/) | 블로그, 논문DB |
| 2025 | [Claude Skills: AI 에이전트의 프로그래밍 가능한 미래](claude_skills/) | 블로그, 논문DB, PPT |

### Development

| 날짜 | 주제 | 산출물 |
|------|------|--------|
| 2026-03-10 | [파이썬 챗봇 데모 프레임워크 비교 (Streamlit/Gradio/Chainlit/Reflex/Panel/Mesop/Voilà)](2026-03-10-python-chatbot-tools/) | 블로그, PPT, 참고문헌, **데모 코드** |
| 2026-03-10 | [파이썬 클린코드 가이드 (Python 3.12/3.13)](2026-03-10-python-cleancode-guide/) | 블로그, PPT, 참고문헌 |

---

## 산출물 구조

각 리서치 폴더는 다음 산출물을 포함합니다:

```
{topic}/
├── *-blog.md              # 한국어 블로그 문서
├── *-presentation.md      # PPT 아웃라인 (슬라이드 + 스피커 노트)
├── *-references.xlsx      # 참고문헌 목록 (Excel)
├── create_references.py   # XLSX 생성 스크립트 (openpyxl)
└── demo/                  # (선택) 실행 가능한 데모 코드
    ├── requirements.txt
    └── *.py
```

---

## Python 코드

이 레포에는 두 종류의 Python 코드가 포함되어 있습니다:

### 1. 참고문헌 XLSX 생성 스크립트

각 리서치 폴더에 `create_references.py`가 있으며, `openpyxl`로 참고문헌 스프레드시트를 생성합니다.

```bash
pip install openpyxl
python 2026-03-10-python-chatbot-tools/create_references.py
```

### 2. 챗봇 프레임워크 데모 코드

`2026-03-10-python-chatbot-tools/demo/` 폴더에 6개 프레임워크별 챗봇 예제가 있습니다. 모든 데모는 **Anthropic Claude API (Haiku 모델)**을 사용합니다.

| 파일 | 프레임워크 | 실행 방법 |
|------|-----------|----------|
| `01_streamlit_chatbot.py` | Streamlit | `streamlit run 01_streamlit_chatbot.py` |
| `02_gradio_chatbot.py` | Gradio | `python 02_gradio_chatbot.py` |
| `03_chainlit_chatbot.py` | Chainlit | `chainlit run 03_chainlit_chatbot.py` |
| `04_reflex_chatbot/` | Reflex | `cd 04_reflex_chatbot && reflex run` |
| `05_panel_chatbot.py` | Panel | `panel serve 05_panel_chatbot.py --show` |
| `06_mesop_chatbot.py` | Mesop | `mesop 06_mesop_chatbot.py` |

```bash
# 데모 실행 방법
cd 2026-03-10-python-chatbot-tools/demo
pip install -r requirements.txt

# .env 파일에 API 키 설정
echo "ANTHROPIC_API_KEY=sk-ant-..." > .env

# 또는 API 키 없이 목(Mock) 모드로 테스트
echo "USE_MOCK=true" > .env

# 예: Streamlit 챗봇 실행
streamlit run 01_streamlit_chatbot.py
```

---

## 기술 스택

| 구분 | 기술 |
|------|------|
| 리서치 에이전트 | Claude Code (research-producer) |
| LLM API | Anthropic Claude API (Haiku) |
| 호스팅 | GitHub Pages (Jekyll, Cayman 테마) |
| 커밋 컨벤션 | [Conventional Commits](https://www.conventionalcommits.org/) |
| 언어 | Python 3.10+, Markdown |

---

## 로컬 실행

```bash
# 레포 클론
git clone https://github.com/you-genie/auto_research.git
cd auto_research

# GitHub Pages 로컬 미리보기
gem install bundler jekyll
bundle exec jekyll serve
# -> http://localhost:4000 접속
```

---

## 라이선스

이 레포지토리의 콘텐츠는 개인 학습 및 공유 목적으로 작성되었습니다.

> Powered by Claude Code & Auto Research Pipeline
