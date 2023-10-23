from typing import Annotated

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError
from sqlalchemy.orm import Session

import crud
import authentication
import schemas
import exceptions
from database import SessionLocal

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(db, email)
    if not user:
        return False
    if not authentication.verify_password(password, user.password):
        return False
    return user


def firewall(token: str, db: Session):
    try:
        payload = authentication.decode_token(token)
        email: str = payload.get("sub")
        if email is None:
            raise exceptions.credentials_exception
        token_data = schemas.TokenData(email=email)
    except JWTError:
        raise exceptions.credentials_exception
    return crud.get_user_by_email(db, token_data.email)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = firewall(token, db)
    if user is None:
        raise exceptions.credentials_exception
    return user


@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise exceptions.invalid_email_or_pwd_exception
    access_token = authentication.create_access_token_expires(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: Annotated[schemas.User, Depends(get_current_user)]):
    return current_user


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise exceptions.email_already_registered
    user.password = authentication.get_password_hash(user.password)
    return crud.create_user(db, user)


@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.delete_user(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.get("/users/", response_model=list[schemas.User])
def read_users(token: Annotated[str, Depends(oauth2_scheme)], skip: int = 0, limit: int = 100,
               db: Session = Depends(get_db)):
    firewall(token, db)
    users = crud.get_users(db, skip=skip, limit=limit)
    print(users)
    return users


@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    auth_user = firewall(token, db)
    if auth_user.id != user_id:
        raise exceptions.private_info_exception
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@app.post("/shopping_lists/", response_model=schemas.ShoppingList)
def create_shopping_list(token: Annotated[str, Depends(oauth2_scheme)], shopping_list: schemas.ShoppingListCreate,
                         db: Session = Depends(get_db)):
    user = firewall(token, db)
    return crud.create_shopping_list(db, shopping_list, user)


@app.get("/shopping_lists/{list_id}", response_model=schemas.ShoppingListWithUsers)
def read_shopping_list(list_id: int, user_id: int, db: Session = Depends(get_db)):
    shopping_list = crud.get_shopping_list(db, list_id, user_id)
    if shopping_list is None:
        raise HTTPException(status_code=404, detail="Shopping list not found")
    return shopping_list


@app.get("/shopping_lists/", response_model=list[schemas.ShoppingListWithUsers])
def read_shopping_lists(user_id: int, db: Session = Depends(get_db)):
    return crud.get_shopping_lists(db, user_id)


@app.post("/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, list_id: int, db: Session = Depends(get_db)):
    return crud.create_item(db, item, list_id)


@app.get("/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    item = crud.get_item(db, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.get("/items/", response_model=list[schemas.Item])
def read_items(list_id: int, db: Session = Depends(get_db)):
    return crud.get_items(db, list_id)


# Command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
