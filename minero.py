import ollama
import csv

print("⚙️  Iniciando proceso ETL (Extract, Transform, Load)...")

# 1. Abrimos el archivo ORIGINAL en modo lectura ('r')
with open('datos.csv', 'r') as archivo_entrada:
    lector = csv.DictReader(archivo_entrada)
    
    # 2. Creamos el archivo NUEVO en modo escritura ('w')
    with open('reporte_final.csv', 'w', newline='') as archivo_salida:
        # Definimos las columnas del nuevo Excel (Añadimos 'Sentimiento')
        campos = ['ID', 'Comentario', 'Sentimiento']
        escritor = csv.DictWriter(archivo_salida, fieldnames=campos)
        
        # Escribimos el encabezado en el archivo nuevo
        escritor.writeheader()
        
        print("🚀 Procesando filas y guardando en disco...")
        
        for fila in lector:
            texto = fila['Comentario']
            
            # --- Aquí ocurre la Magia (IA) ---
            respuesta = ollama.chat(model='llama3.2', messages=[
                {'role': 'system', 'content': 'Clasifica en: POSITIVO, NEGATIVO o NEUTRAL. Solo una palabra.'},
                {'role': 'user', 'content': texto},
            ])
            sentimiento_detectado = respuesta['message']['content'].strip()
            # ---------------------------------
            
            # Guardamos la fila completa + el sentimiento en el archivo nuevo
            escritor.writerow({
                'ID': fila['ID'],
                'Comentario': texto,
                'Sentimiento': sentimiento_detectado
            })
            
            print(f"✅ ID {fila['ID']} procesado -> {sentimiento_detectado}")

print("\n🎉 ¡Listo! Revisa el archivo 'reporte_final.csv'.")
