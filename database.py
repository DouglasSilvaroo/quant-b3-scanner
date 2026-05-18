
from supabase_db import (
    criar_usuario,
    validar_usuario,
    salvar_operacao
)

# ==========================================
# TABELAS
# ==========================================

def criar_tabela_usuarios():
    pass

def criar_tabela_operacoes():
    pass

# ==========================================
# USUÁRIOS
# ==========================================

def adicionar_usuario(username, password):

    return criar_usuario(
        username,
        password
    )

# ==========================================
# LOGIN
# ==========================================

def validar_login(username, password):

    return validar_usuario(
        username,
        password
    )

# ==========================================
# OPERAÇÕES
# ==========================================

def salvar_trade(
    ativo1,
    ativo2,
    zscore,
    score,
    sinal
):

    salvar_operacao(

        ativo1,
        ativo2,
        zscore,
        score,
        sinal

    )
