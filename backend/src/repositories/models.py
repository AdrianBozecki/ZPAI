from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base
from enums import UnitOfMeasureEnum

meal_category_association = Table(
    "meal_category_association",
    Base.metadata,
    Column("meal_id", Integer, ForeignKey("meal.id")),
    Column("category_id", Integer, ForeignKey("category.id")),
)


class Category(Base):
    __tablename__ = "category"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String, unique=True)

    meals = relationship("Meal", secondary=meal_category_association, back_populates="category")


meal_product_association = Table(
    "meal_product_association",
    Base.metadata,
    Column("meal_id", Integer, ForeignKey("meal.id")),
    Column("product_id", Integer, ForeignKey("product.id")),
)


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String, unique=True)
    unit_of_measure: Mapped[str] = mapped_column(Enum(UnitOfMeasureEnum))

    meals = relationship("Meal", secondary=meal_product_association, back_populates="products")


class Meal(Base):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    preparation: Mapped[str] = mapped_column(String)

    user = relationship("User", back_populates="meals")
    category = relationship("Category", secondary=meal_category_association, back_populates="meals")
    products = relationship("Product", secondary=meal_product_association, back_populates="meals")


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    user_details_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_details.id"))

    user_details = relationship("UserDetails", back_populates="user")
    meals = relationship("Meal", back_populates="user")


class UserDetails(Base):
    __tablename__ = "user_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String, index=True)
    lastname: Mapped[str] = mapped_column(String, index=True)
    phone_number: Mapped[str] = mapped_column(String, index=True)

    user = relationship("User", back_populates="user_details")
