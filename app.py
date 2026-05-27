
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
#=====================================
# ATIVOS B3 POR SEGMENTO
# ===================================

SEGMENTOS = {

    "Bancos": [

        "ITUB4.SA",
        "BBDC4.SA",
        "BBAS3.SA"

    ],

    "Petroleo": [

        "PETR3.SA",
        "PETR4.SA",
        "PRIO3.SA"

    ],

    "Mineracao": [

        "VALE3.SA",
        "GGBR4.SA"

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

        if agora - st.session_state["ultima_execucao"] < 3:

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

        dados = dados.dropna()

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

        fator1 = lote1 / 100

        fator2 = lote2 / 100

# ==========================================
# SPREAD
# ==========================================

        spread = (

            (serie1 * fator1)

            -

            (serie2 * fator2)

        )

        media = spread.mean()

        desvio = spread.std()

# ==========================================
# ZSCORE
# ==========================================

        if desvio == 0:

            zscore = 0

        else:

            zscore = (

                spread.iloc[-1]

                -

                media

            ) / desvio

# ==========================================
# CORRELAÇÃO
# ==========================================

        correlacao = serie1.corr(

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
# GRÁFICO SPREAD
# ==========================================

        fig = go.Figure()

        fig.add_trace(

            go.Scatter(

                x=spread.index,

                y=spread,

                name="Spread"

            )

        )

        fig.add_hline(

            y=media,

            line_dash="dash",

            line_color="yellow"

        )

        fig.update_layout(

            template="plotly_dark",

            height=600

        )

        st.plotly_chart(

            fig,

            width="stretch"

        )

    
        # ==========================================
        # HISTOGRAMA
        # ==========================================

        st.subheader(

            f"📊 Histograma de Camadas — {ativo1} x {ativo2}"

        )

        distancia = spread.abs()

        dist_max = float(distancia.max())

        spread_atual = float(abs(spread.iloc[-1]))

        media_hist = float(distancia.mean())

        bins = []

        inicio = 0

        while inicio <= dist_max + camada:

            bins.append(round(inicio, 2))

            inicio += camada

        if len(bins) > 0 and bins[-1] < dist_max:

            bins.append(round(dist_max + camada, 2))

        hist = pd.cut(

            distancia,

            bins=bins,

            include_lowest=True

        )

        freq = hist.value_counts().sort_index()
        
        # ==========================================
        # MAPA INSTITUCIONAL
        # ==========================================

        st.subheader("🔥 Mapa de Concentração Institucional")

        tabela_heatmap = []

        total_ocorrencias = int(freq.sum())

        for faixa, ocorrencias in freq.items():

            zona = (
                f"{faixa.left:.2f} ➜ "
                f"{faixa.right:.2f}"
            )

            ocorrencias = int(ocorrencias)

            percentual = float(
                (ocorrencias / total_ocorrencias) * 100
            )

            score = float(
                percentual * ocorrencias
            )

            tabela_heatmap.append({

                "Zona": zona,

                "Ocorrencias": ocorrencias,

                "Percentual": round(
                    percentual,
                    2
                ),

                "Score": round(
                    score,
                    2
                )

            })

        df_heatmap = pd.DataFrame(
            tabela_heatmap
        )

        df_heatmap = df_heatmap.sort_values(

            by="Score",

            ascending=False

        )

        st.dataframe(

            df_heatmap,

            width="stretch"

        )

        fig_heat = px.bar(

            df_heatmap,

            x="Percentual",

            y="Zona",

            orientation="h",

            text="Percentual",

            template="plotly_dark"

        )

        fig_heat.update_layout(

            title="Mapa de Concentração das Camadas",

            height=700

        )

        st.plotly_chart(

            fig_heat,

            width="stretch"

        )

        st.markdown("---")
        
        # ==========================================
        # PERMANÊNCIA TEMPORAL
        # ==========================================

        st.subheader("⏳ Permanência Temporal das Camadas")

        permanencia = []

        for faixa, ocorrencias in freq.items():

            zona = (
                f"{faixa.left:.2f} ➜ "
                f"{faixa.right:.2f}"
            )

            ocorrencias = int(ocorrencias)

            tempo_medio = round(
                ocorrencias / len(spread),
                2
            )

            tempo_max = ocorrencias

            score_temp = round(
                tempo_medio * ocorrencias,
                2
            )

            permanencia.append({

                "Zona": zona,

                "Tempo Médio": tempo_medio,

                "Tempo Máximo": tempo_max,

                "Ocorrencias": ocorrencias,

                "Score Temporal": score_temp

            })

        df_perm = pd.DataFrame(
            permanencia
        )

        df_perm = df_perm.sort_values(

            by="Tempo Médio",

            ascending=False

        )

        st.dataframe(

            df_perm,

            width="stretch"

        )

        fig_perm = px.bar(

            df_perm,

            x="Tempo Médio",

            y="Zona",

            orientation="h",

            text="Tempo Médio",

            template="plotly_dark"

        )

        fig_perm.update_layout(

            title="Tempo Médio de Permanência por Zona",

            height=700

        )

        st.plotly_chart(

            fig_perm,

            width="stretch"

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

            width="stretch"

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

            width="stretch"

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

            width="stretch"

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

            width="stretch"

        )        
    
    except Exception as erro:

        st.error(
            f"ERRO REAL: {erro}"
        )

        print("ERRO REAL:")
        print(erro)

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
            0.95,
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
            1.5,
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

                                    ativo1_sidebar = row["Ativo 1"]

                                    ativo2_sidebar = row["Ativo 2"]

                                    st.session_state["menu"] = "Painel"

                                    st.session_state["painel_pronto"] = True

                                    st.rerun()                           
                        st.divider()

            except Exception as erro:

                st.error(f"Erro: {erro}")
