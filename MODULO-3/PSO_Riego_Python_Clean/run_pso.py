"""run_pso.py — Script CLI para ejecutar PSO de colocación de sensores.
Autor: Omar Bermejo Osuna & Diego Alberto Araujo
"""
from __future__ import annotations

import argparse
import numpy as np
import geopandas as gpd
from pyswarms.single import GlobalBestPSO

from src.features import load_points, grid_from_bbox, weight_map
from src.pso_placement import loss_sensor_layout, build_bounds


def main() -> None:
    parser = argparse.ArgumentParser(description="Optimización PSO de sensores de humedad")
    parser.add_argument("--csv", default="data/parcelas.csv", help="Ruta al CSV de puntos")
    parser.add_argument("--bbox", default="data/bbox.geojson", help="GeoJSON del área de estudio")
    parser.add_argument("--k", type=int, default=6, help="Número de sensores")
    parser.add_argument("--cell", type=int, default=50, help="Tamaño de celda (m) para la grilla")
    parser.add_argument("--particles", type=int, default=40, help="Número de partículas PSO")
    parser.add_argument("--iters", type=int, default=120, help="Iteraciones PSO")
    parser.add_argument("--lc", type=float, default=0.1, help="Peso de penalización por clustering")
    parser.add_argument("--cap", type=float, default=100.0, help="Radio máximo efectivo (m)")
    parser.add_argument("--out", default="sensors.geojson", help="Archivo GeoJSON de salida")
    args = parser.parse_args()

    # Datos y capas
    pts = load_points(args.csv)
    grid = grid_from_bbox(args.bbox, cell_size=args.cell)
    w = weight_map(pts, grid)

    grid_xy = np.column_stack([grid.geometry.centroid.x.values, grid.geometry.centroid.y.values])

    # Bounds del área
    minx, miny, maxx, maxy = grid.total_bounds
    lb, ub = build_bounds(args.k, minx, miny, maxx, maxy)

    # Función objetivo para PSO
    def objective(X: np.ndarray) -> np.ndarray:
        return loss_sensor_layout(X, args.k, grid_xy, w, lambda_cluster=args.lc, cap_radius=args.cap)

    opt = GlobalBestPSO(
        n_particles=args.particles,
        dimensions=2 * args.k,
        options={"c1": 1.5, "c2": 1.5, "w": 0.6},
        bounds=(lb, ub),
    )

    best_cost, best_pos = opt.optimize(objective, iters=args.iters, verbose=True)
    sensors = best_pos.reshape(args.k, 2)

    # Exporta sensores como GeoJSON en WGS84
    gdf = gpd.GeoDataFrame(geometry=gpd.points_from_xy(sensors[:, 0], sensors[:, 1]), crs=3857)
    gdf = gdf.to_crs(4326)
    gdf.to_file(args.out, driver="GeoJSON")

    print(f"Mejor costo: {best_cost:.6f}")
    print(f"Sensores guardados en: {args.out}")


if __name__ == "__main__":
    main()
