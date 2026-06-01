"""
Build the executive HTML report (docs/index.html) for the Indego bike-rebalancing
project. Pulls already-rendered chart images straight from the two notebooks'
saved outputs (no data re-run needed) and assembles one self-contained, styled,
print-friendly page that tells the Challenge -> Approach -> Solution -> Impact
story.

Run:  python src/build_report.py
Deterministic: re-running reproduces docs/index.html.
"""

import base64
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NB_DIR = ROOT / "notebooks"
OUT = ROOT / "docs" / "index.html"

# Chart -> (notebook stem, 0-indexed cell number). Verified from saved outputs.
CHARTS = {
    # notebook 01 — descriptive
    "growth":        ("01_descriptive_analytics", 7),
    "station_map":   ("01_descriptive_analytics", 9),
    "imbalance":     ("01_descriptive_analytics", 12),
    "concentration": ("01_descriptive_analytics", 14),
    "heatmap":       ("01_descriptive_analytics", 16),
    "event":         ("01_descriptive_analytics", 18),
    "commuter":      ("01_descriptive_analytics", 20),
    "duration":      ("01_descriptive_analytics", 22),
    "ebike_trend":   ("01_descriptive_analytics", 25),
    "weather":       ("01_descriptive_analytics", 28),
    "routes_map":    ("01_descriptive_analytics", 31),
    # notebook 02 — forecasting
    "netflow_dist":  ("02_demand_forecasting", 10),
    "rmse":          ("02_demand_forecasting", 25),
    "lift":          ("02_demand_forecasting", 27),
    "importance":    ("02_demand_forecasting", 28),
    "dispatch":      ("02_demand_forecasting", 31),
}


def _load_images():
    """Return {chart_name: data-URI string} extracted from notebook outputs."""
    cache, imgs = {}, {}
    for name, (stem, idx) in CHARTS.items():
        if stem not in cache:
            cache[stem] = json.loads((NB_DIR / f"{stem}.ipynb").read_text(encoding="utf-8"))
        cell = cache[stem]["cells"][idx]
        data_uri = None
        for out in cell.get("outputs", []):
            data = out.get("data") or {}
            for mime in ("image/png", "image/jpeg"):
                if mime in data:
                    payload = data[mime]
                    if isinstance(payload, list):
                        payload = "".join(payload)
                    payload = payload.strip().replace("\n", "")
                    data_uri = f"data:{mime};base64,{payload}"
                    break
            if data_uri:
                break
        if data_uri is None:
            raise RuntimeError(f"No image found for '{name}' ({stem} cell {idx})")
        imgs[name] = data_uri
    return imgs


