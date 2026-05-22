"""
Gemini Omni Flash - 이미지+텍스트 입력으로 대화형 멀티턴 편집 예시

이 예시는 Omni의 핵심 차별점인 "대화형 반복 편집" 기능을 보여줍니다.
기존 Veo(단일 생성)와 달리 Omni는 멀티턴 대화로 편집을 반복할 수 있습니다.

주의: 2026-05-22 기준 공식 API 미출시 상태. 참고용 코드.

환경변수:
  export GEMINI_API_KEY=your_api_key_here
"""

import os
import pathlib

try:
    import google.generativeai as genai
except ImportError:
    print("[오류] google-generativeai 패키지가 필요합니다: pip install google-generativeai")
    raise


class OmniConversationalEditor:
    """
    Gemini Omni Flash의 대화형 멀티턴 편집 세션을 관리하는 클래스.

    Omni의 핵심 강점: 한번 생성한 비디오를 대화로 반복 편집해도
    캐릭터·배경·물리 일관성이 유지됨.
    """

    def __init__(self, api_key: str | None = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY 환경변수가 필요합니다.")

        genai.configure(api_key=self.api_key)

        # Omni는 멀티턴 편집을 위해 공유 컨텍스트 창 유지
        self.model = genai.GenerativeModel('gemini-omni-flash')
        self.chat = self.model.start_chat(history=[])
        self.turn_count = 0

        print("[OmniEditor] 편집 세션 초기화 완료.")
        print("  SynthID 워터마킹: 활성화 (모든 출력 자동 적용)")

    def create_initial_video(
        self,
        image_path: str | None = None,
        text_prompt: str = "",
    ) -> dict:
        """
        초기 비디오를 이미지 + 텍스트 프롬프트로 생성.

        Args:
            image_path: 참조 이미지 경로 (None이면 텍스트만 사용)
            text_prompt: 비디오 생성 지시
        """
        self.turn_count += 1
        print(f"\n[턴 {self.turn_count}] 초기 비디오 생성")

        parts = [{'text': text_prompt}]

        if image_path:
            img_path = pathlib.Path(image_path)
            if img_path.exists():
                with open(img_path, 'rb') as f:
                    img_bytes = f.read()
                # MIME 타입 추론
                suffix_map = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
                              '.png': 'image/png', '.webp': 'image/webp'}
                mime = suffix_map.get(img_path.suffix.lower(), 'image/jpeg')
                parts.insert(0, {'inline_data': {'mime_type': mime, 'data': img_bytes}})
                print(f"  참조 이미지: {image_path}")
            else:
                print(f"  [경고] 이미지 파일 없음: {image_path}. 텍스트만 사용.")

        print(f"  프롬프트: {text_prompt}")

        try:
            response = self.chat.send_message(
                content=parts,
                generation_config={
                    'output_modalities': ['video', 'text'],
                    'video_config': {'resolution': '720p', 'aspect_ratio': '16:9', 'duration_seconds': 10}
                }
            )
            return self._parse_response(response)
        except Exception as e:
            print(f"  [시뮬레이션] API 미출시 상태: {e}")
            return {
                'status': 'simulated',
                'turn': self.turn_count,
                'description': '시뮬레이션: 초기 비디오 생성됨. 캐릭터/배경/물리 상태 컨텍스트에 저장.',
                'video_url': f'https://omni-sim.example.com/video_turn_{self.turn_count}.mp4',
            }

    def edit_video(self, edit_instruction: str) -> dict:
        """
        대화형 편집 지시로 이전 비디오를 수정.

        Args:
            edit_instruction: 편집 지시 (예: "조명을 따뜻하게 바꿔", "배경을 도시로 변경해")

        Omni 특징: 이전 컨텍스트(캐릭터, 물리, 배경)가 공유 컨텍스트 창에 유지되므로
        연속 편집 후에도 일관성이 유지됨. (기존 Veo: 매번 재생성 필요)
        """
        self.turn_count += 1
        print(f"\n[턴 {self.turn_count}] 편집: '{edit_instruction}'")

        try:
            response = self.chat.send_message(
                content=[{'text': edit_instruction}],
                generation_config={
                    'output_modalities': ['video', 'text'],
                    'video_config': {'resolution': '720p', 'aspect_ratio': '16:9', 'duration_seconds': 10}
                }
            )
            return self._parse_response(response)
        except Exception as e:
            print(f"  [시뮬레이션] API 미출시 상태: {e}")
            return {
                'status': 'simulated',
                'turn': self.turn_count,
                'instruction': edit_instruction,
                'description': f'시뮬레이션: "{edit_instruction}" 적용됨. 이전 컨텍스트 일관성 유지.',
                'video_url': f'https://omni-sim.example.com/video_turn_{self.turn_count}.mp4',
            }

    def _parse_response(self, response) -> dict:
        """응답 객체에서 비디오 및 텍스트 추출."""
        result = {'status': 'success', 'turn': self.turn_count, 'video_data': None, 'description': None}
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data.mime_type.startswith('video/'):
                result['video_data'] = part.inline_data.data
            elif hasattr(part, 'text'):
                result['description'] = part.text
        return result


if __name__ == '__main__':
    print("=" * 60)
    print("Gemini Omni Flash - 대화형 멀티턴 편집 데모")
    print("=" * 60)

    editor = OmniConversationalEditor()

    # --- 단계 1: 초기 비디오 생성 ---
    step1 = editor.create_initial_video(
        image_path=None,  # 실제 사용 시: '/path/to/reference_image.jpg'
        text_prompt=(
            "A lone robot walking through a misty forest at dawn. "
            "Cinematic, photorealistic. No text or people."
        ),
    )
    print(f"  결과: {step1.get('description', step1.get('video_url'))}")

    # --- 단계 2: 대화형 편집 1 — 조명 변경 ---
    step2 = editor.edit_video("조명을 황금빛 석양으로 바꿔줘.")
    print(f"  결과: {step2.get('description', step2.get('video_url'))}")

    # --- 단계 3: 대화형 편집 2 — 배경 추가 ---
    step3 = editor.edit_video("배경에 반짝이는 별을 추가해줘.")
    print(f"  결과: {step3.get('description', step3.get('video_url'))}")

    # --- 단계 4: 대화형 편집 3 — 카메라 각도 변경 ---
    step4 = editor.edit_video("카메라를 로봇 얼굴 클로즈업으로 전환해줘.")
    print(f"  결과: {step4.get('description', step4.get('video_url'))}")

    print("\n" + "=" * 60)
    print("[핵심] 각 편집 단계에서 로봇 외형, 숲 배경, 동작 일관성이 유지됩니다.")
    print("[주의] 음성/오디오 편집은 현재 보류 상태입니다 (딥페이크 안전 정책).")
    print("[SynthID] 모든 출력 비디오에 SynthID 워터마킹이 자동 적용됩니다.")
    print("\n공식 API 출시 후: https://ai.google.dev/gemini-api/docs")
