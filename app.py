# app.py
import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI

from agents.intake_agent import IntakeAgent
from agents.analysis_agent import AnalysisAgent
from agents.drafting_agent import DraftingAgent
from utils import extract_text_from_upload

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    st.error(
        "No se ha encontrado la variable OPENAI_API_KEY.\n"
        "Crea un archivo .env en la carpeta del proyecto con la línea:\n"
        "OPENAI_API_KEY=TU_CLAVE_AQUI"
    )
    st.stop()

client = OpenAI(api_key=api_key)

st.set_page_config(
    page_title="Asistente Fiscal AEAT (Modular)",
    page_icon="⚖️",
    layout="wide",
)

st.title("⚖️ Asistente Fiscal y Contable – AEAT (Módulos conectados)")
st.caption(
    "Herramienta experimental para análisis de notificaciones y trámites ante la AEAT. "
    "No sustituye al asesoramiento profesional presencial."
)

st.sidebar.header("Configuración")
model_choice = st.sidebar.selectbox(
    "Modelo de IA",
    ["gpt-4.1-mini", "gpt-4.1"],
    index=0,
)

intake_agent = IntakeAgent()
analysis_agent = AnalysisAgent(client=client, model=model_choice)
drafting_agent = DraftingAgent(client=client, model=model_choice)

st.markdown("### 1️⃣ Sube el documento de la AEAT (opcional)")
uploaded_file = st.file_uploader(
    "PDF, DOCX o TXT con requerimiento, sanción, liquidación, etc.",
    type=["pdf", "docx", "txt"],
)

document_text = None
if uploaded_file is not None:
    with st.spinner("Leyendo documento..."):
        document_text = extract_text_from_upload(uploaded_file)
    if document_text:
        st.success("Documento leído correctamente. Se usará en el análisis.")
        if st.checkbox("Ver extracto del documento leído"):
            st.text_area(
                "Extracto del documento",
                document_text[:4000],
                height=200,
            )
    else:
        st.error(
            "No se ha podido leer el archivo. Prueba con PDF, DOCX o TXT."
        )

st.markdown("### 2️⃣ Explica tu caso o formula tu pregunta")
user_question = st.text_area(
    "Describe la situación, dudas, importes, fechas de notificación, etc.",
    height=200,
    placeholder=(
        "Ejemplo: He recibido este requerimiento de la AEAT pidiéndome facturas del año 2021 "
        "relacionadas con el IVA. La notificación llegó el 3 de mayo de 2025. "
        "¿Qué significa y qué opciones tengo?"
    ),
)

st.markdown("### 3️⃣ Elige qué quieres que haga la herramienta")
modo = st.radio(
    "Modo de uso",
    [
        "Solo análisis y estrategia",
        "Análisis + redactar borrador de escrito",
    ],
)

extra_instructions = ""
if modo == "Análisis + redactar borrador de escrito":
    extra_instructions = st.text_area(
        "Instrucciones adicionales para el escrito (opcional)",
        height=120,
        placeholder=(
            "Ejemplo: Quiero recurrir la sanción, no estoy de acuerdo con la propuesta de liquidación, "
            "quiero enfatizar que aporté toda la documentación en plazo, etc."
        ),
    )

if st.button("🚀 Ejecutar asistente"):
    if not user_question and not document_text:
        st.error("Escribe al menos una explicación o sube un documento.")
    else:
        with st.spinner("Ejecutando módulos del asistente..."):
            # 1) INTAKE
            intake = intake_agent.run(
                user_question=user_question,
                document_text=document_text,
            )

            # 2) ANÁLISIS
            analysis_text = analysis_agent.run(
                user_question=intake.user_question,
                document_text=intake.document_text,
            )

        st.markdown("### 🧠 Análisis jurídico-fiscal y estrategia propuesta")
        st.markdown(analysis_text)

        if modo == "Análisis + redactar borrador de escrito":
            with st.spinner("Redactando borrador de escrito..."):
                draft = drafting_agent.run(
                    analysis_text=analysis_text,
                    extra_instructions=extra_instructions,
                )

            st.markdown("### ✍️ Borrador de escrito para copiar en Word/PDF")
            st.markdown(draft)
            st.markdown("### 📄 Texto completo para copiar")
            st.text_area(
                "Borrador completo",
                draft,
                height=300,
            )
        else:
            st.info(
                "Si quieres que además se redacte un borrador de escrito, "
                "cambia el modo a 'Análisis + redactar borrador de escrito' arriba."
            )

st.markdown("---")
st.caption(
    "Aviso legal: Esta herramienta es de ayuda general y no constituye asesoramiento jurídico vinculante. "
    "Para casos complejos o de alto riesgo, consulta con un abogado o asesor fiscal."
)
