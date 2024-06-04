from typing import Optional


class MockSession:
    def post(self, url: str, headers: dict, data: str) -> any:
        pass

    def get(self, url: str, headers: dict, params: dict) -> any:
        pass


class MockValkeyConnection:
    def set(self, name: str, value: str, ex: Optional[int]):
        pass

    def get(self):
        pass
