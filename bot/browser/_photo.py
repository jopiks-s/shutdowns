from datetime import datetime
from io import BytesIO

import pandas
from PIL import Image
from pytz import timezone
from selenium.webdriver.common.by import By

from bot.db import DisconSchedule, expiration_check
from config import root_path
from log import logger


def get_preset_photo(self, group_index: int) -> bytes | None:
    if not self.photos.get(group_index, 0):
        if not self._update_preset_photos():
            logger.warning(f'Failed to get preset photo as it does not yet exist')
            return
    logger.info(f'Obtained an image of group {group_index}')
    return self.photos[group_index]


def _update_preset_photos(self) -> bool:
    if not update_preset_htmls():
        logger.warning('Failed to update preset photos')
        return False

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


def update_preset_htmls() -> bool:
    if not len(DisconSchedule.objects()):
        logger.warning('Failed to update preset htmls as preset database is empty')
        return False

    preset: DisconSchedule = DisconSchedule.objects[0]
    column_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    row_names = [f'{v:02d}-{(v + 1):02d}' for v in range(24)]

    last_update = 'last_update expired' if expiration_check(preset) else 'last_update'
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
