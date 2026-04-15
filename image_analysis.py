import anthropic
import base64
import sys
import mimetypes
from pathlib import Path


def analyze_image(image_path: str, prompt: str = "이 이미지를 자세히 분석해줘.") -> str:
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"이미지 파일을 찾을 수 없습니다: {image_path}")

    mime_type, _ = mimetypes.guess_type(image_path)
    supported = {"image/jpeg", "image/png", "image/gif", "image/webp"}
    if mime_type not in supported:
        raise ValueError(f"지원하지 않는 이미지 형식입니다: {mime_type}. 지원 형식: JPEG, PNG, GIF, WEBP")

    with open(image_path, "rb") as f:
        image_data = base64.standard_b64encode(f.read()).decode("utf-8")

    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "image",
                        "source": {
                            "type": "base64",
                            "media_type": mime_type,
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
    )

    return message.content[0].text


def main():
    if len(sys.argv) < 2:
        print("사용법: python image_analysis.py <이미지경로> [분석요청(선택)]")
        print("예시:  python image_analysis.py photo.jpg '이 이미지에서 텍스트를 추출해줘'")
        sys.exit(1)

    image_path = sys.argv[1]
    prompt = sys.argv[2] if len(sys.argv) > 2 else "이 이미지를 자세히 분석해줘."

    print(f"이미지 분석 중: {image_path}")
    print(f"요청: {prompt}\n")

    result = analyze_image(image_path, prompt)
    print("=== 분석 결과 ===")
    print(result)


if __name__ == "__main__":
    main()
