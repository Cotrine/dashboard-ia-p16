from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import streamlit as st
import requests
import pandas as pd
from pypdf import PdfReader
st.set_page_config(page_title="Super IA P16", page_icon="🧠", layout="wide")

# --- BARRA LATERAL (MENU) ---
st.sidebar.title("🔧 Herramientas")
opcion = st.sidebar.radio("Elige una función:", ["Analizador de Sentimiento", "Chatbot General", "Ver Historial","Resumidor de PDFs", "Segmentación de Clientes","Transcriptor de Audio"])

# --- OPCIÓN 1: EL ANALIZADOR (Lo que ya tenías) ---
if opcion == "Analizador de Sentimiento":
    st.header("📊 Aanalizador de Opiniones")
    st.write("Detecta si un comentario es Positivo o Negativo.")
    
    texto = st.text_area("Ingresa el comentario:")
    
    if st.button("Analizar"):
        if texto:
            with st.spinner("La RTX 2000 está pensando..."):
                try:
                    res = requests.post("https://uninhibited-guardlike-stuart.ngrok-free.dev/analizar", json={"texto": texto})
                    datos = res.json()
                    sentimiento = datos['analisis'] # Ojo: Asegúrate de usar la clave correcta
                    
                    if "POSITIVO" in sentimiento:
                        st.success(f"Resultado: {sentimiento}")
                        st.balloons()
                    elif "NEGATIVO" in sentimiento:
                        st.error(f"Resultado: {sentimiento}")
                    else:
                        st.info(f"Resultado: {sentimiento}")
                        
                except Exception as e:
                    st.error(f"Errorr de conexión: {e}")

# --- OPCIÓN 2: EL CHATBOT (Lo Nuevo) ---
elif opcion == "Chatbot General":
    st.header("💬 Chat con Llama 3.2")
    st.write("Pregúntale lo que quieras. Sin restricciones.")
    
    pregunta = st.text_input("Tu pregunta:")
    
    if st.button("Enviar"):
        if pregunta:
            with st.spinner("Escribiendo..."):
                try:
                    # Llamamos a la NUEVA ventanilla /chat
                    res = requests.post("https://uninhibited-guardlike-stuart.ngrok-free.dev/chat", json={"pregunta": pregunta})
                    datos = res.json()
                    st.markdown(f"**🤖 IA:** {datos['respuesta_ia']}")
                except Exception as e:
                    st.error(f"Error: {e}")

# --- OPCIÓN 3: HISTORIAL (Las Gráficas) ---
elif opcion == "Ver Historial":
    st.header("📜 Historial de Base de Datos")
    
    if st.button("Cargar Datos"):
        try:
            res = requests.get("https://uninhibited-guardlike-stuart.ngrok-free.dev/historial")
            df = pd.DataFrame(res.json())
            st.dataframe(df)
            
            # Gráfico si hay datos
            if not df.empty:
                st.subheader("Estadísticas")
                st.bar_chart(df['resultado_ia'].value_counts())
                
        except Exception as e:
            st.error("No se pudo conectar a la base de datos.")
# --- OPCIÓN 4: RESUMIDOR DE PDF (Lo Nuevo) ---
elif opcion == "Resumidor de PDFs":
    st.header("📄 Resumidor de Documentos")
    st.write("Sube un PDF y la IA te dará los puntos clave.")
    
    # Widget para subir archivos
    archivo_pdf = st.file_uploader("Sube tu PDF aquí", type="pdf")
    
    if archivo_pdf is not None:
        # 1. Extraer el texto del PDF (Magia de Python)
        lector = PdfReader(archivo_pdf)
        texto_completo = ""
        for pagina in lector.pages:
            texto_completo += pagina.extract_text()
            
        st.info(f"PDF cargado con éxito. Tiene {len(lector.pages)} páginas.")
        
        # Botón para activar la IA
        if st.button("Generar Resumen"):
            with st.spinner("Leyendo y analizando..."):
                try:
                    # Enviamos el texto extraído a tu API
                    res = requests.post("https://uninhibited-guardlike-stuart.ngrok-free.dev/resumir", json={"texto_largo": texto_completo})
                    
                    if res.status_code == 200:
                        datos = res.json()
                        st.subheader("📝 Resumen Generado:")
                        st.markdown(datos['resumen_ia'])
                    else:
                        st.error("El texto es demasiado largo para procesarlo de una sola vez.")
                        
                except Exception as e:
                    st.error(f"Error: {e}")
# --- OPCIÓN 5: SEGMENTACIÓN DE CLIENTES (Clustering) ---
elif opcion == "Segmentación de Clientes":
    st.header("💎 Minería de Datos: Segmentación de Clientes")
    st.write("Sube tu base de datos y la IA agrupará a tus clientes automáticamente.")
    
    archivo_clientes = st.file_uploader("Sube clientes.csv", type="csv")
    
    if archivo_clientes is not None:
        df = pd.read_csv(archivo_clientes)
        st.write("Datos cargados:", df.head())
        
        # Seleccionamos las columnas para analizar
        # (En un caso real, el usuario elegiría las columnas)
        X = df[['Edad', 'Gasto_Anual']]
        
        # Slider para elegir cuántos grupos queremos buscar
        k = st.slider("¿Cuántos grupos (clusters) quieres buscar?", 2, 6, 3)
        
        if st.button("Ejecutar Clustering (K-Means)"):
            with st.spinner("Calculando distancias matemáticas..."):
                # 1. ENTRENAMIENTO DEL MODELO ML
                kmeans = KMeans(n_clusters=k, random_state=42)
                df['Grupo'] = kmeans.fit_predict(X)
                
                st.success("¡Segmentación Completada!")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Resultados Numéricos")
                    st.dataframe(df)
                    st.write("Promedios por Grupo:")
                    st.write(df.groupby('Grupo')[['Edad', 'Gasto_Anual']].mean())
                
                with col2:
                    st.subheader("Visualización Gráfica")
                    # Usamos Matplotlib para dibujar los puntos
                    fig, ax = plt.subplots()
                    # Colores para cada grupo
                    scatter = ax.scatter(df['Edad'], df['Gasto_Anual'], c=df['Grupo'], cmap='viridis')
                    ax.set_xlabel('Edad')
                    ax.set_ylabel('Gasto Anual ($)')
                    plt.colorbar(scatter, label='Grupo Detectado')
                    st.pyplot(fig)
                    
            st.info("💡 Interpretación de Negocio: Mira qué grupo gasta más y enfoca tu marketing ahí.")
elif opcion == "Transcriptor de Audio":
    st.header("🎧 Transcriptor Inteligente (Whisper)")
    st.write("Sube un audio (mp3, wav, m4a) y la IA lo convertirá en texto.")
    
    archivo_audio = st.file_uploader("Sube tu audio aquí", type=["mp3", "wav", "m4a"])
    
    if archivo_audio is not None:
        st.audio(archivo_audio)
        
        if st.button("Transcribir Audio"):
            with st.spinner("Escuchando... (Esto usa la GPU intensamente)"):
                try:
                    # Preparamos el archivo
                    files = {"file": (archivo_audio.name, archivo_audio, archivo_audio.type)}
                    
                    # Llamamos a la API
                    res = requests.post("https://uninhibited-guardlike-stuart.ngrok-free.dev/transcribir", files=files)
                    
                    if res.status_code == 200:
                        texto = res.json()['transcripcion']
                        st.success("¡Transcripción Completada!")
                        st.text_area("Resultado:", value=texto, height=200)
                    else:
                        st.error("Error en el servidor al procesar el audio.")
                        
                except Exception as e:
                    st.error(f"Error de conexión: {e}")
