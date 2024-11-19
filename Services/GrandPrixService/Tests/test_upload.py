from fastapi.testclient import TestClient
from authentication import MockAuth

from Model.UploadURL import FileType, FileFormat

from main import app

from globalvars import sharedState

import requests

import firebase_admin
from firebase_admin import firestore, credentials

import uuid as UUID

import pytest
from httpx import ASGITransport, AsyncClient

sharedState.state['auth'] = MockAuth.Authorization()

@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'

@pytest.mark.asyncio(scope="session")
async def test1_file_upload():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        response = await client.post(
            "/Driver/",
            headers={"AccessToken": "abc"},
            json={"Id" : "", "Name": "TestDriver"},
        )

        assert response.status_code == 200
        driverId = response.json()['Id']

        response = await client.post(
            "/GetFileUploadURL",
            headers={"AccessToken": "abc"},
            json={"DriverId": driverId, "FileType": FileType.Driver, "FileFormat": FileFormat.python},
        )

        assert response.status_code == 200

        uploadURLResponse = response.json()

        f = open("./Tests/driver.py", "rb")

        upload_response = requests.put(uploadURLResponse['UploadUrl'], data=f, headers={"Content-Type": "text/x-python"})

        assert upload_response.status_code == 200

        f.close()
