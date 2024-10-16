from sqlalchemy import Column, Integer, String

from database import Base


class Receita(Base):
    __tablename__ = "Receitas"

    id: int = Column(Integer, primary_key=True, index=True)
    nome: str = Column(String(100), nullable=False)
    modoDePeparo: str = Column(String(2550), nullable=False)
    tempoDePreparo: int = Column(Integer, nullable=False)
