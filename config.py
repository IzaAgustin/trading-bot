# config.py
CRYPTO_LIST = ["BTC", "ETH", "BNB", "XRP", "ADA", "SOL", "DOT", "MATIC", "AVAX", "LTC"]
INTERVALO_ANALISIS = 300
MODO_REAL = True
MODO_SIMULACION = not MODO_REAL
APIS = {
    "coingecko": "https://api.coingecko.com/api/v3",
    "coinmarketcap": "https://pro-api.coinmarketcap.com",
    "lunarcrush": "https://api.lunarcrush.com/v2",
    "alternative": "https://api.alternative.me/fng/"
}
API_KEYS = {
    "coinmarketcap": "TU_API_KEY_AQUI",
    "lunarcrush": "TU_API_KEY_AQUI"
}
MIN_LIQUIDEZ_USDT = 100000
MAX_SLIPPAGE_PORCENTAJE = 0.5
ANALISIS_FUNDAMENTAL = True
ANALISIS_SENTIMIENTO = True
DETECCION_LIQUIDEZ = True
ANALISIS_TECNICO = True
EXPORTAR_LOGS = True
GUARDAR_RESULTADOS_EXCEL = True
