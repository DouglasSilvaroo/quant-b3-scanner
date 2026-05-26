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

    if not api_key:

        return pd.DataFrame()

    interval = "1day"

    outputsize = 500

    df_final = pd.DataFrame()

    for ativo in ativos:

        try:

            ticker = ativo

            url = (

                f"https://api.twelvedata.com/time_series"

                f"?symbol={ticker}"

                f"&interval={interval}"

                f"&outputsize={outputsize}"

                f"&apikey={api_key}"

            )

            response = requests.get(

                url,

                timeout=15

            )

            data = response.json()

            if "values" not in data:

                continue

            df = pd.DataFrame(
                data["values"]
            )

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

            if df_final.empty:

                df_final = df

            else:

                df_final = df_final.join(

                    df,

                    how="outer"

                )

            time.sleep(1)

        except Exception:

            continue

    return df_final
