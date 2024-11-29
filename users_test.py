from unittest.mock import Mock, patch
from Users.User import User
from Users.UserRepository import create_user, authenticate_user, get_user_by_username
from Users.CreateUser import CreateUser
from passlib.context import CryptContext
import pytest
from sqlalchemy.orm import Session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@pytest.fixture
def mock_db():
    return Mock(spec=Session)

@pytest.fixture
def user_data():
    return CreateUser(username="new_user", password="secure_password")

@pytest.fixture
def user_data_created():
    return User(username="new_user",  hased_password=pwd_context.hash("secure_password"))

def test_create_user_success(mock_db, user_data):
    with patch('Users.UserRepository.get_user_by_username', return_value=None):
        result = create_user(mock_db, user_data)
        assert result == {"detail": "Cadastrado"}
        mock_db.add.assert_called_once()
        mock_db.commit.assert_called_once()

def test_create_user_already_exists(mock_db, user_data):
    with patch('Users.UserRepository.get_user_by_username', return_value=Mock()):
        with pytest.raises(Exception) as excinfo:
            create_user(mock_db, user_data)
        assert excinfo.value.status_code == 400
        assert excinfo.value.detail == "Usuario ja cadastrado!"
        mock_db.add.assert_not_called()
        mock_db.commit.assert_not_called()

def test_get_user_by_username_found(mock_db, user_data):
    mock_user = Mock(user_data)
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    username = "existing_user"

    user = get_user_by_username(mock_db, username)

    assert user == mock_user

def test_get_user_by_username_not_found(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    username = "nonexistent_user"

    user = get_user_by_username(mock_db, username)

    assert user is None

def test_authenticate_user_success(mock_db, user_data_created):
    mock_user = Mock(user_data_created)
    mock_user.username = "new_user"
    mock_user.hased_password = pwd_context.hash("secure_password")
    mock_db.query.return_value.filter.return_value.first.return_value = mock_user
    username = "new_user"
    password = "secure_password" 

    user = authenticate_user(mock_db, username, password)

    assert user == mock_user

def test_authenticate_user_wrong_username(mock_db):
    mock_db.query.return_value.filter.return_value.first.return_value = None
    username = "nonexistent_user"
    password = "any_password"

    user = authenticate_user(mock_db, username, password)

    assert user is False
