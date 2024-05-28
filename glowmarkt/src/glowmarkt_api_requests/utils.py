import requests


def api_get_request(url: str, headers: dict = None, params: dict = None):

    if params is None:
        params = {}

    res = requests.get(url=url, headers=headers, params=params)

    if res.status_code != 200:
        raise requests.HTTPError(
            f"Request failed with status code {res.status_code}. Reason: {res.reason}"
        )

    return res.json()
