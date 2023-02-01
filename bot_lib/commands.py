import json
from enum import Enum


class Commands(Enum):
    start = 0
    setschedule = 1


class CommandsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Commands):
            return obj.name
        return json.JSONEncoder.default(self, obj)
