import time
import pandas as pd
from datetime import datetime
from simulador import Simulador
import config_manager  # ← Nuevo módulo

CRYPTO_LIST = ["BTC", "ETH", "BNB", "ADA", "SOL", "XRP", "DOT", "AVAX", "MATIC", "DOGE"]

class TradingBot:
    def __init__(self):
        self.historial = []
        self.ordenes = []
        self.simulador = Simulador()

    def analizar_mercado(self):
        datos = []
        for symbol in CRYPTO_LIST:
            datos.append({
                "symbol": symbol,
                "volumen_24h": 100000 + hash(symbol) % 50000,
                "slippage": round(hash(symbol) % 5 / 10, 2),
                "indice_miedo_codicia": 60
            })
        return pd.DataFrame(datos)

    def ejecutar(self):
        config = config_manager.cargar_config()
        intervalo = config.get("intervalo_segundos", 10)

        print("🚀 Iniciando bot de trading en tiempo real...")

        while True:
            print("🔄 Analizando mercado...")
            df = self.analizar_mercado()
            ahora = datetime.now()
            df["fecha_hora"] = ahora
            self.historial.append(df)

            print("📈 Historial actualizado.")
            ordenes = self.simulador.simular_compra(df)
            self.ordenes.append(pd.DataFrame(ordenes))
            print(f"📊 Órdenes simuladas: {len(ordenes)}")

            pd.concat(self.historial).to_csv("historial.csv", index=False)
            pd.concat(self.ordenes).to_csv("ordenes.csv", index=False)
            print("💾 Archivos actualizados: historial.csv y ordenes.csv\n")

            time.sleep(intervalo)

if __name__ == "__main__":
    bot = TradingBot()
    bot.ejecutar()