CSS = """
:root{
  --ink:#14213d; --muted:#5b6577; --line:#e6e9ef; --bg:#ffffff; --soft:#f6f8fb;
  --accent:#1565C0; --accent2:#E53935; --good:#2e7d32; --chip:#eef3fb;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth}
body{margin:0;color:var(--ink);background:var(--bg);
  font-family:-apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif;
  line-height:1.65;font-size:17px;-webkit-font-smoothing:antialiased}
.wrap{max-width:880px;margin:0 auto;padding:0 22px}
h1,h2,h3{font-family:Georgia,"Times New Roman",serif;line-height:1.2;color:var(--ink)}
h2{font-size:30px;margin:0 0 6px}
h3{font-size:21px;margin:30px 0 6px}
p{margin:14px 0}
a{color:var(--accent);text-decoration:none}
a:hover{text-decoration:underline}
.eyebrow{font-family:-apple-system,Segoe UI,sans-serif;text-transform:uppercase;
  letter-spacing:.14em;font-size:12.5px;font-weight:700;color:var(--accent)}
/* sticky nav */
nav{position:sticky;top:0;z-index:20;background:rgba(255,255,255,.92);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
nav .wrap{display:flex;gap:18px;align-items:center;height:52px;overflow-x:auto}
nav .brand{font-weight:800;font-family:Georgia,serif;white-space:nowrap}
nav a{color:var(--muted);font-size:14px;font-weight:600;white-space:nowrap}
nav a:hover{color:var(--accent);text-decoration:none}
/* hero */
.hero{background:linear-gradient(160deg,#0d1b3a 0%,#1565C0 100%);color:#fff;
  padding:74px 0 64px}
.hero h1{color:#fff;font-size:46px;margin:10px 0 10px;letter-spacing:-.5px}
.hero .lede{font-size:20px;color:#dce6f7;max-width:680px}
.hero .eyebrow{color:#9ec3f3}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin:38px 0 0}
.kpi{background:rgba(255,255,255,.10);border:1px solid rgba(255,255,255,.18);
  border-radius:14px;padding:18px 16px}
.kpi .n{font-family:Georgia,serif;font-size:30px;font-weight:700;color:#fff;line-height:1.05}
.kpi .l{font-size:13px;color:#cdddf6;margin-top:6px}
/* sections */
section{padding:46px 0;border-bottom:1px solid var(--line)}
section.alt{background:var(--soft)}
.lead{font-size:19px;color:var(--ink)}
.muted{color:var(--muted)}
/* figures */
figure{margin:26px 0;text-align:center}
img.chart{max-width:100%;height:auto;border:1px solid var(--line);border-radius:10px;
  box-shadow:0 6px 22px rgba(20,33,61,.07)}
figcaption{font-size:14px;color:var(--muted);margin-top:9px}
.mapbtn{display:inline-block;margin-top:10px;font-size:14px;font-weight:700;
  background:var(--chip);border:1px solid #d4e0f4;border-radius:999px;
  padding:7px 15px;color:var(--accent)}
.mapbtn:hover{text-decoration:none;background:#e3edfb}
/* tables */
table{width:100%;border-collapse:collapse;margin:20px 0;font-size:15.5px}
th,td{text-align:left;padding:11px 13px;border-bottom:1px solid var(--line);vertical-align:top}
thead th{background:var(--ink);color:#fff;font-family:-apple-system,sans-serif;
  font-size:13px;letter-spacing:.03em}
tbody tr:nth-child(even){background:var(--soft)}
td.num,th.num{text-align:right;font-variant-numeric:tabular-nums}
.win{color:var(--good);font-weight:700}
caption{caption-side:bottom;font-size:13px;color:var(--muted);margin-top:8px;text-align:left}
/* callouts */
.callout{background:#fff;border:1px solid var(--line);border-left:4px solid var(--accent);
  border-radius:10px;padding:16px 20px;margin:22px 0}
.callout.warn{border-left-color:var(--accent2)}
.term{background:#0e1726;color:#dbe7ff;border-radius:10px;padding:18px 20px;margin:22px 0;
  font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:14px;
  line-height:1.7;overflow-x:auto;white-space:pre}
.term .send{color:#ff7a7a;font-weight:700}
.term .rem{color:#7ab8ff;font-weight:700}
.term .ev{color:#ffd166}
/* two-up */
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:24px;align-items:start}
details{margin:14px 0;border:1px solid var(--line);border-radius:10px;padding:4px 16px;background:#fff}
summary{cursor:pointer;font-weight:700;padding:10px 0}
footer{padding:40px 0 70px;color:var(--muted);font-size:14.5px}
footer .name{font-family:Georgia,serif;color:var(--ink);font-size:17px;font-weight:700}
@media (max-width:720px){
  .kpis{grid-template-columns:repeat(2,1fr)} .grid2{grid-template-columns:1fr}
  .hero h1{font-size:34px} h2{font-size:25px}
}
@media print{
  nav{display:none} .hero{background:#0d1b3a!important;-webkit-print-color-adjust:exact;print-color-adjust:exact}
  section{break-inside:avoid;border:none;padding:18px 0} .mapbtn{display:none}
  img.chart{box-shadow:none} a{color:var(--ink)}
  thead th,.term{-webkit-print-color-adjust:exact;print-color-adjust:exact}
}
"""


def build():
    img = _load_images()

    def fig(name, caption, map_link=None):
        btn = f'<a class="mapbtn" href="{map_link}">↗ Open the live interactive map</a>' if map_link else ""
        return (f'<figure><img class="chart" src="{img[name]}" alt="{caption}">'
                f'<figcaption>{caption}</figcaption>{btn}</figure>')

    html = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Indego Bike Rebalancing — Executive Report</title>
<meta name="description" content="Turning four years of Philadelphia Indego trip data into a proactive bike-rebalancing forecast worth an estimated $60–80K/year.">
<style>{CSS}</style>
</head>
<body>

<nav><div class="wrap">
  <span class="brand">Indego · Rebalancing</span>
  <a href="#challenge">Challenge</a>
  <a href="#context">Context</a>
  <a href="#approach">Approach</a>
  <a href="#solution">Solution</a>
  <a href="#impact">Impact</a>
</div></nav>

