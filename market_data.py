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
        "TWELVEDATA_API_KEY"
    )

    # ==========================================
    # VALIDAÇÃO API
    # ==========================================

    if not api_key:

        print("API KEY NÃO ENCONTRADA")

        return pd.DataFrame()

    print("API KEY OK")

    # ==========================================
    # CONFIG
    # ==========================================

    interval = "1day"

    outputsize = 500

    df_final = pd.DataFrame()

    ativos_falharam = []

    # ==========================================
    # LOOP PRINCIPAL
    # ==========================================

    for ativo in ativos:

        try:

            ticker = ativo.replace(
                ".SA",
                ""
            )

            print(f"BAIXANDO: {ticker}")

            # ==========================================
            # URL API
            # ==========================================

            url = (

                "https://api.twelvedata.com/time_series"

                f"?symbol={ticker}"

                f"&interval={interval}"

                f"&outputsize={outputsize}"

                f"&apikey={api_key}"

            )

            # ==========================================
            # REQUEST
            # ==========================================

            response = requests.get(

                url,

                timeout=10

            )

            data = response.json()

            # ==========================================
            # RATE LIMIT
            # ==========================================

            if "code" in data:

                print(f"ERRO API: {ticker}")

                print(data)

                ativos_falharam.append(
                    ticker
                )

                continue

            # ==========================================
            # VALIDAÇÃO
            # ==========================================

            if "values" not in data:

                print(f"SEM DADOS: {ticker}")

                ativos_falharam.append(
                    ticker
                )

                continue

            # ==========================================
            # DATAFRAME
            # ==========================================

            df = pd.DataFrame(

                data["values"]

            )

            if df.empty:

                ativos_falharam.append(
                    ticker
                )

                continue

            # ==========================================
            # DATETIME
            # ==========================================

            df["datetime"] = pd.to_datetime(

                df["datetime"]

            )

            df = df.sort_values(

                "datetime"

            )

            df = df.set_index(

                "datetime"

            )

            # ==========================================
            # PREÇO
            # ==========================================

            df[ativo] = df["close"].astype(

                float

            )

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
            # RATE LIMIT CONTROL
            # ==========================================

            time.sleep(1.2)

        except Exception as erro:

            print(f"ERRO INTERNO: {ativo}")

            print(erro)

            ativos_falharam.append(
                ativo
            )

            continue

    # ==========================================
    # LIMPEZA FINAL
    # ==========================================

    if not df_final.empty:

        df_final = df_final.sort_index()

    # ==========================================
    # LOG FINAL
    # ==========================================

    print("ATIVOS COM FALHA:")

    print(ativos_falharam)

    print("COLUNAS FINAIS:")

    print(df_final.columns.tolist())

    # ==========================================
    # RETURN
    # ==========================================

    return df_final
