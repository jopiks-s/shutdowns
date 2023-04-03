import requests

from log import logger, request_logger
from . import response


def get_updates(self, offset: int, timeout: int) -> response.Updates:
    """Block the thread until a response is received or timeout expires"""
    params = {"offset": offset, "timeout": timeout}
    url = self.api_url("getUpdates")
    resp = requests.get(url, params=params)
    if resp.status_code == 400:
        logger.warning(f"Missing logic for 400 response")

    elif resp.status_code == 200:
        request_logger.info(resp.json())
        return ...

    else:
        logger.warning(f"Unhandled response status code: {resp.status_code}")
