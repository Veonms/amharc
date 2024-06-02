import os

from dotenv import load_dotenv

from glowmarkt.src.custom_exceptions.credential_exceptions import (
    NoCredentialsExistException,
)
from glowmarkt.src.data_model import Credentials


def load_credentials() -> Credentials:
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

    return Credentials(
        bright_username=bright_username,
        bright_password=bright_password,
        bright_application_id=bright_application_id,
        valkey_host=valkey_host,
        valkey_port=valkey_port,
    )
