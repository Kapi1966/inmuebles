import streamlit as st
import pandas as pd
import requests

# 1. CONFIGURACIÓN INICIAL (Siempre arriba)
st.set_page_config(page_title="Gestor Inmo Pro", layout="wide")

# 2. CONFIGURACIÓN DE CONEXIONES
# Sustituye con tu ID de hoja
SHEET_ID = "1N6trH41YU4Edkvy-9XBWb4Zs7_AO25zKwoLq3hsOqmo"
URL_LECTURA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# PEGA AQUÍ LA URL QUE TE DIO GOOGLE APPS SCRIPT (la que termina en /exec)
URL_ESCRITURA = "TU_URL_DE_APPS_SCRIPT_AQUI"

# 3. SEGURIDAD (Login)
if 'autenticado' not in st.session_state:
    st.session_state.autenticado = False

if not st.session_state.autenticado:
    st.title("🔐 Acceso")
    passw = st.text_input("Clave de Agencia", type="password")
    if st.button("Entrar"):
        if passw == "inmo2026":
            st.session_state.autenticado = True
            st.rerun()
        else:
            st.error("Clave incorrecta")
else:
    # --- LA APP EMPIEZA AQUÍ ---
    st.title("🏠 Gestión de Inmuebles Sincronizada")

    # LEER DATOS
    try:
        df_existente = pd.read_csv(URL_LECTURA)
    except:
        df_existente = pd.DataFrame(columns=["Fecha", "Inmueble", "Referencia", "IBI", "Luz", "Agua"])

    # FORMULARIO DE ALTA
    with st.form("nuevo_piso"):
        st.subheader("Registrar Nuevo Inmueble")
        col1, col2 = st.columns(2)
        nombre = col1.text_input("Nombre/Alias del Inmueble")
        ref = col2.text_input("Ref. Catastral")
        
        st.write("**Estado de Trámites**")
        c1, c2, c3 = st.columns(3)
        ibi = c1.selectbox("IBI", ["Pendiente", "Pagado"])
        luz = c2.selectbox("Luz", ["Pendiente", "En trámite", "Completado"])
        agua = c3.selectbox("Agua", ["Pendiente", "En trámite", "Completado"])
        
        btn = st.form_submit_button("🚀 Guardar en Google Sheets")

    if btn:
        if nombre:
            # Datos a enviar al Script de Google
            payload = {
                "fecha": pd.Timestamp.now().strftime("%d/%m/%Y"),
                "inmueble": nombre,
                "referencia": ref,
                "ibi": ibi,
                "luz": luz,
                "agua": agua
            }
            
            try:
                # Enviamos los datos al Script
                response = requests.post(URL_ESCRITURA, json=payload)
                if response.status_code == 200:
                    st.success(f"✅ ¡{nombre} guardado con éxito!")
                    st.rerun()
                else:
                    st.error("Error al guardar. Revisa la URL del Script.")
            except Exception as e:
                st.error(f"No se pudo conectar con el Script: {e}")
        else:
            st.warning("⚠️ El nombre del inmueble es obligatorio")

    # MOSTRAR TABLA
    st.divider()
    st.subheader("📋 Listado Actualizado")
    if not df_existente.empty:
        st.dataframe(df_existente, use_container_width=True)
    else:
        st.info("La hoja de cálculo está vacía o no tiene el formato correcto.")
