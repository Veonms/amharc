import logging
from typing import Optional

import redis

from glowmarkt.src.data_model import CachedCredentials


class ValkeyClient:
    def __init__(self, host: str, port: str, db: int = 0):
        self.pool: Optional[redis.ConnectionPool] = None
        self.connection: Optional[redis.Redis] = None
        self.host = host
        self.port = port
        self.db = db

    def create_connection(self):
        self.pool = pool = redis.ConnectionPool(
            host=self.host, port=self.port, db=self.db
        )
        self.connection = redis.Redis(connection_pool=pool)

    def close_connection(self):
        if self.pool is not None:
            self.pool.close()
        if self.connection is not None:
            self.connection.close()

    def set_credentials(self, token: str, veid: str):
        try:
            self.connection.set(
                name="token", value=token, ex=604800
            )  # Expires token in 7 days
            self.connection.set(name="veid", value=veid)
        except Exception as err:
            logging.error(f"Could not set credentials: {err}")
            raise err

    def get_credentials(self) -> Optional[CachedCredentials]:
        try:
            token = self.connection.get("token")
            veid = self.connection.get("veid")
        except Exception as err:
            logging.warning(f"Could not retrieve credentials: {err}")
            return None
        return CachedCredentials(
            bright_token=token.decode("utf-8") if token else None,
            bright_veid=veid.decode("utf-8") if veid else None,
        )

    def set_delta(self, delta_key: str, delta_value: str) -> None:
        try:
            self.connection.set(name=delta_key, value=delta_value)
        except Exception as err:
            logging.error(f"Could not set the delta: {err}")
            raise err

    def get_delta(self, delta_key) -> Optional[str]:
        try:
            delta = self.connection.get(delta_key)
        except Exception as err:
            logging.error(f"Could not retrieve the delta: {err}")
            return None
        if delta is not None:
            return delta.decode("utf-8")
        return delta

    def set_virtual_entity_id(self, veid: str) -> None:
        try:
            self.connection.set("veid", veid)
        except Exception as err:
            logging.error(f"Could not set the veid: {err}")
            raise err

    def get_virtual_entity_id(self) -> Optional[str]:
        try:
            veid = self.connection.get("veid")
        except Exception as err:
            logging.error(f"Could not retrieve the veid: {err}")
            return None
        return veid
