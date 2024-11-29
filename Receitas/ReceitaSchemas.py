from pydantic import BaseModel


class receitaBase(BaseModel):
    id: int
    nome: str
    modoDePeparo: str
    tempoDePreparo: int
    id_creator: int
    nome_creator: str


class ReceitaRequest(receitaBase):
    nome: str
    modoDePeparo: str
    tempoDePreparo: int
    id_creator: int
    nome_creator: str


class ReceitaResponse(receitaBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
