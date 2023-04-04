import queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from bot.botAPI import BotAPI
from log import logger


class Puller:
    def __init__(self, client: BotAPI, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue

    def _puller(self):
        logger.info("Started")
        offset = 0
        timeout = 60
        while True:
            logger.info(f"pull with offset: {offset}")
            updates = self.client.get_updates(offset, timeout)
            if not updates:
                continue
            offset = updates.last_update_id + 1
            for update in updates.messages:
                self.client_queue.put(update)

    # start [1] thread
    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="puller0", target=self._puller).start)
