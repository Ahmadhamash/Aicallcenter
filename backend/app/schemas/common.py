from enum import Enum
from pydantic import BaseModel, Field


class OrderFlowState(str, Enum):
    GREETING = 'GREETING'
    INTENT_DETECTION = 'INTENT_DETECTION'
    ORDER_BUILDING = 'ORDER_BUILDING'
    CUSTOMER_INFO = 'CUSTOMER_INFO'
    CONFIRMATION = 'CONFIRMATION'
    PAYMENT_OR_COD = 'PAYMENT_OR_COD'
    CREATE_ORDER = 'CREATE_ORDER'
    PRINT_RECEIPT = 'PRINT_RECEIPT'
    END_CALL = 'END_CALL'


class HealthResponse(BaseModel):
    status: str = 'ok'


class MenuItemRequest(BaseModel):
    item_id: int
    quantity: int = Field(gt=0)


class CustomerInfo(BaseModel):
    name: str
    phone: str
    address: str
    order_type: str
