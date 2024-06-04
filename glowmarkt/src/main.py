import logging

import requests

from glowmarkt.src.credentials import load_credentials
from glowmarkt.src.data_model import Credentials, CachedCredentials
from glowmarkt.src.get_date_ranges import get_date_ranges
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.src.valkey_client import ValkeyClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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

    cached_creds: CachedCredentials = valkey_client.get_credentials()

    if cached_creds is None:
        logging.info("No credentials in cache: retrieving new credentials")
        glowmarkt_client.retrieve_credentials()
        valkey_client.set_credentials(
            token=glowmarkt_client.token, veid=glowmarkt_client.veid
        )
    else:
        logging.info("Found credentials")
        glowmarkt_client.token = cached_creds.bright_token
        glowmarkt_client.veid = cached_creds.bright_veid

    resources = glowmarkt_client.retrieve_resources()

    # TODO: Loop for all resources
    resource_id: str = resources[0].resourceId

    logging.info("Retrieving delta")
    start_datetime = valkey_client.get_delta(delta_key=f"delta_{resource_id}")
    if start_datetime is None:
        logging.info("No delta in cache: retrieving first reading")
        start_datetime = glowmarkt_client.retrieve_first_datetime_reading(
            resource_id=resource_id
        )

    latest_datetime = glowmarkt_client.retrieve_latest_datetime_reading(
        resource_id=resource_id
    )

    date_ranges = get_date_ranges(
        start_datetime=start_datetime,
        end_datetime=latest_datetime,
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

    valkey_client.set_delta(
        delta_key=f"delta_{resource_id}", delta_value=latest_datetime
    )
    valkey_client.close_connection()


if __name__ == "__main__":
    main()
