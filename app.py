import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(page_title="Gestor Inmobiliario España", layout="wide")

st.title("🏠 Panel de Control de Inmuebles")
st.subheader("Estado de venta, impuestos y suministros")

# Simulamos una base de datos (En el futuro esto conectará con el SQL de antes)
if 'inmuebles' not in st.session_state:
    st.session_state.inmuebles = [
        {
            "Inmueble": "Ático Gran Vía",
            "IBI": "✅ Pagado",
            "C. Energético": "✅ Sí",
            "Plusvalía": "⚠️ Pendiente Calcular",
            "Luz (CUPS)": "🔴 Pendiente Cambio",
            "Agua": "✅ Completado",
            "Precio": "450.000€"
        },
        {
            "Inmueble": "Piso Calle Mayor",
            "IBI": "🔴 Pendiente",
            "C. Energético": "⚠️ Caducado",
            "Plusvalía": "✅ Calculada",
            "Luz (CUPS)": "✅ Completado",
            "Agua": "🔴 Pendiente Cambio",
            "Precio": "210.000€"
        }
    ]

# --- BARRA LATERAL: AÑADIR NUEVO ---
with st.sidebar:
    st.header("Añadir Nuevo Inmueble")
    nuevo_nombre = st.text_input("Nombre/Alias")
    nueva_ref = st.text_input("Referencia Catastral")
    nuevo_precio = st.number_input("Precio de Venta", min_value=0)
    if st.button("Registrar Inmueble"):
        st.success(f"Registrado: {nuevo_nombre}")

# --- CUERPO PRINCIPAL: LISTADO ---
df = pd.DataFrame(st.session_state.inmuebles)

# Mostrar tabla con formato
st.dataframe(df, use_container_width=True)

# --- DETALLE OPERATIVO ---
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.info("### 📝 Próximos pasos (Suministros)")
    st.checkbox("Llamar a Iberdrola/Endesa para cambio de titular")
    st.checkbox("Solicitar certificado de deuda a la Comunidad")
    st.checkbox("Enviar lectura del contador de agua")

with col2:
    st.warning("### 💰 Impuestos Críticos")
    st.write("- **Plusvalía:** Recordar plazo de 30 días tras firma.")
    st.write("- **IRPF:** Consultar si el vendedor tiene >65 años para exención.")
