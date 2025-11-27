import pandas as pd
import random

# Generamos 500 clientes ficticios
datos = []
for i in range(500):
    # Grupo A: Jóvenes que gastan poco
    if i < 200:
        edad = random.randint(18, 25)
        gasto = random.randint(50, 200)
    # Grupo B: Adultos que gastan mucho
    elif i < 400:
        edad = random.randint(35, 55)
        gasto = random.randint(500, 1000)
    # Grupo C: Jubilados ahorradores
    else:
        edad = random.randint(65, 80)
        gasto = random.randint(100, 300)

    datos.append({"ID": i, "Edad": edad, "Gasto_Anual": gasto})

df = pd.DataFrame(datos)
df.to_csv("clientes.csv", index=False)
print("✅ Archivo 'clientes.csv' generado con éxito.")
