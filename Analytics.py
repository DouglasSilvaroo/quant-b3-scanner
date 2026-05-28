import pandas as pd
import statsmodels.api as sm
import numpy as np
from statsmodels.tsa.stattools import coint


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

# ==========================================
# COINTEGRAÇÃO ROLLING
# ==========================================

def calcular_cointegracao_rolling(

    serie1,
    serie2,
    janela=60

):

    datas = []

    pvalues = []

    for i in range(

        janela,
        len(serie1)

    ):

        s1 = serie1.iloc[

            i - janela:i

        ]

        s2 = serie2.iloc[

            i - janela:i

        ]

        try:

            resultado = coint(

                s1,
                s2

            )

            pvalor = resultado[1]

        except:

            pvalor = 1

        datas.append(

            serie1.index[i]

        )

        pvalues.append(

            pvalor

        )

    df = pd.DataFrame({

        "Data": datas,

        "PValor": pvalues

    })

    df = df.set_index(

        "Data"

    )

    return df

# ==========================================
# REGIME ESTATÍSTICO
# ==========================================

def calcular_regime_estatistico(

    spread,
    zscore,
    half_life,
    df_coint

):

    volatilidade = float(

        spread.std()

    )

    ultimo_pvalor = float(

        df_coint["PValor"].iloc[-1]

    )

    score = 0

    # ==========================================
    # ZSCORE
    # ==========================================

    if abs(zscore) < 1.5:

        score += 1

    # ==========================================
    # HALF LIFE
    # ==========================================

    if half_life < 30:

        score += 1

    # ==========================================
    # COINTEGRAÇÃO
    # ==========================================

    if ultimo_pvalor <= 0.05:

        score += 1

    # ==========================================
    # VOLATILIDADE
    # ==========================================

    if volatilidade > 0:

        score += 1

    # ==========================================
    # CLASSIFICAÇÃO
    # ==========================================

    if score >= 4:

        regime = "🟢 REGIME ESTÁVEL"

    elif score >= 2:

        regime = "🟡 REGIME MODERADO"

    else:

        regime = "🔴 REGIME INSTÁVEL"

    return {

        "regime": regime,

        "score": score,

        "volatilidade": volatilidade,

        "pvalor": ultimo_pvalor

    }

# ==========================================
# SCORE QUANTITATIVO
# ==========================================

def calcular_score_quant(

    zscore,
    correlacao,
    half_life,
    pvalor,
    volatilidade,
    confianca

):

    score = 0

    # ==========================================
    # ZSCORE
    # ==========================================

    if abs(zscore) >= 2:

        score += 25

    elif abs(zscore) >= 1:

        score += 15

    # ==========================================
    # CORRELAÇÃO
    # ==========================================

    if correlacao >= 0.90:

        score += 25

    elif correlacao >= 0.80:

        score += 15

    # ==========================================
    # HALF LIFE
    # ==========================================

    if half_life <= 15:

        score += 20

    elif half_life <= 30:

        score += 10

    # ==========================================
    # COINTEGRAÇÃO
    # ==========================================

    if pvalor <= 0.01:

        score += 20

    elif pvalor <= 0.05:

        score += 10

    # ==========================================
    # CONFIANÇA
    # ==========================================

    score += confianca * 2

    # ==========================================
    # VOLATILIDADE
    # ==========================================

    if volatilidade > 0:

        score += 2

    return min(

        int(score),
        100

    )

