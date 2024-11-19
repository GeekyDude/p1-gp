from email.policy import default
from fastapi import APIRouter, Request, HTTPException

from globalvars import sharedState

from Model.UploadURL import UploadURLRequest, UploadURLResponse, FileType, FileFormat

from Model import GrandPrixServiceErrorCodes

import constants

from google.cloud import storage

from datetime import timedelta, datetime 

router = APIRouter()

@router.post("/GetFileUploadURL", name="Upload File", description="Get secure links to upload files.", response_model=UploadURLResponse)
async def main(request: Request, UploadURLRequest: UploadURLRequest):
    state = sharedState.state
    db = sharedState.state['db']
    auth = sharedState.state['auth']

    userId = 0
    valid, userId = auth.IsUserAuthorized(request.headers)
    if not valid:
        raise HTTPException(status_code=401, detail=GrandPrixServiceErrorCodes.UserNotAuthorized)
    
    driverId = UploadURLRequest.DriverId

    doc_ref = db.collection(constants.Driver(state)).document(driverId)

    doc = await doc_ref.get()

    if(not doc.exists or userId != doc.to_dict()['UserId']):
      raise HTTPException(status_code=404, detail=GrandPrixServiceErrorCodes.DriverIdInvalid)
    
    client = storage.Client.from_service_account_json(sharedState.state['ServiceAccountKey'])

    (bucketName, blobFile, contentType) = GetBucketName(UploadURLRequest.FileType, sharedState.state['Environment'])

    if(bucketName == "unknown"):
      raise HTTPException(status_code=400, detail=GrandPrixServiceErrorCodes.InvalidFileType)

    bucket = client.bucket(bucketName)

    #blobFile = uuid.uuid4().hex + ".csv"

    blob = bucket.blob(driverId + "/" + blobFile)
      
    url = blob.generate_signed_url(version="v4", expiration=timedelta(minutes=60), method="PUT", content_type=contentType)

    response = UploadURLResponse(FileType=UploadURLRequest.FileType, UploadUrl=url, DriverId=driverId, FileFormat=UploadURLRequest.FileFormat, UserId=userId)

    return response

def GetBucketName(feedtype, env):
   if feedtype == FileType.Driver:
      return (env + "p1-gp-drivers", "test.py" if env == "test" else "driver.py", "text/x-python")
   else:
      return ("unknown", "", "")