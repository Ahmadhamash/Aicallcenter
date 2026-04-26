from app.schemas.common import OrderFlowState
from app.services.orders.state_machine import OrderStateMachine


def test_order_state_machine_happy_path():
    sm = OrderStateMachine(session_id='s1')
    assert sm.advance() == OrderFlowState.INTENT_DETECTION
    assert sm.advance() == OrderFlowState.ORDER_BUILDING

    sm.add_item({'item_id': 1, 'quantity': 2})
    assert sm.advance() == OrderFlowState.CUSTOMER_INFO

    sm.mark_customer_info_complete()
    assert sm.advance() == OrderFlowState.CONFIRMATION
    assert sm.advance() == OrderFlowState.PAYMENT_OR_COD

    sm.mark_payment_resolved()
    assert sm.advance() == OrderFlowState.CREATE_ORDER
    assert sm.advance() == OrderFlowState.PRINT_RECEIPT
    assert sm.advance() == OrderFlowState.END_CALL
