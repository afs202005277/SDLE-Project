from pydantic import BaseModel
from typing import List, Union


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


class ItemBase(BaseModel):
    name: str
    quantity: int


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    bought: bool

    class Config:
        orm_mode = True


class ShoppingListBase(BaseModel):
    name: str


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingList(ShoppingListBase):
    id: int
    items = List[Item]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    shoppingLists: List[ShoppingList] = []

    class Config:
        orm_mode = True
