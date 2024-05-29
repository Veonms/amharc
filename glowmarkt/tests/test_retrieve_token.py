import pytest
import requests

from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.tests.fixtures import MockResponse


class MockSessionSuccessful:
    def post(self, url: str, headers: dict, data: str) -> any:
        return MockResponse(status_code=200, reason="OK", token="test-token")

    def get(self, url: str, headers: dict, params: dict) -> any: ...


class MockSessionUnsuccessfulNon200:
    def post(self, url: str, headers: dict, data: str) -> any:
        return MockResponse(status_code=404, reason="Not found", token="test-token")

    def get(self, url: str, headers: dict, params: dict) -> any: ...


class MockSessionUnsuccessfulNoToken:
    def post(self, url: str, headers: dict, data: str) -> any:
        return MockResponse(status_code=404, reason="Not found")

    def get(self, url: str, headers: dict, params: dict) -> any: ...


def test_retrieve_token_successful():
    session = MockSessionSuccessful()

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    client._retrieve_token()
    assert client.token == "test-token"


def test_retrieve_token_unsuccessful_non_200_status_code():
    session = MockSessionUnsuccessfulNon200()

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    with pytest.raises(requests.HTTPError):
        client._retrieve_token()


def test_retrieve_token_unsuccessful_no_token_in_response():
    session = MockSessionUnsuccessfulNoToken()

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    with pytest.raises(requests.HTTPError):
        client._retrieve_token()
