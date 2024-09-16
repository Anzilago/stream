import streamlit as st
import pandas as pd
import streamlit_authenticator as stauth

senhas_criptografadas = stauth.Hasher(["12345", "12345"]).generate()

credenciais = {"usernames":{
    "anzilago": {"name": "Henrique", "password": senhas_criptografadas[0]},
    "glis":{"name": "Glislayne", "password": senhas_criptografadas[1]},
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

    pg = st.navigation(
        {
            "Home": [st.Page("homepage.py", title="Fattura+")],
            "Dashboards": [st.Page("dashboard.py", title="Dashboard"), st.Page("indicadores.py", title="Indicadores")],
            "Conta": [st.Page(logout, title="Sair"), st.Page("conta.py", title="Criar Conta")]
        }
    )

    pg.run()