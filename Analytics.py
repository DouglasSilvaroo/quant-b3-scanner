import pandas as pd
import statsmodels.api as sm
import numpy as np


# ==========================================
# SPREAD
# ==========================================

def calcular_spread(

    serie1,
    serie2,
    fator1,
    fator2

):

    spread = (

        (serie1 * fator1)

        -

        (serie2 * fator2)

    )

    return spread


# ==========================================
# ESTATÍSTICAS
# ==========================================

def calcular_estatisticas(

    spread

):

    media = float(

        spread.mean()

    )

    desvio = float(

        spread.std()

    )

    spread_atual = float(

        spread.iloc[-1]

    )

    if desvio == 0:

        zscore = 0

    else:

        zscore = (

            spread_atual - media

        ) / desvio

    return {

        "media": media,

        "desvio": desvio,

        "spread_atual": spread_atual,

        "zscore": zscore

    }


# ==========================================
# CORRELAÇÃO
# ==========================================

def calcular_correlacao(

    serie1,
    serie2

):

    correlacao = float(

        serie1.corr(

            serie2

        )

    )

    return correlacao

# ==========================================
# HEDGE RATIO
# ==========================================

def calcular_hedge_ratio(

    serie1,
    serie2

):

    x = sm.add_constant(

        serie2

    )

    modelo = sm.OLS(

        serie1,
        x

    ).fit()

    hedge_ratio = float(

        modelo.params.iloc[1]

    )

    return hedge_ratio

# ==========================================
# HALF LIFE
# ==========================================

def calcular_half_life(

    spread

):

    spread_lag = spread.shift(1)

    spread_ret = spread - spread_lag

    spread_lag = spread_lag.dropna()

    spread_ret = spread_ret.dropna()

    spread_lag = sm.add_constant(

        spread_lag

    )

    modelo = sm.OLS(

        spread_ret,
        spread_lag

    ).fit()

    beta = modelo.params.iloc[1]

    if beta == 0:

        return 0

    half_life = -np.log(2) / beta

    return round(

        float(half_life),
        2

    )
