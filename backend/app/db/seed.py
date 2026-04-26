from sqlalchemy.orm import Session

from app.db.session import SessionLocal
from app.models.entities import Branch, MenuCategory, MenuItem, Restaurant


def seed() -> None:
    db: Session = SessionLocal()
    if db.query(Restaurant).first():
        return

    restaurant = Restaurant(name='شاورما الضيعة', default_dialect='ar-JO', active=True)
    db.add(restaurant)
    db.flush()

    branch = Branch(
        restaurant_id=restaurant.id,
        name='فرع الجامعة',
        phone='+962790000001',
        address='عمان - شارع الجامعة',
        timezone='Asia/Amman',
    )
    db.add(branch)
    db.flush()

    cat = MenuCategory(restaurant_id=restaurant.id, name_ar='سندويشات')
    db.add(cat)
    db.flush()

    db.add_all(
        [
            MenuItem(
                restaurant_id=restaurant.id,
                category_id=cat.id,
                name_ar='شاورما دجاج',
                description_ar='خبز عربي، ثوم، مخلل',
                price=2.50,
                is_available=True,
            ),
            MenuItem(
                restaurant_id=restaurant.id,
                category_id=cat.id,
                name_ar='شاورما لحم',
                description_ar='خبز عربي، طحينية، بصل',
                price=3.20,
                is_available=True,
            ),
        ]
    )
    db.commit()


if __name__ == '__main__':
    seed()
