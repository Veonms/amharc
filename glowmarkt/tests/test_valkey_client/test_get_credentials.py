import pytest

from glowmarkt.src.custom_exceptions.valkey_exceptions import NoOpenConnectionException
from glowmarkt.src.valkey_client import ValkeyClient


def test_get_delta_unsuccessful_no_connection():
    valkey_client = ValkeyClient(host="test-host", port="test-port")
    with pytest.raises(NoOpenConnectionException):
        valkey_client.get_credentials()
