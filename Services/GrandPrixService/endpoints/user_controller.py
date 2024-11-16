from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from globalvars import sharedState

from Model import GrandPrixServiceErrorCodes

import constants
from Model.User import UserInput, UserOutput

from firebase_admin import firestore
from datetime import datetime

router = APIRouter()

@router.post("/User", name="Post a user", description="Creates a new / updates existing user and returns the ID", response_model=UserOutput)
async def post(User: UserInput, request: Request, background_tasks: BackgroundTasks):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    userId = 0
    valid, userId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    if User.Id == '':
        user.Id = userId

    if User.Id != userId:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    #If the user Date Of birth is less than 18 years, then the user is a child

    effectiveUserId = userId

    print("before")

    doc_ref = database.collection(constants.User(state)).document(effectiveUserId)
    doc = await doc_ref.get()

    print("after")

    user = {}

    if doc.exists and 'Email' in doc.to_dict():
        user = doc.to_dict()
        user['Name'] = User.Name
        user['DateOfBirth'] = User.DateOfBirth.strftime('%Y-%m-%d')
    else:
        lookedUpUser = auth.GetUser(userId)
        user['Id'] = effectiveUserId
        user['Name'] = User.Name
        user['DateOfBirth'] = User.DateOfBirth.strftime('%Y-%m-%d')
        user['Email'] = lookedUpUser['email']
    
    await doc_ref.set(user, merge=True)
    
    response = UserOutput(Id=userId, Name=User.Name, DateOfBirth=User.DateOfBirth, Email=user['Email'])

    return response

@router.get("/User/{userId}", name="Get user info", description="Fetch a User Info", response_model=UserOutput)
async def get(request: Request, userId: str):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    if tokenUserId != userId:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    doc_ref = database.collection(constants.User(state)).document(userId)
    doc = await doc_ref.get()
    if doc.exists:
        user = doc.to_dict()
        return user
    raise HTTPException(status_code=404, detail=GrandPrixServiceErrorCodes.UserIdInvalid)

@router.delete("/User/{userId}", name="Delete user info", description="Delete", response_model=str)
async def delete(request: Request, userId: str):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    if tokenUserId != userId:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    doc_ref = database.collection(constants.User(state)).document(userId)
    doc = await doc_ref.get()
    if doc.exists:
        await doc_ref.delete()

    return ""
