
# ==========================================
# QUANT B3 SCANNER - BASE INSTITUCIONAL
# ==========================================

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from scanner import executar_scanner

from statsmodels.tsa.stattools import coint
from statsmodels.regression.linear_model import OLS
from statsmodels.tools.tools import add_constant

# ==========================================
# CONFIGURAÇÃO
# ==========================================

st.set_page_config(
    page_title="PAINEL SPREADS",
    page_icon="📈",
    layout="wide"
)

# ==========================================
# LISTA B3
# ==========================================

LISTA_ATIVOS = [

    "PETR3.SA",
    "PETR4.SA",
    "PRIO3.SA",
    "RRRP3.SA",
    "VALE3.SA",
    "CSNA3.SA",
    "USIM3.SA",
    "USIM5.SA",
    "GGBR4.SA",
    "ITUB3.SA",
    "ITUB4.SA",
    "BBDC3.SA",
    "BBDC4.SA",
    "BBAS3.SA",
    "SANB11.SA",
    "BPAC11.SA",
    "CMIG4.SA",
    "CPFE3.SA",
    "EQTL3.SA",
    "TAEE11.SA",
    "EGIE3.SA",
    "ABEV3.SA",
    "LREN3.SA",
    "MGLU3.SA",
    "JBSS3.SA",
    "BRFS3.SA",
    "MRFG3.SA",
    "SUZB3.SA",
    "KLBN11.SA",
    "VIVT3.SA",
    "TIMS3.SA",
    "HAPV3.SA",
    "RADL3.SA",
    "RAIL3.SA",
    "CCRO3.SA",
    "WEGE3.SA",
    "SBSP3.SA",
    "SAPR4.SA",
    "BBSE3.SA",
    "CXSE3.SA",
    "CYRE3.SA",
    "MRVE3.SA",
    "AZUL4.SA",
    "GOLL4.SA",
    "ALUP11.SA",
    "CPLE6.SA",
    "B3SA3.SA",
    "ITSA4.SA",
    "MULT3.SA",
    "SLCE3.SA",
    "SOJA3.SA",
    "UNIP6.SA",
    "EMBR3.SA",
    "GOAU4.SA",
    "VBBR3.SA",
    "UGPA3.SA"

]

# ==========================================
# TÍTULO
# ==========================================

st.title("📊 PAINEL SPREADS")

st.markdown(
    "### Plataforma Profissional de Pair Trading"
)

# ==========================================
# SIDEBAR
# ==========================================

st.sidebar.header("⚙️ Configurações")

ativo1 = st.sidebar.text_input(
    "Ativo 1",
    value="PETR3.SA"
)

ativo2 = st.sidebar.text_input(
    "Ativo 2",
    value="PETR4.SA"
)

periodo = st.sidebar.selectbox(
    "Período",
    ["50d", "100d", "200d", "300d"],
    index=2
)

# ==========================================
# CAMADAS
# ==========================================

st.sidebar.markdown("---")

st.sidebar.header("📊 Camadas de Spread")

spread_alvo = st.sidebar.number_input(
    "Tamanho da Camada",
    value=0.50,
    step=0.10
)

tolerancia = st.sidebar.number_input(
    "Tolerância",
    value=0.10,
    step=0.05
)

# ==========================================
# PROPORÇÃO
# ==========================================

st.sidebar.markdown("---")

st.sidebar.header("⚖️ Proporção Operacional")

quantidade_ativo1 = st.sidebar.number_input(
    f"Lote {ativo1}",
    min_value=1,
    value=100,
    step=10
)

quantidade_ativo2 = st.sidebar.number_input(
    f"Lote {ativo2}",
    min_value=1,
    value=100,
    step=10
)

# ==========================================
# SCANNER
# ==========================================

st.sidebar.markdown("---")

st.sidebar.header("🚀 Scanner Quantitativo")

executar_scan = st.sidebar.button(
    "Executar Scanner"
)

# ==========================================
# DOWNLOAD DADOS
# ==========================================

