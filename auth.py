
import streamlit as st
import bcrypt

from database import (
    adicionar_usuario,
    validar_usuario
)

# ==========================================
# HASH SENHA
# ==========================================

def gerar_hash(senha):

    senha_bytes = senha.encode("utf-8")

    salt = bcrypt.gensalt()

    hash_senha = bcrypt.hashpw(
        senha_bytes,
        salt
    )

    return hash_senha.decode("utf-8")

# ==========================================
# VERIFICAR SENHA
# ==========================================

def verificar_senha(
    senha,
    hash_senha
):

    return bcrypt.checkpw(
        senha.encode("utf-8"),
        hash_senha.encode("utf-8")
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

        if len(nova_senha) < 6:

            st.error(
                "Senha deve ter pelo menos 6 caracteres."
            )

            return

        senha_hash = gerar_hash(
            nova_senha
        )

        sucesso = adicionar_usuario(
            novo_usuario,
            senha_hash
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

        usuario_db = validar_usuario(
            usuario
        )

        if usuario_db:

            senha_hash = usuario_db["password"]

            if verificar_senha(
                senha,
                senha_hash
            ):

                st.session_state["logado"] = True

                st.session_state["usuario"] = usuario

                st.success(
                    "Login realizado!"
                )

                st.rerun()

            else:

                st.error(
                    "Senha inválida."
                )

        else:

            st.error(
                "Usuário não encontrado."
            )
