import json
import queue
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from threading import Thread

from bot_lib.client import Client
from bot_lib.commands import CommandsEncoder
from bot_lib.updates_parser import prettify_updates
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
            logger.info(f"pull with offset: {offset}")
            updates = self.client.poll_updates(offset, timeout)
            logger.debug(json.dumps(updates, indent=4))

            if not updates['ok']:
                logger.warning(f"Missing logic for bad response")
                continue
            for update in updates['result']:
                offset = update.get('update_id', -1) + 1

            updates = prettify_updates(updates)
            for update in updates:
                logger.debug(json.dumps(asdict(update), indent=4, cls=CommandsEncoder))
                self.client_queue.put(update.message)
            logger.debug(f"next offset: {offset}")

    # start [1] thread
    def start(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="poller0", target=self._poller).start)
