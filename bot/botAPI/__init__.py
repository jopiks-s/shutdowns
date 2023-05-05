import json
from typing import List

import requests

from log import logger
from ._commands import Commands
from ._get_updates import pack_updates
from ._updates_parser import ResponseEncoder, ResponseDecoder


class BotAPI:
    from ._get_updates import get_updates
    from ._send_photo import send_photo

    def __init__(self, token):
        self.token = token

    def api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def send_message(self, chat_id: int, text: str) -> dict:
        url = self.api_url('sendMessage')
        payload = {'chat_id': chat_id, 'text': text}
        return requests.post(url, data=payload).json()

    def set_my_commands(self, commands: List[dict]):
        url = self.api_url('setMyCommands')
        payload = {'commands': json.dumps(commands)}
        return requests.post(url, data=payload).json()
