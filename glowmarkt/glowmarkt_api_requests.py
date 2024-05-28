import requests
import json
from data_model import Resource, Reading
from glowmarkt.custom_exceptions.request_exceptions import (
    NoVeIdException,
    NoResourceException,
    NoReadingException,
    NoDataException,
    NoFirstDateException,
    NoLastDateException,
)

from datetime import datetime


def api_get_request(url: str, headers: dict = None, params: dict = None):

    if params is None:
        params = {}

    res = requests.get(url=url, headers=headers, params=params)

    if res.status_code != 200:
        raise requests.HTTPError(
            f"Request failed with status code {res.status_code}. Reason: {res.reason}"
        )

    return res.json()


def get_token(application_id: str, username: str, password: str) -> str:
    res = requests.post(
        url="https://api.glowmarkt.com/api/v0-1/auth",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
        },
        data=json.dumps({"username": username, "password": password}),
    )

    if res.status_code != 200:
        raise Exception(
            f"Request failed with status code {res.status_code}. Reason: {res.reason}"
        )

    token = res.json().get("token", None)

    if token is None:
        raise Exception("No token retrieved.")

    return res.json()["token"]


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


def get_first_datetime_reading(
    application_id: str,
    token: str,
    resource_id: str,
):
    res = api_get_request(
        url=f"https://api.glowmarkt.com/api/v0-1/resource/{resource_id}/first-time",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
    )

    raw_data = res.get("data", None)

    if raw_data is None:
        raise NoDataException()

    first_reading_datetime = raw_data.get("firstTs", None)

    if first_reading_datetime is None:
        raise NoFirstDateException()

    return first_reading_datetime


def get_latest_datetime_reading(
    application_id: str,
    token: str,
    resource_id: str,
):
    res = api_get_request(
        url=f"https://api.glowmarkt.com/api/v0-1/resource/{resource_id}/last-time",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
    )

    raw_data = res.get("data", None)

    if raw_data is None:
        raise NoDataException()

    last_reading_datetime = raw_data.get("lastTs", None)

    if last_reading_datetime is None:
        raise NoLastDateException()

    return last_reading_datetime


def get_usage_readings(
    application_id: str,
    token: str,
    resource_id: str,
    from_date: str,
    to_date: str,
) -> list[Reading]:

    res = api_get_request(
        url=f"https://api.glowmarkt.com/api/v0-1/resource/{resource_id}/readings?",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
            "token": token,
        },
        params={
            "from": from_date,
            "to": to_date,
            "period": "PT30M",
            "function": "sum",
        },
    )

    raw_readings = res.get("data", None)

    if raw_readings is None:
        raise NoReadingException(f"No readings retrieved from the request: {res}")

    readings = [
        Reading(timestamp=reading[0], resourceId=resource_id, value=reading[1])
        for reading in raw_readings
    ]

    return readings
