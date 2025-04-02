import os
import ast
import gspread
import warnings
import numpy  as np
import pandas as pd
import streamlit as st

from pathlib  import Path    
from datetime import datetime
from google.oauth2.service_account import Credentials

warnings.filterwarnings('ignore')

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
link = "https://docs.google.com/spreadsheets/d/1Fy8dVCIIAeElyKrw3TYwhgqoygGxyWWg0dEI6Um4AZk/edit?usp=sharing"
spreadsheet = client.open_by_url(link)

convidados = {
    'Sara e Luan': ['Luan Antônio', 'Sara Gadelha'],
    'Paloma e Guilherme': ['Guilherme Rabelo', 'Paloma Pereira'],
    'Cilene e Toninho': ['Antônio Gomes Toninho', 'Juscilene Pereira Cilene'],
    'Mônica e João': ['João Batista', 'Mônica Maria'],
    'Felipe': ['Felipe Lino'],
    'Eduarda e Pedro': ['Eduarda Moreira', 'Pedro Henrique'],
    'Joyce, Danilo e Daniel': ['Danilo Junio', 'Joyce Moura', 'Daniel Moura'],
    'Renata': ['Renata Cristina'],
    'Marcelo': ['Marcelo Eleutério'],
    'Sidnei': ['Sidnei Junio'],
    'Luisa e Carlos': ['Carlos Germano', 'Luisa Barbosa'],
    'Laiane e Tiago': ['Laiane Camargos', 'Tiago Miller', 'Leonardo', 'Augustus'],
    'Letícia e Tales': ['Letícia Penido', 'Tales'],
    'Alessandra e Dani': ['Alessandra Maciel', 'Daniele Silva'],
    'Izabela e Lincoln': ['Izabela Carvalho', 'Lincoln Siqueira'],
    'Walter e Samuel': ['Walter Junio', 'Samuel Martins'],
    'Thalita e Lucas': ['Thalita Cristina', 'Lucas Adriano'],
    'Fanny Amorim': ['Fanny Amorim'],
    'Jéssica e Anderson': ['Jéssica Conrado', 'Anderson'],
    'Marynna Mendonça': ['Marynna Mendonça'],
    'Isabella e Felipe': ['Isabella Souza', 'Felipe Souza']
}

lista_convidados = list(convidados.values())
lista_nomes_convites = list(convidados.keys())

###### Função de resetar tudo ######
def reset_all(lista_convidados, lista_nomes_convites, spreadsheet, link):

    answer = input('Tem certeza que deseja resetar todas as bases? Você irá perder toda a lista de confirmação. (S/N)')
    if answer.upper() == 'N':
        print("Reset cancelado")
        return None

    ## Cria tabela convites, salva dados no google sheets
    df_convites = pd.DataFrame()
    df_convites['convidados'] = lista_convidados
    df_convites['nome_convite'] = lista_nomes_convites
    n = len(df_convites)
    id_convites = np.random.choice(range(100000, 1000000), size=n, replace=False)
    id_convites = ["C" + str(id) for id in id_convites]
    df_convites['id_convite'] = id_convites
    df_convites = df_convites[['id_convite', 'convidados', 'nome_convite']]
    # Inserir dados de convites no google sheets
    worksheet_convites = spreadsheet.worksheet('Convites')
    worksheet_convites.clear()
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: ", ".join(x))
    df_convites_list = [df_convites.columns.tolist()] + df_convites.values.tolist()
    worksheet_convites.update("A1", df_convites_list)
    print("Tabela 'convites' criada!")

    ## Cria tabela convidados, salva dados no google sheets
    worksheet_convites = spreadsheet.worksheet("Convites")
    data_convites = worksheet_convites.get_all_records()
    df_convites = pd.DataFrame(data_convites)
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: x.replace("[","").replace("]","").replace("'", ""))
    df_convites['convidados'] = df_convites['convidados'].str.split(", ")
    df_convidados = df_convites.explode('convidados', ignore_index=True)
    df_convidados = df_convidados.rename(columns = {'convidados':'nome_convidado'})
    n = len(df_convidados)
    id_convidados = np.random.choice(range(10000, 100000), size=n, replace=False)
    id_convidados = ["V" + str(id) for id in id_convidados]
    df_convidados['id_convidado'] = id_convidados
    df_convidados = df_convidados[['id_convidado', 'nome_convidado', 'id_convite']]
    # Inserir dados de convidados no google sheets
    worksheet_convidados = spreadsheet.worksheet('Convidados')
    worksheet_convidados.clear()
    df_convidados_list = [df_convidados.columns.tolist()] + df_convidados.values.tolist()
    worksheet_convidados.update("A1", df_convidados_list)
    print("Tabela 'convidados' criada!")

    ## Cria tabela confirmados, salva dados no google sheets
    df_confirmados = df_convidados[['id_convidado', 'nome_convidado']]
    df_confirmados['confirmado'] = None
    df_confirmados['autoriza_foto'] = False
    # Inserir dados de confirmados no google sheets
    worksheet_confirmados = spreadsheet.worksheet('Confirmados')
    worksheet_confirmados.clear()
    df_confirmados_list = [df_confirmados.columns.tolist()] + df_confirmados.values.tolist()
    worksheet_confirmados.update("A1", df_confirmados_list)
    print("Tabela 'confirmados' criada!")

    ## Cria tabela de mensagens, salva dados no google sheets
    df_mensagens = pd.DataFrame({'timestamp':[str(datetime.now())], 'nome':['teste'], 'mensagem':['teste']})
    # Inserir dados de mensagens no google sheets
    worksheet_mensagens = spreadsheet.worksheet('Mensagens')
    worksheet_mensagens.clear()
    df_mensagens_list = [df_mensagens.columns.tolist()] + df_mensagens.values.tolist()
    worksheet_mensagens.update("A1", df_mensagens_list)
    print("Tabela 'mensagens' criada!")

    ## Remove fotos da pasta 'permitidos'
    # for arquivo in os.listdir('resources/images/mosaico/permitidos'):
    #     caminho_arquivo = os.path.join('resources/images/mosaico/permitidos', arquivo)
    #     if os.path.isfile(caminho_arquivo):
    #         os.remove(caminho_arquivo)

    print(f"Tabelas criadas no link: {link}")

