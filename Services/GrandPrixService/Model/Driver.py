from pydantic import BaseModel
from enum import Enum
from Model.Paging import Direction

class DriverState(str, Enum):
    Draft = 'Draft'
    Active = 'Active'

class DriverInput(BaseModel):
    Id : str
    Name : str

    
class DriverOutput(BaseModel):
    Id : str
    Name : str
    UserId : str
    CreatedDate : str
    UpdatedDate : str
    DriverState : DriverState
    ProcessStartDate : str
    ProcessEndDate : str

class DriverListInput(BaseModel):
    DriverId : str
    Direction : Direction

class DriverListOutput(BaseModel):
    Drivers : list[DriverOutput] = []