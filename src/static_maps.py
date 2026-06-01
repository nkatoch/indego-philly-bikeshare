"""
Static map snapshots for the Indego analysis notebooks.

GitHub's notebook renderer strips JavaScript, so the interactive Folium maps in
notebook 01 do not display inline on github.com. These matplotlib + contextily
helpers produce static equivalents that *do* render inline, while the Folium
maps are kept for the fully interactive nbviewer / GitHub Pages versions.

Coordinates are reprojected from lon/lat (EPSG:4326) to Web Mercator
(EPSG:3857) and plotted with equal aspect, so the basemap tiles are not
stretched (plotting raw degrees at Philadelphia's latitude distorts the map).
"""

import numpy as np
import matplotlib.pyplot as plt
import contextily as ctx

# CartoDB Positron — matches the `tiles='CartoDB positron'` used by the Folium maps
BASEMAP = ctx.providers.CartoDB.Positron
_R = 6378137.0  # WGS84 / Web Mercator radius (metres)


def to_mercator(lon, lat):
    """Forward Web Mercator (EPSG:4326 -> EPSG:3857). Avoids a pyproj dependency."""
    lon = np.asarray(lon, dtype=float)
    lat = np.asarray(lat, dtype=float)
    x = np.radians(lon) * _R
    y = np.log(np.tan(np.pi / 4 + np.radians(lat) / 2)) * _R
    return x, y


def _framed_axes(xs, ys, pad=0.22, base_h=11, clip_pct=None):
    """Equal-aspect axes with a padded extent; figure sized to the bbox aspect.

    clip_pct: if set (e.g. 1), use the [clip_pct, 100-clip_pct] coordinate
    percentiles for the extent instead of min/max — excludes lone outlier
    stations with bad coordinates that would otherwise blow out the view.
    """
    if clip_pct is not None:
        xmin, xmax = np.percentile(xs, [clip_pct, 100 - clip_pct])
        ymin, ymax = np.percentile(ys, [clip_pct, 100 - clip_pct])
    else:
        xmin, xmax, ymin, ymax = xs.min(), xs.max(), ys.min(), ys.max()
    dx, dy = xmax - xmin, ymax - ymin
    xmin, xmax = xmin - dx * pad, xmax + dx * pad
    ymin, ymax = ymin - dy * pad, ymax + dy * pad
    aspect = (xmax - xmin) / (ymax - ymin)
    fig, ax = plt.subplots(figsize=(base_h * aspect, base_h))
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_aspect("equal")
    ax.set_axis_off()
    return fig, ax


def plot_station_map(station_vol):
    """Static version of the Section 3 station demand map.

    station_vol: DataFrame with columns start_lon, start_lat, trip_count.
    """
    x, y = to_mercator(station_vol["start_lon"].values, station_vol["start_lat"].values)
    max_count = station_vol["trip_count"].max()
    sizes = 18 + (station_vol["trip_count"].values / max_count) * 900

    fig, ax = _framed_axes(x, y, clip_pct=1.0)
    ax.scatter(x, y, s=sizes, color="#E53935", edgecolor="#B71C1C",
               linewidth=0.6, alpha=0.62, zorder=3)
    ctx.add_basemap(ax, source=BASEMAP)
    ax.set_title("Indego Station Demand — trips originating per station (2022–2025)\n"
                 "Circle size scales with trip volume",
                 fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    return fig, ax


def plot_routes_map(top_routes, route_colors, station_names=None):
    """Static version of the Section 9 top-routes map.

    top_routes: DataFrame with start_lat/lon, end_lat/lon, trips (top 10).
    route_colors: list of hex colors, one cycled per route.
    station_names: optional {station_id: name} mapping; if given, points are
        labelled with the real station name instead of the numeric ID.
    """
    sx, sy = to_mercator(top_routes["start_lon"].values, top_routes["start_lat"].values)
    ex, ey = to_mercator(top_routes["end_lon"].values, top_routes["end_lat"].values)
    max_trips = top_routes["trips"].max()

    fig, ax = _framed_axes(np.concatenate([sx, ex]),
                           np.concatenate([sy, ey]), pad=0.28)

    for i, row in top_routes.iterrows():
        color = route_colors[i % len(route_colors)]
        weight = 3 + (row["trips"] / max_trips) * 7
        ax.plot([sx[i], ex[i]], [sy[i], ey[i]], color=color, linewidth=weight,
                alpha=0.8, zorder=3, solid_capstyle="round")
        ax.scatter(sx[i], sy[i], s=90, color=color, edgecolor="white",
                   linewidth=1.5, zorder=4)
        ax.scatter(ex[i], ey[i], s=60, color="white", edgecolor=color,
                   linewidth=1.8, zorder=4)

    # Compact, de-duplicated labels (real station name if available, else ID)
    def _label(stn):
        if station_names:
            return station_names.get(stn, station_names.get(int(stn), str(int(stn))))
        return str(int(stn))

    seen = set()
    for i, row in top_routes.iterrows():
        for stn, px, py in ((row["start_station"], sx[i], sy[i]),
                            (row["end_station"], ex[i], ey[i])):
            if stn in seen:
                continue
            seen.add(stn)
            ax.annotate(_label(stn), (px, py),
                        xytext=(5, 4), textcoords="offset points",
                        fontsize=7.5, fontweight="bold", color="#212121", zorder=5,
                        bbox=dict(boxstyle="round,pad=0.15", fc="white",
                                  ec="none", alpha=0.78))

    ctx.add_basemap(ax, source=BASEMAP)
    ax.set_title("Top 10 Indego Corridors — start → end station pairs (2022–2025)\n"
                 "Line thickness scales with trip volume",
                 fontsize=14, fontweight="bold", pad=12)
    fig.tight_layout()
    return fig, ax
