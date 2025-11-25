# agents/analysis_agent.py

from openai import OpenAI
from prompts import LEGAL_ASSISTANT_SYSTEM_PROMPT

class AnalysisAgent:
    """
    Agente de ANÁLISIS:
    - Recibe los datos normalizados (pregunta + documento).
    - Pide al modelo que analice jurídicamente el caso y proponga estrategia,
      sin redactar aún el escrito final (eso lo hará el DraftingAgent).
    """

    def __init__(self, client: OpenAI, model: str = "gpt-4.1-mini"):
        self.client = client
        self.model = model

    def build_user_message(self, user_question: str, document_text: str | None) -> str:
        partes = []

        if user_question:
            partes.append("CONSULTA / EXPLICACIÓN DEL USUARIO:\n" + user_question)

        if document_text:
            max_chars = 12000
            trozo = document_text[:max_chars]
            partes.append(
                "EXTRACTO DEL DOCUMENTO (p.ej. notificación de la AEAT):\n" + trozo
            )
            if len(document_text) > max_chars:
                partes.append(
                    "\n[NOTA: el documento completo es más largo; se ha recortado para el análisis.]"
                )

        partes.append(
            "\nINDICACIONES PARA EL ANÁLISIS (NO redactes aún el escrito final):\n"
            "- Identifica el tipo de acto (requerimiento, sanción, liquidación, etc.).\n"
            "- Explica en lenguaje claro qué está ocurriendo.\n"
            "- Indica plazos y riesgos aproximados.\n"
            "- Propón varias opciones con ventajas e inconvenientes.\n"
            "- Señala qué datos faltarían para preparar un escrito definitivo."
        )

        return "\n\n".join(partes)

    def run(self, user_question: str, document_text: str | None) -> str:
        user_content = self.build_user_message(user_question, document_text)

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": LEGAL_ASSISTANT_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()
