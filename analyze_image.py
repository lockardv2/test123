#!/usr/bin/env python3
"""
이미지 분석 스크립트 - Claude API를 사용하여 이미지를 분석합니다.
사용법: python analyze_image.py <이미지_파일_경로> [분석_프롬프트]
"""

import sys
import base64
import anthropic
from pathlib import Path

SUPPORTED_FORMATS = {
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".png": "image/png",
    ".gif": "image/gif",
    ".webp": "image/webp",
}


def load_image(image_path: str) -> tuple[str, str]:
    """이미지 파일을 base64로 인코딩하여 반환합니다."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    ext = path.suffix.lower()
    if ext not in SUPPORTED_FORMATS:
        raise ValueError(f"지원하지 않는 형식입니다: {ext}. 지원 형식: {', '.join(SUPPORTED_FORMATS)}")

    with open(path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return image_data, SUPPORTED_FORMATS[ext]


def analyze_image(image_path: str, prompt: str = "이 이미지를 자세히 분석해주세요.") -> str:
    """Claude API를 사용하여 이미지를 분석합니다."""
    client = anthropic.Anthropic()

    image_data, media_type = load_image(image_path)

    print(f"이미지 분석 중: {image_path}")
    print(f"프롬프트: {prompt}\n")

    with client.messages.stream(
        model="claude-opus-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": media_type,
                            "data": image_data,
                        },
                    },
                    {
                        "type": "text",
                        "text": prompt,
                    },
                ],
            }
        ],
    ) as stream:
        print("=== 분석 결과 ===")
        for text in stream.text_stream:
            print(text, end="", flush=True)
        print("\n")
        return stream.get_final_message().content[0].text


def main():
    if len(sys.argv) < 2:
        print("사용법: python analyze_image.py <이미지_파일_경로> [분석_프롬프트]")
        print("예시:  python analyze_image.py photo.png")
        print("예시:  python analyze_image.py photo.png '이미지의 색상과 구성을 설명해줘'")
        sys.exit(1)

    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "이 이미지를 자세히 분석해주세요."

    try:
        analyze_image(image_path, prompt)
    except FileNotFoundError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"오류: {e}", file=sys.stderr)
        sys.exit(1)
    except anthropic.AuthenticationError:
        print("오류: ANTHROPIC_API_KEY 환경 변수를 설정해주세요.", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
