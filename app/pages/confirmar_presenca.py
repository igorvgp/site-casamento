import os
import ast
import base64
import shutil
import gspread
import  pandas    as pd
import streamlit as st

from PIL                           import Image
from math                          import ceil, sqrt
from google.oauth2.service_account import Credentials

local_path = os.getcwd()

@st.dialog("Confirmar Presença")
def tela_de_confirmacao(local_path, spreadsheet):

    worksheet_convites = spreadsheet.worksheet("Convites")
    data_convites = worksheet_convites.get_all_records()
    df_convites = pd.DataFrame(data_convites)
    df_convites['convidados'] = df_convites['convidados'].apply(lambda x: x.replace("[","").replace("]","").replace("'", ""))
    df_convites['convidados'] = df_convites['convidados'].str.split(", ")

    worksheet_convidados = spreadsheet.worksheet("Convidados")
    data_convidados = worksheet_convidados.get_all_records()
    df_convidados = pd.DataFrame(data_convidados)    

    worksheet_confirmados = spreadsheet.worksheet("Confirmados")
    data_confirmados = worksheet_confirmados.get_all_records()
    df_confirmados = pd.DataFrame(data_confirmados)       

    df_confirmados_convidados = df_confirmados.merge(df_convidados[['id_convidado', 'id_convite']], 'left', on = 'id_convidado')
    id_convites_confirmados = df_confirmados_convidados[df_confirmados_convidados['confirmado'] != ""]['id_convite'].values.tolist()

    id_convites = df_convidados['id_convite'].to_list()
    with st.form("confirm_presence"):
        st.title("Confirmar Presença")
        code = st.text_input("Digite o código do convite:")
        code = code.upper()

        if code in id_convites and code not in id_convites_confirmados:
            id_convite = df_convidados[df_convidados['id_convite'] == code]['id_convite'].values[0]
            convidados = df_convites[df_convites['id_convite'] == id_convite]['convidados'].values[0]

            lista_confirmados = {}
            if len(convidados) > 1:
                st.write("**Marque os convidados que irão ao casamento:**")
                for index in range(len(convidados)):
                    lista_confirmados[convidados[index]] = st.checkbox(convidados[index])

            else:
                resposta = st.radio(f"**{convidados[0]}, você deseja confirmar sua presença?**", options=["Sim", "Não"], key = "radio1", index = None)
                if resposta == "Sim":
                    lista_confirmados[convidados[0]] = True
                else:
                    lista_confirmados[convidados[0]] = False            

            lista_fotos_permitidas = {}
            lista_foto_existe = []
            for convidado in convidados:
                image_path = os.path.join(local_path, "resources", "images", "mosaico", convidado +'.jpg')
                lista_foto_existe.append(os.path.isfile(image_path))

            if len(convidados) > 1:
                for index in range(len(convidados)):
                    if index == 0 and True in lista_foto_existe:
                        st.write("**Marque as fotos que você permite que sejam exibidas nesta página:**") 
                    image_path = os.path.join(local_path, "resources", "images", "mosaico", convidados[index]+'.jpg')
                    if os.path.exists(image_path):
                        col1, col2, col3 = st.columns([.5, 3, 8])  # Ajuste a largura das colunas como preferir
                        with col1:
                            lista_fotos_permitidas[convidados[index]] = st.checkbox("", key = convidados[index])
                        with col2:
                            st.image(image_path, use_container_width=False)
            else:
                col1, col2 = st.columns([5, 11])  # Ajuste a largura das colunas como preferir
                with col1:
                    st.image(os.path.join(local_path, "resources", "images", "mosaico", convidados[0]+'.jpg'), use_container_width=True)

                resposta = st.radio("**Você permite que a foto acima seja exibida nesta página?**", options=["Sim", "Não"], key = "radio2", index = None)
                if resposta == "Sim":
                    lista_fotos_permitidas[convidados[0]] = True
                else:
                    lista_fotos_permitidas[convidados[0]] = False 

            for key, value in lista_fotos_permitidas.items():
                #if value == True:
                    # shutil.copy(os.path.join(local_path, "resources", "images", "mosaico", key + '.jpg'), 
                    #             os.path.join(local_path, "resources", "images", "mosaico", "permitidos",  key + '.jpg'))
                    df_confirmados.loc[df_confirmados['nome_convidado'] == key, 'autoriza_foto'] = value
            worksheet_confirmados = spreadsheet.worksheet('Confirmados')
            worksheet_confirmados.clear()
            df_confirmados_list = [df_confirmados.columns.tolist()] + df_confirmados.values.tolist()
            worksheet_confirmados.update("A1", df_confirmados_list)
               
            ok = st.form_submit_button("Salvar", use_container_width=True)

            if ok:
                for key, value in lista_confirmados.items():
                    if value == True:
                        df_confirmados.loc[df_confirmados['nome_convidado'] == key, 'confirmado'] = value
                        df_confirmados_list = [df_confirmados.columns.tolist()] + df_confirmados.values.tolist()
                        worksheet_confirmados.update("A1", df_confirmados_list)
                    else:
                        df_confirmados.loc[df_confirmados['nome_convidado'] == key, 'confirmado'] = value
                        df_confirmados_list = [df_confirmados.columns.tolist()] + df_confirmados.values.tolist()
                        worksheet_confirmados.update("A1", df_confirmados_list)
                st.rerun()

        elif code in id_convites and code in id_convites_confirmados:
            st.write("""Você já preencheu o formulário para este convite.
                        Caso tenha cometido algum erro ao preencher a confirmação
                        de presença, ou queira mudar o status de confirmação, favor
                        entrar em contato com os noivos.""")
            ok = st.form_submit_button("OK", use_container_width=True)   
            if ok:
                st.rerun()        


        elif code != "":
            st.write("""Convidado não encontrado. 
            Verifique se o código foi digitado 
            corretamente ou entre em contato com os noivos.""")
            ok = st.form_submit_button("Buscar", use_container_width=True)
        else:
            ok = st.form_submit_button("Buscar", use_container_width=True)

