from pydantic import BaseModel
from typing import Literal, Optional
from config.prompts import IntentCategory


class SupportRequest(BaseModel):
    message: str
    order_id: str
    customer_id: str


class ClassificationResult(BaseModel):
    intent: IntentCategory
    requires_human: bool


class ResolutionResult(BaseModel):
    action: Literal["refund", "reship", "coupon", "explanation", "escalate"]
    message_to_customer: str
    refund_amount: Optional[float] = None
    coupon_value: Optional[float] = None
    needs_human_approval: bool = False


class EscalationResult(BaseModel):
    summary_for_agent: str
    priority: Literal["low", "medium", "high"]


class SupportResponse(BaseModel):
    order_id: str
    customer_id: str
    intent: IntentCategory
    resolved_automatically: bool
    message_to_customer: str
    action_taken: Optional[str] = None
    escalation_summary: Optional[str] = None
    needs_human_approval: bool = False
    escalation_priority: Optional[Literal["low", "medium", "high"]] = None
