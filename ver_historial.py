import sqlite3

# Conectamos al archivo
conexion = sqlite3.connect("historial.db")
cursor = conexion.cursor()

# Leemos todo (SELECT * es "Traeme todo")
print("\n📜 HISTORIAL DE ANÁLISIS (Base de Datos SQL):")
print("-" * 60)

cursor.execute("SELECT * FROM analisis")
filas = cursor.fetchall()

for fila in filas:
    # fila es una tupla: (id, fecha, texto, resultado)
    print(f"[{fila[1]}] {fila[3]} --> '{fila[2]}'")

print("-" * 60)
conexion.close()
