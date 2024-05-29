class MockResponse:
    def __init__(self, status_code: int, reason: str, token: str = None):
        self.status_code = status_code
        self.reason = reason
        self.token = token

    def json(self):
        return {
            "status_code": self.status_code,
            "reason": self.reason,
            "token": self.token,
        }
