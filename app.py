
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

import yfinance as yf

from auth import (
    tela_login,
    tela_cadastro
)

from scanner import (
    executar_scanner
)

from market_data import (
    baixar_dados_finnhub
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

@st.cache_data(ttl=300)

def baixar_dados(

    ativos,

    periodo

):

    return baixar_dados_finnhub(

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

        import time

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
                "Yahoo Finance temporariamente indisponível. Tente novamente em alguns segundos."
            )

            st.stop()
       
        # ==========================================
        # AJUSTE YFINANCE
        # ==========================================

        if isinstance(
            dados.columns,
            pd.MultiIndex
        ):

            dados = dados.xs(

                "Close",

                axis=1,

                level=0

            )
        # ==========================================
        # REMOVE NAN
        # ==========================================

        dados = dados.dropna()

        if dados.empty:

            st.warning(
                "Sem dados disponíveis."
            )

            st.stop()

        serie1 = dados[ativo1]

        serie2 = dados[ativo2]

        fator1 = lote1 / 100

        fator2 = lote2 / 100

        spread = (

            (serie1 * fator1)

            -

            (serie2 * fator2)

        )

        media = spread.mean()

        desvio = spread.std()

        if desvio == 0:

            zscore = 0

        else:

            zscore = (

                spread.iloc[-1]

                -

                media

            ) / desvio

        correlacao = serie1.corr(

            serie2

        )

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

               "DISTÂNCIA ATUAL",

               f"{spread.iloc[-1]:.2f}"

            )

        with col4:

            st.metric(

                "Pontuação Z",

                f"{zscore:.2f}"

            )

        st.markdown("---")

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(
                "Correlação",
                f"{correlacao:.4f}"
            )
  
        with c2:

            st.metric(
                "Spread Médio",
                f"{media:.2f}"
            )

        with c3:

            st.metric(
                "Desvio",
                f"{desvio:.2f}"
            )

        st.markdown("---")

        st.subheader(

            f"📊 Histograma de Camadas — {ativo1} x {ativo2}"

        )

        distancia = spread.abs()

        dist_max = float(distancia.max())

        dist_min = float(distancia.min())

        spread_atual = float(abs(spread.iloc[-1]))

        media_hist = float(distancia.mean())

        bins = []

        inicio = 0

        while inicio <= dist_max + camada:

            bins.append(round(inicio, 2))

            inicio += camada

        if bins[-1] < dist_max:

            bins.append(round(dist_max + camada, 2))

        hist = pd.cut(

            distancia,

            bins=bins,

            include_lowest=True

        )

        freq = hist.value_counts().sort_index()

        camada_dominante = freq.idxmax()

        camada_texto = (

            f"{camada_dominante.left:.2f} → "
            f"{camada_dominante.right:.2f}"

        )

        h1, h2, h3, h4 = st.columns(4)

        with h1:

            st.metric(

                "Distância Máxima",

                f"R$ {dist_max:.2f}"

            )

        with h2:

            st.metric(

                "Distância Mínima",

                f"R$ {dist_min:.2f}"

            )

        with h3:

            st.metric(

                "Camada Dominante",

                camada_texto

            )

        with h4:

            st.metric(

                "Ocorrências",

                int(freq.max())

            )

        st.info(f"""

📅 PERÍODO ANALISADO: {spread.index[0].strftime('%d/%m/%Y')} até {spread.index[-1].strftime('%d/%m/%Y')}

📊 Velas analisadas: {len(spread)}

📈 Tamanho da camada: R$ {camada}

🎯 Camada dominante: {camada_texto}

📌 Frequência: {freq.max()} ocorrências

🔺 {ativo1} ficou mais caro em: {(spread > 0).mean()*100:.2f}% do período

🔻 {ativo2} ficou mais caro em: {(spread < 0).mean()*100:.2f}% do período

""")

        fig_hist = go.Figure()

        x_labels = [

            round(i.mid, 2)

            for i in freq.index

        ]

        fig_hist.add_trace(

            go.Bar(

                x=x_labels,

                y=freq.values,

                marker_color="#d89500",

                opacity=0.90

            )

        )

        fig_hist.add_vline(

            x=media_hist,

            line_width=3,
 
            line_dash="dash",

            line_color="red"

        )

        fig_hist.add_vline(

            x=spread_atual,

            line_width=3,

            line_color="yellow"

        )

        fig_hist.update_layout(

            template="plotly_dark",

            height=600,

            title="Distribuição da Distância entre os Ativos",

            xaxis_title="Faixas de Distância (R$)",

            yaxis_title="Ocorrências",

            bargap=0.03

         )

        st.plotly_chart(

            fig_hist,

            width="stretch"

        )

        st.markdown("---")

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

        st.error(f"Erro: {erro}")
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
