from fastapi.testclient import TestClient

from multi_provider_llm.api.app import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "ok"
    assert "app_name" in data
    assert "environment" in data


def test_generate_endpoint_with_mock_provider() -> None:
    response = client.post(
        "/generate",
        json={
            "provider": "mock",
            "prompt": "Explain provider abstraction.",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["provider"] == "mock"
    assert "mock LLM response" in data["response"]


def test_generate_endpoint_rejects_empty_prompt() -> None:
    response = client.post(
        "/generate",
        json={
            "provider": "mock",
            "prompt": "",
        },
    )

    assert response.status_code == 422


def test_generate_endpoint_rejects_unsupported_provider() -> None:
    response = client.post(
        "/generate",
        json={
            "provider": "openai",
            "prompt": "Hello",
        },
    )

    assert response.status_code == 400
    assert "Unsupported provider" in response.json()["detail"]


def test_complaint_analysis_endpoint_with_mock_provider() -> None:
    response = client.post(
        "/complaints/analyse",
        json={
            "provider": "mock",
            "complaint": "My QR payment was deducted but the merchant did not receive it.",
        },
    )

    assert response.status_code == 200

    data = response.json()
    assert data["provider"] == "mock"
    assert data["category"] == "payment_dispute"
    assert data["urgency"] == "high"
    assert data["needs_human_review"] is True


def test_complaint_analysis_endpoint_rejects_empty_complaint() -> None:
    response = client.post(
        "/complaints/analyse",
        json={
            "provider": "mock",
            "complaint": "",
        },
    )

    assert response.status_code == 422

def test_stream_generate_endpoint_with_mock_provider() -> None:
    with client.stream(
        "POST",
        "/generate/stream",
        json={
            "provider": "mock",
            "prompt": "Explain streaming.",
        },
    ) as response:
        assert response.status_code == 200
        streamed_text = "".join(response.iter_text())

    assert "mock LLM response" in streamed_text


def test_stream_generate_endpoint_rejects_unsupported_provider() -> None:
    response = client.post(
        "/generate/stream",
        json={
            "provider": "openai",
            "prompt": "Hello",
        },
    )

    assert response.status_code == 400
    assert "Unsupported provider" in response.json()["detail"]


def test_stream_generate_endpoint_rejects_empty_prompt() -> None:
    response = client.post(
        "/generate/stream",
        json={
            "provider": "mock",
            "prompt": "",
        },
    )

    assert response.status_code == 422