from datetime import date, datetime
from pydantic import BaseModel, validator, EmailStr
from enum import Enum

class UserInput(BaseModel):
    Id : str
    Name : str
    DateOfBirth : date

    
class UserOutput(BaseModel):
    Id : str
    Name : str
    DateOfBirth : date
    Email : EmailStr