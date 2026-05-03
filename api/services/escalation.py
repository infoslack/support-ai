import instructor
from groq import Groq
from pydantic import BaseModel
from typing import Literal
from config.prompts import ESCALATION_PROMPT
from config.settings import settings


class EscalationOutput(BaseModel):
    summary_for_agent: str
    priority: Literal["low", "medium", "high"]


HIGH_PRIORITY_INTENTS = {"allergy_incident", "fraud_suspicion", "duplicate_charge"}
MEDIUM_PRIORITY_INTENTS = {"account_problem", "payment_method_issue", "cancelled_order"}


class EscalationService:
    def __init__(self):
        client = Groq(api_key=settings.groq_api_key)
        self.client = instructor.from_groq(client, mode=instructor.Mode.JSON)

    def escalate(
        self, message: str, intent: str, order_context: str
    ) -> EscalationOutput:
        prompt = ESCALATION_PROMPT.format(
            message=message,
            intent=intent,
            order_data=order_context,
        )

        result = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_model=EscalationOutput,
        )

        # Garante prioridade correta independente do LLM
        if intent in HIGH_PRIORITY_INTENTS:
            result.priority = "high"
        elif intent in MEDIUM_PRIORITY_INTENTS:
            result.priority = "medium"

        return result
