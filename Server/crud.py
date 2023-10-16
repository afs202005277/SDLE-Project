from sqlalchemy.orm import Session
import models
import schemas


def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.Users(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int):
    return db.query(models.Users).filter(models.Users.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def create_shopping_list(db: Session, shopping_list: schemas.ShoppingListCreate, user_id: int):
    db_shopping_list = models.ShoppingList(**shopping_list.model_dump(), users=[models.Users(id=user_id)])
    db.add(db_shopping_list)
    db.commit()
    db.refresh(db_shopping_list)
    return db_shopping_list


def get_shopping_lists(db: Session, user_id: int):
    return db.query(models.ShoppingList).filter(models.ShoppingList.users.any(id=user_id)).all()


def get_shopping_list(db: Session, list_id: int, user_id: int):
    return db.query(models.ShoppingList).filter(models.ShoppingList.id == list_id,
                                                models.ShoppingList.users.any(id=user_id)).first()


def create_item(db: Session, item: schemas.ItemCreate, list_id: int):
    db_item = models.Item(**item.model_dump(), list_id=list_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, list_id: int):
    return db.query(models.Item).filter(models.Item.list_id == list_id).all()


def get_item(db: Session, item_id: int):
    return db.query(models.Item).filter(models.Item.id == item_id).first()
