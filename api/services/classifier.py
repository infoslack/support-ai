import instructor
from groq import Groq
from pydantic import BaseModel
from config.prompts import CLASSIFIER_PROMPT, IntentCategory, AUTOMATED_CATEGORIES
from config.settings import settings


class IntentResult(BaseModel):
    intent: IntentCategory


class ClassifierService:
    def __init__(self):
        client = Groq(api_key=settings.groq_api_key)
        self.client = instructor.from_groq(client, mode=instructor.Mode.JSON)

    def classify(self, message: str) -> tuple[IntentCategory, bool]:
        # Guardrail: cliente pediu humano explicitamente
        human_triggers = [
            "falar com humano",
            "atendente",
            "pessoa real",
            "falar com alguém",
            "quero humano",
        ]
        if any(trigger in message.lower() for trigger in human_triggers):
            return IntentCategory.OTHER, True

        prompt = CLASSIFIER_PROMPT.format(message=message)

        result = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_model=IntentResult,
        )

        intent = result.intent
        requires_human = intent not in AUTOMATED_CATEGORIES
        return intent, requires_human
