import queue
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from typing import Tuple

from bot.botAPI import BotAPI
from bot.botAPI.response import PackedUpdate, Updates
from log import logger


def pack_updates(updates: Updates) -> Tuple[PackedUpdate, ...]:
    res = defaultdict(lambda: [])
    for update in updates.messages:
        res[update.from_.id].append(update)

    return tuple(PackedUpdate(user_id, tuple(messages)) for user_id, messages in res.items())


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
            for packed_update in pack_updates(updates):
                logger.debug(f'packed update id: {packed_update.id}, messages: {[m.text for m in packed_update.messages]}')
                self.client_queue.put(packed_update)

    # start [1] thread
    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="puller0", target=self._puller).start)
