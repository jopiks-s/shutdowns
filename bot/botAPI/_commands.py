from enum import Enum
from typing import List


class Commands(Enum):
    start = 'start'
    view = 'view (1-3)'
    setgroup = 'setgroup 1-3'
    notification_advance = 'advance (0-1440)'
    info = 'info'

    @staticmethod
    def to_json() -> List[dict]:
        return [{'command': command.name, 'description': command.value} for
                command in Commands]
