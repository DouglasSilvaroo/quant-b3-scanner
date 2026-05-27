import pandas as pd
import requests
import os
import time


def baixar_dados_finnhub(

    ativos,

    periodo="1y"

):

    api_key = os.getenv(
        "TWELVEDATA_API_KEY"
    )

    print("API KEY:", api_key)

    if not api_key:

        print("API KEY NÃO ENCONTRADA")

        return pd.DataFrame()

    interval = "1day"

    outputsize = 500

    df_final = pd.DataFrame()

    for ativo in ativos:

        try:

            ticker = ativo.replace(
                ".SA",
                ""
            )
                                   
            print(f"BAIXANDO: {ticker}")

            url = (

                f"https://api.twelvedata.com/time_series"

                f"?symbol={ticker}"

                f"&interval={interval}"

                f"&outputsize={outputsize}"

                f"&apikey={api_key}"

            )

            print("URL:", url)

            response = requests.get(

                url,

                timeout=15

            )

            print("STATUS CODE:", response.status_code)

            data = response.json()

            print("RESPOSTA API:")
            print("RESPOSTA API:", str(data)[:1000])
                    
            # ======================================
            # VALIDAÇÃO
            # ======================================

            if "values" not in data:

                print(f"SEM DADOS PARA {ticker}")

                continue

            # ======================================
            # DATAFRAME
            # ======================================

            df = pd.DataFrame(

                data["values"]

            )

            print(df.head())

            df["datetime"] = pd.to_datetime(

                df["datetime"]

            )

            df = df.sort_values(

                "datetime"

            )

            df = df.set_index(

                "datetime"

            )

            df[ativo] = df["close"].astype(

                float

            )

            df = df[[ativo]]

            # ======================================
            # JOIN
            # ======================================

            if df_final.empty:

                df_final = df

            else:

                df_final = df_final.join(

                    df,

                    how="outer"

                )

            time.sleep(1)

        except Exception as erro:

            print("ERRO:")
            print(erro)

            continue

    print("DATAFRAME FINAL:")
    print(df_final.head())

    return df_final
