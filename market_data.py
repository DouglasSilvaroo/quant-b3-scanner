import streamlit as st
import yfinance as yf
import pandas as pd


@st.cache_data(ttl=3600)

def baixar_dados_market(

    ativos,

    periodo="1y"

):

    try:

        dados = yf.download(

            ativos,

            period=periodo,

            auto_adjust=True,
            progress=False

        )

        if dados.empty:

            return pd.DataFrame()

        fechamento = dados["Close"]

        fechamento = fechamento.dropna(

            how="all"

        )

        return fechamento

    except Exception as erro:

        print("ERRO:")
        print(erro)

        return pd.DataFrame()
