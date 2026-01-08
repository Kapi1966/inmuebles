import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Gestor Inmo Pro", layout="wide")

# 1. CONEXIÓN A LA BASE DE DATOS (Google Sheets)
# Debes poner la URL de tu hoja de Google Sheets aquí
url = "https://docs.google.com/spreadsheets/d/1N6trH41YU4Edkvy-9XBWb4Zs7_AO25zKwoLq3hsOqmo/edit?gid=0#gid=0" 

conn = st.connection("gsheets", type=GSheetsConnection)

# 2. SEGURIDAD
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso")
    passw = st.text_input("Clave", type="password")
    if st.button("Entrar"):
        if passw == "inmo2026":
            st.session_state.autenticado = True
            st.rerun()
else:
    st.title("🏠 Gestión Inmobiliaria Sincronizada")

    # Leer datos actuales de Google Sheets
    try:
        df_existente = conn.read(spreadsheet=url)
    except:
        df_existente = pd.DataFrame()

    # FORMULARIO DE ALTA
    with st.form("nuevo_piso"):
        st.subheader("Registrar Inmueble")
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre/Alias")
        ref = col2.text_input("Ref. Catastral")
        
        st.write("**Estado de Trámites**")
        c1, c2, c3 = st.columns(3)
        ibi = c1.selectbox("IBI", ["Pendiente", "Pagado"])
        luz = c2.selectbox("Luz", ["Pendiente", "En trámite", "Completado"])
        agua = c3.selectbox("Agua", ["Pendiente", "En trámite", "Completado"])
        
        btn = st.form_submit_button("Guardar en la Nube")

    if btn:
        if nombre:
            # Crear nueva fila
            nueva_fila = pd.DataFrame([{
                "Fecha": pd.Timestamp.now().strftime("%d/%m/%Y"),
                "Inmueble": nombre,
                "Referencia": ref,
                "IBI": ibi,
                "Luz": luz,
                "Agua": agua
            }])
            
            # Unir con lo anterior y guardar en Google Sheets
            df_final = pd.concat([df_existente, nueva_fila], ignore_index=True)
            conn.update(spreadsheet=url, data=df_final)
            st.success("✅ Guardado en Google Sheets y actualizado para todos los PCs")
            st.rerun()

    # MOSTRAR TABLA REAL
    st.write("### 📋 Listado en Tiempo Real")
    if not df_existente.empty:
        st.dataframe(df_existente, use_container_width=True)
    else:
        st.info("La base de datos está vacía.")

