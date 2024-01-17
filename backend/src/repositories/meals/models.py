

from sqlalchemy import Integer, String, ForeignKey, Enum, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from enums import LikeDislikeEnum

meal_category_association = Table(
    'meal_category_association',
    Base.metadata,
    Column('meal_id', Integer, ForeignKey('meal.id'), primary_key=True),
    Column('category_id', Integer, ForeignKey('category.id'), primary_key=True)
)

class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)

    meals: Mapped[list["Meal"]] = relationship(
        "Meal",
        secondary=meal_category_association,
        back_populates="categories"
    )

class Meal(Base):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    price: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey('user.id'))
    likes_count: Mapped[int] = mapped_column(Integer)

    likes: Mapped[list["Like"]] = relationship("Like", back_populates="meal")
    creator = relationship("User", back_populates="meal")
    categories: Mapped[list[Category]] = relationship(
        "Category",
        secondary=meal_category_association,
        back_populates="meal"
    )


class Like(Base):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer)
    meal_id: Mapped[int] = mapped_column(Integer, ForeignKey('meal.id'))
    value: Mapped[LikeDislikeEnum] = mapped_column(Enum(LikeDislikeEnum))

    meal: Mapped[Meal] = relationship("Meal", back_populates="like")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    user_details_id: Mapped[int] = mapped_column(Integer, ForeignKey('user_details.id'))

    user_details = relationship("UserDetails", back_populates="user")

    meal = relationship("Meal", back_populates="creator")

class UserDetails(Base):
    __tablename__ = "user_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, index=True)
    lastname: Mapped[str] = mapped_column(String, index=True)
    phone_number: Mapped[str] = mapped_column(String, index=True)
