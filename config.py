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
