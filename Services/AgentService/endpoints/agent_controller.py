from fastapi import APIRouter, Request, HTTPException, BackgroundTasks

from globalvars import sharedState

from Model import AgentServiceErrorCodes

import constants
from Model.Agent import AgentInput, AgentOutput, AgentState, AgentListOutput, AgentListInput
from Model.Paging import Direction

from firebase_admin import firestore
from datetime import datetime

import google.cloud.exceptions

router = APIRouter()

@router.post("/Agent/", name="Post a Agent", description="Creates a new / updates existing Agent and returns the ID", response_model=AgentOutput)
async def post(agentInput: AgentInput, request: Request, background_tasks: BackgroundTasks):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    userId = 0
    valid, userId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=AgentServiceErrorCodes.UserNotAuthorized)

    effectiveUserId = userId

    if agentInput.Id == '':
        doc_ref = database.collection(constants.Agent(state)).document()
    else:
        doc_ref = database.collection(constants.Agent(state)).document(agentInput.Id)

    doc = await doc_ref.get()

    agent = {}

    if doc.exists:
        agent = doc.to_dict()
        if agent['UserId'] != userId:
            raise HTTPException(status_code=401, detail=AgentServiceErrorCodes.UserNotAuthorized)
        agent['Name'] = agentInput.Name
        agent['UpdatedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    else:
        agent['Id'] = doc_ref.id
        agent['Name'] = agentInput.Name
        agent['CreatedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        agent['UpdatedDate'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        agent['UserId'] = effectiveUserId
        agent['AgentState'] = AgentState.Draft
        agent['AgentType'] = agentInput.AgentType
        agent['ProcessStartDate'] = ''
        agent['ProcessEndDate'] = ''
        
    
    await doc_ref.set(agent, merge=True)
    
    response = AgentOutput(Id=agent['Id'], Name=agent['Name'], AgentState=agent['AgentState'], AgentType=agent['AgentType'], CreatedDate=agent['CreatedDate'], UpdatedDate=agent['UpdatedDate'], UserId=agent['UserId'], ProcessStartDate=agent['ProcessStartDate'], ProcessEndDate=agent['ProcessEndDate'])

    return response

@router.get("/Agent/{agentId}", name="Get Agent info", description="Fetch a User Info", response_model=AgentOutput)
async def get(request: Request, agentId: str):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=AgentServiceErrorCodes.UserNotAuthorized)

    doc_ref = database.collection(constants.Agent(state)).document(agentId)
    doc = await doc_ref.get()
    if doc.exists:
        if doc.to_dict()['UserId'] != tokenUserId:
            raise HTTPException(status_code=401, detail=AgentServiceErrorCodes.UserNotAuthorized)
        
        agent = doc.to_dict()
        return agent
    raise HTTPException(status_code=404, detail=AgentServiceErrorCodes.AgentIdInvalid)

@router.delete("/Agent/{userId}", name="Delete Agent", description="Delete", response_model=str)
async def delete(request: Request, userId: str):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=AgentServiceErrorCodes.UserNotAuthorized)

    doc_ref = database.collection(constants.User(state)).document(userId)
    doc = await doc_ref.get()
    if doc.exists:
        if doc.to_dict()['UserId'] != tokenUserId:
            raise HTTPException(status_code=401, detail=AgentServiceErrorCodes.UserNotAuthorized)
        await doc_ref.delete()

    return ""

@router.post("/Agents/", name="Get all Agents", description="Fetch all Agents", response_model=AgentListOutput)
async def get_agentss(agentListInput: AgentListInput, request: Request):
    state = sharedState.state
    db = state['db']
    auth = state['auth']
    database = db
    valid, tokenUserId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=AgentServiceErrorCodes.UserNotAuthorized)
    
    userId = tokenUserId
    
    if(agentListInput.AgentId == ""):
        doc_ref = database.collection(constants.Agent(state)).where('UserId', u'==', userId).order_by(u'Id', direction=firestore.Query.ASCENDING).limit(10)
    else:
        try:
            snapshot = database.collection(constants.Agent(state)).document(agentListInput.AgentId).get()
        except google.cloud.exceptions.NotFound:
            raise HTTPException(status_code=404, detail=AgentServiceErrorCodes.AgentIdInvalid)

        if(agentListInput.Direction == Direction.Ascending):
            doc_ref = database.collection(constants.Agent(state)).where('UserId', u'==', userId).order_by(u'Id', direction=firestore.Query.ASCENDING).end_before(snapshot).limit(10)
        else:
            doc_ref = database.collection(constants.Agent(state)).where('UserId', u'==', userId).order_by(u'Id', direction=firestore.Query.DESCENDING).starts_after(snapshot).limit(10)

    agents = []
    docs = doc_ref.stream()
    async for doc in docs:
        agent = doc.to_dict()
        agents.append(agent)

    return AgentListOutput(Agents=agents)