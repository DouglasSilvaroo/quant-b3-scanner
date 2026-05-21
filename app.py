
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

from auth import (
    tela_login,
    tela_cadastro
)

from scanner import (
    executar_scanner
)

# ==========================================
# CONFIG STREAMLIT
# ==========================================

st.set_page_config(

    page_title="PAINEL SPREADS",
    page_icon="📈",
    layout="wide"

)

# ==========================================
# SESSION
# ==========================================

if "logado" not in st.session_state:

    st.session_state["logado"] = False

if "usuario" not in st.session_state:

    st.session_state["usuario"] = ""

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

    # ======================================
    # BANCOS / FINANCEIRO
    # ======================================

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

    # ======================================
    # PETRÓLEO / GÁS
    # ======================================

    "Petroleo": [

        "PETR3.SA",
        "PETR4.SA",
        "PRIO3.SA",
        "RECV3.SA",
        "RRRP3.SA",
        "CSAN3.SA",
        "VBBR3.SA",
        "UGPA3.SA"

    ],

    # ======================================
    # MINERAÇÃO / SIDERURGIA
    # ======================================

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

    # ======================================
    # ENERGIA
    # ======================================

    "Energia": [

        "AXIA3.SA",
        "AXIA6.SA",
        "CPFE3.SA",
        "CMIG3.SA",
        "CMIG4.SA",
        "TAEE3.SA",
        "TAEE5.SA",
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
        "ALUP11.SA",
        "EQTL3.SA"

    ],

    # ======================================
    # VAREJO / CONSUMO
    # ======================================

    "Varejo": [

        "MGLU3.SA",
        "LREN3.SA",
        "VIIA3.SA",
        "ASAI3.SA",
        "PCAR3.SA",
        "CRFB3.SA",
        "RADL3.SA",
        "CEAB3.SA",
        "PETZ3.SA"

    ],

    # ======================================
    # PAPEL / CELULOSE
    # ======================================

    "Papel": [

        "SUZB3.SA",
        "KLBN3.SA",
        "KLBN4.SA",
        "KLBN11.SA",
        "RANI3.SA"

    ],

    # ======================================
    # CONSTRUÇÃO
    # ======================================

    "Construcao": [

        "CYRE3.SA",
        "EZTC3.SA",
        "MRVE3.SA",
        "DIRR3.SA",
        "TEND3.SA",
        "LAVV3.SA"

    ],

    # ======================================
    # TELECOM / TECNOLOGIA
    # ======================================

    "Telecom": [

        "VIVT3.SA",
        "TIMS3.SA",
        "POSI3.SA",
        "TOTS3.SA"

    ],

    # ======================================
    # TRANSPORTE / LOGÍSTICA
    # ======================================

    "Logistica": [

        "RAIL3.SA",
        "AZUL4.SA",
        "GOLL4.SA",
        "CCRO3.SA",
        "ECOR3.SA"

    ],

    # ======================================
    # ALIMENTOS / BEBIDAS
    # ======================================

    "Alimentos": [

        "ABEV3.SA",
        "JBSS3.SA",
        "BRFS3.SA",
        "MRFG3.SA",
        "SLCE3.SA"

    ],

    # ======================================
    # SAÚDE
    # ======================================

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

    st.title("🏦 PAINEL SPREADS")

    st.success(
        f"👤 {st.session_state['usuario']}"
    )

    st.markdown("---")

    menu = st.radio(

        "Navegação",

        [

            "Painel",
            "Scanner"

        ]

    )

    st.markdown("---")

    st.subheader("⚙️ Configurações")

    ativo1_sidebar = st.selectbox(

        "Ativo 1",

        LISTA_ATIVOS,

        index=0

    )

    ativo2_sidebar = st.selectbox(

        "Ativo 2",

        LISTA_ATIVOS,

        index=1

    )

    periodo_sidebar = st.selectbox(

        "Período",

        [

            "3mo",
            "6mo",
            "1y",
            "200d"

        ],

        index=3

    )

    st.markdown("---")

    st.subheader("⚖️ Proporção Operacional")
    
    lote1 = st.number_input(

    f"Lote {ativo1_sidebar}",

    min_value=100,
    step=100,
    value=100

    )

    lote2 = st.number_input(

    f"Lote {ativo2_sidebar}",

    min_value=100,
    step=100,
    value=100

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

    if st.button("Logout"):

        st.session_state["logado"] = False

        st.rerun()

# ==========================================
# PAINEL
# ==========================================

if menu == "Painel":

    st.title("🏦 PAINEL SPREADS")

    ativo1 = ativo1_sidebar
    ativo2 = ativo2_sidebar
    periodo = periodo_sidebar

    try:

        # ==================================
        # DOWNLOAD
        # ==================================

        dados = yf.download(

            [ativo1, ativo2],

            period=periodo,

            auto_adjust=True,

            progress=False

        )

        # ==================================
        # MULTIINDEX
        # ==================================

        if isinstance(
            dados.columns,
            pd.MultiIndex
        ):

            dados = dados["Close"]

        dados = dados.dropna()

        # ==================================
        # SERIES
        # ==================================

        serie1 = dados[ativo1]

        serie2 = dados[ativo2]

        # ==================================
        # SPREAD
        # ==================================

        fator1 = lote1 / 100
        fator2 = lote2 / 100

        spread = (

        (serie1 * fator1)
        -
        (serie2 * fator2)

        )
        media = spread.mean()

        desvio = spread.std()

        zscore = (

            spread.iloc[-1]
            -
            media

        ) / desvio

        correlacao = serie1.corr(
            serie2
        )

        # ==================================
        # CARDS SUPERIORES
        # ==================================

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

                "SPREAD ATUAL",

                f"{spread.iloc[-1]:.2f}"

            )

        with col4:

            st.metric(

                "Pontuação Z",

                f"{zscore:.2f}"

            )

        st.markdown("---")

        # ==================================
        # MÉTRICAS
        # ==================================

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

        # ==================================
        # HISTOGRAMA
        # ==================================

        st.subheader(

            f"📊 Histograma de Camadas — {ativo1} x {ativo2}"

        )

        distancia = spread.abs()

        dist_max = float(distancia.max())

        dist_min = float(distancia.min())

        spread_atual = float(abs(spread.iloc[-1]))

        media_hist = float(distancia.mean())

        # ==================================
        # CAMADAS
        # ==================================

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

        # ==================================
        # MÉTRICAS HISTOGRAMA
        # ==================================

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

        # ==================================
        # BOX INFO
        # ==================================

        st.info(f"""

📅 PERÍODO ANALISADO: {spread.index[0].strftime('%d/%m/%Y')} até {spread.index[-1].strftime('%d/%m/%Y')}

📊 Velas analisadas: {len(spread)}

📈 Tamanho da camada: R$ {camada}

🎯 Camada dominante: {camada_texto}

📌 Frequência: {freq.max()} ocorrências

🔺 {ativo1} ficou mais caro em: {(spread > 0).mean()*100:.2f}% do período

🔻 {ativo2} ficou mais caro em: {(spread < 0).mean()*100:.2f}% do período

""")

        # ==================================
        # HISTOGRAMA PROFISSIONAL
        # ==================================

        x_labels = [

            round(i.mid, 2)

            for i in freq.index

        ]

        fig_hist = go.Figure()

        fig_hist.add_trace(

            go.Bar(

                x=x_labels,

                y=freq.values,

                marker_color="#d89500",

                opacity=0.90

            )

        )

        # MÉDIA

        fig_hist.add_vline(

            x=media_hist,

            line_width=3,

            line_dash="dash",

            line_color="red"

        )

        fig_hist.add_annotation(

            x=media_hist,

            y=max(freq.values),

            text="Média",

            showarrow=False,

            font=dict(

                color="white",
                size=14

            ),

            yshift=18

        )

        # ATUAL

        fig_hist.add_vline(

            x=spread_atual,

            line_width=3,

            line_color="yellow"

        )

        fig_hist.add_annotation(

            x=spread_atual,

            y=max(freq.values),

            text="Atual",

            showarrow=False,

            font=dict(

                color="white",
                size=14

            ),

            yshift=18

        )

        # REGIÃO SOMBREADA

        fig_hist.add_vrect(

            x0=dist_min,

            x1=media_hist,

            fillcolor="orange",

            opacity=0.08,

            line_width=0

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

            use_container_width=True

        )

        # ==========================================
        # MAPA DE CONCENTRAÇÃO INSTITUCIONAL
        # ==========================================

        st.markdown("---")

        st.subheader(
            "🔥 Mapa de Concentração Institucional"
        )

        # ==========================================
        # CÁLCULO CONCENTRAÇÃO
        # ==========================================

        concentracao_df = freq.reset_index()

        concentracao_df.columns = [

            "Zona",
            "Ocorrencias"

        ]

        concentracao_df["Percentual"] = (

            concentracao_df["Ocorrencias"]
            /
            concentracao_df["Ocorrencias"].sum()
            * 100

        ).round(2)

        concentracao_df["Score"] = (

            concentracao_df["Ocorrencias"]
            *
            concentracao_df["Percentual"]

        ).round(2)

        # ==========================================
        # FORMATAÇÃO ZONA
        # ==========================================

        concentracao_df["Zona"] = (

            concentracao_df["Zona"]
            .apply(

                lambda x:
                f"{x.left:.2f} → {x.right:.2f}"

            )

        )

        # ==========================================
        # ORDENAÇÃO
        # ==========================================

        concentracao_df = concentracao_df.sort_values(

            by="Score",
            ascending=False

        )

        # ==========================================
        # TABELA
        # ==========================================

        st.dataframe(

            concentracao_df,

            use_container_width=True,

            height=380

        )

        # ==========================================
        # GRÁFICO HORIZONTAL
        # ==========================================

        fig_concentracao = px.bar(

            concentracao_df.sort_values("Percentual"),

            x="Percentual",

            y="Zona",

            orientation="h",

            text="Percentual",

            title="Mapa de Concentração das Camadas",

            color_discrete_sequence=["#1f77ff"]

        )

        fig_concentracao.update_layout(

            template="plotly_dark",

            height=600,

            xaxis_title="% Concentração",

            yaxis_title="Zonas"

        )

        fig_concentracao.update_traces(

            textposition="outside"

        )

        st.plotly_chart(

            fig_concentracao,

            use_container_width=True

        )

        # ==========================================
        # PERMANÊNCIA TEMPORAL DAS CAMADAS
        # ==========================================

        st.markdown("---")

        st.subheader(
            "⏳ Permanência Temporal das Camadas"
        )

        # ==========================================
        # DATAFRAME SPREAD
        # ==========================================

        spread_df = pd.DataFrame({

            "spread": distancia

        })

        # ==========================================
        # CÁLCULO DAS ZONAS
        # ==========================================

        spread_df["zona"] = pd.cut(

            spread_df["spread"],

            bins=bins,

            include_lowest=True

        )

        # ==========================================
        # IDENTIFICA BLOCOS CONTÍNUOS
        # ==========================================

        spread_df["grupo"] = (

            spread_df["zona"]
            !=
            spread_df["zona"].shift()

        ).cumsum()

        tempo_df = (

            spread_df
            .groupby(["zona", "grupo"])
            .size()
            .reset_index(name="duracao")

        )

        # ==========================================
        # MÉTRICAS TEMPORAIS
        # ==========================================

        tempo_stats = (

            tempo_df
            .groupby("zona")["duracao"]
            .agg([

                ("Tempo Médio", "mean"),
                ("Tempo Máximo", "max"),
                ("Ocorrências", "count")

            ])
            .reset_index()

        )

        tempo_stats["Score Temporal"] = (

            tempo_stats["Tempo Médio"]
            *
            tempo_stats["Ocorrências"]

        ).round(0)

        tempo_stats = tempo_stats.sort_values(

            by="Score Temporal",
            ascending=False

        )

        tempo_stats["Tempo Médio"] = (

            tempo_stats["Tempo Médio"]
            .round(2)

        )

        # ==========================================
        # FORMATAÇÃO DA ZONA
        # ==========================================

        tempo_stats["Zona"] = (

            tempo_stats["zona"]
            .apply(

                lambda x:
                f"{x.left:.2f} → {x.right:.2f}"

            )

        )

        # ==========================================
        # ORGANIZA COLUNAS
        # ==========================================

        tempo_stats = tempo_stats[[

            "Zona",
            "Tempo Médio",
            "Tempo Máximo",
            "Ocorrências",
            "Score Temporal"

        ]]

        # ==========================================
        # TABELA
        # ==========================================

        st.dataframe(

            tempo_stats,

            use_container_width=True,

            height=380

        )

        # ==========================================
        # GRÁFICO TEMPORAL
        # ==========================================

        import plotly.express as px

        fig_tempo = px.bar(

            tempo_stats.sort_values("Tempo Médio"),

            x="Tempo Médio",

            y="Zona",

            orientation="h",

            text="Tempo Médio",

            title="Tempo Médio de Permanência por Zona",

            color_discrete_sequence=["#1f77ff"]

        )

        fig_tempo.update_layout(

            template="plotly_dark",

            height=550,

            xaxis_title="Tempo Médio",

            yaxis_title="Zona"

        )

        fig_tempo.update_traces(

            textposition="outside"

        )

        st.plotly_chart(

            fig_tempo,

            use_container_width=True

        )

        # ==========================================
        # PREÇOS DOS ATIVOS
        # ==========================================

        st.markdown("---")

        st.subheader("📈 Preços dos Ativos")

        fig_precos = go.Figure()

        # ==========================================
        # ATIVO 1
        # ==========================================

        fig_precos.add_trace(

            go.Scatter(

                x=serie1.index,

                y=serie1,

                mode="lines",

                name=ativo1,

                line=dict(

                    color="#f2a900",
                    width=2

                )

            )

        )

        # ==========================================
        # ATIVO 2
        # ==========================================

        fig_precos.add_trace(

            go.Scatter(

                x=serie2.index,

                y=serie2,

                mode="lines",

                name=ativo2,

                line=dict(

                    color="#ff4b4b",
                    width=2

                )

            )

        )

        # ==========================================
        # LAYOUT
        # ==========================================

        fig_precos.update_layout(

            template="plotly_dark",

            height=600,

            hovermode="x unified",

            title="Preços",

            xaxis_title="Data",

            yaxis_title="Preço",

            legend=dict(

                orientation="v",

                yanchor="top",

                y=1,

                xanchor="left",

                x=1.02

            )

        )

        st.plotly_chart(

            fig_precos,

            use_container_width=True

        )

        # ==========================================
        # DISTÂNCIA ENTRE OS ATIVOS
        # ==========================================

        st.markdown("---")

        st.subheader("📊 Distância entre os Ativos")

        fig_distancia = go.Figure()

        # ==========================================
        # LINHA PRINCIPAL
        # ==========================================

        fig_distancia.add_trace(

            go.Scatter(

                x=spread.index,

                y=distancia,

                mode="lines",

                name="Distância",

                line=dict(

                    color="#f2a900",
                    width=2

                )

            )

        )

        # ==========================================
        # LINHA MÉDIA
        # ==========================================

        fig_distancia.add_hline(

            y=media_hist,

            line_dash="dash",

            line_color="yellow",

            annotation_text="Média",

            annotation_position="top left"

        )

        # ==========================================
        # LINHA ATUAL
        # ==========================================

        fig_distancia.add_hline(

            y=spread_atual,

            line_dash="dot",

            line_color="red",

            annotation_text="Atual",

            annotation_position="bottom left"

        )

        # ==========================================
        # LAYOUT
        # ==========================================

        fig_distancia.update_layout(

            template="plotly_dark",

            height=600,

            hovermode="x unified",

            title="Distância entre os Ativos",

            xaxis_title="Data",

            yaxis_title="Distância (R$)"

        )

        st.plotly_chart(

            fig_distancia,

            use_container_width=True

        )

        # ==========================================
        # Z-SCORE PROFISSIONAL
        # ==========================================

        st.markdown("---")

        st.subheader("🎯 Z-Score")

        # ==========================================
        # SÉRIE Z-SCORE
        # ==========================================

        zscore_series = (

            spread - media

        ) / desvio

        # ==========================================
        # FIGURA
        # ==========================================

        fig_z = go.Figure()

        # ==========================================
        # LINHA ZSCORE
        # ==========================================

        fig_z.add_trace(

            go.Scatter(

                x=zscore_series.index,

                y=zscore_series,

                mode="lines",

                name="Z-Score",

                line=dict(

                    color="#00d4ff",
                    width=2

                )

            )

        )

        # ==========================================
        # LINHA ZERO
        # ==========================================

        fig_z.add_hline(

            y=0,

            line_dash="solid",

            line_color="white",

            annotation_text="Média",

            annotation_position="top left"

        )

        # ==========================================
        # LINHA +2
        # ==========================================

        fig_z.add_hline(

            y=2,

            line_dash="dash",

            line_color="red",

            annotation_text="+2",

            annotation_position="top left"

        )

        # ==========================================
        # LINHA -2
        # ==========================================

        fig_z.add_hline(

            y=-2,

            line_dash="dash",

            line_color="lime",

            annotation_text="-2",

            annotation_position="bottom left"

        )

        # ==========================================
        # REGIÕES SOMBREADAS
        # ==========================================

        fig_z.add_hrect(

            y0=2,
            y1=5,

            fillcolor="red",

            opacity=0.08,

            line_width=0

        )

        fig_z.add_hrect(

            y0=-5,
            y1=-2,

            fillcolor="green",

            opacity=0.08,

            line_width=0

        )

        # ==========================================
        # LAYOUT
        # ==========================================

        fig_z.update_layout(

            template="plotly_dark",

            height=600,

            hovermode="x unified",

            title="Z-Score do Spread",

            xaxis_title="Data",

            yaxis_title="Z-Score"

        )

        st.plotly_chart(

            fig_z,

            use_container_width=True

        )

        # ==================================
        # SPREAD
        # ==================================

        st.markdown("---")

        st.subheader("📈 Spread entre Ativos")

        fig = go.Figure()

        fig.add_trace(

            go.Scatter(

                x=spread.index,

                y=spread,

                name="Spread",

                line=dict(
                    color="cyan",
                    width=2
                )

            )

        )

        fig.add_hline(

            y=media,

            line_dash="dash",

            line_color="white"

        )

        fig.update_layout(

            template="plotly_dark",

            height=600

        )

        st.plotly_chart(

            fig,
            use_container_width=True

        )

    except Exception as erro:

        st.error(f"Erro: {erro}")

