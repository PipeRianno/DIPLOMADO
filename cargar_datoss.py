import streamlit as st

def show_data_tab():
    st.header("📥 Cargar archivo de solicitudes")
    uploaded_file = st.file_uploader(
        "Selecciona el archivo Excel", 
        type=["xlsx"], 
        help="Debe contener la hoja 'Solicitudes de los Comercios'"
    )
    if uploaded_file:
        st.session_state["archivo_excel"] = uploaded_file
        st.success("Archivo cargado correctamente")
