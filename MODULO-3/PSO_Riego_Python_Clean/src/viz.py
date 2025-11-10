"""viz.py — Visualización de resultados.
Autor: Omar Bermejo Osuna & Diego Alberto Araujo
"""
from __future__ import annotations

import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx


def plot_solution(
    bbox_path: str,
    sensors_geojson: str,
    grid_gdf: gpd.GeoDataFrame | None = None,
    weights = None
) -> None:
    """Dibuja el polígono del área y los sensores; opcionalmente, heatmap de pesos."""
    area = gpd.read_file(bbox_path).to_crs(3857)
    sensors = gpd.read_file(sensors_geojson).to_crs(3857)

    ax = area.boundary.plot(figsize=(8, 8), linewidth=1.2, alpha=0.8)
    if grid_gdf is not None and weights is not None:
        grid_gdf.assign(w=weights).plot(ax=ax, column="w", alpha=0.55, legend=True)

    sensors.plot(ax=ax, markersize=40)
    cx.add_basemap(ax, crs=area.crs.to_string())
    ax.set_axis_off()
    plt.tight_layout()
    plt.show()
