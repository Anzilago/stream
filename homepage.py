import streamlit as st

secao_usuario = st.session_state
nome_usuario = None
if "username" in secao_usuario:
    nome_usuario = secao_usuario.name

coluna_esquerda, coluna_direita = st.columns([1, 1.5])

if nome_usuario:
    coluna_esquerda.title(f"Bem vindo, {nome_usuario}!")

botao_dashboards = coluna_esquerda.button("Dashboards Projetos")
botao_indicadores = coluna_esquerda.button("Principais Indicadores")

if botao_dashboards:
    st.switch_page("dashboard.py")
if botao_indicadores:
    st.switch_page("indicadores.py")

coluna_direita.image("fattura.png")
