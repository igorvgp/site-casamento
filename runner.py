from app.pages.lista_presentes import lista_presentes
from app.pages.confirmar_presenca import confirmar_presenca
from app.pages.boas_vindas import boas_vindas
from app.pages.cerimonia_e_recepcao import cerimonia_e_recepcao
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
import pandas as pd
from pathlib import Path

local_path = os.getcwd()

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

# Configurar as credenciais do Google Sheets a partir do Streamlit Secrets
creds_json = st.secrets["google"]["creds"]

# Salvar credenciais temporariamente (necessário para gspread)
temp_path = Path("temp_credentials.json")
with open(temp_path, "w") as f:
    f.write(creds_json)

credentials = Credentials.from_service_account_file(temp_path, scopes=scopes)

client = gspread.authorize(credentials)

# Abrir a planilha
spreadsheet = client.open_by_url(st.secrets["database"]["gsheets_url"])

#confirmar_presenca(spreadsheet)

#lista_presentes(spreadsheet)

#####################################
def pagina_inicial():
    boas_vindas()

def deixe_uma_mensagem():
    st.title("Deixe uma mensagem (não criada)")   

def page_lista_presentes():
    lista_presentes(spreadsheet)

def page_confirmar_presenca():
    confirmar_presenca(spreadsheet)

def page_cerimonia_e_recepcao():
    cerimonia_e_recepcao()

pages = {
    "": [
        st.Page(pagina_inicial, title="Página Inicial 🏠"),
        st.Page(page_lista_presentes, title="Lista de Presentes 🎁"),
        st.Page(page_confirmar_presenca, title="Confirme sua presença 📓"),
        st.Page(page_cerimonia_e_recepcao, title="Cerimônia e Recepção 📍"),
        st.Page(deixe_uma_mensagem, title="Deixe uma mensagem ✉️")
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