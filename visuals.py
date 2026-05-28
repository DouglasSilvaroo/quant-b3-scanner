import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from config import *


# ==========================================
# HISTOGRAMA DE CAMADAS
# ==========================================

def render_histograma(

    spread,
    ativo1,
    ativo2,
    camada

):

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

📊 Candles analisados: {len(spread)}

📈 Tamanho da camada: R$ {camada}

🎯 Camada dominante: {camada_texto}

📌 Frequência: {freq.max()} ocorrências

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

        height=PLOT_HEIGHT,

        title="Distribuição da Distância entre os Ativos",

        xaxis_title="Faixas de Distância (R$)",

        yaxis_title="Ocorrências",

        bargap=0.03

    )

    st.plotly_chart(

        fig_hist,

        use_container_width=True

    )

    return freq

# ==========================================
# HEATMAP INSTITUCIONAL
# ==========================================

def render_heatmap(

    freq

):

    st.subheader(

        "🔥 Mapa de Concentração Institucional"

    )

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

    st.data_editor(

        df_tempo,

        use_container_width=True,

        disabled=True

    )

    fig_perm = px.pie(

        df_heatmap,

        x="Percentual",

        y="Zona",

        orientation="h",

        text="Percentual",

        template="plotly_dark"

    )

    fig_heat.update_layout(

        title="Mapa de Concentração das Camadas",

        height=500,

        yaxis=dict(

            autorange="reversed"

        )

    )

    st.plotly_chart(

        fig_heat,

        use_container_width=True

    )

# ==========================================
# PERMANÊNCIA TEMPORAL
# ==========================================

def render_permanencia(

    freq

):

    st.subheader(

        "⏳ Permanência Temporal das Camadas"

    )

    tabela_tempo = []

    total = int(freq.sum())

    for faixa, ocorrencias in freq.items():

        percentual = float(

            (ocorrencias / total) * 100

        )

        tabela_tempo.append({

            "Faixa": (
                f"{faixa.left:.2f} ➜ "
                f"{faixa.right:.2f}"
            ),

            "Candles": int(
                ocorrencias
            ),

            "Percentual": round(
                percentual,
                2
            )

        })

    df_tempo = pd.DataFrame(
        tabela_tempo
    )

    df_tempo = df_tempo.sort_values(

        by="Percentual",

        ascending=False

    )

    st.data_editor(

        df_heatmap,

        use_container_width=True,

        disabled=True

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

        height=500,

        yaxis=dict(

            autorange="reversed"

        )

    )

    st.plotly_chart(

        fig_heat,

        use_container_width=True

    )    

# ==========================================
# ZSCORE INSTITUCIONAL
# ==========================================

def render_zscore(

    spread,
    media,
    desvio

):

    st.subheader(

        "📉 Estrutura Estatística do Spread"

    )

    banda_1_sup = media + desvio
    banda_1_inf = media - desvio

    banda_2_sup = media + (desvio * 2)
    banda_2_inf = media - (desvio * 2)

    fig_z = go.Figure()

    fig_z.add_trace(

        go.Scatter(

            x=spread.index,

            y=spread,

            mode="lines",

            name="Spread",

            line=dict(

                color="#00c853",

                width=2

            )

        )

    )

    fig_z.add_trace(

        go.Scatter(

            x=spread.index,

            y=[media] * len(spread),

            mode="lines",

            name="Média",

            line=dict(

                color="white",

                dash="dash"

            )

        )

    )

    fig_z.add_trace(

        go.Scatter(

            x=spread.index,

            y=[banda_1_sup] * len(spread),

            mode="lines",

            name="+1 Desvio",

            line=dict(

                color="yellow",

                dash="dot"

            )

        )

    )

    fig_z.add_trace(

        go.Scatter(

            x=spread.index,

            y=[banda_1_inf] * len(spread),

            mode="lines",

            name="-1 Desvio",

            line=dict(

                color="yellow",

                dash="dot"

            )

        )

    )

    fig_z.add_trace(

        go.Scatter(

            x=spread.index,

            y=[banda_2_sup] * len(spread),

            mode="lines",

            name="+2 Desvios",

            line=dict(

                color="red",

                dash="dash"

            )

        )

    )

    fig_z.add_trace(

        go.Scatter(

            x=spread.index,

            y=[banda_2_inf] * len(spread),

            mode="lines",

            name="-2 Desvios",

            line=dict(

                color="red",

                dash="dash"

            )

        )

    )

    fig_z.update_layout(

        template="plotly_dark",

        height=PLOT_HEIGHT_BIG,

        title="Estrutura Estatística do Spread",

        xaxis_title="Data",

        yaxis_title="Spread"

    )

    st.plotly_chart(

        fig_z,

        use_container_width=True

    )

