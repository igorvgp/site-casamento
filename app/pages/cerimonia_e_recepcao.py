import streamlit as st
import base64
import folium
from streamlit_folium import st_folium

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

def show_map(lat, 
             long, 
             width=700, 
             height=500):
    """
    JavaScript para obter a largura e altura da tela.
    """
    st.markdown(
        """
        <script>
        const size = {
            width: window.innerWidth,
            height: window.innerHeight,
        };
        const element = document.querySelector('#map-size');
        element.textContent = JSON.stringify(size);
        </script>
        <div id="map-size" style="display: none;"></div>
        """,
        unsafe_allow_html=True
    )
    map_size = st.session_state.get("map_size", {"width": 700, "height": 500})
    width = min(map_size.get("width", 700), 700)  # Limita largura máxima em 700px
    height = int(map_size.get("height", 500) * 0.5)  # Ajusta altura proporcional

    if st.session_state.get("js_enabled", False):
        map_size_str = st.experimental_get_query_params().get("map_size", ["{}"])[0]
        map_size.update(eval(map_size_str))

    # Cria o mapa centralizado na localização
    mapa = folium.Map(location=[lat, long], zoom_start=15)    

    # Adiciona um marcador no mapa
    folium.Marker([lat, long], 
                  popup="Santuário N.S. da Piedade",
                  icon=folium.Icon(color="red"),).add_to(mapa)

    # Renderiza o mapa no Streamlit
    st_data = st_folium(mapa, width=width, height=height)

def cerimonia_e_recepcao():
    
    font_path = "resources/fonts/MonterchiSerif.ttf"
    font_name = "Monterchi Serif"

    # Adiciona imagem de fundo
    add_background_image("resources/images/sand_texture.jpg")

    styled_paragraph(
        text = f'''CERIMÔNIA''', 
        element_name="cerimonia",
        color="#424c34", 
        font_size="40px",    
        font_weight="500",
        align="center", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="0px",
        margin_bottom="0px",
        width="800px"
    )    

    styled_paragraph(
        text = f'''A cerimônia será no Santuário Nossa Senhora da Piedade, na Rua Delfim Moreira, 
        s/nº, Centro, Pará de Minas – MG.''', 
        element_name="cerimonia_text",
        color="#424c34", 
        font_size="22px",
        font_weight="300", 
        align="justify", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="0px",
        margin_bottom="0px",
        width="800px"
    )
    styled_paragraph(
        text = f''' <a href='https://maps.app.goo.gl/oP5eWnVEyGXJQTZx7'>Clique aqui</a> para abrir no google maps''', 
        element_name="cerimonia_clique_aqui",
        color="#424c34", 
        font_size="18px",
        font_weight="300", 
        align="justify", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="-25px",
        margin_bottom="0px",
        width="800px"
    )

    # Plot mapa cerimônia
    latitude = -19.8605176
    longitude = -44.6082123

    show_map(latitude, longitude, width=700, height=500)

    styled_paragraph(
        text = f'''RECEPÇÃO''', 
        element_name="recepcao",
        color="#424c34", 
        font_size="40px",    
        font_weight="500",
        align="center", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="0px",
        margin_bottom="0px",
        width="800px"
    )    

    styled_paragraph(
        text = f'''A recepção será no Espaço Cumari, em Tavares, Pará de Minas - MG.''', 
        element_name="recepcao_text",
        color="#424c34", 
        font_size="22px",
        font_weight="300", 
        align="justify", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="0px",
        margin_bottom="0px",
        width="800px"
    )
    styled_paragraph(
        text = f''' <a href='https://maps.app.goo.gl/f19c5UaTRxUHUVnH7'>Clique aqui</a> para abrir no google maps''', 
        element_name="recepcao_clique_aqui",
        color="#424c34", 
        font_size="18px",
        font_weight="300", 
        align="justify", 
        font_family = font_name, 
        font_path = font_path, 
        margin_top="-25px",
        margin_bottom="0px",
        width="800px"
    )

    # Plot mapa recepção
    latitude = -19.829120645184165
    longitude = -44.52463727519528

    show_map(latitude, longitude, width=700, height=500)