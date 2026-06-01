"""
Static map snapshots for the Indego analysis notebooks.

GitHub's notebook renderer strips JavaScript, so the interactive Folium maps in
notebook 01 do not display inline on github.com. These matplotlib + contextily
helpers produce static PNG equivalents that *do* render inline, while the Folium
maps are kept for the fully interactive nbviewer / GitHub Pages versions.

contextily fetches basemap tiles in EPSG:3857 (Web Mercator); we pass the data
in lon/lat (EPSG:4326) and let `add_basemap` reproject via the `crs` argument.
"""

import matplotlib.pyplot as plt
import contextily as ctx

# CartoDB Positron — matches the `tiles='CartoDB positron'` used by the Folium maps
BASEMAP = ctx.providers.CartoDB.Positron


def plot_station_map(station_vol, figsize=(11, 11)):
    """Static version of the Section 3 station demand map.

    station_vol: DataFrame with columns start_lon, start_lat, trip_count.
    """
    max_count = station_vol['trip_count'].max()
    sizes = (4 + (station_vol['trip_count'] / max_count) * 22) ** 2  # area ~ radius**2

    fig, ax = plt.subplots(figsize=figsize)
    ax.scatter(
        station_vol['start_lon'], station_vol['start_lat'],
        s=sizes, color='#E53935', edgecolor='#C62828',
        linewidth=0.5, alpha=0.65, zorder=3,
    )
    ctx.add_basemap(ax, crs='EPSG:4326', source=BASEMAP)
    ax.set_axis_off()
    ax.set_title(
        'Indego Station Demand — trips originating per station (2022–2025)\n'
        'Circle size scales with trip volume',
        fontsize=13, fontweight='bold', pad=10,
    )
    plt.tight_layout()
    return fig, ax


def plot_routes_map(top_routes, route_colors, figsize=(11, 11)):
    """Static version of the Section 9 top-routes map.

    top_routes: DataFrame with start_lat/lon, end_lat/lon, trips (top 10).
    route_colors: list of hex colors, one cycled per route.
    """
    max_trips = top_routes['trips'].max()

    fig, ax = plt.subplots(figsize=figsize)
    for i, row in top_routes.iterrows():
        color = route_colors[i % len(route_colors)]
        weight = 3 + (row['trips'] / max_trips) * 7
        ax.plot(
            [row['start_lon'], row['end_lon']],
            [row['start_lat'], row['end_lat']],
            color=color, linewidth=weight, alpha=0.8, zorder=3,
        )
        # Start station (filled), end station (hollow)
        ax.scatter(row['start_lon'], row['start_lat'], s=70, color=color,
                   edgecolor=color, linewidth=2, zorder=4)
        ax.scatter(row['end_lon'], row['end_lat'], s=45, color='white',
                   edgecolor=color, linewidth=2, zorder=4)

    ctx.add_basemap(ax, crs='EPSG:4326', source=BASEMAP)
    ax.set_axis_off()
    ax.set_title(
        'Top 10 Indego Corridors — start → end station pairs (2022–2025)\n'
        'Line thickness scales with trip volume',
        fontsize=13, fontweight='bold', pad=10,
    )
    plt.tight_layout()
    return fig, ax
