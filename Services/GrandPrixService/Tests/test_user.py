import asyncio
from fastapi.testclient import TestClient
from authentication import MockAuth

from datetime import date, datetime

from main import app

from globalvars import sharedState

import pytest
from httpx import ASGITransport, AsyncClient

# client = TestClient(app)

sharedState.state['auth'] = MockAuth.Authorization()

#get date from string
def get_date(date_string):
    return datetime.strptime(date_string, '%Y-%m-%d').date()

# get date as string
def get_date_string(date):
    return date.strftime('%Y-%m-%d')

async def createUser(client):
    response = await client.post(
        "/User",
        headers={"AccessToken": "abc"},
        json={"Id": "123", "Name": "TestParent", "DateOfBirth" : "1980-01-01"},
    )

    assert response.status_code == 200
    
    response = await client.post(
        "/User",
        headers={"AccessToken": "def"},
        json={"Id": "456", "Name": "TestChild", "DateOfBirth" : get_date_string(datetime.now())},
    )

    assert response.status_code == 200

@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'

@pytest.mark.anyio
async def test_user():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:

    
        response = await client.delete(
            "/User/" + "123",
            headers={"AccessToken": "abc"},
        )

        response = await client.delete(
            "/User/" + "456",
            headers={"AccessToken": "abc"},
        )

        response = await client.get(
            "/User/" + "1234",
            headers={"AccessToken": "abc"},
        )

        json = response.json()
        print(json)
        assert response.status_code == 401
        assert json["detail"]["Num"] == 1
        
        await createUser(client)

        response = await client.get(
            "/User/" + "123",
            headers={"AccessToken": "abc"},
        )

        assert response.status_code == 200

        response = await client.get(
            "/User/" + "456",
            headers={"AccessToken": "def"},
        )

        print(response.json())

        assert response.status_code == 200
