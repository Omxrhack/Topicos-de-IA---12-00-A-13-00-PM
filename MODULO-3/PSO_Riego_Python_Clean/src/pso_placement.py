"""pso_placement.py — Pérdida y utilidades para PSO.
Autor: Omar Bermejo Osuna & Diego Alberto Araujo
"""
from __future__ import annotations

import numpy as np
from scipy.spatial.distance import cdist


def loss_sensor_layout(
    X: np.ndarray,
    k: int,
    grid_xy: np.ndarray,
    weights: np.ndarray,
    lambda_cluster: float = 0.1,
    cap_radius: float = 100.0,
) -> np.ndarray:
    """Calcula la pérdida para cada partícula.

    Parámetros
    ----------
    X : (n_particles, 2*k)
        Posiciones concatenadas de sensores (x1,y1,...,xk,yk).
    k : int
        Número de sensores.
    grid_xy : (G,2)
        Coordenadas de centros de celdas.
    weights : (G,)
        Peso de cada celda [0,1].
    lambda_cluster : float
        Peso de penalización por agrupamiento.
    cap_radius : float
        Radio máximo efectivo para limitar distancias en cobertura.

    Retorna
    -------
    losses : (n_particles,)
        Pérdida por partícula.
    """
    n_particles = X.shape[0]
    losses = np.zeros(n_particles, dtype=float)

    for i in range(n_particles):
        sensors = X[i].reshape(k, 2)

        # Distancias celdas -> sensores y mínimo por celda
        d = cdist(grid_xy, sensors)  # (G,k)
        dmin = d.min(axis=1)
        dmin = np.minimum(dmin, cap_radius)

        loss_cov = float(np.average(dmin, weights=weights))

        # Penalización por clustering (1/dist) promedio entre sensores
        if k > 1:
            D = cdist(sensors, sensors)
            D[D == 0.0] = np.inf
            invD = 1.0 / D[np.triu_indices(k, 1)]
            cluster_pen = float(invD.mean())
        else:
            cluster_pen = 0.0

        losses[i] = loss_cov + lambda_cluster * cluster_pen

    return losses


def build_bounds(k: int, minx: float, miny: float, maxx: float, maxy: float):
    """Construye cotas inferiores y superiores para cada coordenada de sensor."""
    lb = np.tile([minx, miny], k)
    ub = np.tile([maxx, maxy], k)
    return lb, ub
