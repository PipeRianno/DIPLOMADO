import streamlit as st

from cargar_datos import show_data_tab
from transformacion import show_transform_tab
from visualizaciones import show_visualization_tab
from mapa import show_map_tab
from visualizaciones_2 import show_visualizaciones_tab  # ✅ Nuevo import

# Crear pestañas en el cuerpo de la aplicación
tabs = st.tabs([
    "📥 Carga de Datos",
    "🔧 Transformación y Métricas",
    "📊 Visualizaciones",
    "🗺️ Mapa",
    "📈 Visualizaciones Avanzadas"  # ✅ Nuevo tab
])

# Mostrar contenido en cada pestaña
with tabs[0]:
    show_data_tab()

with tabs[1]:
    show_transform_tab()

with tabs[2]:
    show_visualization_tab()

with tabs[3]:
    show_map_tab()

with tabs[4]:  # ✅ Nueva pestaña
    show_visualizaciones_tab()
