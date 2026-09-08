import pandas as pd
import time
from dataclasses import dataclass


# ----------------------------------------------------------------------
# RULE BASE — CPCB breakpoints. Units: ug/m3 for all, EXCEPT CO (mg/m3).
# Format: (C_low, C_high, I_low, I_high)
# ----------------------------------------------------------------------
CPCB_BREAKPOINTS = {
    "pm2_5": [
        (0, 30, 0, 50), (31, 60, 51, 100), (61, 90, 101, 200),
        (91, 120, 201, 300), (121, 250, 301, 400), (251, 380, 401, 500),
    ],
    "pm10": [
        (0, 50, 0, 50), (51, 100, 51, 100), (101, 250, 101, 200),
        (251, 350, 201, 300), (351, 430, 301, 400), (431, 510, 401, 500),
    ],
    "so2": [
        (0, 40, 0, 50), (41, 80, 51, 100), (81, 380, 101, 200),
        (381, 800, 201, 300), (801, 1600, 301, 400), (1601, 2100, 401, 500),
    ],
    "no2": [
        (0, 40, 0, 50), (41, 80, 51, 100), (81, 180, 101, 200),
        (181, 280, 201, 300), (281, 400, 301, 400), (401, 500, 401, 500),
    ],
    "co": [  # mg/m3
        (0.0, 1.0, 0, 50), (1.1, 2.0, 51, 100), (2.1, 10, 101, 200),
        (10.1, 17, 201, 300), (17.1, 34, 301, 400), (34.1, 50, 401, 500),
    ],
    "o3": [
        (0, 50, 0, 50), (51, 100, 51, 100), (101, 168, 101, 200),
        (169, 208, 201, 300), (209, 748, 301, 400),
    ],
}

CPCB_CATEGORIES = [
    (0, 50, "Good"),
    (51, 100, "Satisfactory"),
    (101, 200, "Moderate"),
    (201, 300, "Poor"),
    (301, 400, "Very Poor"),
    (401, 500, "Severe"),
]


def sub_index(conc, table):
    if conc is None or pd.isna(conc):
        return None
    conc = max(conc, 0)
    for c_lo, c_hi, i_lo, i_hi in table:
        if c_lo <= conc <= c_hi:
            return ((i_hi - i_lo) / (c_hi - c_lo)) * (conc - c_lo) + i_lo
    c_lo, c_hi, i_lo, i_hi = table[-1]
    return float(i_hi) if conc > c_hi else None


def categorize(aqi):
    for lo, hi, label in CPCB_CATEGORIES:
        if lo <= aqi <= hi:
            return label
    return "Severe" if aqi > 500 else "Unknown"


@dataclass
class AQIReading:
    aqi: float
    category: str
    dominant_pollutant: str
    sub_indices: dict


def simple_reflex_agent(percept: dict) -> AQIReading:
    """Condition-action mapping. Uses ONLY the current percept — no memory."""
    values = {
        "pm2_5": percept.get("pm2_5"),
        "pm10": percept.get("pm10"),
        "co": _safe_div(percept.get("carbon_monoxide"), 1000),   # ug/m3 -> mg/m3
        "so2": percept.get("sulphur_dioxide"),
        "no2": percept.get("nitrogen_dioxide"),
        "o3": percept.get("ozone"),
    }

    sub_indices = {}
    for pollutant, value in values.items():
        idx = sub_index(value, CPCB_BREAKPOINTS[pollutant])
        if idx is not None:
            sub_indices[pollutant] = round(idx, 1)

    if not sub_indices:
        return AQIReading(float("nan"), "No Data", "none", {})

    dominant = max(sub_indices, key=sub_indices.get)
    final_aqi = sub_indices[dominant]
    return AQIReading(round(final_aqi, 1), categorize(final_aqi), dominant, sub_indices)


def _safe_div(value, factor):
    return None if value is None or pd.isna(value) else value / factor


# ----------------------------------------------------------------------
# "Live" feed — right now this streams your CSV (stand-in for a sensor).
# Swap get_latest_reading() with a real API/sensor call later; the agent
# function above never has to change.
# ----------------------------------------------------------------------
def latest_hyderabad_reading(csv_path: str) -> dict:
    df = pd.read_csv(csv_path)
    df = df.dropna(subset=["pm2_5", "pm10"])
    latest_row = df.iloc[-1]
    return latest_row.to_dict()


def live_stream(csv_path: str, delay_seconds: float = 2.0, limit: int = 10):
    df = pd.read_csv(csv_path).dropna(subset=["pm2_5", "pm10"])
    for _, row in df.tail(limit).iterrows():
        percept = row.to_dict()
        result = simple_reflex_agent(percept)
        print(f"[{percept.get('date')}] Hyderabad AQI = {result.aqi} "
              f"-> {result.category}  (worst pollutant: {result.dominant_pollutant})")
        time.sleep(delay_seconds)


if __name__ == "__main__":
    CSV_PATH = "air_quality_historical.csv"

    print("=== Hyderabad AQI right now (most recent reading in dataset) ===")
    latest = latest_hyderabad_reading(CSV_PATH)
    result = simple_reflex_agent(latest)
    print(f"Date        : {latest.get('date')}")
    print(f"AQI value   : {result.aqi}")
    print(f"Category    : {result.category}")
    print(f"Worst pollutant driving this AQI: {result.dominant_pollutant}")
    print(f"All sub-indices: {result.sub_indices}")

    print("\n=== Simulated live feed (last 10 days, one 'reading' every 2s) ===")
    live_stream(CSV_PATH, delay_seconds=0, limit=10)
