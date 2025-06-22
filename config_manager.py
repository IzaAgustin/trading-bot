import json

CONFIG_PATH = "config.json"

def cargar_config():
    try:
        with open(CONFIG_PATH, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {"intervalo_segundos": 10}
    except json.JSONDecodeError:
        print("⚠️ Error al leer config.json. Usando valores por defecto.")
        return {"intervalo_segundos": 10}

def guardar_config(nueva_config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(nueva_config, f, indent=4)
