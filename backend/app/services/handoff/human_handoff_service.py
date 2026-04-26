from sqlalchemy.orm import Session

from app.models.entities import HumanHandoff


class HumanHandoffService:
    def __init__(self, db: Session):
        self.db = db

    def transfer(self, call_session_id: int, reason: str, target: str = 'agent_queue') -> HumanHandoff:
        handoff = HumanHandoff(call_session_id=call_session_id, reason=reason, transferred_to=target)
        self.db.add(handoff)
        self.db.commit()
        self.db.refresh(handoff)
        return handoff
