import pandas as pd
import statsmodels.api as sm


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
