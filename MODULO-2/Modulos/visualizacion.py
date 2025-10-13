# -*- coding: utf-8 -*-
"""Funciones de mapeo: visualización de nodos, rutas y rangos."""

import geopandas as gpd
from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import contextily as cx
import pandas as pd


def mostrar_mapa_simple(tiendas: pd.DataFrame):
    """Muestra un mapa simple con centros y tiendas (sin rutas)."""
    geometry = [Point(xy) for xy in zip(
        tiendas['Longitud_WGS84'], tiendas['Latitud_WGS84'])]
    gdf = gpd.GeoDataFrame(tiendas, geometry=geometry,
                           crs="EPSG:4326").to_crs(epsg=3857)

    centros = gdf[gdf['Tipo'].str.contains("Centro", case=False)]
    tiendas = gdf[gdf['Tipo'].str.contains("Tienda", case=False)]

    fig, ax = plt.subplots(figsize=(12, 12))
    tiendas.plot(ax=ax, color="royalblue", markersize=40,
                 alpha=0.8, label="Tiendas")
    centros.plot(ax=ax, color="red", markersize=60,
                 edgecolor="black", label="Centros")

    for idx, row in gdf.iterrows():
        ax.text(row.geometry.x, row.geometry.y, str(idx + 1),
                fontsize=7, color='black', ha='center', va='center')

    cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
    ax.set_title("Mapa simple de Centros y Tiendas", fontsize=16)
    ax.legend()
    ax.set_axis_off()
    plt.show()


def plot_rangos_rutas_nodos(tiendas_df, assignments, solutions, rings_upper, save_path=None):
    """Mapa general con todos los centros, sus rangos, rutas y nodos."""
    geometry = [Point(xy) for xy in zip(
        tiendas_df['Longitud_WGS84'], tiendas_df['Latitud_WGS84'])]
    gdf = gpd.GeoDataFrame(tiendas_df, geometry=geometry,
                           crs="EPSG:4326").to_crs(epsg=3857)

    centros = gdf[gdf['Tipo'].str.contains("Centro", case=False)]
    tiendas = gdf[gdf['Tipo'].str.contains("Tienda", case=False)]

    fig, ax = plt.subplots(figsize=(14, 14))
    centros.plot(ax=ax, color="red", markersize=80,
                 label="Centros", edgecolor="black")

    colores = plt.cm.get_cmap("tab20", len(assignments))

    for d, centro in centros.iterrows():
        x, y = centro.geometry.x, centro.geometry.y
        for r in rings_upper.get(int(d), []):
            circ = plt.Circle((x, y), r * 1000, fill=False,
                              linestyle="--", alpha=0.4, color="gray")
            ax.add_patch(circ)

    for idx_c, (d, nodes) in enumerate(assignments.items()):
        color = colores(idx_c)
        if nodes:
            gdf.loc[nodes].plot(ax=ax, color=color, markersize=40, alpha=0.8,
                                    label=f"Tiendas CD {d + 1}")

        if d in solutions:
            ruta = solutions[d]["route"]
            coords = [(gdf.loc[i].geometry.x, gdf.loc[i].geometry.y)
                      for i in ruta]
            line = LineString(coords)
            gpd.GeoSeries([line], crs="EPSG:3857").plot(
                ax=ax, color=color, linewidth=2, alpha=0.7)

    for idx, row in gdf.iterrows():
        ax.text(row.geometry.x, row.geometry.y, str(idx + 1),
                fontsize=7, color='black', ha='center', va='center')

    cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
    ax.set_title("Centros con Rangos, Rutas y Nodos", fontsize=16)
    ax.legend()
    ax.set_axis_off()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"🗺️ Mapa guardado en {save_path}")
    else:
        plt.show()


def plot_single_center(tiendas_df, centro_id, assignments, solutions, rings_upper, save_path=None):
    """Mapa individual de un centro con su rango, tiendas asignadas y ruta."""
    geometry = [Point(xy) for xy in zip(
        tiendas_df['Longitud_WGS84'], tiendas_df['Latitud_WGS84'])]
    gdf = gpd.GeoDataFrame(tiendas_df, geometry=geometry,
                           crs="EPSG:4326").to_crs(epsg=3857)

    centros = gdf[gdf['Tipo'].str.contains("Centro", case=False)]
    tiendas = gdf[gdf['Tipo'].str.contains("Tienda", case=False)]

    fig, ax = plt.subplots(figsize=(12, 12))
    color = "orange"

    if centro_id >= len(centros):
        print(f"❌ Centro {centro_id + 1} no existe.")
        return

    centro = centros.iloc[centro_id]
    centros.iloc[[centro_id]].plot(
        ax=ax, color="red", markersize=100, edgecolor="black", label="Centro seleccionado")

    if centro_id in rings_upper:
        x, y = centro.geometry.x, centro.geometry.y
        for r in rings_upper[centro_id]:
            circ = plt.Circle((x, y), r * 1000, fill=False,
                              linestyle="--", alpha=0.4, color=color)
            ax.add_patch(circ)
            ax.text(x + r * 1000, y, f"{int(r)} km", fontsize=8, color=color)

    if centro_id in assignments:
        gdf.loc[assignments[centro_id]].plot(
            ax=ax, color=color, markersize=40, alpha=0.8, label="Tiendas asignadas")

    if centro_id in solutions:
        ruta = solutions[centro_id]["route"]
        coords = [(gdf.loc[i].geometry.x, gdf.loc[i].geometry.y) for i in ruta]
        line = LineString(coords)
        gpd.GeoSeries([line], crs="EPSG:3857").plot(
            ax=ax, color=color, linewidth=2, alpha=0.7, label="Ruta optimizada")

    cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
    ax.set_title(
        f"Centro {centro_id + 1} - Rango, Tiendas y Ruta", fontsize=16)
    ax.legend()
    ax.set_axis_off()

    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches="tight")
        print(f"🗺️ Mapa guardado en {save_path}")
    else:
        plt.show()
