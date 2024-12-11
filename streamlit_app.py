import os
import streamlit as st
from app.pages.cerimony import cerimony
from app.pages.presents import presents
from app.pages.lista_presentes import lista_presentes
from app.utils import styled_write

# Definir a configuração da página
st.set_page_config(layout="wide")

# Adicionar CSS personalizado para ajustar a largura e o estilo dos botões
st.markdown("""
    <style>
        .main .block-container {
            max-width: 1200px;  /* Ajuste a largura máxima conforme necessário */
            padding-left: 2rem;  /* Ajuste o preenchimento da esquerda */
            padding-right: 2rem; /* Ajuste o preenchimento da direita */
        }
        /* Estilo personalizado para os botões */
        .stButton>button {
            background-color: transparent; /* Cor de fundo */
            color: black; /* Cor do texto */
            border-radius: 10px; /* Bordas arredondadas */
            border: 0px solid #4CAF50; /* Cor da borda */
            padding: 10px 20px; /* Espaçamento interno */
            font-size: 24px !important; /* Tamanho da fonte */
            cursor: pointer; /* Mostrar cursor como pointer */
            white-space: nowrap; /* Evitar quebra de texto */
            transition: background-color 0.3s ease, transform 0.2s ease; /* Animação */
            display: inline-block; /* Tornar o botão flexível no tamanho */
        }
        /* Efeito de hover nos botões */
        .stButton>button:hover {
            background-color: grey; /* Cor de fundo no hover */
            transform: scale(1.05); /* Leve aumento no tamanho */
        }
    </style>
""", unsafe_allow_html=True)

# Definir estado inicial da navegação
if "current_page" not in st.session_state:
    st.session_state.current_page = "cerimony"

# Função para alterar a página
def set_page(page_name):
    st.session_state.current_page = page_name

# Função para exibir links fixos no topo
def navigation_links():
    col1, col2, col3 = st.columns(3)

    with col1:
        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol1:
            if st.button("Cerimônia"):
                set_page("cerimony")
    with col2:
        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol2:
            if st.button("Presentes"):
                set_page("presents")
    with col3:
        subcol1, subcol2, subcol3 = st.columns(3)
        with subcol3:
            if st.button("Lista de Presentes"):
                set_page("lista_presentes")

# Exibir os links de navegação fixos
navigation_links()

# Configurar o conteúdo com base na página atual
if st.session_state.current_page == "cerimony":
    cerimony()
elif st.session_state.current_page == "presents":
    presents()
elif st.session_state.current_page == "lista_presentes":
    lista_presentes()
