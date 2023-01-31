import queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from bot_lib.client import Client
from log.logger import logger


class Poller:
    def __init__(self, client: Client, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue

    def _poller(self):
        logger.info("Started")
        offset = 0
        timeout = 60
        while True:
            updates = self.client.poll_updates(offset, timeout)
            for update in updates:
                update_id = update.update_id
                logger.info(f"Add in queue: {update_id}")
                logger.debug(f"Queue size: {self.client_queue.qsize()}")
                offset = update_id + 1
                self.client_queue.put(update.message)

    # start [1] thread
    def start(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="poller0", target=self._poller).start)
