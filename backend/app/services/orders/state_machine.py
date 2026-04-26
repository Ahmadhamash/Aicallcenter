from dataclasses import dataclass, field

from app.schemas.common import OrderFlowState


@dataclass
class ConversationState:
    state: OrderFlowState = OrderFlowState.GREETING
    misunderstanding_count: int = 0
    ai_confidence: float = 1.0
    escalation_required: bool = False


@dataclass
class OrderStateMachine:
    session_id: str
    items: list[dict] = field(default_factory=list)
    customer_info_complete: bool = False
    payment_resolved: bool = False
    conversation: ConversationState = field(default_factory=ConversationState)

    def advance(self) -> OrderFlowState:
        st = self.conversation.state
        if st == OrderFlowState.GREETING:
            self.conversation.state = OrderFlowState.INTENT_DETECTION
        elif st == OrderFlowState.INTENT_DETECTION:
            self.conversation.state = OrderFlowState.ORDER_BUILDING
        elif st == OrderFlowState.ORDER_BUILDING and self.items:
            self.conversation.state = OrderFlowState.CUSTOMER_INFO
        elif st == OrderFlowState.CUSTOMER_INFO and self.customer_info_complete:
            self.conversation.state = OrderFlowState.CONFIRMATION
        elif st == OrderFlowState.CONFIRMATION:
            self.conversation.state = OrderFlowState.PAYMENT_OR_COD
        elif st == OrderFlowState.PAYMENT_OR_COD and self.payment_resolved:
            self.conversation.state = OrderFlowState.CREATE_ORDER
        elif st == OrderFlowState.CREATE_ORDER:
            self.conversation.state = OrderFlowState.PRINT_RECEIPT
        elif st == OrderFlowState.PRINT_RECEIPT:
            self.conversation.state = OrderFlowState.END_CALL
        return self.conversation.state

    def add_item(self, item: dict) -> None:
        self.items.append(item)

    def mark_customer_info_complete(self) -> None:
        self.customer_info_complete = True

    def mark_payment_resolved(self) -> None:
        self.payment_resolved = True
