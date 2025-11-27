import requests
import time

# Esta es la dirección de tu API (donde está escuchando el servidor)
URL_API = "http://127.0.0.1:8000/analizar"

print("📱 Iniciando App Cliente (Simulada)...")

while True:
    # 1. Pedimos al usuario que escriba algo
    texto_usuario = input("\n✍️  Escribe un comentario (o 'salir'): ")
    
    if texto_usuario.lower() == 'salir':
        break
    
    print("   Enviando a la nube (API)... ☁️")
    
    # 2. Enviamos el dato al servidor (Request)
    inicio = time.time() # Cronómetro
    try:
        respuesta = requests.post(URL_API, json={"texto": texto_usuario})
        
        # 3. Recibimos la respuesta (Response)
        datos = respuesta.json()
        tiempo_total = time.time() - inicio
        
        # 4. Mostramos el resultado
        print(f"   🤖 IA Dice: {datos['analisis_ia']}")
        print(f"   ⚡ Tiempo: {tiempo_total:.2f} segundos")
        
    except Exception as e:
        print(f"❌ Error: ¿Está prendido el servidor? {e}")

print("App cerrada.")
