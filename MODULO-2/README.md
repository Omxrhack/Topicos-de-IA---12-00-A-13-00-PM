# Optimización de Rutas de Distribución con Recocido Simulado

Este proyecto implementa un sistema completo para optimizar rutas de entrega y distribución entre Centros de Distribución (CDs) y Tiendas, utilizando técnicas de Recocido Simulado (Simulated Annealing), análisis geoespacial con GeoPandas y visualización con Contextily y Matplotlib.

## Descripción General

El sistema permite:

- Cargar datos de tiendas y centros desde un archivo Excel.
- Calcular asignaciones automáticas de tiendas a su CD más eficiente, considerando límites de cobertura en kilómetros.
- Ejecutar una optimización de rutas por CD (modelo tipo TSP).
- Visualizar los resultados en mapas:
  - Mapa general con todos los CDs, rutas y nodos.
  - Mapas individuales por centro de distribución.

El objetivo es modelar un escenario realista de logística y distribución para identificar rutas óptimas, minimizar costos de combustible y reducir distancia total recorrida.

## Estructura del Proyecto

```
Proyecto_Rutas/
│
├── main.py                         # Menú principal interactivo
├── Solucion.py                     # Cálculo de asignaciones y rutas (Simulated Annealing)
├── MapeoRutas.py                   # Módulo de visualización geográfica (GeoPandas + Matplotlib)
│
├── Datos/
│   ├── datos_distribucion_tiendas.xlsx       # Coordenadas, tipo (CD o tienda) y nombres
│   ├── matriz_distancias.xlsx                # Matriz de distancias (km)
│   └── matriz_costos_combustible.xlsx        # Matriz de costos de combustible
│
├── mapas_resultado/
│   ├── mapa_completo.png                     # Mapa con todos los CDs y rutas
│   └── mapa_centro_X.png                     # Mapas individuales por CD
│
└── README.md                                 # Este archivo
```

## Requisitos

### Librerías necesarias

Instala las dependencias con:

```bash
pip install pandas geopandas shapely contextily matplotlib tabulate numpy
```

Asegúrate de tener también `fiona` y `pyproj` correctamente instalados (se instalan automáticamente con GeoPandas).

## Ejecución

### 1. Modo manual (por script)

```python
import pandas as pd
from Solucion import calcular_solucion
from MapeoRutas import plot_rangos_rutas_nodos, plot_single_center

# Carga de datos
tiendas = pd.read_excel("Datos/datos_distribucion_tiendas.xlsx")
D = pd.read_excel("Datos/matriz_distancias.xlsx").values.astype(float)
C = pd.read_excel("Datos/matriz_costos_combustible.xlsx").values.astype(float)

# Cálculo de asignaciones y rutas óptimas
assignments, solutions, rings_upper = calcular_solucion(tiendas, D, C)

# Mapa general
plot_rangos_rutas_nodos(tiendas, assignments, solutions, rings_upper, save_path="mapas_resultado/mapa_completo.png")

# Mapa individual por centro
plot_single_center(tiendas, 0, assignments, solutions, rings_upper, save_path="mapas_resultado/mapa_centro_1.png")
```

### 2. Modo interactivo (main.py)

El archivo `main.py` incluye un menú que permite:

| Opción | Acción |
|:------:|:--------|
| 1 | Mostrar mapa sin rutas |
| 2 | Calcular solución y mostrar tabla |
| 3 | Generar mapa con rangos, rutas y nodos |
| 4 | Mostrar mapa individual de un centro |

Ejecuta con:

```bash
python main.py
```

## Parámetros Importantes

Dentro de `Solucion.py` puedes ajustar los siguientes parámetros globales:

| Parámetro | Descripción | Valor por defecto |
|------------|-------------|-------------------|
| ALPHA | Peso relativo entre distancia y combustible | 0.4 |
| PER_CENTRO_DISTRIBUCION | Rango máximo de cobertura (km) | [3, 6, 9] |
| SA_T0 | Temperatura inicial del recocido simulado | 600.0 |
| SA_COOL | Factor de enfriamiento | 0.9993 |
| SA_ITERS | Iteraciones máximas del algoritmo | 150000 |

## Resultados

En consola se muestra una tabla como la siguiente:

```
=== RESULTADOS POR CENTRO ===
+---------------------------+--------------------+------------------------+---------------------+------------------+--------------------------------------------------------------+
| Centro                    | Tiendas_servicio   | Distancia_total (km)   | Costo_combustible   | Valor_objetivo   | Ruta                                                         |
+---------------------------+--------------------+------------------------+---------------------+------------------+--------------------------------------------------------------+
| Centro de Distribución 1  | 5                  | 13.7                   | 2.06                | 9.04             | CD1 → T38 → T45 → T30 → T49 → T34 → CD1                      |
| Centro de Distribución 2  | 6                  | 16.58                  | 2.49                | 10.94            | CD2 → T1 → T69 → T47 → T81 → T74 → T6 → CD2                  |
+---------------------------+--------------------+------------------------+---------------------+------------------+--------------------------------------------------------------+
```

Los mapas generados muestran:

- Los Centros de Distribución en rojo.
- Las Tiendas en distintos colores según su CD asignado.
- Los anillos de cobertura (rango máximo de entrega).
- Las rutas optimizadas en líneas de color.

## Créditos

Proyecto desarrollado por **Omar Bermejo Osuna y Diego Araujo**  



