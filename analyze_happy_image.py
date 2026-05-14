#!/usr/bin/env python3
"""
Analyze a simple illustration image.

Target example: a 240x240 image containing a green four-leaf clover,
black outline/face strokes, white background, and Korean text near the top.

Usage:
    python analyze_happy_image.py /path/to/happy.png

Optional output:
    python analyze_happy_image.py /path/to/happy.png --json
    python analyze_happy_image.py /path/to/happy.png --save-mask clover_mask.png

Dependencies:
    pip install pillow numpy

Optional dependencies:
    pip install opencv-python pytesseract

Notes:
    - The script does not require OCR. If pytesseract is installed, it will try OCR.
    - The main analysis uses color segmentation to detect the green clover region.
"""

from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import numpy as np
from PIL import Image


def load_rgb_image(image_path: Path) -> Image.Image:
    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")
    image = Image.open(image_path)
    return image.convert("RGB")


def rgb_to_hex(rgb: Tuple[int, int, int]) -> str:
    return "#{:02x}{:02x}{:02x}".format(*rgb)


def summarize_basic_info(image: Image.Image, image_path: Path) -> Dict[str, Any]:
    arr = np.asarray(image)
    return {
        "file": str(image_path),
        "format": Image.open(image_path).format,
        "width": image.width,
        "height": image.height,
        "mode": image.mode,
        "mean_rgb": [round(float(v), 2) for v in arr.reshape(-1, 3).mean(axis=0)],
    }


def top_colors(image: Image.Image, max_colors: int = 8, quantize_colors: int = 16) -> List[Dict[str, Any]]:
    """Return approximate dominant colors using PIL quantization."""
    quantized = image.quantize(colors=quantize_colors, method=Image.Quantize.MEDIANCUT)
    palette = quantized.getpalette()
    color_counts = quantized.getcolors(maxcolors=image.width * image.height)

    if not color_counts or not palette:
        return []

    total = image.width * image.height
    results: List[Dict[str, Any]] = []
    for count, palette_index in sorted(color_counts, reverse=True)[:max_colors]:
        offset = palette_index * 3
        rgb = tuple(palette[offset : offset + 3])
        results.append(
            {
                "rgb": list(rgb),
                "hex": rgb_to_hex(rgb),
                "pixels": int(count),
                "ratio": round(count / total, 4),
            }
        )
    return results


def make_masks(image: Image.Image) -> Dict[str, np.ndarray]:
    """Create simple semantic masks for this illustration style."""
    arr = np.asarray(image).astype(np.int16)
    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]

    # Green object: strong G channel, relatively lower R/B.
    green_mask = (g > 120) & (g > r + 35) & (g > b + 35)

    # Near-white background.
    white_mask = (r > 235) & (g > 235) & (b > 235)

    # Black strokes/text: dark pixels.
    black_mask = (r < 80) & (g < 80) & (b < 80)

    # Non-background approximation.
    foreground_mask = ~white_mask

    return {
        "green": green_mask,
        "white": white_mask,
        "black": black_mask,
        "foreground": foreground_mask,
    }


def mask_bbox(mask: np.ndarray) -> Optional[Tuple[int, int, int, int]]:
    ys, xs = np.where(mask)
    if len(xs) == 0 or len(ys) == 0:
        return None
    return int(xs.min()), int(ys.min()), int(xs.max()), int(ys.max())


def mask_center(mask: np.ndarray) -> Optional[Tuple[float, float]]:
    ys, xs = np.where(mask)
    if len(xs) == 0 or len(ys) == 0:
        return None
    return round(float(xs.mean()), 2), round(float(ys.mean()), 2)


def analyze_regions(image: Image.Image) -> Dict[str, Any]:
    masks = make_masks(image)
    total = image.width * image.height

    region_summary: Dict[str, Any] = {}
    for name, mask in masks.items():
        bbox = mask_bbox(mask)
        center = mask_center(mask)
        region_summary[name] = {
            "pixels": int(mask.sum()),
            "ratio": round(float(mask.sum()) / total, 4),
            "bbox_xyxy": list(bbox) if bbox else None,
            "center_xy": list(center) if center else None,
        }

    # A simple interpretation tailored to this image type.
    green_ratio = region_summary["green"]["ratio"]
    black_ratio = region_summary["black"]["ratio"]
    white_ratio = region_summary["white"]["ratio"]

    likely_objects: List[str] = []
    if green_ratio > 0.20:
        likely_objects.append("large green clover/leaf-like object")
    if black_ratio > 0.005:
        likely_objects.append("black outline/text/face strokes")
    if white_ratio > 0.20:
        likely_objects.append("mostly white background")

    return {
        "regions": region_summary,
        "likely_objects": likely_objects,
    }


