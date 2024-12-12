from app.pages.lista_presentes import lista_presentes
from app.pages.confirmar_presenca import confirmar_presenca
import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import os
import base64
import pandas as pd
import json

local_path = os.getcwd()

creds = {
  "type": "service_account",
  "project_id": "site-casamento-444219",
  "private_key_id": "5a11a0179cfea6ead5c1612976950bfd1176cb90",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQCEZjeCAgXbVSMs\n3woQwHCTHP9ti08y7B286kpTLsY7U+Pns4Er69mx+wNUALJmS8HiIM6a8LSCrYdD\nf1dR/Zb+hjImpMUJeTOYgtS/erDfZjqd2KkubZV0gBH/zg31Ab5Ishms8UJvrzCq\n4jKBDj5KWQoFnweFxc8AzP2YNJR6Ka3kneGbESZ5md8+BREQBw+wS6JneL+Iw4+q\nuTvEllDrhyHWjB7zfAb1CLbkKP+MeRRc9Ob2gTbKE05ictY677sTyPTHdApcKjHT\nIWvppIqA08dJMLLZnHEZX4zpZdINKlRY6BOM7RqDMZithWo4mekLJnmPR+LDJnPO\nbvcDbgAZAgMBAAECggEAAXooaCK65GQgg3eGOpmVDav+dMhf0G0BzJMOHTLeRl02\n+nfVL47jiFi7hDhKRULgAzR85HuL2XZ3/yThlwtBUm5EL5VwgGqJ9eJhFfUubEI6\n0hX9cfI3zRJcp+fAS7h7z+xJxgL1cJEXw5LkLXevjdZocY5u79s9HSLVgiJ+eYU4\nhiqRB8h1DebSGjJeLFp0gkLE5uMxb6Lkf2QIKSyegldki48rtum5SifZS9Dhs10W\nCIanqdRA+b6l6qH4yo+Gb7iFVPgyTNonwjDhD0R5ARZbblmTDhYRIfKf6H5okhHY\nUlLiEpVxdTNPGSghN4gASetOOIE/SStcpINFd+D1kQKBgQC6e5ig9rmGmoerXgxk\n8VZrwMcM3epR7nQsQs6tDzTfm4L4hx3TBScj6sxJqp4wOL4GYdcBQtUE8BXKFm+4\nwpR98f+VsUdjBWVIbV/MBERSD2gx487AYvtKth6Ff49g7pnnmLAg2hzLPp++W8vY\nzWx+cyWUox5iVBcw9p1TMcKRyQKBgQC1wVRPCv3fJ0Gqk0BPMB6OA/1XK0Fz9U+8\nPCX1UAtR4P8hd+SjaryGGklSlwQS5NhbMoy8I1MVtjxUjV86Kvoz6WcFkvdy2VhO\npvXI4fg/pjqxYE3Xv6qOvzfZ+e9gk/mHCAg+glfBv2cg4odNdAdmCF/5ttZxPUxi\nQM0Ti7Kj0QKBgQC4LwTTznv1R0FCb5R8SqVZrcCro68glwzk/mMVKJTHWdhk0UcS\nud8rqWd2Ru8Qn6qHsTDjTPgKdXp/6+MSsBRrxI30cnEYiya6/1QDtB8qkY8O33rA\nJ8Mcyn2gyxl42pDl3rfu6p5P2515LT9L9bD3v5DZmraS1Y1GTf2bQuVyiQKBgGyK\n0jCKHeaAaSTW31brI7QoCcle2a3IWB/Pw9NmQ/xX48U29mHpQkDLvfIGobYu2E5O\nN+G7LskOlaTg8HeqZtVNk+quQ/xgc+40ox+eY0SPnwmCu7oWimLJKy+PpTcF58SO\nNW4vJP1dstbesXK90hVK9xYH7LSfqNgcXtxHVx2hAoGBAJ9c9RShRfZGfeP+ZBhF\nzBsVKAac6B17SJRJhxscbIFE3vCDHOqqO7J1D4Z2Q/7Q1/lMwPLqUaBGGDVr4CbE\nkt641Y1yK1sL8irw7c2Zn15bp5hTmGskBLf/OMoPWJloC+8gbdjBSgEESOwhAybk\nXfX9rt9kpZ6eNIRkmawDH4/N\n-----END PRIVATE KEY-----\n",
  "client_email": "site-casamento@site-casamento-444219.iam.gserviceaccount.com",
  "client_id": "111603794537569223491",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/site-casamento%40site-casamento-444219.iam.gserviceaccount.com",
  "universe_domain": "googleapis.com"
}

# with open(local_path, "w", encoding="utf-8") as arquivo:
#     json.dump(creds, arquivo, indent=4, ensure_ascii=False)

# # Configurar as credenciais do sheets
# credentials_file = os.path.join(local_path, "google_creds.json")

# scopes = [
#     "https://www.googleapis.com/auth/spreadsheets",
#     "https://www.googleapis.com/auth/drive"
# ]
# credentials = Credentials.from_service_account_file(credentials_file, scopes=scopes)
client = gspread.authorize(creds)

# Abrir a planilha
spreadsheet = client.open_by_url("https://docs.google.com/spreadsheets/d/1Fy8dVCIIAeElyKrw3TYwhgqoygGxyWWg0dEI6Um4AZk/edit?usp=sharing")

#confirmar_presenca(spreadsheet)

lista_presentes(spreadsheet)
