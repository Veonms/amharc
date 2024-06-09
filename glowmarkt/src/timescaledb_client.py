import psycopg2


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
