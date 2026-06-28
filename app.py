import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
from pypdf import PdfReader

st.set_page_config(page_title="Extractor IA Multimodal", layout="wide")
st.title("🤖 Extractor de Obligaciones Municipales con IA")
st.write("Esta versión utiliza Inteligencia Artificial para leer dinámicamente cualquier PDF, incluso si es un escaneo o imagen.")

# Entrada para pegar la API Key de forma segura en la interfaz
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

uploaded_file = st.file_uploader("Sube cualquier PDF de comprobantes", type=["pdf"])

if uploaded_file is not None:
    if st.button("Analizar con Inteligencia Artificial"):
        if not api_key:
            st.error("Por favor, ingresa tu API Key de Gemini en la barra lateral izquierda para activar la IA.")
        else:
            with st.spinner("La IA está leyendo y procesando visualmente el documento..."):
                try:
                    # Leer los bytes del archivo para enviárselos a la IA
                    bytes_data = uploaded_file.getvalue()
                    
                    # Inicializar el cliente de IA de Google
                    client = genai.Client(api_key=api_key)
                    
                    # Instrucciones precisas para que la IA extraiga los datos con el formato que necesitas
                    prompt = """
                    Analiza el documento adjunto (comprobantes de pago u obligaciones municipales). 
                    Extrae absolutamente todos los conceptos de cobro detallados por cada año y número de predio.
                    Devuelve la información estrictamente en formato de tabla Markdown con las siguientes columnas:
                    | Predio | Año | No. Orden de pago | Concepto | Valor | Fecha de pago |
                    
                    Reglas:
                    1. Identifica el 'Número de Predio' para cada bloque de obligaciones.
                    2. Si un concepto dice 'Descuento' o similar, pon el valor con signo negativo (ej: -$0.40).
                    3. Si el documento indica 'Fecha Pago', colócala en formato DD/MM/AAAA. Si dice 'Obligaciones por cancelar' o no registra fecha de pago, pon 'Pendiente'.
                    4. No agregues introducciones ni textos extra, solo entrega la tabla Markdown directa.
                    """
                    
                    # Llamar al modelo capaz de procesar archivos/documentos (Gemini 2.5 Flash)
                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[
                            types.Part.from_bytes(
                                data=bytes_data,
                                mime_type='application/pdf',
                            ),
                            prompt
                        ]
                    )
                    
                    st.success("¡Análisis de IA completado con éxito!")
                    
                    # Mostrar la tabla que generó la IA
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Ocurrió un error al conectar con la IA: {e}")
