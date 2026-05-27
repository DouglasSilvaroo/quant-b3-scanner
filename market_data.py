import pandas as pd
import yfinance as yf
import streamlit as st
import time


# ==========================================
# DOWNLOAD MARKET DATA
# ==========================================

@st.cache_data(

    ttl=3600,

    show_spinner=False

)

def baixar_dados_market(

    ativos,

    periodo="1y"

):

    try:

        # ==========================================
        # VALIDAÇÃO
        # ==========================================

        if not ativos:

            return pd.DataFrame()

        # ==========================================
        # REMOVER DUPLICADOS
        # ==========================================

        ativos = list(

            set(ativos)

        )

        print("ATIVOS SOLICITADOS:")

        print(ativos)

        # ==========================================
        # DOWNLOAD LOTE
        # ==========================================

        dados = yf.download(

            ativos,

            period=periodo,

            auto_adjust=True,

            progress=False,

            threads=False

        )

        # ==========================================
        # VALIDAÇÃO
        # ==========================================

        if dados.empty:

            print("DATAFRAME VAZIO")

            return pd.DataFrame()

        # ==========================================
        # CLOSE
        # ==========================================

        if len(ativos) == 1:

            fechamento = dados[["Close"]].copy()

            fechamento.columns = ativos

        else:

            fechamento = dados["Close"].copy()

        # ==========================================
        # LIMPEZA
        # ==========================================

        fechamento = fechamento.dropna(

            how="all"

        )

        fechamento.index = pd.to_datetime(

            fechamento.index

        )

        fechamento = fechamento.sort_index()

        # ==========================================
        # LOG
        # ==========================================

        print("COLUNAS FINAIS:")

        print(

            fechamento.columns.tolist()

        )

        print(

            fechamento.tail()

        )

        # ==========================================
        # PEQUENO DELAY
        # ==========================================

        time.sleep(0.5)

        return fechamento

    except Exception as erro:

        print("ERRO MARKET DATA:")

        print(erro)

        return pd.DataFrame()
