import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import time

# Configuración de la página
st.set_page_config(
    page_title="Dashboard PLANEA",
    page_icon="📊",
    layout="wide"
)

# Título principal
st.title("Dashboard PLANEA - Visualización")
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

# Estado de carga y selección
if 'muestra_2015_2017' not in st.session_state:
    st.session_state.muestra_2015_2017 = None
    st.session_state.muestra_2022 = None
    st.session_state.carga_completa_2015_2017 = False
    st.session_state.carga_completa_2022 = False
    st.session_state.df_2015_2017_completo = None
    st.session_state.df_2022_completo = None

# Configuración de carga progresiva
opciones_carga = st.radio(
    "¿Qué datos deseas analizar?",
    ["Datos 2015-2017", "Datos 2022"],
    horizontal=True
)

# Sidebar para opciones de carga
st.sidebar.header("Opciones de carga")
max_filas = st.sidebar.slider("Número máximo de filas a cargar", 100, 5000, 500, step=100)
cargar_todo = st.sidebar.checkbox("Cargar datos completos (puede tardar)", value=False)

# Función para cargar datos y siempre mostrar gráficas (incluso con muestra)
def cargar_y_procesar_datos(archivo, year, max_filas=500, solo_muestra=True):
    # Determinar qué dataset usar
    if year == "2015-2017":
        if st.session_state.muestra_2015_2017 is None:
            # Cargar muestra inicial
            with st.spinner('Cargando muestra de datos 2015-2017...'):
                df_muestra = pd.read_excel(archivo, nrows=100)
                st.session_state.muestra_2015_2017 = normalizar_columnas(df_muestra)
                st.success('Muestra de datos cargada correctamente')
        
        # Ver si necesitamos cargar datos completos
        if cargar_todo and not st.session_state.carga_completa_2015_2017:
            with st.spinner(f'Cargando datos (máximo {max_filas} filas)...'):
                df_completo = pd.read_excel(archivo, nrows=max_filas)
                st.session_state.df_2015_2017_completo = normalizar_columnas(df_completo)
                st.session_state.carga_completa_2015_2017 = True
                st.success(f'Se han cargado {len(df_completo)} filas')
        
        # Retornar el dataset apropiado
        if st.session_state.carga_completa_2015_2017:
            return st.session_state.df_2015_2017_completo
        else:
            return st.session_state.muestra_2015_2017
    
    else:  # "2022"
        if st.session_state.muestra_2022 is None:
            # Cargar muestra inicial
            with st.spinner('Cargando muestra de datos 2022...'):
                df_muestra = pd.read_excel(archivo, nrows=100)
                st.session_state.muestra_2022 = normalizar_columnas(df_muestra)
                st.success('Muestra de datos cargada correctamente')
        
        # Ver si necesitamos cargar datos completos
        if cargar_todo and not st.session_state.carga_completa_2022:
            with st.spinner(f'Cargando datos (máximo {max_filas} filas)...'):
                df_completo = pd.read_excel(archivo, nrows=max_filas)
                st.session_state.df_2022_completo = normalizar_columnas(df_completo)
                st.session_state.carga_completa_2022 = True
                st.success(f'Se han cargado {len(df_completo)} filas')
        
        # Retornar el dataset apropiado
        if st.session_state.carga_completa_2022:
            return st.session_state.df_2022_completo
        else:
            return st.session_state.muestra_2022

