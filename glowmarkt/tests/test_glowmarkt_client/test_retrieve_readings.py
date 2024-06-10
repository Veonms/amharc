import pytest

from glowmarkt.src.custom_exceptions.request_exceptions import NoReadingException
from glowmarkt.src.data_model import Reading
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.tests.fixtures import MockSession


def test_get_readings_successful(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return {"data": [["test-timestamp", 5.0]]}

    monkeypatch.setattr(
        "glowmarkt.src.glowmarkt_client.GlowmarktClient._execute_get_request",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    client.token = "test-token"
    client.veid = "test-veid"

    assert client.retrieve_usage_readings(
        resource_id="test-resource-id", from_date="test-date", to_date="test-date"
    ) == [
        Reading(
            recordedAt="test-timestamp", resourceId="test-resource-id", readingValue=5.0
        )
    ]


def test_get_readings_unsuccessful_no_reading(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return {"no-data": []}

    monkeypatch.setattr(
        "glowmarkt.src.glowmarkt_client.GlowmarktClient._execute_get_request",
        mock_request,
    )

    client = GlowmarktClient(
        username="username",
        password="password",
        application_id="application_id",
        session=session,
    )

    client.token = "test-token"
    client.veid = "test-veid"

    with pytest.raises(NoReadingException):
        client.retrieve_usage_readings(
            resource_id="test-resource-id", from_date="test-date", to_date="test-date"
        )
