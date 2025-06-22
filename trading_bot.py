import time
import pandas as pd
from config import CRYPTO_LIST, INTERVALO_ANALISIS
from simulador import Simulador

class TradingBot:
    def __init__(self):
        self.simulador = Simulador()
        self.historial = []
        self.ordenes = []

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
        print("🚀 Iniciando bot de trading...")
        for i in range(3):  # solo 3 ciclos para test
            print(f"🔁 Ciclo {i + 1}")
            df = self.analizar_mercado()

            ahora = pd.Timestamp.now()
            df["fecha_hora"] = ahora
            self.historial.append(df)
            print("✅ Historial actualizado")

            ordenes = self.simulador.simular_compra(df)
            self.ordenes.append(pd.DataFrame(ordenes))
            print(f"🧪 Ordenes simuladas: {len(ordenes)}")

            pd.concat(self.historial).to_csv("historial.csv", index=False)
            pd.concat(self.ordenes).to_csv("ordenes.csv", index=False)
            print("📁 Archivos actualizados: historial.csv y ordenes.csv")

            time.sleep(3)

        print("🏁 Bot finalizó los ciclos de prueba.")

