import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import schedule

from bot.db import DisconSchedule
from log import logger


class Notification:
    def __init__(self):
        self.subscribers = tuple([set() for _ in range(3)])

    def _notify(self, timestamp: list, disc_type: str, group: int):
        ...

    def load_notification(self, preset: DisconSchedule):
        schedule.jobs.clear()
        ...

    def _loop(self):
        logger.info('Started')
        while True:
            schedule.run_pending()
            time.sleep(60)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="notification0", target=self._loop).start)
