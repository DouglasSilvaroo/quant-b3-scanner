
import yfinance as yf
import pandas as pd

from statsmodels.tsa.stattools import coint

# ==========================================
# SCANNER QUANTITATIVO
# ==========================================

def executar_scanner(

    lista_ativos,
    periodo="200d"

):

    resultados = []

    # ==========================================
    # LOOP PRINCIPAL
    # ==========================================

    for i in range(len(lista_ativos)):

        for j in range(i + 1, len(lista_ativos)):

            ativo1 = lista_ativos[i]
            ativo2 = lista_ativos[j]

            try:

                # ==================================
                # DOWNLOAD
                # ==================================

                dados = yf.download(

                    [ativo1, ativo2],

                    period=periodo,

                    auto_adjust=True,

                    progress=False

                )

                # ==================================
                # VALIDAÇÃO DOWNLOAD
                # ==================================

                if dados.empty:

                    continue

                # ==================================
                # MULTIINDEX
                # ==================================

                if isinstance(
                    dados.columns,
                    pd.MultiIndex
                ):

                    dados = dados["Close"]

                dados = dados.dropna()

                if len(dados) < 50:

                    continue

                # ==================================
                # VALIDAÇÃO
                # ==================================

                if len(dados) < 50:

                    continue

                # ==================================
                # SÉRIES
                # ==================================

                serie1 = dados[ativo1]
                serie2 = dados[ativo2]

                # ==================================
                # CORRELAÇÃO
                # ==================================

                correlacao = serie1.corr(
                    serie2
                )

                # ==================================
                # COINTEGRAÇÃO
                # ==================================

                _, pvalue, _ = coint(

                    serie1,
                    serie2

                )

                # ==================================
                # SPREAD
                # ==================================

                spread = serie1 - serie2

                media = spread.mean()

                desvio = spread.std()

                # ==================================
                # Z-SCORE
                # ==================================

                zscore = (

                    spread.iloc[-1]
                    -
                    media

                ) / desvio

                # ==================================
                # FILTROS
                # ==================================

                if correlacao < 0.90:

                    continue

                if pvalue > 0.05:

                    continue

                # ==================================
                # STATUS OPERACIONAL
                # ==================================

                if zscore >= 2:

                    status = "🟢 Entrar Crédito"

                elif zscore <= -2:

                    status = "🔴 Entrar Débito"

                else:

                    status = "🟡 Neutro"

                # ==================================
                # SCORE QUANT
                # ==================================

                score = 0

                # Correlação

                if correlacao >= 0.99:

                    score += 40

                elif correlacao >= 0.97:

                    score += 30

                elif correlacao >= 0.95:

                    score += 20

                # P-Value

                if pvalue <= 0.01:

                    score += 40

                elif pvalue <= 0.03:

                    score += 30

                elif pvalue <= 0.05:

                    score += 20

                # Z-Score

                if abs(zscore) >= 3:

                    score += 20

                elif abs(zscore) >= 2:

                    score += 10

                # ==================================
                # RESULTADO
                # ==================================

                resultados.append({

                    "Ativo 1": ativo1,
                    "Ativo 2": ativo2,

                    "Correlação": round(
                        correlacao,
                        4
                    ),

                    "P-Value": round(
                        pvalue,
                        4
                    ),

                    "Pontuação Z": round(
                        zscore,
                        2
                    ),

                    "Status": status,

                    "Score Quant": score

                })

            except:

                continue

    # ==========================================
    # DATAFRAME
    # ==========================================

    df = pd.DataFrame(resultados)

    # ==========================================
    # ORDENAÇÃO
    # ==========================================

    if not df.empty:

        df = df.sort_values(

            by=[

                "Score Quant",
                "Correlação"

            ],

            ascending=False

        )

    return df
