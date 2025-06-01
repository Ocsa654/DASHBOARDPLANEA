# Pestaña 3: Análisis por Estado
with tab3:
    st.header("Análisis por Estado")
    
    # Buscar columna de entidad en los dataframes
    entidad_col = None
    for col in ['ENTIDAD', 'ESTADO', 'ENTIDAD FEDERATIVA']:
        if col in df_2017.columns:  # Usar 2017 como referencia
            entidad_col = col
            break
    
    if not entidad_col:
        st.warning("No se encontró la columna de entidad en los datos.")
        st.stop()
    
    # Obtener lista única de entidades
    entidades = set()
    if df_2015 is not None:
        entidades.update(df_2015[entidad_col].unique())
    if df_2016 is not None:
        entidades.update(df_2016[entidad_col].unique())
    if df_2017 is not None:
        entidades.update(df_2017[entidad_col].unique())
    
    entidades = sorted(list(entidades))
    
    # Selector de entidad
    entidad_seleccionada = st.selectbox("Selecciona una entidad:", entidades)
    
    # Mostrar evolución de la entidad seleccionada
    st.subheader(f"Evolución de {entidad_seleccionada} (2015-2017)")
    
    # Preparar datos para la gráfica
    datos_evolucion = []
    
    # 2015
    if df_2015 is not None:
        df_entidad = df_2015[df_2015[entidad_col] == entidad_seleccionada]
        if not df_entidad.empty:
            datos_evolucion.append({
                "Año": 2015,
                "Lenguaje": calcular_porcentaje_satisfactorio(df_entidad, "LENGUAJE"),
                "Matemáticas": calcular_porcentaje_satisfactorio(df_entidad, "MATEMATICAS")
            })
    
    # 2016
    if df_2016 is not None:
        df_entidad = df_2016[df_2016[entidad_col] == entidad_seleccionada]
        if not df_entidad.empty:
            datos_evolucion.append({
                "Año": 2016,
                "Lenguaje": calcular_porcentaje_satisfactorio(df_entidad, "LENGUAJE"),
                "Matemáticas": calcular_porcentaje_satisfactorio(df_entidad, "MATEMATICAS")
            })
    
    # 2017
    if df_2017 is not None:
        df_entidad = df_2017[df_2017[entidad_col] == entidad_seleccionada]
        if not df_entidad.empty:
            datos_evolucion.append({
                "Año": 2017,
                "Lenguaje": calcular_porcentaje_satisfactorio(df_entidad, "LENGUAJE"),
                "Matemáticas": calcular_porcentaje_satisfactorio(df_entidad, "MATEMATICAS")
            })
    
    if datos_evolucion:
        df_evolucion = pd.DataFrame(datos_evolucion)
        
        # Convertir a formato "largo" para plotly
        df_long = pd.melt(
            df_evolucion,
            id_vars=["Año"],
            value_vars=["Lenguaje", "Matemáticas"],
            var_name="Materia",
            value_name="Porcentaje"
        )
        
        # Crear gráfico de línea
        fig = px.line(
            df_long,
            x="Año",
            y="Porcentaje",
            color="Materia",
            markers=True,
            title=f"Evolución de niveles satisfactorios en {entidad_seleccionada} (2015-2017)",
            labels={"Porcentaje": "Porcentaje de estudiantes (%)"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Calcular cambio porcentual entre 2015 y 2017
        if len(df_evolucion) >= 2:
            primer_año = df_evolucion["Año"].min()
            ultimo_año = df_evolucion["Año"].max()
            
            valor_inicial_lenguaje = df_evolucion[df_evolucion["Año"] == primer_año]["Lenguaje"].values[0]
            valor_final_lenguaje = df_evolucion[df_evolucion["Año"] == ultimo_año]["Lenguaje"].values[0]
            
            valor_inicial_matematicas = df_evolucion[df_evolucion["Año"] == primer_año]["Matemáticas"].values[0]
            valor_final_matematicas = df_evolucion[df_evolucion["Año"] == ultimo_año]["Matemáticas"].values[0]
            
            cambio_lenguaje = valor_final_lenguaje - valor_inicial_lenguaje
            cambio_matematicas = valor_final_matematicas - valor_inicial_matematicas
            
            # Mostrar métricas de cambio
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric(
                    label=f"Cambio en Lenguaje ({primer_año}-{ultimo_año})",
                    value=f"{valor_final_lenguaje:.1f}%",
                    delta=f"{cambio_lenguaje:.1f}%"
                )
            
            with col2:
                st.metric(
                    label=f"Cambio en Matemáticas ({primer_año}-{ultimo_año})",
                    value=f"{valor_final_matematicas:.1f}%",
                    delta=f"{cambio_matematicas:.1f}%"
                )
    
    # Comparativa de la entidad con el promedio nacional
    st.subheader(f"Comparativa de {entidad_seleccionada} con el promedio nacional")
    
    # Selector de año para la comparativa
    año_comparativa = st.selectbox(
        "Selecciona año para la comparativa:",
        [2015, 2016, 2017],
        index=2  # Por defecto 2017
    )
    
    # Obtener dataframe del año seleccionado
    df_año = None
    if año_comparativa == 2015:
        df_año = df_2015
    elif año_comparativa == 2016:
        df_año = df_2016
    elif año_comparativa == 2017:
        df_año = df_2017
    
    if df_año is not None:
        # Filtrar por entidad seleccionada
        df_entidad = df_año[df_año[entidad_col] == entidad_seleccionada]
        
        # Calcular valores para la entidad y el promedio nacional
        valores_comparativa = []
        
        # Valor nacional Lenguaje
        valor_nacional_lenguaje = calcular_porcentaje_satisfactorio(df_año, "LENGUAJE")
        valores_comparativa.append({
            "Grupo": "Promedio Nacional",
            "Materia": "Lenguaje",
            "Porcentaje": valor_nacional_lenguaje
        })
        
        # Valor entidad Lenguaje
        valor_entidad_lenguaje = calcular_porcentaje_satisfactorio(df_entidad, "LENGUAJE")
        valores_comparativa.append({
            "Grupo": entidad_seleccionada,
            "Materia": "Lenguaje",
            "Porcentaje": valor_entidad_lenguaje
        })
        
        # Valor nacional Matemáticas
        valor_nacional_matematicas = calcular_porcentaje_satisfactorio(df_año, "MATEMATICAS")
        valores_comparativa.append({
            "Grupo": "Promedio Nacional",
            "Materia": "Matemáticas",
            "Porcentaje": valor_nacional_matematicas
        })
        
        # Valor entidad Matemáticas
        valor_entidad_matematicas = calcular_porcentaje_satisfactorio(df_entidad, "MATEMATICAS")
        valores_comparativa.append({
            "Grupo": entidad_seleccionada,
            "Materia": "Matemáticas",
            "Porcentaje": valor_entidad_matematicas
        })
        
        # Crear DataFrame para la comparativa
        df_comparativa = pd.DataFrame(valores_comparativa)
        
        # Crear gráfico de barras para la comparativa
        fig = px.bar(
            df_comparativa,
            x="Materia",
            y="Porcentaje",
            color="Grupo",
            barmode="group",
            title=f"Comparativa de {entidad_seleccionada} con el promedio nacional ({año_comparativa})",
            labels={"Porcentaje": "Porcentaje de estudiantes (%)"}
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Mostrar diferencia con el promedio nacional
        col1, col2 = st.columns(2)
        
        with col1:
            diferencia_lenguaje = valor_entidad_lenguaje - valor_nacional_lenguaje
            st.metric(
                label=f"Diferencia con promedio nacional en Lenguaje ({año_comparativa})",
                value=f"{valor_entidad_lenguaje:.1f}%",
                delta=f"{diferencia_lenguaje:.1f}%",
                help=f"Promedio nacional: {valor_nacional_lenguaje:.1f}%"
            )
        
        with col2:
            diferencia_matematicas = valor_entidad_matematicas - valor_nacional_matematicas
            st.metric(
                label=f"Diferencia con promedio nacional en Matemáticas ({año_comparativa})",
                value=f"{valor_entidad_matematicas:.1f}%",
                delta=f"{diferencia_matematicas:.1f}%",
                help=f"Promedio nacional: {valor_nacional_matematicas:.1f}%"
            )
    
    # Ranking de la entidad a nivel nacional
    st.subheader(f"Posición de {entidad_seleccionada} en el ranking nacional")
    
    # Selector de año y materia para el ranking
    col1, col2 = st.columns(2)
    
    with col1:
        año_ranking = st.selectbox(
            "Selecciona año para el ranking:",
            [2015, 2016, 2017],
            index=2,  # Por defecto 2017
            key="año_ranking"
        )
    
    with col2:
        materia_ranking = st.selectbox(
            "Selecciona materia para el ranking:",
            ["LENGUAJE", "MATEMATICAS"],
            format_func=lambda x: "Lenguaje" if x == "LENGUAJE" else "Matemáticas",
            key="materia_ranking"
        )
    
    # Obtener dataframe del año seleccionado
    df_año = None
    if año_ranking == 2015:
        df_año = df_2015
    elif año_ranking == 2016:
        df_año = df_2016
    elif año_ranking == 2017:
        df_año = df_2017
    
    if df_año is not None:
        # Preparar datos para el ranking
        ranking_datos = []
        
        for entidad in entidades:
            df_entidad = df_año[df_año[entidad_col] == entidad]
            
            if not df_entidad.empty:
                ranking_datos.append({
                    "Entidad": entidad,
                    "Porcentaje": calcular_porcentaje_satisfactorio(df_entidad, materia_ranking)
                })
        
        # Crear DataFrame para el ranking
        df_ranking = pd.DataFrame(ranking_datos)
        
        # Validar existencia de datos y columna 'Porcentaje'
        if df_ranking.empty or "Porcentaje" not in df_ranking.columns:
            st.warning("No se pudo calcular el ranking: faltan datos o columna 'Porcentaje'.")
        else:
            # Ordenar por porcentaje (descendente)
            df_ranking = df_ranking.sort_values("Porcentaje", ascending=False)
            # Agregar columna de posición
            df_ranking["Posición"] = range(1, len(df_ranking) + 1)
            # Encontrar posición de la entidad seleccionada
            posicion = df_ranking[df_ranking["Entidad"] == entidad_seleccionada]["Posición"].values[0]
            valor = df_ranking[df_ranking["Entidad"] == entidad_seleccionada]["Porcentaje"].values[0]
            # Mostrar posición en el ranking
            titulo_materia = "Lenguaje" if materia_ranking == "LENGUAJE" else "Matemáticas"
            leyenda = "(Promedio de calificación)" if año_ranking == 2022 else "(Porcentaje satisfactorio)"
            st.metric(
                label=f"Posición en el ranking nacional {leyenda} - {titulo_materia}, {año_ranking}",
                value=f"{posicion}° lugar",
                delta=f"{valor:.1f}",
                delta_color="off"
            )
            # Mostrar top 5 y bottom 5 del ranking
            col1, col2 = st.columns(2)
            with col1:
                st.subheader("Top 5 entidades")
                df_top5 = df_ranking.head(5).copy()
                df_top5["Porcentaje"] = df_top5["Porcentaje"].round(1).astype(str) + "%"
                if entidad_seleccionada in df_top5["Entidad"].values:
                    st.markdown(f"**{entidad_seleccionada} está en el Top 5**")
                st.table(df_top5[["Posición", "Entidad", "Porcentaje"]])
            with col2:
                st.subheader("Últimas 5 entidades")
                df_bottom5 = df_ranking.tail(5).copy()
                df_bottom5["Porcentaje"] = df_bottom5["Porcentaje"].round(1).astype(str) + "%"
                if entidad_seleccionada in df_bottom5["Entidad"].values:
                    st.markdown(f"**{entidad_seleccionada} está en las últimas 5 posiciones**")
                st.table(df_bottom5[["Posición", "Entidad", "Porcentaje"]])
            # Mostrar ranking completo
            st.subheader("Ranking completo")
            df_ranking_display = df_ranking.copy()
            df_ranking_display["Porcentaje"] = df_ranking_display["Porcentaje"].round(1).astype(str) + "%"
            def highlight_row(row):
                if row["Entidad"] == entidad_seleccionada:
                    return ['background-color: #FFFF00'] * len(row)
                return [''] * len(row)
        
        # Mostrar ranking con entidad destacada solo si existe
        if 'df_ranking_display' in locals():
            st.dataframe(df_ranking_display[["Posición", "Entidad", "Porcentaje"]], height=400)
