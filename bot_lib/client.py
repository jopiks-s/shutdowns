import json
from typing import List
import requests
import dacite
from bot_lib import response, commands
from dataclasses import asdict


def _add_commands(updates: dict) -> dict:
    # regular finding command and parameters
    for update in updates['result']:
        message = update['message']
        if 'text' not in message.keys():
            return updates

        text: str = message['text'].strip()
        command = None
        parameters = []

        for i, s in enumerate(text.split(" ")):
            if i == 0:
                if len(s) > 1 and s[0] == '/':
                    print("enter to parsing")
                    command = s[1:]
                    if not hasattr(commands.Commands, command):
                        command = None
                        break
                    command = commands.Commands[command]
                    continue
                else:
                    break

            if len(s) > 0:
                parameters.append(s)

        message['command'] = command
        message['parameters'] = parameters

    return updates


def _prettify_updates(updates: dict) -> List[response.ResultObj]:
    # rename update['message]['from'] key to 'from_' because otherwise dacite can`t parse from_dict to dataclass
    for i, message in enumerate([update['message'] for update in updates['result']]):
        copy = {}
        for k, v in message.items():
            copy["from_" if k == "from" else k] = v
        updates['result'][i]['message'] = copy

    _add_commands(updates)

    return dacite.from_dict(response.GetUpdatesResponse, updates).result


class Client:
    def __init__(self, token):
        self.token = token

    def api_url(self, method: str) -> str:
        return f"https://api.telegram.org/bot{self.token}/{method}"

    def poll_updates(self, offset: int, timeout: int) -> List[response.ResultObj]:
        params = {"offset": offset, "timeout": timeout}
        url = self.api_url("getUpdates")
        updates = requests.get(url, params=params).json()
        print(json.dumps(updates, indent=4))

        return _prettify_updates(updates)


    # Debug version
    def send_message(self, chat_id, text) -> dict:
        payload = {"chat_id": chat_id, "text": text}
        url = self.api_url("sendMessage")
        return requests.post(url, data=payload).json()
