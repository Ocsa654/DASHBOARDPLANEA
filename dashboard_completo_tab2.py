# Pestaña 2: Análisis por Año (2015-2017)
with tab2:
    st.header("Análisis por Año (2015-2017)")
    
    # Selector de año
    año_seleccionado = st.selectbox(
        "Selecciona el año a analizar:",
        [2015, 2016, 2017],
        index=2  # Por defecto 2017
    )
    
    # Obtener el dataframe del año seleccionado
    df_año = None
    if año_seleccionado == 2015:
        df_año = df_2015
    elif año_seleccionado == 2016:
        df_año = df_2016
    elif año_seleccionado == 2017:
        df_año = df_2017
    
    if df_año is None:
        st.warning(f"No hay datos disponibles para el año {año_seleccionado}.")
        st.stop()
    
    # Información general del año seleccionado
    st.subheader(f"Datos generales para {año_seleccionado}")
    
    # Mostrar estadísticas generales
    col1, col2 = st.columns(2)
    
    with col1:
        # Calcular porcentajes por nivel para Lenguaje
        datos_lenguaje = []
        for nivel in range(1, 5):
            col_nivel = None
            for col in df_año.columns:
                if ("LENGUAJE" in col or "COMUNICACION" in col) and f"NIVEL {nivel}" in col and "%" in col:
                    col_nivel = col
                    break
            
            if col_nivel:
                datos_lenguaje.append({
                    "Nivel": f"Nivel {nivel}",
                    "Porcentaje": df_año[col_nivel].mean()
                })
        
        # Crear gráfico de pie para Lenguaje
        if datos_lenguaje:
            df_lenguaje = pd.DataFrame(datos_lenguaje)
            fig = px.pie(
                df_lenguaje,
                values="Porcentaje",
                names="Nivel",
                title=f"Distribución por niveles en Lenguaje ({año_seleccionado})",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostrar porcentaje de niveles satisfactorios
            porcentaje_satisfactorio = sum(df_lenguaje[df_lenguaje["Nivel"].isin(["Nivel 3", "Nivel 4", "Nivel III", "Nivel IV"])]["Porcentaje"])
            st.metric(
                label="Porcentaje en niveles satisfactorios (Lenguaje)",
                value=f"{porcentaje_satisfactorio:.1f}%"
            )
    
    with col2:
        # Calcular porcentajes por nivel para Matemáticas
        datos_matematicas = []
        for nivel in range(1, 5):
            col_nivel = None
            for col in df_año.columns:
                if ("MATEMATICAS" in col or "MATEMÁTICAS" in col) and f"NIVEL {nivel}" in col and "%" in col:
                    col_nivel = col
                    break
            
            if col_nivel:
                datos_matematicas.append({
                    "Nivel": f"Nivel {nivel}",
                    "Porcentaje": df_año[col_nivel].mean()
                })
        
        # Crear gráfico de pie para Matemáticas
        if datos_matematicas:
            df_matematicas = pd.DataFrame(datos_matematicas)
            fig = px.pie(
                df_matematicas,
                values="Porcentaje",
                names="Nivel",
                title=f"Distribución por niveles en Matemáticas ({año_seleccionado})",
                hole=0.4
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostrar porcentaje de niveles satisfactorios
            porcentaje_satisfactorio = sum(df_matematicas[df_matematicas["Nivel"].isin(["Nivel 3", "Nivel 4", "Nivel III", "Nivel IV"])]["Porcentaje"])
            st.metric(
                label="Porcentaje en niveles satisfactorios (Matemáticas)",
                value=f"{porcentaje_satisfactorio:.1f}%"
            )
    
    # Análisis por tipo de escuela
    st.subheader("Análisis por tipo de escuela")
    
    # Buscar columna de tipo de escuela
    tipo_escuela_col = None
    for col in ['TIPO DE ESCUELA', 'TIPO ESCUELA', 'TIPO', 'SOSTENIMIENTO']:
        if col in df_año.columns:
            tipo_escuela_col = col
            break
    
    if tipo_escuela_col:
        # Filtrar por tipo de escuela
        tipos_escuela = sorted(df_año[tipo_escuela_col].unique())
        tipo_seleccionado = st.selectbox("Selecciona tipo de escuela:", tipos_escuela)
        
        # Filtrar datos
        df_tipo = df_año[df_año[tipo_escuela_col] == tipo_seleccionado]
        
        # Mostrar datos para el tipo seleccionado
        col1, col2 = st.columns(2)
        
        with col1:
            # Lenguaje
            st.subheader(f"Lenguaje - {tipo_seleccionado}")
            porcentaje_satisfactorio = calcular_porcentaje_satisfactorio(df_tipo, "LENGUAJE")
            st.metric(
                label="Porcentaje en niveles satisfactorios",
                value=f"{porcentaje_satisfactorio:.1f}%"
            )
            
            # Calcular porcentajes por nivel para Lenguaje
            datos_lenguaje = []
            for nivel in range(1, 5):
                col_nivel = None
                for col in df_tipo.columns:
                    if ("LENGUAJE" in col or "COMUNICACION" in col) and f"NIVEL {nivel}" in col and "%" in col:
                        col_nivel = col
                        break
                
                if col_nivel:
                    datos_lenguaje.append({
                        "Nivel": f"Nivel {nivel}",
                        "Porcentaje": df_tipo[col_nivel].mean()
                    })
            
            # Crear gráfico de barras para Lenguaje
            if datos_lenguaje:
                df_lenguaje = pd.DataFrame(datos_lenguaje)
                fig = px.bar(
                    df_lenguaje,
                    x="Nivel",
                    y="Porcentaje",
                    title=f"Distribución por niveles en Lenguaje ({tipo_seleccionado})",
                    color="Nivel"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Matemáticas
            st.subheader(f"Matemáticas - {tipo_seleccionado}")
            porcentaje_satisfactorio = calcular_porcentaje_satisfactorio(df_tipo, "MATEMATICAS")
            st.metric(
                label="Porcentaje en niveles satisfactorios",
                value=f"{porcentaje_satisfactorio:.1f}%"
            )
            
            # Calcular porcentajes por nivel para Matemáticas
            datos_matematicas = []
            for nivel in range(1, 5):
                col_nivel = None
                for col in df_tipo.columns:
                    if ("MATEMATICAS" in col or "MATEMÁTICAS" in col) and f"NIVEL {nivel}" in col and "%" in col:
                        col_nivel = col
                        break
                
                if col_nivel:
                    datos_matematicas.append({
                        "Nivel": f"Nivel {nivel}",
                        "Porcentaje": df_tipo[col_nivel].mean()
                    })
            
            # Crear gráfico de barras para Matemáticas
            if datos_matematicas:
                df_matematicas = pd.DataFrame(datos_matematicas)
                fig = px.bar(
                    df_matematicas,
                    x="Nivel",
                    y="Porcentaje",
                    title=f"Distribución por niveles en Matemáticas ({tipo_seleccionado})",
                    color="Nivel"
                )
                st.plotly_chart(fig, use_container_width=True)
        
        # Comparativa entre todos los tipos de escuela
        st.subheader("Comparativa entre tipos de escuela")
        
        # Preparar datos para la comparativa
        datos_comparativa = []
        
        for tipo in tipos_escuela:
            df_tipo = df_año[df_año[tipo_escuela_col] == tipo]
            
            datos_comparativa.append({
                "Tipo de Escuela": tipo,
                "Lenguaje": calcular_porcentaje_satisfactorio(df_tipo, "LENGUAJE"),
                "Matemáticas": calcular_porcentaje_satisfactorio(df_tipo, "MATEMATICAS")
            })
        
        if datos_comparativa:
            df_comparativa = pd.DataFrame(datos_comparativa)
            
            # Convertir a formato "largo" para plotly
            df_long = pd.melt(
                df_comparativa,
                id_vars=["Tipo de Escuela"],
                value_vars=["Lenguaje", "Matemáticas"],
                var_name="Materia",
                value_name="Porcentaje"
            )
            
            # Crear gráfico de barras agrupadas
            fig = px.bar(
                df_long,
                x="Tipo de Escuela",
                y="Porcentaje",
                color="Materia",
                barmode="group",
                title=f"Porcentaje de estudiantes en niveles satisfactorios por tipo de escuela ({año_seleccionado})",
                labels={"Porcentaje": "Porcentaje de estudiantes (%)"}
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontró información sobre el tipo de escuela en los datos.")
    
    # Análisis de correlaciones
    st.subheader("Correlaciones entre variables")
    
    # Buscar columnas numéricas para el análisis de correlación
    cols_numericas = []
    for col in df_año.columns:
        try:
            if df_año[col].dtype in ['int64', 'float64'] and not col.lower().startswith('cct') and not col.lower().startswith('folio'):
                cols_numericas.append(col)
        except:
            pass
    
    if cols_numericas:
        # Seleccionar columnas para correlación
        cols_seleccionadas = st.multiselect(
            "Selecciona variables para el análisis de correlación:",
            cols_numericas,
            default=cols_numericas[:4] if len(cols_numericas) >= 4 else cols_numericas
        )
        
        if cols_seleccionadas:
            # Calcular matriz de correlación
            df_corr = df_año[cols_seleccionadas].corr()
            
            # Crear mapa de calor
            fig = px.imshow(
                df_corr,
                labels=dict(x="Variable", y="Variable", color="Correlación"),
                x=df_corr.columns,
                y=df_corr.columns,
                color_continuous_scale="RdBu_r",
                title=f"Matriz de correlación para variables seleccionadas ({año_seleccionado})"
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Explicación de la correlación
            st.info("""
            **Interpretación de la correlación:**
            - Valores cercanos a 1: Correlación positiva fuerte (cuando una variable aumenta, la otra también)
            - Valores cercanos a -1: Correlación negativa fuerte (cuando una variable aumenta, la otra disminuye)
            - Valores cercanos a 0: Poca o ninguna correlación
            """)
    else:
        st.warning("No se encontraron columnas numéricas adecuadas para el análisis de correlación.")
