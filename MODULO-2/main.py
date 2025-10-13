# -*- coding: utf-8 -*-
"""
MAIN interactivo para distribución logística.
Opciones:
1) Mapa sin rutas
2) Calcular solución y generar Excel
3) Mapa con rangos y rutas optimizadas
4) Mapa de un centro específico
0) Salir
"""

import os
import pandas as pd
from shapely.geometry import Point
import geopandas as gpd
import matplotlib.pyplot as plt
import contextily as cx

# Importar módulos del proyecto
from Modulos.solucion import calcular_solucion
from Modulos.visualizacion import plot_rangos_rutas_nodos, plot_single_center


# === FUNCIÓN DE MAPA SIMPLE ===
def mostrar_mapa_simple(tiendas):
    """Mapa simple de centros y tiendas con nodos (sin rutas)."""
    geometry = [Point(xy) for xy in zip(
        tiendas['Longitud_WGS84'], tiendas['Latitud_WGS84'])]
    gdf = gpd.GeoDataFrame(tiendas, geometry=geometry, crs="EPSG:4326")
    gdf_wm = gdf.to_crs(epsg=3857)

    centros_wm = gdf_wm[gdf_wm['Tipo'].str.contains("Centro", case=False)]
    tiendas_wm = gdf_wm[gdf_wm['Tipo'].str.contains("Tienda", case=False)]

    fig, ax = plt.subplots(figsize=(12, 12))
    tiendas_wm.plot(ax=ax, color="royalblue", markersize=40,
                    alpha=0.8, label="Tiendas")
    centros_wm.plot(ax=ax, color="red", markersize=60,
                    edgecolor="black", label="Centros")

    for idx, row in gdf_wm.iterrows():
        ax.text(row.geometry.x, row.geometry.y, str(idx + 1),
                fontsize=7, color='black', ha='center', va='center')

    cx.add_basemap(ax, source=cx.providers.OpenStreetMap.Mapnik)
    ax.set_title("Mapa simple de Centros y Tiendas", fontsize=16)
    ax.legend()
    ax.set_axis_off()
    plt.show()


# === BLOQUE PRINCIPAL ===
if __name__ == "__main__":

    # 🔹 Ruta base de los datos
    DATA_PATH = "/Users/omarbermejoosuna/Desktop/PP2TIA/Datos"

    # 🔹 Cargar archivos base
    tiendas = pd.read_excel(os.path.join(
        DATA_PATH, "datos_distribucion_tiendas.xlsx"))
    D = pd.read_excel(os.path.join(
        DATA_PATH, "matriz_distancias.xlsx")).values.astype(float)
    C = pd.read_excel(os.path.join(
        DATA_PATH, "matriz_costos_combustible.xlsx")).values.astype(float)

    assignments = solutions = rings_upper = None

    # === MENÚ INTERACTIVO ===
    while True:
        print("\n=== MENÚ ===")
        print("1) Mapa simple (sin rutas)")
        print("2) Calcular solución y generar Excel")
        print("3) Mapa con rangos y rutas (todos los centros)")
        print("4) Mapa de un centro específico")
        print("0) Salir")

        opcion = input("Elige una opción: ")

        if opcion == "1":
            mostrar_mapa_simple(tiendas)

        elif opcion == "2":
            assignments, solutions, rings_upper = calcular_solucion(
                tiendas, D, C, data_path=DATA_PATH
            )

        elif opcion == "3":
            if assignments is None:
                print("⚠️ Primero calcula la solución con opción 2.")
            else:
                plot_rangos_rutas_nodos(
                    tiendas, assignments, solutions, rings_upper,
                    save_path=os.path.join(
                        DATA_PATH, "mapa_rangos_rutas_nodos.png")
                )

        elif opcion == "4":
            if assignments is None:
                print("⚠️ Primero calcula la solución con opción 2.")
            else:
                try:
                    centro_input = int(
                        input("Ingresa el ID del centro que quieres visualizar: "))
                    centro_id = centro_input - 1
                    if centro_id < 0 or centro_id >= len(tiendas[tiendas['Tipo'].str.contains("Centro", case=False)]):
                        print(
                            f"❌ Centro {centro_input} no existe. Los centros válidos son del 1 al 10.")
                    else:
                        plot_single_center(
                            tiendas, centro_id, assignments, solutions, rings_upper,
                            save_path=os.path.join(
                                DATA_PATH, f"mapa_centro_{centro_input}.png")
                        )
                except ValueError:
                    print("❌ Ingresa un número válido.")

        elif opcion == "0":
            print("👋 Saliendo del programa...")
            break

        else:
            print("Opción inválida, intenta nuevamente.")
