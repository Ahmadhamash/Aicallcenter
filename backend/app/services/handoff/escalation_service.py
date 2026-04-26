class EscalationService:
    TRIGGERS = {
        'human_request',
        'complaint',
        'refund',
        'cancel',
        'low_confidence',
        'misunderstanding',
        'unsupported',
        'payment_problem',
        'angry',
        'allergy_ambiguity',
    }

    def should_escalate(self, signals: set[str], confidence: float, misunderstandings: int) -> bool:
        if signals.intersection(self.TRIGGERS):
            return True
        if confidence < 0.65:
            return True
        return misunderstandings >= 2
