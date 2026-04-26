from dataclasses import dataclass


@dataclass
class ReceiptPrinterService:
    def print_receipt(self, order_id: int, branch_id: int) -> dict:
        # TODO: Replace mock with real printer connector (network ESC/POS or vendor SDK).
        return {
            'order_id': order_id,
            'branch_id': branch_id,
            'status': 'queued',
            'provider': 'mock-printer',
        }
