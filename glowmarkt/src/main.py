import os

import requests
from dotenv import load_dotenv

from glowmarkt.src.custom_exceptions.credential_exceptions import (
    NoCredentialsExistException,
)
from glowmarkt.src.get_date_ranges import get_date_ranges
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.src.valkey_client import ValkeyClient


def main():
    # TODO: Move credential handling to a separate function
    # Get credentials
    load_dotenv()
    bright_username = os.getenv("bright_username")
    bright_password = os.getenv("bright_password")
    bright_application_id = os.getenv("bright_application_id")
    valkey_host = os.getenv("valkey_host")
    valkey_port = os.getenv("valkey_port")

    if None in [
        bright_username,
        bright_password,
        bright_application_id,
        valkey_host,
        valkey_port,
    ]:
        raise NoCredentialsExistException(f"One or more credentials are None")

    valkey_client = ValkeyClient(host=valkey_host, port=valkey_port)

    valkey_client.create_connection()

    # TODO: Close session from GlowmarktClient
    glowmarkt_client = GlowmarktClient(
        username=bright_username,
        password=bright_password,
        application_id=bright_application_id,
        session=requests.Session(),
    )

    cache_token, cache_veid = valkey_client.get_credentials()

    if cache_token is None or cache_veid is None:
        glowmarkt_client.retrieve_credentials()
        valkey_client.set_credentials(
            token=glowmarkt_client.token, veid=glowmarkt_client.token
        )

    resources = glowmarkt_client.retrieve_resources()

    # TODO: Loop for all resources
    resource_id: str = resources[0].resourceId

    first_timestamp = glowmarkt_client.retrieve_first_datetime_reading(
        resource_id=resource_id
    )

    latest_timestamp = glowmarkt_client.retrieve_latest_datetime_reading(
        resource_id=resource_id
    )

    date_ranges = get_date_ranges(
        start_datetime=first_timestamp, end_datetime=latest_timestamp
    )

    readings = []

    # TODO: Make API calls asynchronous
    for date_range in date_ranges:
        date_range_start, date_range_end = date_range
        readings.extend(
            glowmarkt_client.retrieve_usage_readings(
                resource_id=resource_id,
                from_date=date_range_start,
                to_date=date_range_end,
            )
        )

    for reading in readings:
        if reading.value == 0:
            continue
        print(reading)


if __name__ == "__main__":
    main()
