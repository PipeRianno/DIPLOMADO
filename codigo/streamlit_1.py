import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import requests

# Configuración general de la app
st.set_page_config(page_title="Visualización de Educación", layout="wide")
st.title("📊 Análisis de Cobertura y Matrícula en Educación")

# Función para cargar datos desde la API
@st.cache_data
def load_data():
    api_url = "https://www.datos.gov.co/resource/nudc-7mev.json?$limit=50000"
    try:
        st.info(f"📥 Extrayendo datos desde la API...")
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        st.success(f"✅ Datos cargados exitosamente: {len(df)} filas.")
        return df
    except Exception as e:
        st.error(f"❌ Error al cargar datos: {e}")
        return pd.DataFrame()

# Cargar datos
df_raw = load_data()

# Convertir columnas necesarias
numeric_cols = ['tasa_matriculaci_n_5_16', 'cobertura_neta', 'cobertura_bruta']
for col in numeric_cols:
    if col in df_raw.columns:
        df_raw[col] = pd.to_numeric(df_raw[col], errors='coerce')

# Menú lateral
menu = st.sidebar.selectbox(
    "Selecciona una visualización",
    [
        "📉 Histograma: Tasa de Matrícula 5-16",
        "📦 Boxplot: Cobertura Neta por Departamento",
        "📍 Dispersión: Matrícula vs Cobertura Bruta",
        "📊 Barras: Promedio Matrícula por Departamento"
    ]
)

# Visualizaciones
if menu == "📉 Histograma: Tasa de Matrícula 5-16":
    st.header("Distribución de la Tasa de Matrícula (5-16 años)")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(df_raw['tasa_matriculaci_n_5_16'].dropna(), bins=30, kde=True, ax=ax)
    ax.set_xlabel('Tasa de Matriculación 5-16')
    ax.set_ylabel('Frecuencia')
    ax.grid(True)
    st.pyplot(fig)

elif menu == "📦 Boxplot: Cobertura Neta por Departamento":
    st.header("Cobertura Neta por Departamento (Top 8)")
    fig, ax = plt.subplots(figsize=(12, 6))
    top_deptos = df_raw['departamento'].value_counts().index[:8]
    sns.boxplot(
        data=df_raw[df_raw['departamento'].isin(top_deptos)],
        x='departamento',
        y='cobertura_neta',
        ax=ax
    )
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
    ax.set_xlabel('Departamento')
    ax.set_ylabel('Cobertura Neta')
    ax.grid(True)
    st.pyplot(fig)

elif menu == "📍 Dispersión: Matrícula vs Cobertura Bruta":
    st.header("Relación entre Tasa de Matrícula y Cobertura Bruta")
    fig, ax = plt.subplots(figsize=(8, 6))
    sns.scatterplot(
        data=df_raw,
        x='tasa_matriculaci_n_5_16',
        y='cobertura_bruta',
        alpha=0.5,
        ax=ax
    )
    ax.set_xlabel('Tasa de Matriculación 5-16')
    ax.set_ylabel('Cobertura Bruta')
    ax.grid(True)
    st.pyplot(fig)

elif menu == "📊 Barras: Promedio Matrícula por Departamento":
    st.header("Top 10 Departamentos por Promedio de Tasa de Matrícula (5-16)")
    fig, ax = plt.subplots(figsize=(12, 6))
    promedio_depto = (
        df_raw.groupby('departamento')['tasa_matriculaci_n_5_16']
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )
    sns.barplot(x=promedio_depto.values, y=promedio_depto.index, palette='viridis', ax=ax)
    ax.set_xlabel('Promedio Tasa de Matrícula')
    ax.set_ylabel('Departamento')
    ax.grid(True, axis='x')
    st.pyplot(fig)
