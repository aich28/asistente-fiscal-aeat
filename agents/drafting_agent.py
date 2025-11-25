# agents/drafting_agent.py

from openai import OpenAI
from prompts import LEGAL_ASSISTANT_SYSTEM_PROMPT

class DraftingAgent:
    """
    Agente de REDACCIÓN:
    - Recibe el análisis previo (texto) + datos que el usuario confirme.
    - Redacta un borrador de escrito (alegaciones, recurso, etc.).
    """

    def __init__(self, client: OpenAI, model: str = "gpt-4.1-mini"):
        self.client = client
        self.model = model

    def run(
        self,
        analysis_text: str,
        extra_instructions: str | None = None,
    ) -> str:
        instrucciones = extra_instructions or ""
        user_content = (
            "ANÁLISIS PREVIO DEL CASO (BASE PARA REDACTAR):\n"
            + analysis_text
            + "\n\n"
            + "INSTRUCCIONES ADICIONALES DEL USUARIO (si las hay):\n"
            + instrucciones
            + "\n\n"
            "TAREA: Redacta ahora un borrador de escrito jurídico-fiscal completo, "
            "listo para copiar en Word/PDF, siguiendo este esquema:\n"
            "1) Encabezado (órgano, datos del interesado, referencia del expediente)\n"
            "2) Exposición de hechos\n"
            "3) Fundamentos de Derecho (sin exceso de citas, solo las necesarias)\n"
            "4) Petición final\n"
            "Marca con texto entre corchetes [ASÍ] los datos que falten por rellenar "
            "(nombre, NIF, número de expediente, fechas, etc.)."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": LEGAL_ASSISTANT_SYSTEM_PROMPT},
                {"role": "user", "content": user_content},
            ],
            temperature=0.2,
        )

        return response.choices[0].message.content.strip()
