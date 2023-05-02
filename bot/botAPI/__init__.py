import requests

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
        payload = {'chat_id': chat_id, 'text': text}
        url = self.api_url('sendMessage')
        return requests.post(url, data=payload).json()
