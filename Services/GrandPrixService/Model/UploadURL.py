from pydantic import BaseModel, validator
from enum import Enum

class FileType(str, Enum):
    Driver = 'Driver'

class FileFormat(str, Enum):
    python = 'python'

class UploadURLRequest(BaseModel):
    DriverId : str
    FileType : FileType
    FileFormat : FileFormat

class UploadURLResponse(BaseModel):
    UploadUrl : str
    DriverId : str
    UserId : str
    FileFormat : FileFormat
    FileType : FileType