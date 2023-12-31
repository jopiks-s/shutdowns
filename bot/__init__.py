import queue
from concurrent.futures import ThreadPoolExecutor

from bot.botAPI import BotAPI, Commands
from bot.browser import Browser
from bot.db import DisconSchedule
from bot.updater import Updater
from bot.message_handler import MessageHandler
from bot.notification import Notification
from bot.puller import Puller
from log import logger


class Bot:
    def __init__(self, token: str, threads_n: int = 2):
        self.client = BotAPI(token)
        self.client.set_my_commands(Commands.to_json())
        logger.warning("Bot must have at least 2 threads!") if threads_n < 2 else ...
        self.threads_n = max(2, threads_n)
        self.client_queue = queue.Queue()

        self.browser = Browser()
        self.notification = Notification(self.client)
        self.updater = Updater(1, self.browser, self.notification)
        self.poller = Puller(self.client, self.client_queue)
        self.message_manager = MessageHandler(self.client, self.client_queue, self.notification, self.browser)

    def loop(self) -> None:
        """
        Start bot
        Will block main thread
        """
        with ThreadPoolExecutor(max_workers=self.threads_n) as executor:
            self.notification.start_thread(executor)
            self.poller.start_thread(executor)
            self.message_manager.start_threads(executor, self.threads_n - 2)
