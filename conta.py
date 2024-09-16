import streamlit as st
from models import session, Usuario
import streamlit_authenticator as stauth

st.title("Criar Conta")

form = st.form("form_criar_conta")
nome_usuario = form.text_input("Nome do usuário")
email_usuario = form.text_input("Email do usuário")
senha_usuario = form.text_input("Senha do usuário", type="password")
admin_usuario = form.checkbox("É um admin")
botao_submit = form.form_submit_button("Enviar")

if botao_submit:
    lista_usuarios_existentes = session.query(Usuario).filter_by(email=email_usuario).all()
    if len(lista_usuarios_existentes) > 0:
        st.write("Ja existe esse email")
    else:
        senha_criptografada = stauth.Hasher([senha_usuario]).generate()[0]
        usuario = Usuario(nome=nome_usuario, senha=senha_criptografada, email=email_usuario, admin=admin_usuario)
        session.add(usuario)
        session.commit()
        st.write("Cadastrado com sucesso!")
        st.switch_page("homepage.py")