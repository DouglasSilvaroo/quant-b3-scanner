import pandas as pd
import requests
import os
import time


def baixar_dados_finnhub(

    ativos,

    periodo="1y"

):

    api_key = os.getenv(
        "FINNHUB_API_KEY"
    )

    if not api_key:

        return pd.DataFrame()

    dias = {

        "3mo": 90,
        "6mo": 180,
        "1y": 365,
        "2y": 730,
        "3y": 1095,
        "90d": 90,
        "120d": 120,
        "180d": 180,
        "200d": 200,
        "250d": 250

    }

    dias_periodo = dias.get(
        periodo,
        365
    )

    fim = int(time.time())

    inicio = fim - (
        dias_periodo * 24 * 60 * 60
    )

    df_final = pd.DataFrame()

    for ativo in ativos:

        try:

            ticker = ativo.replace(
                ".SA",
                ""
            )

            ticker = f"BVMF:{ticker}"

            url = (

                f"https://finnhub.io/api/v1/stock/candle"

                f"?symbol={ticker}"

                f"&resolution=D"

                f"&from={inicio}"

                f"&to={fim}"

                f"&token={api_key}"

            )

            response = requests.get(

                url,

                timeout=15

            )

            data = response.json()

            if data.get("s") != "ok":

                continue

            df = pd.DataFrame({

                ativo: data["c"]

            })

            df.index = pd.to_datetime(

                data["t"],

                unit="s"

            )

            if df_final.empty:

                df_final = df

            else:

                df_final = df_final.join(

                    df,

                    how="outer"

                )

            time.sleep(0.5)

        except Exception:

            continue

    return df_final
