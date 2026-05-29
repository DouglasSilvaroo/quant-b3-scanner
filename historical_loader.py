import os
import time
import pandas as pd
import yfinance as yf

from supabase import create_client
from dotenv import load_dotenv

from config import (
    SEGMENTOS,
    MARKET_HISTORY_PERIOD,
    MARKET_MAX_RETRIES,
    MARKET_RETRY_SLEEP,
    MARKET_DOWNLOAD_SLEEP,
    MARKET_TABLE
)

from logger import logger


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

logger.info(
    f"KEY PREFIX: {SUPABASE_KEY[:30]}"
)

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# ==========================================
# LISTA DE ATIVOS
# ==========================================

def obter_ativos():

    ativos = []

    for segmento in SEGMENTOS.values():

        ativos.extend(segmento)

    return sorted(
        list(set(ativos))
    )


# ==========================================
# FUNÇÃO PRINCIPAL
# ==========================================

def carregar_historico():

    ativos = obter_ativos()

    logger.info(
        f"TOTAL DE ATIVOS: {len(ativos)}"
    )

    ativos_processados = 0

    for ativo in ativos:

        logger.info(
            f"BAIXANDO HISTÓRICO: {ativo}"
        )

        dados = pd.DataFrame()

        # ==================================
        # DOWNLOAD
        # ==================================

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
                    f"TENTATIVA {tentativa + 1} | "
                    f"{erro}"
                )

                time.sleep(
                    MARKET_RETRY_SLEEP
                )

        # ==================================
        # VALIDAÇÕES
        # ==================================

        if dados.empty:

            logger.warning(
                f"{ativo} sem histórico"
            )

            continue

        dados = dados.dropna()

        if dados.empty:

            logger.warning(
                f"{ativo} sem histórico válido"
            )

            continue

        if len(dados) < 30:

            logger.warning(
                f"{ativo} histórico insuficiente"
            )

            continue

        # ==================================
        # RESET INDEX
        # ==================================

        dados = dados.reset_index()

        if isinstance(
            dados.columns,
            pd.MultiIndex
        ):

            dados.columns = [
                col[0]
                for col in dados.columns
            ]

        logger.info(
            f"{ativo} | "
            f"{len(dados)} registros"
        )

        # ==================================
        # PREPARA LOTE
        # ==================================

        registros = []

        for _, row in dados.iterrows():

            try:

                registros.append({

                    "ticker": ativo,

                    "date": pd.to_datetime(
                        row["Date"]
                    ).date().isoformat(),

                    "open": float(
                        row["Open"]
                    ),

                    "high": float(
                        row["High"]
                    ),

                    "low": float(
                        row["Low"]
                    ),

                    "close": float(
                        row["Close"]
                    ),

                    "volume": float(
                        row["Volume"]
                    )

                })

            except Exception as erro:

                logger.error(
                    f"ERRO PREPARANDO "
                    f"REGISTRO {ativo}: "
                    f"{erro}"
                )

        # ==================================
        # UPSERT EM LOTE
        # ==================================

        try:

            if registros:

                supabase.table(
                    MARKET_TABLE
                ).upsert(
                    registros,
                    on_conflict="ticker,date"
                ).execute()

        except Exception as erro:

            logger.exception(
                f"ERRO UPSERT LOTE "
                f"{ativo}"
            )

            continue

        ativos_processados += 1

        logger.info(
            f"HISTÓRICO SALVO: {ativo}"
        )

    logger.info(
        f"CARGA FINALIZADA | "
        f"ATIVOS PROCESSADOS: "
        f"{ativos_processados}"
    )