# ==========================================
# STATUS OPERACIONAL
# ==========================================

def render_status_operacional(

    zscore

):

    st.subheader(

        "🚦 Status Operacional"

    )

    if zscore >= 2:

        status = "🔴 VENDA SPREAD"

        cor = "error"

        descricao = (
            "Spread extremamente esticado para cima."
        )

    elif zscore <= -2:

        status = "🟢 COMPRA SPREAD"

        cor = "success"

        descricao = (
            "Spread extremamente descontado."
        )

    elif abs(zscore) >= 1:

        status = "🟡 ATENÇÃO"

        cor = "warning"

        descricao = (
            "Spread entrando em zona operacional."
        )

    else:

        status = "⚪ NEUTRO"

        cor = "info"

        descricao = (
            "Spread em equilíbrio estatístico."
        )

    c1, c2 = st.columns(

        [1, 3]

    )

    with c1:

        st.metric(

            "Z-Score",

            f"{zscore:.2f}"

        )

    with c2:

        if cor == "success":

            st.success(

                f"{status}\n\n{descricao}"

            )

        elif cor == "warning":

            st.warning(

                f"{status}\n\n{descricao}"

            )

        elif cor == "error":

            st.error(

                f"{status}\n\n{descricao}"

            )

        else:

            st.info(

                f"{status}\n\n{descricao}"

            )

# ==========================================
# DASHBOARD EXECUTIVO
# ==========================================

def render_dashboard_executivo(

    spread,
    media,
    desvio,
    zscore,
    half_life

):

    st.subheader(

        "📊 Dashboard Executivo Quantitativo"

    )

    volatilidade = float(

        spread.std()

    )

    amplitude = float(

        spread.max() - spread.min()

    )

    spread_max = float(
        spread.max()
    )

    spread_min = float(
        spread.min()
    )

    desvio_atual = float(

        spread.iloc[-1] - media

    )

    score_quant = float(

        abs(zscore) * volatilidade

    )

    c1, c2, c3 = st.columns(3)

    with c1:

        st.metric(

            "Volatilidade",

            f"{volatilidade:.2f}"

        )

        st.metric(

            "Amplitude",

            f"{amplitude:.2f}"

        )

    with c2:

        st.metric(

            "Spread Máximo",

            f"{spread_max:.2f}"

        )

        st.metric(

            "Spread Mínimo",

            f"{spread_min:.2f}"

        )

    with c3:

        st.metric(

            "Desvio Atual",

            f"{desvio_atual:.2f}"

        )

        st.metric(

            "Score Quant",

            f"{score_quant:.2f}"

        st.metric(

            "Half-Life",

            f"{half_life:.2f}"

        )


# ==========================================
# COINTEGRAÇÃO ROLLING
# ==========================================

def render_cointegracao_rolling(

    df_coint

):

    st.subheader(

        "🧠 Cointegração Rolling"

    )

    fig_coint = go.Figure()

    fig_coint.add_trace(

        go.Scatter(

            x=df_coint.index,

            y=df_coint["PValor"],

            mode="lines",

            name="P-Valor",

            line=dict(

                color="#00b0ff",

                width=2

            )

        )

    )

    fig_coint.add_hline(

        y=0.05,

        line_dash="dash",

        line_color="red"

    )

    fig_coint.update_layout(

        template="plotly_dark",

        height=500,

        title="Estabilidade Estatística do Par",

        xaxis_title="Data",

        yaxis_title="P-Valor"

    )

    st.plotly_chart(

        fig_coint,

        use_container_width=True

    )

    ultimo_pvalor = float(

        df_coint["PValor"].iloc[-1]

    )

    if ultimo_pvalor <= 0.05:

        st.success(

            f"Cointegração ATIVA | P-Valor: {ultimo_pvalor:.4f}"

        )

    else:

        st.error(

            f"Cointegração FRACA | P-Valor: {ultimo_pvalor:.4f}"

        )

# ==========================================
# REGIME ESTATÍSTICO
# ==========================================

def render_regime_estatistico(

    regime_info

):

    st.subheader(

        "📡 Regime Estatístico"

    )

    regime = regime_info["regime"]

    score = regime_info["score"]

    volatilidade = regime_info["volatilidade"]

    pvalor = regime_info["pvalor"]

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Score Regime",

            score

        )

    with c2:

        st.metric(

            "Volatilidade",

            f"{volatilidade:.2f}"

        )

    with c3:

        st.metric(

            "P-Valor",

            f"{pvalor:.4f}"

        )

    with c4:

        if "ESTÁVEL" in regime:

            st.success(regime)

        elif "MODERADO" in regime:

            st.warning(regime)

        else:

            st.error(regime)

