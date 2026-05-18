
# ==========================================
# BACKTEST ENGINE INSTITUCIONAL
# ==========================================

import pandas as pd
import numpy as np

# ==========================================
# BACKTEST
# ==========================================

def executar_backtest(
    spread,
    zscore,
    entry=2,
    exit=0.5,
    stop=3.5
):

    operacoes = []

    posicao = 0

    entrada_spread = 0

    entrada_data = None

    equity = []

    capital = 10000

    # ======================================
    # LOOP
    # ======================================

    for i in range(len(zscore)):

        z = zscore.iloc[i]

        spread_atual = spread.iloc[i]

        data = spread.index[i]

        # ==================================
        # ENTRADA SHORT
        # ==================================

        if posicao == 0 and z > entry:

            posicao = -1

            entrada_spread = spread_atual

            entrada_data = data

        # ==================================
        # ENTRADA LONG
        # ==================================

        elif posicao == 0 and z < -entry:

            posicao = 1

            entrada_spread = spread_atual

            entrada_data = data

        # ==================================
        # SAÍDA LONG
        # ==================================

        elif posicao == 1:

            retorno = spread_atual - entrada_spread

            if z >= -exit or z <= -stop:

                pnl = retorno * 100

                capital += pnl

                operacoes.append({

                    "Tipo": "LONG",
                    "Entrada": entrada_data,
                    "Saida": data,
                    "PnL": round(pnl, 2),
                    "Capital": round(capital, 2)

                })

                posicao = 0

        # ==================================
        # SAÍDA SHORT
        # ==================================

        elif posicao == -1:

            retorno = entrada_spread - spread_atual

            if z <= exit or z >= stop:

                pnl = retorno * 100

                capital += pnl

                operacoes.append({

                    "Tipo": "SHORT",
                    "Entrada": entrada_data,
                    "Saida": data,
                    "PnL": round(pnl, 2),
                    "Capital": round(capital, 2)

                })

                posicao = 0

        equity.append(capital)

    # ======================================
    # DATAFRAME
    # ======================================

    trades = pd.DataFrame(operacoes)

    equity_curve = pd.DataFrame({

        "Data": spread.index,

        "Capital": equity

    })

    return trades, equity_curve
