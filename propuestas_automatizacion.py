import streamlit as st

def show_propuestas_tab():
    st.header("💡 Propuestas para Automatización del Proceso de Reversos")
    st.write("""
    Aquí puedes ver y simular cómo se podrían automatizar los pasos del proceso
    usando Google Apps Script, APIs y flujos automáticos.
    """)

    # Lista de propuestas con acciones
    propuestas = [
        {
            "item": "0. Validar formato de solicitud",
            "descripcion": """
            - **Apps Script**: Leer archivo desde Google Drive y validar formato (columnas, tipos de datos).
            - **Automatización**: Enviar correo automático al solicitante si hay errores, adjuntando reporte.
            """,
            "accion": "Ejecutar validación de formato"
        },
        {
            "item": "1. Autenticación del remitente",
            "descripcion": """
            - **Apps Script**: Usar Gmail API para identificar remitente y compararlo con lista blanca en Google Sheets.
            - **Automatización**: Responder automáticamente si no está autorizado.
            """,
            "accion": "Verificar remitente"
        },
        {
            "item": "2. Validación de procedencia",
            "descripcion": """
            - **Apps Script**: Consultar API interna o base de datos para validar CU, autorización y valores.
            - **Automatización**: Marcar en Google Sheets como 'Procedente' o 'No procedente'.
            """,
            "accion": "Validar procedencia"
        },
        {
            "item": "3. Reversar transacciones masivamente",
            "descripcion": """
            - **API Interna**: Endpoint para procesar reversos en lote.
            - **Automatización**: Apps Script llama a la API y guarda resultados.
            """,
            "accion": "Ejecutar reverso masivo"
        },
        {
            "item": "4. Responder al comercio solicitante",
            "descripcion": """
            - **Apps Script + Gmail API**: Enviar correo con detalle de reversos y rechazos.
            - **Automatización**: Adjuntar PDF o Excel generado automáticamente.
            """,
            "accion": "Enviar correo al comercio"
        }
    ]

    # Mostrar cada propuesta con su botón
    for prop in propuestas:
        st.subheader(prop["item"])
        st.markdown(prop["descripcion"])

        if st.button(prop["accion"], key=prop["item"]):
            st.info(f"🔄 Simulando: {prop['accion']}...")
            st.success(f"✅ Acción '{prop['accion']}' completada en la simulación.")
