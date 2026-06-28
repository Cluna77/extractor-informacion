import streamlit as st
import pandas as pd
import re
from pypdf import PdfReader

st.set_page_config(page_title="Extractor Dinámico Real", layout="wide")
st.title("📋 Extractor de Obligaciones Municipales (100% Dinámico)")

uploaded_file = st.file_uploader("Sube cualquier PDF de comprobantes", type=["pdf"])

if uploaded_file is not None:
    if st.button("Analizar Documento Real"):
        with st.spinner("Analizando la estructura del PDF subido..."):
            
            reader = PdfReader(uploaded_file)
            filas_extraidas = []
            
            # Recorrer cada página del PDF real subido por el usuario
            for num_pag, pagina in enumerate(reader.pages):
                texto = pagina.extract_text()
                if not texto:
                    continue # Si la página es una imagen pura, saltar
                
                # Buscar patrones reales en el texto de esta página específica
                predio_match = re.search(r"(?:Número de Predio|Predio)\s*:\s*(\d+)", texto, re.IGNORECASE)
                anio_match = re.search(r"(?:Año de Obligación|Año)\s*:\s*(\d+)", texto, re.IGNORECASE)
                orden_match = re.search(r"(?:Orden para el Pago|Orden)\s*:\s*(\d+)", texto, re.IGNORECASE)
                
                predio = predio_match.group(1) if predio_match else "No detectado"
                anio = anio_match.group(1) if anio_match else "No detectado"
                orden = orden_match.group(1) if orden_match else "No detectado"
                
                # Buscar líneas de conceptos y valores numéricos ej: "INTERES POR MORA 0,71"
                lineas = texto.split("\n")
                for linea in lineas:
                    # Expresión regular para capturar el concepto de texto y el valor económico al final
                    match_valores = re.search(r"([A-Z\s]+(?:\s[A-Z\s]+)*)\s+(\d+[\s,.]\d{2})", linea)
                    if match_valores:
                        concepto = match_valores.group(1).strip()
                        valor = match_valores.group(2).strip()
                        
                        # Filtrar palabras que no son conceptos tributarios comunes
                        if "TOTAL" not in concepto and "SUBTOTAL" not in concepto:
                            filas_extraidas.append({
                                "Predio": predio,
                                "Año": anio,
                                "No. Orden de pago": orden,
                                "Concepto": concepto,
                                "Valor": f"${valor}",
                                "Fecha de pago": "Verificar en PDF"
                            })
            
            if filas_extraidas:
                df_resultado = pd.DataFrame(filas_extraidas)
                st.success("¡Datos extraídos dinámicamente del archivo!")
                st.dataframe(df_resultado, use_container_width=True)
            else:
                st.error("No se pudo extraer texto indexable de este PDF específico. Verifique si es un escaneo tipo imagen.")
