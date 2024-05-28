from glowmarkt.src.custom_exceptions.request_exceptions import (
    NoVeIdException,
    NoResourceException,
)
from glowmarkt.src.data_model import Resource
from glowmarkt.src.glowmarkt_api_requests.utils import api_get_request


def get_virtual_entity_id(application_id: str, token: str) -> str:
    res = api_get_request(
        url="https://api.glowmarkt.com/api/v0-1/virtualentity",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
    )

    veid = res[0].get("veId", None)

    if veid is None:
        raise NoVeIdException(f"No veId retrieved from the request: {res}")

    return veid


def get_resources(application_id: str, token: str, veid: str) -> list[Resource]:
    res = api_get_request(
        url=f"https://api.glowmarkt.com/api/v0-1/virtualentity/{veid}/resources",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
    )

    raw_resources = res.get("resources", None)

    if raw_resources is None:
        raise NoResourceException(f"No resources retrieved from the request: {res}")

    resources = [
        Resource(
            resourceTypeId=resource["resourceTypeId"],
            name=resource["name"],
            type=resource["dataSourceResourceTypeInfo"]["type"],
            description=resource["description"],
            dataSourceType=resource["dataSourceType"],
            baseUnit=resource["baseUnit"],
            resourceId=resource["resourceId"],
            createdAt=resource["createdAt"],
        )
        for resource in raw_resources
    ]

    return resources
