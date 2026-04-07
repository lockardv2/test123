#!/usr/bin/env python3
"""
이미지 분석 스크립트 - Claude API를 사용하여 이미지를 분석합니다.
"""

import anthropic
import base64
import sys
from pathlib import Path


def analyze_image_from_file(image_path: str, question: str = "이 이미지를 자세히 설명해주세요.") -> str:
    """
    로컬 이미지 파일을 Claude API로 분석합니다.

    Args:
        image_path: 분석할 이미지 파일 경로
        question: 이미지에 대해 물어볼 질문

    Returns:
        Claude의 이미지 분석 결과
    """
    client = anthropic.Anthropic()

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    # MIME 타입 결정
    suffix = path.suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(suffix)
    if not media_type:
        raise ValueError(f"지원하지 않는 이미지 형식입니다: {suffix}")

    # 이미지를 base64로 인코딩
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    print(f"이미지 분석 중: {image_path}")
    print(f"질문: {question}")
    print("-" * 50)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=16000,
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
                        "text": question,
                    },
                ],
            }
        ],
    )

    result = response.content[0].text
    return result


def analyze_image_from_url(image_url: str, question: str = "이 이미지를 자세히 설명해주세요.") -> str:
    """
    URL의 이미지를 Claude API로 분석합니다.

    Args:
        image_url: 분석할 이미지의 URL
        question: 이미지에 대해 물어볼 질문

    Returns:
        Claude의 이미지 분석 결과
    """
    client = anthropic.Anthropic()

    print(f"이미지 URL 분석 중: {image_url}")
    print(f"질문: {question}")
    print("-" * 50)

    response = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=16000,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "url",
                            "url": image_url,
                        },
                    },
                    {
                        "type": "text",
                        "text": question,
                    },
                ],
            }
        ],
    )

    result = response.content[0].text
    return result


def main():
    """메인 함수: 커맨드라인 인자로 이미지 파일 경로를 받아 분석합니다."""
    if len(sys.argv) < 2:
        print("사용법: python analyze_image.py <이미지_경로> [질문]")
        print("예시: python analyze_image.py image.png '이 이미지에서 무엇이 보이나요?'")
        sys.exit(1)

    image_path = sys.argv[1]
    question = sys.argv[2] if len(sys.argv) > 2 else "이 이미지를 자세히 설명해주세요. 이미지에 있는 모든 요소를 분석해주세요."

    result = analyze_image_from_file(image_path, question)
    print(result)


if __name__ == "__main__":
    main()
