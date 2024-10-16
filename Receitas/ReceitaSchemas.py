from pydantic import BaseModel


class receitaBase(BaseModel):
    nome: str
    modoDePeparo: str
    tempoDePreparo: int


class ReceitaRequest(receitaBase):
    ...


class ReceitaResponse(receitaBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True
