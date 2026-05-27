import pandas as pd
import requests
import os
import time


# ==========================================
# DOWNLOAD MARKET DATA
# ==========================================

def baixar_dados_market(

    ativos,

    periodo="1y"

):

    api_key = os.getenv(
        "ALPHAVANTAGE_API_KEY"
    )

    if not api_key:

        print("API KEY NÃO ENCONTRADA")

        return pd.DataFrame()

    print("API KEY CARREGADA")

    df_final = pd.DataFrame()

    ativos_falharam = []

    # ==========================================
    # LOOP ATIVOS
    # ==========================================

    for ativo in ativos:

        try:

            ticker = ativo.replace(
                ".SA",
                ""
            )

            print(f"BAIXANDO: {ticker}")

            # ==========================================
            # URL ALPHAVANTAGE
            # ==========================================

            url = (

                "https://www.alphavantage.co/query"

                f"?function=TIME_SERIES_DAILY_ADJUSTED"

                f"&symbol={ticker}.SAO"

                f"&outputsize=full"

                f"&apikey={api_key}"

            )

            response = requests.get(

                url,

                timeout=10

            )

            data = response.json()

            # ==========================================
            # VALIDAÇÃO
            # ==========================================

            if (

                "Time Series (Daily)" not in data

                or

                len(data["Time Series (Daily)"]) == 0

            ):

                print(f"SEM DADOS PARA {ticker}")

               ativos_falharam.append(
                   ticker
            )

            print(data)

            continue
            
            # ==========================================
            # DATAFRAME
            # ==========================================

            serie = data[
                "Time Series (Daily)"
            ]

            df = pd.DataFrame.from_dict(

                serie,

                orient="index"

            )

            df.index = pd.to_datetime(
                df.index
            )

            df = df.sort_index()

            df[ativo] = df[
                "5. adjusted close"
            ].astype(float)

            df = df[[ativo]]

            # ==========================================
            # JOIN
            # ==========================================

            if df_final.empty:

                df_final = df

            else:

                df_final = df_final.join(

                    df,

                    how="outer"

                )

            # ==========================================
            # RATE LIMIT
            # ==========================================

            time.sleep(12)

        except Exception as erro:

            print("ERRO:")
            print(erro)

            continue

    # ==========================================
    # FINAL
    # ==========================================

    print("DATAFRAME FINAL:")
    print(df_final.head())

    print("ATIVOS COM FALHA:")
    print(ativos_falharam)

    return df_final
