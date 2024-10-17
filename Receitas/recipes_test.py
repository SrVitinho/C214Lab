from unittest.mock import Mock

import pytest

from Receitas.Receita import Receita as ReceitaClass
from Receitas.ReceitaRepository import ReceitaRepository

from sqlalchemy.orm import Session


@pytest.fixture
def mock_db():
    return Mock(spec=Session) 


@pytest.fixture
def mock_receita():
    return ReceitaClass(nome="New Recipe", modoDePeparo="A delicious dish", tempoDePreparo=30, id=1)


def test_save_new_receita(mock_db, mock_receita):
    mock_receita.id = None  

    saved_receita = ReceitaRepository.save(mock_db, mock_receita)

    assert saved_receita is mock_receita
    mock_db.add.assert_called_once_with(mock_receita)
    mock_db.commit.assert_called_once()


def test_save_existing_receita(mock_db, mock_receita):
    mock_receita.id = 1 

    saved_receita = ReceitaRepository.save(mock_db, mock_receita)

    assert saved_receita is mock_receita
    mock_db.merge.assert_called_once_with(mock_receita)
    mock_db.commit.assert_called_once()


def test_find_all_empty(mock_db):
    mock_db.query.return_value.all.return_value = []

    recipes = ReceitaRepository.find_all(mock_db)

    assert recipes == []

def test_find_all_multiple_recipes(mock_db, mock_receita):
    mock_recipes = [mock_receita, Mock(spec=ReceitaClass), Mock(spec=ReceitaClass)]
    mock_db.query.return_value.all.return_value = mock_recipes

    recipes = ReceitaRepository.find_all(mock_db)

    assert recipes == mock_recipes