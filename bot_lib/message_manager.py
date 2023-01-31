import json
import queue
from dataclasses import asdict
from threading import Thread
from concurrent.futures import ThreadPoolExecutor

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
        while True:
            message: response.Message = self.client_queue.get()
            logger.debug((json.dumps(asdict(message), indent=4)))

            if not message.command:
                continue
            elif message.command == Commands.start:
                ...
            elif message.command == Commands.setschedule:
                if len(message.parameters) == 0:
                    logger.info(f"{message.from_.username} send command [{message.command}] without parameters")
                    logger.info(f"Missing logic for {message.command} if send without params")
                    continue

                self.client.send_message(message.chat.id,
                                         f"Got command: {message.command}, params: {message.parameters}")

    # start [n] threads
    def start(self, executor: ThreadPoolExecutor, n):
        [executor.submit(Thread(name=f"worker{i}", target=self._worker).start) for i in range(n)]
