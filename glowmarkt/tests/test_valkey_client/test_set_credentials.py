import pytest

from glowmarkt.src.custom_exceptions.valkey_exceptions import NoOpenConnectionException
from glowmarkt.src.valkey_client import ValkeyClient
from glowmarkt.tests.fixtures import MockValkeyConnection


def test_set_credentials_successful():
    valkey_client = ValkeyClient(host="test-host", port="test-port")
    valkey_client.connection = MockValkeyConnection()
    valkey_client.set_credentials(token="test-token", veid="test-veid")


def test_set_credentials_unsuccessful_no_open_connection():
    valkey_client = ValkeyClient(host="test-host", port="test-port")
    with pytest.raises(NoOpenConnectionException):
        valkey_client.set_credentials(token="test-token", veid="test-veid")
