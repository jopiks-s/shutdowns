import copy
import itertools
import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import schedule

from bot.db.discon_schedule import DisconSchedule
from bot.db.user import User
from log import logger


class Notification:
    def _notify(self, *, user_id: int, timestamp: list, disc_type: str):
        ...

    def _loop(self):
        logger.info('Started')
        while True:
            schedule.run_pending()
            time.sleep(60)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="notification0", target=self._loop).start)

    def update_all_notification(self, preset: DisconSchedule):
        ...

    def subscribe_user(self, preset: DisconSchedule, user: User):
        if user.group is None:
            subscribe_log = f'Failed to subscribe user "{user.user_id}"\n' \
                            f'User does not have a group set'
            logger.warning(subscribe_log)
            return

        schedule.jobs = list(
            filter(lambda job: job.job_func.keywords['user_id'] != user.user_id,
                   schedule.jobs)
        )

# todo test sunday -> monday disconnections round robin
    @staticmethod
    def split_into_intervals():
        result = []
        group = DisconSchedule.objects[0].groups[1]
        combined_days = [day.timetable for day in group.days]
        combined_days = list(itertools.chain.from_iterable(combined_days))
        start_index = combined_days.index('yes') + 1
        i = start_index
        day_i = 0

        round_days = itertools.cycle(combined_days)
        [round_days.__next__() for _ in range(start_index)]

        print('Day: 1')
        for state in round_days:
            if state in ['no', 'maybe']:
                discon_end = i + 1
                j = 0
                discon_robin = copy.deepcopy(round_days)
                for discon_state in discon_robin:
                    if state == discon_state:
                        j += 1
                        discon_end = (discon_end + 1) % 24
                    else:
                        break

                print(f'{i:02d}-{discon_end :02d}')
                i += j
                [round_days.__next__() for _ in range(j)]

            if i + 1 > 23:
                i %= 23
                day_i += 1
                if day_i > 6:
                    return
                print(f'\n\nDay: {day_i + 1}')
            else:
                i += 1


if __name__ == '__main__':
    Notification.split_into_intervals()
