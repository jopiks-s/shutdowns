from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Browser:
    from ._parser import update_preset

    def __init__(self):
        options = Options()
        # options.headless = True
        self.browser = webdriver.Chrome(options=options)
        # self.browser = undetected_chromedriver.Chrome(options=options)
        self.url = 'https://www.dtek-kem.com.ua/ua/shutdowns'
