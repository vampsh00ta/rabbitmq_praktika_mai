import enum
from datetime import datetime,timedelta

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, Boolean,DateTime
from sqlalchemy.orm import DeclarativeBase, relationship




from migrations.relationships import user_item_recommendation, user_item, Base




class User(Base):
    __tablename__ = "customers"
    id = Column(Integer,primary_key=True)
    email = Column(String, nullable=False)
    items = relationship("Item", backref="customers.items",lazy="selectin")
    username = Column(String, nullable=False)
    registered_at = Column(TIMESTAMP, default=datetime.utcnow)
    updated_at = Column(TIMESTAMP,default=datetime.utcnow)
    orders = relationship("Order", backref="customers.orders",lazy="joined")
    recommendation_items = relationship("Item", backref="customers.recommendation_items",lazy="selectin", secondary=user_item_recommendation)

    hashed_password = Column(String(length=1024), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_superuser = Column( Boolean, default=False, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    liked_items = relationship("Item", backref="customers.liked_items",lazy="selectin", secondary=user_item)



