import streamlit as st
from ultralytics import YOLO
from PIL import Image
import numpy as np

st.set_page_config(page_title="Ojo Digital P16", page_icon="👁️")

st.title("👁️ Reconocimiento Móvil")
st.write("Toma una foto con tu celular y la RTX 2000 la analizará.")

@st.cache_resource
def cargar_modelo():
    return YOLO('yolov8n.pt')

modelo = cargar_modelo()

# --- CAMBIO IMPORTANTE AQUÍ ---
# En lugar de stream de video, usamos el uploader.
# En el celular, esto te abrirá la opción de "Cámara" o "Galería".
img_file = st.file_uploader("Toca aquí para tomar foto", type=['jpg', 'png', 'jpeg'])

if img_file:
    # 1. Abrimos la imagen que subió el celular
    image = Image.open(img_file)
    
    # Mostrar la foto original
    st.image(image, caption='Foto enviada desde el celular', use_container_width=True)
    
    # 2. Botón para activar el análisis (para que no lo haga automático si no quieres)
    if st.button("🔍 Analizar con IA"):
        with st.spinner('Enviando a la ThinkPad P16...'):
            # Procesar con YOLO
            results = modelo(image)
            
            # Dibujar resultados
            res_plotted = results[0].plot()
            
            # Mostrar resultado final
            st.success("¡Análisis Completado!")
            st.image(res_plotted, caption='Lo que ve la IA', use_container_width=True)
            
            # Listar objetos
            detectados = []
            for box in results[0].boxes:
                clase = int(box.cls[0])
                detectados.append(modelo.names[clase])
            
            if detectados:
                st.info(f"Objetos encontrados: {', '.join(set(detectados))}")
