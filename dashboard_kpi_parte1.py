import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Dashboard PLANEA KPIs",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("Dashboard PLANEA - Indicadores Clave")
st.markdown("---")

# Función para normalizar nombres de columnas
def normalizar_columnas(df):
    rename_dict = {}
    for col in df.columns:
        # Crear versión normalizada (sin acentos)
        new_col = col
        for a, b in [('Á', 'A'), ('É', 'E'), ('Í', 'I'), ('Ó', 'O'), ('Ú', 'U'),
                    ('á', 'a'), ('é', 'e'), ('í', 'i'), ('ó', 'o'), ('ú', 'u'),
                    ('Ñ', 'N'), ('ñ', 'n')]:
            new_col = new_col.replace(a, b)
        
        if new_col != col:
            rename_dict[col] = new_col
    
    if rename_dict:
        return df.rename(columns=rename_dict)
    return df

# Funciones auxiliares para calcular KPIs
def calcular_porcentaje_satisfactorio(df, tipo="LENGUAJE"):
    """Calcula el porcentaje de estudiantes en niveles satisfactorios (III y IV)"""
    # Buscar columnas de nivel III y IV para el tipo especificado (lenguaje o matemáticas)
    nivel3_col = None
    nivel4_col = None
    
    if tipo == "LENGUAJE":
        for col in df.columns:
            if ("LENGUAJE" in col or "COMUNICACION" in col) and "NIVEL III" in col and "%" in col:
                nivel3_col = col
            elif ("LENGUAJE" in col or "COMUNICACION" in col) and "NIVEL IV" in col and "%" in col:
                nivel4_col = col
    else:  # MATEMATICAS
        for col in df.columns:
            if ("MATEMATICAS" in col or "MATEMÁTICAS" in col) and "NIVEL III" in col and "%" in col:
                nivel3_col = col
            elif ("MATEMATICAS" in col or "MATEMÁTICAS" in col) and "NIVEL IV" in col and "%" in col:
                nivel4_col = col
    
    # Si encontramos ambas columnas, calcular el promedio
    if nivel3_col and nivel4_col:
        return df[nivel3_col].mean() + df[nivel4_col].mean()
    
    return 0  # Valor por defecto si no encontramos las columnas

def obtener_mejor_estado(df, tipo="LENGUAJE"):
    """Obtiene el estado con mejor desempeño"""
    resultados = []
    
    # Buscar columna de entidad
    entidad_col = None
    for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
        if col in df.columns:
            entidad_col = col
            break
    
    if not entidad_col:
        return {"estado": "Desconocido", "valor": 0}
    
    # Agrupar por entidad y calcular porcentaje satisfactorio
    for entidad in df[entidad_col].unique():
        df_entidad = df[df[entidad_col] == entidad]
        valor = calcular_porcentaje_satisfactorio(df_entidad, tipo)
        resultados.append({"estado": entidad, "valor": valor})
    
    # Ordenar y obtener el mejor
    resultados = sorted(resultados, key=lambda x: x["valor"], reverse=True)
    
    if resultados:
        return resultados[0]
    
    return {"estado": "Desconocido", "valor": 0}

def obtener_peor_estado(df, tipo="LENGUAJE"):
    """Obtiene el estado con peor desempeño"""
    resultados = []
    
    # Buscar columna de entidad
    entidad_col = None
    for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
        if col in df.columns:
            entidad_col = col
            break
    
    if not entidad_col:
        return {"estado": "Desconocido", "valor": 0}
    
    # Agrupar por entidad y calcular porcentaje satisfactorio
    for entidad in df[entidad_col].unique():
        df_entidad = df[df[entidad_col] == entidad]
        valor = calcular_porcentaje_satisfactorio(df_entidad, tipo)
        resultados.append({"estado": entidad, "valor": valor})
    
    # Ordenar y obtener el peor
    resultados = sorted(resultados, key=lambda x: x["valor"])
    
    if resultados:
        return resultados[0]
    
    return {"estado": "Desconocido", "valor": 0}

def calcular_tendencia(df_list, años, tipo="LENGUAJE"):
    """Calcula la tendencia a lo largo de los años"""
    if not df_list or not años or len(df_list) != len(años):
        return 0
    
    valores = []
    for df in df_list:
        valores.append(calcular_porcentaje_satisfactorio(df, tipo))
    
    # Si solo tenemos un año, no podemos calcular tendencia
    if len(valores) <= 1:
        return 0
    
    # Calcular pendiente usando regresión lineal simple
    x = np.array(años)
    y = np.array(valores)
    
    # Evitar división por cero
    if np.var(x) == 0:
        return 0
    
    # Pendiente de la regresión lineal
    pendiente = np.cov(x, y)[0, 1] / np.var(x)
    return pendiente

# Estado de carga y selección
if 'df_2015' not in st.session_state:
    st.session_state.df_2015 = None
    st.session_state.df_2016 = None
    st.session_state.df_2017 = None
    st.session_state.df_2022 = None
    st.session_state.carga_completa = False

# Sidebar para opciones de carga
st.sidebar.header("Opciones de carga")
max_filas = st.sidebar.slider("Número máximo de filas a cargar", 100, 5000, 500, step=100)
cargar_todo = st.sidebar.checkbox("Cargar datos completos (puede tardar)", value=False)

# Función para cargar datos por año
def cargar_datos_por_año(archivo, año, max_filas=500):
    try:
        with st.spinner(f'Cargando datos {año}...'):
            df = pd.read_excel(archivo, nrows=max_filas)
            df = normalizar_columnas(df)
            
            # Filtrar por año si es necesario
            año_col = None
            for col in ['ANO', 'ANIO', 'AÑO', 'A?O', 'YEAR']:
                if col in df.columns:
                    año_col = col
                    break
            
            if año_col and año:
                df = df[df[año_col] == año]
            
            return df
    except Exception as e:
        st.error(f"Error al cargar datos {año}: {str(e)}")
        return None

# Cargar datos cuando se activa la opción
if cargar_todo and not st.session_state.carga_completa:
    # Cargar datos 2015-2017
    st.session_state.df_2015 = cargar_datos_por_año('DATOS2015-2017.xlsx', 2015, max_filas)
    st.session_state.df_2016 = cargar_datos_por_año('DATOS2015-2017.xlsx', 2016, max_filas)
    st.session_state.df_2017 = cargar_datos_por_año('DATOS2015-2017.xlsx', 2017, max_filas)
    
    # Cargar datos 2022
    st.session_state.df_2022 = cargar_datos_por_año('DATOS2022.xlsx', None, max_filas)
    
    st.session_state.carga_completa = True
    st.success("Datos cargados correctamente")

# Verificar si se han cargado los datos
if not st.session_state.carga_completa:
    st.warning("Para ver los KPIs, activa la opción 'Cargar datos completos' en la barra lateral.")
    st.stop()

# Obtener los dataframes cargados
df_2015 = st.session_state.df_2015
df_2016 = st.session_state.df_2016
df_2017 = st.session_state.df_2017
df_2022 = st.session_state.df_2022

# Aquí continuaremos con la implementación de los KPIs en las siguientes partes
