# 파이썬 챗봇 프레임워크 데모 모음

이 디렉토리에는 7가지 파이썬 챗봇 프레임워크로 구현한 동일한 GPT-4o 챗봇 데모가 포함되어 있습니다.

## 폴더 구조

```
demo/
├── README.md               ← 이 파일
├── requirements.txt        ← 전체 의존성
├── .env.example            ← 환경변수 예시
├── 01_streamlit_chatbot.py ← Streamlit 챗봇
├── 02_gradio_chatbot.py    ← Gradio 챗봇
├── 03_chainlit_chatbot.py  ← Chainlit 챗봇
├── 04_reflex_chatbot/      ← Reflex 챗봇 (폴더)
│   ├── chatbot.py
│   └── rxconfig.py
├── 05_panel_chatbot.py     ← Panel 챗봇
├── 06_mesop_chatbot.py     ← Mesop 챗봇
└── 07_voila_chatbot.ipynb  ← Voilà 챗봇 (Jupyter 노트북)
```

## 설치 방법

```bash
# 1. 가상환경 생성
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 2. 의존성 설치
pip install -r requirements.txt

# 3. 환경변수 설정
cp .env.example .env
# .env 파일을 열어 OPENAI_API_KEY를 입력하세요
```

## 각 데모 실행 방법

### 1. Streamlit
```bash
streamlit run 01_streamlit_chatbot.py
# 브라우저에서 http://localhost:8501 접속
```

### 2. Gradio
```bash
python 02_gradio_chatbot.py
# 브라우저에서 http://localhost:7860 접속
```

### 3. Chainlit
```bash
chainlit run 03_chainlit_chatbot.py
# 브라우저에서 http://localhost:8000 접속
```

### 4. Reflex
```bash
cd 04_reflex_chatbot
reflex init
reflex run
# 브라우저에서 http://localhost:3000 접속
```

### 5. Panel
```bash
panel serve 05_panel_chatbot.py --show
# 브라우저에서 http://localhost:5006 접속
```

### 6. Mesop
```bash
mesop 06_mesop_chatbot.py
# 브라우저에서 http://localhost:32123 접속
```

### 7. Voilà (Jupyter 노트북)
```bash
voila 07_voila_chatbot.ipynb
# 브라우저에서 자동으로 열림
```

## OpenAI API 키 없이 테스트하기

`USE_MOCK=true` 환경변수를 설정하면 실제 API 호출 없이 에코 응답으로 테스트할 수 있습니다:

```bash
USE_MOCK=true streamlit run 01_streamlit_chatbot.py
```

## 주의사항

- Python 3.10 이상 권장
- Reflex는 초기 빌드에 시간이 걸릴 수 있습니다 (1-3분)
- Chainlit은 `chainlit run` 명령어를 사용해야 합니다 (`python` 직접 실행 불가)
- Voilà는 반드시 `.ipynb` 파일을 사용해야 합니다
