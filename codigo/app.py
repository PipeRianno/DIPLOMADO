import streamlit as st

from cargar_datos import show_data_tab
from transformacion import show_transform_tab
from visualizaciones import show_visualization_tab

# Crear pestañas en el cuerpo de la aplicación
tabs = st.tabs(["📥 Carga de Datos", "🔧 Transformación y Métricas", "📊 Visualizaciones", "🗺️ Mapa"])

# Mostrar contenido en cada pestaña
with tabs[0]:
    show_data_tab()

with tabs[1]:
    show_transform_tab()

with tabs[2]:
    show_visualization_tab()

with tabs[3]:
    st.subheader("🗺️ Mapa")
    st.write("Aquí irá el contenido del mapa.")

from mapa import cargar_divipola, unir_datos, graficar_mapa

with tabs[3]:
    st.subheader("🗺️ Mapa interactivo")

    if 'df_raw' not in st.session_state:
        st.warning("Primero debes cargar los datos en la pestaña '📥 Carga de Datos'.")
    else:
        df_men = st.session_state['df_raw']
        df_divipola = cargar_divipola()

        if not df_divipola.empty:
            df_merged = unir_datos(df_men, df_divipola)

            columnas_numericas = df_merged.select_dtypes(include='number').columns.tolist()
            if columnas_numericas:
                columna_valor = st.selectbox("Selecciona la variable a visualizar:", columnas_numericas)
                graficar_mapa(df_merged, columna_valor, f"Mapa: {columna_valor}")
            else:
                st.warning("No hay columnas numéricas disponibles para graficar.")