# ==========================================
# SINAL OPERACIONAL
# ==========================================

def render_sinal(

    sinal_info

):

    st.subheader(

        "🚨 Engine de Sinais"

    )

    sinal = sinal_info["sinal"]

    confianca = sinal_info["confianca"]

    motivo = sinal_info["motivo"]

    c1, c2 = st.columns(

        [1, 3]

    )

    with c1:

        st.metric(

            "Confiança",

            f"{confianca}/4"

        )

    with c2:

        texto = "\n".join(

            motivo

        )

        if "BUY" in sinal:

            st.success(

                f"{sinal}\n\n{texto}"

            )

        elif "SELL" in sinal:

            st.error(

                f"{sinal}\n\n{texto}"

            )

        else:

            st.info(

                f"{sinal}\n\n{texto}"

            )

# ==========================================
# SCORE QUANT
# ==========================================

def render_score_quant(

    score_quant

):

    st.subheader(

        "🎯 Score Quantitativo"

    )

    if score_quant >= 80:

        st.success(

            f"🔥 SCORE INSTITUCIONAL: {score_quant}/100"

        )

    elif score_quant >= 60:

        st.warning(

            f"⚡ SCORE MODERADO: {score_quant}/100"

        )

    else:

        st.error(

            f"❌ SCORE FRACO: {score_quant}/100"

        )

    progresso = score_quant / 100

    st.progress(

        progresso

    )

# ==========================================
# BACKTEST
# ==========================================

def render_backtest(

    backtest_info

):

    st.subheader(

        "🧪 Backtest Operacional"

    )

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "Trades",

            backtest_info["trades"]

        )

    with c2:

        st.metric(

            "Win Rate",

            f"{backtest_info['winrate']}%"

        )

    with c3:

        st.metric(

            "Retorno Total",

            f"{backtest_info['retorno_total']:.2f}"

        )

    with c4:

        st.metric(

            "Retorno Médio",

            f"{backtest_info['retorno_medio']:.2f}"

        )

    if backtest_info["winrate"] >= 60:

        st.success(

            "Estratégia Estatisticamente Forte"

        )

    elif backtest_info["winrate"] >= 45:

        st.warning(

            "Estratégia Moderada"

        )

    else:

        st.error(

            "Estratégia Fraca"

        )

# ==========================================
# RISCO OPERACIONAL
# ==========================================

def render_risco_operacional(

    risco_info

):

    st.subheader(

        "🛡️ Risco Operacional"

    )

    risco = risco_info["risco"]

    nivel = risco_info["nivel"]

    c1, c2 = st.columns(

        [1, 3]

    )

    with c1:

        st.metric(

            "Risk Score",

            risco

        )

    with c2:

        if "BAIXO" in nivel:

            st.success(nivel)

        elif "MODERADO" in nivel:

            st.warning(nivel)

        else:

            st.error(nivel)

    progresso = min(

        risco / 10,
        1.0

    )

    st.progress(

        progresso

    )

    
