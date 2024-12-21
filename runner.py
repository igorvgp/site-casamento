from app.pages.lista_presentes import lista_presentes
from app.pages.confirmar_presenca import confirmar_presenca
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
import base64
import pandas as pd
from pathlib import Path

local_path = os.getcwd()

# Configurar as credenciais do Google Sheets a partir do Streamlit Secrets
creds_json = st.secrets["google"]["creds"]

# Salvar credenciais temporariamente (necessário para gspread)
temp_path = Path("temp_credentials.json")
with open(temp_path, "w") as f:
    f.write(creds_json)

# Configurar as credenciais do sheets
#credentials_file = os.path.join(local_path, "settings", "credentials.json")

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

credentials = Credentials.from_service_account_file(temp_path, scopes=scopes)
#credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
client = gspread.authorize(credentials)

# Abrir a planilha
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Fy8dVCIIAeElyKrw3TYwhgqoygGxyWWg0dEI6Um4AZk/edit?usp=sharing")

#confirmar_presenca(spreadsheet)

#lista_presentes(spreadsheet)

#####################################
def pagina_inicial():
    st.title("Página Inicial (não criada)")

def deixe_uma_mensagem():
    st.title("Deixe uma mensagem (não criada)")   

def page_lista_presentes():
    lista_presentes(spreadsheet)

def page_confirmar_presenca():
    confirmar_presenca(spreadsheet)

pages = {
    "Páginas": [
        st.Page(pagina_inicial, title="Página Inicial"),
        st.Page(page_lista_presentes, title="Lista de Presentes"),
        st.Page(page_confirmar_presenca, title="Confirme sua presença"),
        st.Page(deixe_uma_mensagem, title="Deixe uma mensagem")
    ],
}

# Markdown para alterar a cor de fundo do sidebar
st.markdown(
    """
    <style>
    [data-testid="stSidebar"] {
        background-color: #ffffff !important; /* Change this to your preferred color */
        opacity: 1 !important; /* Ensure full opacity */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pg = st.navigation(pages)
pg.run()