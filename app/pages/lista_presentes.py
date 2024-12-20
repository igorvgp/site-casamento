import base64
import pandas as pd
import streamlit as st
from datetime import datetime

@st.dialog("Presentear")
def handle_button_click(
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
            }}vbnm       
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
        mensagem = st.input("Digite sua mensagem")

        ok = st.form_submit_button("Enviar", use_container_width=True)
        if ok:
            if len(mensagem) > 0:
                with st.spinner("Executando envio..."):
                    pass
                    worksheet_mensagens = spreadsheet.worksheet("Mensagens")
                    data_mensagens = worksheet_mensagens.get_all_records()
                    df_mensagens = pd.DataFrame(data_mensagens)    
                    #df_mensagens = pd.read_csv('data/mensagens.csv', sep = ';')
                    df_nova_mensagem = pd.DataFrame({'timestamp':[str(datetime.now())], 'nome':[nome], 'mensagem':[mensagem]})
                    df_mensagens = pd.concat([df_mensagens, df_nova_mensagem])
                    # Inserir dados de mensagens no google sheets
                    worksheet_mensagens = spreadsheet.worksheet('Mensagens')
                    df_mensagens_list = [df_mensagens.columns.tolist()] + df_mensagens.values.tolist()
                    worksheet_mensagens.update("A1", df_mensagens_list)
            st.rerun()

def render_product(image_path, name, price, key, link_font, font_name, spreadsheet):
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
        </style>
        <div class="center-container">
            <img src="data:image/jpeg;base64,{encoded_image}" class="custom-image" alt="{name}">
            <div class="item-name">{name}</div>
            <div class="item-price">{price}</div>
        </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)

    button_key = f"gift_button_{key}"  # Chave única por produto
    button_present = st.button("Presentear", key=button_key)

    st.markdown("""
        <style>
        .stButton {
            display: flex;
            justify-content: center;
        }
        .stButton>button {
            display: inline-block;
            padding: 7px 24px; 
            font-size: 13px;
            font-weight: bold;
            color: white !important;
            background-color: #d2b48c;
            border: none;
            border-radius: 45px;
            text-align: center;
            cursor: pointer;
            margin-top: 10px; 
        }
        .stButton>button:hover {
            background-color: #c3a37c; 
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

    if button_present:
        handle_button_click("resources/images/qr_liquidificador.png", spreadsheet)

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

    # Lista de produtos
    produtos = [
        {"image": "resources/images/liquidificador.jpg", "name": "Liquidificador", "price": "R$140,00"},
        {"image": "resources/images/airfryer.jpg", "name": "AirFryer", "price": "R$550,00"},
        {"image": "resources/images/ar-condicionado.jpg", "name": "Ar Condicionado", "price": "R$3100,00"},
        {"image": "resources/images/sofa.jpg", "name": "Sofá", "price": "R$2500,00"},
        {"image": "resources/images/panelas.jpg", "name": "Jogo de Panelas", "price": "R$400,00"},
        {"image": "resources/images/mesa-jantar.jpg", "name": "Mesa de Jantar", "price": "R$3500,00"}
    ]

    # Renderizar produtos
    for i in range(0, len(produtos), 3):
        cols = st.columns(3)
        for j, produto in enumerate(produtos[i:i+3]):
            with cols[j]:
                render_product(
                    produto["image"],
                    produto["name"],
                    produto["price"],
                    f"{i+j}",  # Chave única
                    link_font,
                    font_name,
                    spreadsheet
                )
