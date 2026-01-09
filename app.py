import streamlit as st
import pandas as pd
import requests

st.set_page_config(page_title="Gestor Inmobiliario Pro", layout="wide")

# --- CONFIGURACIÓN DE CONEXIONES ---
SHEET_ID = "1N6trH41YU4Edkvy-9XBWb4Zs7_AO25zKwoLq3hsOqmo"
URL_LECTURA = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"
# RECUERDA: Poner aquí tu nueva URL de Apps Script (la que termina en /exec)
URL_ESCRITURA = "TU_NUEVA_URL_DE_APPS_SCRIPT_AQUI" 

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
    # --- BARRA LATERAL (Calculadora y Exportar) ---
    with st.sidebar:
        st.header("🧮 Plusvalía Estimada")
        v_suelo = st.number_input("Valor Suelo (€)", min_value=0, value=50000)
        años = st.slider("Años propiedad", 1, 20, 5)
        if st.button("Calcular"):
            res = (v_suelo * (años * 0.03)) * 0.30
            st.metric("Total estimado", f"{res:,.2f} €")
        
        st.divider()
        st.header("📥 Descargar Datos")
        # El botón de exportar se activará si hay datos
        st.caption("Exporta el listado actual a un archivo compatible con Excel.")

    st.title("🏠 Panel de Control Inmobiliario")

    # LEER DATOS
    try:
        df = pd.read_csv(URL_LECTURA)
        # Limpieza de datos básica para evitar errores de visualización
        df = df.fillna("Pendiente") 
    except:
        df = pd.DataFrame(columns=["Fecha", "Inmueble", "Referencia", "IBI", "Luz", "Agua"])

    # BOTÓN DE EXPORTACIÓN (En la barra lateral)
    if not df.empty:
        csv = df.to_csv(index=False).encode('utf-8-sig')
        st.sidebar.download_button(
            label="📊 Descargar Excel (.csv)",
            data=csv,
            file_name=f"listado_inmuebles_{pd.Timestamp.now().strftime('%d_%m_%Y')}.csv",
            mime="text/csv",
        )

    # FORMULARIO DE ALTA
    with st.expander("➕ Añadir Nuevo Inmueble"):
        with st.form("nuevo"):
            c1, c2 = st.columns(2)
            n_inmueble = c1.text_input("Nombre / Alias del Inmueble")
            n_ref = c2.text_input("Referencia Catastral")
            if st.form_submit_button("Registrar en Base de Datos"):
                if n_inmueble:
                    payload = {
                        "action": "create", "fecha": pd.Timestamp.now().strftime("%d/%m/%Y"),
                        "inmueble": n_inmueble, "referencia": n_ref,
                        "ibi": "Pendiente", "luz": "Pendiente", "agua": "Pendiente"
                    }
                    requests.post(URL_ESCRITURA, json=payload)
                    st.success("Registrado. Actualizando...")
                    st.rerun()
                else:
                    st.warning("Escribe el nombre del inmueble.")

    # LISTADO Y EDICIÓN
    st.subheader("📋 Inmuebles Registrados")
    opciones = ["Pendiente", "En trámite", "Pagado", "Completado"]

    for index, row in df.iterrows():
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 0.5])
            
            col1.write(f"**{row['Inmueble']}**")
            col1.caption(f"Ref: {row['Referencia']}")

            # Función para encontrar el índice del valor actual en la lista de opciones
            def get_index(val, lista):
                try: return lista.index(val)
                except: return 0

            # Selectores de estado
            n_ibi = col2.selectbox("IBI", ["Pendiente", "Pagado"], index=get_index(row['IBI'], ["Pendiente", "Pagado"]), key=f"ibi_{index}")
            n_luz = col3.selectbox("Luz", opciones, index=get_index(row['Luz'], opciones), key=f"luz_{index}")
            n_agua = col4.selectbox("Agua", opciones, index=get_index(row['Agua'], opciones), key=f"agua_{index}")

            # Botones de Guardar (Disco) y Borrar (Papelera)
            if col5.button("💾", key=f"s_{index}", help="Guardar cambios"):
                p = {"action": "update", "inmueble": row['Inmueble'], "ibi": n_ibi, "luz": n_luz, "agua": n_agua}
                requests.post(URL_ESCRITURA, json=p)
                st.rerun()
                
            if col5.button("🗑️", key=f"d_{index}", help="Eliminar inmueble"):
                p = {"action": "delete", "inmueble": row['Inmueble']}
                requests.post(URL_ESCRITURA, json=p)
                st.rerun()
            st.divider()
