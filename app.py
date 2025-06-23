import streamlit as st
import gspread
from google.oauth2.service_account import Credentials

# Obtener credenciales desde secrets.toml
service_account_info = st.secrets["gcp_service_account"]

# Autenticación con Google Sheets
credentials = Credentials.from_service_account_info(service_account_info)
client = gspread.authorize(credentials)

# Abrir la hoja de cálculo
sheet = client.open_by_key("1o-GozoYaU_4Ra2KgX05Yi4biDV9zcd6BGdqOdSxKAv0").sheet1
