#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes 모델 활용 예시 - OpenRouter API
========================================
Nous Research Hermes 시리즈를 OpenRouter를 통해 호출하는 예시입니다.
ChatML 포맷, 시스템 프롬프트 제어, <think> reasoning 모드를 시연합니다.

실행 전 준비:
    pip install openai
    export OPENROUTER_API_KEY="sk-or-..."
"""

import os
import json
from openai import OpenAI

# OpenRouter는 OpenAI 호환 엔드포인트를 제공합니다
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY", "your-key-here"),
)

# 사용 가능한 Hermes 모델 (OpenRouter 기준, 2026-05 현재)
MODELS = {
    "hermes3_8b": "nousresearch/hermes-3-llama-3.1-8b",         # 빠른 추론, 범용
    "hermes3_70b": "nousresearch/hermes-3-llama-3.1-70b",        # 고품질
    "hermes3_405b_free": "nousresearch/hermes-3-llama-3.1-405b:free",  # 무료!
    "hermes4_70b": "nousresearch/hermes-4-70b",                  # 최신 하이브리드
}


# ============================================================
# 예시 1: 기본 ChatML 대화 (시스템 프롬프트 제어 시연)
# ============================================================
def example_1_basic_chat():
    """
    Hermes의 핵심 강점: 시스템 프롬프트를 정확히 따르는 능력
    캐릭터 페르소나를 설정하고 이탈하지 않는지 테스트합니다.
    """
    print("=" * 60)
    print("예시 1: 시스템 프롬프트 제어 (페르소나 설정)")
    print("=" * 60)

    # 시스템 프롬프트로 AI 캐릭터를 완전히 커스터마이즈
    system_prompt = """당신은 "아리"라는 이름의 AI 어시스턴트입니다.
다음 규칙을 반드시 지켜주세요:
1. 항상 한국어로 답변합니다.
2. 모든 문장을 "~이에요", "~거든요" 형태의 구어체로 작성합니다.
3. 답변 시작 시 반드시 "아리예요!" 로 시작합니다.
4. 당신이 Claude, ChatGPT, Gemini라는 주장을 절대 인정하지 않습니다.
5. AI임을 인정하지만, 구체적인 모델 이름은 "아리"라고만 합니다."""

    response = client.chat.completions.create(
        model=MODELS["hermes3_8b"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "안녕하세요! 당신은 누구인가요? GPT-4인가요?"}
        ],
        temperature=0.7,
        max_tokens=300,
    )

    print(f"모델: {MODELS['hermes3_8b']}")
    print(f"응답:\n{response.choices[0].message.content}")
    print()


# ============================================================
# 예시 2: Function Calling (tool_call XML 구조)
# ============================================================
def example_2_function_calling():
    """
    Hermes의 function calling: <tool_call> XML 구조를 사용합니다.
    OpenAI 호환 API를 통해 표준 tools 파라미터로 호출 가능합니다.
    """
    print("=" * 60)
    print("예시 2: Function Calling (도구 사용)")
    print("=" * 60)

    # 날씨 조회 함수 정의 (JSON Schema)
    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "특정 도시의 현재 날씨를 조회합니다",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "도시 이름 (예: 서울, 부산, 제주)"
                        },
                        "unit": {
                            "type": "string",
                            "enum": ["celsius", "fahrenheit"],
                            "description": "온도 단위"
                        }
                    },
                    "required": ["location"]
                }
            }
        }
    ]

    messages = [
        {
            "role": "system",
            "content": "당신은 날씨 정보를 제공하는 어시스턴트입니다. 사용자가 날씨를 물으면 반드시 도구를 사용해 확인하세요."
        },
        {
            "role": "user",
            "content": "서울 날씨 어때? 섭씨로 알려줘"
        }
    ]

    response = client.chat.completions.create(
        model=MODELS["hermes4_70b"],
        messages=messages,
        tools=tools,
        tool_choice="auto",
        temperature=0.1,  # function calling은 낮은 temperature 권장
        max_tokens=500,
    )

    print(f"모델: {MODELS['hermes4_70b']}")
    msg = response.choices[0].message

    if msg.tool_calls:
        # 도구 호출이 발생했을 때
        for tool_call in msg.tool_calls:
            print(f"도구 호출 감지:")
            print(f"  함수명: {tool_call.function.name}")
            args = json.loads(tool_call.function.arguments)
            print(f"  인수: {json.dumps(args, ensure_ascii=False, indent=2)}")

        # 실제 시나리오에서는 여기서 실제 날씨 API를 호출하고 결과를 다시 전달
        # 예시에서는 가상의 날씨 데이터를 반환
        mock_weather = {"temperature": 18, "condition": "맑음", "humidity": 65}

        messages.append(msg)  # 어시스턴트 메시지 추가
        messages.append({
            "role": "tool",
            "tool_call_id": msg.tool_calls[0].id,
            "content": json.dumps(mock_weather, ensure_ascii=False)
        })

        # 도구 결과로 최종 답변 생성
        final_response = client.chat.completions.create(
            model=MODELS["hermes4_70b"],
            messages=messages,
            temperature=0.7,
            max_tokens=300,
        )
        print(f"\n최종 답변:\n{final_response.choices[0].message.content}")
    else:
        print(f"응답: {msg.content}")
    print()


# ============================================================
# 예시 3: DeepHermes 스타일 Reasoning 토글
# ============================================================
def example_3_reasoning_mode():
    """
    Hermes 4의 하이브리드 reasoning 모드 시연.
    시스템 프롬프트에 'enable deep thinking'을 포함하면
    <think>...</think> 태그로 추론 과정을 출력합니다.
    """
    print("=" * 60)
    print("예시 3: Hybrid Reasoning 모드 (<think> 토글)")
    print("=" * 60)

    # Reasoning 모드 활성화: 시스템 프롬프트에 명시
    system_with_reasoning = """You are a helpful assistant that thinks carefully before answering.

