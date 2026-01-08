import streamlit as st
import pandas as pd

# CONFIGURACIÓN
st.set_page_config(page_title="Gestor Inmo Pro", layout="wide")

# SUSTITUYE AQUÍ TU URL DE GOOGLE SHEETS (Asegúrate de que termina en /export?format=csv)
# Ejemplo: https://docs.google.com/spreadsheets/d/TU_ID/export?format=csv
SHEET_ID = "1N6trH41YU4Edkvy-9XBWb4Zs7_AO25zKwoLq3hsOqmo"
url_csv = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

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

    # LEER DATOS (Sin librerías raras)
    try:
        df_existente = pd.read_csv(url_csv)
    except:
        df_existente = pd.DataFrame(columns=["Fecha", "Inmueble", "Referencia", "IBI", "Luz", "Agua"])

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
        
        btn = st.form_submit_button("Guardar Localmente")

    if btn:
        if nombre:
            nueva_fila = {
                "Fecha": pd.Timestamp.now().strftime("%d/%m/%Y"),
                "Inmueble": nombre,
                "Referencia": ref,
                "IBI": ibi,
                "Luz": luz,
                "Agua": agua
            }
            # Nota: Para escribir en Google Sheets con este método sencillo, 
            # lo ideal es que descargues el CSV modificado.
            st.session_state.temp_df = pd.concat([df_existente, pd.DataFrame([nueva_fila])], ignore_index=True)
            st.success("✅ Añadido a la lista visual")
    
    st.write("### 📋 Listado Actual")
    df_mostrar = st.session_state.get('temp_df', df_existente)
    st.dataframe(df_mostrar, use_container_width=True)

    # BOTÓN PARA DESCARGAR EL EXCEL ACTUALIZADO
    csv_data = df_mostrar.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 Descargar Excel con cambios", data=csv_data, file_name="inmuebles_actualizados.csv")
