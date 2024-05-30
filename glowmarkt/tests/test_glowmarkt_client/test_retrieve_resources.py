import pytest

from glowmarkt.src.custom_exceptions.request_exceptions import NoResourceException
from glowmarkt.src.data_model import Resource
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.tests.fixtures import MockSession


def test_get_resources_successful(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return {
            "resources": [
                {
                    "resourceTypeId": "test-id",
                    "name": "test-name",
                    "dataSourceResourceTypeInfo": {"type": "test-type"},
                    "description": "test-description",
                    "dataSourceType": "test-source-type",
                    "baseUnit": "test-base-unit",
                    "resourceId": "test-resource-id",
                    "createdAt": "test-timestamp",
                }
            ]
        }

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

    assert client.retrieve_resources() == [
        Resource(
            resourceTypeId="test-id",
            name="test-name",
            type="test-type",
            description="test-description",
            dataSourceType="test-source-type",
            baseUnit="test-base-unit",
            resourceId="test-resource-id",
            createdAt="test-timestamp",
        )
    ]


def test_get_resources_unsuccessful_no_resource(monkeypatch: pytest.MonkeyPatch):
    session = MockSession()

    def mock_request(*args, **kwargs):
        return {"resources-fail": "value"}

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

    with pytest.raises(NoResourceException):
        client.retrieve_resources()
