from datetime import datetime, timedelta

from sqlalchemy import Column, Enum, ForeignKey, Integer, String, Table, Float, DateTime, \
    UniqueConstraint
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


class Product(Base):
    __tablename__ = "product"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String)
    unit_of_measure: Mapped[str] = mapped_column(Enum(UnitOfMeasureEnum))
    value: Mapped[float] = mapped_column(Float)
    meal_id: Mapped[int] = mapped_column(Integer, ForeignKey("meal.id"))

    meal = relationship("Meal", back_populates="products")


class Meal(Base):
    __tablename__ = "meal"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    preparation: Mapped[str] = mapped_column(String)
    image_url: Mapped[str] = mapped_column(String, nullable=True)

    user = relationship("User", back_populates="meals")
    category = relationship("Category", secondary=meal_category_association, back_populates="meals")
    products = relationship("Product", back_populates="meal")
    comments = relationship("Comment", back_populates="meal")
    likes = relationship("Like", back_populates="meal")

class RefreshToken(Base):
    __tablename__ = "refresh_tokens"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, nullable=False)
    user_email = Column(String, ForeignKey("user.email"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(days=14))

    user = relationship("User", back_populates="refresh_tokens")

class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    email: Mapped[str] = mapped_column(String, unique=True)
    password: Mapped[str] = mapped_column(String)
    user_details_id: Mapped[int] = mapped_column(Integer, ForeignKey("user_details.id"))

    user_details = relationship("UserDetails", back_populates="user")
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete-orphan")
    meals = relationship("Meal", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    likes = relationship("Like", back_populates="user")


class UserDetails(Base):
    __tablename__ = "user_details"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)  # noqa: A003
    name: Mapped[str] = mapped_column(String, index=True)
    lastname: Mapped[str] = mapped_column(String, index=True)
    phone_number: Mapped[str] = mapped_column(String, index=True)

    user = relationship("User", back_populates="user_details")


class Comment(Base):
    __tablename__ = "comment"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    content: Mapped[str] = mapped_column(String)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    meal_id: Mapped[int] = mapped_column(Integer, ForeignKey("meal.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


    user = relationship("User", back_populates="comments")
    meal = relationship("Meal", back_populates="comments")


class Like(Base):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)  # noqa: A003
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    meal_id: Mapped[int] = mapped_column(Integer, ForeignKey("meal.id"))

    user = relationship("User", back_populates="likes")
    meal = relationship("Meal", back_populates="likes")

    __table_args__ = (UniqueConstraint('user_id', 'meal_id', name='_user_meal_uc'),)