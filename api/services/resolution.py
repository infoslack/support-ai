import instructor
from groq import Groq
from config.prompts import RESOLUTION_PROMPT, MAX_AUTO_REFUND
from config.settings import settings
from models.support import ResolutionResult


class ResolutionService:
    def __init__(self):
        client = Groq(api_key=settings.groq_api_key)
        self.client = instructor.from_groq(client, mode=instructor.Mode.JSON)

    def resolve(
        self, message: str, intent: str, order_context: str, order_value: float
    ) -> ResolutionResult:
        prompt = RESOLUTION_PROMPT.format(
            message=message,
            intent=intent,
            order_data=order_context,
        )

        result = self.client.chat.completions.create(
            model=settings.groq_model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
            response_model=ResolutionResult,
        )

        # Guardrail: reembolso acima do limite vai para aprovação humana
        if (result.refund_amount and result.refund_amount > MAX_AUTO_REFUND) or (
            result.action == "refund" and order_value > MAX_AUTO_REFUND
        ):
            result.needs_human_approval = True
            result.action = "escalate"
            result.message_to_customer = (
                "Entendemos o seu problema e queremos resolver da melhor forma. "
                "Por se tratar de um valor acima do limite automático, "
                "um de nossos especialistas irá analisar e retornar em até 5 minutos."
            )

        return result
