import json
from typing import TypeVar

import requests

from log import request_logger

T = TypeVar('T', bound='BotAPI')


def send_photo(self: T, chat_id: str, photo: str | bytes, caption: str = '') -> dict | None:
    url = self.api_url('sendPhoto')
    payload = {'chat_id': chat_id, 'caption': caption}

    files = {}
    if isinstance(photo, str):
        payload['photo'] = photo
    else:
        files['photo'] = photo

    resp = requests.post(url, data=payload, files=files)

    match resp.status_code:
        case 400:
            photo_log = 'Send photo response status code 400\n' \
                        'Send photo response:\n'
            photo_log += json.dumps(resp.json(), indent=4)
            request_logger.warning(photo_log)
            return
        case 200:
            photo_log = 'Send photo response:\n'
            photo_log += json.dumps(resp.json(), indent=4)
            request_logger.info(photo_log)
            return resp.json()
