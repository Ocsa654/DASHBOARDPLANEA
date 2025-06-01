# Pestaña 4: Datos 2022
with tab4:
    st.header("Análisis de Datos 2022")
    
    if df_2022 is None:
        st.warning("No hay datos disponibles para el año 2022.")
        st.stop()
    
    # Información general de los datos 2022
    st.subheader("Información General")
    
    # Buscar columnas relevantes
    cal_lenguaje_col = None
    cal_matematicas_col = None
    entidad_col = None
    
    for col in df_2022.columns:
        if "CALIF" in col and ("LENGUAJE" in col or "COMUNICACION" in col):
            cal_lenguaje_col = col
        elif "CALIF" in col and ("MATEMATICAS" in col or "MATEMÁTICAS" in col):
            cal_matematicas_col = col
        elif col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
            entidad_col = col
    
    # Mostrar métricas generales de 2022
    col1, col2 = st.columns(2)
    
    with col1:
        if cal_lenguaje_col:
            prom_lenguaje = df_2022[cal_lenguaje_col].mean()
            st.metric(
                label="Calificación promedio en Lenguaje",
                value=f"{prom_lenguaje:.1f}"
            )
            
            # Mostrar histograma de calificaciones de Lenguaje
            fig = px.histogram(
                df_2022,
                x=cal_lenguaje_col,
                title="Distribución de Calificaciones de Lenguaje",
                labels={cal_lenguaje_col: "Calificación"},
                nbins=20
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        if cal_matematicas_col:
            prom_matematicas = df_2022[cal_matematicas_col].mean()
            st.metric(
                label="Calificación promedio en Matemáticas",
                value=f"{prom_matematicas:.1f}"
            )
            
            # Mostrar histograma de calificaciones de Matemáticas
            fig = px.histogram(
                df_2022,
                x=cal_matematicas_col,
                title="Distribución de Calificaciones de Matemáticas",
                labels={cal_matematicas_col: "Calificación"},
                nbins=20
            )
            st.plotly_chart(fig, use_container_width=True)
    
    # Análisis por entidad
    if entidad_col:
        st.subheader("Análisis por Entidad")
        
        # Obtener lista de entidades
        entidades = sorted(df_2022[entidad_col].unique())
        
        # Calcular promedios por entidad
        datos_entidad = []
        
        for entidad in entidades:
            df_entidad = df_2022[df_2022[entidad_col] == entidad]
            
            datos_entidad.append({
                "Entidad": entidad,
                "Lenguaje": df_entidad[cal_lenguaje_col].mean() if cal_lenguaje_col else 0,
                "Matemáticas": df_entidad[cal_matematicas_col].mean() if cal_matematicas_col else 0
            })
        
        # Crear DataFrame para los datos por entidad
        df_entidades = pd.DataFrame(datos_entidad)
        
        # Selector de métrica a visualizar
        metrica = st.selectbox(
            "Selecciona materia para el análisis:",
            ["Lenguaje", "Matemáticas", "Ambas"],
            index=2  # Por defecto mostrar ambas
        )
        
        if metrica == "Lenguaje":
            # Ordenar por Lenguaje (descendente)
            df_entidades = df_entidades.sort_values("Lenguaje", ascending=False)
            
            # Crear gráfico de barras
            fig = px.bar(
                df_entidades,
                x="Entidad",
                y="Lenguaje",
                title="Calificación promedio en Lenguaje por Entidad",
                labels={"Lenguaje": "Calificación promedio"},
                color="Lenguaje",
                color_continuous_scale="Viridis"
            )
            
            # Ajustar layout para mejor visualización
            fig.update_layout(
                xaxis={'categoryorder':'total descending'},
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        elif metrica == "Matemáticas":
            # Ordenar por Matemáticas (descendente)
            df_entidades = df_entidades.sort_values("Matemáticas", ascending=False)
            
            # Crear gráfico de barras
            fig = px.bar(
                df_entidades,
                x="Entidad",
                y="Matemáticas",
                title="Calificación promedio en Matemáticas por Entidad",
                labels={"Matemáticas": "Calificación promedio"},
                color="Matemáticas",
                color_continuous_scale="Viridis"
            )
            
            # Ajustar layout para mejor visualización
            fig.update_layout(
                xaxis={'categoryorder':'total descending'},
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
        else:  # Ambas
            # Convertir a formato "largo" para plotly
            df_long = pd.melt(
                df_entidades,
                id_vars=["Entidad"],
                value_vars=["Lenguaje", "Matemáticas"],
                var_name="Materia",
                value_name="Calificación"
            )
            
            # Crear gráfico de barras agrupadas
            fig = px.bar(
                df_long,
                x="Entidad",
                y="Calificación",
                color="Materia",
                barmode="group",
                title="Calificación promedio por Entidad y Materia",
                labels={"Calificación": "Calificación promedio"}
            )
            
            # Ajustar layout para mejor visualización
            fig.update_layout(
                xaxis={'categoryorder':'total ascending'},
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # Análisis detallado de una entidad específica
        st.subheader("Análisis detallado por Entidad")
        
        # Selector de entidad
        entidad_seleccionada = st.selectbox("Selecciona una entidad:", entidades)
        
        # Filtrar datos para la entidad seleccionada
        df_entidad = df_2022[df_2022[entidad_col] == entidad_seleccionada]
        
        # Mostrar estadísticas básicas
        col1, col2 = st.columns(2)
        
        with col1:
            if cal_lenguaje_col:
                st.subheader(f"Lenguaje - {entidad_seleccionada}")
                
                # Estadísticas descriptivas
                media = df_entidad[cal_lenguaje_col].mean()
                mediana = df_entidad[cal_lenguaje_col].median()
                min_val = df_entidad[cal_lenguaje_col].min()
                max_val = df_entidad[cal_lenguaje_col].max()
                
                # Mostrar métricas
                st.metric("Promedio", f"{media:.1f}")
                st.metric("Mediana", f"{mediana:.1f}")
                st.metric("Rango", f"{min_val:.1f} - {max_val:.1f}")
                
                # Mostrar histograma
                fig = px.histogram(
                    df_entidad,
                    x=cal_lenguaje_col,
                    title=f"Distribución de Calificaciones de Lenguaje en {entidad_seleccionada}",
                    labels={cal_lenguaje_col: "Calificación"},
                    nbins=15
                )
                
                # Agregar línea vertical para la media
                fig.add_vline(x=media, line_dash="dash", line_color="red")
                
                st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            if cal_matematicas_col:
                st.subheader(f"Matemáticas - {entidad_seleccionada}")
                
                # Estadísticas descriptivas
                media = df_entidad[cal_matematicas_col].mean()
                mediana = df_entidad[cal_matematicas_col].median()
                min_val = df_entidad[cal_matematicas_col].min()
                max_val = df_entidad[cal_matematicas_col].max()
                
                # Mostrar métricas
                st.metric("Promedio", f"{media:.1f}")
                st.metric("Mediana", f"{mediana:.1f}")
                st.metric("Rango", f"{min_val:.1f} - {max_val:.1f}")
                
                # Mostrar histograma
                fig = px.histogram(
                    df_entidad,
                    x=cal_matematicas_col,
                    title=f"Distribución de Calificaciones de Matemáticas en {entidad_seleccionada}",
                    labels={cal_matematicas_col: "Calificación"},
                    nbins=15
                )
                
                # Agregar línea vertical para la media
                fig.add_vline(x=media, line_dash="dash", line_color="red")
                
                st.plotly_chart(fig, use_container_width=True)
    
    # Comparativa 2022 vs 2017
    st.subheader("Comparativa 2022 vs 2017")
    
    st.info("""
    **Nota importante:** La comparación directa entre los datos de 2022 y 2017 debe interpretarse con precaución debido a:
    - Posibles diferencias en la metodología de evaluación
    - Cambios en los contenidos evaluados
    - Efectos de la pandemia en el sistema educativo
    - Diferencias en las escalas de calificación
    """)
    
    # Buscar columnas similares en ambos conjuntos de datos
    columnas_comunes = []
    
    if df_2017 is not None:
        for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA', 'TIPO DE ESCUELA', 'TIPO ESCUELA', 'SOSTENIMIENTO']:
            if col in df_2017.columns and col in df_2022.columns:
                columnas_comunes.append(col)
    
    if columnas_comunes:
        # Selector de columna para comparación
        columna_comparativa = st.selectbox(
            "Selecciona variable para comparar 2017 vs 2022:",
            columnas_comunes
        )
        
        # Obtener valores únicos para la columna seleccionada
        valores_2017 = sorted(df_2017[columna_comparativa].unique())
        valores_2022 = sorted(df_2022[columna_comparativa].unique())
        
        # Encontrar valores comunes
        valores_comunes = list(set(valores_2017).intersection(set(valores_2022)))
        
        if valores_comunes:
            # Preparar datos para la comparativa
            datos_comparativa = []
            
            for valor in valores_comunes:
                # Datos 2017
                df_2017_filtrado = df_2017[df_2017[columna_comparativa] == valor]
                lenguaje_2017 = calcular_porcentaje_satisfactorio(df_2017_filtrado, "LENGUAJE")
                matematicas_2017 = calcular_porcentaje_satisfactorio(df_2017_filtrado, "MATEMATICAS")
                
                # Datos 2022
                df_2022_filtrado = df_2022[df_2022[columna_comparativa] == valor]
                lenguaje_2022 = df_2022_filtrado[cal_lenguaje_col].mean() if cal_lenguaje_col else 0
                matematicas_2022 = df_2022_filtrado[cal_matematicas_col].mean() if cal_matematicas_col else 0
                
                # Normalizar calificaciones 2022 (asumiendo escala de 0-100)
                lenguaje_2022_norm = (lenguaje_2022 / 10) * 100 if lenguaje_2022 > 0 else 0
                matematicas_2022_norm = (matematicas_2022 / 10) * 100 if matematicas_2022 > 0 else 0
                
                # Agregar datos de Lenguaje
                datos_comparativa.append({
                    "Grupo": valor,
                    "Materia": "Lenguaje",
                    "Año": "2017",
                    "Valor": lenguaje_2017
                })
                
                datos_comparativa.append({
                    "Grupo": valor,
                    "Materia": "Lenguaje",
                    "Año": "2022",
                    "Valor": lenguaje_2022_norm
                })
                
                # Agregar datos de Matemáticas
                datos_comparativa.append({
                    "Grupo": valor,
                    "Materia": "Matemáticas",
                    "Año": "2017",
                    "Valor": matematicas_2017
                })
                
                datos_comparativa.append({
                    "Grupo": valor,
                    "Materia": "Matemáticas",
                    "Año": "2022",
                    "Valor": matematicas_2022_norm
                })
            
            # Crear DataFrame para la comparativa
            df_comparativa = pd.DataFrame(datos_comparativa)
            
            # Selector de materia
            materia_comp = st.radio(
                "Selecciona materia para la comparativa:",
                ["Lenguaje", "Matemáticas"],
                horizontal=True
            )
            
            # Filtrar por materia
            df_filtrado = df_comparativa[df_comparativa["Materia"] == materia_comp]
            
            # Crear gráfico de barras agrupadas
            fig = px.bar(
                df_filtrado,
                x="Grupo",
                y="Valor",
                color="Año",
                barmode="group",
                title=f"Comparativa 2017 vs 2022 por {columna_comparativa} ({materia_comp})",
                labels={"Valor": "Valor (normalizado)"}
            )
            
            # Ajustar layout para mejor visualización
            fig.update_layout(
                xaxis_tickangle=-45
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Mostrar advertencia sobre la comparabilidad
            st.warning("""
            **Nota sobre comparabilidad:**
            - Los valores de 2022 han sido normalizados para facilitar la comparación visual
            - Las diferencias pueden deberse a múltiples factores y no solo a cambios en el rendimiento
            """)
        else:
            st.warning(f"No se encontraron valores comunes para {columna_comparativa} entre los datos de 2017 y 2022.")
    else:
        st.warning("No se encontraron columnas comunes para comparar entre los datos de 2017 y 2022.")
