import streamlit as st
from datetime import date
import gspread
# Importamos la clase de credenciales moderna
from google.oauth2.service_account import Credentials
import pandas as pd # Importado por si en el futuro quieres mostrar datos, aunque no se usa directamente en este ejemplo de app.py

# --- Configuración de la página de Streamlit ---
st.set_page_config(page_title="Alisto Unimar", layout="centered")
st.title("Formulario - Alisto Unimar")
st.markdown("Por favor completa los siguientes datos:")

# --- Lista de placas (sin cambios, tomada de tu código) ---
placas = [
    "200", "201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "213", "214", "215", "216", "216", "218",
    "300", "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "316", "317", "318",
    "400", "401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413",
    "500", "505", "506", "507", "508", "509", "510", "511", "512", "513",
    "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10",
    "POZUELO", "SIGMA", "COMAPAN", "MAFAM", "MEGASUPER", "AUTOMERCADO",
    "DEMASA", "INOLASA", "EXPORTACION UNIMAR", "HILLTOP", "SAM", "CARTAINESA", "AUTODELI", "WALMART", "PRICSMART"
]

# --- Autenticación con Google Sheets (Zona de cambios clave y manejo de errores) ---
# ID de tu Google Sheet
# Asegúrate de que este ID sea correcto para tu hoja de cálculo
GOOGLE_SHEET_ID = "1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0"

try:
    # Definir los scopes necesarios para Google Sheets y Google Drive
    # Google Drive es necesario para gspread en algunos casos de permisos.
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    # Cargar las credenciales desde los secretos de Streamlit
    # La clave 'gcp_service_account' DEBE coincidir con la sección en tu secrets.toml
    service_account_info = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)

    # Autorizar gspread con las credenciales
    gc = gspread.authorize(credentials)

    # Abrir la hoja de cálculo y seleccionar la primera hoja (sheet1)
    # Incluimos un try-except específico para la apertura de la hoja
    try:
        sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1
    except gspread.exceptions.SpreadsheetNotFound:
        st.error(f"Error: La hoja de cálculo con ID '{GOOGLE_SHEET_ID}' no fue encontrada o no tienes permisos.")
        st.info("Por favor, asegúrate de que el ID es correcto y que tu cuenta de servicio tiene acceso de 'Editor' a la hoja.")
        st.stop() # Detiene la ejecución para evitar más errores

except Exception as e:
    st.error(f"Error al configurar la autenticación de Google Sheets. Esto puede ser debido a:")
    st.markdown("- 1. El archivo `secrets.toml` no está configurado correctamente en Streamlit Cloud.")
    st.markdown("- 2. Las APIs de Google Sheets y Google Drive no están habilitadas en tu proyecto de Google Cloud.")
    st.markdown("- 3. Las credenciales de la cuenta de servicio son incorrectas o están expiradas.")
    st.error(f"Detalles del error técnico: {e}")
    st.stop() # Detiene la ejecución de la app si hay un error de autenticación grave

# --- Formulario de Registro (tomado de tu código, con el manejo de errores mejorado) ---
with st.form("formulario_registro"):
    fecha = st.date_input("Fecha", value=date.today())
    placa = st.selectbox("Placa", placas)
    hora_inicio = st.time_input("Hora de inicio")
    hora_fin = st.time_input("Hora de fin")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        try:
            # Asegúrate de que los tipos de datos sean compatibles con Google Sheets (ej. convertir a string)
            # Y que el orden coincida con tus columnas en la hoja de cálculo.
            row_data = [str(fecha), placa, str(hora_inicio), str(hora_fin)]
            sheet.append_row(row_data)
            st.success("✅ Datos enviados exitosamente a Google Sheets")
            st.write(f"📅 Fecha: {fecha}")
            st.write(f"🚛 Placa: {placa}")
            st.write(f"🕐 Hora de inicio: {hora_inicio}")
            st.write(f"🕓 Hora de fin: {hora_fin}")
            # Opcional: Recargar la página para limpiar el formulario después de enviar
            # st.experimental_rerun() # Usar si quieres que el formulario se resetee

        except Exception as e:
            st.error(f"❌ Ocurrió un error al intentar guardar los datos en Google Sheets.")
            st.info("Verifica que las columnas en tu Google Sheet existan y estén en el orden esperado.")
            st.error(f"Detalles del error técnico: {e}")