<header class="hero"><div class="wrap">
  <div class="eyebrow">Philadelphia Bike Share · Operations Analytics</div>
  <h1>Predicting the morning bike shortage before it happens</h1>
  <p class="lede">Every rush hour, Indego stations drain and overflow in predictable
  patterns. Using four years of public trip data, we forecast each station's net
  bike flow per rush session — turning reactive scrambling into a proactive dispatch plan.</p>
  <div class="kpis">
    <div class="kpi"><div class="n">4.6M</div><div class="l">trips analysed (2022–2025)</div></div>
    <div class="kpi"><div class="n">~$246K</div><div class="l">est. annual rebalancing cost</div></div>
    <div class="kpi"><div class="n">+12%<span style="font-size:15px">→+34%</span></div><div class="l">forecast accuracy lift vs. baseline (overall → holidays)</div></div>
    <div class="kpi"><div class="n">$60–80K</div><div class="l">est. annual value unlocked</div></div>
  </div>
</div></header>

<section id="challenge"><div class="wrap">
  <div class="eyebrow">The Challenge</div>
  <h2>The problem isn't how many bikes move — it's where they end up</h2>
  <p class="lead">Indego's stations face a structural supply–demand imbalance every
  rush hour. In the morning, riders cycle <em>from</em> residential neighbourhoods
  <em>into</em> Center City and University City. Residential docks empty out;
  downtown docks fill up with nowhere to return a bike. In the evening the imbalance
  runs in reverse. The operational signal that matters is not raw departures — it is
  <strong>net flow</strong>: departures minus arrivals over a rush session.</p>

  <table>
    <caption>Why net flow, not departures, is the metric dispatchers act on.</caption>
    <thead><tr><th>Metric</th><th>Value</th><th>Operational meaning</th></tr></thead>
    <tbody>
      <tr><td>Avg. departures/hour at a top station</td><td class="num">~3 bikes</td>
          <td>A 15-dock station takes ~5 hours to empty — not urgent.</td></tr>
      <tr><td><strong>Avg. net flow over the AM rush session</strong></td><td class="num"><strong>−8 bikes</strong></td>
          <td><strong>Station loses 8 bikes in 3 hours — needs a truck before 7am.</strong></td></tr>
    </tbody>
  </table>

  {fig("station_map", "Station demand across Philadelphia — circle size scales with trips originating. Demand concentrates sharply in Center City and University City.", "map_stations.html")}

  <p>That concentration is the crux of the operational problem: bikes flow along a
  handful of dominant corridors into a small set of stations.</p>

  <div class="grid2">
    {fig("imbalance", "Net flow by station during AM and PM rush — red stations drain (need bikes pre-positioned), blue stations fill (need bikes collected).")}
    {fig("concentration", "Demand is highly concentrated: the top 50 stations carry roughly half of all rush-hour trips — so that is where forecasting pays off.")}
  </div>

  <h3>What reactive rebalancing costs</h3>
  <p>Today, roughly a third of dispatches are <em>reactive</em> — a driver is sent
  only after a station has already run empty or full. That is the expensive,
  service-damaging share.</p>
  <table>
    <caption>Rebalancing cost estimate. Indego does not publish these figures; values
    are industry benchmarks (≈15 runs/day, ~$45/run, ~30% reactive per Singhvi et al., 2015) — directional, not audited.</caption>
    <thead><tr><th>Cost component</th><th class="num">Estimate</th></tr></thead>
    <tbody>
      <tr><td>Truck runs per day</td><td class="num">12–18</td></tr>
      <tr><td>Cost per run (driver + fuel + vehicle)</td><td class="num">~$45</td></tr>
      <tr><td>Annual rebalancing cost</td><td class="num">~$246K</td></tr>
      <tr><td>Share that is reactive</td><td class="num">~30%</td></tr>
    </tbody>
  </table>
</div></section>

<section id="context" class="alt"><div class="wrap">
  <div class="eyebrow">The Context</div>
  <h2>How Philadelphia actually rides</h2>
  <p class="lead">Before modelling, the data tells a clear behavioural story —
  and every pattern below feeds the forecast that follows.</p>

  {fig("growth", "Indego ridership grew steadily across 2022–2025, reaching a record ~1.3M trips in 2024.")}

  <div class="grid2">
    {fig("heatmap", "Trips by hour and weekday. Two sharp weekday commute peaks (≈8am, 5–6pm) define the rush windows the model forecasts.")}
    {fig("weather", "Ridership tracks temperature, and rain days see materially fewer trips — a signal the model encodes directly.")}
  </div>

  {fig("routes_map", "The top 10 corridors — start → end station pairs — cluster tightly around Center City and University City, the same stations that drain and fill.", "map_routes.html")}
