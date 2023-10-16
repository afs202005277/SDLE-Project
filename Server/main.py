from typing import Annotated, Union, List, Dict
from pydantic import BaseModel
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from jose import JWTError
from sqlalchemy.orm import Session

from Server import authentication, exceptions

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], expose_headers=["*"])


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Union[str, None] = None


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def authenticate_user(email: str, password: str, db: Session):
    user = crud.get_user_by_email(email, db)
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
    return crud.get_user_by_email(token_data.email, db)


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Session = Depends(get_db)):
    user = firewall(token, db)
    if user is None:
        raise exceptions.credentials_exception
    return user


@app.post("/token", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
                                 db: Session = Depends(get_db)):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise exceptions.invalid_email_or_pwd_exception
    access_token = authentication.create_access_token_expires(user.email)
    return {"access_token": access_token, "token_type": "bearer"}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(email=user.email, db=db)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    user.password = authentication.get_password_hash(user.password)
    return crud.create_user(db, user)


# Command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
