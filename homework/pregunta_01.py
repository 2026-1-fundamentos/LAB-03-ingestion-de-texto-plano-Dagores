"""
Escriba el codigo que ejecute la accion solicitada en cada pregunta.
"""

# pylint: disable=import-outside-toplevel

import os
import re

import pandas as pd


def pregunta_01():
    """
    Construya y retorne un dataframe de Pandas a partir del archivo
    'files/input/clusters_report.txt'. Los requierimientos son los siguientes:

    - El dataframe tiene la misma estructura que el archivo original.
    - Los nombres de las columnas deben ser en minusculas, reemplazando los
      espacios por guiones bajos.
    - Las palabras clave deben estar separadas por coma y con un solo
      espacio entre palabra y palabra.

    """
    path = os.path.join(os.path.dirname(__file__), "..", "files", "input", "clusters_report.txt")
    path = os.path.normpath(path)

    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    data = []
    parsing = False
    current = None

    record_re = re.compile(r"^\s*(\d+)\s+(\d+)\s+([0-9,]+)\s*%\s+(.*)$")

    for line in lines:
        if not parsing:
            if line.strip().startswith("---"):
                parsing = True
            continue

        if not line.strip():
            continue

        match = record_re.match(line)
        if match:
            if current is not None:
                data.append(current)

            cluster = int(match.group(1))
            cantidad = int(match.group(2))
            porcentaje_raw = match.group(3).replace(",", ".")
            porcentaje = float(porcentaje_raw)
            keywords = match.group(4).strip()
            current = {
                "Cluster": cluster,
                "Cantidad de palabras clave": cantidad,
                "Porcentaje de palabras clave": porcentaje,
                "Principales palabras clave": keywords,
            }
        else:
            if current is not None:
                current["Principales palabras clave"] += " " + line.strip()

    if current is not None:
        data.append(current)

    cleaned = []
    for item in data:
        keywords = item["Principales palabras clave"]
        keywords = re.sub(r"\s+", " ", keywords)
        keywords = re.sub(r"\s*,\s*", ", ", keywords)
        keywords = keywords.strip()
        if keywords.endswith("."):
            keywords = keywords[:-1]
        item["Principales palabras clave"] = keywords
        cleaned.append(item)

    df = pd.DataFrame(cleaned)
    df.columns = [col.lower().replace(" ", "_") for col in df.columns]
    return df
