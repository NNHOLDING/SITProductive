import streamlit as st
import gspread
from datetime import datetime

# Autenticación con gspread usando los secretos de Streamlit Cloud
gc = gspread.service_account_from_dict(st.secrets["gcp_service_account"])

# Abrir la hoja de cálculo por su ID
sheet = gc.open_by_key("1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0").sheet1

# Título de la app
st.title("Formulario de Registro - Alisto Unimar")

# Formulario
with st.form("registro_form"):
    nombre = st.text_input("Nombre completo")
    correo = st.text_input("Correo electrónico")
    carrera = st.selectbox("Carrera", ["Ingeniería", "Diseño", "Educación", "Administración", "Otra"])
    comentarios = st.text_area("Comentarios adicionales")
    enviar = st.form_submit_button("Enviar")

# Si se envió el formulario
if enviar:
    if nombre and correo:
        # Agregar datos a la hoja de cálculo con fecha
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fila = [fecha, nombre, correo, carrera, comentarios]
        sheet.append_row(fila)
        st.success("✅ Tus datos se han registrado correctamente.")
    else:
        st.warning("Por favor completa los campos obligatorios: nombre y correo.")
