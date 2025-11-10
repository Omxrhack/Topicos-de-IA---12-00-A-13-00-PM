import numpy as np
from src.features import load_points, grid_from_bbox, weight_map


def test_grid_and_weights():
    gdf = load_points("data/parcelas.csv")
    grid = grid_from_bbox("data/bbox.geojson", cell_size=50)
    w = weight_map(gdf, grid)
    assert len(w) == len(grid)
    assert np.all(w >= 0) and np.all(w <= 1)
