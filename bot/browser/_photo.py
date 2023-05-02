from io import BytesIO

import pandas
from PIL import Image
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
    for i in range(3):
        self.driver.get(f'{root_path}/bot/browser/render/group{i + 1}.html')
        wrapper = self.driver.find_element(By.CLASS_NAME, 'wrapper')
        b = self.driver.execute_script('return arguments[0].getBoundingClientRect();', wrapper)
        image = Image.open(BytesIO(self.driver.get_screenshot_as_png()))
        image = image.crop((0, 0, b['right'] + 8, b['bottom'] - 16))
        image.save(f'{root_path}/bot/browser/render/group{i + 1}.png')
        image.close()
        with open(f'{root_path}/bot/browser/render/group{i + 1}.png', 'rb') as img:
            self.photos[i+1] = img.read()
    logger.info('Photos successfully updated')
    return True


def update_preset_htmls() -> bool:
    if len(DisconSchedule.objects()) == 0:
        logger.warning('Failed to update preset htmls as database is empty')
        return False

    preset: DisconSchedule = DisconSchedule.objects[0]
    column_names = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    row_names = [f'{v}-{v + 1}' for v in range(24)]
    for i, group in enumerate(preset.groups):
        d = {day: group.days[j].timetable for j, day in enumerate(column_names)}
        df = pandas.DataFrame(d, index=row_names)

        css = '<link rel="stylesheet" href="style.css">'
        wrapper = '<div class="wrapper">\n'
        table = df.to_html()
        last_update = 'last_update expired' if expiration_check(preset) else 'last_update'
        last_update = f'<p class="{last_update}">{preset.last_update.strftime("%d %B, %H:%M:%S")}</p>\n'
        with open(f'{root_path}/bot/browser/render/group{i + 1}.html', 'w') as f:
            f.write(css)
            f.write(wrapper)
            f.write(table + '\n')
            f.write(last_update)
            f.write('</div>')
    logger.info('Htmls successfully updated')
    return True
