import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

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
    st.session_state["logado"] = True

if "usuario" not in st.session_state:
    st.session_state["usuario"] = "administrador"

if "menu" not in st.session_state:
    st.session_state["menu"] = "Painel"

# ==========================================
# ATIVOS
# ==========================================

LISTA_ATIVOS = [
    "VALE3.SA",
    "BRAP4.SA",
    "PETR4.SA",
    "PRIO3.SA",
    "ITUB4.SA",
    "BBDC4.SA",
    "TAEE11.SA",
    "EGIE3.SA"
]

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
        index=0
    )

    ativo2_sidebar = st.selectbox(
        "Ativo 2",
        LISTA_ATIVOS,
        index=1
    )

    periodo_sidebar = st.selectbox(
        "Período",
        ["3mo", "6mo", "1y", "200d"],
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

# ==========================================
# PAINEL
# ==========================================

if st.session_state["menu"] == "Painel":

    st.title("🏦 PAINEL SPREADS")

    try:

        dados = yf.download(
            [ativo1_sidebar, ativo2_sidebar],
            period=periodo_sidebar,
            auto_adjust=True,
            progress=False
        )

        if isinstance(dados.columns, pd.MultiIndex):
            dados = dados["Close"]

        dados = dados.dropna()

        if dados.empty:

           st.warning(
               "Sem dados disponíveis para este par."
           )

           st.stop()

        serie1 = dados[ativo1_sidebar]
        serie2 = dados[ativo2_sidebar]

        fator1 = lote1 / 100
        fator2 = lote2 / 100

        spread = (
            (serie1 * fator1)
            -
            (serie2 * fator2)
        )

        media = spread.mean()
        desvio = spread.std()

        zscore = 0

        if desvio != 0:
            zscore = (
                spread.iloc[-1]
                -
                media
            ) / desvio

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric(
                ativo1_sidebar,
                f"{serie1.iloc[-1]:.2f}"
            )

        with col2:
            st.metric(
                ativo2_sidebar,
                f"{serie2.iloc[-1]:.2f}"
            )

        with col3:
            st.metric(
                "Spread Atual",
                f"{spread.iloc[-1]:.2f}"
            )

        with col4:
            st.metric(
                "Pontuação Z",
                f"{zscore:.2f}"
            )

        st.markdown("---")

        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=spread.index,
                y=spread,
                mode="lines",
                name="Spread"
            )
        )

        fig.update_layout(
            template="plotly_dark",
            height=600,
            title="Spread Operacional"
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

elif st.session_state["menu"] == "Scanner":

    st.title("🚀 Scanner Quantitativo")

    st.info(
        "Scanner carregado com sucesso."
    )

    dados_scanner = pd.DataFrame({

        "Ativo 1": ["VALE3.SA", "PETR4.SA"],
        "Ativo 2": ["BRAP4.SA", "PRIO3.SA"],
        "Correlação": [0.99, 0.96],
        "Pontuação Z": [2.1, -2.3],
        "Status": [
            "🟢 Entrar Crédito",
            "🔴 Entrar Débito"
        ]

    })

    st.dataframe(
        dados_scanner,
        use_container_width=True
    )

    for idx, row in dados_scanner.iterrows():

        if st.button(
            f"📂 Abrir {idx}"
        ):

            st.session_state["menu"] = "Painel"

            st.rerun()
