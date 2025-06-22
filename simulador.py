class Simulador:
    def simular_compra(self, datos):
        ordenes = []
        for _, fila in datos.iterrows():
            ordenes.append({
                "activo": fila["symbol"],
                "monto": 100,
                "precio_estimado": 1.0,
                "resultado": "simulado"
            })
        return ordenes