try:

    dados = yf.download(

        [ativo1, ativo2],

        period=periodo,

        auto_adjust=True,

        progress=False

    )

    # ======================================
    # MULTI INDEX
    # ======================================

    if isinstance(dados.columns, pd.MultiIndex):

        if "Close" in dados.columns.get_level_values(0):

            dados = dados["Close"]

        elif "Adj Close" in dados.columns.get_level_values(0):

            dados = dados["Adj Close"]

    dados = dados.dropna()

    if dados.empty:

        st.error("Nenhum dado encontrado")

        st.stop()

    # ======================================
    # SÉRIES
    # ======================================

    serie1 = dados[ativo1]

    serie2 = dados[ativo2]

    # ======================================
    # CORRELAÇÃO
    # ======================================

    correlacao = serie1.corr(serie2)

    # ======================================
    # COINTEGRAÇÃO
    # ======================================

    resultado = coint(
        serie1,
        serie2
    )

    pvalue = resultado[1]

    # ======================================
    # HEDGE RATIO
    # ======================================

    modelo = OLS(
        serie1,
        add_constant(serie2)
    ).fit()

    hedge_ratio = modelo.params.iloc[1]

    # ======================================
    # SPREAD ESTATÍSTICO
    # ======================================

    spread_stat = (
        serie1
        -
        (hedge_ratio * serie2)
    )

    media_stat = spread_stat.mean()

    desvio_stat = spread_stat.std()

    if desvio_stat == 0:

        st.error("Desvio padrão zerado.")

        st.stop()

    # ======================================
    # ZSCORE
    # ======================================

    zscore = (
        spread_stat - media_stat
    ) / desvio_stat

    ultimo_z = zscore.iloc[-1]

    # ======================================
    # SPREAD VISUAL
    # ======================================

    spread = serie1 - serie2

    media = spread.mean()

    desvio = spread.std()

    spread_atual = round(spread.iloc[-1], 2)

    distancia_minima = round(spread.min(), 2)

    distancia_maxima = round(spread.max(), 2)

    # ======================================
    # OCORRÊNCIAS
    # ======================================

    percentual_ocorrencias = (

        (
            (
                spread >= (
                    spread_alvo - tolerancia
                )
            )
            &
            (
                spread <= (
                    spread_alvo + tolerancia
                )
            )
        ).mean()

    ) * 100

    # ======================================
    # CARDS
    # ======================================

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "Correlação",
            round(correlacao, 4)
        )

    with col2:

        st.metric(
            "Valor-p",
            round(pvalue, 4)
        )

    with col3:

        st.metric(
            "Índice de Cobertura",
            round(hedge_ratio, 4)
        )

    with col4:

        st.metric(
            "Pontuação Z",
            round(ultimo_z, 2)
        )

    # ======================================
    # SINAL
    # ======================================

    if ultimo_z > 2:

        st.error("🔴 SHORT SPREAD")

    elif ultimo_z < -2:

        st.success("🟢 LONG SPREAD")

    else:

        st.warning("🟡 NEUTRO")

    # ======================================
    # HISTOGRAMA
    # ======================================

    st.subheader(
        f"📊 Histograma de Camadas — {ativo1} x {ativo2}"
    )

    if distancia_minima == distancia_maxima:

        distancia_maxima += spread_alvo

    bins = np.arange(

        distancia_minima,

        distancia_maxima + spread_alvo,

        spread_alvo

    )

    hist, edges = np.histogram(

        spread,

        bins=bins

    )

    # ======================================
    # CAMADA DOMINANTE
    # ======================================

    indice_max = np.argmax(hist)

    camada_inicio = round(edges[indice_max], 2)

    camada_fim = round(edges[indice_max + 1], 2)

    maior_ocorrencia = int(hist[indice_max])

    # ======================================
    # INFORMAÇÕES
    # ======================================

    data_inicio = dados.index.min().strftime("%d/%m/%Y")

    data_fim = dados.index.max().strftime("%d/%m/%Y")

    dias_total = len(dados)

    spread_raw = (
        (serie1 * quantidade_ativo1)
        -
        (serie2 * quantidade_ativo2)
    )

    freq_ativo1 = (
        (spread_raw > 0).mean()
    ) * 100

    freq_ativo2 = (
        (spread_raw < 0).mean()
    ) * 100

    # ======================================
    # PAINEL SUPERIOR
    # ======================================

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:

        st.metric(
            "Distância Atual",
            f"R$ {spread_atual}"
        )

    with col2:

        st.metric(
            "Distância Máxima",
            f"R$ {distancia_maxima}"
        )

    with col3:

        st.metric(
            "Distância Mínima",
            f"R$ {distancia_minima}"
        )

    with col4:

        st.metric(
            "Camada Dominante",
            f"{camada_inicio} → {camada_fim}"
        )

    with col5:

        st.metric(
            "Ocorrências",
            maior_ocorrencia
        )


    # ======================================
    # INFO GERAL
    # ======================================

    st.info(f"""

📅 PERÍODO ANALISADO:
{data_inicio} até {data_fim}

📊 Velas analisadas:
{dias_total}

📈 Tamanho da camada:
R$ {spread_alvo}

🎯 Camada dominante:
R$ {camada_inicio} → R$ {camada_fim}

📌 Frequência:
{maior_ocorrencia} ocorrências

🔺 {ativo1} ficou mais caro em:
{freq_ativo1:.2f}% do período

🔻 {ativo2} ficou mais caro em:
{freq_ativo2:.2f}% do período

🎯 Ocorrência dentro da camada alvo:
{percentual_ocorrencias:.2f}%

""")

    # ======================================
    # DISTRIBUIÇÃO DA DISTÂNCIA
    # ======================================

    fig_hist = go.Figure()

    fig_hist.add_trace(

        go.Histogram(

            x=spread,

            xbins=dict(
                start=distancia_minima,
                end=distancia_maxima,
                size=spread_alvo
            ),

            marker=dict(

                color="orange",

                line=dict(
                    color="#ffb347",
                    width=1
                )

            ),

            opacity=0.90

        )

    )

    fig_hist.add_vline(

        x=media,

        line_dash="dash",

        line_color="red",

        annotation_text="Média",

        annotation_position="top"

    )

    fig_hist.add_vline(

        x=spread_atual,

        line_dash="solid",

        line_color="yellow",

        annotation_text="Atual",

        annotation_position="top"

    )

    fig_hist.add_vrect(

        x0=(media - desvio),

        x1=(media + desvio),

        fillcolor="orange",

        opacity=0.08,

        line_width=0

    )

    fig_hist.update_layout(

        template="plotly_dark",

        title="Distribuição da Distância entre os Ativos",

        height=650,

        bargap=0.05,

        xaxis_title="Faixas de Distância (R$)",

        yaxis_title="Ocorrências",

        showlegend=False

    )

    st.plotly_chart(
        fig_hist,
        use_container_width=True,
        key=f"histograma_{ativo1}_{ativo2}"
    )

    # ======================================
    # MAPA DE CONCENTRAÇÃO
    # ======================================

    st.markdown("---")

    st.subheader("🔥 Mapa de Concentração Institucional")

    zonas_df = pd.DataFrame({

        "Faixa Inicial": edges[:-1],

        "Faixa Final": edges[1:],

        "Ocorrências": hist

    })

    zonas_df["Percentual"] = (

        zonas_df["Ocorrências"]
        /
        zonas_df["Ocorrências"].sum()

    ) * 100

    zonas_df["Zona"] = (

        zonas_df["Faixa Inicial"]
        .round(2)
        .astype(str)

        +

        " → "

        +

        zonas_df["Faixa Final"]
        .round(2)
        .astype(str)

    )

    zonas_df["Score"] = (

        zonas_df["Percentual"]
        *
        zonas_df["Ocorrências"]

    ).round(2)

    zonas_df = zonas_df.sort_values(
        by="Score",
        ascending=False
    )

    st.dataframe(

        zonas_df[
            [
                "Zona",
                "Ocorrências",
                "Percentual",
                "Score"
            ]
        ].head(10),

        use_container_width=True

    )

    fig_heat = px.bar(

        zonas_df.head(15),

        x="Percentual",

        y="Zona",

        orientation="h",

        text="Percentual",

        height=600

    )

    fig_heat.update_layout(

        template="plotly_dark",

        title="Mapa de Concentração das Camadas",

        yaxis_title="Zonas",

        xaxis_title="% Concentração"

    )

    st.plotly_chart(
        fig_heat,
        use_container_width=True,
        key=f"heatmap_{ativo1}_{ativo2}"
    )

    # ======================================
    # PERMANÊNCIA TEMPORAL
    # ======================================

    st.markdown("---")

    st.subheader("⏳ Permanência Temporal das Camadas")

    zonas_tempo = pd.cut(
        spread,
        bins=bins,
        include_lowest=True
    )

    permanencias = []

    zona_atual = None

    contador = 0

    for zona in zonas_tempo:

        if zona == zona_atual:

            contador += 1

        else:

            if zona_atual is not None:

                permanencias.append({

                    "Zona": str(zona_atual),

                    "Tempo": contador

                })

            zona_atual = zona

            contador = 1

    permanencias.append({

        "Zona": str(zona_atual),

        "Tempo": contador

    })

    permanencia_df = pd.DataFrame(
        permanencias
    )

    permanencia_stats = (

        permanencia_df
        .groupby("Zona")["Tempo"]
        .agg(
            [
                "mean",
                "max",
                "count"
            ]
        )
        .reset_index()

    )

    permanencia_stats.columns = [

        "Zona",
        "Tempo Médio",
        "Tempo Máximo",
        "Ocorrências"

    ]

    permanencia_stats["Score Temporal"] = (

        permanencia_stats["Tempo Médio"]
        *
        permanencia_stats["Ocorrências"]

    ).round(2)

    permanencia_stats = permanencia_stats.sort_values(
        by="Score Temporal",
        ascending=False
    )

    # ======================================
    # SCORE DE REVERSÃO INSTITUCIONAL
    # ======================================

    # --------------------------------------
    # SCORE CORRELAÇÃO
    # Peso: 20
    # --------------------------------------

    score_correlacao = min(
        correlacao * 20,
        20
    )

    # --------------------------------------
    # SCORE COINTEGRAÇÃO
    # Peso: 25
    # --------------------------------------

    if pvalue <= 0.05:

        score_cointegracao = 25

    elif pvalue <= 0.10:

        score_cointegracao = 18

    elif pvalue <= 0.20:

        score_cointegracao = 10

    elif pvalue <= 0.30:

        score_cointegracao = 5

    else:

        score_cointegracao = 0

    # --------------------------------------
    # SCORE ZSCORE
    # Peso: 25
    # --------------------------------------

    score_zscore = min(
        abs(ultimo_z) * 10,
        25
    )

    # --------------------------------------
    # SCORE FREQUÊNCIA HISTÓRICA
    # Peso: 15
    # --------------------------------------

    score_frequencia = min(
        percentual_ocorrencias,
        15
    )

    # --------------------------------------
    # SCORE TEMPORAL
    # Peso: 15
    # --------------------------------------

    tempo_medio_global = (

        permanencia_stats[
            "Tempo Médio"
        ].mean()

    )

    score_tempo = min(
        tempo_medio_global,
        15
    )

    # --------------------------------------
    # SCORE FINAL
    # --------------------------------------

    score_reversao = (

        score_correlacao
        +
        score_cointegracao
        +
        score_zscore
        +
        score_frequencia
        +
        score_tempo

    )

    score_reversao = min(
        round(score_reversao, 2),
        100
    )

    # ======================================
    # CARD SCORE INSTITUCIONAL
    # ======================================

    st.markdown("---")

    st.subheader(
        "🧠 Score Institucional"
    )

    col_score1, col_score2 = st.columns([1,1])

    with col_score1:

        st.metric(
            "🧠 Reversão Score",
            f"{score_reversao}/100"
        )

    with col_score2:

        if score_reversao >= 80:

            st.success(
                "🔥 SETUP INSTITUCIONAL FORTE"
            )

        elif score_reversao >= 60:

            st.warning(
                "⚠️ SETUP MODERADO"
            )

        else:

            st.error(
                "❌ SETUP FRACO"
            )

    # ======================================
    # DETALHAMENTO DOS SCORES
    # ======================================

    score_df = pd.DataFrame({

        "Fator": [

            "Correlação",
            "Cointegração",
            "Z-Score",
            "Frequência",
            "Tempo"

        ],

        "Score": [

            round(score_correlacao, 2),
            round(score_cointegracao, 2),
            round(score_zscore, 2),
            round(score_frequencia, 2),
            round(score_tempo, 2)

        ]

    })

    st.dataframe(
        score_df,
        use_container_width=True
    )

    # ======================================
    # GRÁFICO DOS SCORES
    # ======================================

    fig_score = px.bar(

        score_df,

        x="Fator",

        y="Score",

        text="Score",

        height=500

    )

    fig_score.update_layout(

        template="plotly_dark",

        title="Composição do Reversão Score",

        yaxis_title="Pontuação",

        xaxis_title="Fatores"

    )

    st.plotly_chart(
        fig_score,
        use_container_width=True,
        key=f"score_{ativo1}_{ativo2}"
    )

    st.dataframe(

        permanencia_stats.head(15),

        use_container_width=True

    )

    fig_tempo = px.bar(

        permanencia_stats.head(15),

        x="Tempo Médio",

        y="Zona",

        orientation="h",

        text="Tempo Médio",

        height=650

    )

    fig_tempo.update_layout(

        template="plotly_dark",

        title="Tempo Médio de Permanência por Zona",

        yaxis_title="Zona",

        xaxis_title="Candles Médios"

    )

    st.plotly_chart(
        fig_tempo,
        use_container_width=True,
        key=f"tempo_{ativo1}_{ativo2}"
    )

    # ======================================
    # HEATMAP OPERACIONAL
    # ======================================

    st.markdown("---")

    st.subheader("🔥 Heatmap Operacional Institucional")

    heatmap_df = zonas_df.copy()

    heatmap_df = heatmap_df.merge(

        permanencia_stats[
            [
                "Zona",
                "Tempo Médio",
                "Tempo Máximo",
                "Ocorrências"
            ]
        ],

        on="Zona",

        how="left"

    )

    heatmap_df["Score Operacional"] = (

        heatmap_df["Percentual"]
        *
        heatmap_df["Tempo Médio"]

    ).round(2)

    heatmap_df = heatmap_df.sort_values(
        by="Score Operacional",
        ascending=False
    )

    st.dataframe(

        heatmap_df[
            [
                "Zona",
                "Percentual",
                "Tempo Médio",
                "Tempo Máximo",
                "Score Operacional"
            ]
        ].head(15),

        use_container_width=True

    )

    fig_operacional = px.density_heatmap(

        heatmap_df.head(20),

        x="Percentual",

        y="Tempo Médio",

        z="Score Operacional",

        text_auto=True,

        height=700

    )

    fig_operacional.update_layout(

        template="plotly_dark",

        title="Mapa de Intensidade Operacional",

        xaxis_title="% Concentração",

        yaxis_title="Tempo Médio"

    )

    st.plotly_chart(
        fig_operacional,
        use_container_width=True,
        key=f"operacional_{ativo1}_{ativo2}"
    )

    # ======================================
    # PREÇOS
    # ======================================

    fig1 = go.Figure()

    fig1.add_trace(
        go.Scatter(
            x=dados.index,
            y=serie1,
            name=ativo1,
            line=dict(color="orange")
        )
    )

    fig1.add_trace(
        go.Scatter(
            x=dados.index,
            y=serie2,
            name=ativo2
        )
    )

    fig1.update_layout(
        title="Preços",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig1,
        use_container_width=True,
        key=f"precos_{ativo1}_{ativo2}"
    )


    # ======================================
    # SPREAD
    # ======================================

    fig2 = go.Figure()

    fig2.add_trace(
        go.Scatter(
            x=spread.index,
            y=spread,
            name="Distância",
            line=dict(color="orange")
        )
    )

    fig2.add_hline(
        y=media,
        line_color="yellow",
        line_dash="dash"
    )

    fig2.update_layout(
        title="Distância entre os Ativos",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig2,
        use_container_width=True,
        key=f"spread_{ativo1}_{ativo2}"
    )

    # ======================================
    # ZSCORE
    # ======================================

    fig3 = go.Figure()

    fig3.add_trace(
        go.Scatter(
            x=zscore.index,
            y=zscore,
            name="Z-Score",
            line=dict(color="orange")
        )
    )

    fig3.add_hline(
        y=2,
        line_color="red",
        line_dash="dash"
    )

    fig3.add_hline(
        y=-2,
        line_color="green",
        line_dash="dash"
    )

    fig3.add_hline(
        y=0,
        line_color="white",
        line_dash="dot"
    )

    fig3.update_layout(
        title="Z-Score",
        template="plotly_dark",
        height=500
    )

    st.plotly_chart(
        fig3,
        use_container_width=True,
        key=f"zscore_{ativo1}_{ativo2}"
    )

except Exception as erro:

    st.error(
        f"Erro: {erro}"
    )

# ==========================================
# SCANNER
# ==========================================

if executar_scan:

    st.markdown("---")

    st.header(
        "🚀 Ranking Quantitativo B3"
    )

    with st.spinner(
        "Analisando pares..."
    ):

        try:

            df_scan = executar_scanner(

                lista_ativos=LISTA_ATIVOS,

                periodo=periodo,

                correlacao_minima=0.70,

                pvalue_maximo=0.05

            )

            if len(df_scan) == 0:

                st.warning(
                    "Nenhum par encontrado."
                )

            else:

                st.success(
                    f"{len(df_scan)} pares encontrados"
                )

                st.dataframe(
                    df_scan.head(20),
                    use_container_width=True
                )

        except Exception as erro:

            st.error(
                f"Erro Scanner: {erro}"
            )
