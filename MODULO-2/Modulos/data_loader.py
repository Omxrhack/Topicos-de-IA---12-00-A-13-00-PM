# -*- coding: utf-8 -*-
"""Carga de datos de entrada para el modelo de distribución."""

import os
import pandas as pd


def cargar_datos(data_path: str):
    """
    Carga los tres archivos principales:
    - datos_distribucion_tiendas.xlsx
    - matriz_distancias.xlsx
    - matriz_costos_combustible.xlsx

    Devuelve:
    tiendas (DataFrame), D (numpy.ndarray), C (numpy.ndarray)
    """
    try:
        tiendas = pd.read_excel(os.path.join(
            data_path, "datos_distribucion_tiendas.xlsx"))
        D = pd.read_excel(os.path.join(
            data_path, "matriz_distancias.xlsx")).values.astype(float)
        C = pd.read_excel(os.path.join(
            data_path, "matriz_costos_combustible.xlsx")).values.astype(float)

        print("✅ Datos cargados correctamente.")
        return tiendas, D, C

    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        raise
