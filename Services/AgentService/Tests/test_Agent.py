import asyncio
from fastapi.testclient import TestClient
from authentication import MockAuth

from datetime import date, datetime

from main import app

from globalvars import sharedState

import pytest
from httpx import ASGITransport, AsyncClient

from Model.Paging import Direction

from Model.Agent import AgentType

# client = TestClient(app)

sharedState.state['auth'] = MockAuth.Authorization()

@pytest.fixture(scope="module")
def anyio_backend():
    return 'asyncio'

@pytest.mark.asyncio(scope="session")
async def test_agent():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:

        response = await client.post(
            "/Agents/",
            headers={"AccessToken": "abc"},
            json={"AgentId": "", "Direction" : Direction.Ascending},
        )

        assert response.status_code == 200

        json = response.json()
        agents = json['Agents']

        for agent in agents:
            response = await client.delete(
                "/Agent/" + agent['Id'],
                headers={"AccessToken": "abc"},
            )

    
        response = await client.post(
            "/Agent/",
            headers={"AccessToken": "abc"},
            json={"Id" : "", "Name": "Kimi", "AgentType": AgentType.Driver},
        )                

        assert response.status_code == 200
        json = response.json()

        agentId = json['Id']

        response = await client.post(
            "/Agent/",
            headers={"AccessToken": "abc"},
            json={"Id" : agentId, "Name": "Kimi Raikonnen", "AgentType": AgentType.Driver},
        )

        assert response.status_code == 200

        response = await client.get(
            "/Agent/" + json['Id'],
            headers={"AccessToken": "abc"},
        )

        assert response.status_code == 200

        json = response.json()

        assert json['Name'] == "Kimi Raikonnen"

        response = await client.delete(
            "/Agent/" + json['Id'],
            headers={"AccessToken": "abc"},
        )

        assert response.status_code == 200


