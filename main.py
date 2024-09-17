import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth
from models import session, Usuario

# Esconder o ícone do GitHub e a marca d'água do Streamlit
hide_streamlit_style = """
    <style>

    footer {visibility: hidden;}

    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

lista_usuarios = session.query(Usuario).all()

#senhas_criptografadas = stauth.Hasher(["12345", "12345"]).generate()

credenciais = {"usernames":{
    usuario.email: {"name": usuario.nome, "password": usuario.senha} for usuario in lista_usuarios
}}

authenticator = stauth.Authenticate(credenciais, "credencias_fattura", "fsyfus%$67fs76AH7", cookie_expiry_days=30)

def autenticar_usuario(authenticator):
    nome, status_autenticacao, username = authenticator.login()

    if status_autenticacao:
        return {"nome": nome, "username": username}
    elif status_autenticacao == False:
        st.error("Usuário ou senha inválido!")
    else:
        st.error("Preencha para fazer login!")

def logout():
    authenticator.logout()

dados_usuario = autenticar_usuario(authenticator)

if dados_usuario:
    @st.cache_data
    def carregar_dados():
        tabela = pd.read_excel("Base.xlsx")
        return tabela

    base = carregar_dados()

    email_usuario = dados_usuario["username"]
    usuario = session.query(Usuario).filter_by(email=email_usuario).first()

    if usuario.admin:
        pg = st.navigation(
            {
                "Home": [st.Page("homepage.py", title="Fattura+")],
                "Dashboards": [st.Page("dashboard.py", title="Dashboard"), st.Page("indicadores.py", title="Indicadores")],
                "Conta": [st.Page(logout, title="Sair"), st.Page("conta.py", title="Criar Conta")]
            }
        )
    else:
        pg = st.navigation(
        {
            "Home": [st.Page("homepage.py", title="Fattura+")],
            "Dashboards": [st.Page("dashboard.py", title="Dashboard"), st.Page("indicadores.py", title="Indicadores")],
            "Conta": [st.Page(logout, title="Sair")]
        }
    )
        
    pg.run()
