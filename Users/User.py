from sqlalchemy import Column, Integer, String

from database import Base, engine


class User(Base):
    __tablename__ = "users"
    
    def __init__(self, username: str, hased_password: str):
        self.username = username
        self.hased_password = hased_password
        

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hased_password = Column(String)


