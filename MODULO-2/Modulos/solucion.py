# -*- coding: utf-8 -*-
"""
Módulo de cálculo de solución logística y exportación a Excel.
"""

import numpy as np
import pandas as pd
import os


def calcular_solucion(tiendas, D, C, data_path=None):
    """
    Calcula la asignación de tiendas a centros, rutas y rangos.
    Genera también un archivo Excel con los resultados.
    """

    print("🔄 Calculando solución optimizada...")

    # --- Identificar nodos ---
    n_centros = sum(tiendas['Tipo'].str.contains("Centro", case=False))
    n_tiendas = sum(tiendas['Tipo'].str.contains("Tienda", case=False))

    # --- Simulación de asignaciones (ejemplo, reemplaza por tu algoritmo real) ---
    assignments = {
        c: list(range(c * (n_tiendas // n_centros),
                      (c + 1) * (n_tiendas // n_centros)))
        for c in range(n_centros)
    }

    # --- Simulación de rutas ---
    solutions = {
        c: {"route": [c] + assignments[c] + [c]} for c in range(n_centros)
    }

    # --- Simulación de rangos (en km) ---
    rings_upper = {c: [5, 10, 15] for c in range(n_centros)}

    print("✅ Solución generada exitosamente.")

    # --- Crear DataFrames para exportar ---
    df_asignaciones = []
    for centro, tiendas_ids in assignments.items():
        for t in tiendas_ids:
            nombre_tienda = tiendas.iloc[t][
                "Nombre"] if "Nombre" in tiendas.columns else f"Tienda_{t+1}"
            df_asignaciones.append({
                "Centro_ID": centro + 1,
                "Tienda_ID": t + 1,
                "Nombre_Tienda": nombre_tienda
            })
    df_asignaciones = pd.DataFrame(df_asignaciones)

    df_rutas = []
    for centro, data in solutions.items():
        ruta = data["route"]
        for orden, nodo in enumerate(ruta):
            df_rutas.append({
                "Centro_ID": centro + 1,
                "Orden": orden + 1,
                "Nodo_ID": nodo + 1
            })
    df_rutas = pd.DataFrame(df_rutas)

    df_rangos = []
    for centro, rangos in rings_upper.items():
        for r in rangos:
            df_rangos.append({
                "Centro_ID": centro + 1,
                "Rango_km": r
            })
    df_rangos = pd.DataFrame(df_rangos)

    # --- Guardar Excel ---
    if data_path:
        output_path = os.path.join(data_path, "resultado_solucion.xlsx")
        with pd.ExcelWriter(output_path, engine="openpyxl") as writer:
            df_asignaciones.to_excel(
                writer, index=False, sheet_name="Asignaciones")
            df_rutas.to_excel(writer, index=False, sheet_name="Rutas")
            df_rangos.to_excel(writer, index=False, sheet_name="Rangos")

        print(f"📘 Archivo Excel generado en:\n   {output_path}")

    return assignments, solutions, rings_upper
