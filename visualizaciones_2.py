import streamlit as st
import pandas as pd
import plotly.express as px
import os
import unidecode

# ==========================
# 🎨 PALETA DE COLORES
# ==========================

UST_BLUE = "#002855"
UST_YELLOW = "#FFD100"
UST_GRAY = "#F5F5F5"
UST_WHITE = "#FFFFFF"

st.markdown(f"""
    <style>
    .main {{
        background-color: {UST_GRAY};
    }}
    .stApp {{
        background-color: {UST_WHITE};
        color: #000000;
        font-family: 'Segoe UI', sans-serif;
    }}
    .stButton>button {{
        background-color: {UST_YELLOW};
        color: black;
        font-weight: bold;
        border-radius: 10px;
        padding: 0.5em 1em;
    }}
    .stTabs [data-baseweb="tab"] {{
        font-weight: bold;
        background-color: {UST_WHITE};
        color: {UST_BLUE};
        border-radius: 6px 6px 0 0;
        border: 1px solid #CCC;
    }}
    </style>
""", unsafe_allow_html=True)

# ==========================
# 🔧 FUNCIONES DE LIMPIEZA
# ==========================
def normalizar_texto(texto: str) -> str:
    if pd.isna(texto):
        return texto
    txt = unidecode.unidecode(texto.strip().lower())
    txt = txt.replace(".", "").replace(",", "")
    return txt

def corregir_departamentos(df: pd.DataFrame) -> pd.DataFrame:
    if "nombre_departamento" in df.columns:
        df["nombre_departamento"] = df["nombre_departamento"].astype(str)
        df["nombre_departamento"] = df["nombre_departamento"].str.replace(r"bogota.*", "bogota", regex=True)
        df["nombre_departamento"] = df["nombre_departamento"].str.replace(r"san andres.*", "san andres", regex=True)
        df["nombre_departamento"] = df["nombre_departamento"].str.replace(r"valle del cauca", "valle", regex=True)
    return df

