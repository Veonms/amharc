import pytest
import requests

from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.tests.fixtures import MockSession


class MockResponse:
    def __init__(self, status_code: int, reason: str, token: str = None):
        self.status_code = status_code
        self.reason = reason
        self.token = token

    def json(self):
        return {
            "status_code": self.status_code,
            "reason": self.reason,
            "token": self.token,
        }


def test_retrieve_token_successful(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return MockResponse(status_code=200, reason="OK", token="test-token")

    monkeypatch.setattr(
        "test_retrieve_token.MockSession.post",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    client._retrieve_token()
    assert client.token == "test-token"


def test_retrieve_token_unsuccessful_non_200_status_code(
    monkeypatch: pytest.MonkeyPatch,
):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return MockResponse(status_code=404, reason="Not found", token="test-token")

    monkeypatch.setattr(
        "test_retrieve_token.MockSession.post",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    with pytest.raises(requests.HTTPError):
        client._retrieve_token()


def test_retrieve_token_unsuccessful_no_token_in_response(
    monkeypatch: pytest.MonkeyPatch,
):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return MockResponse(status_code=404, reason="Not found")

    monkeypatch.setattr(
        "test_retrieve_token.MockSession.post",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    with pytest.raises(requests.HTTPError):
        client._retrieve_token()
