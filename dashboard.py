import gradio as gr
import pandas as pd

# Funciones de ejemplo — reemplazalas por las tuyas reales
def obtener_criptos():
    return ["BTC", "ETH", "BNB", "SOL", "ADA"]

def filtrar_por_cripto(cripto):
    # Simulación: cargá tus datos reales acá
    df = pd.read_csv("precios.csv")
    return df[df["cripto"] == cripto]

def generar_analisis_tecnico():
    return pd.DataFrame({"Indicador": ["RSI", "MACD"], "Valor": [45.2, 0.87]})

def generar_metrica():
    return pd.DataFrame({"Métrica": ["Ganancia Total", "Órdenes ejecutadas"], "Valor": ["+12.4%", 134]})

# Interfaz Gradio con pestañas
with gr.Blocks() as interface:
    with gr.Tab("📈 Análisis Técnico"):
        graf_analisis = gr.Dataframe()
        boton_analisis = gr.Button("📊 Ver Análisis Técnico")
        boton_analisis.click(fn=generar_analisis_tecnico, outputs=graf_analisis)

    with gr.Tab("📋 Tabla de Órdenes + Filtro"):
        cripto_selector = gr.Dropdown(choices=obtener_criptos(), label="Filtrar por Criptomoneda")
        tabla_filtrada = gr.Dataframe()
        cripto_selector.change(fn=filtrar_por_cripto, inputs=cripto_selector, outputs=tabla_filtrada)

    with gr.Tab("📊 Métricas del Sistema"):
        tabla_metrica = gr.Dataframe()
        boton_metrica = gr.Button("📈 Ver Métricas Generales")
        boton_metrica.click(fn=generar_metrica, outputs=tabla_metrica)

# Esta línea es la clave
interface.launch(share=True)
