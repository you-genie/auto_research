"""
Gemini Omni Flash - 텍스트 프롬프트로 비디오 생성 예시

주의: 2026-05-22 기준 공식 Gemini Omni API는 미출시 상태입니다.
이 코드는 기존 Google Generative AI SDK 패턴과
공개된 예상 API 구조를 기반으로 작성한 참고용 코드입니다.

공식 API 출시 후: https://ai.google.dev/gemini-api/docs
Vertex AI 공식 문서:  https://cloud.google.com/vertex-ai/generative-ai/docs

환경변수 설정:
  export GEMINI_API_KEY=your_api_key_here
"""

import os
import time
import base64

# google-generativeai 패키지 필요
# pip install google-generativeai
try:
    import google.generativeai as genai
except ImportError:
    print("[오류] google-generativeai 패키지가 필요합니다: pip install google-generativeai")
    raise


def create_video_from_text(
    prompt: str,
    resolution: str = "720p",
    aspect_ratio: str = "16:9",
    duration_seconds: int = 10,
) -> dict:
    """
    텍스트 프롬프트로 Gemini Omni Flash 비디오 생성 (예상 API 패턴).

    Args:
        prompt: 비디오 생성에 사용할 텍스트 프롬프트
        resolution: 해상도 ("720p", "1080p", "4k") — 티어별 제한 적용
        aspect_ratio: 화면 비율 ("16:9", "9:16", "1:1")
        duration_seconds: 클립 길이 (현재 최대 10초)

    Returns:
        생성 결과 딕셔너리 (video_url, duration, watermark_id 등)
    """
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY 환경변수가 설정되지 않았습니다.")

    # API 클라이언트 초기화
    genai.configure(api_key=api_key)

    print(f"[Gemini Omni Flash] 비디오 생성 시작...")
    print(f"  프롬프트: {prompt[:80]}{'...' if len(prompt) > 80 else ''}")
    print(f"  해상도: {resolution}, 비율: {aspect_ratio}, 길이: {duration_seconds}초")

    # 예상 API 호출 패턴
    # 실제 출시 후 모델명과 파라미터가 변경될 수 있음
    model = genai.GenerativeModel('gemini-omni-flash')

    generation_config = {
        # 출력 모달리티 지정 — 비디오와 텍스트(설명) 동시 요청
        'output_modalities': ['video', 'text'],
        'video_config': {
            'resolution': resolution,
            'aspect_ratio': aspect_ratio,
            'duration_seconds': duration_seconds,
        }
    }

    # SynthID 워터마킹은 비활성화 불가 — 모든 출력에 자동 적용됨
    print("[Omni] SynthID 워터마킹이 자동으로 적용됩니다 (비활성화 불가).")

    try:
        response = model.generate_content(
            contents=[{'role': 'user', 'parts': [{'text': prompt}]}],
            generation_config=generation_config,
        )

        # 응답에서 비디오 데이터 추출
        result = {
            'status': 'success',
            'prompt': prompt,
            'video_data': None,
            'description': None,
            'watermark_id': None,
        }

        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data.mime_type.startswith('video/'):
                result['video_data'] = part.inline_data.data
                print(f"[완료] 비디오 생성 완료. 크기: {len(part.inline_data.data) // 1024}KB")
            elif hasattr(part, 'text'):
                result['description'] = part.text
                print(f"[설명] {part.text[:100]}")

        return result

    except Exception as e:
        # API 미출시 상태이므로 시뮬레이션 응답 반환
        print(f"[경고] API 호출 실패 (미출시 상태): {e}")
        print("[시뮬레이션] 예상 응답 구조를 반환합니다.")
        return {
            'status': 'simulated',
            'prompt': prompt,
            'video_url': 'https://storage.googleapis.com/gemini-omni-output/example.mp4',
            'description': '시뮬레이션: 구슬이 경사면을 따라 정확한 물리 법칙으로 굴러가는 10초 클립',
            'watermark_id': 'synthid-sim-abc123',
            'synthid_enabled': True,
        }


def save_video(video_data: bytes, output_path: str) -> None:
    """생성된 비디오를 파일로 저장."""
    with open(output_path, 'wb') as f:
        f.write(video_data)
    print(f"[저장] 비디오 저장 완료: {output_path}")


if __name__ == '__main__':
    # --- 예시 1: 물리 시뮬레이션 데모 ---
    demo_prompt_1 = (
        "A marble rolling down a curved wooden ramp, "
        "with accurate physics and motion blur. "
        "Cinematic lighting, slow motion at the end. "
        "No text, no people."
    )

    result1 = create_video_from_text(
        prompt=demo_prompt_1,
        resolution="1080p",
        aspect_ratio="16:9",
        duration_seconds=10,
    )
    print(f"\n결과 1: {result1.get('status')}")
    if result1.get('video_data'):
        save_video(result1['video_data'], '/tmp/omni_marble.mp4')

    print("\n" + "="*60)

    # --- 예시 2: 세로형 YouTube Shorts 스타일 ---
    demo_prompt_2 = (
        "A claymation-style short about how photosynthesis works. "
        "Colorful, educational, suitable for children. "
        "Vertical format for mobile viewing."
    )

    result2 = create_video_from_text(
        prompt=demo_prompt_2,
        resolution="1080p",
        aspect_ratio="9:16",
        duration_seconds=10,
    )
    print(f"\n결과 2: {result2.get('status')}")
    print(f"SynthID 활성화: {result2.get('synthid_enabled', True)}")

    print("\n" + "="*60)
    print("참고: 공식 API 출시 후 https://ai.google.dev/gemini-api/docs 확인 필요")
