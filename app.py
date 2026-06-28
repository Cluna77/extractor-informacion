import streamlit as st
import pdfplumber
import re
import pandas as pd

st.set_page_config(page_title="Extractor de Obligaciones Municipales", layout="wide")

st.title("📋 Extractor Automático de Comprobantes y Obligaciones")
st.write("Sube el PDF consolidado de tus comprobantes de pago para generar la tabla estructurada automáticamente.")

# 1. Cargador de archivos
uploaded_file = st.file_uploader("Elige el archivo PDF de los comprobantes", type=["pdf"])

def procesar_pdf(file):
    datos_consolidados = []
    contribuyente = "No detectado"
    
    with pdfplumber.open(file) as pdf:
        texto_completo = ""
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() + "\n--- PAGINA ---\n"
            
        # Intentar extraer el nombre del contribuyente
        match_contribuyente = re.search(r"Contribuyente\s*:\s*([^\n]+)", texto_completo)
        if match_contribuyente:
            contribuyente = match_contribuyente.group(1).strip()
            
        # Dividir por secciones para simular las órdenes/comprobantes
        # En una versión avanzada, aquí puedes usar expresiones regulares adaptadas a las 
        # estructuras fijas del Municipio de Quito (Predio, Año, No. Orden, Conceptos)
        
        # Como ejemplo de estructura de datos extraída:
        # Aquí procesarías línea por línea buscando patrones como "Número de Predio:", "Año de Obligación:", etc.
        
    return contribuyente, texto_completo

if uploaded_file is not None:
    if st.button("Generar Tabla"):
        with st.spinner("Procesando documento y extrayendo conceptos..."):
            
            # Procesar el archivo subido
            contribuyente, texto = procesar_pdf(uploaded_file)
            
            st.success("¡Documento procesado con éxito!")
            st.markdown(f"### **Contribuyente:** {contribuyente}")
            
            # Nota: Para que la IA procese el texto en tiempo real de forma dinámica dentro de tu app, 
            # se suele conectar este texto extraído a una API (como la de Google Gemini) mediante un prompt.
            st.info("Texto extraído del PDF listo para estructurar:")
            st.text_area("Datos crudos extraídos:", texto, height=300)
