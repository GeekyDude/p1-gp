import asyncio
from fastapi.testclient import TestClient
from authentication import MockAuth

from datetime import date, datetime

from main import app

from globalvars import sharedState

import pytest
from httpx import ASGITransport, AsyncClient

from Model.Paging import Direction

# client = TestClient(app)

sharedState.state['auth'] = MockAuth.Authorization()

@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'

@pytest.mark.asyncio(scope="session")
async def test_driver():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:

        response = await client.post(
            "/Drivers/",
            headers={"AccessToken": "abc"},
            json={"DriverId": "", "Direction" : Direction.Ascending},
        )

        assert response.status_code == 200

        json = response.json()
        drivers = json['Drivers']

        for driver in drivers:
            response = await client.delete(
                "/Driver/" + driver['Id'],
                headers={"AccessToken": "abc"},
            )

    
        response = await client.post(
            "/Driver/",
            headers={"AccessToken": "abc"},
            json={"Id" : "", "Name": "Kimi"},
        )                

        assert response.status_code == 200
        json = response.json()

        driverId = json['Id']

        response = await client.post(
            "/Driver/",
            headers={"AccessToken": "abc"},
            json={"Id" : driverId, "Name": "Kimi Raikonnen"},
        )

        assert response.status_code == 200

        response = await client.get(
            "/Driver/" + json['Id'],
            headers={"AccessToken": "abc"},
        )

        assert response.status_code == 200

        json = response.json()

        assert json['Name'] == "Kimi Raikonnen"

        response = await client.delete(
            "/Driver/" + json['Id'],
            headers={"AccessToken": "abc"},
        )

        assert response.status_code == 200


