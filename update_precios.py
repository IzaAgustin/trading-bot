import time
import pandas as pd
import random
from datetime import datetime

def generar_precios_simulados():
    activos = ["BTC", "ETH", "BNB", "SOL", "ADA", "XRP", "DOGE", "AVAX", "MATIC", "DOT"]
    datos = []

    for activo in activos:
        for i in range(40):
            base = random.uniform(1, 100)
            apertura = round(base, 2)
            alto = round(base + random.uniform(0.1, 5), 2)
            bajo = round(base - random.uniform(0.1, 5), 2)
            cierre = round(random.uniform(bajo, alto), 2)
            volumen = round(random.uniform(1000, 10000), 2)
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            datos.append([timestamp, activo, apertura, alto, bajo, cierre, volumen])

    df = pd.DataFrame(datos, columns=["timestamp", "activo", "precio_apertura", "precio_alto", "precio_bajo", "precio_cierre", "volumen"])
    df.to_csv("precios.csv", index=False)
    print(f"✅ precios.csv actualizado: {datetime.now().strftime('%H:%M:%S')}")

while True:
    generar_precios_simulados()
    time.sleep(60)
