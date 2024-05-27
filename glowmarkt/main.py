from dotenv import load_dotenv
import os

from data_model import Resource, Reading
from glowmarkt.glowmarkt_api_requests import (
    get_token,
    get_virtual_entity_id,
    get_resources,
    get_usage_readings,
)


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

    readings: list[Reading] = get_usage_readings(
        application_id=bright_application_id, token=token, resource_id=resource_id
    )

    for reading in readings:
        print(reading)


if __name__ == "__main__":
    main()
