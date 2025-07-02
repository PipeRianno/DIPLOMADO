# mapa.py
import pandas as pd
import plotly.express as px
import requests
import streamlit as st

# -------------------------------------------------------------------
# Función: cargar_divipola()
# -------------------------------------------------------------------
def cargar_divipola() -> pd.DataFrame:
    url = "https://www.datos.gov.co/resource/gdxc-w37w.json?$limit=50000"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        df = pd.DataFrame(data)
        st.success(f"DIVIPOLA cargado con {len(df)} filas.")
        return df
    except Exception as e:
        st.error(f"Error al cargar DIVIPOLA: {e}")
        return pd.DataFrame()

# -------------------------------------------------------------------
# Función: unir_datos()
# -------------------------------------------------------------------
def unir_datos(df_men: pd.DataFrame, df_divipola: pd.DataFrame) -> pd.DataFrame:
    # Preparar claves
    df_men['cod_departamento'] = df_men['cod_departamento'].astype(str)
    df_men['cod_municipio'] = df_men['cod_municipio'].astype(str)

    df_divipola['codigo_departamento'] = df_divipola['codigo_departamento'].astype(str)
    df_divipola['codigo_municipio'] = df_divipola['codigo_municipio'].astype(str)

    # Renombrar para facilitar el merge
    df_divipola = df_divipola.rename(columns={
        'codigo_departamento': 'cod_departamento',
        'codigo_municipio': 'cod_municipio',
        'municipio': 'municipio_divipola'
    })

    # Hacer la unión
    df_merged = pd.merge(df_men, df_divipola,
                         on=['cod_departamento', 'cod_municipio'],
                         how='left')

    return df_merged

# -------------------------------------------------------------------
# Función: graficar_mapa()
# -------------------------------------------------------------------
def graficar_mapa(df: pd.DataFrame, columna_valor: str, titulo: str):
    # Convertir coordenadas a numérico
    df['latitud'] = pd.to_numeric(df['latitud'], errors='coerce')
    df['longitud'] = pd.to_numeric(df['longitud'], errors='coerce')

    fig = px.scatter_mapbox(
        df,
        lat='latitud',
        lon='longitud',
        color=columna_valor,
        hover_name='municipio',
        zoom=4,
        height=700,
        mapbox_style="carto-positron",
        title=titulo
    )
    st.plotly_chart(fig, use_container_width=True)
