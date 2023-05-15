from datetime import datetime
from io import BytesIO

import pandas
from PIL import Image
from pytz import timezone
from selenium.webdriver.common.by import By

from bot.updater import fresh, expired
from bot import updater
from bot.db.discon_schedule import DisconSchedule
from config import root_path
from log import logger


def get_photo(self, group_index: int) -> bytes | None:
    with self.photos_lock:
        if not self.photos.get(group_index, 0):
            logger.warning(f'Failed to get photo of group {group_index}\n'
                           f'Browser._photo module is not fully initialized'
                           f'Maybe you forgot to use update_photos on startup xD')
            return
        if not updater.fresh:
            logger.warning('Generating dynamic data based on outdated data')

        logger.info(f'Obtained an image of group {group_index}')
        return self.photos[group_index]


def update_photos(self, preset: DisconSchedule) -> bool:
    with self.driver_lock:
        self._update_preset_htmls(preset)

        day_index = datetime.now(timezone('Europe/Kiev')).weekday() + 1
        for i in range(3):
            self.driver.get(f'{root_path}/bot/browser/render/group{i + 1}.html?{day_index=}')
            wrapper = self.driver.find_element(By.CLASS_NAME, 'wrapper')
            b = self.driver.execute_script('return arguments[0].getBoundingClientRect();', wrapper)
            with Image.open(BytesIO(self.driver.get_screenshot_as_png())) as image:
                image = image.crop((0, 0, b['right'] + 8, b['bottom'] - 16))
                image.save(f'{root_path}/bot/browser/render/group{i + 1}.png')
                image.close()
                with open(f'{root_path}/bot/browser/render/group{i + 1}.png', 'rb') as img:
                    self.photos[i + 1] = img.read()
        logger.info('Photos successfully updated')
        return True


def _update_preset_htmls(self, preset: DisconSchedule) -> bool:
    with self.htmls_lock:
        column_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        row_names = [f'{v:02d}-{(v + 1):02d}' for v in range(24)]

        last_update = 'last_update expired' if updater.expired(preset) else 'last_update'
        with open(f'{root_path}/bot/browser/render/html_markup.html', 'r') as f:
            html_markup = ''.join(f.readlines())

        for i, group in enumerate(preset.groups):
            d = {day: group.days[j].timetable for j, day in enumerate(column_names)}
            df = pandas.DataFrame(d, index=row_names)
            table = df.to_html()
            with open(f'{root_path}/bot/browser/render/group{i + 1}.html', 'w') as f:
                f.write(html_markup.format(table=table, last_update=last_update,
                                           time=preset.last_update.strftime("%d %B, %H:%M:%S")))
        logger.info('Htmls successfully updated')
        return True
