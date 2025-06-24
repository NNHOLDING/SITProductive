import streamlit as st
from datetime import date, datetime
import gspread
from google.oauth2.service_account import Credentials

# Configurar página
st.set_page_config(page_title="Alisto Unimar", layout="centered")
st.title("Formulario - Alisto Unimar")
st.markdown("Por favor completa los siguientes datos:")

# Lista de placas
placas = [
    "200", "201", "202", "203", "204", "205", "206", "207", "208", "209", "210", "211", "212", "213", "214", "215", "216", "216", "218",
    "300", "301", "302", "303", "304", "305", "306", "307", "308", "309", "310", "311", "312", "313", "314", "315", "316", "317", "318",
    "400", "401", "402", "403", "404", "405", "406", "407", "408", "409", "410", "411", "412", "413",
    "500", "505", "506", "507", "508", "509", "510", "511", "512", "513",
    "F01", "F02", "F03", "F04", "F05", "F06", "F07", "F08", "F09", "F10",
    "POZUELO", "SIGMA", "COMAPAN", "MAFAM", "MEGASUPER", "AUTOMERCADO",
    "DEMASA", "INOLASA", "EXPORTACION UNIMAR", "HILLTOP", "SAM", "CARTAINESA", "AUTODELI", "WALMART", "PRICSMART"
]

# Lista de usuarios
usuarios = [
    "51416", "51417", "59907", "51918", "58898", "59116", "52106",
    "54933", "51857", "53990", "52190", "52182", "00000", "11111"
]

GOOGLE_SHEET_ID = "1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0"

try:
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    service_account_info = st.secrets["gcp_service_account"]
    credentials = Credentials.from_service_account_info(service_account_info, scopes=scope)
    gc = gspread.authorize(credentials)
    sheet = gc.open_by_key(GOOGLE_SHEET_ID).sheet1

except Exception as e:
    st.error("Error al configurar la autenticación de Google Sheets.")
    st.stop()

# Formulario actualizado
with st.form("formulario_registro"):
    fecha = st.date_input("Fecha", value=date.today())
    placa = st.selectbox("Placa", placas)
    usuario = st.selectbox("Usuario", usuarios)
    cantidad_lineas = st.number_input("Cantidad de líneas", min_value=0, step=1)
    hora_inicio = st.time_input("Hora de inicio", value=datetime.now().time())
    hora_fin = st.time_input("Hora de fin")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        try:
            row_data = [
                str(fecha), placa, usuario, int(cantidad_lineas),
                str(hora_inicio), str(hora_fin)
            ]
            sheet.append_row(row_data)
            st.success("✅ Datos enviados exitosamente a Google Sheets")
        except Exception as e:
            st.error("❌ Error al guardar los datos en Google Sheets.")
            st.error(f"Detalles técnicos: {e}")
