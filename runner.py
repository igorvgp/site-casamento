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
#redentials_file = os.path.join(local_path, "settings", "credentials.json")

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
        st.Page(page_lista_presentes, title="Presenteie o casal"),
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

# Adicionando CSS para estilizar o botão do sidebar
st.markdown(
    """
    <style>
    /* Estiliza o botão de toggle (seta) para visibilidade */
    [data-testid="collapsedControl"] {
        background-color: #007bff !important; /* Cor azul de destaque */
        border-radius: 50% !important; /* Botão circular */
        width: 50px !important; /* Aumenta a largura */
        height: 50px !important; /* Aumenta a altura */
        color: white !important; /* Cor do ícone */
        font-size: 20px !important; /* Aumenta o tamanho do ícone */
        box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.3); /* Sombra para destaque */
        display: flex;
        justify-content: center;
        align-items: center;
    }
    /* Hover para o botão */
    [data-testid="collapsedControl"]:hover {
        background-color: #0056b3 !important; /* Azul mais escuro no hover */
        cursor: pointer; /* Mostra o cursor como pointer */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

pg = st.navigation(pages)
pg.run()

# Configurar as opções do sidebar
# st.sidebar.title("Navegação")
# opcao = st.sidebar.selectbox(
#     "Escolha uma página:",  # Texto do selectbox
#     ["Página Inicial", "Lista de Presentes", "Confirmar Presença"]  # Opções disponíveis
# )

# # Renderizar a página com base na seleção
# if opcao == "Página Inicial":
#     st.title("Bem-vindo ao Site de Casamento")
#     st.write("Aqui você encontra todas as informações sobre nosso casamento.")
    
# elif opcao == "Lista de Presentes":
#     lista_presentes(spreadsheet)

# elif opcao == "Confirmar Presença":
#     confirmar_presenca(spreadsheet)
