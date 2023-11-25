from sqlalchemy import Column, Integer, String

from database import Base


class Meals(Base):
    __tablename__ = "meals"

    id = Column(Integer, primary_key=True, index=True)  # noqa: A003
    name = Column(String, index=True)
    description = Column(String, index=True)
    price = Column(Integer, index=True)
    user_id = Column(Integer, index=True)
