import streamlit as st
import base64

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
    color="black", 
    font_size="16px", 
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
            .responsive-paragraph {{
                font-size: 12px; /* Tamanho menor para telas pequenas */
            }}
        }}
        @media (min-width: 601px) and (max-width: 1200px) {{
            .responsive-paragraph {{
                font-size: 14px; /* Tamanho médio para telas médias */
            }}
        }}
        @media (min-width: 1201px) {{
            .responsive-paragraph {{
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
        <p class="responsive-paragraph" style="
            color: {color};
            text-align: center;
            width: {width};
            margin: 0 auto;
            font-family: {font_family}, sans-serif;
            line-height: 1.6;
            word-wrap: break-word;
        ">
            {text}
        </p>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)


def boas_vindas():
    font_path = "resources/fonts/MonterchiSerif.ttf"
    font_name = "Monterchi Serif"
    # Adiciona imagem de fundo
    add_background_image("resources/images/sand_texture.jpg")

    st.image("resources/images/logo.png")

    styled_paragraph(
        text = f'''Criamos este espaço com muito carinho para compartilhar com você todas as informações importantes
        do nosso casamento. Não se esqueça de confirmar a sua presença!''', 
        color="black", 
        font_size="25px", 
        align="center", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="20px",
        margin_bottom="0px",
        width="800px"
    )
