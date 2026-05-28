
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import time

from auth import (
    tela_login,
    tela_cadastro
)

from scanner import (
    executar_scanner
)

from market_data import (
    baixar_dados_market
)

from visuals import (

    render_histograma,
    render_heatmap
    render_permanencia
    render_zscore
    render_status_operacional
    render_dashboard_executivo
    render_cointegracao_rolling
  
)

from analytics import (

    calcular_spread,
    calcular_estatisticas,
    calcular_correlacao,
    calcular_hedge_ratio,
    calcular_half_life
    calcular_cointegracao_rolling

)

# ==========================================

# CONFIG STREAMLIT

# ==========================================

st.set_page_config(


page_title="PAINEL SPREADS",
page_icon="📈",
layout="wide",

)

# ==========================================

# SESSION

# ==========================================

if "logado" not in st.session_state:

    st.session_state["logado"] = False


if "usuario" not in st.session_state:

    st.session_state["usuario"] = ""


if "menu" not in st.session_state:

    st.session_state["menu"] = "Painel"


if "painel_pronto" not in st.session_state:

    st.session_state["painel_pronto"] = False
    
# ==========================================

# LOGIN

# ==========================================

if not st.session_state["logado"]:

    st.title("🏦 PAINEL SPREADS")

    aba1, aba2 = st.tabs([

    "Login",
    "Cadastro"

    ])

    with aba1:

        tela_login()

    with aba2:

        tela_cadastro()

    st.stop()

# ==========================================

# ATIVOS B3 POR SEGMENTO

# ==========================================

SEGMENTOS = {

"Bancos": [

    "ITUB3.SA",
    "ITUB4.SA",
    "BBDC3.SA",
    "BBDC4.SA",
    "BBAS3.SA",
    "SANB3.SA",
    "SANB4.SA",
    "SANB11.SA",
    "BPAC11.SA",
    "ABCB4.SA",
    "BRSR3.SA",
    "BRSR6.SA",
    "BMGB4.SA"

],

"Petroleo": [

    "PETR3.SA",
    "PETR4.SA",
    "PRIO3.SA",
    "RECV3.SA",
    "BRAV3.SA",
    "CSAN3.SA",
    "VBBR3.SA",
    "UGPA3.SA"

],

"Mineracao": [

    "VALE3.SA",
    "BRAP3.SA",
    "BRAP4.SA",
    "CSNA3.SA",
    "GGBR3.SA",
    "GGBR4.SA",
    "GOAU3.SA",
    "GOAU4.SA",
    "USIM3.SA",
    "USIM5.SA",
    "CMIN3.SA"

],

"Energia": [

    "AXIA3.SA",
    "AXIA6.SA",
    "CPFE3.SA",
    "CMIG3.SA",
    "CMIG4.SA",
    "TAEE3.SA",
    "TAEE4.SA",
    "TAEE11.SA",
    "EGIE3.SA",
    "ENGI11.SA",
    "EQTL3.SA",
    "ENEV3.SA",
    "CPLE3.SA",
    "NEOE3.SA",
    "ISAE3.SA",
    "ISAE4.SA",
    "AURE3.SA",
    "ALUP3.SA",
    "ALUP4.SA",
    "ALUP11.SA"

],

"Varejo": [

    "MGLU3.SA",
    "LREN3.SA",
    "BHIA3.SA",
    "ASAI3.SA",
    "PCAR3.SA",
    "RADL3.SA",
    "CEAB3.SA",
    "AUAU3.SA"

],

"Papel": [

    "SUZB3.SA",
    "KLBN3.SA",
    "KLBN4.SA",
    "KLBN11.SA",
    "RANI3.SA"

],

"Construcao": [

    "CYRE3.SA",
    "EZTC3.SA",
    "MRVE3.SA",
    "DIRR3.SA",
    "TEND3.SA",
    "LAVV3.SA"

],

"Telecom": [

    "VIVT3.SA",
    "TIMS3.SA",
    "POSI3.SA",
    "TOTS3.SA"

],

"Logistica": [

    "RAIL3.SA",
    "MOTV3.SA",
    "ECOR3.SA"

],

"Alimentos": [

    "ABEV3.SA",
    "MBRF3.SA",
    "SLCE3.SA"

],

"Saude": [

    "HAPV3.SA",
    "QUAL3.SA",
    "FLRY3.SA",
    "RDOR3.SA"

]

}

# ==========================================

# LISTA CONSOLIDADA

# ==========================================

LISTA_ATIVOS = []

for setor in SEGMENTOS.values():

    LISTA_ATIVOS.extend(setor)

