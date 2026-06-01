"""
Data loading utilities for the Indego Philadelphia Bike Share analysis.
Downloads trip data from Indego and weather data from Open-Meteo.
"""

import io
import zipfile
import requests
import pandas as pd
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent / "data"
WEATHER_API = "https://archive-api.open-meteo.com/v1/archive"

# Philadelphia coordinates
PHL_LAT = 39.9526
PHL_LON = -75.1652

# Hardcoded URL map: (year, quarter) → upload path.
# Indego publishes files at /wp-content/uploads/YYYY/MM/indego-trips-YYYY-qQ.zip
# The upload month varies, so we maintain an explicit table rather than guessing.
INDEGO_URLS = {
    (2022, 1): "2022/04/indego-trips-2022-q1.zip",
    (2022, 2): "2022/07/indego-trips-2022-q2.zip",
    (2022, 3): "2022/12/indego-trips-2022-q3.zip",
    (2022, 4): "2023/01/indego-trips-2022-q4.zip",
    (2023, 1): "2023/04/indego-trips-2023-q1.zip",
    (2023, 2): "2023/07/indego-trips-2023-q2.zip",
    (2023, 3): "2023/10/indego-trips-2023-q3.zip",
    (2023, 4): "2024/01/indego-trips-2023-q4.zip",
    (2024, 1): "2024/04/indego-trips-2024-q1.zip",
    (2024, 2): "2024/07/indego-trips-2024-q2.zip",
    (2024, 3): "2024/10/indego-trips-2024-q3.zip",
    (2024, 4): "2025/01/indego-trips-2024-q4.zip",
    (2025, 1): "2025/04/indego-trips-2025-q1.zip",
    (2025, 2): "2025/07/indego-trips-2025-q2.zip",
    (2025, 3): "2025/10/indego-trips-2025-q3.zip",
    (2025, 4): "2026/01/indego-trips-2025-q4.zip",
}

INDEGO_BASE = "https://www.rideindego.com/wp-content/uploads"
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; IndegoBikeAnalysis/1.0)"}


def download_indego_quarter(year: int, quarter: int, force: bool = False) -> Path:
    """Download and extract one quarter of Indego trip data."""
    key = (year, quarter)
    if key not in INDEGO_URLS:
        raise ValueError(f"No URL configured for {year} Q{quarter}. Update INDEGO_URLS in data_loader.py.")

    filename = f"indego-trips-{year}-q{quarter}.csv"
    dest = DATA_DIR / filename
    if dest.exists() and not force:
        print(f"  {filename} already exists, skipping.")
        return dest

    url = f"{INDEGO_BASE}/{INDEGO_URLS[key]}"
    print(f"Downloading {year} Q{quarter} from {url} ...")
    r = requests.get(url, headers=HEADERS, timeout=120)
    r.raise_for_status()

    with zipfile.ZipFile(io.BytesIO(r.content)) as z:
        csv_names = [n for n in z.namelist() if n.endswith(".csv")]
        if not csv_names:
            raise ValueError(f"No CSV found in zip for {year} Q{quarter}")
        with z.open(csv_names[0]) as src, open(dest, "wb") as dst:
            dst.write(src.read())

    print(f"  Saved: {dest}")
    return dest


def download_all(start_year: int = 2022, end_year: int = 2025) -> None:
    """Download all configured quarters for the given year range."""
    DATA_DIR.mkdir(exist_ok=True)
    for year in range(start_year, end_year + 1):
        for quarter in range(1, 5):
            if (year, quarter) not in INDEGO_URLS:
                continue
            try:
                download_indego_quarter(year, quarter)
            except requests.HTTPError as e:
                print(f"  Skipping {year} Q{quarter}: {e}")


def load_trips(start_year: int = 2022, end_year: int = 2025) -> pd.DataFrame:
    """Load all downloaded quarterly CSVs into a single cleaned DataFrame."""
    frames = []
    for path in sorted(DATA_DIR.glob("indego-trips-*.csv")):
        year = int(path.stem.split("-")[2])
        if start_year <= year <= end_year:
            frames.append(pd.read_csv(path, low_memory=False))

    if not frames:
        raise FileNotFoundError(
            "No Indego CSV files found in data/.\n"
            "Run:  python src/data_loader.py\n"
            "Or see data/README.md for manual download instructions."
        )

    df = pd.concat(frames, ignore_index=True)

    # Normalise column names
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

    # Parse timestamps
    for col in ("start_time", "end_time"):
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")

    # Enforce Indego's own policy: trips > 1 min and ≤ 24 hours
    df = df[df["duration"].between(1, 1440)].copy()

    return df


def fetch_weather(start_date: str = "2022-01-01", end_date: str = "2025-12-31") -> pd.DataFrame:
    """
    Fetch daily weather for Philadelphia from Open-Meteo (free, no API key).
    Returns one row per day.
    """
    params = {
        "latitude": PHL_LAT,
        "longitude": PHL_LON,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join([
            "temperature_2m_mean",
            "temperature_2m_max",
            "temperature_2m_min",
            "precipitation_sum",
            "windspeed_10m_max",
            "relative_humidity_2m_mean",
            "uv_index_max",
        ]),
        "timezone": "America/New_York",
        "temperature_unit": "fahrenheit",
        "windspeed_unit": "mph",
        "precipitation_unit": "inch",
    }
    r = requests.get(WEATHER_API, params=params, timeout=60)
    r.raise_for_status()
    daily = r.json()["daily"]
    df = pd.DataFrame(daily)
    df.rename(columns={"time": "date"}, inplace=True)
    df["date"] = pd.to_datetime(df["date"])
    return df


STATIONS_JSON = "https://www.rideindego.com/stations/json/"
STATIONS_CACHE = DATA_DIR / "indego_stations.csv"


def load_station_names(force: bool = False) -> dict:
    """Return a {station_id: station_name} mapping from Indego's live station feed.

    Cached to data/indego_stations.csv so the notebooks work offline after the
    first fetch. The feed's ``kioskId`` matches the station numbers in the trip
    data (e.g. 3020 -> "University City Station").
    """
    if STATIONS_CACHE.exists() and not force:
        cached = pd.read_csv(STATIONS_CACHE)
        return dict(zip(cached["station_id"], cached["name"]))

    r = requests.get(STATIONS_JSON, headers=HEADERS, timeout=30)
    r.raise_for_status()
    rows = [
        {"station_id": f["properties"]["kioskId"], "name": f["properties"]["name"]}
        for f in r.json()["features"]
        if f.get("properties", {}).get("kioskId") is not None
    ]
    stations = pd.DataFrame(rows).drop_duplicates("station_id")
    DATA_DIR.mkdir(exist_ok=True)
    stations.to_csv(STATIONS_CACHE, index=False)
    return dict(zip(stations["station_id"], stations["name"]))


if __name__ == "__main__":
    print("Downloading Indego trip data (2022–2025)...")
    download_all(2022, 2025)
    print("\nDone. Run the notebooks to start the analysis.")
