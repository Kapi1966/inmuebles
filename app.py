import requests # Añade esto al principio de tu app.py

# ... (tu código de login y lectura de tabla) ...

# 1. PEGA AQUÍ LA URL QUE COPIASTE DEL PASO ANTERIOR
URL_SCRIPT = "https://script.google.com/macros/s/AKfycbyChPL3E66Dn4gmWOrBHXgSaY7Px05kzjX_yKXW1ndYC-j9AMFFytl_Gap2-_kxxZxi/exec"

with st.form("nuevo_piso"):
    st.subheader("Registrar Inmueble")
    nombre = st.text_input("Nombre/Alias")
    ref = st.text_input("Ref. Catastral")
    c1, c2, c3 = st.columns(3)
    ibi = c1.selectbox("IBI", ["Pendiente", "Pagado"])
    luz = c2.selectbox("Luz", ["Pendiente", "Completado"])
    agua = c3.selectbox("Agua", ["Pendiente", "Completado"])
    
    if st.form_submit_button("Guardar en Google Sheets"):
        if nombre:
            # Preparamos los datos
            datos = {
                "fecha": pd.Timestamp.now().strftime("%d/%m/%Y"),
                "inmueble": nombre,
                "referencia": ref,
                "ibi": ibi,
                "luz": luz,
                "agua": agua
            }
            # Enviamos los datos al "Portero" de Google
            res = requests.post(URL_SCRIPT, json=datos)
            
            if res.status_code == 200:
                st.success("✅ Guardado permanentemente en el Excel")
                st.rerun() # Refresca la tabla para ver el nuevo registro
            else:
                st.error("Error al conectar con Google")
        else:
            st.warning("El nombre es obligatorio")