LISTA_ATIVOS = sorted(list(set(LISTA_ATIVOS)))

# ==========================================

# SIDEBAR

# ==========================================

with st.sidebar:

    st.title("🏦 PAINEL SPREAD")

    st.success(
        f"👤 {st.session_state['usuario']}"
    )

    st.markdown("---")

    menu = st.radio(

        "Navegação",

        [
            "Painel",
            "Scanner"
        ],

        index=0 if st.session_state["menu"] == "Painel" else 1

    )

    st.session_state["menu"] = menu

    if menu == "Scanner":

        st.session_state["painel_pronto"] = False

    st.markdown("---")

    st.subheader("⚙️ Configurações")

    ativo1_sidebar = st.selectbox(

        "Ativo 1",

        ["Selecione"] + LISTA_ATIVOS,

        key="ativo1_select"

    )

    # ==========================================
    # REMOVE ATIVO JÁ SELECIONADO
    # ==========================================

    LISTA_ATIVOS_2 = [

        ativo for ativo in LISTA_ATIVOS

        if ativo != ativo1_sidebar

    ]

    LISTA_ATIVOS_2 = ["Selecione"] + LISTA_ATIVOS_2

    # ==========================================
    # ATIVO 2
    # ==========================================

    ativo2_sidebar = st.selectbox(

        "Ativo 2",

        LISTA_ATIVOS_2,

        key="ativo2_select"

    )

    periodo_sidebar = st.selectbox(

        "Período",

        [
            "3mo",
            "6mo",
            "1y",
            "2y",
            "3y"
        ],

        key="periodo_select"

    )

    if st.button("📊 Carregar Painel"):

        if (

            ativo1_sidebar != "Selecione"

            and

            ativo2_sidebar != "Selecione"

        ):

            st.session_state["painel_pronto"] = True

            st.session_state["menu"] = "Painel"

            st.rerun()

        else:

            st.warning(
                "Selecione os dois ativos."
            )

    st.markdown("---")

    st.subheader("⚖️ Proporção Operacional")

    lote1 = st.number_input(

        f"Lote {ativo1_sidebar}",

        min_value=100,

        step=100,

        value=100,

        key="lote1"

    )

    lote2 = st.number_input(

        f"Lote {ativo2_sidebar}",

        min_value=100,

        step=100,

        value=100,

        key="lote2"

    )

    st.markdown("---")

    st.subheader("📊 Camadas de Spread")

    camada = st.number_input(

        "Tamanho da Camada",

        value=0.50,

        step=0.10

    )

    tolerancia = st.number_input(

        "Tolerância",

        value=0.10,

        step=0.10

    )

    st.markdown("---")

    if st.button("Sair"):

        st.session_state["logado"] = False

        st.session_state["painel_pronto"] = False

        st.rerun()    
        
# ==========================================
# PAINEL
# ==========================================


def baixar_dados(

    ativos,

    periodo

):

    return baixar_dados_market(

        ativos,

        periodo

    )


if (

    st.session_state["menu"] == "Painel"

    and

    st.session_state["painel_pronto"]

):
    
    st.title("🏦 PAINEL SPREADS")

    ativo1 = ativo1_sidebar

    ativo2 = ativo2_sidebar

    periodo = periodo_sidebar

    if (

        ativo1 == "Selecione"

        or

        ativo2 == "Selecione"

    ):

        st.info(
            "Selecione os ativos e clique em 📊 Carregar Painel."
        )

        st.stop()

    try:

     
        agora = time.time()

        if "ultima_execucao" not in st.session_state:

            st.session_state["ultima_execucao"] = 0

        if agora - st.session_state["ultima_execucao"] < 1:

            st.stop()

        st.session_state["ultima_execucao"] = agora

        dados = baixar_dados(

            [ativo1, ativo2],

            periodo

        )

        if dados.empty:

            st.error(
                "Nenhum dado retornado pela API."
            )

            st.stop()

# ==========================================
# REMOVE NAN
# ==========================================

        dados = dados.dropna(

            subset=[

                ativo1,
                ativo2

            ]

        )
        if dados.empty:

            st.warning(
                "Sem dados disponíveis."
            )

            st.stop()

# ==========================================
# SÉRIES
# ==========================================

        if ativo1 not in dados.columns:

           st.error(
               f"Ativo sem dados: {ativo1}"
           )

           st.stop()

        if ativo2 not in dados.columns:

            st.error(
               f"Ativo sem dados: {ativo2}"
            )

            st.stop()

        serie1 = dados[ativo1]

        serie2 = dados[ativo2]

