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
