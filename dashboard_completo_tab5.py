# Pestaña 5: Tablas y Estadísticas
with tab5:
    st.header("Tablas y Estadísticas")
    
    # Selector de conjunto de datos
    dataset = st.selectbox(
        "Selecciona conjunto de datos:",
        ["2015", "2016", "2017", "2022"],
        index=2  # Por defecto 2017
    )
    
    # Obtener el dataframe seleccionado
    df_seleccionado = None
    if dataset == "2015":
        df_seleccionado = df_2015
    elif dataset == "2016":
        df_seleccionado = df_2016
    elif dataset == "2017":
        df_seleccionado = df_2017
    elif dataset == "2022":
        df_seleccionado = df_2022
    
    if df_seleccionado is None:
        st.warning(f"No hay datos disponibles para el año {dataset}.")
        st.stop()
    
    # Mostrar información del conjunto de datos
    st.subheader("Información del conjunto de datos")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Número de filas", f"{df_seleccionado.shape[0]:,}")
    
    with col2:
        st.metric("Número de columnas", f"{df_seleccionado.shape[1]:,}")
    
    with col3:
        # Calcular porcentaje de valores faltantes
        valores_faltantes = df_seleccionado.isnull().sum().sum()
        total_valores = df_seleccionado.size
        porcentaje_faltantes = (valores_faltantes / total_valores) * 100
        
        st.metric("Valores faltantes", f"{porcentaje_faltantes:.1f}%")
    
    # Mostrar primeras filas del conjunto de datos
    st.subheader("Vista previa de los datos")
    
    num_filas = st.slider("Número de filas a mostrar", 5, 50, 10)
    st.dataframe(df_seleccionado.head(num_filas))
    
    # Estadísticas descriptivas
    st.subheader("Estadísticas descriptivas")
    
    # Filtrar solo columnas numéricas
    cols_numericas = df_seleccionado.select_dtypes(include=['int64', 'float64']).columns.tolist()
    
    if cols_numericas:
        # Selector de columnas para estadísticas
        cols_seleccionadas = st.multiselect(
            "Selecciona columnas para estadísticas:",
            cols_numericas,
            default=cols_numericas[:5] if len(cols_numericas) >= 5 else cols_numericas
        )
        
        if cols_seleccionadas:
            # Calcular estadísticas descriptivas
            df_stats = df_seleccionado[cols_seleccionadas].describe().T
            
            # Redondear valores a 2 decimales
            df_stats = df_stats.round(2)
            
            # Mostrar estadísticas
            st.dataframe(df_stats)
            
            # Selector de columna para histograma
            col_histograma = st.selectbox("Selecciona columna para histograma:", cols_seleccionadas)
            
            # Crear histograma
            fig = px.histogram(
                df_seleccionado,
                x=col_histograma,
                title=f"Distribución de {col_histograma}",
                nbins=30
            )
            
            # Agregar línea vertical para la media
            media = df_seleccionado[col_histograma].mean()
            fig.add_vline(x=media, line_dash="dash", line_color="red")
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("No se encontraron columnas numéricas en el conjunto de datos.")
    
    # Análisis por grupos
    st.subheader("Análisis por grupos")
    
    # Buscar columnas categóricas
    cols_categoricas = []
    for col in df_seleccionado.columns:
        if df_seleccionado[col].dtype == 'object' or df_seleccionado[col].nunique() < 20:
            cols_categoricas.append(col)
    
    if cols_categoricas:
        # Selector de columna para agrupación
        col_grupo = st.selectbox("Selecciona columna para agrupar:", cols_categoricas)
        
        # Verificar que la columna tenga valores únicos razonables
        valores_unicos = df_seleccionado[col_grupo].nunique()
        
        if valores_unicos > 0 and valores_unicos <= 50:  # Limitar a 50 grupos como máximo
            # Selector de columna para análisis
            col_analisis = st.selectbox(
                "Selecciona columna para analizar:",
                cols_numericas
            )
            
            # Calcular estadísticas por grupo
            df_grupo = df_seleccionado.groupby(col_grupo)[col_analisis].agg(['mean', 'median', 'std', 'min', 'max', 'count']).reset_index()
            df_grupo = df_grupo.sort_values('mean', ascending=False)
            
            # Renombrar columnas para mejor visualización
            df_grupo = df_grupo.rename(columns={
                'mean': 'Promedio',
                'median': 'Mediana',
                'std': 'Desv. Estándar',
                'min': 'Mínimo',
                'max': 'Máximo',
                'count': 'Conteo'
            })
            
            # Redondear valores a 2 decimales
            for col in ['Promedio', 'Mediana', 'Desv. Estándar', 'Mínimo', 'Máximo']:
                df_grupo[col] = df_grupo[col].round(2)
            
            # Mostrar tabla de estadísticas por grupo
            st.dataframe(df_grupo)
            
            # Crear gráfico de barras
            fig = px.bar(
                df_grupo,
                x=col_grupo,
                y='Promedio',
                error_y='Desv. Estándar',
                title=f"Promedio de {col_analisis} por {col_grupo}",
                labels={'Promedio': f'Promedio de {col_analisis}'}
            )
            
            # Ajustar layout para mejor visualización
            fig.update_layout(
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Crear gráfico de caja
            fig = px.box(
                df_seleccionado,
                x=col_grupo,
                y=col_analisis,
                title=f"Distribución de {col_analisis} por {col_grupo}",
                labels={col_analisis: col_analisis}
            )
            
            # Ajustar layout para mejor visualización
            fig.update_layout(
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning(f"La columna {col_grupo} tiene demasiados valores únicos ({valores_unicos}) para un análisis efectivo por grupos.")
    else:
        st.warning("No se encontraron columnas categóricas adecuadas para agrupar.")
    
    # Filtrado personalizado de datos
    st.subheader("Filtrado personalizado de datos")
    
    # Selector de columnas para filtrar
    col_filtro = st.selectbox("Selecciona columna para filtrar:", df_seleccionado.columns)
    
    # Determinar tipo de filtro según el tipo de datos
    if df_seleccionado[col_filtro].dtype == 'object' or df_seleccionado[col_filtro].nunique() < 20:
        # Para columnas categóricas o con pocos valores únicos
        valores_unicos = sorted(df_seleccionado[col_filtro].dropna().unique())
        valores_seleccionados = st.multiselect(
            f"Selecciona valores de {col_filtro}:",
            valores_unicos,
            default=valores_unicos[:5] if len(valores_unicos) >= 5 else valores_unicos
        )
        
        if valores_seleccionados:
            df_filtrado = df_seleccionado[df_seleccionado[col_filtro].isin(valores_seleccionados)]
        else:
            df_filtrado = df_seleccionado
    else:
        # Para columnas numéricas
        min_val = float(df_seleccionado[col_filtro].min())
        max_val = float(df_seleccionado[col_filtro].max())
        
        rango_valores = st.slider(
            f"Rango de valores para {col_filtro}:",
            min_val,
            max_val,
            (min_val, max_val)
        )
        
        df_filtrado = df_seleccionado[(df_seleccionado[col_filtro] >= rango_valores[0]) & 
                                    (df_seleccionado[col_filtro] <= rango_valores[1])]
    
    # Mostrar datos filtrados
    st.subheader("Datos filtrados")
    st.write(f"Mostrando {len(df_filtrado)} filas de {len(df_seleccionado)} totales")
    
    num_filas_filtradas = st.slider("Número de filas filtradas a mostrar", 5, 50, 10, key="num_filas_filtradas")
    st.dataframe(df_filtrado.head(num_filas_filtradas))
    
    # Exportar datos
    st.subheader("Exportar datos")
    
    @st.cache_data
    def convertir_df_a_csv(df):
        return df.to_csv(index=False).encode('utf-8')
    
    csv = convertir_df_a_csv(df_filtrado)
    
    st.download_button(
        label="Descargar datos filtrados como CSV",
        data=csv,
        file_name=f'datos_planea_{dataset}_filtrados.csv',
        mime='text/csv',
    )
