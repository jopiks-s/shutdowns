import json
from datetime import datetime

from bs4 import BeautifulSoup
from mongoengine import ValidationError

from log import logger
from bot.db import DisconSchedule


def update_preset(self) -> DisconSchedule | None:
    self.browser.get(self.url)
    raw_preset = _discon_txt_to_json(self.browser.page_source)
    db_preset = _preset_mapper(raw_preset)

    try:
        discon_schedule = DisconSchedule(**db_preset)
        discon_schedule.validate()
        DisconSchedule.objects().delete()
        discon_schedule.save()
        logger.info('Preset successfully updated')
        return discon_schedule
    except ValidationError as e:
        logger.warning('Failed to update preset')
        logger.warning('Can`t validate "db_preset" to create "DisconSchedule" object')
        logger.warning(f'Object to validate: {db_preset=}')
        logger.warning(f'Exception: {e}')
        return
    except Exception as e:
        logger.warning('Failed to update preset')
        logger.warning(f'An unexpected exception occurred: {e}')
        logger.warning(f'Object to validate: {db_preset=}')
        return


def _discon_txt_to_json(page_source: str) -> dict:
    soup = BeautifulSoup(page_source, 'html.parser')
    script = soup.find('script', string=lambda txt: 'DisconSchedule.preset' in txt if txt else False)

    if script is None:
        logger.warning('Bs4 didn`t find script tag with content: "DisconSchedule.preset"')
        logger.warning(f'Page source: {page_source}')
        return {}

    preset_text = script.text.strip()
    l_edge = preset_text.find('DisconSchedule.preset')
    r_edge = preset_text.find('}}}}', l_edge) + 4
    preset_text = preset_text[l_edge:r_edge].split('=')

    if len(preset_text) < 2:
        logger.warning(f'Corrupted script text: \n{script.text}')
        logger.warning(f'Result of parsing the script text: {preset_text}')
        return {}

    try:
        return json.loads(preset_text[1]).get('data', {})
    except Exception as e:
        logger.warning('Can`t deserialize parsed text from script')
        logger.warning(f'Result of parsing the script text: {preset_text}')
        logger.warning(f'Exception: {e}')
        return {}


def _preset_mapper(preset: dict) -> dict:
    db_preset = {'groups': []}
    for i, discon_data in enumerate(preset.values()):
        db_preset['groups'].append({'days': []})
        for days in list(discon_data.values()):
            db_preset['groups'][i]['days'].append({'timetable': list(days.values())})
    db_preset['last_update'] = datetime.utcnow().strftime('%d/%m/%y %H:%M:%S')
    return db_preset
