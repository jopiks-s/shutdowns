import queue
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from bot_lib import response
from bot_lib.client import Client
from bot_lib.commands import Commands
from log.logger import logger


class MessageManager:
    def __init__(self, client: Client, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue

    def _worker(self):
        logger.info("Started")
        actions = {
            None: self.not_command,
            Commands.start: self.start_command,
            Commands.setschedule: self.setschedule_command
        }
        while True:
            message: response.Message = self.client_queue.get()
            actions[message.command](message)

    # start [n] threads
    def start_threads(self, executor: ThreadPoolExecutor, n):
        [executor.submit(Thread(name=f"worker{i}", target=self._worker).start) for i in range(n)]

    def not_command(self, message: response.Message):
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
