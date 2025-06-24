import streamlit as st
from datetime import date
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuración inicial
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

# Autenticación con Google Sheets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_info = st.secrets["gcp_service_account"]  # ❗️Este es el cambio corregido
credentials = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(credentials)
sheet = client.open_by_key("1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0").sheet1

# Formulario
with st.form("formulario_registro"):
    fecha = st.date_input("Fecha", value=date.today())
    placa = st.selectbox("Placa", placas)
    hora_inicio = st.time_input("Hora de inicio")
    hora_fin = st.time_input("Hora de fin")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        sheet.append_row([str(fecha), placa, str(hora_inicio), str(hora_fin)])
        st.success("✅ Datos enviados exitosamente a Google Sheets")
        st.write(f"📅 Fecha: {fecha}")
        st.write(f"🚛 Placa: {placa}")
        st.write(f"🕐 Hora de inicio: {hora_inicio}")
        st.write(f"🕓 Hora de fin: {hora_fin}")