# Função inserir novo convidado
def inserir_convite(dicionario_novos_convidados, spreadsheet):
    '''
    recebe uma dicionario com chave "nome_convite" e valor "convidados", como no exemplo:
    {
        'convite_1: ['Convidado x', 'Convidado y'],
        'convite_2: ['Convidado z']
    }
    separe os nomes com ", " vírgula e espaço

    ** Não se esqueça de incluir as fotos dos convidados **

    '''
    matriz_novos_convidados = list(dicionario_novos_convidados.values())
    ## Tabela convites
    worksheet_convites = spreadsheet.worksheet("Convites")
    data_convites = worksheet_convites.get_all_records()
    df_convites = pd.DataFrame(data_convites)
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: x.replace("[","").replace("]","").replace("'", ""))
    df_convites['convidados'] = df_convites['convidados'].str.split(", ")
    list_convidados_nomes_insert = [[nome_convite, convidados] for nome_convite, convidados in dicionario_novos_convidados.items()  if convidados not in df_convites['convidados'].values.tolist()]
    list_nomes_insert = [item[0] for item in list_convidados_nomes_insert]
    list_convidados_insert = [item[1] for item in list_convidados_nomes_insert]
    list_ids_existentes = df_convites['id_convite'].values.tolist()
    codigos_gerados = set()
    while len(codigos_gerados) < len(list_convidados_insert):
            random_id = "C" + str(np.random.randint(10000, 1000000 + 1))
            if random_id not in list_ids_existentes and random_id not in codigos_gerados:
                codigos_gerados.add(random_id)
    df_novos_convidados = pd.DataFrame({'id_convite':list(codigos_gerados), 'convidados':list_convidados_insert, 'nome_convite':list_nomes_insert})
    df_convites = pd.concat([df_convites, df_novos_convidados])
    # Inserir novos convites no google sheets
    worksheet_convites = spreadsheet.worksheet('Convites')
    worksheet_convites.clear()
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: ", ".join(x))
    df_convites_list = [df_convites.columns.tolist()] + df_convites.values.tolist()
    worksheet_convites.update("A1", df_convites_list)

    ## Tabela convidados
    worksheet_convites = spreadsheet.worksheet("Convites")
    data_convites = worksheet_convites.get_all_records()
    df_convites = pd.DataFrame(data_convites)
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: x.replace("[","").replace("]","").replace("'", ""))
    df_convites['convidados'] = df_convites['convidados'].str.split(", ")
    worksheet_convidados = spreadsheet.worksheet("Convidados")
    data_convidados = worksheet_convidados.get_all_records()
    df_convidados = pd.DataFrame(data_convidados)
    ids_in_convites = df_convites['id_convite'].values.tolist()
    ids_in_convidados = df_convidados['id_convite'].values.tolist()
    ids_convites_novos = [id_ for id_ in ids_in_convites if id_ not in ids_in_convidados]
    df_convites_novos = df_convites[df_convites['id_convite'].isin(ids_convites_novos)]
    df_convidados_novos = df_convites_novos.explode('convidados', ignore_index=True)
    df_convidados_novos = df_convidados_novos.rename(columns = {'convidados':'nome_convidado'})
    list_ids_existentes = df_convidados['id_convidado'].values.tolist()
    codigos_gerados = set()
    while len(codigos_gerados) < len(df_convidados_novos):
        random_id = "V" + str(np.random.randint(10000, 1000000 + 1))
        if random_id not in list_ids_existentes and random_id not in codigos_gerados:
            codigos_gerados.add(random_id)
    df_convidados_novos['id_convidado'] = list(codigos_gerados)
    df_convidados_novos = df_convidados_novos[['id_convidado', 'nome_convidado', 'id_convite']]
    df_convidados = pd.concat([df_convidados, df_convidados_novos])
    # Inserir dados de convidados no google sheets
    worksheet_convidados = spreadsheet.worksheet('Convidados')
    worksheet_convidados.clear()
    df_convidados_list = [df_convidados.columns.tolist()] + df_convidados.values.tolist()
    worksheet_convidados.update("A1", df_convidados_list)

    ## Tabela confirmados
    worksheet_confirmados = spreadsheet.worksheet("Confirmados")
    data_confirmados = worksheet_confirmados.get_all_records()
    df_confirmados = pd.DataFrame(data_confirmados)
    df_convidados_novos = df_convidados_novos.rename(columns = {'id_convite':'confirmado'})
    df_convidados_novos['confirmado'] = None
    df_convidados_novos['autoriza_foto'] = False
    df_confirmados = pd.concat([df_confirmados, df_convidados_novos])
    # Inserir dados de confirmados no google sheets
    df_confirmados = df_confirmados.fillna('')
    worksheet_confirmados = spreadsheet.worksheet('Confirmados')
    worksheet_confirmados.clear()
    df_confirmados_list = [df_confirmados.columns.tolist()] + df_confirmados.values.tolist()
    worksheet_confirmados.update("A1", df_confirmados_list)