# Cargar datos según la selección
if opciones_carga == "Datos 2015-2017":
    df = cargar_y_procesar_datos('DATOS2015-2017.xlsx', "2015-2017", max_filas, not cargar_todo)
    
    # Mensaje de advertencia si estamos usando una muestra
    if not st.session_state.carga_completa_2015_2017:
        st.warning("⚠️ Estás viendo gráficas basadas en una muestra de 100 filas. Para un análisis más preciso, activa 'Cargar datos completos' en la barra lateral.")
    
    # Crear pestañas para organizar el contenido
    tab1, tab2 = st.tabs(["Niveles de Desempeño", "Análisis por Entidad"])
    
    with tab1:
        st.header("Niveles de Desempeño en PLANEA 2015-2017")
        
        # Determinar columna de año si existe
        año_col = None
        for col in ['ANO', 'ANIO', 'AÑO', 'A?O', 'YEAR']:
            if col in df.columns:
                año_col = col
                break
        
        # Filtro por año si está disponible
        if año_col and len(df[año_col].unique()) > 1:
            años = sorted(df[año_col].unique())
            año_seleccionado = st.selectbox("Selecciona un año:", años)
            df_filtrado = df[df[año_col] == año_seleccionado]
        else:
            df_filtrado = df
        
        # Buscar columnas de niveles
        niveles_lenguaje = []
        for col in df_filtrado.columns:
            if ("LENGUAJE" in col or "COMUNICACION" in col) and "NIVEL" in col and "%" in col:
                niveles_lenguaje.append(col)
        
        niveles_matematicas = []
        for col in df_filtrado.columns:
            if ("MATEMATICAS" in col or "MATEMÁTICAS" in col) and "NIVEL" in col and "%" in col:
                niveles_matematicas.append(col)
        
        # Crear gráficas
        col1, col2 = st.columns(2)
        
        with col1:
            if niveles_lenguaje:
                # Preparar datos para gráfica
                niveles_data = []
                for col in sorted(niveles_lenguaje):
                    nivel = col.split("NIVEL")[-1].strip().split(" ")[0]
                    valor = df_filtrado[col].mean()
                    niveles_data.append({"Nivel": f"Nivel {nivel}", "Valor": valor})
                
                df_niveles = pd.DataFrame(niveles_data)
                
                # Crear gráfica de barras
                fig = px.bar(
                    df_niveles,
                    x="Nivel",
                    y="Valor",
                    title="Distribución por niveles - Lenguaje y Comunicación",
                    color="Nivel",
                    labels={"Valor": "Porcentaje Promedio (%)"}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No se encontraron columnas de niveles para Lenguaje")
        
        with col2:
            if niveles_matematicas:
                # Preparar datos para gráfica
                niveles_data = []
                for col in sorted(niveles_matematicas):
                    nivel = col.split("NIVEL")[-1].strip().split(" ")[0]
                    valor = df_filtrado[col].mean()
                    niveles_data.append({"Nivel": f"Nivel {nivel}", "Valor": valor})
                
                df_niveles = pd.DataFrame(niveles_data)
                
                # Crear gráfica de barras
                fig = px.bar(
                    df_niveles,
                    x="Nivel",
                    y="Valor",
                    title="Distribución por niveles - Matemáticas",
                    color="Nivel",
                    labels={"Valor": "Porcentaje Promedio (%)"}
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No se encontraron columnas de niveles para Matemáticas")
        
        # Gráfico combinado
        st.subheader("Comparativa de niveles satisfactorios")
        
        if niveles_lenguaje and niveles_matematicas:
            # Calcular porcentajes satisfactorios (niveles III y IV)
            niveles_satisfactorios = {"Materia": [], "Porcentaje": []}
            
            # Lenguaje
            nivel3_lenguaje = None
            nivel4_lenguaje = None
            for col in niveles_lenguaje:
                if "NIVEL III" in col:
                    nivel3_lenguaje = col
                elif "NIVEL IV" in col:
                    nivel4_lenguaje = col
            
            if nivel3_lenguaje and nivel4_lenguaje:
                porcentaje_satisfactorio = df_filtrado[nivel3_lenguaje].mean() + df_filtrado[nivel4_lenguaje].mean()
                niveles_satisfactorios["Materia"].append("Lenguaje")
                niveles_satisfactorios["Porcentaje"].append(porcentaje_satisfactorio)
            
            # Matemáticas
            nivel3_matematicas = None
            nivel4_matematicas = None
            for col in niveles_matematicas:
                if "NIVEL III" in col:
                    nivel3_matematicas = col
                elif "NIVEL IV" in col:
                    nivel4_matematicas = col
            
            if nivel3_matematicas and nivel4_matematicas:
                porcentaje_satisfactorio = df_filtrado[nivel3_matematicas].mean() + df_filtrado[nivel4_matematicas].mean()
                niveles_satisfactorios["Materia"].append("Matemáticas")
                niveles_satisfactorios["Porcentaje"].append(porcentaje_satisfactorio)
            
            # Crear gráfica
            if niveles_satisfactorios["Materia"]:
                df_satisfactorios = pd.DataFrame(niveles_satisfactorios)
                
                fig = px.bar(
                    df_satisfactorios,
                    x="Materia",
                    y="Porcentaje",
                    title="Porcentaje de alumnos en niveles satisfactorios (III y IV)",
                    color="Materia",
                    labels={"Porcentaje": "Porcentaje (%)"}
                )
                st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Análisis por Entidad")
        
        # Determinar columna de entidad
        entidad_col = None
        for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
            if col in df.columns:
                entidad_col = col
                break
        
        if entidad_col:
            # Selector de entidad
            entidades = sorted(df[entidad_col].unique())
            entidad_seleccionada = st.selectbox("Selecciona una entidad:", entidades)
            
            # Filtrar por entidad
            df_entidad = df[df[entidad_col] == entidad_seleccionada]
            
            # Buscar columnas relevantes
            alumnos_col = None
            for col in df.columns:
                if "ALUMNOS EVALUADOS" in col:
                    alumnos_col = col
                    break
            
            # Gráfica de distribución de alumnos evaluados
            if alumnos_col:
                st.subheader(f"Distribución de alumnos evaluados en {entidad_seleccionada}")
                
                # Buscar columna de municipio o localidad
                ubicacion_col = None
                for col in df_entidad.columns:
                    if "MUNICIPIO" in col or "LOCALIDAD" in col:
                        ubicacion_col = col
                        break
                
                if ubicacion_col and len(df_entidad[ubicacion_col].unique()) > 1:
                    # Agrupar por ubicación
                    df_ubicacion = df_entidad.groupby(ubicacion_col)[alumnos_col].sum().reset_index()
                    df_ubicacion = df_ubicacion.sort_values(alumnos_col, ascending=False).head(10)
                    
                    # Crear gráfica
                    fig = px.bar(
                        df_ubicacion,
                        x=ubicacion_col,
                        y=alumnos_col,
                        title=f"Alumnos evaluados por {ubicacion_col.lower().split()[-1]} (Top 10)",
                        labels={alumnos_col: "Alumnos evaluados"},
                        color=alumnos_col,
                        color_continuous_scale="Viridis"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                else:
                    st.info(f"No hay suficientes datos de ubicación para {entidad_seleccionada}")
            
            # Gráfico de niveles por entidad
            niveles_lenguaje = []
            for col in df.columns:
                if ("LENGUAJE" in col or "COMUNICACION" in col) and "NIVEL" in col and "%" in col:
                    niveles_lenguaje.append(col)
            
            if niveles_lenguaje:
                st.subheader(f"Distribución de niveles en {entidad_seleccionada}")
                
                # Preparar datos para gráfica
                niveles_data = []
                for col in sorted(niveles_lenguaje):
                    nivel = col.split("NIVEL")[-1].strip().split(" ")[0]
                    valor = df_entidad[col].mean()
                    niveles_data.append({"Nivel": f"Nivel {nivel}", "Valor": valor})
                
                df_niveles = pd.DataFrame(niveles_data)
                
                # Crear gráfica
                fig = px.pie(
                    df_niveles, 
                    values='Valor', 
                    names='Nivel',
                    title=f"Distribución por niveles en Lenguaje - {entidad_seleccionada}",
                    hole=0.4
                )
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No se encontró la columna de entidad en los datos")

elif opciones_carga == "Datos 2022":
    df = cargar_y_procesar_datos('DATOS2022.xlsx', "2022", max_filas, not cargar_todo)
    
    # Mensaje de advertencia si estamos usando una muestra
    if not st.session_state.carga_completa_2022:
        st.warning("⚠️ Estás viendo gráficas basadas en una muestra de 100 filas. Para un análisis más preciso, activa 'Cargar datos completos' en la barra lateral.")
    
    # Crear pestañas para organizar el contenido
    tab1, tab2 = st.tabs(["Calificaciones", "Análisis por Entidad"])
    
    with tab1:
        st.header("Distribución de Calificaciones PLANEA 2022")
        
        # Buscar columnas de calificaciones
        cal_lenguaje = None
        cal_matematicas = None
        
        for col in df.columns:
            if "CALIF" in col and ("LENGUAJE" in col or "COMUNICACION" in col):
                cal_lenguaje = col
            elif "CALIF" in col and ("MATEMATICAS" in col or "MATEMÁTICAS" in col):
                cal_matematicas = col
        
        # Crear gráficas
        col1, col2 = st.columns(2)
        
        with col1:
            if cal_lenguaje:
                # Histograma de calificaciones en Lenguaje
                fig = px.histogram(
                    df,
                    x=cal_lenguaje,
                    nbins=20,
                    title="Distribución de calificaciones en Lenguaje",
                    labels={cal_lenguaje: "Calificación"},
                    color_discrete_sequence=["#1f77b4"]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No se encontró la columna de calificación en Lenguaje")
        
        with col2:
            if cal_matematicas:
                # Histograma de calificaciones en Matemáticas
                fig = px.histogram(
                    df,
                    x=cal_matematicas,
                    nbins=20,
                    title="Distribución de calificaciones en Matemáticas",
                    labels={cal_matematicas: "Calificación"},
                    color_discrete_sequence=["#ff7f0e"]
                )
                st.plotly_chart(fig, use_container_width=True)
            else:
                st.info("No se encontró la columna de calificación en Matemáticas")
        
        # Gráfico de dispersión
        if cal_lenguaje and cal_matematicas:
            st.subheader("Relación entre calificaciones de Lenguaje y Matemáticas")
            
            fig = px.scatter(
                df,
                x=cal_lenguaje,
                y=cal_matematicas,
                title="Correlación entre calificaciones",
                labels={
                    cal_lenguaje: "Calificación Lenguaje",
                    cal_matematicas: "Calificación Matemáticas"
                },
                trendline="ols"
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Calcular correlación
            correlacion = df[cal_lenguaje].corr(df[cal_matematicas])
            st.metric("Correlación", f"{correlacion:.4f}")
        
        # Análisis por género
        sexo_col = None
        for col in ["SEXO", "GENERO", "GÉNERO"]:
            if col in df.columns:
                sexo_col = col
                break
        
        if sexo_col and (cal_lenguaje or cal_matematicas):
            st.subheader("Análisis por género")
            
            col1, col2 = st.columns(2)
            
            with col1:
                if cal_lenguaje:
                    fig = px.box(
                        df,
                        x=sexo_col,
                        y=cal_lenguaje,
                        title="Calificaciones en Lenguaje por género",
                        color=sexo_col
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                if cal_matematicas:
                    fig = px.box(
                        df,
                        x=sexo_col,
                        y=cal_matematicas,
                        title="Calificaciones en Matemáticas por género",
                        color=sexo_col
                    )
                    st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.header("Análisis por Entidad")
        
        # Determinar columna de entidad
        entidad_col = None
        for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
            if col in df.columns:
                entidad_col = col
                break
        
        if entidad_col:
            # Selector de entidad
            entidades = sorted(df[entidad_col].unique())
            entidad_seleccionada = st.selectbox("Selecciona una entidad:", entidades)
            
            # Filtrar por entidad
            df_entidad = df[df[entidad_col] == entidad_seleccionada]
            
            # Buscar columnas de calificaciones
            cal_lenguaje = None
            cal_matematicas = None
            
            for col in df.columns:
                if "CALIF" in col and ("LENGUAJE" in col or "COMUNICACION" in col):
                    cal_lenguaje = col
                elif "CALIF" in col and ("MATEMATICAS" in col or "MATEMÁTICAS" in col):
                    cal_matematicas = col
            
            # Crear gráficas
            if cal_lenguaje and cal_matematicas:
                st.subheader(f"Distribución de calificaciones en {entidad_seleccionada}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Histograma de calificaciones en Lenguaje
                    fig = px.histogram(
                        df_entidad,
                        x=cal_lenguaje,
                        nbins=15,
                        title=f"Calificaciones en Lenguaje - {entidad_seleccionada}",
                        labels={cal_lenguaje: "Calificación"},
                        color_discrete_sequence=["#1f77b4"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Histograma de calificaciones en Matemáticas
                    fig = px.histogram(
                        df_entidad,
                        x=cal_matematicas,
                        nbins=15,
                        title=f"Calificaciones en Matemáticas - {entidad_seleccionada}",
                        labels={cal_matematicas: "Calificación"},
                        color_discrete_sequence=["#ff7f0e"]
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Estadísticas descriptivas
                st.subheader("Estadísticas descriptivas")
                stats_df = df_entidad[[cal_lenguaje, cal_matematicas]].describe().round(2)
                st.dataframe(stats_df)
            
            # Análisis por semestre si está disponible
            semestre_col = None
            for col in ["SEMESTRE", "GRADO"]:
                if col in df.columns:
                    semestre_col = col
                    break
            
            if semestre_col and (cal_lenguaje or cal_matematicas):
                st.subheader(f"Análisis por {semestre_col}")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    if cal_lenguaje:
                        fig = px.box(
                            df_entidad,
                            x=semestre_col,
                            y=cal_lenguaje,
                            title=f"Calificaciones en Lenguaje por {semestre_col}",
                            color=semestre_col
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    if cal_matematicas:
                        fig = px.box(
                            df_entidad,
                            x=semestre_col,
                            y=cal_matematicas,
                            title=f"Calificaciones en Matemáticas por {semestre_col}",
                            color=semestre_col
                        )
                        st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No se encontró la columna de entidad en los datos")

# Indicador de modo de visualización
st.sidebar.markdown("---")
if opciones_carga == "Datos 2015-2017":
    if st.session_state.carga_completa_2015_2017:
        st.sidebar.success(f"Visualizando hasta {max_filas} filas de datos 2015-2017")
    else:
        st.sidebar.warning("Visualizando muestra de 100 filas de datos 2015-2017")
else:  # "Datos 2022"
    if st.session_state.carga_completa_2022:
        st.sidebar.success(f"Visualizando hasta {max_filas} filas de datos 2022")
    else:
        st.sidebar.warning("Visualizando muestra de 100 filas de datos 2022")

# Pie de página
st.markdown("---")
st.markdown("Dashboard PLANEA desarrollado con Streamlit")
