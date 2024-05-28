import json

import requests


def get_token(application_id: str, username: str, password: str) -> str:
    res = requests.post(
        url="https://api.glowmarkt.com/api/v0-1/auth",
        headers={
            "Content-Type": "application/json",
            "applicationId": application_id,
        },
        data=json.dumps({"username": username, "password": password}),
    )

    if res.status_code != 200:
        raise Exception(
            f"Request failed with status code {res.status_code}. Reason: {res.reason}"
        )

    token = res.json().get("token", None)

    if token is None:
        raise Exception("No token retrieved.")

    return res.json()["token"]
