from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from routers import router

import firebase_admin
from firebase_admin import firestore_async, credentials

from google.cloud import bigquery

from globalvars import sharedState

from os.path import exists


def ReadFile(path):
    with open(path, 'r') as f:
        return f.read().rstrip()    
if (not len(firebase_admin._apps)):
    if exists("huntfishbuddy-test-serviceaccount.json"):
        cred = credentials.Certificate("huntfishbuddy-test-serviceaccount.json")
        default_app = firebase_admin.initialize_app(cred)
        sharedState.state['ServiceAccountKey'] = 'huntfishbuddy-test-serviceaccount.json'
        sharedState.state['Environment'] = 'test'
    else:
        cred = credentials.Certificate('/mnt/hfb/serviceaccount')
        default_app = firebase_admin.initialize_app(cred)
        sharedState.state['ServiceAccountKey'] = '/mnt/hfb/serviceaccount'
        sharedState.state['Environment'] = ''
sharedState.state['db'] = firestore_async.client()
sharedState.state['bq'] = bigquery.Client.from_service_account_json(sharedState.state['ServiceAccountKey'])

# fastapi app
app = FastAPI(
    title="GrandPrix Serivce API",
    description="API for the GrandPrix service",
    version="0.1"
)

origins = [
    "*", # allow all origins
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


# uvicorn main:app --reload