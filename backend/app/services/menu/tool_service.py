from sqlalchemy.orm import Session

from app.models.entities import MenuItem


class MenuToolService:
    def __init__(self, db: Session, restaurant_id: int):
        self.db = db
        self.restaurant_id = restaurant_id

    def get_menu(self) -> list[dict]:
        rows = self.db.query(MenuItem).filter(MenuItem.restaurant_id == self.restaurant_id).all()
        return [
            {
                'id': r.id,
                'name_ar': r.name_ar,
                'price': float(r.price),
                'is_available': r.is_available,
            }
            for r in rows
        ]

    def check_item_availability(self, item_id: int) -> bool:
        item = self.db.query(MenuItem).filter(
            MenuItem.restaurant_id == self.restaurant_id, MenuItem.id == item_id
        ).first()
        return bool(item and item.is_available)

    def calculate_total_price(self, items: list[dict]) -> float:
        total = 0.0
        for item in items:
            menu_item = self.db.query(MenuItem).filter(MenuItem.id == item['item_id']).first()
            if not menu_item:
                continue
            total += float(menu_item.price) * item['quantity']
        return round(total, 2)
