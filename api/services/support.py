from services.classifier import ClassifierService
from services.resolution import ResolutionService
from services.escalation import EscalationService
from services.database import get_order_data, format_order_context
from models.support import SupportRequest, SupportResponse


class SupportService:
    def __init__(self):
        self.classifier = ClassifierService()
        self.resolution = ResolutionService()
        self.escalation = EscalationService()

    def handle(self, request: SupportRequest) -> SupportResponse:
        # 1. Busca dados do pedido no banco
        order_data = get_order_data(request.order_id, request.customer_id)
        if not order_data:
            return SupportResponse(
                order_id=request.order_id,
                customer_id=request.customer_id,
                intent="other",
                resolved_automatically=False,
                message_to_customer="Não encontramos o pedido informado. Por favor, verifique o número e tente novamente.",
                needs_human_approval=False,
            )

        order_context = format_order_context(order_data)

        # 2. Classifica a intenção (guardrails de "quero humano" ficam dentro do classifier)
        intent, requires_human = self.classifier.classify(request.message)

        # 3. Roteamento
        if requires_human:
            escalation = self.escalation.escalate(
                message=request.message,
                intent=intent.value,
                order_context=order_context,
            )
            return SupportResponse(
                order_id=request.order_id,
                customer_id=request.customer_id,
                intent=intent,
                resolved_automatically=False,
                message_to_customer=(
                    "Seu caso foi encaminhado para um de nossos especialistas. "
                    "Em breve você receberá um retorno."
                ),
                escalation_summary=escalation.summary_for_agent,
                needs_human_approval=False,
            )

        # 4. Resolução automática
        resolution = self.resolution.resolve(
            message=request.message,
            intent=intent.value,
            order_context=order_context,
            order_value=float(order_data["total_value"]),
        )

        # Se a resolução gerou uma escalação por limite de reembolso
        if resolution.needs_human_approval:
            escalation = self.escalation.escalate(
                message=request.message,
                intent=intent.value,
                order_context=order_context,
            )
            return SupportResponse(
                order_id=request.order_id,
                customer_id=request.customer_id,
                intent=intent,
                resolved_automatically=False,
                message_to_customer=resolution.message_to_customer,
                action_taken=resolution.action,
                escalation_summary=escalation.summary_for_agent,
                needs_human_approval=True,
            )

        return SupportResponse(
            order_id=request.order_id,
            customer_id=request.customer_id,
            intent=intent,
            resolved_automatically=True,
            message_to_customer=resolution.message_to_customer,
            action_taken=resolution.action,
            needs_human_approval=False,
        )
