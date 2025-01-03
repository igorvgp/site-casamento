import streamlit as st
import base64
from datetime import datetime, timedelta
import time

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

def styled_paragraph(
    text, 
    element_name="paragraph",
    color="black", 
    font_size="16px", 
    font_weight="300",
    align="left", 
    font_family="Arial", 
    font_path=None, 
    margin_top="20px",
    margin_bottom="20px",
    width="1700px"
):
    """
    Função para exibir um parágrafo estilizado com configurações de cor, tamanho e alinhamento.

    Parâmetros:
    - text (str): O texto do parágrafo.
    - color (str): Cor do texto.
    - font_size (str): Tamanho da fonte padrão.
    - font_weight: espessura da fonte
    - align (str): Alinhamento do texto (left, center, right, justify).
    - font_family (str): Nome da fonte.
    - font_path (str): Caminho para uma fonte personalizada no formato .ttf.
    - margin_top (str): Espaço acima do parágrafo (ex: "10px", "20px").
    - width: Define a largura máxima do texto.
    """
    # Se uma fonte local for fornecida, convertemos para Base64
    if font_path:
        with open(font_path, "rb") as font_file:
            font_data = base64.b64encode(font_file.read()).decode("utf-8")
        font_face = f"""
        @font-face {{
            font-family: '{font_family}';
            src: url('data:font/ttf;base64,{font_data}') format('truetype');
        }}
        """
        st.markdown(f"<style>{font_face}</style>", unsafe_allow_html=True)

    # CSS responsivo com media queries
    responsive_style = f"""
    <style>
        @media (max-width: 600px) {{
            .{element_name} {{
                font-size: 12px; /* Tamanho menor para telas pequenas */
            }}
        }}
        @media (min-width: 601px) and (max-width: 1200px) {{
            .{element_name} {{
                font-size: 14px; /* Tamanho médio para telas médias */
            }}
        }}
        @media (min-width: 1201px) {{
            .{element_name} {{
                font-size: {font_size}; /* Tamanho padrão para telas grandes */
            }}
        }}
    </style>
    """

    st.markdown(responsive_style, unsafe_allow_html=True)

    # Exibir o parágrafo com as configurações de estilo CSS
    html_content = f"""
    <div style="
        display: flex;
        justify-content: {align};
        margin-top: {margin_top};
        margin-bottom: {margin_bottom};
    ">
        <p class={element_name} style="
            color: {color};
            text-align: {align};
            width: {width};
            margin: 0 auto;
            font-family: {font_family}, sans-serif;
            font-weight: {font_weight};
            line-height: 1.6;
            word-wrap: break-word;
        ">
            {text}
        </p>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)
    
def countdown_to_date(target_date, placeholder):
    """
    Mostra uma contagem regressiva até a data e horário alvo.
    :param target_date: datetime object representando a data alvo.
    :param placeholder: st.empty() para atualizar dinamicamente o conteúdo.
    """
    while True:
        # Obtém a data e hora atuais
        now = datetime.now()
        remaining_time = target_date - now

        # Se a data alvo já passou
        if remaining_time.total_seconds() <= 0:
            placeholder.success("Chegou o grande dia! 🎉")
            break

        # Calcula os componentes do tempo restante
        days = remaining_time.days
        seconds = remaining_time.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60

        # Atualiza o texto na página
        placeholder.markdown(
            f"""
            <h3 style="text-align: center;">
                Faltam <strong>{days}</strong> dias, <strong>{hours}</strong> horas,
                <strong>{minutes}</strong> minutos e <strong>{seconds}</strong> segundos.
            </h3>
            """,
            unsafe_allow_html=True
        )

        # Aguarda 1 segundo antes de atualizar
        time.sleep(1)

def boas_vindas():
    font_path = "resources/fonts/MonterchiSerif.ttf"
    font_name = "Monterchi Serif"

    # Adiciona imagem de fundo
    add_background_image("resources/images/sand_texture.jpg")

    st.image("resources/images/logo.png", use_container_width=True,  caption=None)

    styled_paragraph(
        text = f'''Criamos este espaço com muito carinho para compartilhar com você todas as informações importantes
        do nosso casamento. Não se esqueça de confirmar a sua presença!''', 
        element_name = "text_welcome",
        color="#424c34", 
        font_size="25px",
        font_weight="300", 
        align="center", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="0px",
        margin_bottom="0px",
        width="800px"
    )

    # # Contagem regressiva
    # target_date = datetime(2025, 8, 2, 0, 0, 0)
    # countdown_placeholder = st.empty()
    # countdown_to_date(target_date, countdown_placeholder)
