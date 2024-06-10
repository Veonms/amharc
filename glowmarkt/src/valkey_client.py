import logging
from typing import Optional, Protocol

import redis

from glowmarkt.src.custom_exceptions.valkey_exceptions import NoOpenConnectionException
from glowmarkt.src.data_model import CachedCredentials


class ValkeyPool(Protocol):
    def close(self) -> None:
        pass


class ValkeyConnection(Protocol):
    def set(self, name: str, value: str, ex: Optional[int] = None) -> None:
        pass

    def get(self, name: str) -> bytes:
        pass

    def close(self) -> None:
        pass


class ValkeyClient:
    def __init__(self, host: str, port: str, db: int = 0):
        self.pool: Optional[ValkeyPool] = None
        self.connection: Optional[ValkeyConnection] = None
        self.host = host
        self.port = port
        self.db = db

    def create_connection(self):
        self.pool = redis.ConnectionPool(host=self.host, port=self.port, db=self.db)
        self.connection = redis.Redis(connection_pool=self.pool)

    def close_connection(self):
        if self.pool is not None:
            self.pool.close()
        if self.connection is not None:
            self.connection.close()

    def set_credentials(self, token: str, veid: str) -> None:
        if self.connection is None:
            raise NoOpenConnectionException(
                "No open connection when setting credentials"
            )
        try:
            self.connection.set(
                name="token", value=token, ex=604800
            )  # Expires token in 7 days
            self.connection.set(name="veid", value=veid)
        except Exception as err:
            logging.error(f"Could not set credentials: {err}")
            raise err

    def get_credentials(self) -> Optional[CachedCredentials]:
        if self.connection is None:
            raise NoOpenConnectionException(
                "No open connection when getting credentials"
            )
        try:
            token = self.connection.get(name="token")
            veid = self.connection.get(name="veid")
        except Exception as err:
            logging.warning(f"Could not retrieve credentials: {err}")
            return None
        if not token or not veid:
            return None
        return CachedCredentials(
            bright_token=token.decode("utf-8"),
            bright_veid=veid.decode("utf-8"),
        )

    def set_delta(self, delta_key: str, delta_value: str) -> None:
        if self.connection is None:
            raise NoOpenConnectionException("No open connection when setting delta")
        try:
            self.connection.set(name=delta_key, value=delta_value)
        except Exception as err:
            logging.error(f"Could not set the delta: {err}")
            raise err

    def get_delta(self, delta_key) -> Optional[str]:
        if self.connection is None:
            raise NoOpenConnectionException("No open connection when getting delta")
        try:
            delta = self.connection.get(name=delta_key)
        except Exception as err:
            logging.error(f"Could not retrieve the delta: {err}")
            raise err
        if delta is not None:
            return delta.decode("utf-8")
        return delta
