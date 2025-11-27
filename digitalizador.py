import ollama
import json
import csv
import os

# Carpeta donde pondremos las fotos de las facturas
CARPETA_IMAGENES = "./facturas"

# Aseguramos que exista la carpeta
if not os.path.exists(CARPETA_IMAGENES):
    os.makedirs(CARPETA_IMAGENES)
    print(f"📂 Carpeta '{CARPETA_IMAGENES}' creada. Pon tus fotos ahí.")

print("🤖 Iniciando el Digitalizador (Motor: LLaVA + RTX 2000)...")

def analizar_factura(ruta_imagen):
    print(f"   👁️ Leyendo: {ruta_imagen}...")
    
    # El Prompt es la clave del Data Mining. Le damos instrucciones estrictas.
    prompt = """
    Actúa como un sistema OCR de contabilidad. Analiza esta imagen de una factura o recibo.
    Extrae la siguiente información y entrégala SOLO en formato JSON:
    {
        "tienda": "nombre del lugar",
        "fecha": "fecha de compra",
        "total": "monto total (solo el numero)",
        "moneda": "tipo de moneda (USD, PEN, EUR)",
        "items": ["lista", "de", "productos"]
    }
    Si no encuentras algún dato, pon null. No expliques nada, solo dame el JSON.
    """

    # Enviamos la imagen y el texto a la IA
    respuesta = ollama.chat(model='llava', messages=[
        {
            'role': 'user',
            'content': prompt,
            'images': [ruta_imagen]
        }
    ],
     options={'temperature': 0})

    texto_respuesta = respuesta['message']['content']
    
    # Limpieza básica por si la IA habla de más
    inicio = texto_respuesta.find('{')
    fin = texto_respuesta.rfind('}') + 1
    json_limpio = texto_respuesta[inicio:fin]
    
    return json.loads(json_limpio)

# --- BUCLE PRINCIPAL ---
# Busca todas las imágenes en la carpeta
archivos = [f for f in os.listdir(CARPETA_IMAGENES) if f.endswith(('.jpg', '.png', '.jpeg'))]

if not archivos:
    print("⚠️ No hay imágenes en la carpeta 'facturas'.")
else:
    datos_extraidos = []
    
    for archivo in archivos:
        ruta = os.path.join(CARPETA_IMAGENES, archivo)
        try:
            datos = analizar_factura(ruta)
            datos['archivo_origen'] = archivo # Agregamos el nombre del archivo
            datos_extraidos.append(datos)
            print(f"   ✅ Éxito: {datos['tienda']} - Total: {datos['total']}")
        except Exception as e:
            print(f"   ❌ Error leyendo {archivo}: {e}")

    # Guardar todo en un Excel (CSV)
    if datos_extraidos:
        keys = datos_extraidos[0].keys()
        with open('reporte_gastos.csv', 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(datos_extraidos)
        print("\n🎉 ¡Listo! Revisa el archivo 'reporte_gastos.csv'")
