from math import ceil

from dotenv import load_dotenv
import os

from data_model import Resource
from glowmarkt.src.glowmarkt_api_requests import (
    get_token,
    get_virtual_entity_id,
    get_resources,
    get_usage_readings,
    get_first_datetime_reading,
    get_latest_datetime_reading,
)

from datetime import datetime, timedelta


def get_date_ranges(start_datetime: str, end_datetime: str):
    date_ranges = []

    date_diff = (
        datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")
        - datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
    ).days

    temp_start_date = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S")
    temp_end_date = datetime.strptime(start_datetime, "%Y-%m-%dT%H:%M:%S") + timedelta(
        days=10
    )
    end_date_obj = datetime.strptime(end_datetime, "%Y-%m-%dT%H:%M:%S")

    for i in range(ceil(date_diff / 10)):
        if temp_end_date > end_date_obj:
            temp_end_date = end_date_obj
        date_ranges.append(
            (
                temp_start_date.strftime("%Y-%m-%dT%H:%M:%S"),
                temp_end_date.strftime("%Y-%m-%dT%H:%M:%S"),
            )
        )
        temp_start_date += timedelta(days=10)
        temp_end_date += timedelta(days=10)

    return date_ranges


def main():
    # Get credentials
    load_dotenv()
    bright_username = os.getenv("bright_username")
    bright_password = os.getenv("bright_password")
    bright_application_id = os.getenv("bright_application_id")

    token: str = get_token(
        application_id=bright_application_id,
        username=bright_username,
        password=bright_password,
    )

    veid: str = get_virtual_entity_id(application_id=bright_application_id, token=token)

    resources: list[Resource] = get_resources(
        application_id=bright_application_id, token=token, veid=veid
    )

    resource_id: str = resources[0].resourceId

    first_reading_time = datetime.fromtimestamp(
        get_first_datetime_reading(
            application_id=bright_application_id,
            token=token,
            resource_id=resource_id,
        )
    ).strftime("%Y-%m-%dT%H:%M:%S")

    end_date = datetime.fromtimestamp(
        get_latest_datetime_reading(
            application_id=bright_application_id,
            token=token,
            resource_id=resource_id,
        )
    ).strftime("%Y-%m-%dT%H:%M:%S")

    date_ranges = get_date_ranges(
        start_datetime=first_reading_time, end_datetime=end_date
    )

    readings = []

    for date_range in date_ranges:
        date_range_start, date_range_end = date_range
        readings.extend(
            get_usage_readings(
                application_id=bright_application_id,
                token=token,
                resource_id=resource_id,
                from_date=date_range_start,
                to_date=date_range_end,
            )
        )

    for reading in readings:
        print(reading)


if __name__ == "__main__":
    main()
