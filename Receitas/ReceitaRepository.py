from typing import List, Type

from sqlalchemy.orm import Session

from Receitas import Receita
from Receitas.Receita import Receita as ReceitaClass


class ReceitaRepository:
    @staticmethod
    def find_all(db: Session) -> list[Type[ReceitaClass]]:
        return db.query(ReceitaClass).all()

    @staticmethod
    def seeMyRecipes(db: Session, id: int):
        return db.query()

    @staticmethod
    def save(db: Session, receita: ReceitaClass) -> Receita:
        if receita.id:
            db.merge(receita)
        else:
            db.add(receita)
        db.commit()
        return receita

    @staticmethod
    def find_by_id_user(db: Session, id_user: int) -> list[Type[ReceitaClass]]:
        return db.query(ReceitaClass).filter(ReceitaClass.id_creator == id_user).all()

    @staticmethod
    def find_by_id(db: Session, id: int) -> Receita:
        return db.query(Receita).filter(Receita.id == id).first()

    @staticmethod
    def exists_by_id(db: Session, id: int) -> bool:
        return db.query(Receita).filter(Receita.id == id).first() is not None

    @staticmethod
    def delete_by_id(db: Session, id: int) -> None:
        receita = db.query(Receita).filter(Receita.id == id).first()
        if receita is not None:
            db.delete(receita)
            db.commit()