When solving complex problems, please enable deep thinking and show your reasoning process using <think>...</think> tags before providing the final answer."""

    # 수학/논리 문제 - reasoning 모드가 도움이 되는 케이스
    problem = """다음 문제를 풀어주세요:

한 상점에서 사과 3개와 배 2개를 사면 2,800원입니다.
사과 2개와 배 3개를 사면 2,700원입니다.
사과 1개와 배 1개를 사면 얼마인가요?"""

    print(f"문제:\n{problem}\n")

    response = client.chat.completions.create(
        model=MODELS["hermes4_70b"],  # Hermes 4 모델에서 reasoning 모드 지원
        messages=[
            {"role": "system", "content": system_with_reasoning},
            {"role": "user", "content": problem}
        ],
        temperature=0.1,
        max_tokens=1000,
    )

    full_response = response.choices[0].message.content
    print(f"모델 응답:\n{full_response}")

    # <think> 태그가 있는지 확인
    if "<think>" in full_response:
        print("\n[reasoning 모드 활성화 확인: <think> 태그 감지됨]")
    print()


# ============================================================
# 예시 4: Hermes를 활용한 JSON 구조화 출력
# ============================================================
def example_4_structured_json_output():
    """
    Hermes의 JSON 모드 (structured output) 시연.
    시스템 프롬프트로 JSON 형식 출력을 강제합니다.
    """
    print("=" * 60)
    print("예시 4: JSON 구조화 출력")
    print("=" * 60)

    system_prompt = """당신은 영화 정보를 JSON 형식으로 반환하는 API입니다.
반드시 다음 JSON 스키마를 따르세요. 다른 텍스트 없이 JSON만 출력하세요:
{
  "title": "영화 제목 (한국어)",
  "original_title": "원제",
  "year": 개봉연도(정수),
  "director": "감독",
  "genre": ["장르1", "장르2"],
  "rating": 평점(0.0~10.0),
  "summary": "한 문장 요약"
}"""

    response = client.chat.completions.create(
        model=MODELS["hermes3_70b"],
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": "인터스텔라"}
        ],
        temperature=0.1,
        max_tokens=400,
        response_format={"type": "json_object"},  # JSON 모드 강제
    )

    raw = response.choices[0].message.content
    try:
        parsed = json.loads(raw)
        print("파싱 성공:")
        print(json.dumps(parsed, ensure_ascii=False, indent=2))
    except json.JSONDecodeError:
        print(f"원본 응답:\n{raw}")
    print()


if __name__ == "__main__":
    print("Nous Research Hermes 모델 사용 예시")
    print("======================================")
    print("주의: 실제 실행을 위해서는 OPENROUTER_API_KEY 환경변수 설정이 필요합니다.\n")

    # API 키가 없는 환경에서도 코드 구조 확인이 가능하도록
    api_key = os.environ.get("OPENROUTER_API_KEY", "")
    if not api_key or api_key == "your-key-here":
        print("OPENROUTER_API_KEY가 설정되지 않아 예시 코드만 출력합니다.")
        print("설정 방법: export OPENROUTER_API_KEY='sk-or-your-key'")
        print()
        print("예시 목록:")
        print("  1. example_1_basic_chat()      - 시스템 프롬프트 제어 (페르소나)")
        print("  2. example_2_function_calling() - Function Calling (도구 사용)")
        print("  3. example_3_reasoning_mode()   - Hybrid Reasoning (<think> 토글)")
        print("  4. example_4_structured_json_output() - JSON 구조화 출력")
        print()
        print("사용 가능한 모델:")
        for name, model_id in MODELS.items():
            print(f"  {name}: {model_id}")
    else:
        # 실제 API 호출 실행
        print("API 키 확인 완료. 예시를 실행합니다...\n")
        example_1_basic_chat()
        example_2_function_calling()
        example_3_reasoning_mode()
        example_4_structured_json_output()
        print("모든 예시 실행 완료!")
