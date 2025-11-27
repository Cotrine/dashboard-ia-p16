import ollama

print("🧠 Cargando el cerebro de tu ThinkPad (RTX 2000)...")

# Aquí definimos la pregunta
pregunta = "Explica en una frase corta qué es el Data Mining."

# Aquí enviamos la orden a la IA
respuesta = ollama.chat(model='llama3.2', messages=[
  {
    'role': 'user',
    'content': pregunta,
  },
])

# Aquí mostramos solo el contenido del mensaje de vuelta
print("\nRespuesta de la IA:")
print(respuesta['message']['content'])
