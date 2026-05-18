
import yfinance as yf
import pandas as pd

from statsmodels.tsa.stattools import coint

# ==========================================
# SCANNER QUANTITATIVO
# ==========================================

def executar_scanner(

    lista_ativos,
    periodo="200d",
    correlacao_minima=0.70,
    pvalue_maximo=0.05

):

    resultados = []

    dados = yf.download(

        lista_ativos,

        period=periodo,

        auto_adjust=True,

        progress=False

    )

    # ======================================
    # AJUSTE MULTIINDEX
    # ======================================

    if isinstance(dados.columns, pd.MultiIndex):

        if "Close" in dados.columns.get_level_values(0):

            dados = dados["Close"]

        elif "Adj Close" in dados.columns.get_level_values(0):

            dados = dados["Adj Close"]

    dados = dados.dropna(axis=1)

    ativos = list(dados.columns)

    # ======================================
    # LOOP PARES
    # ======================================

    for i in range(len(ativos)):

        for j in range(i + 1, len(ativos)):

            try:

                ativo1 = ativos[i]
                ativo2 = ativos[j]

                serie1 = dados[ativo1]
                serie2 = dados[ativo2]

                correlacao = serie1.corr(serie2)

                if correlacao < correlacao_minima:
                    continue

                resultado = coint(
                    serie1,
                    serie2
                )

                pvalue = resultado[1]

                if pvalue > pvalue_maximo:
                    continue

                resultados.append({

                    "Ativo 1": ativo1,
                    "Ativo 2": ativo2,
                    "Correlação": round(correlacao, 4),
                    "P-Value": round(pvalue, 4)

                })

            except:
                pass

    # ======================================
    # DATAFRAME FINAL
    # ======================================

    df = pd.DataFrame(resultados)

    if not df.empty:

        df = df.sort_values(
            by="Correlação",
            ascending=False
        )

    return df
