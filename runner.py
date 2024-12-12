from app.pages.lista_presentes import lista_presentes
from app.pages.confirmar_presenca import confirmar_presenca
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
import base64
import pandas as pd

local_path = os.getcwd()

# Configurar as credenciais do sheets
credentials_file = os.path.join(local_path, "settings", "credentials.json")

scopes = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]
credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
client = gspread.authorize(credentials)

# Abrir a planilha
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Fy8dVCIIAeElyKrw3TYwhgqoygGxyWWg0dEI6Um4AZk/edit?usp=sharing")

#confirmar_presenca(spreadsheet)

lista_presentes(spreadsheet)