# Função remover convite
def remover_convite(ids_convites, spreadsheet):
    '''
    id_convite: uma lista com os id's dos convites que serão removidos
    '''
    ## Tabela convites
    worksheet_convites = spreadsheet.worksheet("Convites")
    data_convites = worksheet_convites.get_all_records()
    df_convites = pd.DataFrame(data_convites)
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: x.replace("[","").replace("]","").replace("'", ""))
    df_convites['convidados'] = df_convites['convidados'].str.split(", ")
    df_convites = df_convites[~df_convites['id_convite'].isin(ids_convites)]
    # Inserir novos convites no google sheets
    worksheet_convites = spreadsheet.worksheet('Convites')
    worksheet_convites.clear()
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: ", ".join(x))
    df_convites_list = [df_convites.columns.tolist()] + df_convites.values.tolist()
    worksheet_convites.update("A1", df_convites_list)

    ## Tabela convidados
    worksheet_convidados = spreadsheet.worksheet("Convidados")
    data_convidados = worksheet_convidados.get_all_records()
    df_convidados = pd.DataFrame(data_convidados)
    id_convidados_remover = df_convidados[df_convidados['id_convite'].isin(ids_convites)]['id_convidado'].values.tolist()
    df_convidados = df_convidados[~df_convidados['id_convite'].isin(ids_convites)]
    # Inserir dados de convidados no google sheets
    worksheet_convidados = spreadsheet.worksheet('Convidados')
    worksheet_convidados.clear()
    df_convidados_list = [df_convidados.columns.tolist()] + df_convidados.values.tolist()
    worksheet_convidados.update("A1", df_convidados_list)

    ## Tabela confirmados
    worksheet_confirmados = spreadsheet.worksheet("Confirmados")
    data_confirmados = worksheet_confirmados.get_all_records()
    df_confirmados = pd.DataFrame(data_confirmados)
    df_confirmados = df_confirmados[~df_confirmados['id_convidado'].isin(id_convidados_remover)]
    # Inserir dados de confirmados no google sheets
    df_confirmados = df_confirmados.fillna('')
    worksheet_confirmados = spreadsheet.worksheet('Confirmados')
    worksheet_confirmados.clear()
    df_confirmados_list = [df_confirmados.columns.tolist()] + df_confirmados.values.tolist()
    worksheet_confirmados.update("A1", df_confirmados_list)

    print(f"Convites {ids_convites} removidos com sucesso!")
    
reset_all(lista_convidados, lista_nomes_convites, spreadsheet, link)
inserir_convite(
    {'Alessandra e Dani': ['Alessandra Maciel', 'Daniele Silva'],
     'Izabela e Lincoln': ['Izabela Carvalho', 'Lincoln Siqueira'],
    # 'Jéssica e Anderson': ['Jéssica Conrado', 'Anderson'],
     'Walter e Samuel': ['Walter Junio', 'Samuel Martins'],
     'Thalita e Lucas': ['Thalita Cristina', 'Lucas Adriano']
     },
    spreadsheet)
#remover_convite(['C347167', 'C761346'], spreadsheet)