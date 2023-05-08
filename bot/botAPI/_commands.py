from enum import Enum
from typing import List


class Commands(Enum):
    start = 'Activate bot'
    view = 'Show schedule of blackouts'
    setgroup = 'Set your group index from 1 to 3'
    notification = 'Enable/disable notification'
    info = 'Statistics about your account'
    help = 'Information help bot'

    @staticmethod
    def to_json() -> List[dict]:
        return [{'command': command.name, 'description': command.value} for command in Commands]
