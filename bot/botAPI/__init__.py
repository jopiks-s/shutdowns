import requests

from ._commands import Commands
from ._updates_parser import ResponseEncoder
from ._updates_parser import ResponseDecoder
from ._get_updates import pack_updates


class BotAPI:
    from ._get_updates import get_updates

    def __init__(self, token):
        self.token = token

    def api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    # Debug version
    def send_message(self, chat_id, text) -> dict:
        payload = {"chat_id": chat_id, "text": text}
        url = self.api_url("sendMessage")
        return requests.post(url, data=payload).json()

# Move the logic for handling response updates from the puller to botAPI->get_updates. get_updates makes a request
# which is 'response.Updates' And finish uml structure diagram
# to the API, after receiving the response it returns the result of the custom ResponseDecoder,
# Finish uml structure diagram
