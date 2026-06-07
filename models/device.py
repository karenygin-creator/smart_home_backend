from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base


class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    status = Column(String,default="off")
    is_online = Column(Boolean,default=True)

    house_id = Column(Integer, ForeignKey("houses.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))