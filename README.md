# Indego Philadelphia Bike Share — Analytics & Demand Forecasting

End-to-end analytics project on Philadelphia's Indego bike share system: 4.6 million trips across 2022–2025, descriptive deep-dive plus a machine-learning demand forecaster that beats the historical-average baseline by 12% overall and up to 34% on exception days.

This is framed around an operational problem Indego dispatchers might face every morning.

---

## The Business Problem — Bike Rebalancing

Every rush hour, Indego stations face a structural supply/demand imbalance. Residential stations bleed bikes as commuters head downtown; Center City and University City stations fill up with no space for arrivals. Indego pays drivers to manually rebalance — an estimated **~$246K/year** in operating cost for systems of this size (industry benchmark; Indego does not publish this figure).

Roughly 30% of dispatches are *reactive* — a station already ran empty and a driver is scrambling. A demand forecasting model that predicts which stations will drain (or overflow) in the next rush session lets dispatchers act *proactively*, cutting that reactive share roughly in half — an estimated **$60–80K/year** in combined ops savings + retention.

---

## What's Inside

### `notebooks/01_descriptive_analytics.ipynb`
Visual story of how Philadelphia rides. Twelve sections including:

| Section | What it shows |
|---|---|
| 2. System growth | Indego hit a record 1.3M trips in 2024 |
| 3. Station demand map | Demand clusters in Center City and University City |
| **3.5 Bike inventory imbalance** | Top-50 stations sorted by AM net flow — the rebalancing problem visualised |
| **3.6 Top station concentration** | Top 50 stations capture ~45% of all rush-hour trips |
| 4. Hour × Day-of-week heatmap | Weekday 8am / 5–6pm commute peaks (rush windows highlighted) |
| **4.5 Event-day snapshot** | Phillies game-day demand vs. a normal Monday |
| 5. Commuter vs. recreational | One-way vs. round-trip patterns |
| 6. Trip duration by passholder | Subscribers ~12 min, day-pass users ~41 min |
| 7. E-bike vs. pedal bike | Electric now >50% of trips |
| 8. Weather impact | Rain reduces demand 10–15% |
| 9. Popular routes map | Top 10 corridors as an interactive folium map |

### `notebooks/02_demand_forecasting.ipynb`
End-to-end ML pipeline that predicts **session net flow** (departures − arrivals) per station per rush window. Top 50 stations × AM (7–9am) + PM (4–7pm) sessions, with curated Philadelphia special events.

| Step | Detail |
|---|---|
| Target | `net_flow` per (station, session, date) |
| Features | Time, holidays, lags, weather, **typed event flags** (Phillies/Eagles/festival/academic), interactions |
| Models | Historical-average baseline → Random Forest → XGBoost → LightGBM |
| Split | Strict temporal: 2022–2023 train → 2024 val (early stopping) → 2025 holdout |

---

## Key Results

**Overall (2025 holdout, 36,500 sessions):**

| Model | RMSE (bikes/session) | Direction Accuracy | vs. Baseline |
|---|---|---|---|
| Baseline (historical avg) | 3.74 | 93.4% | — |
| **Random Forest** | **3.29** | 93.8% | **+12.1%** |
| XGBoost | 3.32 | 93.6% | +11.1% |
| LightGBM | 3.32 | 93.7% | +11.2% |

**Stratified — where ML actually earns its keep:**

| Day type | Sessions | Baseline RMSE | Best ML lift |
|---|---|---|---|
| Holidays | 1,100 | 4.97 | **+34.4%** |
| Festival days | 800 | 4.31 | **+20.7%** |
| Normal weekdays | 14,600 | 4.03 | +12.5% |
| Phillies game days | 7,700 | 3.92 | +10.4% |
| Rainy days | 8,800 | 3.57 | +9.6% |
| Eagles game days | 1,000 | 2.78 | +8.3% |
| Weekends (dry) | 8,000 | 2.63 | +1.1% |

The honest takeaway: the historical average is a strong baseline for routine days. ML earns its keep on **exception days** — which is exactly when dispatchers most need decision support.

**Dispatcher dashboard output** (Monday Sept 8 2025, Phillies vs. Mets):

```
📅 EVENT TODAY: Phillies vs. Mets
   Model applying event-day adjustment

Station 3038  predicted: -16  hist_avg: -13  adjustment: -3  →  🔴 SEND 16 bikes
Station 3208  predicted: -13  hist_avg: -14  adjustment: +1  →  🔴 SEND 13 bikes
...
13 stations SEND  |  12 stations REMOVE  |  25 stations OK
```

---

## Setup

```bash
git clone https://github.com/navalkatoch/indego-philly-bikeshare.git
cd indego-philly-bikeshare

# Install dependencies
pip install -r requirements.txt

# Download Indego trip CSVs (~600 MB, only needs to run once)
python src/data_loader.py

# Launch Jupyter
jupyter lab
```

Then open either notebook and run all cells.

---

## Project Structure

```
indego-philly-bikeshare/
├── notebooks/
│   ├── 01_descriptive_analytics.ipynb     # Visual deep-dive + rebalancing problem setup
│   └── 02_demand_forecasting.ipynb        # Net-flow ML pipeline + dispatcher dashboard
├── src/
│   ├── data_loader.py                     # Indego CSV download + Open-Meteo weather
│   └── build_special_events.py            # Curated event-date CSV builder
├── data/
│   ├── README.md                          # Data download instructions
│   └── special_events.csv                 # 390 curated event dates (2022–2025)
├── requirements.txt
└── README.md
```

Trip CSVs (~600 MB total) are not committed — regenerate via `python src/data_loader.py`.

---

## Data Sources

| Source | What | Cost |
|---|---|---|
| [Indego Trip Data](https://www.rideindego.com/about/data/) | 4.6M trips, 2022–2025 | Free |
| [Open-Meteo Historical API](https://open-meteo.com/en/docs/historical-weather-api) | Daily Philadelphia weather | Free, no API key |
| Wikipedia season pages | Phillies & Eagles home schedules | Free |
| Public Philly event calendars | Festivals, races, graduations | Free |

`data/special_events.csv` is reproducible via `python src/build_special_events.py` — sources hardcoded for portability.

---

## Methodology Caveats

- **Rebalancing cost figures** are industry benchmarks, not verified Indego operational data. The $246K baseline assumes 15 truck runs/day × $45/run × 365 days. Treat as directional.
- **Top-50 station scope** captures ~45% of rush-hour trips. Lower-volume stations are excluded because predicting demand at a 2-trip/day station has no operational value.
- **No data leakage**: train uses 2022–2024 only for historical-average and station-rank features; 2025 is a true holdout.
- **Special events flags**: curated through 2025-Q3. Future production deployment would need a live event-feed integration.

---

## Background

This project is inspired by a Data Science Bootcamp I had done while I was working at IBM. I had analyzed NYC CitiBike data and IBM's proprietary Weather Company API. This rebuild:

- Switches to **Philadelphia's Indego system** — a local observation during my time at The Wharton School
- Replaces proprietary weather with **Open-Meteo** (free, ERA5 reanalysis)
- Drops demographic features (gender, birth year) that modern datasets no longer publish for privacy reasons
- **Reframes the problem** from generic exploration to bike rebalancing — a concrete operational use case with measurable ROI

---

*Naval Katoch*
