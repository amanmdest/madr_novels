from fastapi.testclient import TestClient

from madr_novels import app

cliente = TestClient(app)
