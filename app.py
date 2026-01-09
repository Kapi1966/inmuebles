import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Gestor Inmobiliario Pro", layout="wide")

# --- CONFIGURACIÓN DE CONEXIONES ---
SHEET_ID = "1N6trH41YU4Edkvy-9XBWb4Zs7_AO25zKwoLq3hsOqmo"
URL_LECTURA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
URL_ESCRITURA = "https://script.google.com/macros/s/AKfycbyndiXJR1Lc4sf-Ighx-n9jz81TOFReIDVn65Y0I3TNHpqKsmdnH6fchznAavdHEYln5w/exec" 

# --- SEGURIDAD ---
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso Privado")
    passw = st.text_input("Contraseña", type="password")
    if st.button("Entrar"):
        if passw == "inmo2026":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
else:
    # --- CALCULADORA EN BARRA LATERAL ---
    with st.sidebar:
        st.header("🧮 Plusvalía Estimada")
        v_suelo = st.number_input("Valor Suelo (€)", min_value=0, value=50000)
        años = st.slider("Años propiedad", 1, 20, 5)
        if st.button("Calcular"):
            # Cálculo simple objetivo (aprox 3% anual sobre valor suelo al 30% impuesto)
            res = (v_suelo * (años * 0.03)) * 0.30
            st.metric("Total estimado", f"{res:,.2f} €")
            st.caption("Cálculo orientativo")

    st.title("🏠 Panel de Control Inmobiliario")

    # LEER DATOS
    try:
        df = pd.read_csv(URL_LECTURA)
    except:
        df = pd.DataFrame(columns=["Fecha", "Inmueble", "Referencia", "IBI", "Luz", "Agua"])

    # FORMULARIO DE ALTA
    with st.expander("➕ Añadir Inmueble"):
        with st.form("nuevo"):
            c1, c2 = st.columns(2)
            n_inmueble = c1.text_input("Nombre / Alias")
            n_ref = c2.text_input("Ref. Catastral")
            if st.form_submit_button("Registrar"):
                payload = {
                    "action": "create", "fecha": pd.Timestamp.now().strftime("%d/%m/%Y"),
                    "inmueble": n_inmueble, "referencia": n_ref,
                    "ibi": "Pendiente", "luz": "Pendiente", "agua": "Pendiente"
                }
                requests.post(URL_ESCRITURA, json=payload)
                st.rerun()

    # LISTADO Y EDICIÓN
    st.subheader("📋 Inmuebles Registrados")
    opciones = ["Pendiente", "En trámite", "Pagado", "Completado"]

    for index, row in df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])
            
            col1.write(f"**{row['Inmueble']}**")
            col1.caption(f"Ref: {row['Referencia']}")

            # Lógica de seguridad para evitar ValueError
            def get_index(val, lista):
                return lista.index(val) if val in lista else 0

            # Selectores de estado
            n_ibi = col2.selectbox("IBI", ["Pendiente", "Pagado"], index=get_index(row['IBI'], ["Pendiente", "Pagado"]), key=f"ibi_{index}")
            n_luz = col3.selectbox("Luz", opciones, index=get_index(row['Luz'], opciones), key=f"luz_{index}")
            n_agua = col4.selectbox("Agua", opciones, index=get_index(row['Agua'], opciones), key=f"agua_{index}")

            # Botones de Guardar y Borrar
            if col5.button("💾", key=f"s_{index}"):
                p = {"action": "update", "inmueble": row['Inmueble'], "ibi": n_ibi, "luz": n_luz, "agua": n_agua}
                requests.post(URL_ESCRITURA, json=p)
                st.rerun()
                
            if col5.button("🗑️", key=f"d_{index}"):
                p = {"action": "delete", "inmueble": row['Inmueble']}
                requests.post(URL_ESCRITURA, json=p)
                st.rerun()
            st.divider()


