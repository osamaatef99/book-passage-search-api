from fastapi.testclient import TestClient

from app.main import app
from app.search import Passage, PassageIndex

client = TestClient(app)


def test_finds_relevant_passage():
    r = client.get("/search", params={"q": "how many hours of sleep do adults need"})
    assert r.status_code == 200
    top = r.json()["results"][0]
    assert "Healthy Habits" in top["book"] and top["page"] == 1


def test_ranks_by_topic():
    r = client.get("/search", params={"q": "writing tests before fixing a bug"})
    assert "Learning Python" in r.json()["results"][0]["book"]


def test_no_match_returns_empty():
    assert client.get("/search", params={"q": "quantum chromodynamics"}).json()["results"] == []


def test_validation():
    assert client.get("/search", params={"q": "a"}).status_code == 422
    assert client.get("/search", params={"q": "sleep", "top_k": 99}).status_code == 422


def test_empty_index_rejected():
    import pytest
    with pytest.raises(ValueError):
        PassageIndex([])


def test_health():
    assert client.get("/health").json()["status"] == "ok"
