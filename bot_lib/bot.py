import queue
import threading
from concurrent.futures import ThreadPoolExecutor

from bot_lib.client import Client
from bot_lib.poller import Poller
from bot_lib.message_manager import MessageManager


class Bot:
    def __init__(self, token: str, threads_n: int):
        self.client = Client(token)
        # To functioning bot must have at least [2] threads
        self.threads_n = max(2, threads_n)
        self.client_queue = queue.Queue()
        self.poller = Poller(self.client, self.client_queue)
        self.message_manager = MessageManager(self.client, self.client_queue)

    def loop(self):
        with ThreadPoolExecutor(max_workers=self.threads_n) as executor:
            self.poller.start(executor)
            self.message_manager.start(executor, self.threads_n - 1)
