import streamlit as st
import gspread
import json
from oauth2client.service_account import ServiceAccountCredentials
from datetime import date

# Configuración de página
st.set_page_config(page_title="Alisto Unimar", layout="centered")

# Estilos opcionales
st.markdown("""
    <style>
    .stButton>button {
        background-color: teal;
        color: white;
    }
    </style>
""", unsafe_allow_html=True)

# Lista de placas
placas = [
    "200","201","202","203","204","205","206","207","208","209","210","211","212","213","214","215","216","216","218",
    "300","301","302","303","304","305","306","307","308","309","310","311","312","313","314","315","316","317","318",
    "400","401","402","403","404","405","406","407","408","409","410","411","412","413",
    "500","505","506","507","508","509","510","511","512","513",
    "F01","F02","F03","F04","F05","F06","F07","F08","F09","F10",
    "POZUELO","SIGMA","COMAPAN","MAFAM","MEGASUPER","AUTOMERCADO",
    "DEMASA","INOLASA","EXPORTACION UNIMAR","HILLTOP","SAM","CARTAINESA","AUTODELI","WALMART","PRICSMART"
]

# Autenticación con Google Sheets desde secrets
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
service_account_info = json.loads(st.secrets["gcp_service_account"].to_json())
creds = ServiceAccountCredentials.from_json_keyfile_dict(service_account_info, scope)
client = gspread.authorize(creds)

# Accede a la hoja de cálculo
sheet = client.open("Registros Unimar").sheet1

# Encabezado
st.markdown("<h2 style='color: teal;'>📋 Registro de ingreso de unidades</h2>", unsafe_allow_html=True)

# Formulario
with st.form("registro_formulario"):
    fecha = st.date_input("Fecha", value=date.today())
    placa = st.selectbox("Placa", placas)
    hora_inicio = st.time_input("Hora de inicio")
    hora_fin = st.time_input("Hora de fin")
    enviado = st.form_submit_button("Enviar")

    if enviado:
        sheet.append_row([str(fecha), placa, str(hora_inicio), str(hora_fin)])
        st.success("✅ Registro enviado correctamente a Google Sheets")