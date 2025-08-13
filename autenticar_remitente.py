import pandas as pd
import streamlit as st

# Lista blanca de correos autorizados (puede cambiarse luego para leer desde CSV)
CORREOS_AUTORIZADOS = [
    "francy.gonzalez@rappi.com" 
 
]

def show_autenticacion_tab():
    st.header("🔐 Autenticación de remitente")
    if "archivo_excel" not in st.session_state:
        st.warning("Primero carga el archivo en la pestaña 📥 Carga de Datos")
        return

    df = pd.read_excel(st.session_state["archivo_excel"], sheet_name="Solicitudes de los Comercios")

    if "Correo que remite la solicitud" not in df.columns:
        st.error("No se encontró la columna 'Correo que remite la solicitud'")
        return

    df["Correo válido"] = df["Correo que remite la solicitud"].isin(CORREOS_AUTORIZADOS)
    
    # Resumen
    total = len(df)
    validos = df["Correo válido"].sum()
    invalidos = total - validos

    st.info(f"📊 Total registros: {total}")
    st.success(f"✅ Correos autorizados: {validos}")
    st.error(f"❌ Correos no autorizados: {invalidos}")

    # Mostrar detalle de no autorizados
    df_invalidos = df[~df["Correo válido"]]
    if not df_invalidos.empty:
        st.subheader("❌ Correos no autorizados")
        st.dataframe(df_invalidos[["Correo que remite la solicitud"]].drop_duplicates())

        # Botón de descarga
        csv = df_invalidos.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar lista de no autorizados", csv, "correos_no_autorizados.csv", "text/csv")
