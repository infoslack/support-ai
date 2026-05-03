from enum import Enum


class IntentCategory(str, Enum):
    # As 6 categorias automatizáveis
    WRONG_ITEM = "wrong_item"
    MISSING_ITEM = "missing_item"
    LATE_DELIVERY = "late_delivery"
    DUPLICATE_CHARGE = "duplicate_charge"
    CANCELLED_ORDER = "cancelled_order"
    POOR_QUALITY = "poor_quality"

    # As demais categorias (escalam para humano)
    RESTAURANT_COMPLAINT = "restaurant_complaint"
    DELIVERY_PERSON_COMPLAINT = "delivery_person_complaint"
    APP_TECHNICAL_ISSUE = "app_technical_issue"
    ACCOUNT_PROBLEM = "account_problem"
    COUPON_NOT_APPLIED = "coupon_not_applied"
    PAYMENT_METHOD_ISSUE = "payment_method_issue"
    ALLERGY_INCIDENT = "allergy_incident"
    FRAUD_SUSPICION = "fraud_suspicion"
    OTHER = "other"


# Categorias que podem ser resolvidas automaticamente
AUTOMATED_CATEGORIES = {
    IntentCategory.WRONG_ITEM,
    IntentCategory.MISSING_ITEM,
    IntentCategory.LATE_DELIVERY,
    IntentCategory.DUPLICATE_CHARGE,
    IntentCategory.CANCELLED_ORDER,
    IntentCategory.POOR_QUALITY,
}

# Valor máximo de reembolso sem aprovação humana
MAX_AUTO_REFUND = 50.0

CLASSIFIER_PROMPT = """You are a customer support intent classifier for a food delivery marketplace.

Classify the customer message into exactly one of these categories:
- wrong_item: customer received wrong items
- missing_item: items are missing from the order
- late_delivery: order arrived late or hasn't arrived
- duplicate_charge: customer was charged more than once
- cancelled_order: order was cancelled unexpectedly
- poor_quality: food quality was bad
- restaurant_complaint: complaint about the restaurant (not food quality)
- delivery_person_complaint: complaint about the delivery person behavior
- app_technical_issue: problem with the app itself
- account_problem: issues with account access or data
- coupon_not_applied: discount coupon didn't work
- payment_method_issue: problem with payment method
- allergy_incident: customer had allergic reaction
- fraud_suspicion: customer suspects fraudulent activity
- other: anything that doesn't fit the above

Customer message: {message}

Respond with ONLY the category key, nothing else."""

RESOLUTION_PROMPT = """You are a customer support agent for a food delivery marketplace.

You must resolve the customer issue based on the data below. Be empathetic and direct.

Customer message: {message}
Intent: {intent}
Order data:
{order_data}

Rules:
- For wrong_item or missing_item: offer reshipment if restaurant is still open, otherwise offer refund
- For late_delivery: offer a R$10 courtesy coupon if order arrived, full refund if not arrived
- For duplicate_charge: confirm the duplicate and issue full refund of the extra charge
- For cancelled_order: explain why if possible and offer full refund
- For poor_quality: offer 50% refund or a R$15 coupon

IMPORTANT: If the refund amount exceeds R$50.00, do NOT promise it. Say it needs manual review.

Generate a resolution message to send to the customer and specify the action taken."""

ESCALATION_PROMPT = """You are a customer support assistant preparing a case for a human agent.

Summarize the following support case clearly and concisely for the human agent.

Customer message: {message}
Intent: {intent}
Order data:
{order_data}

Escreva um breve resumo (3-5 frases) cobrindo: o problema, contexto relevante do pedido e próximos passos sugeridos para o agente humano."""
