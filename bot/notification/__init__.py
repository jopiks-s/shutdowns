import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, current_thread, Lock

import schedule

from bot import db
from bot.botAPI import BotAPI, Messages
from bot.db import User
from log import logger


# todo find bug: user get discon notifications even without group set
class Notification:
    from .subscribers import update_all_notification, subscribe_user

    def __init__(self, client: BotAPI):
        self.client = client
        self.intervals = None
        self.subscribe_lock = Lock()
        self.weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def _notify(self, *, user: User, timestamp: list, disc_type: str, day_i: int):
        msg = Messages.notify_fan if disc_type == 'maybe' else Messages.notify_stab
        start, end = (f'{timestamp[0]:02d}:00', f'{timestamp[1]:02d}:00')
        self.client.send_message(user, msg, start=start, end=end)

    def _loop(self):
        logger.info(f'Notification looping: {current_thread().name}')
        while True:
            schedule.run_pending()
            time.sleep(10)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="notification0", target=self._loop).start)
