
import time
import pandas as pd
import yfinance as yf

from supabase import create_client

from config import (
    SEGMENTOS,
    MARKET_HISTORY_PERIOD,
    MARKET_MAX_RETRIES,
    MARKET_RETRY_SLEEP,
    MARKET_DOWNLOAD_SLEEP,
    MARKET_TABLE
)

from logger import logger

from dotenv import load_dotenv

import os


# ==========================================
# LOAD ENV
# ==========================================

load_dotenv()


# ==========================================
# SUPABASE
# ==========================================

SUPABASE_URL = os.getenv(

    "SUPABASE_URL"

)

SUPABASE_KEY = os.getenv(

    "SUPABASE_KEY"

)

supabase = create_client(

    SUPABASE_URL,
    SUPABASE_KEY

)


# ==========================================
# LISTA ATIVOS
# ==========================================

ativos = []

for segmento in SEGMENTOS.values():

    ativos.extend(segmento)

ativos = list(set(ativos))

ativos = ativos[:5]


# ==========================================
# DOWNLOAD + INSERT
# ==========================================

for ativo in ativos:

    logger.info(

        f"BAIXANDO HISTÓRICO: {ativo}"

    )

    dados = pd.DataFrame()

    for tentativa in range(

        MARKET_MAX_RETRIES

    ):

        try:

            time.sleep(

                MARKET_DOWNLOAD_SLEEP

            )

            dados = yf.download(

                ativo,

                period=MARKET_HISTORY_PERIOD,

                auto_adjust=True,

                progress=False,

                threads=False

            )

            if not dados.empty:

                break

        except Exception as erro:

            logger.error(

                f"{ativo} | "
                f"TENTATIVA "
                f"{tentativa + 1} | "
                f"{erro}"

            )

            time.sleep(

                MARKET_RETRY_SLEEP

            )
            
        dados = dados.dropna()

        if dados.empty:

            logger.warning(f"{ticker} sem histórico válido")
            continue

        if len(dados) < 100:

            logger.warning(f"{ticker} histórico insuficiente")
            continue

    # ==========================================
    # VALIDAÇÃO
    # ==========================================

    if dados.empty:

        logger.error(

            f"SEM DADOS: {ativo}"

        )

        continue

    # ==========================================
    # RESET INDEX
    # ==========================================

    dados = dados.reset_index()

    # ==========================================
    # PREPARAÇÃO DOS DADOS
    # ==========================================

    dados = dados.dropna()

    if dados.empty:

        logger.warning(

            f"{ativo} sem histórico válido"

        )

        return

    dados = dados.reset_index
