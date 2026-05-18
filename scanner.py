
# ==========================================
# SCANNER QUANT B3 PROFISSIONAL
# ==========================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

from concurrent.futures import ThreadPoolExecutor

from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant
from statsmodels.tsa.stattools import coint

# ==========================================
# CACHE DOWNLOAD
# ==========================================

@st.cache_data(ttl=3600)

def baixar_dados(lista_ativos, periodo="200d"):

<<<<<<< HEAD
=======
    st.cache_data.clear()

    yf.shared._DFS = {}
>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
    dados = yf.download(
        lista_ativos,
        period=periodo,
        auto_adjust=True,
        progress=False,
        threads=True
    )

<<<<<<< HEAD
=======
    # ======================================
    # MULTI INDEX
    # ======================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
    if isinstance(dados.columns, pd.MultiIndex):

        if "Close" in dados.columns.get_level_values(0):

            dados = dados["Close"]

        elif "Adj Close" in dados.columns.get_level_values(0):

            dados = dados["Adj Close"]

    dados = dados.dropna(axis=1, how="all")

    return dados

# ==========================================
# HALF LIFE
# ==========================================

def calcular_half_life(spread):

    spread_lag = spread.shift(1)

    spread_delta = spread - spread_lag

    spread_lag = spread_lag.dropna()

    spread_delta = spread_delta.dropna()

    if len(spread_lag) < 10:

        return np.nan

    beta = np.polyfit(
        spread_lag,
        spread_delta,
        1
    )[0]

    if beta == 0:

        return np.nan

    half_life = -np.log(2) / beta

    return round(half_life, 2)

# ==========================================
# SCORE
# ==========================================

def calcular_score(
    correlacao,
    pvalue,
    half_life,
    zscore_atual
):

    score = (

        (correlacao * 40)

        +

        ((1 - pvalue) * 35)

        +

        (abs(zscore_atual) * 15)

        -

        (half_life * 0.5)

    )

    return round(score, 2)

# ==========================================
# ANALISAR PAR
# ==========================================

def analisar_par(
    ativo1,
    ativo2,
    dados
):

    try:

        df = dados[[ativo1, ativo2]].dropna()

        if len(df) < 100:

            return None

        serie1 = df[ativo1]

        serie2 = df[ativo2]

<<<<<<< HEAD
        correlacao = serie1.corr(serie2)

=======
        # ==================================
        # CORRELAÇÃO
        # ==================================

        correlacao = serie1.corr(serie2)

        # ==================================
        # FILTRO PERFORMANCE
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        if correlacao < 0.70:

            return None

<<<<<<< HEAD
=======
        # ==================================
        # COINTEGRAÇÃO
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        resultado_coint = coint(
            serie1,
            serie2
        )

        pvalue = resultado_coint[1]

<<<<<<< HEAD
=======
        # ==================================
        # HEDGE RATIO
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        modelo = OLS(
            serie1,
            add_constant(serie2)
        ).fit()

        hedge_ratio = modelo.params.iloc[1]

<<<<<<< HEAD
=======
        # ==================================
        # SPREAD
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        spread = (
            serie1
            -
            (hedge_ratio * serie2)
        )

        media = spread.mean()

        desvio = spread.std()

        if desvio == 0:

            return None

<<<<<<< HEAD
=======
        # ==================================
        # ZSCORE
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        zscore = (
            spread - media
        ) / desvio

        ultimo_z = zscore.iloc[-1]

<<<<<<< HEAD
=======
        # ==================================
        # HALF LIFE
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        half_life = calcular_half_life(
            spread
        )

        if pd.isna(half_life):

            return None

<<<<<<< HEAD
=======
        # ==================================
        # SCORE
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        score = calcular_score(
            correlacao,
            pvalue,
            half_life,
            ultimo_z
        )

<<<<<<< HEAD
=======
        # ==================================
        # SINAL
        # ==================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
        if ultimo_z > 2:

            sinal = "SHORT SPREAD"

        elif ultimo_z < -2:

            sinal = "LONG SPREAD"

        else:

            sinal = "NEUTRO"

        return {

            "ATIVO 1": ativo1,
            "ATIVO 2": ativo2,
            "CORRELAÇÃO": round(correlacao, 4),
            "P-VALUE": round(pvalue, 4),
            "HEDGE RATIO": round(hedge_ratio, 4),
            "HALF LIFE": round(half_life, 2),
            "ZSCORE": round(ultimo_z, 2),
            "SCORE": round(score, 2),
            "SINAL": sinal

        }

    except:

        return None

# ==========================================
# EXECUTAR SCANNER
# ==========================================

def executar_scanner(
    lista_ativos,
    periodo="200d",
    correlacao_minima=0.70,
    pvalue_maximo=0.05
):

    dados = baixar_dados(
        lista_ativos,
        periodo
    )

    resultados = []

    pares = []

    for i in range(len(lista_ativos)):

        for j in range(i + 1, len(lista_ativos)):

            pares.append(
                (
                    lista_ativos[i],
                    lista_ativos[j]
                )
            )

<<<<<<< HEAD
=======
    # ======================================
    # MULTI THREAD
    # ======================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
    with ThreadPoolExecutor(max_workers=4) as executor:

        futuros = [

            executor.submit(
                analisar_par,
                par[0],
                par[1],
                dados
            )

            for par in pares

        ]

        for futuro in futuros:

            resultado = futuro.result()

            if resultado is not None:

                if (

                    resultado["CORRELAÇÃO"]
                    >= correlacao_minima

                    and

                    resultado["P-VALUE"]
                    <= pvalue_maximo

                ):

                    resultados.append(
                        resultado
                    )

<<<<<<< HEAD
=======
    # ======================================
    # DATAFRAME FINAL
    # ======================================

>>>>>>> cacc436634282f3814cff45df2c715a714d9f6f5
    if len(resultados) == 0:

        return pd.DataFrame()

    df = pd.DataFrame(resultados)

    df = df.sort_values(
        by="SCORE",
        ascending=False
    )

    df.reset_index(
        drop=True,
        inplace=True
    )

    return df
