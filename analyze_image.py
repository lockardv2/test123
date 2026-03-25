#!/usr/bin/env python3
"""
이미지 분석 스크립트 - Claude API를 사용하여 이미지를 분석합니다.
사용법: python analyze_image.py <이미지_경로>
"""

import anthropic
import base64
import sys
from pathlib import Path


def analyze_image(image_path: str) -> str:
    """이미지를 분석하고 결과를 반환합니다."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    # 미디어 타입 결정
    suffix = path.suffix.lower()
    media_types = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_types.get(suffix, "image/jpeg")

    # 이미지를 Base64로 인코딩
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    client = anthropic.Anthropic()

    print(f"이미지 분석 중: {image_path}")

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
                        "text": "이 이미지를 자세히 분석해 주세요. 무엇이 보이는지, 주요 특징, 색상, 분위기 등을 설명해 주세요.",
                    },
                ],
            }
        ],
    ) as stream:
        print("\n분석 결과:")
        print("-" * 40)
        result = ""
        for text in stream.text_stream:
            print(text, end="", flush=True)
            result += text
        print("\n" + "-" * 40)

    return result


def main():
    if len(sys.argv) < 2:
        print("사용법: python analyze_image.py <이미지_경로>")
        print("예시: python analyze_image.py photo.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    try:
        analyze_image(image_path)
    except FileNotFoundError as e:
        print(f"오류: {e}")
        sys.exit(1)
    except anthropic.AuthenticationError:
        print("오류: ANTHROPIC_API_KEY 환경변수를 설정해 주세요.")
        sys.exit(1)
    except anthropic.APIError as e:
        print(f"API 오류: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
