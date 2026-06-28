import streamlit as st
import pandas as pd
from google import genai
from google.genai import types
from pypdf import PdfReader

st.set_page_config(page_title="Extractor IA Multimodal", layout="wide")
st.title("🤖 Extractor de Obligaciones Municipales con IA")
st.write("Esta versión utiliza Inteligencia Artificial para leer dinámicamente cualquier PDF, extraer el contribuyente y formatear los valores a USD.")

# Entrada para pegar la API Key de forma segura en la interfaz
api_key = st.sidebar.text_input("Ingresa tu Gemini API Key:", type="password")

uploaded_file = st.file_uploader("Sube cualquier PDF de comprobantes", type=["pdf"])

if uploaded_file is not None:
    if st.button("Analizar con Inteligencia Artificial"):
        if not api_key:
            st.error("Por favor, ingresa tu API Key de Gemini en la barra lateral izquierda para activar la IA.")
        else:
            with st.spinner("La IA está leyendo el documento y estructurando los datos..."):
                try:
                    # Leer los bytes del archivo para enviárselos a la IA
                    bytes_data = uploaded_file.getvalue()
                    
                    # Inicializar el cliente de IA de Google
                    client = genai.Client(api_key=api_key)
                    
                    # Instrucciones mejoradas con las nuevas peticiones de formato
                    prompt = """
                    Analiza el documento adjunto (comprobantes de pago u obligaciones municipales del GAD de Quito). 
                    
                    Debes entregar tu respuesta estructurada exactamente de la siguiente manera:
                    
                    1. Un encabezado principal que identifique al contribuyente encontrado en el documento, usando este formato exacto:
                    ## Detalle de Comprobantes de Pago y Obligaciones
                    **Contribuyente:** [NOMBRE DEL CONTRIBUYENTE DETECTADO]
                    
                    2. Una tabla Markdown con la información extraída de todos los conceptos de cobro detallados por cada año y número de predio, usando estas columnas exactas:
                    | Predio | Año | No. Orden de pago | Concepto | Valor | Fecha de pago |
                    
                    Reglas estrictas para el contenido de la tabla:
                    - Columna 'Predio': Identifica el 'Número de Predio' correspondiente a cada bloque de obligaciones.
                    - Columna 'Valor': Todos los montos deben llevar obligatoriamente formato de moneda USD usando el símbolo '$', seguido del número con coma para los decimales (ejemplo: $20,27 o $0,89). Si el concepto corresponde a un 'Descuento' o 'Descuentos Generales', el valor debe reflejarse obligatoriamente con signo negativo (ejemplo: -$0,40 o -$0,01).
                    - Columna 'Fecha de pago': Si el documento indica 'Fecha Pago', colócala en formato DD/MM/AAAA. Si la sección corresponde a 'Obligaciones por cancelar' o no registra una fecha de pago efectiva, coloca textualmente 'Pendiente'.
                    
                    No agregues saludos, explicaciones previas ni textos adicionales al final. Entrega directamente el encabezado y la tabla Markdown.
                    """
                    
                    # Llamar al modelo multimodal (Gemini 2.5 Flash)
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
                    
                    # Renderizar el resultado directamente en la aplicación
                    st.markdown(response.text)
                    
                except Exception as e:
                    st.error(f"Ocurrió un error al conectar con la IA: {e}")
