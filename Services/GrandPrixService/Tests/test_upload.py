from fastapi.testclient import TestClient

from datetime import date, datetime

from main import app

from globalvars import sharedState

client = TestClient(app)

def test_redirect():
    response = client.get("/upload")

    print(response)

    assert response.status_code == 200
    assert response.text == "Hello World!"
