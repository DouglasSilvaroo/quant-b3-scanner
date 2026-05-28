import pandas as pd
import yfinance as yf
import streamlit as st
import time
from logger import logger



# ==========================================
# DOWNLOAD MARKET DATA
# ==========================================

@st.cache_data(

    ttl=300,

    show_spinner=False

)

def baixar_dados_market(

    ativos,

    periodo="1y"

):

    try:

        # ==========================================
        # VALIDAÇÃO
        # ==========================================

        if not ativos:

            return pd.DataFrame()

        # ==========================================
        # REMOVER DUPLICADOS
        # ==========================================

        ativos = list(

            set(ativos)

        )

        logger.info(

            f"ATIVOS SOLICITADOS: {ativos}"

        )

        # ==========================================
        # DOWNLOAD LOTE
        # ==========================================

        dados = pd.DataFrame()

        for tentativa in range(3):

            try:

                time.sleep(2)

                dados = yf.download(

                    ativos,

                    period=periodo,

                    auto_adjust=True,

                    progress=False,

                    threads=True

            )

            if not dados.empty:

                break

        except Exception as erro:

            logger.error(

                f"TENTATIVA {tentativa + 1} FALHOU: {erro}"

            )

            time.sleep(5)
            
        # ==========================================
        # MULTIINDEX
        # ==========================================

        if isinstance(

            dados.columns,

            pd.MultiIndex

        ):

            dados = dados["Close"]

        
        # ==========================================
        # VALIDAÇÃO
        # ==========================================

        if dados.empty:

            logger.warning(

                "DATAFRAME VAZIO"

        )

        # ==========================================
        # CLOSE
        # ==========================================
        
        if len(ativos) == 1:

            fechamento = pd.DataFrame(

            dados.copy()

            )

            fechamento.columns = ativos

        else:

            fechamento = dados.copy()
        
        # ==========================================
        # LIMPEZA
        # ==========================================

        fechamento = fechamento.dropna(

            how="all"

        )

        fechamento.index = pd.to_datetime(

            fechamento.index

        )

        fechamento = fechamento.sort_index()

        # ==========================================
        # LOG
        # ==========================================

        logger.info(

            "COLUNAS FINAIS"

        )

        logger.info(

            fechamento.columns.tolist()

        )

        logger.info(

            fechamento.tail()

        )
        # ==========================================
        # PEQUENO DELAY
        # ==========================================

        
        return fechamento

    except Exception as erro:

        logger.error(

            f"ERRO MARKET DATA: {erro}"

        )
  
        return pd.DataFrame()
