import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Gestor Inmo Pro", layout="wide")

SHEET_ID = "1N6trH41YU4Edkvy-9XBWb4Zs7_AO25zKwoLq3hsOqmo"
URL_LECTURA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
URL_ESCRITURA = "https://script.google.com/macros/s/AKfycbzV-DySuoKLBgg0Mv8aOBKHnWSaOGXDA56e5VqJh9afGpSknLm1bBtXqx6ktyOnjVGXdQ/exec" # <--- Pon la nueva aquí

if 'autenticado' not in st.session_state: st.session_state.autenticado = False

if not st.session_state.autenticado:
    # ... (Código de login igual que antes) ...
    passw = st.text_input("Clave", type="password")
    if st.button("Entrar"):
        if passw == "inmo2026":
            st.session_state.autenticado = True
            st.rerun()
else:
    st.title("🏠 Gestión y Edición de Inmuebles")

    # LEER DATOS
    try: df = pd.read_csv(URL_LECTURA)
    except: df = pd.DataFrame(columns=["Fecha", "Inmueble", "Referencia", "IBI", "Luz", "Agua"])

    # FORMULARIO ALTA (NUEVO)
    with st.expander("➕ DAR DE ALTA NUEVO"):
        with st.form("alta"):
            nombre = st.text_input("Nombre")
            ref = st.text_input("Referencia")
            if st.form_submit_button("Guardar"):
                payload = {"action": "create", "fecha": pd.Timestamp.now().strftime("%d/%m/%Y"), "inmueble": nombre, "referencia": ref, "ibi": "Pendiente", "luz": "Pendiente", "agua": "Pendiente"}
                requests.post(URL_ESCRITURA, json=payload)
                st.rerun()

    # LISTADO CON EDICIÓN
    st.subheader("📋 Panel de Control")
    for index, row in df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])
            
            col1.write(f"**{row['Inmueble']}** ({row['Referencia']})")
            
            # Selectores para cambiar estado en tiempo real
            nuevo_ibi = col2.selectbox(f"IBI", ["Pendiente", "Pagado"], index=0 if row['IBI']=="Pendiente" else 1, key=f"ibi_{index}")
            nuevo_luz = col3.selectbox(f"Luz", ["Pendiente", "En trámite", "Completado"], index=["Pendiente", "En trámite", "Completado"].index(row['Luz']), key=f"luz_{index}")
            nuevo_agua = col4.selectbox(f"Agua", ["Pendiente", "En trámite", "Completado"], index=["Pendiente", "En trámite", "Completado"].index(row['Agua']), key=f"agua_{index}")
            
            # Botones de Acción
            btn_col1, btn_col2 = st.columns([1,1])
            if col5.button("💾", key=f"upd_{index}", help="Actualizar estados"):
                payload = {"action": "update", "inmueble": row['Inmueble'], "ibi": nuevo_ibi, "luz": nuevo_luz, "agua": nuevo_agua}
                requests.post(URL_ESCRITURA, json=payload)
                st.success("Actualizado")
                st.rerun()
                
            if col5.button("🗑️", key=f"del_{index}", help="Borrar inmueble"):
                payload = {"action": "delete", "inmueble": row['Inmueble']}
                requests.post(URL_ESCRITURA, json=payload)
                st.warning("Borrado")
                st.rerun()
            st.divider()
