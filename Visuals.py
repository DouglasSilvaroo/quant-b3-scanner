import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


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
