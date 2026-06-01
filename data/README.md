# Data

CSV files are not committed to this repo (too large). Follow the steps below to download them before running the notebooks.

## 1. Indego Trip Data (2022–2025)

Download the quarterly zip files from https://www.rideindego.com/about/data/ and extract them into this `data/` folder.

Files needed:
```
indego-trips-2022-q1.zip  →  extract to data/
indego-trips-2022-q2.zip  →  extract to data/
indego-trips-2022-q3.zip  →  extract to data/
indego-trips-2022-q4.zip  →  extract to data/
indego-trips-2023-q1.zip  →  extract to data/
indego-trips-2023-q2.zip  →  extract to data/
indego-trips-2023-q3.zip  →  extract to data/
indego-trips-2023-q4.zip  →  extract to data/
indego-trips-2024-q1.zip  →  extract to data/
indego-trips-2024-q2.zip  →  extract to data/
indego-trips-2024-q3.zip  →  extract to data/
indego-trips-2024-q4.zip  →  extract to data/
indego-trips-2025-q1.zip  →  extract to data/
indego-trips-2025-q2.zip  →  extract to data/
indego-trips-2025-q3.zip  →  extract to data/
indego-trips-2025-q4.zip  →  extract to data/
```

Or run the download script from the repo root:
```bash
python src/data_loader.py
```

## 2. Weather Data

Weather is fetched automatically from the Open-Meteo API (free, no key required) when you run the notebooks. No download needed.

## 3. Station Metadata

Station locations are fetched automatically from the OpenDataPhilly API when you run the notebooks.