# ==========================
# 📊 FUNCIÓN PRINCIPAL
# ==========================
def show_visualizaciones_tab():
    st.title("📊 Análisis Avanzado: Cobertura y Matriculación")

    ruta_datos = r"C:\Users\juanF\proyectos_diplomado\DIPLOMADO\datos"

    # ==========================
    # 1️⃣ CARGA DE DATOS LIMPIOS
    # ==========================
    try:
        df_clean = pd.read_csv(os.path.join(ruta_datos, "Educacion_Limpio.csv"))
        df_clean["codigo_departamento"] = df_clean["codigo_departamento"].astype(str)
        df_clean["nombre_departamento"] = df_clean["nombre_departamento"].apply(normalizar_texto)
        df_clean = corregir_departamentos(df_clean)
        st.success(f"✅ Datos educativos cargados: {df_clean.shape[0]:,} registros.")
    except FileNotFoundError:
        st.error("❌ No se encontró 'Educacion_Limpio.csv' en la carpeta datos.")
        return

    # ==========================
    # 2️⃣ CARGA Y UNIÓN DE POBLACIÓN
    # ==========================
    try:
        df_pob1 = pd.read_excel(os.path.join(ruta_datos, "Info_2005_2019.xlsx"))
        df_pob2 = pd.read_excel(os.path.join(ruta_datos, "Info_2020_2035.xlsx"))
        df_poblacion = pd.concat([df_pob1, df_pob2], ignore_index=True)
    except FileNotFoundError:
        st.error("❌ No se encontraron los archivos de población en la carpeta datos.")
        return

    df_poblacion = df_poblacion.rename(columns={
        "DP": "codigo_departamento",
        "DPNOM": "nombre_departamento",
        "AÑO": "anio",
        "Población": "poblacion_proyectada"
    })
    df_poblacion["codigo_departamento"] = df_poblacion["codigo_departamento"].astype(str)
    df_poblacion["nombre_departamento"] = df_poblacion["nombre_departamento"].apply(normalizar_texto)
    df_poblacion = corregir_departamentos(df_poblacion)
    df_poblacion = df_poblacion[
        ["codigo_departamento", "nombre_departamento", "anio", "poblacion_proyectada"]
    ]

    # ==========================
    # 3️⃣ UNIÓN FINAL
    # ==========================
    df_union = df_clean.merge(
        df_poblacion,
        on=["codigo_departamento", "nombre_departamento", "anio"],
        how="left"
    )
    st.info(f"✅ Datos unidos: {df_union.shape[0]:,} registros finales.")

    # Filtros interactivos
    anios = sorted(df_union["anio"].unique())
    departamentos = sorted(df_union["nombre_departamento"].unique())
    col1, col2 = st.columns(2)
    anio_sel = col1.selectbox("📆 Selecciona el año:", options=["Todos"] + list(anios))
    depto_sel = col2.selectbox("🏛️ Selecciona un departamento:", options=["Todos"] + list(departamentos))

    df_filtro = df_union.copy()
    if anio_sel != "Todos":
        df_filtro = df_filtro[df_filtro["anio"] == anio_sel]
    if depto_sel != "Todos":
        df_filtro = df_filtro[df_filtro["nombre_departamento"] == depto_sel]

    # ==========================
    # 4️⃣ ANÁLISIS TEMPORAL
    # ==========================
    st.subheader("📈 Evolución Temporal Nacional")
    tendencia = df_union.groupby("anio")[["tasa_matriculacion_5_16", "cobertura_neta_total"]].mean().reset_index()

    fig_tendencia = px.line(
        tendencia,
        x="anio",
        y=["tasa_matriculacion_5_16", "cobertura_neta_total"],
        markers=True,
        title="Evolución Nacional: Tasa de Matriculación y Cobertura Neta",
        labels={"value": "Porcentaje (%)", "anio": "Año", "variable": "Indicador"},
        color_discrete_sequence=[UST_BLUE, UST_YELLOW]
    )
    st.plotly_chart(fig_tendencia, use_container_width=True)

    # ==========================
    # 5️⃣ TOP DEPARTAMENTOS
    # ==========================
    st.subheader("🏛️ Top 10 Departamentos por Cobertura Neta")
    top_deptos = df_union.groupby("nombre_departamento")[["cobertura_neta_total"]].mean().reset_index()
    top_deptos = top_deptos.sort_values(by="cobertura_neta_total", ascending=False).head(10)

    fig_top = px.bar(
        top_deptos,
        x="nombre_departamento",
        y="cobertura_neta_total",
        color="cobertura_neta_total",
        color_continuous_scale="Blues",
        title="Top 10 Departamentos por Cobertura Neta Total Promedio"
    )
    st.plotly_chart(fig_top, use_container_width=True)

    # ==========================
    # 6️⃣ MAPA INTERACTIVO
    # ==========================
    st.subheader(f"🗺️ Cobertura Neta por Departamento ({anio_sel if anio_sel != 'Todos' else 'Último año'})")
    ultimo_anio = anio_sel if anio_sel != "Todos" else df_union["anio"].max()
    mapa_data = df_union[df_union["anio"] == ultimo_anio].groupby(
        "nombre_departamento"
    )[["cobertura_neta_total"]].mean().reset_index()

    fig_mapa = px.choropleth(
        mapa_data,
        locations="nombre_departamento",
        locationmode="geojson-id",
        geojson="https://raw.githubusercontent.com/marcovega/colombia-json/master/colombia.json",
        color="cobertura_neta_total",
        hover_name="nombre_departamento",
        color_continuous_scale="Blues",
        title=f"Cobertura Neta Total por Departamento ({ultimo_anio})"
    )
    fig_mapa.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig_mapa, use_container_width=True)

    # ==========================
    # 7️⃣ RELACIÓN COBERTURA VS POBLACIÓN
    # ==========================
    st.subheader("🔍 Relación Cobertura Neta vs Población Proyectada")
    scatter_rel = df_union.groupby("nombre_departamento")[["cobertura_neta_total", "poblacion_proyectada"]].mean().reset_index()

    fig_scatter = px.scatter(
        scatter_rel,
        x="poblacion_proyectada",
        y="cobertura_neta_total",
        size="poblacion_proyectada",
        color="cobertura_neta_total",
        hover_name="nombre_departamento",
        title="Cobertura Neta vs Población Proyectada"
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

    # ==========================
    # 8️⃣ DESCARGA
    # ==========================
    st.subheader("📥 Descarga de Datos Unidos")
    st.dataframe(df_union.head(50))
    csv_export = df_union.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Descargar CSV con Datos Unidos",
        data=csv_export,
        file_name="Educacion_Union_Poblacion.csv",
        mime="text/csv"
    )
