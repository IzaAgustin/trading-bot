import os
import pandas as pd

def validar_y_corregir_csv(ruta_archivo):
    try:
        df = pd.read_csv(ruta_archivo)

        if "ordenes" in ruta_archivo:
            columnas_esperadas = ["timestamp", "cripto", "exchange_origen", "precio_origen",
                                  "exchange_destino", "precio_destino", "ganancia", "diferencia_pct"]
        elif "historial" in ruta_archivo:
            columnas_esperadas = ["timestamp", "precio", "ganancia"]
        else:
            columnas_esperadas = df.columns.tolist()

        if len(df.columns) != len(columnas_esperadas):
            df.columns = columnas_esperadas[:len(df.columns)]

        df.dropna(how='all', inplace=True)
        df.to_csv(ruta_archivo, index=False)
        return f"✅ {ruta_archivo} corregido correctamente."
    except Exception as e:
        return f"❌ Error al procesar {ruta_archivo}: {e}"

def validar_csvs_en_directorio(directorio="."):
    salida = "🔍 Validando archivos CSV...\n"
    for archivo in os.listdir(directorio):
        if archivo.endswith(".csv"):
            ruta_completa = os.path.join(directorio, archivo)
            try:
                salida += validar_y_corregir_csv(ruta_completa) + "\n"
            except Exception as e:
                salida += f"❌ Error al procesar {ruta_completa}: {e}\n"
    salida += "🧹 Validación completa."
    return salida
