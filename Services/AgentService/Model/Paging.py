from pydantic import BaseModel
from enum import Enum

class Direction(str, Enum):
    Ascending = 'Ascending'
    Descending = 'Descending'