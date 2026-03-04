"""
이미지 분석 스크립트
- 이미지 기본 정보 분석
- 색상 분석
- 밝기 분석
- 히스토그램 생성
"""

import sys
from PIL import Image
import numpy as np
from collections import Counter


def analyze_image(image_path):
    """이미지를 분석하고 결과를 출력합니다."""

    try:
        # 이미지 열기
        img = Image.open(image_path)
        print("=" * 50)
        print("📷 이미지 분석 결과")
        print("=" * 50)

        # 기본 정보
        print("\n📋 기본 정보:")
        print(f"  - 파일 경로: {image_path}")
        print(f"  - 포맷: {img.format}")
        print(f"  - 모드: {img.mode}")
        print(f"  - 크기: {img.width} x {img.height} 픽셀")
        print(f"  - 총 픽셀 수: {img.width * img.height:,}")

        # EXIF 정보 (있는 경우)
        if hasattr(img, '_getexif') and img._getexif():
            print("\n📸 EXIF 정보 발견됨")

        # RGB로 변환하여 색상 분석
        if img.mode != 'RGB':
            img_rgb = img.convert('RGB')
        else:
            img_rgb = img

        # numpy 배열로 변환
        img_array = np.array(img_rgb)

        # 색상 분석
        print("\n🎨 색상 분석:")
        avg_color = img_array.mean(axis=(0, 1))
        print(f"  - 평균 RGB: R={avg_color[0]:.1f}, G={avg_color[1]:.1f}, B={avg_color[2]:.1f}")

        # 밝기 분석
        brightness = np.mean(avg_color)
        print(f"  - 평균 밝기: {brightness:.1f}/255")
        if brightness < 85:
            print("  - 밝기 평가: 어두운 이미지")
        elif brightness < 170:
            print("  - 밝기 평가: 보통 밝기")
        else:
            print("  - 밝기 평가: 밝은 이미지")

        # 색상 대비 분석
        std_color = img_array.std(axis=(0, 1))
        print(f"  - 색상 표준편차: R={std_color[0]:.1f}, G={std_color[1]:.1f}, B={std_color[2]:.1f}")

        avg_std = np.mean(std_color)
        if avg_std < 30:
            print("  - 대비 평가: 낮은 대비 (단조로운 색상)")
        elif avg_std < 60:
            print("  - 대비 평가: 보통 대비")
        else:
            print("  - 대비 평가: 높은 대비 (다양한 색상)")

        # 주요 색상 찾기 (간단한 방식)
        print("\n🔝 주요 색상:")
        # 이미지를 작게 리사이즈하여 계산 효율화
        small_img = img_rgb.resize((100, 100))
        pixels = list(small_img.getdata())

        # 색상을 더 큰 범위로 그룹화 (32단위로)
        def round_color(color):
            return tuple((c // 32) * 32 for c in color)

        rounded_pixels = [round_color(p) for p in pixels]
        color_counts = Counter(rounded_pixels)
        top_colors = color_counts.most_common(5)

        for i, (color, count) in enumerate(top_colors, 1):
            percentage = (count / len(rounded_pixels)) * 100
            print(f"  {i}. RGB{color} - {percentage:.1f}%")

        # 이미지 특성 분석
        print("\n📊 이미지 특성:")

        # 가로/세로 비율
        aspect_ratio = img.width / img.height
        if aspect_ratio > 1.3:
            orientation = "가로형 (Landscape)"
        elif aspect_ratio < 0.77:
            orientation = "세로형 (Portrait)"
        else:
            orientation = "정사각형에 가까움"
        print(f"  - 비율: {aspect_ratio:.2f} ({orientation})")

        # 해상도 등급
        total_pixels = img.width * img.height
        if total_pixels >= 8000000:
            resolution = "고해상도 (8MP 이상)"
        elif total_pixels >= 2000000:
            resolution = "중간 해상도 (2-8MP)"
        else:
            resolution = "저해상도 (2MP 미만)"
        print(f"  - 해상도 등급: {resolution}")

        print("\n" + "=" * 50)
        print("✅ 분석 완료!")
        print("=" * 50)

        return True

    except FileNotFoundError:
        print(f"❌ 오류: 파일을 찾을 수 없습니다 - {image_path}")
        return False
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        return False


def main():
    if len(sys.argv) < 2:
        print("사용법: python image_analyzer.py <이미지_파일_경로>")
        print("예시: python image_analyzer.py photo.jpg")
        return

    image_path = sys.argv[1]
    analyze_image(image_path)


if __name__ == "__main__":
    main()
