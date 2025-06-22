import requests
import pandas as pd
import time
from datetime import datetime

# Lista de criptomonedas y exchanges
criptos = ['BTC', 'ETH', 'BNB', 'SOL', 'ADA', 'XRP', 'DOGE', 'DOT', 'MATIC', 'SHIB']
exchanges = ['binance', 'kucoin', 'coinbase', 'kraken', 'coingecko']

# Funciones para obtener precios

def get_price_binance(symbol):
    try:
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
        r = requests.get(url).json()
        return float(r['price'])
    except:
        return None

def get_price_kucoin(symbol):
    try:
        url = f"https://api.kucoin.com/api/v1/market/orderbook/level1?symbol={symbol}-USDT"
        r = requests.get(url).json()
        return float(r['data']['price'])
    except:
        return None

def get_price_coinbase(symbol):
    try:
        url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
        r = requests.get(url).json()
        return float(r['data']['amount'])
    except:
        return None

def get_price_kraken(symbol):
    try:
        symbol_map = {'BTC': 'XBT', 'ETH': 'ETH', 'BNB': 'BNB', 'SOL': 'SOL', 'ADA': 'ADA', 'XRP': 'XRP', 'DOGE': 'DOGE', 'DOT': 'DOT', 'MATIC': 'MATIC', 'SHIB': 'SHIB'}
        kraken_symbol = symbol_map.get(symbol, symbol) + 'USD'
        url = f"https://api.kraken.com/0/public/Ticker?pair={kraken_symbol}"
        r = requests.get(url).json()
        key = list(r['result'].keys())[0]
        return float(r['result'][key]['c'][0])
    except:
        return None

def get_price_coingecko(symbol):
    try:
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
        r = requests.get(url).json()
        return float(r[symbol.lower()]['usd'])
    except:
        return None

# Diccionario de funciones
funciones = {
    'binance': get_price_binance,
    'kucoin': get_price_kucoin,
    'coinbase': get_price_coinbase,
    'kraken': get_price_kraken,
    'coingecko': get_price_coingecko
}

# Función principal de arbitraje
def detectar_arbitraje():
    oportunidades = []
    for cripto in criptos:
        precios = {}
        for ex in exchanges:
            precio = funciones[ex](cripto)
            if precio:
                precios[ex] = precio
        if len(precios) >= 2:
            min_ex = min(precios, key=precios.get)
            max_ex = max(precios, key=precios.get)
            spread = precios[max_ex] - precios[min_ex]
            if spread > 10:
                oportunidades.append({
                    'timestamp': datetime.now(),
                    'cripto': cripto,
                    'exchange_origen': min_ex,
                    'precio_origen': precios[min_ex],
                    'exchange_destino': max_ex,
                    'precio_destino': precios[max_ex],
                    'spread': spread,
                    'ganancia_estim': round(spread / precios[min_ex] * 100, 2)
                })
    if oportunidades:
        df = pd.DataFrame(oportunidades)
        df.to_csv("ordenes.csv", mode='a', header=not pd.read_csv("ordenes.csv").shape[0], index=False)
        print("Oportunidades detectadas y registradas ✔")
    else:
        print("Sin oportunidades de arbitraje en este ciclo ❌")

# Ejecutar cada 60 segundos
if __name__ == "__main__":
    while True:
        detectar_arbitraje()
        time.sleep(60)
