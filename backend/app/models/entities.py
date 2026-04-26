from datetime import datetime
from enum import Enum

from sqlalchemy import Boolean, DateTime, Enum as SAEnum, Float, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Role(str, Enum):
    ADMIN = 'admin'
    OWNER = 'owner'
    AGENT = 'agent'


class CallStatus(str, Enum):
    ACTIVE = 'active'
    ENDED = 'ended'
    ESCALATED = 'escalated'


class OrderStatus(str, Enum):
    CREATED = 'created'
    CONFIRMED = 'confirmed'
    CANCELLED = 'cancelled'


class User(Base):
    __tablename__ = 'users'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int | None] = mapped_column(ForeignKey('restaurants.id'))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    full_name: Mapped[str] = mapped_column(String(255))
    password_hash: Mapped[str] = mapped_column(String(255))
    role: Mapped[Role] = mapped_column(SAEnum(Role))


class Restaurant(Base):
    __tablename__ = 'restaurants'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(255))
    default_dialect: Mapped[str] = mapped_column(String(50), default='ar-JO')
    active: Mapped[bool] = mapped_column(Boolean, default=True)


class Branch(Base):
    __tablename__ = 'branches'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'))
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(Text)
    timezone: Mapped[str] = mapped_column(String(64), default='Asia/Amman')


class MenuCategory(Base):
    __tablename__ = 'menu_categories'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'))
    name_ar: Mapped[str] = mapped_column(String(255))


class MenuItem(Base):
    __tablename__ = 'menu_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('menu_categories.id'))
    name_ar: Mapped[str] = mapped_column(String(255))
    description_ar: Mapped[str] = mapped_column(Text, default='')
    price: Mapped[float] = mapped_column(Numeric(10, 2))
    is_available: Mapped[bool] = mapped_column(Boolean, default=True)


class ModifierGroup(Base):
    __tablename__ = 'modifier_groups'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    menu_item_id: Mapped[int] = mapped_column(ForeignKey('menu_items.id'))
    name_ar: Mapped[str] = mapped_column(String(255))


class ModifierOption(Base):
    __tablename__ = 'modifier_options'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    group_id: Mapped[int] = mapped_column(ForeignKey('modifier_groups.id'))
    name_ar: Mapped[str] = mapped_column(String(255))
    extra_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)


class Customer(Base):
    __tablename__ = 'customers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'))
    name: Mapped[str] = mapped_column(String(255))
    phone: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(Text, default='')


class CallSession(Base):
    __tablename__ = 'call_sessions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'))
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'))
    customer_id: Mapped[int | None] = mapped_column(ForeignKey('customers.id'))
    provider_call_id: Mapped[str] = mapped_column(String(255), unique=True)
    status: Mapped[CallStatus] = mapped_column(SAEnum(CallStatus), default=CallStatus.ACTIVE)
    ai_summary: Mapped[str] = mapped_column(Text, default='')
    started_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)


class TranscriptMessage(Base):
    __tablename__ = 'transcript_messages'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_session_id: Mapped[int] = mapped_column(ForeignKey('call_sessions.id'))
    role: Mapped[str] = mapped_column(String(30))
    text: Mapped[str] = mapped_column(Text)
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Order(Base):
    __tablename__ = 'orders'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'))
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'))
    customer_id: Mapped[int] = mapped_column(ForeignKey('customers.id'))
    call_session_id: Mapped[int | None] = mapped_column(ForeignKey('call_sessions.id'))
    status: Mapped[OrderStatus] = mapped_column(SAEnum(OrderStatus), default=OrderStatus.CREATED)
    order_type: Mapped[str] = mapped_column(String(20), default='delivery')
    total_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)


class OrderItem(Base):
    __tablename__ = 'order_items'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey('orders.id'))
    menu_item_id: Mapped[int] = mapped_column(ForeignKey('menu_items.id'))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Numeric(10, 2))


class OrderModifier(Base):
    __tablename__ = 'order_modifiers'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order_item_id: Mapped[int] = mapped_column(ForeignKey('order_items.id'))
    modifier_option_id: Mapped[int] = mapped_column(ForeignKey('modifier_options.id'))
    extra_price: Mapped[float] = mapped_column(Numeric(10, 2), default=0)


class HumanHandoff(Base):
    __tablename__ = 'human_handoffs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    call_session_id: Mapped[int] = mapped_column(ForeignKey('call_sessions.id'))
    reason: Mapped[str] = mapped_column(String(255))
    transferred_to: Mapped[str] = mapped_column(String(255), default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Subscription(Base):
    __tablename__ = 'subscriptions'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey('restaurants.id'))
    plan: Mapped[str] = mapped_column(String(100))
    status: Mapped[str] = mapped_column(String(30), default='active')


class AuditLog(Base):
    __tablename__ = 'audit_logs'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    actor_user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    restaurant_id: Mapped[int | None] = mapped_column(ForeignKey('restaurants.id'))
    action: Mapped[str] = mapped_column(String(255))
    details: Mapped[str] = mapped_column(Text, default='')
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class PrinterDevice(Base):
    __tablename__ = 'printer_devices'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    branch_id: Mapped[int] = mapped_column(ForeignKey('branches.id'))
    name: Mapped[str] = mapped_column(String(255))
    endpoint: Mapped[str] = mapped_column(String(255))
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
