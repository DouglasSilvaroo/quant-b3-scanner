
from supabase import create_client
import os

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================
# USUÁRIOS
# ==========================================

def criar_usuario(username, password):

    existente = supabase.table("usuarios").select("*").eq(
        "username",
        username
    ).execute()

    if existente.data:

        return False

    supabase.table("usuarios").insert({

        "username": username,
        "password": password

    }).execute()

    return True


def validar_usuario(username, password):

    resultado = supabase.table("usuarios").select("*").eq(
        "username",
        username
    ).eq(
        "password",
        password
    ).execute()

    return len(resultado.data) > 0

# ==========================================
# OPERAÇÕES
# ==========================================

def salvar_operacao(
    ativo1,
    ativo2,
    zscore,
    score,
    sinal
):

    supabase.table("operacoes").insert({

        "ativo1": ativo1,
        "ativo2": ativo2,
        "zscore": float(zscore),
        "score": float(score),
        "sinal": sinal

    }).execute()
