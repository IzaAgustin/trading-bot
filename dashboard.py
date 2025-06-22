import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import os
import requests
import time
from threading import Thread

# Variables globales para asegurar carga dinámica del selector
cripto_selector = None
ultima_data = None

# Lista de criptos predefinidas
CRIPTOS = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "XRPUSDT", "ADAUSDT", "SOLUSDT", "DOGEUSDT", "AVAXUSDT", "MATICUSDT", "DOTUSDT"]

# Función: cargar historial y graficar precio + ganancia
def generar_grafico_general():
    archivo = "historial.csv"
    if not os.path.exists(archivo):
        return go.Figure().update_layout(title="Archivo historial.csv no encontrado")

    df = pd.read_csv(archivo, header=None)
    if df.shape[1] < 3:
        return go.Figure().update_layout(title="Se requieren al menos 3 columnas: timestamp, precio, ganancia")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[1], mode='lines+markers', name='Precio'))
    fig.add_trace(go.Scatter(x=df.index, y=df[2], mode='lines', name='Ganancia'))
    fig.update_layout(title='📈 Rendimiento General', xaxis_title='Operación', yaxis_title='Valor')
    return fig

# Función: gráfico solo de análisis técnico
def generar_analisis_tecnico():
    archivo = "historial.csv"
    if not os.path.exists(archivo):
        return go.Figure().update_layout(title="Archivo historial.csv no encontrado")

    df = pd.read_csv(archivo, header=None)
    if df.shape[1] < 2:
        return go.Figure().update_layout(title="El archivo no tiene suficientes columnas")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df[1], mode='lines+markers', name='Precio'))
    fig.update_layout(title='📊 Análisis Técnico Interactivo', xaxis_title='Operación', yaxis_title='Precio')
    return fig

# Función: mostrar tabla completa de órdenes
def mostrar_tabla():
    archivo = "ordenes.csv"
    if not os.path.exists(archivo):
        return pd.DataFrame()
    return pd.read_csv(archivo)

# Función: generar métricas
def generar_metrica():
    archivo = "ordenes.csv"
    if not os.path.exists(archivo):
        return pd.DataFrame({"Métrica": ["Sin datos"], "Valor": ["-"]})
    df = pd.read_csv(archivo)
    total = len(df)
    ganadoras = df[df['ganancia'] > 0].shape[0] if 'ganancia' in df.columns else 0
    perdedoras = df[df['ganancia'] <= 0].shape[0] if 'ganancia' in df.columns else 0
    ganancia_total = df['ganancia'].sum() if 'ganancia' in df.columns else 0
    efectividad = (ganadoras / total * 100) if total > 0 else 0
    resumen = pd.DataFrame({
        "Métrica": ["Órdenes Totales", "Ganadoras", "Perdedoras", "Ganancia Neta", "Efectividad %"],
        "Valor": [total, ganadoras, perdedoras, round(ganancia_total, 2), f"{round(efectividad,2)} %"]
    })
    return resumen

# Función: filtrar por criptomoneda
def filtrar_por_cripto(cripto):
    archivo = "ordenes.csv"
    if not os.path.exists(archivo):
        return pd.DataFrame()
    df = pd.read_csv(archivo)
    if cripto == "Todas":
        return df
    return df[df['cripto'] == cripto]

# Función auxiliar para lista de criptos
def obtener_criptos():
    archivo = "ordenes.csv"
    if not os.path.exists(archivo):
        return ["Todas"] + CRIPTOS
    df = pd.read_csv(archivo)
    if 'cripto' not in df.columns:
        return ["Todas"] + CRIPTOS
    criptos = ["Todas"] + sorted(df['cripto'].dropna().unique().astype(str).tolist())
    if cripto_selector:
        cripto_selector.choices = criptos
    return criptos

# Gráfico de velas japonesas en tiempo real
def obtener_velas():
    url = f"https://api.binance.com/api/v3/klines?symbol=BTCUSDT&interval=1m&limit=50"
    try:
        response = requests.get(url)
        data = response.json()
        df = pd.DataFrame(data, columns=["timestamp", "o", "h", "l", "c", "v", "c2", "q", "n", "taker_buy_base", "taker_buy_quote", "ignore"])
        df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
        fig = go.Figure(data=[go.Candlestick(x=df['timestamp'], open=df['o'].astype(float), high=df['h'].astype(float),
                                             low=df['l'].astype(float), close=df['c'].astype(float))])
        fig.update_layout(title="💹 Velas Japonesas BTC/USDT (1m)", xaxis_title="Tiempo", yaxis_title="Precio")
        return fig
    except:
        return go.Figure().update_layout(title="Error al cargar datos desde Binance")

# UI con Gradio
with gr.Blocks(title="📊 Dashboard Completo Trading IA") as demo:
    gr.Markdown("# 🤖 Dashboard de Trading Autónomo con IA")

    with gr.Tab("📈 Gráfico General"):
        graf_general = gr.Plot()
        boton_grafico = gr.Button("🔁 Actualizar Gráfico General")
        boton_grafico.click(fn=generar_grafico_general, outputs=graf_general)

    with gr.Tab("📊 Análisis Técnico"):
        graf_analisis = gr.Plot()
        boton_analisis = gr.Button("📉 Ver Análisis Técnico")
        boton_analisis.click(fn=generar_analisis_tecnico, outputs=graf_analisis)

    with gr.Tab("📋 Tabla de Órdenes + Filtro"):
        cripto_selector = gr.Dropdown(choices=obtener_criptos(), label="Filtrar por Criptomoneda")
        tabla_filtrada = gr.Dataframe()
        cripto_selector.change(fn=filtrar_por_cripto, inputs=cripto_selector, outputs=tabla_filtrada)

    with gr.Tab("📊 Métricas del Sistema"):
        tabla_metrica = gr.Dataframe()
        boton_metrica = gr.Button("📊 Ver Métricas Generales")
        boton_metrica.click(fn=generar_metrica, outputs=tabla_metrica)

    with gr.Tab("📉 Velas Japonesas Tiempo Real"):
        graf_velas = gr.Plot()
        def actualizar_auto():
            while True:
                time.sleep(10)
                with demo:
                    graf_velas.update(obtener_velas())
        Thread(target=actualizar_auto, daemon=True).start()
        graf_velas.render()

if __name__ == "__main__":
    demo.launch()
