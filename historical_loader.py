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
    # RETRY DOWNLOAD
    # ==================================

    for tentativa in range(
        MARKET_MAX_RETRIES
    ):

        try:

            time

