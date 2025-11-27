import cv2
from ultralytics import YOLO
import time

print("👁️ Cargando sistema de conteo en RTX 2000...")
modelo = YOLO('yolov8n.pt') 

# Usamos el video que descargaste
cap = cv2.VideoCapture("prueba.mp4")

# Colores para el texto
COLOR_TEXTO = (0, 255, 0) # Verde brillante

while True:
    ret, frame = cap.read()
    if not ret:
        break # Si se acaba el video, salimos

    # Detectamos
    resultados = modelo(frame, stream=True, verbose=False)

    conteo_personas = 0

    for r in resultados:
        # Dibujamos las cajas
        frame_anotado = r.plot()
        
        # --- LÓGICA DE NEGOCIO (Data Mining Visual) ---
        # Analizamos qué cosas detectó la IA
        for caja in r.boxes:
            # La clase 0 en YOLO es 'person'
            if int(caja.cls[0]) == 0:
                conteo_personas += 1

    # Escribimos el reporte en la pantalla en vivo
    texto = f"CLIENTES DETECTADOS: {conteo_personas}"
    
    # Dibujamos un rectángulo negro de fondo para que se lea bien
    cv2.rectangle(frame_anotado, (10, 10), (450, 60), (0, 0, 0), -1)
    cv2.putText(frame_anotado, texto, (20, 45), 
                cv2.FONT_HERSHEY_SIMPLEX, 1, COLOR_TEXTO, 2)

    # Alerta visual si hay mucha gente (Aglomeración)
    if conteo_personas > 5:
        cv2.putText(frame_anotado, "¡ALERTA DE AFORO!", (20, 90), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

    # Mostramos
    cv2.imshow("Retail Analytics - ThinkPad P16", frame_anotado)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
