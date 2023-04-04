import json
from dataclasses import asdict

import requests

from log import logger, request_logger
from . import response, ResponseDecoder, ResponseEncoder


def get_updates(self, offset: int, timeout: int) -> response.Updates | None:
    """Block the thread until a response is received or timeout expires"""
    params = {"offset": offset, "timeout": timeout}
    url = self.api_url("getUpdates")
    resp = requests.get(url, params=params)

    match resp.status_code:
        case 400:
            logger.warning(f"Missing logic for 400 response")
        case 200:
            updates_log = 'Raw Updates:\n'
            updates_log += json.dumps(resp.json(), indent=4)

            updates = json.loads(resp.text, cls=ResponseDecoder)

            updates_log += '\nParsed Updates:\n'
            for update in updates.messages:
                updates_log += json.dumps(asdict(update), cls=ResponseEncoder, indent=4)
            request_logger.info(updates_log)

            return updates
        case _ as code:
            logger.warning(f"Unhandled response status code: {code}")
