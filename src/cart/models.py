import enum
from datetime import datetime

from sqlalchemy import MetaData, Column, Integer,  ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, relationship

from migrations.relationships import item_category, user_item_recommendation, item_order, user_item,Base


class Order(Base):
    __tablename__ = 'orders'
    id = Column(Integer,primary_key=True)
    date = Column(DateTime,default=datetime.utcnow())
    user_id  = Column(Integer, ForeignKey('customers.id'),nullable=True)
    items = relationship("Item", backref="orders.items",lazy="selectin",secondary=item_order)