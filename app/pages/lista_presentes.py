import base64
import pandas as pd
import streamlit as st
from datetime import datetime
from pathlib  import Path   
from google.oauth2.service_account import Credentials
import gspread


@st.dialog("Presentear")
def handle_button_click_1(
    image_path, spreadsheet
#    db_conn: PostgresqlDatabaseConnector
):
    with st.form("new_name"):
        st.write(
            "Leia o QR Code ou copie o código PIX abaixo:"
        )
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        alt_text = "image"

        # HTML para ajustar a imagem a 50% do contêiner
        image_html = f"""
        <style>
            .image-container {{
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%; /* Garante que o contêiner ocupa toda a largura */
            }}
            .image-container img {{
                width: 50%; /* Ajusta a imagem para ocupar 50% do contêiner */
                max-width: 100%; /* Garante responsividade */
                height: auto; /* Mantém a proporção da imagem */
                border-radius: 10px; /* Borda arredondada opcional */
            }}
        </style>
        <div class="image-container">
            <img src="data:image/jpeg;base64,{encoded_image}" alt="{alt_text}">
        </div>
        """
        # Renderiza o HTML com a imagem
        st.markdown(image_html, unsafe_allow_html=True)
        
        st.write("")
        
        st.code("00020126580014BR.GOV.BCB.PIX01366f24ae58-c4be-4c30-bcee-1a6c64aa37ec52040000530398654040.015802BR5925Igor Vinicius Gomes Perei6009SAO PAULO62140510SvWReKzy7x6304ECEB")

        st.write("")

        st.title("Deixe sua mensagem de carinho")
        st.write("(opcional)")

        nome = st.text_input("Digite seu nome")
        mensagem = st.text_area("Digite sua mensagem")

        ok = st.form_submit_button("Enviar", use_container_width=True)
        if "n" not in st.session_state:
            st.session_state.n = 0
        if ok:
            if len(nome) == 0 and len(mensagem) == 0:
                st.rerun()
            elif ((len(nome) > 0 and len(mensagem) > 0 and (st.session_state.n == 0 or st.session_state.n == 1)) 
            or (len(nome) == 0 and len(mensagem) > 0)):
                with st.spinner("Executando envio..."):
                    pass
                    worksheet_mensagens = spreadsheet.worksheet("Mensagens")
                    data_mensagens = worksheet_mensagens.get_all_records()
                    df_mensagens = pd.DataFrame(data_mensagens)    
                    df_nova_mensagem = pd.DataFrame({'timestamp':[str(datetime.now())], 'nome':[nome], 'mensagem':[mensagem]})
                    df_mensagens = pd.concat([df_mensagens, df_nova_mensagem])
                    # Inserir dados de mensagens no google sheets
                    worksheet_mensagens = spreadsheet.worksheet('Mensagens')
                    df_mensagens_list = [df_mensagens.columns.tolist()] + df_mensagens.values.tolist()
                    worksheet_mensagens.update("A1", df_mensagens_list)
                    st.session_state.n = 0
                st.rerun()
            elif len(nome) > 0 and len(mensagem) == 0 and st.session_state.n != 0:
                st.session_state.n = 0
                st.rerun()
            else:
                st.write("Toque em 'enviar' novamente")
                st.session_state.n = 1
    
def handle_button_click(link):
    st.markdown(f"""
        <meta http-equiv="refresh" content="0; url={link}">
    """, unsafe_allow_html=True)


def render_product(image_path, name, price, link, key, link_font, font_name, spreadsheet):
    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

    html_content = f"""
        <style>
        {link_font} /* Fonte Poppins */
        
        .center-container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            max-width: 300px; 
            width: 100%;
            padding: 20px; 
            margin-top: 30px; 
            margin-bottom: 5px;
            text-align: center;
        }}
        .custom-image {{
            width: 90%; 
            border-radius: 15px;
            margin-bottom: 20px;
        }}
        .item-name {{
            font-size: 16px;
            font-family: {font_name}, sans-serif; 
            color: #333333;
            margin-bottom: 15px;
        }}
        .item-price {{
            font-size: 24px;
            font-family: {font_name}, sans-serif; 
            font-weight: bold;
            color: #555555;
            margin-bottom: 3px;
        }}
        .button-container {{
            display: flex;
            justify-content: center;
            align-items: center;
            width: 100%;
        }}
        .custom-button {{
            display: inline-flex;
            justify-content: center;
            align-items: center;
            padding: 10px 36px;  /* Aumentado */
            font-size: 18px;     /* Aumentado */
            font-weight: normal;
            color: white !important;
            background-color: #d2b48c;
            border: none;
            border-radius: 45px;
            text-align: center;
            cursor: pointer;
            margin-top: 10px;
            text-decoration: none !important;
            transition: background-color 0.3s ease, box-shadow 0.3s ease;
            min-width: 170px;  /* Um pouco maior */
            box-shadow: none;
        }}
        .custom-button:hover {{
            background-color: #c3a37c;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }}
        </style>
        <div class="center-container">
            <img src="data:image/jpeg;base64,{encoded_image}" class="custom-image" alt="{name}">
            <div class="item-name">{name}</div>
            <div class="item-price">{price}</div>
            <a href="{link}" target="_blank" class="custom-button">Presentear</a>
        </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


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

def lista_presentes(spreadsheet):

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

    # Adiciona imagem de fundo
    add_background_image("resources/images/sand_texture.jpg")
    link_font = "@import url('https://fonts.googleapis.com/css2?family=Raleway:wght@200;400;500&display=swap');"
    font_name = 'Raleway'

    # Adiciona título da página
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
        <div class="page-title">Lista de Presentes</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

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

    # Lista de produtos
    worksheet_produtos = spreadsheet.worksheet("Produtos")
    data_produtos = worksheet_produtos.get_all_records()
    df_produtos = pd.DataFrame(data_produtos)
    produtos = df_produtos.to_dict(orient='records')

    # Renderizar produtos
    for i in range(0, len(produtos), 3):
        cols = st.columns(3)
        for j, produto in enumerate(produtos[i:i+3]):
            with cols[j]:
                try:
                    render_product(
                        produto["path"],
                        produto["nome"],
                        produto["preco"],
                        produto["link"],
                        f"{i+j}",  # Chave única
                        link_font,
                        font_name,
                        spreadsheet
                    )
                except:
                    pass
