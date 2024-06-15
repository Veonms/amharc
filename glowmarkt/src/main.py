import logging

import requests

from glowmarkt.src.credentials import load_credentials
from glowmarkt.src.data_model import Credentials, Resource
from glowmarkt.src.get_date_ranges import get_date_ranges
from glowmarkt.src.glowmarkt_client import GlowmarktClient
from glowmarkt.src.timescaledb_client import TimescaledbClient
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
    glowmarkt_client = GlowmarktClient(
        username=credentials.bright_username,
        password=credentials.bright_password,
        application_id=credentials.bright_application_id,
        session=requests.Session(),
    )

    timescaledb_client = TimescaledbClient(
        username="timescaledb",
        password="password",
        host="localhost",
        port=5432,
        database="glowmarkt",
    )

    try:
        valkey_client.create_connection()
    except Exception as err:
        logging.error(f"Exception during valkey connection: {err}")
        exit()

    cached_creds = valkey_client.get_credentials()

    if cached_creds is None:
        logging.info("No credentials in cache: retrieving new credentials")
        glowmarkt_client.retrieve_credentials()
        valkey_client.set_credentials(
            token=glowmarkt_client.token, veid=glowmarkt_client.veid
        )
    else:
        logging.info("Found cached credentials")
        glowmarkt_client.token = cached_creds.bright_token
        glowmarkt_client.veid = cached_creds.bright_veid

    logging.info("Retrieving resources")
    resources: list[Resource] = glowmarkt_client.retrieve_resources()

    logging.info("Writing resources to db")
    timescaledb_client.write_resources(resources)

    for resource in resources:
        logging.info(f"Retrieving delta for resource {resource.resource_id}")
        start_datetime = valkey_client.get_delta(
            delta_key=f"delta_{resource.resource_id}"
        )
        if start_datetime is None:
            logging.info("No delta in cache: retrieving first reading")
            start_datetime = glowmarkt_client.retrieve_first_datetime_reading(
                resource_id=resource.resource_id
            )

        latest_datetime = glowmarkt_client.retrieve_latest_datetime_reading(
            resource_id=resource.resource_id
        )

        date_ranges = get_date_ranges(
            start_datetime=start_datetime,
            end_datetime=latest_datetime,
        )

        readings = []

        # TODO: Make API calls asynchronous
        logging.info("Retrieving readings")
        for date_range in date_ranges:
            readings.extend(
                glowmarkt_client.retrieve_usage_readings(
                    resource_id=resource.resource_id,
                    from_date=date_range.start_date,
                    to_date=date_range.end_date,
                )
            )

        filtered_readings = [
            reading for reading in readings if reading.reading_value != 0
        ]

        logging.info("Writing readings to db")
        timescaledb_client.write_readings(filtered_readings)

        # TODO: latest_datetime could have a reading of 0. Need to change to filtered_readings [-1]
        logging.info(f"Updating delta to {latest_datetime}")
        valkey_client.set_delta(
            delta_key=f"delta_{resource.resource_id}", delta_value=latest_datetime
        )

    # TODO: Close session from GlowmarktClient
    # TODO: Close timescaleDB connection
    valkey_client.close_connection()


if __name__ == "__main__":
    main()
