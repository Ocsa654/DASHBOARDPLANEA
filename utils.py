import pandas as pd
import numpy as np

__all__ = [
    "normalizar_columnas",
    "calcular_porcentaje_satisfactorio",
    "obtener_mejor_estado",
    "obtener_peor_estado",
    "calcular_tendencia",
]

def normalizar_columnas(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza nombres de columnas eliminando acentos y caracteres especiales."""
    rename_dict = {}
    for col in df.columns:
        new_col = col
        for a, b in [
            ("Á", "A"),
            ("É", "E"),
            ("Í", "I"),
            ("Ó", "O"),
            ("Ú", "U"),
            ("á", "a"),
            ("é", "e"),
            ("í", "i"),
            ("ó", "o"),
            ("ú", "u"),
            ("Ñ", "N"),
            ("ñ", "n"),
        ]:
            new_col = new_col.replace(a, b)
        if new_col != col:
            rename_dict[col] = new_col
    return df.rename(columns=rename_dict) if rename_dict else df


def _buscar_columnas_por_nivel(df: pd.DataFrame, materia_keywords: list[str], nivel: str) -> str | None:
    """Devuelve el nombre de la columna que coincide con materia, nivel y porcentaje."""
    for col in df.columns:
        if any(k in col for k in materia_keywords) and nivel in col and "%" in col:
            return col
    return None


def calcular_porcentaje_satisfactorio(df: pd.DataFrame, tipo: str = "LENGUAJE") -> float:
    """Porcentaje promedio de estudiantes en niveles III y IV (satisfactorio)."""
    if df is None or df.empty:
        return 0.0
    if tipo == "LENGUAJE":
        keywords = ["LENGUAJE", "COMUNICACION"]
    else:  # MATEMATICAS
        keywords = ["MATEMATICAS", "MATEMÁTICAS"]
    nivel3_col = _buscar_columnas_por_nivel(df, keywords, "NIVEL III")
    nivel4_col = _buscar_columnas_por_nivel(df, keywords, "NIVEL IV")
    if nivel3_col and nivel4_col:
        return float(df[nivel3_col].mean() + df[nivel4_col].mean())
    # Si no hay columnas de porcentaje, usar siempre el promedio de CALIF LENGUAJE o CALIF MATEMATICAS
    calif_cols = [col for col in df.columns if "CALIF" in col and any(k in col for k in keywords)]
    if calif_cols:
        return float(df[calif_cols[0]].mean())
    return 0.0


def _obtener_col_entidad(df: pd.DataFrame) -> str | None:
    for col in ["ENTIDAD", "ESTADO", "ENTIDAD FEDERATIVA"]:
        if col in df.columns:
            return col
    return None


def obtener_mejor_estado(df: pd.DataFrame, tipo: str = "LENGUAJE") -> dict:
    """Estado con mayor porcentaje satisfactorio."""
    entidad_col = _obtener_col_entidad(df)
    if not entidad_col:
        return {"estado": "Desconocido", "valor": 0}
    resultados = [
        {
            "estado": entidad,
            "valor": calcular_porcentaje_satisfactorio(df[df[entidad_col] == entidad], tipo),
        }
        for entidad in df[entidad_col].unique()
    ]
    resultados.sort(key=lambda x: x["valor"], reverse=True)
    return resultados[0] if resultados else {"estado": "Desconocido", "valor": 0}


def obtener_peor_estado(df: pd.DataFrame, tipo: str = "LENGUAJE") -> dict:
    """Estado con menor porcentaje satisfactorio."""
    entidad_col = _obtener_col_entidad(df)
    if not entidad_col:
        return {"estado": "Desconocido", "valor": 0}
    resultados = [
        {
            "estado": entidad,
            "valor": calcular_porcentaje_satisfactorio(df[df[entidad_col] == entidad], tipo),
        }
        for entidad in df[entidad_col].unique()
    ]
    resultados.sort(key=lambda x: x["valor"])
    return resultados[0] if resultados else {"estado": "Desconocido", "valor": 0}


def calcular_tendencia(df_list: list[pd.DataFrame], años: list[int], tipo: str = "LENGUAJE") -> float:
    """Pendiente lineal de la evolución de porcentaje satisfactorio a lo largo de los años."""
    if not df_list or not años or len(df_list) != len(años):
        return 0.0
    y = np.array([calcular_porcentaje_satisfactorio(df, tipo) for df in df_list], dtype=float)
    x = np.array(años, dtype=float)
    var_x = np.var(x)
    if var_x == 0:
        return 0.0
    pendiente = np.cov(x, y)[0, 1] / var_x
    return float(pendiente)
