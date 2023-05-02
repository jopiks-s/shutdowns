from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Browser:
    from ._parser import update_preset
    from ._photo import get_preset_photo, _update_preset_photos

    def __init__(self):
        self.photos = {}
        self.url = 'https://www.dtek-kem.com.ua/ua/shutdowns'

        options = Options()
        # options.add_argument('--headless')
        self.browser = webdriver.Chrome(options=options)

        options = Options()
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        options.add_argument('--force-device-scale-factor=1')
        self.driver = webdriver.Chrome(options=options)

