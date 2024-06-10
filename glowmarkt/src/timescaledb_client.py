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
                    f"VALUES ({resource.resource_type_id},"
                    f"{resource.name},"
                    f"{resource.type},"
                    f"{resource.description},"
                    f"{resource.data_source_type},"
                    f"{resource.base_unit},"
                    f"{resource.resource_id},"
                    f"{resource.created_at});"
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
                    f"VALUES ({reading.recorded_at}, {reading.resource_id}, {reading.reading_value});"
                )
            except psycopg2.Error as err:
                logging.error(
                    f"An exception occurred when writing resource {reading}: {err}"
                )