# ==========================================
# FATORES
# ==========================================

        hedge_ratio = calcular_hedge_ratio(

            serie1,
            serie2

        )

        fator1 = 1

        fator2 = hedge_ratio

# ==========================================
# SPREAD
# ==========================================

        spread = calcular_spread(

            serie1,
            serie2,
            fator1,
            fator2

        )

        estatisticas = calcular_estatisticas(

            spread

        )

        media = estatisticas["media"]

        desvio = estatisticas["desvio"]

        zscore = estatisticas["zscore"]

        correlacao = calcular_correlacao(

            serie1,
            serie2

        )
        
        half_life = calcular_half_life(

            spread

        )

        df_coint = calcular_cointegracao_rolling(

            serie1,
            serie2

        )

        

# ==========================================
# MÉTRICAS
# ==========================================

        col1, col2, col3, col4 = st.columns(4)

        with col1:

            st.metric(

                ativo1,

                f"{serie1.iloc[-1]:.2f}"

            )

        with col2:

            st.metric(

                ativo2,

                f"{serie2.iloc[-1]:.2f}"

            )

        with col3:

            st.metric(

                "Spread",

                f"{spread.iloc[-1]:.2f}"

            )

        with col4:

            st.metric(

                "Z-Score",

                f"{zscore:.2f}"

            )

        st.markdown("---")

        # ==========================================
        # STATUS OPERACIONAL
        # ==========================================

        render_status_operacional(

            zscore

        )

        st.markdown("---")       

        # ==========================================
        # DASHBOARD EXECUTIVO
        # ==========================================

        render_dashboard_executivo(

            spread,
            media,
            desvio,
            zscore,
            half_life

        )

        st.markdown("---")

        # ==========================================
        # COINTEGRAÇÃO ROLLING
        # ==========================================

        render_cointegracao_rolling(

            df_coint

        )

        st.markdown("---")        
        

        # ==========================================
        # ZSCORE INSTITUCIONAL
        # ==========================================

        render_zscore(

            spread,
            media,
            desvio

        )

        st.markdown("---")

    
        # ==========================================
        # HISTOGRAMA
        # ==========================================

        freq = render_histograma(

            spread,
            ativo1,
            ativo2,
            camada

        )

        # ==========================================
        # MAPA INSTITUCIONAL
        # ==========================================

        render_heatmap(

           freq

        )

        st.markdown("---")        


        
        # ==========================================
        # PERMANÊNCIA TEMPORAL
        # ==========================================

        render_permanencia(

            freq

        )

        st.markdown("---")
        
        # ==========================================
        # PREÇOS DOS ATIVOS
        # ==========================================

        st.subheader("📈 Preços dos Ativos")

        fig_preco = go.Figure()

        fig_preco.add_trace(

            go.Scatter(

                x=dados.index,

                y=serie1,

                name=ativo1

            )

        )

        fig_preco.add_trace(

            go.Scatter(

                x=dados.index,

                y=serie2,

                name=ativo2

            )

        )

        fig_preco.update_layout(

            template="plotly_dark",

            height=600

        )

        st.plotly_chart(

            fig_preco,

            use_container_width=True

        )

        st.markdown("---")

        # ==========================================
        # DISTÂNCIA
        # ==========================================

        st.subheader("📊 Distância entre os Ativos")

        fig_dist = go.Figure()

        fig_dist.add_trace(

            go.Scatter(

                x=spread.index,

                y=spread,

                name="Distância"

            )

        )

        fig_dist.add_hline(

            y=spread.mean(),

            line_dash="dash",

            annotation_text="Média"

        )

        fig_dist.add_hline(

            y=spread.iloc[-1],

            line_dash="dot",

            annotation_text="Atual"

        )

        fig_dist.update_layout(

            template="plotly_dark",

            height=600

        )

        st.plotly_chart(

            fig_dist,

            use_container_width=True

        )

        st.markdown("---")

        # ==========================================
        # ZSCORE
        # ==========================================

        st.subheader("📉 Z-Score do Spread")

        if spread.std() == 0:

            zscore_serie = spread * 0

        else:

            zscore_serie = (

                spread - spread.mean()

            ) / spread.std()
            
        fig_z = go.Figure()

        fig_z.add_trace(

            go.Scatter(

                x=spread.index,

                y=zscore_serie,

                name="Z-Score"

            )

        )

        fig_z.add_hline(

            y=0,

            line_color="white"

        )

        fig_z.add_hline(

            y=2,

            line_dash="dash",

            line_color="red"

        )

        fig_z.add_hline(

            y=-2,

            line_dash="dash",

            line_color="green"

        )

        fig_z.update_layout(

            template="plotly_dark",

            height=600

        )

        st.plotly_chart(

            fig_z,

            use_container_width=True

        )

        st.markdown("---")

        # ==========================================
        # SPREAD
        # ==========================================

        st.subheader("📈 Spread entre Ativos")

        fig_spread = go.Figure()

        fig_spread.add_trace(

            go.Scatter(

                x=spread.index,

                y=spread,

                name="Spread"

            )

        )

        fig_spread.add_hline(

            y=spread.mean(),

            line_dash="dash"

        )

        fig_spread.update_layout(

            template="plotly_dark",

            height=600

        )

        st.plotly_chart(

            fig_spread,

            use_container_width=True

        )        
    
    except Exception as erro:

        st.error(
            f"ERRO REAL: {erro}"
        )

        print("ERRO REAL:")
        print(str(erro))

        st.stop()

