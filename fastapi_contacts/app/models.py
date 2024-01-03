# app/models.py
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    surname = Column(String, index=True)
    email = Column(String, index=True, unique=True)
    phone_number = Column(String)
    birthday = Column(String)  # Keep it as a string
    additional_info = Column(String, nullable=True)

# app/schemas.py
from pydantic import BaseModel

class Contact(BaseModel):
    name: str
    surname: str
    email: str
    phone_number: str
    birthday: str  # Keep it as a string
    additional_info: str = None

