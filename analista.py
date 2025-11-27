import ollama


# 1. Estos son los "Datos Crudos" (imaginemos que vienen de un Excel)
comentarios_clientes = [
    "El producto llegó roto y la caja estaba abierta, pésimo servicio.",
    "Me encantó el color, es exactamente igual a la foto, muy feliz.",
    "El envío tardó un poco más de lo esperado, pero el producto está bien.",
    "No sirve para nada, quiero mi dinero de vuelta inmediatamente."
]

print(f"📊 Analizando {len(comentarios_clientes)} comentarios con tu RTX 2000...\n")

# 2. El Bucle (Data Mining en acción)
for comentario in comentarios_clientes:
    
    # Le damos una instrucción precisa a la IA (System Prompt)
    respuesta = ollama.chat(model='llama3.2', messages=[
        {
            'role': 'system', 
            'content': 'Eres un clasificador de datos. Responde SOLO con una palabra: "POSITIVO", "NEGATIVO" o "NEUTRAL". No des explicaciones.'
        },
        {
            'role': 'user', 
            'content': f"Analiza este comentario: {comentario}"
        },
    ])
    
    # 3. Limpiamos el resultado
    sentimiento = respuesta['message']['content'].strip()
    
    # 4. Imprimimos el resultado bonito
    print(f"💬 Comentario: {comentario}")
    print(f"🤖 Veredicto IA: {sentimiento}")
    print("-" * 30) # Una linea separadora
