from typing import List, Type
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from keys import key_jtw as key
from passlib.context import CryptContext
from Users.User import User
from sqlalchemy.orm import Session

from Users.CreateUser import CreateUser

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

SECRET_KEY = key
ALGORITHM = "HS256"
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: CreateUser):
    db_user = get_user_by_username(db, username=user.username)
    print(db_user)
    if db_user:
        raise HTTPException(status_code=400, detail="Usuario ja cadastrado!")
    hased_password = pwd_context.hash(user.password)
    db_user = User(username=user.username, hased_password=hased_password)
    db.add(db_user)
    db.commit()
    return {"detail": "Cadastrado"}


def authenticate_user(db: Session, username: str, password: str):
    users = db.query(User).filter(User.username == username).first()
    if not users:
        return False
    if not pwd_context.verify(password, users.hased_password):
        return False
    return users


def create_acess_token(data: dict):
    to_encode = data.copy()
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Depends(oauth2_schema)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=403, detail="Invalid Token")
        return payload
    except JWTError:
        raise HTTPException(status_code=403, detail="Invalid Token")
