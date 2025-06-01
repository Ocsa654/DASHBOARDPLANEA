import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
from dashboard_kpi_parte1 import *  # Importar todas las funciones de la parte 1

# Sección de Visualizaciones
st.header("Visualizaciones de Tendencias")

# Crear pestañas para diferentes tipos de visualizaciones
tab1, tab2, tab3 = st.tabs(["Tendencias por Año", "Comparativa entre Estados", "Mapa de Calor"])

# Función para preparar datos de tendencia por año
def preparar_datos_tendencia_por_año():
    datos = []
    
    # Verificar qué años están disponibles
    años_disponibles = []
    df_años = []
    
    if st.session_state.df_2015 is not None:
        años_disponibles.append(2015)
        df_años.append(st.session_state.df_2015)
    
    if st.session_state.df_2016 is not None:
        años_disponibles.append(2016)
        df_años.append(st.session_state.df_2016)
    
    if st.session_state.df_2017 is not None:
        años_disponibles.append(2017)
        df_años.append(st.session_state.df_2017)
    
    # Para cada año, calcular los porcentajes por nivel
    for i, año in enumerate(años_disponibles):
        df = df_años[i]
        
        # Calcular porcentajes por nivel para Lenguaje
        for nivel in range(1, 5):
            col_nivel = None
            for col in df.columns:
                if ("LENGUAJE" in col or "COMUNICACION" in col) and f"NIVEL {nivel}" in col and "%" in col:
                    col_nivel = col
                    break
            
            if col_nivel:
                datos.append({
                    "Año": año,
                    "Materia": "Lenguaje",
                    "Nivel": f"Nivel {nivel}",
                    "Porcentaje": df[col_nivel].mean()
                })
        
        # Calcular porcentajes por nivel para Matemáticas
        for nivel in range(1, 5):
            col_nivel = None
            for col in df.columns:
                if ("MATEMATICAS" in col or "MATEMÁTICAS" in col) and f"NIVEL {nivel}" in col and "%" in col:
                    col_nivel = col
                    break
            
            if col_nivel:
                datos.append({
                    "Año": año,
                    "Materia": "Matemáticas",
                    "Nivel": f"Nivel {nivel}",
                    "Porcentaje": df[col_nivel].mean()
                })
    
    return pd.DataFrame(datos) if datos else None

# Función para preparar datos por estado
def preparar_datos_por_estado(año, materia):
    df = None
    
    if año == 2015:
        df = st.session_state.df_2015
    elif año == 2016:
        df = st.session_state.df_2016
    elif año == 2017:
        df = st.session_state.df_2017
    
    if df is None:
        return None
    
    # Buscar columna de entidad
    entidad_col = None
    for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
        if col in df.columns:
            entidad_col = col
            break
    
    if not entidad_col:
        return None
    
    # Preparar datos por estado
    datos = []
    
    for entidad in df[entidad_col].unique():
        df_entidad = df[df[entidad_col] == entidad]
        valor = calcular_porcentaje_satisfactorio(df_entidad, materia)
        
        # Buscar columnas de nivel III y IV
        if materia == "LENGUAJE":
            for nivel in range(1, 5):
                col_nivel = None
                for col in df.columns:
                    if ("LENGUAJE" in col or "COMUNICACION" in col) and f"NIVEL {nivel}" in col and "%" in col:
                        col_nivel = col
                        break
                
                if col_nivel:
                    datos.append({
                        "Entidad": entidad,
                        "Nivel": f"Nivel {nivel}",
                        "Porcentaje": df_entidad[col_nivel].mean()
                    })
        else:  # MATEMATICAS
            for nivel in range(1, 5):
                col_nivel = None
                for col in df.columns:
                    if ("MATEMATICAS" in col or "MATEMÁTICAS" in col) and f"NIVEL {nivel}" in col and "%" in col:
                        col_nivel = col
                        break
                
                if col_nivel:
                    datos.append({
                        "Entidad": entidad,
                        "Nivel": f"Nivel {nivel}",
                        "Porcentaje": df_entidad[col_nivel].mean()
                    })
    
    return pd.DataFrame(datos) if datos else None

