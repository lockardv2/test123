#!/usr/bin/env python3
"""Analyze today's weather in Seoul, South Korea.

The script fetches current-day observations/forecast values from the free
Open-Meteo API, summarizes comfort and risk factors, and prints either a
human-readable Korean report or JSON.

Usage:
    python seoul_weather_analysis.py
    python seoul_weather_analysis.py --json
    python seoul_weather_analysis.py --date 2026-06-16

No third-party Python packages are required.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass, asdict
from datetime import date, datetime
from typing import Any

SEOUL_LATITUDE = 37.5665
SEOUL_LONGITUDE = 126.9780
SEOUL_TIMEZONE = "Asia/Seoul"
OPEN_METEO_URL = "https://api.open-meteo.com/v1/forecast"

WEATHER_CODE_KO = {
    0: "맑음",
    1: "대체로 맑음",
    2: "부분적으로 흐림",
    3: "흐림",
    45: "안개",
    48: "서리 안개",
    51: "약한 이슬비",
    53: "이슬비",
    55: "강한 이슬비",
    61: "약한 비",
    63: "비",
    65: "강한 비",
    71: "약한 눈",
    73: "눈",
    75: "강한 눈",
    80: "약한 소나기",
    81: "소나기",
    82: "강한 소나기",
    95: "뇌우",
    96: "우박 동반 뇌우",
    99: "강한 우박 동반 뇌우",
}


@dataclass(frozen=True)
class WeatherAnalysis:
    location: str
    date: str
    condition: str
    min_temperature_c: float
    max_temperature_c: float
    average_temperature_c: float
    total_precipitation_mm: float
    max_precipitation_probability_percent: int
    max_wind_speed_kmh: float
    comfort_level: str
    rain_risk: str
    wind_risk: str
    recommendation: str


def fetch_weather(target_date: date) -> dict[str, Any]:
    """Fetch Seoul weather data for the requested date from Open-Meteo."""
    query = {
        "latitude": SEOUL_LATITUDE,
        "longitude": SEOUL_LONGITUDE,
        "timezone": SEOUL_TIMEZONE,
        "start_date": target_date.isoformat(),
        "end_date": target_date.isoformat(),
        "daily": "weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max",
        "hourly": "temperature_2m",
    }
    url = f"{OPEN_METEO_URL}?{urllib.parse.urlencode(query)}"
    with urllib.request.urlopen(url, timeout=10) as response:
        if response.status != 200:
            raise RuntimeError(f"Open-Meteo API returned HTTP {response.status}")
        return json.loads(response.read().decode("utf-8"))


def _first(daily: dict[str, list[Any]], key: str) -> Any:
    values = daily.get(key) or []
    if not values:
        raise ValueError(f"Missing daily weather value: {key}")
    return values[0]


def classify_comfort(avg_temp: float, max_temp: float, precipitation_mm: float) -> str:
    if max_temp >= 33:
        return "매우 더움"
    if avg_temp >= 27:
        return "더움"
    if precipitation_mm >= 10:
        return "습하고 비가 많음"
    if 18 <= avg_temp <= 24:
        return "쾌적함"
    if avg_temp < 5:
        return "추움"
    return "보통"


def classify_rain(probability: int, precipitation_mm: float) -> str:
    if precipitation_mm >= 20 or probability >= 80:
        return "높음"
    if precipitation_mm >= 3 or probability >= 50:
        return "보통"
    return "낮음"


def classify_wind(max_wind_kmh: float) -> str:
    if max_wind_kmh >= 45:
        return "강풍 주의"
    if max_wind_kmh >= 25:
        return "다소 강함"
    return "약함"


def build_recommendation(comfort: str, rain_risk: str, wind_risk: str) -> str:
    tips: list[str] = []
    if comfort in {"매우 더움", "더움"}:
        tips.append("수분을 자주 섭취하고 한낮 야외 활동을 줄이세요")
    elif comfort == "추움":
        tips.append("보온이 되는 겉옷을 준비하세요")
    elif comfort == "쾌적함":
        tips.append("야외 활동하기 비교적 좋은 날씨입니다")
    else:
        tips.append("일반적인 외출 준비면 충분합니다")

    if rain_risk in {"높음", "보통"}:
        tips.append("우산이나 방수 신발을 준비하세요")
    if wind_risk != "약함":
        tips.append("가벼운 물건이 날리지 않도록 주의하세요")
    return "; ".join(tips) + "."


def analyze_weather(data: dict[str, Any], target_date: date) -> WeatherAnalysis:
    daily = data.get("daily") or {}
    hourly = data.get("hourly") or {}
    hourly_temps = [float(value) for value in hourly.get("temperature_2m", []) if value is not None]

    min_temp = float(_first(daily, "temperature_2m_min"))
    max_temp = float(_first(daily, "temperature_2m_max"))
    avg_temp = round(statistics.fmean(hourly_temps), 1) if hourly_temps else round((min_temp + max_temp) / 2, 1)
    precipitation = float(_first(daily, "precipitation_sum"))
    rain_probability = int(_first(daily, "precipitation_probability_max"))
    max_wind = float(_first(daily, "wind_speed_10m_max"))
    weather_code = int(_first(daily, "weather_code"))

    comfort = classify_comfort(avg_temp, max_temp, precipitation)
    rain_risk = classify_rain(rain_probability, precipitation)
    wind_risk = classify_wind(max_wind)

    return WeatherAnalysis(
        location="서울",
        date=target_date.isoformat(),
        condition=WEATHER_CODE_KO.get(weather_code, f"알 수 없음({weather_code})"),
        min_temperature_c=min_temp,
        max_temperature_c=max_temp,
        average_temperature_c=avg_temp,
        total_precipitation_mm=precipitation,
        max_precipitation_probability_percent=rain_probability,
        max_wind_speed_kmh=max_wind,
        comfort_level=comfort,
        rain_risk=rain_risk,
        wind_risk=wind_risk,
        recommendation=build_recommendation(comfort, rain_risk, wind_risk),
    )


def format_korean_report(analysis: WeatherAnalysis) -> str:
    return "\n".join(
        [
            f"서울 날씨 분석 ({analysis.date})",
            "=" * 28,
            f"날씨: {analysis.condition}",
            f"기온: {analysis.min_temperature_c:.1f}°C ~ {analysis.max_temperature_c:.1f}°C (평균 {analysis.average_temperature_c:.1f}°C)",
            f"강수량/확률: {analysis.total_precipitation_mm:.1f}mm / 최대 {analysis.max_precipitation_probability_percent}%",
            f"최대 풍속: {analysis.max_wind_speed_kmh:.1f}km/h",
            f"체감 분류: {analysis.comfort_level}",
            f"비 위험도: {analysis.rain_risk}",
            f"바람 위험도: {analysis.wind_risk}",
            f"추천: {analysis.recommendation}",
        ]
    )


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="오늘 서울 날씨를 가져와 분석합니다.")
    parser.add_argument("--date", default=date.today().isoformat(), help="분석 날짜(YYYY-MM-DD). 기본값: 오늘")
    parser.add_argument("--json", action="store_true", help="분석 결과를 JSON으로 출력")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
        analysis = analyze_weather(fetch_weather(target_date), target_date)
    except Exception as exc:  # user-facing CLI error handling
        print(f"날씨 데이터를 분석하지 못했습니다: {exc}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(asdict(analysis), ensure_ascii=False, indent=2))
    else:
        print(format_korean_report(analysis))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
