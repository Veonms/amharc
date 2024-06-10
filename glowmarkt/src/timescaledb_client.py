import logging

import psycopg2

from glowmarkt.src.data_model import Resource, Reading


class TimescaledbClient:
    def __init__(
        self, username: str, password: str, host: str, port: int, database: str
    ):
        self.conn = psycopg2.connect(
            user=username, password=password, host=host, port=port, database=database
        )
        self.cursor = self.conn.cursor()

    def test_conn(self):
        self.cursor.execute("SELECT 'hello world'")
        print(self.cursor.fetchone())

    def write_resources(self, resources: list[Resource]):
        for resource in resources:
            try:
                self.cursor.execute(
                    f"INSERT INTO resources"
                    f"(resourceTypeId,"
                    f"name,"
                    f"type,"
                    f"description,"
                    f"dataSourceType,"
                    f"baseUnit,"
                    f"resourceId,"
                    f"createdAt)"
                    f"VALUES ({resource.resourceTypeId},"
                    f"{resource.name},"
                    f"{resource.type},"
                    f"{resource.description},"
                    f"{resource.dataSourceType},"
                    f"{resource.baseUnit},"
                    f"{resource.resourceId},"
                    f"{resource.createdAt});"
                )
            except psycopg2.Error as err:
                logging.error(
                    f"An exception occurred when writing resource {resource}: {err}"
                )

    def write_readings(self, readings: list[Reading]):
        for reading in readings:
            try:
                self.cursor.execute(
                    f"INSERT INTO readings"
                    f"(timestamp, resourceId, value)"
                    f"VALUES ({reading.recordedAt}, {reading.resourceId}, {reading.readingValue});"
                )
            except psycopg2.Error as err:
                logging.error(
                    f"An exception occurred when writing resource {reading}: {err}"
                )
