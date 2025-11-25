# agents/intake_agent.py

from dataclasses import dataclass

@dataclass
class IntakeResult:
    user_question: str
    document_text: str | None


class IntakeAgent:
    """
    Agente de entrada:
    - Recibe la explicación del usuario.
    - Recibe el texto del documento (si lo hay).
    - Devuelve un objeto normalizado.
    """

    def run(self, user_question: str, document_text: str | None) -> IntakeResult:
        user_question = (user_question or "").strip()
        doc = (document_text or "").strip() or None
        return IntakeResult(user_question=user_question, document_text=doc)
