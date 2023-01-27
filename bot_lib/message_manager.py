import queue
import time
from concurrent.futures import ThreadPoolExecutor

from selenium import webdriver

from bot_lib.client import Client


class MessageManager:
    def __init__(self, client: Client, client_queue: queue.Queue):
        self.client = client
        self.client_queue = client_queue

    def _worker(self, name):
        ...

    # start [n] threads
    def start(self, executor: ThreadPoolExecutor, n):
        [executor.submit(self._worker, f"worker{i}") for i in range(n)]
