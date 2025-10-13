
# Optimización de Rutas de Distribución con Recocido Simulado

Este proyecto implementa un sistema completo para **optimizar rutas de entrega y distribución** entre **Centros de Distribución (CDs)** y **Tiendas**, utilizando técnicas de **Recocido Simulado (Simulated Annealing)**, análisis geoespacial con **GeoPandas**, y visualización con **Contextily** y **Matplotlib**.

---

## Descripción General

El sistema permite:

- Cargar datos de tiendas y centros desde un archivo Excel.
- Calcular **asignaciones automáticas** de tiendas a su CD más eficiente, considerando límites de cobertura en kilómetros.
- Ejecutar una **optimización de rutas** por CD (modelo tipo TSP).
- Visualizar los resultados en mapas:
  -  Mapa general con todos los CDs, rutas y nodos.
  -  Mapas individuales por centro de distribución.

El objetivo es modelar un escenario realista de **logística y distribución** para identificar rutas óptimas, minimizar costos de combustible y reducir distancia total recorrida.

---

## Estructura del Proyecto

| Proyecto_Rutas/
│
├── main.py # Menú principal interactivo
├── Solucion.py # Cálculo de asignaciones y rutas (Simulated Annealing)
├── MapeoRutas.py # Módulo de visualización geográfica (GeoPandas + Matplotlib)
│
├── Datos/
│ ├── datos_distribucion_tiendas.xlsx # Coordenadas, tipo (CD o tienda) y nombres
│ ├── matriz_distancias.xlsx # Matriz de distancias (km)
│ └── matriz_costos_combustible.xlsx # Matriz de costos de combustible
│
├── mapas_resultado/
│ ├── mapa_completo.png # Mapa con todos los CDs y rutas
│ └── mapa_centro_X.png # Mapas individuales por CD
│
└── README.md # Este archivo


---

##  Requisitos

###  Librerías necesarias

Instala las dependencias con:

```bash
pip install pandas geopandas shapely contextily matplotlib tabulate numpy
