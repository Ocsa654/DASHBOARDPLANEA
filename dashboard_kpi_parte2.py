import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
from dashboard_kpi_parte1 import *  # Importar todas las funciones de la parte 1

# Sección de KPIs principales
st.header("KPIs Principales")

# KPIs de Lenguaje
st.subheader("Indicadores de Lenguaje y Comunicación")

# Crear fila de métricas para Lenguaje
col1, col2, col3 = st.columns(3)

# Porcentaje satisfactorio 2015 vs 2017 (Lenguaje)
with col1:
    if df_2015 is not None and df_2017 is not None:
        valor_2015 = calcular_porcentaje_satisfactorio(df_2015, "LENGUAJE")
        valor_2017 = calcular_porcentaje_satisfactorio(df_2017, "LENGUAJE")
        cambio = valor_2017 - valor_2015
        
        st.metric(
            label="Cambio en niveles satisfactorios (Lenguaje)",
            value=f"{valor_2017:.1f}%",
            delta=f"{cambio:.1f}%",
            help="Cambio en el porcentaje de estudiantes en niveles III y IV entre 2015 y 2017"
        )
    else:
        st.metric(
            label="Cambio en niveles satisfactorios (Lenguaje)",
            value="N/A",
            delta=None
        )

# Mejor y peor estado 2017 (Lenguaje)
with col2:
    if df_2017 is not None:
        mejor_estado = obtener_mejor_estado(df_2017, "LENGUAJE")
        peor_estado = obtener_peor_estado(df_2017, "LENGUAJE")
        brecha = mejor_estado["valor"] - peor_estado["valor"]
        
        st.metric(
            label=f"Brecha entre estados 2017 (Lenguaje)",
            value=f"{brecha:.1f}%",
            delta=None,
            help=f"Diferencia entre {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%) y {peor_estado['estado']} ({peor_estado['valor']:.1f}%)"
        )
        
        # Mostrar mejor y peor estado
        st.caption(f"Mejor: {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%)")
        st.caption(f"Peor: {peor_estado['estado']} ({peor_estado['valor']:.1f}%)")
    else:
        st.metric(
            label="Brecha entre estados 2017 (Lenguaje)",
            value="N/A",
            delta=None
        )

# Tendencia 2015-2017 (Lenguaje)
with col3:
    if df_2015 is not None and df_2016 is not None and df_2017 is not None:
        tendencia = calcular_tendencia(
            [df_2015, df_2016, df_2017],
            [2015, 2016, 2017],
            "LENGUAJE"
        )
        
        st.metric(
            label="Tendencia 2015-2017 (Lenguaje)",
            value=f"{tendencia:.2f}%/año",
            delta=f"{tendencia:.2f}%",
            delta_color="normal",
            help="Cambio promedio anual en el porcentaje de estudiantes en niveles satisfactorios"
        )
    else:
        st.metric(
            label="Tendencia 2015-2017 (Lenguaje)",
            value="N/A",
            delta=None
        )

st.markdown("---")

# KPIs de Matemáticas
st.subheader("Indicadores de Matemáticas")

# Crear fila de métricas para Matemáticas
col1, col2, col3 = st.columns(3)

# Porcentaje satisfactorio 2015 vs 2017 (Matemáticas)
with col1:
    if df_2015 is not None and df_2017 is not None:
        valor_2015 = calcular_porcentaje_satisfactorio(df_2015, "MATEMATICAS")
        valor_2017 = calcular_porcentaje_satisfactorio(df_2017, "MATEMATICAS")
        cambio = valor_2017 - valor_2015
        
        st.metric(
            label="Cambio en niveles satisfactorios (Matemáticas)",
            value=f"{valor_2017:.1f}%",
            delta=f"{cambio:.1f}%",
            help="Cambio en el porcentaje de estudiantes en niveles III y IV entre 2015 y 2017"
        )
    else:
        st.metric(
            label="Cambio en niveles satisfactorios (Matemáticas)",
            value="N/A",
            delta=None
        )

# Mejor y peor estado 2017 (Matemáticas)
with col2:
    if df_2017 is not None:
        mejor_estado = obtener_mejor_estado(df_2017, "MATEMATICAS")
        peor_estado = obtener_peor_estado(df_2017, "MATEMATICAS")
        brecha = mejor_estado["valor"] - peor_estado["valor"]
        
        st.metric(
            label=f"Brecha entre estados 2017 (Matemáticas)",
            value=f"{brecha:.1f}%",
            delta=None,
            help=f"Diferencia entre {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%) y {peor_estado['estado']} ({peor_estado['valor']:.1f}%)"
        )
        
        # Mostrar mejor y peor estado
        st.caption(f"Mejor: {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%)")
        st.caption(f"Peor: {peor_estado['estado']} ({peor_estado['valor']:.1f}%)")
    else:
        st.metric(
            label="Brecha entre estados 2017 (Matemáticas)",
            value="N/A",
            delta=None
        )

# Tendencia 2015-2017 (Matemáticas)
with col3:
    if df_2015 is not None and df_2016 is not None and df_2017 is not None:
        tendencia = calcular_tendencia(
            [df_2015, df_2016, df_2017],
            [2015, 2016, 2017],
            "MATEMATICAS"
        )
        
        st.metric(
            label="Tendencia 2015-2017 (Matemáticas)",
            value=f"{tendencia:.2f}%/año",
            delta=f"{tendencia:.2f}%",
            delta_color="normal",
            help="Cambio promedio anual en el porcentaje de estudiantes en niveles satisfactorios"
        )
    else:
        st.metric(
            label="Tendencia 2015-2017 (Matemáticas)",
            value="N/A",
            delta=None
        )

st.markdown("---")

# Comparativa 2022 vs 2017
st.subheader("Comparativa 2022 vs 2017")

# Función para buscar calificación promedio en df_2022
def obtener_calificacion_promedio(df, tipo="LENGUAJE"):
    cal_col = None
    
    if tipo == "LENGUAJE":
        for col in df.columns:
            if "CALIF" in col and ("LENGUAJE" in col or "COMUNICACION" in col):
                cal_col = col
                break
    else:  # MATEMATICAS
        for col in df.columns:
            if "CALIF" in col and ("MATEMATICAS" in col or "MATEMÁTICAS" in col):
                cal_col = col
                break
    
    if cal_col:
        return df[cal_col].mean()
    
    return 0

# Crear fila de métricas para comparativa 2022 vs 2017
col1, col2 = st.columns(2)

# Calificación promedio en Lenguaje 2022
with col1:
    if df_2022 is not None:
        prom_lenguaje_2022 = obtener_calificacion_promedio(df_2022, "LENGUAJE")
        
        st.metric(
            label="Calificación promedio Lenguaje 2022",
            value=f"{prom_lenguaje_2022:.1f}",
            delta=None,
            help="Calificación promedio en Lenguaje en la evaluación 2022"
        )
    else:
        st.metric(
            label="Calificación promedio Lenguaje 2022",
            value="N/A",
            delta=None
        )

# Calificación promedio en Matemáticas 2022
with col2:
    if df_2022 is not None:
        prom_matematicas_2022 = obtener_calificacion_promedio(df_2022, "MATEMATICAS")
        
        st.metric(
            label="Calificación promedio Matemáticas 2022",
            value=f"{prom_matematicas_2022:.1f}",
            delta=None,
            help="Calificación promedio en Matemáticas en la evaluación 2022"
        )
    else:
        st.metric(
            label="Calificación promedio Matemáticas 2022",
            value="N/A",
            delta=None
        )
