
from supabase_db import (
    criar_usuario,
    buscar_usuario,
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
# ADICIONAR USUÁRIO
# ==========================================

def adicionar_usuario(
    username,
    password
):

    return criar_usuario(
        username,
        password
    )

# ==========================================
# VALIDAR USUÁRIO
# ==========================================

def validar_usuario(
    username
):

    return buscar_usuario(
        username
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