# ==========================================
# SCANNER
# ==========================================

elif menu == "Scanner":

    st.title("🚀 Scanner Quantitativo")

    st.markdown("""
    ### 🎯 Objetivo do Scanner

    Encontrar pares com:

    - Alta correlação
    - Cointegração estatística
    - Boa reversão à média
    - Spread operacional utilizável
    """)

    # ==========================================
    # FILTROS
    # ==========================================

    st.markdown("---")

    st.subheader("⚙️ Filtros do Scanner")

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

    # ==========================================
    # EXECUTAR SCANNER
    # ==========================================

    if st.button("🚀 Executar Scanner"):

        with st.spinner("Analisando pares..."):

            try:

                df = executar_scanner(

                    LISTA_ATIVOS,
                    periodo=periodo_scanner

                )

                # ==========================================
                # VALIDAÇÃO
                # ==========================================

                if df.empty:

                    st.warning(
                        "Nenhum par encontrado"
                    )

                else:

                    # ==========================================
                    # FILTROS
                    # ==========================================

                    if "Correlação" in df.columns:

                        df = df[
                            df["Correlação"] >= correlacao_min
                        ]

                    if "P-Value" in df.columns:

                        df = df[
                            df["P-Value"] <= pvalue_max
                        ]

                    if "Pontuação Z" in df.columns:

                        df = df[
                            abs(df["Pontuação Z"]) >= zscore_min
                        ]

                    # ==========================================
                    # STATUS OPERACIONAL
                    # ==========================================

                    if "Pontuação Z" in df.columns:

                        status_lista = []

                        for _, row in df.iterrows():

                            z = row["Pontuação Z"]

                            if z >= 2:

                                status_lista.append(
                                    "🟢 Entrar Crédito"
                                )

                            elif z <= -2:

                                status_lista.append(
                                    "🔴 Entrar Débito"
                                )

                            else:

                                status_lista.append(
                                    "🟡 Neutro"
                                )

                        df["Status"] = status_lista

                    # ==========================================
                    # SCORE QUANT
                    # ==========================================

                    score_lista = []

                    for _, row in df.iterrows():

                        score = 0

                        # ==================================
                        # CORRELAÇÃO
                        # ==================================

                        corr = row["Correlação"]

                        if corr >= 0.99:

                            score += 40

                        elif corr >= 0.97:

                            score += 30

                        elif corr >= 0.95:

                            score += 20

                        # ==================================
                        # P-VALUE
                        # ==================================

                        pv = row["P-Value"]

                        if pv <= 0.01:

                            score += 40

                        elif pv <= 0.03:

                            score += 30

                        elif pv <= 0.05:

                            score += 20

                        # ==================================
                        # Z-SCORE
                        # ==================================

                        if "Pontuação Z" in df.columns:

                            zscore = abs(
                                row["Pontuação Z"]
                            )

                            if zscore >= 3:

                                score += 20

                            elif zscore >= 2:

                                score += 10

                        score_lista.append(score)

                    df["Score Quant"] = score_lista

                    # ==========================================
                    # ORDENAÇÃO
                    # ==========================================

                    df = df.sort_values(

                        by=[
                            "Score Quant",
                            "Correlação"
                        ],

                        ascending=False

                    )

                    # ==========================================
                    # KPIs
                    # ==========================================

                    st.success(
                        f"{len(df)} pares encontrados"
                    )

                    k1, k2, k3, k4 = st.columns(4)

                    with k1:

                        st.metric(

                            "Pares",

                            len(df)

                        )

                    with k2:

                        st.metric(

                            "Maior Correlação",

                            f"{df['Correlação'].max():.4f}"

                        )

                    with k3:

                        if "Pontuação Z" in df.columns:

                            st.metric(

                                "Maior Z-Score",

                                f"{df['Pontuação Z'].abs().max():.2f}"

                            )

                    with k4:

                        st.metric(

                            "Melhor Score",

                            int(df["Score Quant"].max())

                        )

                    st.markdown("---")

                    # ==========================================
                    # TABELA
                    # ==========================================

                    st.dataframe(

                        df,

                        use_container_width=True,
                        height=700

                    )

                    # ==========================================
                    # TOP 10
                    # ==========================================

                    st.markdown("---")

                    st.subheader(
                        "🏆 TOP 10 Oportunidades"
                    )

                    top10 = df.head(10)

                    for _, row in top10.iterrows():

                        st.markdown(f"""

### {row['Ativo 1']} x {row['Ativo 2']}

- Status: {row.get('Status', 'N/A')}
- Correlação: {row['Correlação']:.4f}
- P-Value: {row['P-Value']:.4f}
- Z-Score: {row.get('Pontuação Z', 0):.2f}
- Score Quant: {row['Score Quant']}

---

""")

            except Exception as erro:

                st.error(f"Erro: {erro}")
