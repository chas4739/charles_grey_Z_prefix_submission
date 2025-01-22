from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float

class Item(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True, index=True)
    userId = Column(Integer)
    itemName = Column(String)
    itemDescription = Column(String)
    itemQuantity = Column(Integer)

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    username = Column(String, unique=True, index=True)
    password = Column(String)