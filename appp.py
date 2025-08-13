import streamlit as st
from cargar_datoss import show_data_tab
from validar_formato import show_validacion_tab
from autenticar_remitente import show_autenticacion_tab
from propuestas_automatizacion import show_propuestas_tab

# Crear pestañas
tabs = st.tabs([
    "📥 Carga de Datos", 
    "✅ Validación Formato", 
    "🔐 Autenticación Remitente",
    "🔧 Transformación y Métricas", 
    "📊 Visualizaciones",
    "💡 Propuestas de Automatización"
])

with tabs[0]:
    show_data_tab()

with tabs[1]:
    show_validacion_tab()

with tabs[2]:
    show_autenticacion_tab()

# Las pestañas 3 y 4 (Transformación y Visualizaciones) quedan para después
with tabs[5]:
    show_propuestas_tab()
