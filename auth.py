
import streamlit as st
import bcrypt

from database import (
    adicionar_usuario,
    validar_usuario
)

# ==========================================
# HASH
# ==========================================

def gerar_hash(senha):

    return bcrypt.hashpw(
        senha.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

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

    st.subheader("Cadastro")

    novo_usuario = st.text_input(
        "Usuário",
        key="cadastro_usuario"
    )

    nova_senha = st.text_input(
        "Senha",
        type="password",
        key="cadastro_senha"
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
                "Usuário cadastrado com sucesso!"
            )

        else:

            st.error(
                "Usuário já existe."
            )

# ==========================================
# LOGIN
# ==========================================

def tela_login():

    st.subheader("Login")

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

        # DEBUG
        print(usuario_db)

        if usuario_db is None:

            st.error(
                "Usuário não encontrado."
            )

            return

        senha_hash = usuario_db.get(
            "password"
        )

        if senha_hash is None:

            st.error(
                "Senha não encontrada no banco."
            )

            return

        senha_valida = verificar_senha(
            senha,
            senha_hash
        )

        if senha_valida:

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
