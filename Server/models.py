from sqlalchemy import Column, Integer, String, ForeignKey, Table, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

user_list = Table(
    "user_list",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id")),
    Column("list_id", Integer, ForeignKey("shopping_lists.id")),
)


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    shopping_lists = relationship("ShoppingList", secondary=user_list, back_populates="users")


class ShoppingList(Base):
    __tablename__ = "shopping_lists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    users = relationship("Users", secondary=user_list, back_populates="shopping_lists")
    items = relationship("Item", back_populates="list")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    list_id = Column(Integer, ForeignKey("shopping_lists.id"))
    list = relationship("ShoppingList", back_populates="items")
    bought = Column(Boolean, index=True)
    quantity = Column(Integer, index=True)
