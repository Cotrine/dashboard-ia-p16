from fastapi import FastAPI
from pydantic import BaseModel
import ollama
import sqlite3
import datetime

app = FastAPI()

# --- CONFIGURACIÓN DE BASE DE DATOS ---
def init_db():
    conexion = sqlite3.connect("historial.db")
    cursor = conexion.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS analisis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            texto_usuario TEXT,
            resultado_ia TEXT
        )
    ''')
    conexion.commit()
    conexion.close()

init_db()
print("💾 Base de Datos SQL conectada y lista.")

class Peticion(BaseModel):
    texto: str

@app.post("/analizar")
def analizar_sentimiento(datos: Peticion):
    # 1. IA
    respuesta = ollama.chat(model='llama3.2', messages=[
        {'role': 'system', 'content': 'Responde SOLO con: POSITIVO, NEGATIVO o NEUTRAL.'},
        {'role': 'user', 'content': datos.texto},
    ])
    sentimiento = respuesta['message']['content'].strip()
    
    # 2. SQL
    conexion = sqlite3.connect("historial.db")
    cursor = conexion.cursor()
    fecha_actual = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO analisis (fecha, texto_usuario, resultado_ia) VALUES (?, ?, ?)",
                   (fecha_actual, datos.texto, sentimiento))
    conexion.commit()
    conexion.close()
    
    print(f"✅ Guardado en DB: {datos.texto} -> {sentimiento}")

    return {"mensaje": datos.texto, "analisis": sentimiento}
# --- NUEVA VENTANILLA: VER HISTORIAL ---
@app.get("/historial")
def obtener_historial():
    conexion = sqlite3.connect("historial.db")
    conexion.row_factory = sqlite3.Row # Esto hace que los datos salgan con nombre, no solo números
    cursor = conexion.cursor()
    
    # Pedimos todo a la base de datos
    cursor.execute("SELECT * FROM analisis ORDER BY id DESC")
    filas = cursor.fetchall()
    
    conexion.close()
    
    return filas
# --- NUEVA VENTANILLA: CHAT GENERAL ---
class PeticionChat(BaseModel):
    pregunta: str

@app.post("/chat")
def chat_general(datos: PeticionChat):
    # Aquí NO le ponemos restricciones de "SOLO POSITIVO/NEGATIVO"
    # Dejamos que la IA sea libre.
    respuesta = ollama.chat(model='llama3.2', messages=[
        {'role': 'user', 'content': datos.pregunta},
    ])
    
    texto_respuesta = respuesta['message']['content']
    
    # También podríamos guardar esto en otra tabla de SQL, 
    # pero por ahora solo devolvemos la respuesta.
    return {"respuesta_ia": texto_respuesta}
# --- NUEVA VENTANILLA: RESUMIDOR ---
class PeticionResumen(BaseModel):
    texto_largo: str

@app.post("/resumir")
def resumir_documento(datos: PeticionResumen):
    # Aquí le damos una instrucción de sistema muy específica
    respuesta = ollama.chat(model='llama3.2', messages=[
        {'role': 'system', 'content': 'Eres un asistente experto. Resume el siguiente texto en 5 puntos clave (bullet points). Sé conciso.'},
        {'role': 'user', 'content': datos.texto_largo},
    ])
    
    resumen = respuesta['message']['content']
    return {"resumen_ia": resumen}
