# Hermes 예시 코드

Nous Research Hermes 모델을 사용하는 두 가지 예시입니다.

## 파일 목록

| 파일 | 설명 | 요구사항 |
|------|------|---------|
| `hermes_openrouter_example.py` | OpenRouter API를 통한 호출 (클라우드, 무료 옵션 포함) | `openai` 패키지, OpenRouter API 키 |
| `hermes_hf_local.py` | HuggingFace Transformers 로컬 실행 | `transformers`, `torch`, GPU 권장 |

## 빠른 시작

### 1. OpenRouter (가장 쉬운 방법)

```bash
pip install openai
export OPENROUTER_API_KEY="sk-or-..."
python hermes_openrouter_example.py
```

무료 모델 사용: `nousresearch/hermes-3-llama-3.1-405b:free`

### 2. 로컬 실행 (HuggingFace)

```bash
pip install transformers torch accelerate bitsandbytes
python hermes_hf_local.py
```

VRAM 요구사항:
- Hermes 3 8B: 6~8GB (fp16) / 4~5GB (4-bit)
- Hermes 4 70B: 40GB+ (fp16) / 24GB (4-bit)

### 3. Ollama (가장 쉬운 로컬 실행)

```bash
ollama pull nous-hermes3:8b
ollama run nous-hermes3:8b
```

## 시연 내용

- **예시 1**: 시스템 프롬프트로 페르소나 설정 (Hermes 고유 강점)
- **예시 2**: Function Calling / 도구 사용 (`<tool_call>` 구조)
- **예시 3**: Hybrid Reasoning 모드 (`<think>` 태그 토글)
- **예시 4**: JSON 구조화 출력

## ChatML 프롬프트 형식

```
<|im_start|>system
시스템 메시지<|im_end|>
<|im_start|>user
사용자 입력<|im_end|>
<|im_start|>assistant
```

Hermes 1부터 4.3까지 모든 버전이 동일한 형식을 사용합니다.
