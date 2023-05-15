from threading import Lock

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from log import logger


class Browser:
    from ._parser import retrieve_preset
    from ._photo import get_photo, update_photos, _update_preset_htmls

    def __init__(self):
        self.photos = {}
        self.url = 'https://www.dtek-kem.com.ua/ua/shutdowns'
        self.photos_lock = Lock()
        self.htmls_lock = Lock()

        options = Options()
        options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)
        self.browser_lock = Lock()

        options = Options()
        options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--force-device-scale-factor=1')
        self.driver = webdriver.Chrome(options=options)
        self.driver.set_window_size(1920, 1080)
        self.driver_lock = Lock()

        logger.info('Browser started')
