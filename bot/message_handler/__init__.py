import queue
import threading
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from threading import Thread

from bot.botAPI import BotAPI, Commands, response
from bot.browser import Browser
from log import logger


class MessageHandler:
    from ._commands_handler import not_command
    from ._commands_handler import start_command
    from ._commands_handler import viewschedule_command
    from ._commands_handler import setgroup_command
    from ._commands_handler import notification_command
    from ._commands_handler import info_command
    from ._commands_handler import about_command

    def __init__(self, client: BotAPI, client_queue: queue.Queue, browser: Browser):
        self.client = client
        self.client_queue = client_queue
        self.browser = browser
        self.commands = {
            None: self.not_command,
            Commands.start: self.start_command,
            Commands.viewschedule: self.viewschedule_command,
            Commands.setgroup: self.setgroup_command,
            Commands.notification: self.notification_command,
            Commands.info: self.info_command,
            Commands.about: self.about_command,

        }
        self.user_locks = defaultdict(threading.Lock)

    def _worker(self):
        logger.info("Started")
        while True:
            packed_update: response.PackedUpdate = self.client_queue.get()
            with self.user_locks[packed_update.id]:
                for message in packed_update.messages:
                    self.commands[message.command](message)

    def start_threads(self, executor: ThreadPoolExecutor, n):
        """start [n] threads"""
        [executor.submit(Thread(name=f"worker{i}", target=self._worker).start) for i in range(n)]