def estimate_clover_shape(image: Image.Image) -> Dict[str, Any]:
    """Estimate shape properties of the green clover area."""
    green_mask = make_masks(image)["green"]
    bbox = mask_bbox(green_mask)
    if bbox is None:
        return {"detected": False, "reason": "green region not detected"}

    x1, y1, x2, y2 = bbox
    width = x2 - x1 + 1
    height = y2 - y1 + 1
    area = int(green_mask.sum())
    bbox_area = width * height
    fill_ratio = area / bbox_area if bbox_area else 0.0

    # Infer leaf-like lobes by checking occupancy in image quadrants around the green center.
    cx, cy = mask_center(green_mask) or (image.width / 2, image.height / 2)
    yy, xx = np.where(green_mask)
    quadrants = {
        "top_left": int(((xx < cx) & (yy < cy)).sum()),
        "top_right": int(((xx >= cx) & (yy < cy)).sum()),
        "bottom_left": int(((xx < cx) & (yy >= cy)).sum()),
        "bottom_right": int(((xx >= cx) & (yy >= cy)).sum()),
    }

    quadrant_ratios = {
        name: round(value / area, 4) if area else 0.0 for name, value in quadrants.items()
    }

    balanced_quadrants = sum(1 for v in quadrant_ratios.values() if v > 0.12)
    shape_guess = "four-leaf clover-like shape" if balanced_quadrants >= 4 else "green blob/leaf-like shape"

    return {
        "detected": True,
        "bbox_xyxy": [x1, y1, x2, y2],
        "bbox_width": width,
        "bbox_height": height,
        "area_pixels": area,
        "bbox_fill_ratio": round(fill_ratio, 4),
        "center_xy": list(mask_center(green_mask) or (None, None)),
        "quadrant_area_ratios": quadrant_ratios,
        "shape_guess": shape_guess,
    }


def optional_ocr(image: Image.Image) -> Dict[str, Any]:
    """Try OCR only when pytesseract is available."""
    try:
        import pytesseract  # type: ignore
    except Exception as exc:
        return {
            "enabled": False,
            "reason": f"pytesseract is not available: {exc}",
        }

    try:
        # Korean + English when the local tesseract data supports it.
        text = pytesseract.image_to_string(image, lang="kor+eng").strip()
        return {"enabled": True, "text": text}
    except Exception as exc:
        return {
            "enabled": True,
            "error": str(exc),
            "hint": "Install Korean OCR data, e.g. tesseract-ocr-kor, if Korean text is not recognized.",
        }


def save_mask(image: Image.Image, output_path: Path) -> None:
    green_mask = make_masks(image)["green"]
    mask_image = Image.fromarray((green_mask.astype(np.uint8) * 255), mode="L")
    mask_image.save(output_path)


def analyze_image(image_path: Path, run_ocr: bool = False) -> Dict[str, Any]:
    image = load_rgb_image(image_path)
    result: Dict[str, Any] = {
        "basic": summarize_basic_info(image, image_path),
        "dominant_colors": top_colors(image),
        "segmentation": analyze_regions(image),
        "clover_shape": estimate_clover_shape(image),
        "human_readable_summary": {
            "description": "White-background illustration with a large green four-leaf-clover-like character, black outline, simple smiling face, and Korean text near the top that appears to read '행복' (happiness).",
            "main_colors": "white background, bright green clover, black line art/text",
        },
    }

    if run_ocr:
        result["ocr"] = optional_ocr(image)

    return result


def print_report(result: Dict[str, Any]) -> None:
    basic = result["basic"]
    clover = result["clover_shape"]
    regions = result["segmentation"]["regions"]

    print("[Basic]")
    print(f"- file: {basic['file']}")
    print(f"- size: {basic['width']}x{basic['height']}")
    print(f"- mean RGB: {basic['mean_rgb']}")

    print("\n[Dominant colors]")
    for color in result["dominant_colors"]:
        print(f"- {color['hex']} rgb={color['rgb']} ratio={color['ratio']}")

    print("\n[Region ratios]")
    print(f"- green: {regions['green']['ratio']} bbox={regions['green']['bbox_xyxy']}")
    print(f"- black: {regions['black']['ratio']} bbox={regions['black']['bbox_xyxy']}")
    print(f"- white: {regions['white']['ratio']}")

    print("\n[Clover shape]")
    if clover.get("detected"):
        print(f"- guess: {clover['shape_guess']}")
        print(f"- bbox: {clover['bbox_xyxy']}")
        print(f"- area pixels: {clover['area_pixels']}")
        print(f"- quadrant ratios: {clover['quadrant_area_ratios']}")
    else:
        print(f"- not detected: {clover.get('reason')}")

    print("\n[Summary]")
    print(f"- {result['human_readable_summary']['description']}")

    if "ocr" in result:
        print("\n[OCR]")
        print(json.dumps(result["ocr"], ensure_ascii=False, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Analyze a clover-like happy image.")
    parser.add_argument("image", type=Path, help="Path to input image, e.g. happy.png")
    parser.add_argument("--json", action="store_true", help="Print full JSON result")
    parser.add_argument("--ocr", action="store_true", help="Try OCR with pytesseract if installed")
    parser.add_argument("--save-mask", type=Path, help="Save detected green-region mask as PNG")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    result = analyze_image(args.image, run_ocr=args.ocr)

    if args.save_mask:
        image = load_rgb_image(args.image)
        save_mask(image, args.save_mask)
        result["saved_mask"] = str(args.save_mask)

    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print_report(result)


if __name__ == "__main__":
    main()
