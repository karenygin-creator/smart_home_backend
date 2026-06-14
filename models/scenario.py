from sqlalchemy import Column, Integer, String, Boolean, ForeignKey

from database import Base


class Scenario(Base):
    __tablename__ = "scenarios"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    condition= Column(String)
    action= Column(String)
    is_active = Column(Boolean, default=True)
    house_id = Column(Integer, ForeignKey("houses.id"))