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

# Crear pestañas principales para el dashboard completo
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "KPIs Principales", 
    "Análisis por Año (2015-2017)", 
    "Análisis por Estado",
    "Datos 2022",
    "Tablas y Estadísticas"
])

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

# Crear pestañas principales para el dashboard completo
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "KPIs Principales", 
    "Análisis por Año (2015-2017)", 
    "Análisis por Estado",
    "Datos 2022",
    "Tablas y Estadísticas"
])

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
    
    # Obtener el dataframe del año seleccionado
    df_año = None
    if año_seleccionado == 2015:
        df_año = st.session_state.df_2015
    elif año_seleccionado == 2016:
        df_año = st.session_state.df_2016
    elif año_seleccionado == 2017:
        df_año = st.session_state.df_2017
    
    if df_año is not None:
        # Buscar columna de entidad
        entidad_col = None
        for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
            if col in df_año.columns:
                entidad_col = col
                break
        
        if entidad_col:
            # Preparar datos para la gráfica
            datos_estados = []
            
            for entidad in df_año[entidad_col].unique():
                df_entidad = df_año[df_año[entidad_col] == entidad]
                valor = calcular_porcentaje_satisfactorio(df_entidad, materia_seleccionada)
                
                datos_estados.append({
                    "Entidad": entidad,
                    "Porcentaje": valor
                })
            
            if datos_estados:
                df_estados = pd.DataFrame(datos_estados)
                df_estados = df_estados.sort_values("Porcentaje", ascending=False)
                
                # Crear gráfico de barras horizontales
                titulo = "Lenguaje" if materia_seleccionada == "LENGUAJE" else "Matemáticas"
                fig = px.bar(
                    df_estados,
                    x="Porcentaje",
                    y="Entidad",
                    title=f"Porcentaje de estudiantes en niveles satisfactorios por entidad - {titulo} ({año_seleccionado})",
                    labels={"Porcentaje": "Porcentaje de estudiantes (%)", "Entidad": "Entidad"},
                    color="Porcentaje",
                    color_continuous_scale="Viridis",
                    orientation='h'
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info(f"No hay datos suficientes para mostrar la comparativa por estados en {año_seleccionado}.")
        else:
            st.warning(f"No se encontró la columna de entidad en los datos de {año_seleccionado}.")
    else:
        st.warning(f"No hay datos disponibles para el año {año_seleccionado}.")

# Pie de página
st.markdown("---")
st.markdown("Dashboard PLANEA con KPIs - Desarrollado con Streamlit")
