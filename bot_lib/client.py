import json
from typing import Tuple

import dacite
import requests

from bot_lib import response
from bot_lib.commands import Commands
from log.logger import logger


def _add_commands(updates: dict) -> dict:
    # regular finding command and parameters
    for update in updates.get('result', []):
        message = update.get('message', {})
        text: str = message.get('text', "").strip()
        command, parameters = None, []

        if text and text[0] == "/":
            command = text.split(" ")[0][1:]
            if getattr(Commands, command, None):
                command = Commands(command)
                parameters = [p for p in text.split(" ")[1:] if p]

        message['command'] = command
        message['parameters'] = parameters

    return updates


def _prettify_updates(updates: dict) -> Tuple[response.ResultObj]:
    def update_message_from_to__from(d):
        """
        dacite.from_dict can`t parse key value 'from' to 'from_'
        """
        for update in d['result']:
            update['message']['from_'] = update['message'].pop('from', None)

    def lists_to_tuples(d):
        if isinstance(d, dict):
            for k, v in d.items():
                d[k] = lists_to_tuples(v)
        elif isinstance(d, list):
            return tuple(lists_to_tuples(i) for i in d)

        return d

    update_message_from_to__from(updates)
    _add_commands(updates)
    lists_to_tuples(updates)

    return dacite.from_dict(response.GetUpdatesResponse, updates).result


class Client:
    def __init__(self, token):
        self.token = token

    def api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def poll_updates(self, offset: int, timeout: int) -> Tuple[response.ResultObj]:
        params = {"offset": offset, "timeout": timeout}
        url = self.api_url("getUpdates")
        updates = requests.get(url, params=params).json()
        logger.debug(json.dumps(updates, indent=4))

        return _prettify_updates(updates)

    # Debug version
    def send_message(self, chat_id, text) -> dict:
        payload = {"chat_id": chat_id, "text": text}
        url = self.api_url("sendMessage")
        return requests.post(url, data=payload).json()
