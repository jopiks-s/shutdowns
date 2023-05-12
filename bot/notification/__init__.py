import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

import schedule

from bot.botAPI import BotAPI
from bot.db import DB
from log import logger


class Notification:
    from .subscribers import update_all_notification, subscribe_user, update_intervals

    def __init__(self, client: BotAPI, db: DB):
        self.client = client
        self.DB = db
        self.intervals = None

    def _notify(self, *, user_id: int, timestamp: list, disc_type: str):
        disc_type = 'possible disconnection' if disc_type == 'maybe' else 'will be a shutdown'
        msg = f'Caution\n' \
              f'{timestamp[0]:02d}-{timestamp[1]:02d} {disc_type}'
        self.client.send_message(user_id, msg)

    def _loop(self):
        logger.info('Started')
        while True:
            schedule.run_pending()
            time.sleep(60)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="notification0", target=self._loop).start)
