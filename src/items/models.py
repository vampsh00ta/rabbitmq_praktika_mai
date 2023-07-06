import enum
from datetime import datetime,timedelta

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean,DateTime
from sqlalchemy.orm import DeclarativeBase, relationship

from migrations.relationships import item_category, user_item_recommendation, item_order, user_item,Base

class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer,primary_key=True)
    is_active = Column(Boolean,default=True)
    publish_time = Column(DateTime,default=datetime.utcnow())
    expiring_at = Column(DateTime,default=datetime.utcnow()+timedelta(minutes = 1))
    change_item = Column(DateTime,default=datetime.utcnow())
    name = Column(String,nullable=False)
    price = Column(String,nullable=False)
    brand = Column(String,nullable=True)
    image = Column(String,nullable=True)
    size = Column(String,nullable=False)
    recommendation_users = relationship("User", backref="items.recommendation_users",lazy="selectin", secondary=user_item_recommendation)
    used = Column(Boolean,nullable=False)
    category =  relationship("Category", backref="items.category", lazy="selectin",secondary=item_category)
    orders = relationship("Order", backref="items.orders",lazy="selectin", secondary=item_order)
    owner_id = Column(Integer, ForeignKey('customers.id'),nullable=False)
    liked_by = relationship("User", backref="items.liked_by",lazy="selectin", secondary=user_item)
    def __str__(self):
        return f"{self.name}"
class Category(Base):
    __tablename__ = 'categories'
    id = Column(Integer,primary_key=True)
    name = Column(String(255),nullable=False)
    item =  relationship("Item", backref="categories.items", lazy="selectin",secondary=item_category)