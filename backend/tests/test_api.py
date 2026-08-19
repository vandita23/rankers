import io

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health():
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok"}


def test_chat_valid():
    res = client.post("/api/v1/chat", json={"message": "Why are my leaves yellow?", "language": "en"})
    assert res.status_code == 200
    body = res.json()
    assert body["reply"]
    assert body["language"] == "en"


def test_chat_missing_message():
    res = client.post("/api/v1/chat", json={"language": "en"})
    assert res.status_code == 422


def test_chat_invalid_language():
    res = client.post("/api/v1/chat", json={"message": "hi", "language": "fr"})
    assert res.status_code == 422


def test_weather_requires_location():
    res = client.get("/api/v1/weather")
    assert res.status_code == 422


def test_weather_valid():
    res = client.get("/api/v1/weather", params={"location": "Barabanki"})
    assert res.status_code == 200
    body = res.json()
    assert body["location"] == "Barabanki"
    assert len(body["forecast"]) == 5


def test_schemes_query():
    res = client.post("/api/v1/schemes/query", json={"question": "loan for seeds", "language": "en"})
    assert res.status_code == 200
    body = res.json()
    assert len(body["schemes"]) >= 1


def test_disease_predict_valid_image():
    fake_image = io.BytesIO(b"fake-image-bytes")
    res = client.post(
        "/api/v1/disease/predict",
        files={"image": ("leaf.jpg", fake_image, "image/jpeg")},
        data={"language": "en"},
    )
    assert res.status_code == 200
    body = res.json()
    assert "disease" in body
    assert 0 <= body["confidence"] <= 100


def test_disease_predict_rejects_bad_type():
    fake_file = io.BytesIO(b"not-an-image")
    res = client.post(
        "/api/v1/disease/predict",
        files={"image": ("leaf.txt", fake_file, "text/plain")},
        data={"language": "en"},
    )
    assert res.status_code == 422


def test_dashboard_fallback_without_db():
    res = client.get("/api/v1/dashboard")
    assert res.status_code == 200
    body = res.json()
    assert body["farmer"]["name"]
    assert isinstance(body["alerts"], list)
    assert isinstance(body["action_plan"], list)
