# Proyecto PSO — Optimización de Colocación de Sensores de Riego (Guasave)

Este repositorio contiene una implementación limpia en **Python 3** del algoritmo **PSO (Particle Swarm Optimization)** para ubicar sensores de humedad del suelo de forma óptima dentro de un polígono de estudio (ej. parcela en Guasave, Sinaloa).

## Estructura

```
pso_riego_python_clean/
├─ data/
│  ├─ parcelas.csv         # datos de ejemplo
│  └─ bbox.geojson         # polígono del área de estudio (WGS84)
├─ src/
│  ├─ features.py          # generación de grilla, pesos y lectura de datos
│  ├─ pso_placement.py     # función de pérdida y utilidades PSO
│  ├─ viz.py               # visualización de resultados
├─ tests/
│  ├─ test_features.py
│  └─ test_objective.py
├─ notebooks/
│  └─ (opcional)
├─ requirements.txt
└─ run_pso.py              # script CLI para ejecutar el optimizador
```

## Uso rápido

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

python run_pso.py --k 6 --iters 120 --particles 40   --csv data/parcelas.csv --bbox data/bbox.geojson   --cell 50 --lc 0.1 --cap 100 --out sensors.geojson
```

Luego, para visualizar:

```python
from src.viz import plot_solution
import geopandas as gpd
from src.features import grid_from_bbox, load_points, weight_map

grid = grid_from_bbox("data/bbox.geojson", cell_size=50)
pts = load_points("data/parcelas.csv")
w = weight_map(pts, grid)
plot_solution("data/bbox.geojson", "sensors.geojson", grid, w)
```

## Créditos
Autores: **Omar Bermejo Osuna y Diego Alberto Araujo** — Módulo III