# ==========================================

# SCANNER

# ==========================================

elif st.session_state["menu"] == "Scanner":

    st.title("🚀 Scanner Quantitativo")

    st.markdown("""

### 🎯 Objetivo do Scanner

Encontrar pares com:

- Alta correlação
- Cointegração estatística
- Boa reversão à média
- Spread operacional utilizável

""")

    st.markdown("---")

    st.subheader("⚙️ Filtros do Scanner")

    modo_scanner = st.radio(

        "Modo do Scanner",

        [
            "Mesmo Setor",
            "Todos os Setores"
        ],

        horizontal=True

    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        correlacao_min = st.slider(

            "Correlação mínima",

            0.50,
            1.00,
            0.80,
            0.01

        )

    with col2:

        pvalue_max = st.slider(

            "P-Value máximo",

            0.001,
            0.10,
            0.05,
            0.001

        )

    with col3:

        zscore_min = st.slider(

            "Z-Score mínimo",

            0.0,
            5.0,
            0.8,
            0.1

        )

    with col4:

        periodo_scanner = st.selectbox(

            "Período",

            [
                "90d",
                "120d",
                "180d",
                "200d",
                "250d",
                "1y"
            ],

            index=3

        )

    st.markdown("---")

    if st.button("🚀 Executar Scanner"):

        with st.spinner("Analisando pares..."):

            try:

                df = executar_scanner(

                    segmentos=SEGMENTOS,

                    lista_ativos=LISTA_ATIVOS,

                    periodo=periodo_scanner,

                    modo=modo_scanner,

                    correlacao_min=correlacao_min,

                    pvalue_max=pvalue_max,

                    zscore_min=zscore_min

                )

                if df.empty:

                    st.warning(
                        "Nenhum par encontrado"
                    )

                    st.stop()

                else:

                    st.success(
                        f"{len(df)} pares encontrados"
                    )

                    h1, h2, h3, h4, h5, h6, h7, h8 = st.columns(
                            [2, 2, 1, 1, 1, 1, 1, 1]
                    )

                    with h1:
                        st.markdown("### Ativo 1")

                    with h2:
                        st.markdown("### Ativo 2")

                    with h3:
                        st.markdown("### Corr")

                    with h4:
                        st.markdown("### P-Val")

                    with h5:
                        st.markdown("### Z")

                    with h6:
                        st.markdown("### Vol")

                    with h7:
                        st.markdown("### Status")

                    with h8:
                        st.markdown("### Painel")

                    st.divider()

                    for idx, row in df.iterrows():

                        with st.container():

                            col1, col2, col3, col4, col5, col6, col7, col8 = st.columns(
                                [2, 2, 1, 1, 1, 1, 1, 1]
                            )

                            with col1:

                                st.write(
                                    row["Ativo 1"]
                                )

                            with col2:

                                st.write(
                                    row["Ativo 2"]
                                )

                            with col3:

                                st.write(
                                    f"{row['Correlação']:.4f}"
                                )

                            with col4:

                                st.write(
                                    f"{row['P-Value']:.4f}"
                                )

                            with col5:

                                st.write(
                                    f"{row['Pontuação Z']:.2f}"
                                )

                            with col6:

                                st.write(
                                    f"{row['Vol Spread']:.2f}"
                                )

                            with col7:

                                st.write(
                                    row["Status"]
                                )

                            with col8:

                                if st.button(

                                    "📂 Abrir",

                                    key=f"abrir_{idx}"

                                ):

                                    st.session_state["ativo1_select"] = row["Ativo 1"]

                                    st.session_state["ativo2_select"] = row["Ativo 2"]
                                    
                                    st.session_state["menu"] = "Painel"

                                    st.session_state["painel_pronto"] = True

                                    st.rerun()                           
                        st.divider()

            except Exception as erro:

                st.error(f"Erro: {erro}")
