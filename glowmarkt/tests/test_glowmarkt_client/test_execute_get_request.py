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


def test_request_successful(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return MockResponse(status_code=200, reason="OK", token="test-token")

    monkeypatch.setattr(
        "test_execute_get_request.MockSession.get",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    res = client._execute_get_request(url="", headers={}, params={})
    assert res == {
        "status_code": 200,
        "reason": "OK",
        "token": "test-token",
    }


def test_request_successful_params_none(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return MockResponse(status_code=200, reason="OK", token="test-token")

    monkeypatch.setattr(
        "test_execute_get_request.MockSession.get",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    res = client._execute_get_request(url="", headers={})
    assert res == {
        "status_code": 200,
        "reason": "OK",
        "token": "test-token",
    }


def test_request_unsuccessful_non_200_code(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return MockResponse(status_code=404, reason="Not found", token="test-token")

    monkeypatch.setattr(
        "test_execute_get_request.MockSession.get",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )
    with pytest.raises(requests.HTTPError):
        client._execute_get_request(url="", headers={}, params={})


def test_request_unsuccessful_non_200_code_params_none(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return MockResponse(status_code=404, reason="Not found", token="test-token")

    monkeypatch.setattr(
        "test_execute_get_request.MockSession.get",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )
    with pytest.raises(requests.HTTPError):
        client._execute_get_request(url="", headers={})
