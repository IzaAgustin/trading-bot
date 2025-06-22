import gradio as gr
import pandas as pd
import plotly.graph_objects as go
import requests

# --- Simulaciones de funciones previas ---
def obtener_criptos():
    return ["BTC", "ETH", "ADA"]

def filtrar_por_cripto(cripto):
    df = pd.DataFrame({"Orden": ["Compra", "Venta"], "Cripto": [cripto, cripto], "Monto": [0.5, 0.8]})
    return df

def fn_analisis():
    df = pd.DataFrame({"Indicador": ["RSI", "MACD"], "Valor": [45.2, 0.87]})
    return df

def fn_generar_metrica():
    df = pd.DataFrame({"Métrica": ["Ganancia Total", "Órdenes Ejecutadas"], "Valor": [1500, 24]})
    return df

# --- Nueva función para gráfico de velas japonesas ---
def obtener_velas_japonesas():
    url = "https://api.binance.com/api/v3/klines"
    params = {
        "symbol": "BTCUSDT",
        "interval": "1m",
        "limit": 50
    }
    response = requests.get(url, params=params)
    data = response.json()

    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        "close_time", "quote_asset_volume", "trades", "taker_buy_base", "taker_buy_quote", "ignore"
    ])
    df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
    df[["open", "high", "low", "close"]] = df[["open", "high", "low", "close"]].astype(float)

    fig = go.Figure(data=[go.Candlestick(
        x=df["timestamp"],
        open=df["open"],
        high=df["high"],
        low=df["low"],
        close=df["close"],
        increasing_line_color='green',
        decreasing_line_color='red'
    )])

    fig.update_layout(title="BTC/USDT - Velas Japonesas (1m)",
                      xaxis_title="Tiempo",
                      yaxis_title="Precio (USDT)",
                      xaxis_rangeslider_visible=False)
    return fig

# --- Interfaz Gradio ---
with gr.Blocks() as interface:
    with gr.Tab("📊 Análisis Técnico"):
        tabla = gr.Dataframe()
        boton = gr.Button("📈 Ver Análisis Técnico")
        boton.click(fn=fn_analisis, outputs=tabla)

    with gr.Tab("📋 Tabla de Órdenes + Filtro"):
        cripto_selector = gr.Dropdown(choices=obtener_criptos(), label="Filtrar por Cripto")
        tabla_filtrada = gr.Dataframe()
        cripto_selector.change(fn=filtrar_por_cripto, inputs=cripto_selector, outputs=tabla_filtrada)

    with gr.Tab("📊 Métricas del Sistema"):
        tabla_metrica = gr.Dataframe()
        boton_metrica = gr.Button("📊 Ver Métricas Generales")
        boton_metrica.click(fn=fn_generar_metrica, outputs=tabla_metrica)

    with gr.Tab("📈 Gráfico de Velas"):
        grafico = gr.Plot()
        boton_grafico = gr.Button("📊 Ver Gráfico en Tiempo Real")
        boton_grafico.click(fn=obtener_velas_japonesas, outputs=grafico)

interface.launch(server_name="0.0.0.0", server_port=7860, share=True)
