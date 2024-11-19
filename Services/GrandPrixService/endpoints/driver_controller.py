from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from globalvars import sharedState

from Model import GrandPrixServiceErrorCodes

import constants
from Model.Driver import DriverInput, DriverOutput, DriverState, DriverListOutput, DriverListInput
from Model.Paging import Direction

from firebase_admin import firestore
from datetime import datetime

import google.cloud.exceptions

router = APIRouter()

@router.post("/Driver/", name="Post a user", description="Creates a new / updates existing user and returns the ID", response_model=DriverOutput)
async def post(driverInput: DriverInput, request: Request, background_tasks: BackgroundTasks):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    userId = 0
    valid, userId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    effectiveUserId = userId

    if driverInput.Id == '':
        doc_ref = database.collection(constants.Driver(state)).document()
    else:
        doc_ref = database.collection(constants.Driver(state)).document(driverInput.Id)

    doc = await doc_ref.get()

    driver = {}

    if doc.exists:
        driver = doc.to_dict()
        if driver['UserId'] != userId:
            raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)
        driver['Name'] = driverInput.Name
        driver['UpdatedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        driver['Id'] = doc_ref.id
        driver['Name'] = driverInput.Name
        driver['CreatedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        driver['UpdatedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        driver['UserId'] = effectiveUserId
        driver['DriverState'] = DriverState.Draft
        driver['ProcessStartDate'] = ''
        driver['ProcessEndDate'] = ''
        
    
    await doc_ref.set(driver, merge=True)
    
    response = DriverOutput(Id=driver['Id'], Name=driver['Name'], DriverState=driver['DriverState'], CreatedDate=driver['CreatedDate'], UpdatedDate=driver['UpdatedDate'], UserId=driver['UserId'], ProcessStartDate=driver['ProcessStartDate'], ProcessEndDate=driver['ProcessEndDate'])

    return response

@router.get("/Driver/{driverId}", name="Get user info", description="Fetch a User Info", response_model=DriverOutput)
async def get(request: Request, driverId: str):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    doc_ref = database.collection(constants.Driver(state)).document(driverId)
    doc = await doc_ref.get()
    if doc.exists:
        if doc.to_dict()['UserId'] != tokenUserId:
            raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)
        
        driver = doc.to_dict()
        return driver
    raise HTTPException(status_code=404, detail=GrandPrixServiceErrorCodes.DriverIdInvalid)

@router.delete("/Driver/{userId}", name="Delete user info", description="Delete", response_model=str)
async def delete(request: Request, userId: str):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)

    doc_ref = database.collection(constants.User(state)).document(userId)
    doc = await doc_ref.get()
    if doc.exists:
        if doc.to_dict()['UserId'] != tokenUserId:
            raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)
        await doc_ref.delete()

    return ""

@router.post("/Drivers/", name="Get all drivers", description="Fetch all drivers", response_model=DriverListOutput)
async def get_drivers(driverListInput: DriverListInput, request: Request):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)
    
    userId = tokenUserId
    
    if(driverListInput.DriverId == ""):
        doc_ref = database.collection(constants.Driver(state)).where('UserId', u'==', userId).order_by(u'Id', direction=firestore.Query.ASCENDING).limit(10)
    else:
        try:
            snapshot = database.collection(constants.Driver(state)).document(driverListInput.DriverId).get()
        except google.cloud.exceptions.NotFound:
            raise HTTPException(status_code=404, detail=GrandPrixServiceErrorCodes.DriverNotFound)

        if(driverListInput.Direction == Direction.Ascending):
            doc_ref = database.collection(constants.Driver(state)).where('UserId', u'==', userId).order_by(u'Id', direction=firestore.Query.ASCENDING).end_before(snapshot).limit(10)
        else:
            doc_ref = database.collection(constants.Driver(state)).where('UserId', u'==', userId).order_by(u'Id', direction=firestore.Query.DESCENDING).starts_after(snapshot).limit(10)

    drivers = []
    docs = doc_ref.stream()
    async for doc in docs:
        driver = doc.to_dict()
        drivers.append(driver)

    return DriverListOutput(Drivers=drivers)