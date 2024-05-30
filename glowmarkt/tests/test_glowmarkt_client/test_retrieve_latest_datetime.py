import pytest

from glowmarkt.src.custom_exceptions.request_exceptions import (
    NoDataException,
    NoLastDateException,
)
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.tests.fixtures import MockSession


def test_get_datetime_reading_successful(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return {"data": {"lastTs": 1717070400}}  # Thursday, 30 May 2024 12:00:00

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

    assert (
        client.retrieve_latest_datetime_reading(resource_id="test-id")
        == "2024-05-30T12:00:00"
    )


def test_get_datetime_reading_unsuccessful_no_data(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return {}

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

    with pytest.raises(NoDataException):
        client.retrieve_latest_datetime_reading(resource_id="test-id")


def test_get_datetime_reading_unsuccessful_no_timestamp(
    monkeypatch: pytest.MonkeyPatch,
):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return {"data": {"tsFail": 1717070400}}

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

    with pytest.raises(NoLastDateException):
        client.retrieve_latest_datetime_reading(resource_id="test-id")
