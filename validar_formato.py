import pandas as pd
import re
import streamlit as st
from datetime import datetime

# Columnas esperadas
COLUMNAS_ESPERADAS = [
    "NOMBRE COMERCIO",
    "TIPO DE REVERSIÓN (TOTAL - PARCIAL)",
    "NIT COMERCIO SIN SEPARACIÓN (INLCUYENDO DÍGITO DE VERIFICACIÓN)",
    "CÓDIGO ÚNICO (8 DÍGITOS)",
    "FECHA TRANSACCIÓN AAAAMMDD",
    "4 ÚLLTIMOS DE LA TARJETA (4 digitos)",
    "FRANQUICIA (DINERS, VISA, MASTER)",
    "CÓDIGO AUTORIZACIÓN (6 digitos)",
    "CAMPO EXCLUSIVO DE DAVIVIENDA",
    "CAMPO EXCLUSIVO DE DAVIVIENDA",
    "VR COMPRA",
    "VR DE IVA",
    "IMP NAC CONSUMO",
    "VR PROPINA",
    "TOTAL VENTA \n(CAMPO FORMULADO)",
    "(APICA SOLO PARA AJUSTES PARCIALES) \n\nVR NUEVA COMPRA",
    "(APLICA SOLO PARA AJUSTES PARCIALES) \n\nVR DE IVA",
    "(APLICA SOLO PARA AJUSTES PARCIALES) \n\nIMP NAC CONSUMO",
    "(APLICA SOLO PARA AJUSTES PARCIALES) \n\nVR PROPINA",
    "(APLICA SOLO PARA AJUSTES PARCIALES) \nVR TOTAL NUEVAVENTA \n(CAMPO FORMULADO)",
    "(APLICA SOLO PARA AJUSTES PARCIALES) \n\nVR A REVERSAR",
    "Correo que remite la solicitud"
]

# Funciones de validación
def validar_nit(valor): return bool(re.fullmatch(r"\d+", str(valor)))
def validar_codigo_unico(valor): return bool(re.fullmatch(r"\d{8}", str(valor)))
def validar_fecha(valor):
    try:
        datetime.strptime(str(valor), "%Y%m%d"); return True
    except: return False
def validar_ultimos_tarjeta(valor): return bool(re.fullmatch(r"\d{4}", str(valor)))
def validar_franquicia(valor): return str(valor).upper() in ["DINERS", "VISA", "MASTER"]
def validar_codigo_autorizacion(valor): return bool(re.fullmatch(r"\d{6}", str(valor)))
def validar_valor(valor):
    try: float(valor); return True
    except: return False
def validar_correo(valor): return bool(re.fullmatch(r"[^@]+@[^@]+\.[^@]+", str(valor)))

# Mostrar la validación en Streamlit
def show_validacion_tab():
    st.header("✅ Validación de Formato")
    if "archivo_excel" not in st.session_state:
        st.warning("Primero carga el archivo en la pestaña 📥 Carga de Datos")
        return

    df = pd.read_excel(st.session_state["archivo_excel"], sheet_name="Solicitudes de los Comercios")
    faltantes = [col for col in COLUMNAS_ESPERADAS if col not in df.columns]

    if faltantes:
        st.error(f"Columnas faltantes: {faltantes}")
        return

    errores = []
    errores_formato_extra = []

    for idx, fila in df.iterrows():
        fila_errores = {}

        if not validar_nit(fila[COLUMNAS_ESPERADAS[2]]):
            fila_errores["NIT COMERCIO"] = "Formato inválido"

        if not validar_codigo_unico(fila[COLUMNAS_ESPERADAS[3]]):
            fila_errores["CÓDIGO ÚNICO"] = "Debe tener 8 dígitos"

        if not validar_fecha(fila[COLUMNAS_ESPERADAS[4]]):
            fila_errores["FECHA TRANSACCIÓN"] = "Formato AAAAMMDD inválido"

        if not validar_ultimos_tarjeta(fila[COLUMNAS_ESPERADAS[5]]):
            fila_errores["4 ÚLTIMOS TARJETA"] = "Debe tener 4 dígitos"

        if not validar_franquicia(fila[COLUMNAS_ESPERADAS[6]]):
            fila_errores["FRANQUICIA"] = "Debe ser DINERS, VISA o MASTER"

        if not validar_codigo_autorizacion(fila[COLUMNAS_ESPERADAS[7]]):
            fila_errores["CÓDIGO AUTORIZACIÓN"] = "Debe tener 6 dígitos"

        if not validar_valor(fila[COLUMNAS_ESPERADAS[10]]):
            fila_errores["VR COMPRA"] = "Debe ser numérico"

        if not validar_correo(fila[COLUMNAS_ESPERADAS[-1]]):
            fila_errores["Correo"] = "Formato inválido"

        # Validación especial desde fila 66
        if idx + 2 >= 66 and fila_errores:
            errores_formato_extra.append({"Fila": idx + 2, **fila_errores})

        if fila_errores:
            errores.append({"Fila": idx + 2, **fila_errores})

    if errores:
        st.warning(f"Se encontraron {len(errores)} registros con errores")
        df_errores = pd.DataFrame(errores)
        st.dataframe(df_errores)
        csv = df_errores.to_csv(index=False).encode("utf-8")
        st.download_button("Descargar errores en CSV", csv, "errores.csv", "text/csv")
    else:
        st.success("✅ Todos los registros cumplen con el formato")

    if errores_formato_extra:
        st.error(f"⚠ Detectadas {len(errores_formato_extra)} filas con problemas desde la fila 66")
        st.dataframe(pd.DataFrame(errores_formato_extra))
