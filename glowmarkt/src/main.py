import logging

import requests

from glowmarkt.src.credentials import load_credentials
from glowmarkt.src.data_model import Credentials
from glowmarkt.src.get_date_ranges import get_date_ranges
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.src.valkey_client import ValkeyClient


def main():
    credentials: Credentials = load_credentials()

    # Create clients
    valkey_client = ValkeyClient(
        host=credentials.valkey_host, port=credentials.valkey_port
    )
    # TODO: Close session from GlowmarktClient
    glowmarkt_client = GlowmarktClient(
        username=credentials.bright_username,
        password=credentials.bright_password,
        application_id=credentials.bright_application_id,
        session=requests.Session(),
    )

    try:
        valkey_client.create_connection()
    except Exception as err:
        logging.error(f"Exception during valkey connection: {err}")
        exit()

    cache_token, cache_veid = valkey_client.get_credentials()

    if not all([cache_token, cache_veid]):
        glowmarkt_client.retrieve_credentials()
        valkey_client.set_credentials(
            token=glowmarkt_client.token, veid=glowmarkt_client.token
        )
    else:
        glowmarkt_client.token = cache_token
        glowmarkt_client.veid = cache_veid

    resources = glowmarkt_client.retrieve_resources()

    # TODO: Loop for all resources
    resource_id: str = resources[0].resourceId

    # TODO: Get delta from cache and compare
    start_datetime = glowmarkt_client.retrieve_first_datetime_reading

    date_ranges = get_date_ranges(
        start_datetime=start_datetime(resource_id=resource_id),
        end_datetime=glowmarkt_client.retrieve_latest_datetime_reading(
            resource_id=resource_id
        ),
    )

    readings = []

    # TODO: Make API calls asynchronous
    for date_range in date_ranges:
        readings.extend(
            glowmarkt_client.retrieve_usage_readings(
                resource_id=resource_id,
                from_date=date_range.start_date,
                to_date=date_range.end_date,
            )
        )

    for reading in readings:
        if reading.value == 0:
            continue
        print(reading)


if __name__ == "__main__":
    main()
