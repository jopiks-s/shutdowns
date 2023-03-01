from dataclasses import is_dataclass
from typing import Type, get_args, Tuple

import dacite

from bot import response
from bot.commands import Commands


def add_commands(updates: dict) -> dict:
    # regular finding command and parameters
    for update in updates.get('result', []):
        message = update.get('message', {})
        text: str = message.get('text', "")
        command, parameters = None, []

        for entity in message.get('entities', []):
            if entity.get('type', '') == 'bot_command' and entity.get('offset', -1) == 0:
                command = text[1:entity.get('length', 0)]
                command = getattr(Commands, command, None)
                if command:
                    command = Commands(command)
                    parameters = [p for p in text.split(" ")[1:] if p]

            break

        message['command'] = command
        message['parameters'] = parameters

    return updates


def have_required_keys(d: dict, cls: Type) -> bool:
    required_fields = {k: field_type for k, field_type in cls.__annotations__.items()
                       if type(None) not in get_args(field_type)}
    # print(f"cls '{cls}' required keys: {required_fields.keys()}")
    # print(f"given keys in dict: {d.keys()}")

    if not all(key in d for key in required_fields.keys()):
        # print(f"given dict haven`t all required keys")
        return False

    for key, field_type in required_fields.items():
        if is_dataclass(field_type) and not have_required_keys(d[key], field_type):
            return False

    return True


def prettify_updates(updates: dict) -> Tuple[response.ResultObj]:
    def _validate_updates(d):
        for update in d.get('result', [])[:]:
            if update.get('message', None):
                update['message']['from_'] = update['message'].pop('from', None)
            if not have_required_keys(update, response.ResultObj):
                d['result'].remove(update)

    def _lists_to_tuples(d):
        if isinstance(d, dict):
            for k, v in d.items():
                d[k] = _lists_to_tuples(v)
        elif isinstance(d, list):
            return tuple(_lists_to_tuples(i) for i in d)

        return d

    _validate_updates(updates)
    add_commands(updates)
    _lists_to_tuples(updates)

    return dacite.from_dict(response.GetUpdatesResponse, updates).result
