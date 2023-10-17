from pydantic import BaseModel
from typing import List, Union


class ItemBase(BaseModel):
    name: str
    quantity: int
    bought: bool = False


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class ShoppingListBase(BaseModel):
    name: str


class ShoppingListCreate(ShoppingListBase):
    pass


class ShoppingList(ShoppingListBase):
    id: int
    items: List[Item]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class UserWithoutList(UserBase):
    id: int


class User(UserWithoutList):
    shopping_lists: List[ShoppingList] = []

    class Config:
        orm_mode = True


class ShoppingListWithUsers(ShoppingList):
    users: List[UserWithoutList] = []


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None
