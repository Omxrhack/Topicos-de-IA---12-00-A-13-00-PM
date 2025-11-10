"""features.py — Utilidades de datos y construcción de pesos.
Autor: Omar Bermejo Osuna & Diego Alberto Araujo
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple
import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point, box

CULTIVO_PESOS = {"tomate": 1.0, "chile": 0.8, "maiz": 0.6}


def load_points(csv_path: str) -> gpd.GeoDataFrame:
    """Carga un CSV de puntos (lat, lon, cultivo, elev_m, salinidad_dSm, humedad_pct, temp_c)
    y devuelve un GeoDataFrame en EPSG:3857 (metros).
    """
    df = pd.read_csv(csv_path)
    required = {"lat", "lon", "cultivo", "elev_m", "salinidad_dSm", "humedad_pct", "temp_c"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas en {csv_path}: {sorted(missing)}")

    gdf = gpd.GeoDataFrame(
        df,
        geometry=gpd.points_from_xy(df["lon"], df["lat"]),
        crs="EPSG:4326"
    ).to_crs(3857)
    return gdf


def grid_from_bbox(bbox_geojson: str, cell_size: int = 50) -> gpd.GeoDataFrame:
    """Crea una grilla de celdas cuadradas dentro del polígono del bbox.
    - bbox_geojson: GeoJSON en WGS84.
    - cell_size: tamaño de celda (m).
    """
    area = gpd.read_file(bbox_geojson).to_crs(3857)
    minx, miny, maxx, maxy = area.total_bounds

    xs = np.arange(minx, maxx, cell_size)
    ys = np.arange(miny, maxy, cell_size)

    cells = []
    area_union = area.geometry.unary_union
    for x in xs:
        for y in ys:
            poly = box(x, y, x + cell_size, y + cell_size)
            if area_union.intersects(poly):
                cells.append(poly)

    return gpd.GeoDataFrame(geometry=cells, crs=3857)


def _idw(xy_targets: np.ndarray, pts: np.ndarray, values: np.ndarray, power: float = 2.0) -> np.ndarray:
    """Interpolación Inversa a la Distancia (IDW) simple.”””
    d = np.linalg.norm(xy_targets[:, None, :] - pts[None, :, :], axis=2) + 1e-6
    w = 1.0 / np.power(d, power)
    w = w / (w.sum(axis=1, keepdims=True))
    return (w * values[None, :]).sum(axis=1)


def _norm(z: np.ndarray) -> np.ndarray:
    z = z.astype(float)
    rng = z.max() - z.min()
    if rng <= 0:
        return np.zeros_like(z)
    return (z - z.min()) / rng


def weight_map(
    gdf_points: gpd.GeoDataFrame,
    grid_gdf: gpd.GeoDataFrame,
    w_cultivo: float = 0.5,
    w_salinidad: float = 0.25,
    w_relieve: float = 0.2,
    w_temp: float = 0.05,
) -> np.ndarray:
    """Construye un mapa de pesos [0,1] para cada celda de la grilla."""
    centroids = grid_gdf.geometry.centroid
    grid_xy = np.column_stack([centroids.x.values, centroids.y.values])

    pts_xy = np.column_stack([gdf_points.geometry.x.values, gdf_points.geometry.y.values])

    # Interpolar atributos
    sal = _idw(grid_xy, pts_xy, gdf_points["salinidad_dSm"].values)
    elev = _idw(grid_xy, pts_xy, gdf_points["elev_m"].values)
    temp = _idw(grid_xy, pts_xy, gdf_points["temp_c"].values)

    sal_n, elev_n, temp_n = _norm(sal), _norm(elev), _norm(temp)

    # Peso por cultivo (dummy IDW de pertenencia a cada cultivo)
    cult_score = np.zeros(len(grid_gdf), dtype=float)
    for c, pc in CULTIVO_PESOS.items():
        dmy = (gdf_points["cultivo"].str.lower() == c).astype(float).values
        cult_c = _idw(grid_xy, pts_xy, dmy)
        cult_score += pc * cult_c

    w = (w_cultivo * cult_score
         + w_salinidad * sal_n
         + w_relieve * elev_n
         + w_temp * temp_n)

    return _norm(w)
