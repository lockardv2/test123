"""
이미지 파일 분석 스크립트
사용법: python analyze_image.py <이미지 파일 경로>
"""

import sys
from pathlib import Path

try:
    from PIL import Image, ImageStat
    import PIL.ExifTags
except ImportError:
    print("Pillow 라이브러리가 필요합니다: pip install Pillow")
    sys.exit(1)


def analyze_image(file_path: str) -> None:
    path = Path(file_path)

    if not path.exists():
        print(f"파일을 찾을 수 없습니다: {file_path}")
        sys.exit(1)

    print(f"=== 이미지 분석 결과: {path.name} ===\n")

    with Image.open(path) as img:
        # 기본 정보
        print(f"파일 크기  : {path.stat().st_size:,} bytes")
        print(f"형식       : {img.format}")
        print(f"모드       : {img.mode}  (예: RGB, RGBA, L ...)")
        print(f"해상도     : {img.width} x {img.height} px")

        # 색상 통계 (ImageStat 사용 — deprecation 경고 없음)
        if img.mode in ("RGB", "RGBA"):
            stat = ImageStat.Stat(img.convert("RGB"))
            avg_r, avg_g, avg_b = stat.mean
            print(f"\n평균 색상  : R={avg_r:.1f}, G={avg_g:.1f}, B={avg_b:.1f}")

        # 투명도 여부 (RGBA)
        if img.mode == "RGBA":
            alpha_stat = ImageStat.Stat(img.split()[3])  # 알파 채널
            avg_alpha = alpha_stat.mean[0]
            transparent_ratio = (1 - avg_alpha / 255) * 100
            print(f"투명 픽셀  : ~{transparent_ratio:.1f}% (평균 알파={avg_alpha:.1f})")

        # 주요 색상 상위 5개
        num_colors = min(5, img.width * img.height)
        print(f"\n[주요 색상 Top {num_colors}]")
        quantized = img.convert("RGB").quantize(colors=num_colors)
        palette = quantized.getpalette()
        num_entries = len(palette) // 3
        for i in range(min(num_colors, num_entries)):
            r, g, b = palette[i * 3], palette[i * 3 + 1], palette[i * 3 + 2]
            print(f"  #{i+1}  RGB({r:3d}, {g:3d}, {b:3d})  #{r:02X}{g:02X}{b:02X}")

        # EXIF 메타데이터
        exif_data = img._getexif() if hasattr(img, "_getexif") else None
        if exif_data:
            print("\n[EXIF 메타데이터]")
            for tag_id, value in exif_data.items():
                tag = PIL.ExifTags.TAGS.get(tag_id, tag_id)
                print(f"  {tag}: {value}")
        else:
            print("\nEXIF 메타데이터 없음")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("사용법: python analyze_image.py <이미지 파일 경로>")
        print("예시 : python analyze_image.py photo.png")
        sys.exit(1)

    analyze_image(sys.argv[1])
