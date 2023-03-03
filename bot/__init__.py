import queue
from concurrent.futures import ThreadPoolExecutor

import mongoengine

from bot.client import Client
from bot.message_handler import MessageHandler
from bot.puller import Puller
from log import logger


class Bot:
    def __init__(self, token: str, threads_n: int = 2):
        self.client = Client(token)
        logger.warning("Bot must have at least 2 threads!") if threads_n < 2 else ...
        self.threads_n = max(2, threads_n)
        self.client_queue = queue.Queue()
        self.poller = Puller(self.client, self.client_queue)
        self.message_manager = MessageHandler(self.client, self.client_queue)

    def loop(self) -> None:
        """
        Start bot
        Will block main thread
        """
        with ThreadPoolExecutor(max_workers=self.threads_n) as executor:
            self.poller.start_threads(executor)
            self.message_manager.start_threads(executor, self.threads_n - 1)
