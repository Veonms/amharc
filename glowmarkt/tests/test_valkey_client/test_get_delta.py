import pytest
from pytest import MonkeyPatch

from glowmarkt.src.custom_exceptions.valkey_exceptions import NoOpenConnectionException
from glowmarkt.src.valkey_client import ValkeyClient
from glowmarkt.tests.fixtures import MockValkeyConnection


def test_get_delta_successful_no_cached_delta(monkeypatch: MonkeyPatch):
    def mock_get_delta(*args, **kwargs):
        return None

    monkeypatch.setattr(
        "glowmarkt.src.valkey_client.ValkeyConnection.get",
        mock_get_delta,
    )

    valkey_client = ValkeyClient(host="test-host", port="test-port")
    valkey_client.connection = MockValkeyConnection()
    delta = valkey_client.get_delta(delta_key="test-delta-key")
    assert delta is None


def test_get_delta_successful_cached_delta(monkeypatch: MonkeyPatch):
    def mock_get_delta(*args, **kwargs):
        return b"test-delta"

    monkeypatch.setattr(
        "glowmarkt.tests.fixtures.MockValkeyConnection.get",
        mock_get_delta,
    )

    valkey_client = ValkeyClient(host="test-host", port="test-port")
    valkey_client.connection = MockValkeyConnection()
    delta = valkey_client.get_delta(delta_key="test-delta-key")
    assert delta == "test-delta"


def test_get_delta_unsuccessful_no_connection():
    valkey_client = ValkeyClient(host="test-host", port="test-port")
    with pytest.raises(NoOpenConnectionException):
        valkey_client.get_delta(delta_key="test-delta-key")
