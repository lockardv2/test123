import anthropic
import base64
import sys
import os


def encode_image_file(image_path: str) -> tuple[str, str]:
    """이미지 파일을 base64로 인코딩하고 미디어 타입을 반환합니다."""
    ext = os.path.splitext(image_path)[1].lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(ext, "image/jpeg")

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    return image_data, media_type


def analyze_image_file(image_path: str) -> str:
    """로컬 이미지 파일을 Claude API로 분석합니다."""
    client = anthropic.Anthropic()
    image_data, media_type = encode_image_file(image_path)

    message = client.messages.create(
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
                        "text": (
                            "이 이미지를 자세히 분석해주세요. 다음 항목들을 포함해서 설명해주세요:\n"
                            "1. 이미지에 있는 주요 객체/피사체\n"
                            "2. 색상 및 스타일\n"
                            "3. 전반적인 분위기나 느낌\n"
                            "4. 기타 눈에 띄는 세부 사항"
                        ),
                    },
                ],
            }
        ],
    )

    return message.content[0].text


def analyze_image_url(image_url: str) -> str:
    """URL로 제공된 이미지를 Claude API로 분석합니다."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=1024,
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
                        "text": (
                            "이 이미지를 자세히 분석해주세요. 다음 항목들을 포함해서 설명해주세요:\n"
                            "1. 이미지에 있는 주요 객체/피사체\n"
                            "2. 색상 및 스타일\n"
                            "3. 전반적인 분위기나 느낌\n"
                            "4. 기타 눈에 띄는 세부 사항"
                        ),
                    },
                ],
            }
        ],
    )

    return message.content[0].text


def main():
    if len(sys.argv) < 2:
        print("사용법:")
        print("  로컬 파일: python analyze_image.py <이미지_경로>")
        print("  URL:       python analyze_image.py <이미지_URL>")
        print("예시: python analyze_image.py photo.png")
        print("예시: python analyze_image.py https://example.com/image.jpg")
        sys.exit(1)

    target = sys.argv[1]

    print(f"이미지 분석 중: {target}")
    print("-" * 50)

    if target.startswith("http://") or target.startswith("https://"):
        result = analyze_image_url(target)
    else:
        if not os.path.exists(target):
            print(f"오류: 파일을 찾을 수 없습니다 - {target}")
            sys.exit(1)
        result = analyze_image_file(target)

    print(result)


if __name__ == "__main__":
    main()
