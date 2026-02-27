from fastapi.testclient import TestClient
from backend.main import app
from backend.app.models.trade import create_db_and_tables

client = TestClient(app)
create_db_and_tables()

def test_read_portfolio():
    assert client.get("/api/portfolio").status_code == 200

def test_read_trades():
    assert client.get("/api/trades").status_code == 200
