
# ==========================================
# QUANT B3 SCANNER - BASE INSTITUCIONAL
# ==========================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from scanner import executar_scanner
from backtest import executar_backtest

from auth import (
    tela_login,
    tela_cadastro
)

from database import (
    criar_tabela_operacoes,
    criar_tabela_usuarios
)

from supabase_db import salvar_operacao

from statsmodels.tsa.stattools import coint
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant

# ==========================================
# CONFIG STREAMLIT
# ==========================================

st.set_page_config(
    page_title="PAINEL SPREADS",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# BANCO
# ==========================================

criar_tabela_usuarios()
criar_tabela_operacoes()

# ==========================================
# SESSION
# ==========================================

if "logado" not in st.session_state:
    st.session_state["logado"] = False

if "usuario" not in st.session_state:
    st.session_state["usuario"] = ""

# ==========================================
# LISTA B3
# ==========================================

LISTA_ATIVOS = [

    "PETR3.SA","PETR4.SA","VALE3.SA","PRIO3.SA",
    "RRRP3.SA","CSNA3.SA","USIM5.SA","GGBR4.SA",
    "ITUB4.SA","BBDC4.SA","BBAS3.SA","SANB11.SA",
    "BPAC11.SA","CMIG4.SA","CPFE3.SA","EQTL3.SA",
    "TAEE11.SA","EGIE3.SA","ABEV3.SA","LREN3.SA",
    "MGLU3.SA","JBSS3.SA","BRFS3.SA","MRFG3.SA",
    "SUZB3.SA","KLBN11.SA","VIVT3.SA","TIMS3.SA",
    "HAPV3.SA","RADL3.SA","RAIL3.SA","CCRO3.SA",
    "WEGE3.SA","SBSP3.SA","SAPR4.SA","BBSE3.SA",
    "CXSE3.SA","CYRE3.SA","MRVE3.SA","AZUL4.SA",
    "GOLL4.SA","ALUP11.SA","CPLE6.SA","B3SA3.SA",
    "ITSA4.SA","MULT3.SA","SLCE3.SA","SOJA3.SA",
    "UNIP6.SA","EMBR3.SA","GOAU4.SA","VBBR3.SA",
    "UGPA3.SA"

]

# ==========================================
# LOGIN
# ==========================================

if not st.session_state["logado"]:

    st.title("🏦 QUANT B3 INSTITUCIONAL")

    aba1, aba2 = st.tabs(["Login", "Cadastro"])

    with aba1:
        tela_login()

    with aba2:
        tela_cadastro()

    st.stop()

# ==========================================
# HEADER
# ==========================================

st.title("📊 PAINEL SPREADS")

st.markdown(
    f"### Usuário logado: {st.session_state['usuario']}"
)

if st.button("Logout"):

    st.session_state["logado"] = False
    st.rerun()

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Configurações")

ativo1 = st.sidebar.selectbox(
    "Ativo 1",
    LISTA_ATIVOS,
    index=0
)

ativo2 = st.sidebar.selectbox(
    "Ativo 2",
    LISTA_ATIVOS,
    index=1
)

periodo = st.sidebar.selectbox(
    "Período",
    ["50d", "100d", "200d", "300d"],
    index=2
)

st.sidebar.markdown("---")

spread_alvo = st.sidebar.number_input(
    "Tamanho da Camada",
    value=0.50,
    step=0.10
)

tolerancia = st.sidebar.number_input(
    "Tolerância",
    value=0.10,
    step=0.05
)

st.sidebar.markdown("---")

quantidade_ativo1 = st.sidebar.number_input(
    f"Lote {ativo1}",
    min_value=1,
    value=100
)

quantidade_ativo2 = st.sidebar.number_input(
    f"Lote {ativo2}",
    min_value=1,
    value=100
)

st.sidebar.markdown("---")

executar_scan = st.sidebar.button(
    "🚀 Executar Scanner"
)

# ==========================================
# DOWNLOAD DADOS
# ==========================================

try:

    dados = yf.download(
        [ativo1, ativo2],
        period=periodo,
        auto_adjust=True,
        progress=False
    )

    if dados.empty:
        st.error("Erro ao baixar dados.")
        st.stop()

    if isinstance(dados.columns, pd.MultiIndex):

        if "Close" in dados.columns.get_level_values(0):
            dados = dados["Close"]

        elif "Adj Close" in dados.columns.get_level_values(0):
            dados = dados["Adj Close"]

    dados = dados.dropna()

    serie1 = dados[ativo1]
    serie2 = dados[ativo2]

    correlacao = serie1.corr(serie2)

    resultado = coint(serie1, serie2)

    pvalue = resultado[1]

    modelo = OLS(
        serie1,
        add_constant(serie2)
    ).fit()

    hedge_ratio = float(modelo.params.iloc[1])

    spread_stat = serie1 - (
        hedge_ratio * serie2
    )

    media_stat = spread_stat.mean()
    desvio_stat = spread_stat.std()

    zscore = (
        spread_stat - media_stat
    ) / desvio_stat

    ultimo_z = float(zscore.iloc[-1])

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "Correlação",
        round(correlacao, 4)
    )

    col2.metric(
        "P-Value",
        round(pvalue, 4)
    )

    col3.metric(
        "Hedge Ratio",
        round(hedge_ratio, 4)
    )

    col4.metric(
        "Z-Score",
        round(ultimo_z, 2)
    )

    if ultimo_z > 2:

        sinal = "SHORT"
        st.error("🔴 SHORT SPREAD")

    elif ultimo_z < -2:

        sinal = "LONG"
        st.success("🟢 LONG SPREAD")

    else:

        sinal = "NEUTRO"
        st.warning("🟡 NEUTRO")

    score_reversao = min(
        round(
            abs(ultimo_z) * 20 +
            correlacao * 20,
            2
        ),
        100
    )

    salvar_operacao(
        ativo1,
        ativo2,
        round(ultimo_z, 2),
        score_reversao,
        sinal
    )

    st.markdown("---")

    st.subheader("🧠 Score Institucional")

    st.metric(
        "Reversão Score",
        f"{score_reversao}/100"
    )

except Exception as erro:

    st.error(f"Erro: {erro}")

# ==========================================
# SCANNER
# ==========================================

if executar_scan:

    st.markdown("---")

    st.header(
        "🚀 Scanner Quantitativo"
    )

    with st.spinner("Analisando pares..."):

        try:

            df_scan = executar_scanner(
                lista_ativos=LISTA_ATIVOS,
                periodo=periodo,
                correlacao_minima=0.70,
                pvalue_maximo=0.05
            )

            if df_scan.empty:

                st.warning(
                    "Nenhum par encontrado."
                )

            else:

                st.success(
                    f"{len(df_scan)} pares encontrados"
                )

                st.dataframe(
                    df_scan.head(20),
                    use_container_width=True
                )

        except Exception as erro:

            st.error(
                f"Erro Scanner: {erro}"
            )
