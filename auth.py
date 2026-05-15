
import streamlit as st

from database import (

    adicionar_usuario,
    validar_usuario

)

# ==========================================
# CADASTRO
# ==========================================

def tela_cadastro():

    st.subheader("📝 Cadastro")

    novo_usuario = st.text_input(
        "Usuário",
        key="cad_usuario"
    )

    nova_senha = st.text_input(
        "Senha",
        type="password",
        key="cad_senha"
    )

    if st.button("Cadastrar"):

        sucesso = adicionar_usuario(
            novo_usuario,
            nova_senha
        )

        if sucesso:

            st.success(
                "Usuário criado com sucesso!"
            )

        else:

            st.error(
                "Usuário já existe."
            )

# ==========================================
# LOGIN
# ==========================================

def tela_login():

    st.subheader("🔐 Login Institucional")

    usuario = st.text_input(
        "Usuário",
        key="login_usuario"
    )

    senha = st.text_input(
        "Senha",
        type="password",
        key="login_senha"
    )

    if st.button("Entrar"):

        validacao = validar_usuario(
            usuario,
            senha
        )

        if validacao:

            st.session_state["logado"] = True

            st.session_state["usuario"] = usuario

            st.success(
                "Login realizado!"
            )

            st.rerun()

        else:

            st.error(
                "Usuário ou senha inválidos."
            )
