import pandas as pd
import plotly.graph_objects as go

def graficar_analisis_tecnico(activo):
    try:
        df = pd.read_csv("precios.csv")
        df = df[df["activo"] == activo].copy()

        df["SMA_7"] = df["precio_cierre"].rolling(window=7).mean()
        df["SMA_21"] = df["precio_cierre"].rolling(window=21).mean()
        df["EMA_7"] = df["precio_cierre"].ewm(span=7, adjust=False).mean()
        df["EMA_21"] = df["precio_cierre"].ewm(span=21, adjust=False).mean()

        delta = df["precio_cierre"].diff()
        ganancia = delta.where(delta > 0, 0)
        perdida = -delta.where(delta < 0, 0)
        media_ganancia = ganancia.rolling(window=14).mean()
        media_perdida = perdida.rolling(window=14).mean()
        rs = media_ganancia / media_perdida
        df["RSI"] = 100 - (100 / (1 + rs))

        fig = go.Figure()

        fig.add_trace(go.Candlestick(
            x=df["timestamp"],
            open=df["precio_apertura"],
            high=df["precio_alto"],
            low=df["precio_bajo"],
            close=df["precio_cierre"],
            name="Velas"
        ))

        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["SMA_7"], line=dict(color='blue'), name="SMA 7"))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["SMA_21"], line=dict(color='orange'), name="SMA 21"))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["EMA_7"], line=dict(color='green'), name="EMA 7"))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["EMA_21"], line=dict(color='red'), name="EMA 21"))
        fig.add_trace(go.Scatter(x=df["timestamp"], y=df["RSI"], line=dict(color='purple'), name="RSI", yaxis="y2"))

        fig.update_layout(
            title=f"📊 Análisis Técnico - {activo}",
            xaxis_title="Tiempo",
            yaxis_title="Precio",
            yaxis2=dict(
                title="RSI",
                overlaying="y",
                side="right",
                showgrid=False
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )

        return fig
    except Exception as e:
        print(f"⚠️ Error en análisis técnico: {e}")
        return None