# Función para preparar datos del mapa de calor
def preparar_datos_mapa_calor(materia):
    datos = []
    
    # Verificar qué años están disponibles
    años_disponibles = []
    df_años = []
    
    if st.session_state.df_2015 is not None:
        años_disponibles.append(2015)
        df_años.append(st.session_state.df_2015)
    
    if st.session_state.df_2016 is not None:
        años_disponibles.append(2016)
        df_años.append(st.session_state.df_2016)
    
    if st.session_state.df_2017 is not None:
        años_disponibles.append(2017)
        df_años.append(st.session_state.df_2017)
    
    # Para cada año, calcular los porcentajes satisfactorios por entidad
    for i, año in enumerate(años_disponibles):
        df = df_años[i]
        
        # Buscar columna de entidad
        entidad_col = None
        for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
            if col in df.columns:
                entidad_col = col
                break
        
        if entidad_col:
            for entidad in df[entidad_col].unique():
                df_entidad = df[df[entidad_col] == entidad]
                valor = calcular_porcentaje_satisfactorio(df_entidad, materia)
                
                datos.append({
                    "Año": año,
                    "Entidad": entidad,
                    "Porcentaje": valor
                })
    
    return pd.DataFrame(datos) if datos else None

# Pestaña 1: Tendencias por Año
with tab1:
    # Preparar datos
    df_tendencia = preparar_datos_tendencia_por_año()
    
    if df_tendencia is not None:
        # Selector de materia
        materia = st.radio("Selecciona materia:", ["Lenguaje", "Matemáticas"], horizontal=True, key="materia_tendencia")
        
        # Filtrar por materia seleccionada
        df_filtrado = df_tendencia[df_tendencia["Materia"] == materia]
        
        # Crear gráfico de línea
        fig = px.line(
            df_filtrado,
            x="Año",
            y="Porcentaje",
            color="Nivel",
            markers=True,
            title=f"Evolución de niveles de desempeño en {materia} (2015-2017)",
            labels={"Porcentaje": "Porcentaje de estudiantes (%)"}
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar tendencia de niveles satisfactorios (III y IV)
        st.subheader(f"Tendencia de niveles satisfactorios en {materia}")
        
        # Filtrar solo niveles III y IV
        df_satisfactorios = df_filtrado[df_filtrado["Nivel"].isin(["Nivel 3", "Nivel 4", "Nivel III", "Nivel IV"])]
        
        # Sumar porcentajes por año
        df_suma = df_satisfactorios.groupby("Año")["Porcentaje"].sum().reset_index()
        
        # Crear gráfico de barras
        fig = px.bar(
            df_suma,
            x="Año",
            y="Porcentaje",
            title=f"Porcentaje de estudiantes en niveles satisfactorios (III y IV) - {materia}",
            labels={"Porcentaje": "Porcentaje de estudiantes (%)"},
            color_discrete_sequence=["#1f77b4" if materia == "Lenguaje" else "#ff7f0e"]
        )
        
        # Añadir línea de tendencia
        fig.add_trace(
            go.Scatter(
                x=df_suma["Año"],
                y=df_suma["Porcentaje"],
                mode='lines+markers',
                line=dict(color='red', width=2, dash='dash'),
                name='Tendencia'
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No hay suficientes datos para mostrar tendencias por año.")

# Pestaña 2: Comparativa entre Estados
with tab2:
    # Selector de año y materia
    col1, col2 = st.columns(2)
    
    with col1:
        año_seleccionado = st.selectbox(
            "Selecciona año:",
            [2015, 2016, 2017],
            index=2  # Por defecto, mostrar 2017
        )
    
    with col2:
        materia_seleccionada = st.selectbox(
            "Selecciona materia:",
            ["LENGUAJE", "MATEMATICAS"],
            format_func=lambda x: "Lenguaje" if x == "LENGUAJE" else "Matemáticas"
        )
    
    # Preparar datos por estado
    df_estados = preparar_datos_por_estado(año_seleccionado, materia_seleccionada)
    
    if df_estados is not None:
        # Calcular porcentaje satisfactorio por entidad
        df_satisfactorios = df_estados[df_estados["Nivel"].isin(["Nivel 3", "Nivel 4", "Nivel III", "Nivel IV"])]
        df_suma = df_satisfactorios.groupby("Entidad")["Porcentaje"].sum().reset_index()
        df_suma = df_suma.sort_values("Porcentaje", ascending=False)
        
        # Crear gráfico de barras
        titulo = "Lenguaje" if materia_seleccionada == "LENGUAJE" else "Matemáticas"
        fig = px.bar(
            df_suma,
            x="Porcentaje",
            y="Entidad",
            title=f"Porcentaje de estudiantes en niveles satisfactorios por entidad - {titulo} ({año_seleccionado})",
            labels={"Porcentaje": "Porcentaje de estudiantes (%)", "Entidad": "Entidad"},
            color="Porcentaje",
            color_continuous_scale="Viridis",
            orientation='h'
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar distribución por niveles para la entidad seleccionada
        st.subheader("Distribución por niveles para una entidad específica")
        
        entidad_seleccionada = st.selectbox(
            "Selecciona una entidad:",
            df_suma["Entidad"].unique()
        )
        
        # Filtrar datos para la entidad seleccionada
        df_entidad = df_estados[df_estados["Entidad"] == entidad_seleccionada]
        
        # Crear gráfico de pastel
        fig = px.pie(
            df_entidad,
            values="Porcentaje",
            names="Nivel",
            title=f"Distribución por niveles en {entidad_seleccionada} - {titulo} ({año_seleccionado})",
            hole=0.4
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info(f"No hay datos disponibles para el año {año_seleccionado}.")

# Pestaña 3: Mapa de Calor
with tab3:
    # Selector de materia
    materia_mapa = st.radio(
        "Selecciona materia para el mapa de calor:",
        ["LENGUAJE", "MATEMATICAS"],
        format_func=lambda x: "Lenguaje" if x == "LENGUAJE" else "Matemáticas",
        horizontal=True,
        key="materia_mapa"
    )
    
    # Preparar datos para el mapa de calor
    df_mapa = preparar_datos_mapa_calor(materia_mapa)
    
    if df_mapa is not None:
        # Crear tabla pivote para el mapa de calor
        df_pivot = df_mapa.pivot(index="Entidad", columns="Año", values="Porcentaje")
        
        # Ordenar por el último año disponible (generalmente 2017)
        ultimo_año = df_mapa["Año"].max()
        if ultimo_año in df_pivot.columns:
            df_pivot = df_pivot.sort_values(ultimo_año, ascending=False)
        
        # Crear mapa de calor
        titulo = "Lenguaje" if materia_mapa == "LENGUAJE" else "Matemáticas"
        fig = px.imshow(
            df_pivot,
            labels=dict(x="Año", y="Entidad", color="% en niveles III y IV"),
            title=f"Evolución del porcentaje de estudiantes en niveles satisfactorios por entidad - {titulo}",
            color_continuous_scale="RdYlGn",  # Rojo (bajo) a Verde (alto)
            text_auto='.1f'  # Mostrar valores con 1 decimal
        )
        
        # Personalizar mapa de calor
        fig.update_layout(
            height=800,  # Mayor altura para mostrar todas las entidades
            xaxis=dict(side="top")  # Años en la parte superior
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calcular y mostrar las entidades con mayor mejora
        if len(df_pivot.columns) > 1:
            primer_año = df_pivot.columns.min()
            ultimo_año = df_pivot.columns.max()
            
            # Calcular diferencia entre primer y último año
            df_pivot["Cambio"] = df_pivot[ultimo_año] - df_pivot[primer_año]
            
            # Ordenar por cambio
            df_mejora = df_pivot.sort_values("Cambio", ascending=False).reset_index()
            
            # Mostrar top 5 de mejora y deterioro
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Top 5 entidades con mayor mejora")
                
                df_top_mejora = df_mejora.head(5)[["Entidad", "Cambio"]].copy()
                df_top_mejora["Cambio"] = df_top_mejora["Cambio"].round(1).astype(str) + "%"
                
                st.table(df_top_mejora)
            
            with col2:
                st.subheader("Top 5 entidades con mayor deterioro")
                
                df_top_deterioro = df_mejora.tail(5)[["Entidad", "Cambio"]].sort_values("Cambio").copy()
                df_top_deterioro["Cambio"] = df_top_deterioro["Cambio"].round(1).astype(str) + "%"
                
                st.table(df_top_deterioro)
    else:
        st.info("No hay suficientes datos para generar el mapa de calor.")