</div></section>

<section id="approach"><div class="wrap">
  <div class="eyebrow">The Approach</div>
  <h2>Forecasting net flow, one rush session at a time</h2>
  <p class="lead">We predict <strong>net bike flow</strong> for each of the top 50
  stations across the <strong>AM rush (7–9am)</strong> and <strong>PM rush (4–7pm)</strong>
  sessions. A predicted −8 means <em>pre-position 8 bikes before the rush</em>; a
  predicted +6 means <em>remove 6 bikes after it</em>. The output is the dispatch instruction itself.</p>

  <h3>Engineered features</h3>
  <p>All features use only information available <em>before</em> a session begins —
  prior-day lags, calendar, and weather forecast — so there is no data leakage.</p>
  <table>
    <thead><tr><th>Driver</th><th>Features</th></tr></thead>
    <tbody>
      <tr><td><strong>Session &amp; time</strong></td><td>AM/PM session, day of week, month, season, weekend flag, holiday flag, year</td></tr>
      <tr><td><strong>Station history</strong></td><td>Historical average net flow for station × session × weekday (training set only)</td></tr>
      <tr><td><strong>Recent activity</strong></td><td>Lag 1-day, lag 7-day (same session), rolling 7-day average</td></tr>
      <tr><td><strong>Weather</strong></td><td>Temperature, precipitation, wind, rain-day flag</td></tr>
      <tr><td><strong>Interactions</strong></td><td>Temperature × weekend, rain × AM session</td></tr>
      <tr><td><strong>Events</strong></td><td>Phillies/Eagles home games, festivals, academic events</td></tr>
    </tbody>
  </table>

  <div class="callout"><strong>Honest evaluation by design.</strong> The data is split
  strictly in time — train on 2022–2023, tune on 2024 (with early stopping), and
  report only on a fully held-out 2025. Four models are compared on the same holdout:
  a historical-average baseline, Random Forest, XGBoost, and LightGBM.</div>

  {fig("netflow_dist", "Session-level net flow is centred near zero but with heavy operational tails — the −8 and +6 sessions are exactly the ones worth dispatching for.")}
</div></section>

<section id="solution" class="alt"><div class="wrap">
  <div class="eyebrow">The Solution</div>
  <h2>A model that beats the baseline where it counts</h2>
  <p class="lead">On the 2025 holdout (36,500 sessions), machine learning improves
  forecast error by ~12% overall. But the average understates the story — the real
  value shows up on the exception days dispatchers struggle with most.</p>

  <table>
    <caption>All models evaluated on the untouched 2025 holdout. Direction accuracy =
    share of operationally significant sessions (|net flow| &gt; 3) dispatched in the correct direction.</caption>
    <thead><tr><th>Model</th><th class="num">RMSE (bikes/session)</th><th class="num">Direction accuracy</th><th class="num">vs. baseline</th></tr></thead>
    <tbody>
      <tr><td>Baseline (historical average)</td><td class="num">3.74</td><td class="num">93.4%</td><td class="num">—</td></tr>
      <tr><td><strong>Random Forest</strong></td><td class="num"><strong>3.29</strong></td><td class="num">93.8%</td><td class="num win">+12.1%</td></tr>
      <tr><td>XGBoost</td><td class="num">3.32</td><td class="num">93.6%</td><td class="num win">+11.1%</td></tr>
      <tr><td>LightGBM</td><td class="num">3.32</td><td class="num">93.7%</td><td class="num win">+11.2%</td></tr>
    </tbody>
  </table>

  <div class="grid2">
    {fig("rmse", "Forecast error by model — every ML approach beats the historical-average baseline.")}
    {fig("importance", "What drives the forecast: station history and recent lags dominate, with weather and calendar refining the edges.")}
  </div>

  <h3>Where ML earns its keep</h3>
  <p>On routine days the historical average is already strong. The model pulls ahead
  precisely on the irregular, high-stress days — holidays, festivals, game days,
  rain — when dispatchers most need decision support.</p>
  <table>
    <caption>Best-model RMSE improvement over baseline, stratified by day type (2025 holdout).</caption>
    <thead><tr><th>Day type</th><th class="num">Sessions</th><th class="num">Baseline RMSE</th><th class="num">Best ML lift</th></tr></thead>
    <tbody>
      <tr><td>Holidays</td><td class="num">1,100</td><td class="num">4.97</td><td class="num win">+34.4%</td></tr>
      <tr><td>Festival days</td><td class="num">800</td><td class="num">4.31</td><td class="num win">+20.7%</td></tr>
      <tr><td>Normal weekdays</td><td class="num">14,600</td><td class="num">4.03</td><td class="num win">+12.5%</td></tr>
      <tr><td>Phillies game days</td><td class="num">7,700</td><td class="num">3.92</td><td class="num win">+10.4%</td></tr>
      <tr><td>Rainy days</td><td class="num">8,800</td><td class="num">3.57</td><td class="num win">+9.6%</td></tr>
      <tr><td>Eagles game days</td><td class="num">1,000</td><td class="num">2.78</td><td class="num win">+8.3%</td></tr>
      <tr><td>Weekends (dry)</td><td class="num">8,000</td><td class="num">2.63</td><td class="num">+1.1%</td></tr>
    </tbody>
  </table>

  {fig("lift", "Forecast-accuracy lift over the baseline by day type — the model's advantage is largest exactly on the hardest-to-predict exception days.")}

  <h3>The output is a dispatch plan</h3>
  <p>Run twice daily — before AM rush (~6:30am) and PM rush (~3:30pm) — the model
  produces a ranked, actionable list, not a chart to interpret.</p>
  {fig("dispatch", "Forecast dispatch plan for a Monday AM rush — red stations need bikes pre-positioned, blue stations need bikes removed.")}
  <div class="term"><span class="ev">📅 EVENT TODAY: Phillies vs. Mets — model applying event-day adjustment</span>

