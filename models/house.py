from sqlalchemy import Column, Integer, String, ForeignKey

from database import Base


class House(Base):
    __tablename__="houses"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    address = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))