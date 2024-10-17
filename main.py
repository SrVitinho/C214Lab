from fastapi import FastAPI, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from Receitas import Receita, ReceitaRepository
from Users.CreateUser import CreateUser
from Users.UserRepository import get_user_by_username, create_user, authenticate_user, create_acess_token, verify_token
from database import engine, Base, get_db
from Receitas.ReceitaRepository import ReceitaRepository
from Receitas import ReceitaSchemas
from Receitas.Receita import Receita as ReceitaClass
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi.middleware.cors import CORSMiddleware
from keys import key_jtw as key

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/receita/create", response_model=ReceitaSchemas.ReceitaResponse, status_code=status.HTTP_201_CREATED)
def create(request: ReceitaSchemas.ReceitaRequest, db: Session = Depends(get_db)):
    receita = ReceitaRepository.save(db, ReceitaClass(**request.dict()))
    return ReceitaSchemas.ReceitaResponse.from_orm(receita)


@app.get("/receita/cursos", response_model=list[ReceitaSchemas.ReceitaResponse])
def find_all(db: Session = Depends(get_db)):
    receitas = ReceitaRepository.find_all(db)
    return [ReceitaSchemas.ReceitaResponse.from_orm(receita) for receita in receitas]


@app.get("/receita/cursos/{id}", response_model=ReceitaSchemas.ReceitaResponse)
def find_by_id(id: int, db: Session = Depends(get_db)):
    receita = ReceitaRepository.find_by_id(db, id)
    if not receita:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="receita não encontrado"
        )
    return ReceitaSchemas.ReceitaResponse.from_orm(receita)


@app.delete("/receita/cursos/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_by_id(id: int, db: Session = Depends(get_db)):
    if not ReceitaRepository.exists_by_id(db, id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="receita não encontrado"
        )
    ReceitaRepository.delete_by_id(db, id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.post("/register")
def register_user(users: CreateUser, db: Session = Depends(get_db)):
    return create_user(db=db, user=users)


@app.post("/token")
def login_for_acess_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    users = authenticate_user(form_data.username, form_data.password, db)
    if not users:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid credentials",
                            headers={"WWW-Authenticate": "Bearer"}
                            )
    acess_token = create_acess_token(
        data={"sub": users.username}
    )
    return {"acess_token": acess_token, "token_type": "bearer"}


@app.get("/verify-token/{token}")
async def verify_users_token(token: str):
    verify_token(token=token)
    return {"message": "Token is valid"}