import requests
import json
from data_model import Resource, Reading


def get_token(application_id: str, username: str, password: str) -> str:
    res = requests.post(
        url="https://api.glowmarkt.com/api/v0-1/auth",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
        },
        data=json.dumps({"username": username, "password": password}),
    )

    return res.json()["token"]


def get_virtual_entity_id(application_id: str, token: str) -> str:
    res = requests.get(
        url="https://api.glowmarkt.com/api/v0-1/virtualentity",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
    ).json()[0]
    return res["veId"]


def get_resources(application_id: str, token: str, veid: str) -> list[Resource]:
    res = requests.get(
        url=f"https://api.glowmarkt.com/api/v0-1/virtualentity/{veid}/resources",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
    ).json()

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
        for resource in res["resources"]
    ]

    return resources


def get_usage_readings(
    application_id: str, token: str, resource_id: str
) -> list[Reading]:
    res = requests.get(
        url=f"https://api.glowmarkt.com/api/v0-1/resource/{resource_id}/readings?",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
        params={
            "from": "2024-05-01T00:00:00",
            "to": "2024-05-10T00:00:00",
            "period": "PT30M",
            "function": "sum",
        },
    ).json()

    resource_id = res["resourceId"]

    readings = [
        Reading(timestamp=reading[0], resourceId=resource_id, value=reading[1])
        for reading in res["data"]
    ]

    return readings
