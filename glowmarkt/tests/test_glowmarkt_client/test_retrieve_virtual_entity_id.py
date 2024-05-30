import pytest

from glowmarkt.src.custom_exceptions.request_exceptions import NoVeIdException
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.tests.fixtures import MockSession


def test_retrieve_veid_successful(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MockSession()
    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    def mock_execute_request(*args, **kwargs):
        return [{"veId": "test-veId"}]

    monkeypatch.setattr(
        "glowmarkt.src.glowmarkt_client.GlowmarktClient._execute_get_request",
        mock_execute_request,
    )

    client.token = "test-token"
    client._retrieve_virtual_entity_id()

    assert client.veid == "test-veId"


def test_retrieve_veid_unsuccessful_no_veid(monkeypatch: pytest.MonkeyPatch) -> None:
    session = MockSession()
    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    def mock_execute_request(*args, **kwargs):
        return [{}]

    monkeypatch.setattr(
        "glowmarkt.src.glowmarkt_client.GlowmarktClient._execute_get_request",
        mock_execute_request,
    )
    client.token = "test-token"

    with pytest.raises(NoVeIdException):
        client._retrieve_virtual_entity_id()
