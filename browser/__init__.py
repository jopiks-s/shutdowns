# from selenium import webdriver
import json
from datetime import datetime

import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self):
        options = Options()
        # options.headless = True
        self.browser = undetected_chromedriver.Chrome(options=options)
        self.url = 'https://www.dtek-kem.com.ua/ua/shutdowns'

    def test(self):
        # url = 'https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html'
        # url = 'https://www.vindecoderz.com/EN/check-lookup/ZDMMADBMXHB001652'
        self.browser.get(self.url)
        print(BeautifulSoup(self.browser.page_source, 'html.parser').prettify())

        input('>>')

    def get_preset(self):
        # todo safety

        self.browser.get(self.url)

        html_preset = self.parse_html(self.browser.page_source)
        preset = json.loads(html_preset.split('=')[-1])
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        preset = {'data': preset['data']}
        for group_i, discon_data in preset.items():
            for day_i in discon_data.keys():
                discon_data[days[int(day_i) - 1]] = discon_data.pop(day_i)
        preset['last_update'] = datetime.now().strftime('%d/%m/%y %H:%M:%S')
        return preset

    @staticmethod
    def parse_html(page_source: str) -> str:
        soup = BeautifulSoup(page_source, 'html.parser')
        script = soup.find('script', string=lambda text: 'DisconSchedule.preset' in text)
        preset_text = script.text.strip()
        r_edge = preset_text.find('DisconSchedule.preset')
        l_edge = preset_text.find('}}}}', r_edge) + 4
        return preset_text[r_edge:l_edge]


if __name__ == '__main__':
    browser = Browser()
    browser.test()
