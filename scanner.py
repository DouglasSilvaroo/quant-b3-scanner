
import yfinance as yf
import pandas as pd
import numpy as np

from statsmodels.tsa.stattools import coint

# ==========================================
# SCANNER QUANTITATIVO
# ==========================================

def executar_scanner(

    segmentos,
    lista_ativos,

    periodo="200d",

    modo="Mesmo Setor",

    correlacao_min=0.95,

    pvalue_max=0.05,

    zscore_min=1.5

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

            progress=False,

            threads=True

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
    # ATIVOS VÁLIDOS
    # ==========================================

    ativos_validos = list(dados.columns)

    # ==========================================
    # DEFINIÇÃO DOS PARES
    # ==========================================

    pares = []

    # ==========================================
    # MESMO SETOR
    # ==========================================

    if modo == "Mesmo Setor":

        for setor, ativos in segmentos.items():

            ativos_filtrados = [

                ativo
                for ativo in ativos

                if ativo in ativos_validos

            ]

            for i in range(len(ativos_filtrados)):

                for j in range(i + 1, len(ativos_filtrados)):

                    ativo1 = ativos_filtrados[i]
                    ativo2 = ativos_filtrados[j]

                    pares.append(

                        (ativo1, ativo2)

                    )

    # ==========================================
    # TODOS OS SETORES
    # ==========================================

    else:

        for i in range(len(ativos_validos)):

            for j in range(i + 1, len(ativos_validos)):

                ativo1 = ativos_validos[i]
                ativo2 = ativos_validos[j]

                pares.append(

                    (ativo1, ativo2)

                )

    # ==========================================
    # LOOP PRINCIPAL
    # ==========================================

    for ativo1, ativo2 in pares:

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

            if pd.isna(correlacao):

                continue

            if correlacao < correlacao_min:

                continue

            # ==================================
            # COINTEGRAÇÃO
            # ==================================

            _, pvalue, _ = coint(

                serie1,
                serie2

            )

            if pd.isna(pvalue):

                continue

            if pvalue > pvalue_max:

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
            # Z-SCORE
            # ==================================

            zscore = (

                spread.iloc[-1]
                -
                media

            ) / desvio

            if pd.isna(zscore):

                continue

            # ==================================
            # FILTRO ZSCORE
            # ==================================

            if abs(zscore) < zscore_min:

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

            # Cointegração

            if pvalue <= 0.01:

                score += 40

            elif pvalue <= 0.03:

                score += 30

            elif pvalue <= 0.05:

                score += 20

            # Zscore

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

    # ==========================================
    # LIMPEZA FINAL
    # ==========================================

    if not df.empty:

        df = df.replace(

            [np.inf, -np.inf],
            np.nan

        )

        df = df.dropna()

        # ======================================
        # ORDENAÇÃO
        # ======================================

        df = df.sort_values(

            by=[

                "Score Quant",
                "Correlação"

            ],

            ascending=False

        )

        df = df.reset_index(

            drop=True

        )

    return df
