import json
from typing import List

import requests

from bot.db import User
from log import request_logger, logger
from ._commands import Commands
from ._get_updates import pack_updates
from ._updates_parser import ResponseEncoder, ResponseDecoder
from .messages import Messages, get_translation


class BotAPI:
    from ._get_updates import get_updates
    from ._send_photo import send_photo

    def __init__(self, token):
        self.token = token

    def api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def send_message(self, user: User, msgs: tuple[Messages] | Messages, **kwargs) -> dict:
        url = self.api_url('sendMessage')
        text = get_translation(msgs, user.language_code, **kwargs)
        payload = {'chat_id': user.user_id, 'text': text, 'parse_mode': 'Markdown'}
        resp = requests.post(url, data=payload).json()
        request_logger.info(json.dumps(resp, indent=4))
        return resp

    # todo add localization
    def set_my_commands(self, commands: List[dict]) -> dict:
        url = self.api_url('setMyCommands')
        payload = {'commands': json.dumps(commands)}
        resp = requests.post(url, data=payload).json()
        request_logger.info(json.dumps(resp, indent=4))
        return resp
