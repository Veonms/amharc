from glowmarkt.src.custom_exceptions.request_exceptions import (
    NoReadingException,
    NoDataException,
    NoFirstDateException,
    NoLastDateException,
)
from glowmarkt.src.data_model import Reading
from glowmarkt.src.glowmarkt_api_requests.utils import api_get_request


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
