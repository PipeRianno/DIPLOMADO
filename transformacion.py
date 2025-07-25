import streamlit as st
import pandas as pd
import plotly.express as px
import unidecode
import io

# Colores oficiales Universidad Santo Tomás
UST_BLUE = "#002855"
UST_YELLOW = "#FFD100"
UST_GRAY = "#F5F5F5"
UST_WHITE = "#FFFFFF"

# Estilo general
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
    .stDownloadButton>button {{
        background-color: {UST_BLUE};
        color: white;
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

# =========================
# 🔧 Funciones de Limpieza
# =========================
def normalizar_texto(texto: str) -> str:
    """Minúsculas, sin tildes, sin puntos/comas."""
    if pd.isna(texto):
        return texto
    txt = unidecode.unidecode(texto.strip().lower())
    txt = txt.replace(".", "").replace(",", "")
    return txt

def corregir_departamentos(df: pd.DataFrame) -> pd.DataFrame:
    """Unifica nombres de departamentos problemáticos."""
    df["departamento"] = df["departamento"].astype(str)
    df["departamento"] = df["departamento"].str.replace(r"bogota.*", "bogota", regex=True)
    df["departamento"] = df["departamento"].str.replace(r"san andres.*", "san andres", regex=True)
    df["departamento"] = df["departamento"].str.replace(r"valle del cauca", "valle", regex=True)
    return df

def limpiar_metricas(df: pd.DataFrame) -> pd.DataFrame:
    """Convierte a numérico y elimina negativos (pero mantiene >100)."""
    for col in ["tasa_matriculaci_n_5_16", "cobertura_neta", "cobertura_bruta"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df.loc[df[col] < 0, col] = None
    return df

# =========================
# 🖥️ Dashboard Principal
# =========================
def show_transform_tab():
    st.title("📊 Dashboard Educativo: Modelo Estrella")

    if 'df_raw' not in st.session_state:
        st.warning("🔺 Primero debes cargar los datos desde la pestaña correspondiente.")
        return

    df = st.session_state['df_raw'].copy()

    # --- Limpieza inicial de NACIONAL ---
    tabla_deptos = (
        df.query("departamento != 'NACIONAL'")
          [['c_digo_departamento', 'departamento']]
          .drop_duplicates()
          .groupby('c_digo_departamento')
          .sample(n=1, random_state=1)
          .reset_index()
          .drop(columns='index')
    )

    df = (
        df.query("departamento != 'NACIONAL'")
          .drop(columns='departamento')
          .merge(tabla_deptos, on='c_digo_departamento', how='left')
    )

    st.markdown("""
    ### 🛠️ Etapas del Flujo de Trabajo
    1. **Limpieza de datos**
    2. **Construcción de dimensiones**
    3. **Modelo estrella y tabla de hechos**
    4. **Visualización y métricas clave**
    5. **Descarga y resumen detallado**
    """)

    # =========================
    # 1️⃣ Limpieza y Validación
    # =========================
    st.markdown("---")
    st.subheader("1️⃣ Limpieza y Validación de Datos")

    columnas_relevantes = [
        'a_o', 'departamento', 'municipio', 'c_digo_departamento',
        'poblaci_n_5_16', 'tasa_matriculaci_n_5_16',
        'cobertura_neta', 'cobertura_bruta'
    ]
    columnas_faltantes = [col for col in columnas_relevantes if col not in df.columns]
    if columnas_faltantes:
        st.error(f"❌ Columnas faltantes: {columnas_faltantes}")
        return

    df = df[columnas_relevantes]

    # --- Normalización de texto ---
    for col in ["departamento", "municipio"]:
        df[col] = df[col].astype(str).apply(normalizar_texto)

    df = corregir_departamentos(df)
    df = limpiar_metricas(df)
    df = df.drop_duplicates()
    df_clean = df.dropna()

    col1, col2 = st.columns(2)
    col1.metric("Registros originales", len(st.session_state['df_raw']))
    col2.metric("Registros válidos", len(df_clean))
    st.session_state['df_clean'] = df_clean

    # =========================
    # 2️⃣ Dimensiones
    # =========================
    st.markdown("---")
    st.subheader("2️⃣ Dimensiones del Modelo Estrella")

    def crear_dimension(df, cols, nombre, sort_col=None):
        dim = df[cols].drop_duplicates()
        if sort_col:
            dim = dim.sort_values(by=sort_col)
        dim = dim.reset_index(drop=True)
        dim[f"id_{nombre}"] = dim.index + 1
        return dim[[f"id_{nombre}"] + cols]

    dim_tiempo = crear_dimension(df_clean, ['a_o'], 'tiempo', sort_col='a_o')
    dim_geo = crear_dimension(df_clean, ['c_digo_departamento', 'departamento', 'municipio'],
                              'geo', sort_col='c_digo_departamento')

    col3, col4 = st.columns(2)
    col3.metric("Dimensión Tiempo", len(dim_tiempo))
    col4.metric("Dimensión Geográfica", len(dim_geo))

    st.session_state['dim_geo'] = dim_geo
    st.session_state['dim_tiempo'] = dim_tiempo

    # =========================
    # 3️⃣ Tabla de Hechos
    # =========================
    st.markdown("---")
    st.subheader("3️⃣ Tabla de Hechos")

    df_fact = df_clean.merge(dim_tiempo, on='a_o') \
                      .merge(dim_geo, on=['departamento', 'municipio', 'c_digo_departamento'], how='inner')
    df_fact = df_fact[[
        'id_tiempo', 'id_geo',
        'poblaci_n_5_16', 'tasa_matriculaci_n_5_16',
        'cobertura_neta', 'cobertura_bruta'
    ]]

    st.success(f"✅ Tabla de hechos construida con {len(df_fact):,} registros.")
    st.session_state['df_fact'] = df_fact

    # =========================
    # 4️⃣ Indicadores y Visualizaciones
    # =========================
    st.markdown("---")
    st.subheader("4️⃣ Indicadores y Visualizaciones")

    escolaridad_prom = df_fact.groupby('id_geo')[['tasa_matriculaci_n_5_16']].mean().reset_index()
    escolaridad_prom = escolaridad_prom.merge(dim_geo, on='id_geo')
    top_mpios = escolaridad_prom.sort_values(by='tasa_matriculaci_n_5_16', ascending=False).head(10)

    fig = px.bar(
        top_mpios,
        x='municipio',
        y='tasa_matriculaci_n_5_16',
        title='Top 10 Municipios con Mayor Tasa de Escolaridad (5-16 años)',
        labels={'tasa_matriculaci_n_5_16': 'Tasa de Escolaridad (%)'},
        color_discrete_sequence=[UST_BLUE]
    )
    st.plotly_chart(fig, use_container_width=True)

    cobertura_depto = df_fact.merge(dim_geo, on='id_geo') \
        .groupby('departamento')['cobertura_neta'].mean().sort_values(ascending=False).head(10)
    st.markdown("**🏛️ Top Departamentos por Cobertura Neta Promedio**")
    st.dataframe(cobertura_depto.reset_index())

    # =========================
    # 5️⃣ Descarga y Resumen
    # =========================
    st.markdown("---")
    st.subheader("5️⃣ Vista y Descarga de la Tabla de Hechos")

    st.dataframe(df_fact.head(50))
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_fact.to_excel(writer, index=False, sheet_name='TablaHechos')
    output.seek(0)

    st.download_button(
        label="📥 Descargar Tabla de Hechos",
        data=output,
        file_name='tabla_hechos_educacion.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    st.markdown("---")
    st.subheader("📈 Resumen por Departamento y Año")

    df_fact_ext = df_fact.merge(dim_geo, on='id_geo').merge(dim_tiempo, on='id_tiempo')
    resumen = df_fact_ext.groupby(['departamento', 'a_o'])[
        ['tasa_matriculaci_n_5_16', 'cobertura_neta', 'cobertura_bruta']].mean().reset_index()
    st.dataframe(resumen.head(20))
