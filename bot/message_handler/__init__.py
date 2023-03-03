import queue
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from bot import response
from bot.client import Client
from bot.commands import Commands
from log import logger


class MessageHandler:
    from ._commands_handler import not_command
    from ._commands_handler import start_command

    def __init__(self, client: Client, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue
        self.commands = {
            None: self.not_command,
            Commands.start: self.start_command,
        }
        self.user_locks = defaultdict(threading.Lock)

    def _worker(self):
        logger.info("Started")

        while True:
            message: response.Message = self.client_queue.get()
            user_id = message.from_.id
            lock = self.user_locks[user_id]
            with lock:
                self.commands[message.command](message)

    # start [n] threads
    def start_threads(self, executor: ThreadPoolExecutor, n):
        [executor.submit(Thread(name=f"worker{i}", target=self._worker).start) for i in range(n)]
