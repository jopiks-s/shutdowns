import json
from enum import Enum


class Commands(Enum):
    start = 0
    viewschedule = 1
    setgroup = 2
    notification = 3
    info = 4
    about = 5


class CommandsEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Commands):
            return obj.name
        return json.JSONEncoder.default(self, obj)
