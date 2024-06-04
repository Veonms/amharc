import pytest

from glowmarkt.src.custom_exceptions.valkey_exceptions import NoOpenConnectionException
from glowmarkt.src.valkey_client import ValkeyClient
from glowmarkt.tests.fixtures import MockValkeyConnection


def test_set_delta_successful():
    valkey_client = ValkeyClient(host="test-host", port="test-port")
    valkey_client.connection = MockValkeyConnection()
    valkey_client.set_delta(delta_key="test-delta-key", delta_value="test-delta-value")


def test_set_delta_unsuccessful_no_connection():
    valkey_client = ValkeyClient(host="test-host", port="test-port")
    with pytest.raises(NoOpenConnectionException):
        valkey_client.set_delta(
            delta_key="test-delta-key", delta_value="test-delta-value"
        )
