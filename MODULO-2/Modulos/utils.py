
# -*- coding: utf-8 -*-
"""Funciones utilitarias genéricas."""

import os


def verificar_archivo(ruta):
    """Verifica si existe un archivo."""
    if not os.path.exists(ruta):
        raise FileNotFoundError(f"Archivo no encontrado: {ruta}")
    return True
