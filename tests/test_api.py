from fastapi.testclient import TestClient

from ai_agent.api import app


def test_health_endpoint():
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["service"] == "ai-agent-rag"


def test_ask_endpoint(mocker):
    mocker.patch("ai_agent.api.run_agent", return_value="Resposta mockada")
    client = TestClient(app)
    response = client.post("/ask", json={"question": "Qual o prazo de devolução?"})
    assert response.status_code == 200
    assert response.json()["answer"] == "Resposta mockada"
