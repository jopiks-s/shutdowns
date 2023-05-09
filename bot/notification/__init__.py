import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import schedule

from bot.db.user import User
from bot.db.discon_schedule import DisconSchedule
from log import logger


class Notification:
    def __init__(self):
        self.subscribers = {}

    def _notify(self, user_id: int, timestamp: list, disc_type: str):
        ...

    def _loop(self):
        logger.info('Started')
        while True:
            schedule.run_pending()
            time.sleep(60)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="notification0", target=self._loop).start)

    def update_all_notification(self, preset: DisconSchedule):
        schedule.jobs.clear()
        ...

    def add_subscriber(self, preset: DisconSchedule, user: User):
        ...
