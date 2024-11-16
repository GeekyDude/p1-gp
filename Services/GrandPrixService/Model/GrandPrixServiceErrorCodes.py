from pydantic import BaseModel

class Error(BaseModel):
    Num : int
    Message : str


#1-99 // User errors
UserNotAuthorized = {"Num" : 1, "Message" : "User is Not Authorized!"}
UserIdInvalid = {"Num" : 2, "Message" : "User Id is Invalid!"}