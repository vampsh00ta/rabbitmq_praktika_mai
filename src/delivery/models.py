import uuid

from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy.testing.schema import Table

from sqlalchemy import Integer, String, Column, ForeignKey, DateTime, Boolean, MetaData, UUID


class Base(DeclarativeBase):
    metadata = MetaData()

class Status(Base):
    __tablename__ = 'status'
    id = Column(Integer, primary_key=True)
    current_city = Column(String(length=35), nullable=False)
    last_update = Column(DateTime,nullable=False)
    track_id  = Column(UUID, ForeignKey('delivery.track_id'))
    delivery_status_name =  Column(Integer, ForeignKey('status_name.id'))



class StatusName(Base):
    __tablename__ = 'status_name'
    id = Column(Integer, primary_key=True)
    name = Column(String(length=1024), nullable=False)


class Delivery(Base):
    __tablename__ = 'delivery'
    track_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    receiver_name = Column(String(length=300),nullable=False)
    telephone_number = Column(String(length=35),nullable=False)
    street = Column(String(length=300),nullable=False)
    city = Column(String(length=35),nullable=False)
    dilivery_day = Column(DateTime, nullable=True)
    status = relationship("Status", foreign_keys='Status.track_id',backref="delivery.statuses",lazy='selectin')




