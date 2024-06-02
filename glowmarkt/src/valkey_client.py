import logging
from typing import Optional

import redis


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

    def get_credentials(self) -> Optional[tuple[str, str]]:
        try:
            token = self.connection.get("token")
            veid = self.connection.get("veid")
        except Exception as err:
            logging.warning(f"Could not retrieve credentials: {err}")
            return None
        return token, veid

    def set_delta(self, delta: str) -> None:
        try:
            self.connection.set("delta", delta)
        except Exception as err:
            logging.error(f"Could not set the delta: {err}")
            raise err

    def get_delta(self) -> Optional[str]:
        try:
            delta = self.connection.get("delta")
        except Exception as err:
            logging.error(f"Could not retrieve the delta: {err}")
            return None
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
