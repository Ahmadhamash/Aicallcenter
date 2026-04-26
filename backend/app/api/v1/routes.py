from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.common import CustomerInfo, HealthResponse, MenuItemRequest
from app.services.handoff.escalation_service import EscalationService
from app.services.menu.tool_service import MenuToolService
from app.services.orders.state_machine import OrderStateMachine
from app.services.printer.receipt_printer import ReceiptPrinterService

router = APIRouter()


@router.get('/health', response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status='ok')


@router.get('/restaurants/{restaurant_id}/menu')
def get_menu(restaurant_id: int, db: Session = Depends(get_db)):
    return MenuToolService(db, restaurant_id).get_menu()


@router.post('/sessions/{session_id}/order/add-item')
def add_item(session_id: str, payload: MenuItemRequest):
    machine = OrderStateMachine(session_id=session_id)
    machine.add_item({'item_id': payload.item_id, 'quantity': payload.quantity})
    machine.advance()
    return {'state': machine.conversation.state, 'items': machine.items}


@router.post('/sessions/{session_id}/escalate')
def escalate(session_id: str, reason: str, confidence: float = 1.0, misunderstandings: int = 0):
    should = EscalationService().should_escalate({reason}, confidence, misunderstandings)
    if not should:
        raise HTTPException(status_code=400, detail='No escalation needed')
    return {'session_id': session_id, 'escalation': True, 'reason': reason}


@router.post('/orders/{order_id}/print')
def print_receipt(order_id: int, branch_id: int):
    return ReceiptPrinterService().print_receipt(order_id=order_id, branch_id=branch_id)


@router.post('/sessions/{session_id}/customer-info')
def customer_info(session_id: str, payload: CustomerInfo):
    return {'session_id': session_id, 'customer': payload.model_dump()}
