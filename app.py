
import streamlit as st 
import yfinance as yf 
import pandas as pd 
import plotly.graph_objects as go 
import plotly.express as px
from auth import ( tela_login, tela_cadastro )

from scanner import ( executar_scanner )

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


if "menu" not in st.session_state:


    st.session_state["menu"] = "Painel"


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
    ],

    index=0 if st.session_state["menu"] == "Painel" else 1

)

st.session_state["menu"] = menu

st.markdown("---")

st.subheader("⚙️ Configurações")

ativo1_sidebar = st.selectbox(

    "Ativo 1",

    LISTA_ATIVOS,

    index=LISTA_ATIVOS.index(

        st.session_state.get(

            "ativo1",

            LISTA_ATIVOS[0]

        )

    ),

    key="ativo1_select"

)

ativo2_sidebar = st.selectbox(

    "Ativo 2",

    LISTA_ATIVOS,

    index=LISTA_ATIVOS.index(

        st.session_state.get(

            "ativo2",

            LISTA_ATIVOS[1]

        )

    ),

    key="ativo2_select"

)

periodo_sidebar = st.selectbox(

    "Período",

    [
        "3mo",
        "6mo",
        "1y",
        "200d"
    ],

    index=3,

    key="periodo_select"

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

if st.session_state["menu"] == "Painel":

    st.title("🏦 PAINEL SPREADS")

    ativo1 = ativo1_sidebar
    ativo2 = ativo2_sidebar
    periodo = periodo_sidebar

    try:

        dados = yf.download(

            [ativo1, ativo2],

            period=periodo,

            auto_adjust=True,

            progress=False

        )

        if isinstance(
        dados.columns,
        pd.MultiIndex
        ):

        dados = dados["Close"]

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

                                st.session_state["ativo1"] = row["Ativo 1"]

                                st.session_state["ativo2"] = row["Ativo 2"]

                                st.session_state["menu"] = "Painel"

                                st.rerun()

                    st.divider()

            except Exception as erro:

                st.error(f"Erro: {erro}")
