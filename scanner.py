
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
    # DOWNLOAD ÚNICO
    # ==========================================

    try:

        dados = yf.download(

            lista_ativos,

            period=periodo,

            auto_adjust=True,

            progress=False

        )

    except:

        return pd.DataFrame()

    # ==========================================
    # MULTIINDEX
    # ==========================================

    if isinstance(
        dados.columns,
        pd.MultiIndex
    ):

        dados = dados["Close"]

    # ==========================================
    # REMOVE COLUNAS VAZIAS
    # ==========================================

    dados = dados.dropna(
        axis=1,
        how="all"
    )

    # ==========================================
    # LOOP PARES
    # ==========================================

    ativos_validos = list(dados.columns)

    for i in range(len(ativos_validos)):

        for j in range(i + 1, len(ativos_validos)):

            ativo1 = ativos_validos[i]
            ativo2 = ativos_validos[j]

            try:

                # ==================================
                # SÉRIES
                # ==================================

                serie1 = dados[ativo1]
                serie2 = dados[ativo2]

                df_temp = pd.concat(

                    [serie1, serie2],

                    axis=1

                ).dropna()

                # ==================================
                # VALIDAÇÃO
                # ==================================

                if len(df_temp) < 80:

                    continue

                serie1 = df_temp.iloc[:, 0]
                serie2 = df_temp.iloc[:, 1]

                # ==================================
                # CORRELAÇÃO
                # ==================================

                correlacao = serie1.corr(
                    serie2
                )

                if correlacao < 0.90:

                    continue

                # ==================================
                # COINTEGRAÇÃO
                # ==================================

                _, pvalue, _ = coint(

                    serie1,
                    serie2

                )

                if pvalue > 0.05:

                    continue

                # ==================================
                # SPREAD
                # ==================================

                spread = serie1 - serie2

                media = spread.mean()

                desvio = spread.std()

                if desvio == 0:

                    continue

                # ==================================
                # ZSCORE
                # ==================================

                zscore = (

                    spread.iloc[-1]
                    -
                    media

                ) / desvio

                # ==================================
                # STATUS
                # ==================================

                if zscore >= 2:

                    status = "🟢 Entrar Crédito"

                elif zscore <= -2:

                    status = "🔴 Entrar Débito"

                else:

                    status = "🟡 Neutro"

                # ==================================
                # SCORE
                # ==================================

                score = 0

                if correlacao >= 0.99:

                    score += 40

                elif correlacao >= 0.97:

                    score += 30

                elif correlacao >= 0.95:

                    score += 20

                if pvalue <= 0.01:

                    score += 40

                elif pvalue <= 0.03:

                    score += 30

                elif pvalue <= 0.05:

                    score += 20

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
    # DATAFRAME FINAL
    # ==========================================

    df = pd.DataFrame(resultados)

    if not df.empty:

        df = df.sort_values(

            by=[

                "Score Quant",
                "Correlação"

            ],

            ascending=False

        )

    return df
