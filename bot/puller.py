import queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread, current_thread

from bot import botAPI
from log import logger


class Puller:
    def __init__(self, client: botAPI.BotAPI, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue

    def _puller(self):
        logger.info(f"Puller looping: {current_thread().name}")
        offset = 0
        timeout = 60
        while True:
            logger.info(f"pull with offset: {offset}")
            updates = self.client.get_updates(offset, timeout)
            if not updates:
                continue
            offset = updates.last_update_id + 1
            for packed_update in botAPI.pack_updates(updates):
                self.client_queue.put(packed_update)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="puller0", target=self._puller).start)
