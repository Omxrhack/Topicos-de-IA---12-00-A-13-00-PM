import numpy as np
from src.pso_placement import loss_sensor_layout


def test_loss_shapes():
    G = 100
    grid_xy = np.random.rand(G, 2) * 1000.0
    weights = np.random.rand(G)
    k = 5
    X = np.random.rand(3, 2 * k) * 1000.0  # 3 partículas
    L = loss_sensor_layout(X, k, grid_xy, weights)
    assert L.shape == (3,)
    assert np.all(np.isfinite(L))
