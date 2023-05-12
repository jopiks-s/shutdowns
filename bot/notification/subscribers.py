import itertools
from copy import copy
from datetime import timedelta
from typing import List

import schedule

from bot.db import DisconSchedule, User
from log import logger


# todo add lock
# todo add logs
def subscribe_user(self, user: User, locked=!!!) -> None:
    if user.group is None:
        logger.warning(f'Failed to subscribe user "{user.user_id}"\n'
                       f'User does not have a group set')
        return
    if self.intervals is None:
        logger.warning(f'Failed to subscribe user "{user.user_id}"\n'
                       f'Notification class is not fully initialized.\n'
                       f'Maybe you forgot to use update_all_notification on startup xD')
        return
    if not self.DB.get_preset()[1]:
        logger.warning('Generating dynamic data based on outdated data')

    schedule.clear(f'{user.user_id=}')
    interval = self.intervals[user.group - 1]
    weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    for day_i, day in enumerate(interval):
        for state in day:
            day_index = day_i
            timestamp = list(state.values())[0]
            base_hour = timestamp[0]
            advance_time = timedelta(days=1, hours=base_hour) - timedelta(minutes=user.notification_advance)

            strftime = str(advance_time).split(',')[-1]  # 0:00:00
            strftime = strftime[0:strftime.rfind(':')]  # 0:00
            strftime = ':'.join([f'{int(h):02d}' for h in strftime.split(':')])  # 00:00

            if advance_time.days < 1:
                day_index = (day_i - 1) % 7

            getattr(schedule.every(), weekday[day_index]).at(strftime, 'Europe/Kiev').do(
                self._notify, user_id=user.user_id, timestamp=timestamp, disc_type=list(state.keys())[0]
            ).tag(f'{user.user_id=}')

    logger.info(f'User {user.user_id} notification updated')


# todo watch out for this edge case:
# user input = /setgroup 1. _commands_handler -> notification.add_subscriber (with lock) -> DB.get_preset() ->
# -> DB._update_storage() -> notification.update_all... -> notification.add_subscriber (with lock x2) =
# = deadlock!!!
def update_all_notification(self, preset: DisconSchedule) -> None:
    self.intervals = _get_intervals(preset)
    for user in User.objects():
        if user.group is None:
            continue

        self.subscribe_user(user, locked=!!!)

    logger.info('Notifications successfully updated')


def _get_intervals(preset: DisconSchedule) -> List[list]:
    intervals = []
    for group in preset.groups:
        interval = [[] for _ in range(7)]
        combined_days = [day.timetable for day in group.days]
        combined_days = list(itertools.chain.from_iterable(combined_days))

        temp_state = {}
        day_i = 0

        for i, state in enumerate(combined_days):
            if i == 0:
                temp_state[state] = [0, 0]
                for reverse_state in combined_days[::-1]:
                    if reverse_state in temp_state:
                        temp_state[state][0] = (temp_state[state][0] - 1) % 24
                    else:
                        break

            if i % 24 == 0 and i != 0:
                day_i += 1
            i %= 24
            if state not in temp_state:
                if 'yes' not in temp_state:
                    start_hour, end_hour = list(temp_state.values())[0]
                    if start_hour > end_hour:
                        interval[day_i - 1].append(copy(temp_state))
                    else:
                        interval[day_i].append(copy(temp_state))

                temp_state.clear()
                temp_state[state] = [i, (i + 1) % 24]
            else:
                temp_state[state][1] = (temp_state[state][1] + 1) % 24

        if 'yes' not in temp_state and temp_state.keys() != interval[0][0].keys():
            interval[day_i].append(temp_state)

        intervals.append(interval)

    return intervals
