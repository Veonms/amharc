import json
from datetime import datetime
from typing import Protocol

import requests

from glowmarkt.src.custom_exceptions.request_exceptions import (
    NoVeIdException,
    NoResourceException,
    NoDataException,
    NoFirstDateException,
    NoLastDateException,
    NoReadingException,
)
from glowmarkt.src.data_model import Resource, Reading


class Session(Protocol):
    def post(self, url: str, headers: dict, data: str) -> any:
        """Makes a POST request."""

    def get(self, url: str, headers: dict, params: dict) -> any:
        """Makes a GET request."""


class GlowmarktClient:
    def __init__(
        self, username: str, password: str, application_id: str, session: Session
    ) -> None:
        self.username = username
        self.password = password
        self.application_id = application_id
        self.session = session
        self.token = self._retrieve_token()
        self.veid = self._retrieve_virtual_entity_id()

    def _retrieve_token(self) -> str:
        res = self.session.post(
            url="https://api.glowmarkt.com/api/v0-1/auth",
            headers={
                "Content-Type": "application/json",
                "applicationId": self.application_id,
            },
            data=json.dumps({"username": self.username, "password": self.password}),
        )

        if res.status_code != 200:
            raise requests.HTTPError(
                f"Request failed with status code {res.status_code}. Reason: {res.reason}"
            )

        token = res.json().get("token", None)

        if token is None:
            raise Exception("No token retrieved.")

        return token

    def _execute_get_request(
        self, url: str, headers: dict, params: dict = None
    ) -> dict:
        if params is None:
            params = {}

        res = self.session.get(url=url, headers=headers, params=params)

        if res.status_code != 200:
            raise requests.HTTPError(
                f"Request failed with status code {res.status_code}. Reason: {res.reason}"
            )

        return res.json()

    def _retrieve_virtual_entity_id(self) -> str:
        res = self._execute_get_request(
            url="https://api.glowmarkt.com/api/v0-1/virtualentity",
            headers={
                "Content-Type": "application/json",
                "applicationId": self.application_id,
                "token": self.token,
            },
        )

        veid = res[0].get("veId", None)

        if veid is None:
            raise NoVeIdException(f"No veId retrieved from the request: {res}")

        return veid

    def retrieve_resources(self) -> list[Resource]:
        res = self._execute_get_request(
            url=f"https://api.glowmarkt.com/api/v0-1/virtualentity/{self.veid}/resources",
            headers={
                "Content-Type": "application/json",
                "applicationId": self.application_id,
                "token": self.token,
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

    def retrieve_first_datetime_reading(self, resource_id: str):
        res = self._execute_get_request(
            url=f"https://api.glowmarkt.com/api/v0-1/resource/{resource_id}/first-time",
            headers={
                "Content-Type": "application/json",
                "applicationId": self.application_id,
                "token": self.token,
            },
        )

        raw_data = res.get("data", None)

        if raw_data is None:
            raise NoDataException()

        first_reading_datetime = raw_data.get("firstTs", None)

        if first_reading_datetime is None:
            raise NoFirstDateException()

        return datetime.fromtimestamp(first_reading_datetime).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

    def retrieve_latest_datetime_reading(self, resource_id: str):
        res = self._execute_get_request(
            url=f"https://api.glowmarkt.com/api/v0-1/resource/{resource_id}/last-time",
            headers={
                "Content-Type": "application/json",
                "applicationId": self.application_id,
                "token": self.token,
            },
        )

        raw_data = res.get("data", None)

        if raw_data is None:
            raise NoDataException()

        last_reading_datetime = raw_data.get("lastTs", None)

        if last_reading_datetime is None:
            raise NoLastDateException()

        return datetime.fromtimestamp(last_reading_datetime).strftime(
            "%Y-%m-%dT%H:%M:%S"
        )

    def retrieve_usage_readings(
        self,
        resource_id: str,
        from_date: str,
        to_date: str,
    ) -> list[Reading]:

        res = self._execute_get_request(
            url=f"https://api.glowmarkt.com/api/v0-1/resource/{resource_id}/readings?",
            headers={
                "Content-Type": "application/json",
                "applicationId": self.application_id,
                "token": self.token,
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
