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
            
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
                label="Cambio en niveles satisfactorios (Lenguaje)",
                value=f"{valor_2017:.1f}%",
                delta=f"{cambio:.1f}%",
                help="Cambio en el porcentaje de estudiantes en niveles III y IV entre 2015 y 2017"
            )
        else:
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
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
            
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
                label=f"Brecha entre estados 2017 (Lenguaje)",
                value=f"{brecha:.1f}%",
                delta=None,
                help=f"Diferencia entre {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%) y {peor_estado['estado']} ({peor_estado['valor']:.1f}%)"
            )
            
            # Mostrar mejor y peor estado
            st.caption(f"Mejor: {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%)")
            st.caption(f"Peor: {peor_estado['estado']} ({peor_estado['valor']:.1f}%)")
        else:
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
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
            
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
                label="Tendencia 2015-2017 (Lenguaje)",
                value=f"{tendencia:.2f}%/año",
                delta=f"{tendencia:.2f}%",
                delta_color="normal",
                help="Cambio promedio anual en el porcentaje de estudiantes en niveles satisfactorios"
            )
        else:
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
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
            
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
                label="Cambio en niveles satisfactorios (Matemáticas)",
                value=f"{valor_2017:.1f}%",
                delta=f"{cambio:.1f}%",
                help="Cambio en el porcentaje de estudiantes en niveles III y IV entre 2015 y 2017"
            )
        else:
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
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
            
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
                label=f"Brecha entre estados 2017 (Matemáticas)",
                value=f"{brecha:.1f}%",
                delta=None,
                help=f"Diferencia entre {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%) y {peor_estado['estado']} ({peor_estado['valor']:.1f}%)"
            )
            
            # Mostrar mejor y peor estado
            st.caption(f"Mejor: {mejor_estado['estado']} ({mejor_estado['valor']:.1f}%)")
            st.caption(f"Peor: {peor_estado['estado']} ({peor_estado['valor']:.1f}%)")
        else:
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
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
            
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
                label="Tendencia 2015-2017 (Matemáticas)",
                value=f"{tendencia:.2f}%/año",
                delta=f"{tendencia:.2f}%",
                delta_color="normal",
                help="Cambio promedio anual en el porcentaje de estudiantes en niveles satisfactorios"
            )
        else:
            leyenda = "(Promedio de calificación)" if año == 2022 else "(Porcentaje satisfactorio)"
st.metric(label=f"Lenguaje {leyenda}", value=f"{porcentaje_lenguaje:.1f}")
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
