import requests


class Client:
    def __init__(self, token):
        self.token = token

    def api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def poll_updates(self, offset: int, timeout: int) -> dict:
        params = {"offset": offset, "timeout": timeout}
        url = self.api_url("getUpdates")
        return requests.get(url, params=params).json()

    # Debug version
    def send_message(self, chat_id, text) -> dict:
        payload = {"chat_id": chat_id, "text": text}
        url = self.api_url("sendMessage")
        return requests.post(url, data=payload).json()

# d = {"ok": True, "result": [{"update_id": 930735281,
#                              "message": {"message_id": 304,
#                                          "from": {"id": 760317971, "is_bot": False, "first_name": "Ne",
#                                                   "last_name": "budlo", "username": "Az0npisyarnui",
#                                                   "language_code": "en"},
#                                          "chat": {"id": 760317971, "first_name": "Ne", "last_name": "budlo",
#                                                   "username": "Az0npisyarnui", "type": "private"}, "date": 1675422946,
#                                          "text": ")"}}]}


# TODO move logic of prettifying updates to poller
