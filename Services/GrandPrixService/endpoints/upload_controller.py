from fastapi import APIRouter, Request, HTTPException, BackgroundTasks
from fastapi.responses import RedirectResponse, HTMLResponse

from globalvars import sharedState

import constants

from datetime import datetime

import pytz

router = APIRouter()

@router.get("/upload")
async def redirect(request: Request, background_tasks: BackgroundTasks):
    """
    Uploads a driver code with given ID.
    """
    try:
    
        return HTMLResponse(content="Hello World!", status_code=200)
    
    except Exception as e:
        # An error occurred
        print(e)
        # print stack trace
        import traceback
        traceback.print_exc()

        raise HTTPException(status_code=500, detail="An error occurred")