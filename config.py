# ==========================================
# CONFIGURAÇÕES QUANTITATIVAS
# ==========================================

# ZSCORE

ZSCORE_ENTRY = 2
ZSCORE_ALERT = 1
ZSCORE_EXIT = 0.5

# CORRELAÇÃO

CORRELACAO_MIN = 0.80
CORRELACAO_FORTE = 0.90

# COINTEGRAÇÃO

PVALOR_LIMITE = 0.05
PVALOR_FORTE = 0.01

# HALF LIFE

HALF_LIFE_RAPIDO = 15
HALF_LIFE_MAX = 30
HALF_LIFE_LENTO = 50

# SCORE QUANT

SCORE_EXCELENTE = 80
SCORE_MODERADO = 60

# BACKTEST

WINRATE_FORTE = 60
WINRATE_MODERADO = 45

# CACHE

CACHE_TTL = 3600

# SCANNER

SCANNER_MIN_PERIODOS = 100

# VISUAL

PLOT_HEIGHT = 600
PLOT_HEIGHT_BIG = 700

# ==========================================
# MARKET DATA ENGINE
# ==========================================

MARKET_HISTORY_PERIOD = "5y"

MARKET_INTERVAL = "1d"

MARKET_MAX_RETRIES = 3

MARKET_RETRY_SLEEP = 5

MARKET_DOWNLOAD_SLEEP = 2

MARKET_BATCH_SIZE = 10

# ==========================================
# SUPABASE MARKET DATA
# ==========================================

MARKET_TABLE = "market_data"

# ==========================================
# UPDATE AUTOMÁTICO
# ==========================================

UPDATE_HOUR = 18

UPDATE_MINUTE = 10

# ==========================================
# PERFORMANCE
# ==========================================

DB_BATCH_INSERT = 500

MAX_ATIVOS_SCANNER = 200

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

