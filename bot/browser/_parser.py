import json
import traceback
from datetime import datetime
from typing import Any

from bs4 import BeautifulSoup
from pytz import timezone

from bot.db.discon_schedule import DisconSchedule
from log import logger


# todo edge case testing
def retrieve_preset(self) -> DisconSchedule | None:
    with self.browser_lock:
        logger.info('Retrieval a preset from the server')
        self.browser.get(self.url)
        raw_preset = _discon_txt_to_json(self.browser.page_source)
        if raw_preset is None:
            logger.warning('Failed to retrieve preset')
            return None

        db_preset = _preset_mapper(raw_preset)
        logger.info('Successfully retrieved preset from the server')
        return DisconSchedule(**db_preset)


def _discon_txt_to_json(page_source: str) -> dict[str, Any] | None:
    soup = BeautifulSoup(page_source, 'html.parser')
    script = soup.find('script', string=lambda txt: 'DisconSchedule.preset' in txt if txt else False)

    if script is None:
        logger.warning('Failed to find and parse preset in html')
        logger.warning('Bs4 didn`t find script tag with content: "DisconSchedule.preset"\n'
                       'Page source:\n'
                       f'{soup.prettify()}')
        return None

    script_txt = script.text.strip()
    preset_txt = script.text.strip()
    l_edge = preset_txt.find('DisconSchedule.preset')
    r_edge = preset_txt.find('}}}}', l_edge) + 4
    preset_txt = script_txt[l_edge:r_edge].split('=')

    if len(preset_txt) < 2:
        logger.warning('Failed to find and parse preset in html')
        logger.warning(f'Invalid raw script text\n'
                       f'Raw script text: \n{script_txt}'
                       f'Result of parsing the script text: \n{preset_txt}')
        return None

    try:
        return json.loads(preset_txt[1]).get('data', None)
    except:
        logger.warning('Failed to find and parse preset in html')
        logger.warning('Can`t deserialize parsed text from script'
                       f'Result of parsing the script text: {preset_txt}\n'
                       f'Exception: {traceback.print_exc()}')
        return None


def _preset_mapper(preset: dict) -> dict:
    db_preset = {'groups': []}
    for i, discon_data in enumerate(preset.values()):
        db_preset['groups'].append({'days': []})
        for days in list(discon_data.values()):
            db_preset['groups'][i]['days'].append({'timetable': list(days.values())})

    db_preset['last_update'] = datetime.now(timezone('Europe/Kiev')).replace(tzinfo=None)
    return db_preset
