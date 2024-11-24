from pydantic import BaseModel, validator
from enum import Enum


class FileFormat(str, Enum):
    python = 'python'

class UploadURLRequest(BaseModel):
    AgentId : str
    FileFormat : FileFormat

class UploadURLResponse(BaseModel):
    UploadUrl : str
    AgentId : str
    UserId : str
    FileFormat : FileFormat