Station 3038   predicted: −16   hist_avg: −13   → <span class="send">🔴 SEND 16 bikes</span>
Station 3208   predicted: −13   hist_avg: −14   → <span class="send">🔴 SEND 13 bikes</span>
Station 3032   predicted:  +9   hist_avg:  +7   → <span class="rem">🔵 REMOVE 9 bikes</span>
…
<span class="send">13 stations SEND</span>  |  <span class="rem">12 stations REMOVE</span>  |  25 stations OK</div>
</div></section>

<section id="impact"><div class="wrap">
  <div class="eyebrow">The Impact</div>
  <h2>An estimated $60–80K/year — from public data alone</h2>
  <p class="lead">Cutting the reactive dispatch share roughly in half — achievable
  with reliable demand prediction — converts into both direct operating savings and
  better rider experience.</p>
  <table>
    <thead><tr><th>Value lever</th><th class="num">Est. annual value</th></tr></thead>
    <tbody>
      <tr><td>Direct operations savings (fewer reactive runs)</td><td class="num">~$37K</td></tr>
      <tr><td>Subscriber retention (fewer empty/full-station encounters)</td><td class="num">~$26K</td></tr>
      <tr><td><strong>Total</strong></td><td class="num"><strong>~$60–80K</strong></td></tr>
    </tbody>
  </table>

  <div class="callout warn"><strong>Methodology caveats.</strong> Cost and value
  figures are industry-benchmark estimates, not audited Indego data, and should be
  read as directional. The forecast scope is the top 50 stations (~half of rush-hour
  demand); very low-volume stations are intentionally excluded. 2025 is a true holdout —
  no leakage into training.</div>

  <h3>From prototype to production</h3>
  <p>Next steps: integrate Indego's live GBFS station feed for real-time inventory
  validation, keep the event calendar current, retrain quarterly as new trip data
  lands, and surface the twice-daily plan in a simple dispatcher dashboard.</p>

  <details><summary>Appendix — additional analysis</summary>
    {fig("commuter", "One-way (commute) vs. round-trip (recreational) riding by hour and by weekday/weekend.")}
    {fig("duration", "Average and median trip duration by passholder type — subscribers take shorter, purposeful trips.")}
    {fig("ebike_trend", "Electric bikes now make up the majority of Indego trips, and their share keeps climbing.")}
    {fig("event", "A Phillies home-game Monday vs. a normal Monday — same season and weekday, very different demand.")}
  </details>
</div></section>

<footer><div class="wrap">
  <p class="name">Naval Katoch</p>
  <p class="muted">Senior Analytics Consultant · WEMBA, The Wharton School<br>
  Data: Indego Bike Share (Bicycle Transit Systems / City of Philadelphia) · Weather: Open-Meteo historical API.<br>
  Full analysis: <a href="https://github.com/nkatoch/indego-philly-bikeshare">github.com/nkatoch/indego-philly-bikeshare</a></p>
</div></footer>

</body>
</html>"""

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(html, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)}  ({OUT.stat().st_size/1e6:.2f} MB)")


if __name__ == "__main__":
    build()
