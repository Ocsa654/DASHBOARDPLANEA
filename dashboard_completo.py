import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import numpy as np
from utils import (
    normalizar_columnas,
    calcular_porcentaje_satisfactorio,
    obtener_mejor_estado,
    obtener_peor_estado,
    calcular_tendencia,
)

# Configuración de la página
st.set_page_config(
    page_title="Dashboard PLANEA Completo",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("Dashboard PLANEA - Análisis Completo")
st.markdown("---")

# Cachear la carga de datos para acelerar el dashboard
@st.cache_data(show_spinner=False)
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

# Estado de carga y selección
if 'df_2015' not in st.session_state:
    st.session_state.df_2015 = None
    st.session_state.df_2016 = None
    st.session_state.df_2017 = None
    st.session_state.df_2022 = None
    st.session_state.carga_completa = False

# Sidebar para opciones de carga
st.sidebar.header("Opciones de carga")
max_filas = st.sidebar.slider("Número máximo de filas a cargar", 500, 50000, 10000, step=1000)
cargar_todo = st.sidebar.checkbox("Cargar datos completos (puede tardar)", value=False)

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
    st.warning("Para ver el dashboard completo, activa la opción 'Cargar datos completos' en la barra lateral.")
    st.stop()

# Obtener los dataframes cargados
df_2015 = st.session_state.df_2015
df_2016 = st.session_state.df_2016
df_2017 = st.session_state.df_2017
df_2022 = st.session_state.df_2022

# Crear pestañas principales para el dashboard completo
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "KPIs Principales", 
    "Análisis por Año (2015-2017)", 
    "Análisis por Estado",
    "Datos 2022",
    "Tablas y Estadísticas"
])

# Pestaña 1: KPIs Principales
with tab1:
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
            
    # Gráficos de resumen para KPIs
    st.subheader("Gráficos de Resumen")
    
    # Datos para el gráfico de barras
    datos_resumen = []
    
    if df_2015 is not None:
        datos_resumen.append({
            "Año": 2015,
            "Lenguaje": calcular_porcentaje_satisfactorio(df_2015, "LENGUAJE"),
            "Matemáticas": calcular_porcentaje_satisfactorio(df_2015, "MATEMATICAS")
        })
    
    if df_2016 is not None:
        datos_resumen.append({
            "Año": 2016,
            "Lenguaje": calcular_porcentaje_satisfactorio(df_2016, "LENGUAJE"),
            "Matemáticas": calcular_porcentaje_satisfactorio(df_2016, "MATEMATICAS")
        })
    
    if df_2017 is not None:
        datos_resumen.append({
            "Año": 2017,
            "Lenguaje": calcular_porcentaje_satisfactorio(df_2017, "LENGUAJE"),
            "Matemáticas": calcular_porcentaje_satisfactorio(df_2017, "MATEMATICAS")
        })
    
    if datos_resumen:
        df_resumen = pd.DataFrame(datos_resumen)
        
        # Convertir a formato "largo" para plotly
        df_long = pd.melt(
            df_resumen,
            id_vars=["Año"],
            value_vars=["Lenguaje", "Matemáticas"],
            var_name="Materia",
            value_name="Porcentaje"
        )
        
        # Crear gráfico de barras agrupadas
        fig = px.bar(
            df_long,
            x="Año",
            y="Porcentaje",
            color="Materia",
            barmode="group",
            title="Porcentaje de estudiantes en niveles satisfactorios por año y materia",
            labels={"Porcentaje": "Porcentaje de estudiantes (%)"}
        )
        
        st.plotly_chart(fig, use_container_width=True)

# Importar y ejecutar código de las otras pestañas con manejo de codificación robusto

def _exec_tab(path: str):
    for enc in ("utf-8", "latin-1", "cp1252"):
        try:
            exec(open(path, encoding=enc).read(), globals())
            return
        except UnicodeDecodeError:
            continue
    st.error(f"No se pudo leer el archivo {path} con las codificaciones estándar.")

_exec_tab("dashboard_completo_tab2.py")
_exec_tab("dashboard_completo_tab3.py")
_exec_tab("dashboard_completo_tab4.py")
_exec_tab("dashboard_completo_tab5.py")
