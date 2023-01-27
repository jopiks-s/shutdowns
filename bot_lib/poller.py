import queue
from concurrent.futures import ThreadPoolExecutor

from bot_lib.client import Client


class Poller:
    def __init__(self, client: Client, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue

    def _poller(self, name):
        print(f"{name}: started")
        offset = 0
        timeout = 60
        while True:
            updates = self.client.poll_updates(offset, timeout)
            for update in updates:
                update_id = update.update_id
                print(f"{name}: put in queue")
                print(f"    {name}: update_id {update_id}")
                print(f"    {name}: queue size {self.client_queue.qsize()}")
                offset = update_id + 1
                self.client_queue.put(update)

    # start [1] thread
    def start(self, executor: ThreadPoolExecutor):
        executor.submit(self._poller, "poller0")
