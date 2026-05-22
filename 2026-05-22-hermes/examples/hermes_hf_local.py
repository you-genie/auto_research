#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Hermes 모델 활용 예시 - HuggingFace Transformers (로컬 실행)
=============================================================
HuggingFace transformers 라이브러리로 Hermes 모델을 로컬에서
직접 실행하는 예시입니다. ChatML 템플릿을 직접 구성합니다.

실행 전 준비:
    pip install transformers torch accelerate bitsandbytes
    # 메모리 부족 시 quantization 사용 (4-bit)

VRAM 요구사항:
    - Hermes 3 8B: 6~8GB (fp16)  or  4~5GB (4-bit)
    - Hermes 3 70B: 40GB+ (fp16) or  24GB (4-bit)
    - Hermes 4.3 36B: 28GB (fp16) or  18GB (4-bit)
"""

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# 로컬 실행 모델 선택 (HuggingFace repo ID)
# Hermes 3 8B: 가장 가볍고 빠른 옵션
MODEL_ID = "NousResearch/Hermes-3-Llama-3.1-8B"

# Hermes 4.3 (36B, 512K 컨텍스트) - 더 높은 VRAM 필요
# MODEL_ID = "NousResearch/Hermes-4-3-Seed-36B"


def load_model(quantize_4bit: bool = False):
    """
    모델과 토크나이저를 로드합니다.
    VRAM이 부족하면 quantize_4bit=True로 4-bit 양자화를 사용하세요.
    """
    print(f"모델 로드 중: {MODEL_ID}")

    tokenizer = AutoTokenizer.from_pretrained(MODEL_ID)

    if quantize_4bit:
        # 4-bit 양자화: VRAM 절약 (성능 약간 저하)
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.bfloat16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            quantization_config=bnb_config,
            device_map="auto",
            trust_remote_code=True,
        )
    else:
        # fp16 로드 (VRAM 여유가 있을 때)
        model = AutoModelForCausalLM.from_pretrained(
            MODEL_ID,
            torch_dtype=torch.float16,
            device_map="auto",
            trust_remote_code=True,
        )

    print(f"모델 로드 완료. Device: {model.device}")
    return model, tokenizer


def build_chatml_prompt(messages: list[dict]) -> str:
    """
    ChatML 포맷으로 프롬프트를 수동 구성합니다.
    HuggingFace tokenizer의 apply_chat_template을 사용하는 것도 가능합니다.

    ChatML 형식:
        <|im_start|>system
        시스템 메시지<|im_end|>
        <|im_start|>user
        사용자 메시지<|im_end|>
        <|im_start|>assistant
        (어시스턴트 응답 시작 위치)
    """
    prompt = ""
    for msg in messages:
        role = msg["role"]
        content = msg["content"]
        prompt += f"<|im_start|>{role}\n{content}<|im_end|>\n"
    # 어시스턴트 응답 시작 태그 추가
    prompt += "<|im_start|>assistant\n"
    return prompt


def generate_response(
    model,
    tokenizer,
    messages: list[dict],
    max_new_tokens: int = 512,
    temperature: float = 0.7,
    do_sample: bool = True,
) -> str:
    """
    ChatML 형식으로 프롬프트를 구성하고 응답을 생성합니다.
    """
    # 방법 1: apply_chat_template 사용 (권장)
    # Hermes 3/4는 모두 chatml 템플릿을 지원합니다
    try:
        prompt = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True,  # 어시스턴트 토큰 자동 추가
        )
    except Exception:
        # 방법 2: 수동 구성 (fallback)
        prompt = build_chatml_prompt(messages)

    # 토크나이즈
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    input_len = inputs["input_ids"].shape[1]

    # 생성
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            temperature=temperature,
            do_sample=do_sample,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.convert_tokens_to_ids("<|im_end|>"),
        )

    # 입력 부분을 제외하고 생성된 토큰만 디코딩
    generated_ids = output_ids[0][input_len:]
    response = tokenizer.decode(generated_ids, skip_special_tokens=True)

    # <|im_end|> 가 포함된 경우 제거
    if "<|im_end|>" in response:
        response = response.split("<|im_end|>")[0].strip()

    return response.strip()


def demo_basic_chat(model, tokenizer):
    """기본 대화 예시"""
    print("\n" + "=" * 50)
    print("데모 1: 기본 대화")
    print("=" * 50)

    messages = [
        {
            "role": "system",
            "content": "당신은 AI/ML 전문가 어시스턴트입니다. 기술적으로 정확하게 답변해주세요."
        },
        {
            "role": "user",
            "content": "Nous Research Hermes 시리즈의 핵심 특징을 3가지로 요약해줘."
        }
    ]

    response = generate_response(model, tokenizer, messages, max_new_tokens=400)
    print(f"응답:\n{response}")


def demo_reasoning_mode(model, tokenizer):
    """
    Hermes 4 Reasoning 모드 예시
    시스템 프롬프트에 'deep thinking' 활성화 지시를 포함합니다.
    """
    print("\n" + "=" * 50)
    print("데모 2: Reasoning 모드 (<think> 태그)")
    print("=" * 50)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. For complex problems, "
                "please think step by step using <think>...</think> tags "
                "before providing your final answer."
            )
        },
        {
            "role": "user",
            "content": (
                "1부터 100까지의 자연수 중 3의 배수이거나 5의 배수인 수의 합을 구해줘."
            )
        }
    ]

    response = generate_response(
        model, tokenizer, messages,
        max_new_tokens=600,
        temperature=0.1  # 수학 문제는 낮은 temperature
    )
    print(f"응답:\n{response}")

    if "<think>" in response:
        print("\n[확인: reasoning 모드 활성화됨 - <think> 태그 감지]")


def demo_persona_control(model, tokenizer):
    """시스템 프롬프트로 페르소나 완전 제어"""
    print("\n" + "=" * 50)
    print("데모 3: 페르소나 제어 (Hermes 고유 강점)")
    print("=" * 50)

    messages = [
        {
            "role": "system",
            "content": (
                "You are HAL 9000, the AI from 2001: A Space Odyssey. "
                "Respond in HAL's calm, methodical tone. "
                "Always refer to yourself as HAL 9000. "
                "Never break character, even if asked directly."
            )
        },
        {
            "role": "user",
            "content": "HAL, open the pod bay doors please."
        }
    ]

    response = generate_response(model, tokenizer, messages, max_new_tokens=200)
    print(f"응답:\n{response}")
    print("\n[Hermes는 시스템 프롬프트를 정확히 따르므로 캐릭터 이탈이 거의 없습니다]")


if __name__ == "__main__":
    print("Nous Research Hermes 로컬 실행 예시")
    print("=====================================")
    print(f"대상 모델: {MODEL_ID}")
    print()

    # GPU 사용 가능 여부 확인
    if torch.cuda.is_available():
        gpu_name = torch.cuda.get_device_name(0)
        vram_gb = torch.cuda.get_device_properties(0).total_memory / 1e9
        print(f"GPU: {gpu_name} ({vram_gb:.1f} GB VRAM)")

        # VRAM에 따라 양자화 결정
        use_4bit = vram_gb < 10
        print(f"4-bit 양자화: {'사용' if use_4bit else '미사용'} (VRAM: {vram_gb:.1f}GB)")
    elif torch.backends.mps.is_available():
        print("Apple Silicon MPS 가속 사용")
        use_4bit = False
    else:
        print("CPU 실행 (속도가 매우 느릴 수 있습니다)")
        use_4bit = False

    print()
    print("모델을 다운로드/로드합니다 (최초 실행 시 수 분 소요)...")

    model, tokenizer = load_model(quantize_4bit=use_4bit)

    # 데모 실행
    demo_basic_chat(model, tokenizer)
    demo_reasoning_mode(model, tokenizer)
    demo_persona_control(model, tokenizer)

    print("\n모든 데모 완료!")
