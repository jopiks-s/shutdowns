from bot.db import DisconSchedule
import json
from datetime import datetime

import undetected_chromedriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options


class Browser:
    def __init__(self):
        options = Options()
        options.headless = True
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
        raw_preset = self.discon_txt_to_json(self.browser.page_source)
        db_preset = self.preset_mapper(raw_preset)

        return db_preset

    @staticmethod
    def discon_txt_to_json(page_source: str) -> dict | None:
        # todo SAFETY

        soup = BeautifulSoup(page_source, 'html.parser')
        script = soup.find('script', string=lambda text: 'DisconSchedule.r_p' in text)
        preset_text = script.text.strip()
        r_edge = preset_text.find('DisconSchedule.r_p')
        l_edge = preset_text.find('}}}}', r_edge) + 4
        preset_text = preset_text[r_edge:l_edge]
        raw_preset = json.loads(preset_text.split('=')[1]).get('data', {})
        return raw_preset

    @staticmethod
    def preset_mapper(raw_preset: dict) -> dict | None:
        db_preset = {'groups': []}
        for i, discon_data in enumerate(r_p.values()):
            db_preset['groups'].append({'days': []})
            for days in list(discon_data.values()):
                db_preset['groups'][i]['days'].append({'timetable': list(days.values())})
        db_preset['last_update'] = datetime.utcnow().strftime('%d/%m/%y %H:%M:%S')
        return db_preset


if __name__ == '__main__':
    browser = Browser()
    source = ''
    with open('site.html', encoding='utf-8') as f:
        source = ''.join(f.readlines())
    r_p = Browser.discon_txt_to_json(source)
    print(r_p)
    print(json.dumps(r_p, indent=4))
    db_p = Browser.preset_mapper(r_p)
    print(db_p)
    print(json.dumps(db_p, indent=4))
    s = DisconSchedule(**db_p)
    s.save()

    # browser.test()
