from pydantic import BaseModel
from enum import Enum
from Model.Paging import Direction

class AgentType(str, Enum):
    Driver = 'Driver'

class AgentState(str, Enum):
    Draft = 'Draft'
    Active = 'Active'

class AgentInput(BaseModel):
    Id : str
    Name : str
    AgentType : AgentType

    
class AgentOutput(BaseModel):
    Id : str
    Name : str
    UserId : str
    CreatedDate : str
    UpdatedDate : str
    AgentState : AgentState
    AgentType : AgentType
    ProcessStartDate : str
    ProcessEndDate : str

class AgentListInput(BaseModel):
    AgentId : str
    Direction : Direction

class AgentListOutput(BaseModel):
    Agents : list[AgentOutput] = []