import csv

def validar_temperatura(valor):
    try:
        temperatura = float(valor)
        if -50 <= temperatura <= 100:
            return True, temperatura
        else:
            return False, None
    except ValueError:
        return False, None

# Listas para almacenar y clasificar la información
registros_validos = []
registros_rechazados = []
sumas_por_zona = {}
conteo_por_zona = {}
total_rechazados = 0

# 1. Leer el archivo CSV
with open('datos.csv', mode='r', encoding='utf-8') as archivo:
    lector = csv.DictReader(archivo)
    
    for fila in lector:
        sensor = fila['sensor']
        temp_raw = fila['temperatura']
        ubicacion = fila['ubicacion']
        
        # 2. Validar cada registro
        es_valido, temp_num = validar_temperatura(temp_raw)
        
        if es_valido:
            # Clasificar si la medición es alta (>= 35)
            clasificacion = "Alta" if temp_num >= 35 else "Normal"
            
            registro = {
                'sensor': sensor,
                'temperatura': temp_num,
                'ubicacion': ubicacion,
                'clasificacion': clasificacion
            }
            registros_validos.append(registro)
            
            # Acumular para el promedio por ubicación
            if ubicacion not in sumas_por_zona:
                sumas_por_zona[ubicacion] = 0.0
                conteo_por_zona[ubicacion] = 0
            
            sumas_por_zona[ubicacion] += temp_num
            conteo_por_zona[ubicacion] += 1
        else:
            registros_rechazados.append({
                'sensor': sensor,
                'temperatura': temp_raw,
                'ubicacion': ubicacion,
                'motivo': 'Temperatura inválida o fuera de rango'
            })
            total_rechazados += 1

# 3. Calcular y mostrar promedios por ubicación
print("=== INDICADORES Y RESULTADOS ===")
print(f"Total de registros rechazados: {total_rechazados}\n")

print("Promedio de temperatura por ubicación:")
for zona in sumas_por_zona:
    promedio = sumas_por_zona[zona] / conteo_por_zona[zona]
    print(f" - {zona}: {promedio:.2f} °C")

# 4. Generar archivo de válidos
with open('validos.csv', mode='w', newline='', encoding='utf-8') as f_validos:
    campos = ['sensor', 'temperatura', 'ubicacion', 'clasificacion']
    escritor = csv.DictWriter(f_validos, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(registros_validos)

# Generar archivo de rechazados
with open('rechazados.csv', mode='w', newline='', encoding='utf-8') as f_rechazados:
    campos = ['sensor', 'temperatura', 'ubicacion', 'motivo']
    escritor = csv.DictWriter(f_rechazados, fieldnames=campos)
    escritor.writeheader()
    escritor.writerows(registros_rechazados)

print("\nArchivos 'validos.csv' y 'rechazados.csv' generados con éxito.")