import anthropic
import base64
import sys
from pathlib import Path


def analyze_image(image_path: str) -> str:
    """
    이미지를 분석하고 설명을 반환합니다.

    Args:
        image_path: 분석할 이미지 파일 경로

    Returns:
        이미지 분석 결과 텍스트
    """
    client = anthropic.Anthropic()

    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    # 파일 확장자로 미디어 타입 결정
    ext = path.suffix.lower()
    media_type_map = {
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    media_type = media_type_map.get(ext)
    if not media_type:
        raise ValueError(f"지원하지 않는 이미지 형식입니다: {ext}")

    # 이미지를 base64로 인코딩
    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    # Claude API로 이미지 분석 요청
    response = client.messages.create(
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
                        "text": "이 이미지를 자세히 분석해주세요. 이미지에 무엇이 있는지, 색상, 구도, 분위기 등을 설명해주세요.",
                    },
                ],
            }
        ],
    )

    return response.content[0].text


def main():
    if len(sys.argv) < 2:
        print("사용법: python analyze_image.py <이미지 파일 경로>")
        print("예시: python analyze_image.py photo.jpg")
        sys.exit(1)

    image_path = sys.argv[1]

    print(f"이미지 분석 중: {image_path}")
    print("-" * 50)

    result = analyze_image(image_path)
    print(result)


if __name__ == "__main__":
    main()
