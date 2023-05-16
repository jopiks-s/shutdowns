import time
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, current_thread, Lock

import schedule

from bot.botAPI import BotAPI
from log import logger


class Notification:
    from .subscribers import update_all_notification, subscribe_user

    def __init__(self, client: BotAPI):
        self.client = client
        self.intervals = None
        self.subscribe_lock = Lock()
        self.weekday = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

    def _notify(self, *, user_id: int, timestamp: list, disc_type: str, day_i: int):
        disc_type = 'possible disconnection' if disc_type == 'maybe' else 'will be a shutdown'
        msg = f'{timestamp[0]:02d}-{timestamp[1]:02d} {disc_type}'
        if timestamp[0] > timestamp[1]:
            day_i = (day_i + 1) % 7
            msg += f' ({self.weekday[day_i]})'
        self.client.send_message(user_id, msg)

    def _loop(self):
        logger.info(f'Notification looping: {current_thread().name}')
        while True:
            schedule.run_pending()
            time.sleep(30)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="notification0", target=self._loop).start)