def exibir_mosaico(image_folder, link_font, font_name, spreadsheet):

    # Carregar imagens
    # image_paths = [os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(("png", "jpg", "jpeg"))]

    worksheet_confirmados = spreadsheet.worksheet("Confirmados")
    data_confirmados = worksheet_confirmados.get_all_records()
    df_confirmados = pd.DataFrame(data_confirmados)  
    list_autoriza_foto_names = df_confirmados[df_confirmados['autoriza_foto'] == 'TRUE']['nome_convidado'].values.tolist()
    # show_images = []
    # for photo in image_paths:
    #     for name in list_autoriza_foto_names:
    #         if name in photo:
    #             show_images.append(photo)
    #         else:
    #             pass

    # image_paths = show_images
    image_paths = []
    for nome in list_autoriza_foto_names:
        image_paths.append(os.path.join(image_folder) + "/" + nome + ".jpg")


    if not image_paths:
        pass
    else:
        # Adiciona descrição mosaico
        st.markdown(f"""
        <style>
        {link_font} /* Fonte Poppins */
            .mosaic-description {{
                font-size: 18px;
                font-family: {font_name}, sans-serif; 
                font-weight: 400;
                color: #333333;
                margin-bottom: 15px;
            }}
        </style>
        <div class="left-container">
            <div class="mosaic-description">Estes são os convidados que já confirmaram presença:</div>
        </div>
        """, unsafe_allow_html=True)
        # Controle de tamanho de célula no mosaico
        cell_size = 500
        
        # Calcular o número de células por linha
        total_images = len(image_paths)
        cells_per_row = ceil(sqrt(total_images))
        
        # Carregar e redimensionar imagens mantendo proporções
        resized_images = []
        for path in image_paths:
            img = Image.open(path)
            img.thumbnail((cell_size, cell_size))  # Reduzir para o tamanho máximo mantendo proporções
            
            # Centralizar imagem na célula
            canvas = Image.new('RGB', (cell_size, cell_size), (255, 255, 255))  # Fundo branco
            offset_x = (cell_size - img.width) // 2
            offset_y = (cell_size - img.height) // 2
            canvas.paste(img, (offset_x, offset_y))
            resized_images.append(canvas)
        
        # Criar o mosaico
        mosaic_width = cells_per_row * cell_size
        mosaic_height = ceil(total_images / cells_per_row) * cell_size
        mosaic = Image.new('RGBA', (mosaic_width, mosaic_height), (255, 255, 255, 0))  # Fundo branco
        
        for idx, img in enumerate(resized_images):
            x = (idx % cells_per_row) * cell_size
            y = (idx // cells_per_row) * cell_size
            mosaic.paste(img, (x, y))
        
        # Mostrar o mosaico no Streamlit
        st.image(mosaic, use_container_width=True)
 

def add_background_image(image_path):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpeg;base64,{encoded_image}");
        background-size: cover; /* Ajusta para cobrir toda a área */
        background-repeat: no-repeat; /* Evita repetição */
        background-attachment: fixed; /* Fixa o fundo para não rolar junto com o conteúdo */
    }}
    [data-testid="stHeader"] {{
        background-color: rgba(0, 0, 0, 0); /* Deixa o cabeçalho transparente */
    }}
    [data-testid="stSidebar"] {{
        background-color: rgba(255, 255, 255, 0.8); /* Fundo claro para a barra lateral */
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def confirmar_presenca(spreadsheet):
     # Ajustar o fundo e remover a faixa branca
    st.markdown(
        """
        <style>
        /* Estiliza o fundo de toda a página */
        [data-testid="stAppViewContainer"] {
            background-color: #f0f8ff; /* Cor de fundo */
            padding-top: 0rem; /* Remove o espaço superior */
        }
        /* Remove a margem no topo */
        [data-testid="stHeader"] {
            background-color: transparent; /* Deixa o cabeçalho transparente */
        }
        /* Estiliza a barra lateral (opcional) */
        [data-testid="stSidebar"] {
            background-color: #dcdcdc; /* Cor do fundo da barra lateral */
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    add_background_image("resources/images/sand_texture.jpg")
    link_font = "@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@200;400;500&display=swap');"
    font_name = 'Raleway'

    # Título da página
    st.markdown(f"""
    <style>
    {link_font} /* Fonte Poppins */
        .page-title {{
            font-size: 32px;
            font-family: {font_name}, sans-serif; 
            font-weight: bold;
            color: #333333;
            margin-bottom: 20px;
        }}
    </style>
    <div class="left-container">
        <div class="page-title">Confirmar Presença</div>
    </div>
    """, unsafe_allow_html=True)

    st.divider() 

    # Mosaico de fotos
    exibir_mosaico(os.getcwd()+"/resources/images/mosaico", link_font, font_name, spreadsheet)

    add_names_button = st.button(
        "Confirmar Presença", use_container_width=True
    )
    if add_names_button:
        tela_de_confirmacao(local_path, spreadsheet)
    st.divider()
          