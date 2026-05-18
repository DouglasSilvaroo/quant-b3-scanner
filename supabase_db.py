
import os

from supabase import create_client

# ==========================================
# CONEXÃO
# ==========================================

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================
# CRIAR USUÁRIO
# ==========================================

def criar_usuario(
    username,
    password
):

    try:

        resposta = supabase.table(
            "usuarios"
        ).select("*").eq(
            "username",
            username
        ).execute()

        if len(resposta.data) > 0:

            return False

        supabase.table(
            "usuarios"
        ).insert({

            "username": username,
            "password": password

        }).execute()

        return True

    except Exception as erro:

        print("ERRO CRIAR USUARIO:")
        print(erro)

        return False

# ==========================================
# BUSCAR USUÁRIO
# ==========================================

def buscar_usuario(username):

    try:

        resposta = supabase.table(
            "usuarios"
        ).select("*").eq(
            "username",
            username
        ).execute()

        if len(resposta.data) > 0:

            return resposta.data[0]

        return None

    except Exception as erro:

        print("ERRO BUSCAR:")
        print(erro)

        return None

# ==========================================
# SALVAR OPERAÇÃO
# ==========================================

def salvar_operacao(

    ativo1,
    ativo2,
    zscore,
    score,
    sinal

):

    try:

        supabase.table(
            "operacoes"
        ).insert({

            "ativo1": ativo1,
            "ativo2": ativo2,
            "zscore": zscore,
            "score": score,
            "sinal": sinal

        }).execute()

    except Exception as erro:

        print("ERRO SALVAR:")
        print(erro)
