import queue
import threading
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
from collections import defaultdict

from bot import response
from bot.client import Client
from bot.commands import Commands
from log.logger import logger


class MessageManager:
    def __init__(self, client: Client, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue
        self.commands = {
            None: self.not_command,
            Commands.start: self.start_command,
            Commands.setschedule: self.setschedule_command
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

    def not_command(self, message: response.Message):
        # time.sleep(random.random()*5)
        self.client.send_message(message.chat.id,
                                 f"Your message: {message.text}")

    def start_command(self, message: response.Message):
        self.client.send_message(message.chat.id,
                                 f"Got command: {message.command}, params: {message.parameters}")

    def setschedule_command(self, message: response.Message):
        if len(message.parameters) == 0:
            logger.debug(f"{message.from_.username} send command [{message.command}] without parameters")
            logger.warning(f"Missing logic for {message.command} if send without params")
            return

        self.client.send_message(message.chat.id,
                                 f"Got command: {message.command}, params: {message.parameters}")
