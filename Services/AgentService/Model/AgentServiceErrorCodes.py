from pydantic import BaseModel

class Error(BaseModel):
    Num : int
    Message : str


#1-99 // User errors
UserNotAuthorized = {"Num" : 1, "Message" : "User is Not Authorized!"}
UserIdInvalid = {"Num" : 2, "Message" : "User Id is Invalid!"}

#200-299 // File Error
InvalidFileType = {"Num" : 200, "Message" : "Invalid File Type!"}
InvalidFeedStatus = {"Num" : 201, "Message" : "Invalid Feed Status!"}

#300-399 // Agent Errors
AgentIdInvalid = {"Num" : 300, "Message" : "Agent Id is Invalid!"}