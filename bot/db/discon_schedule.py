from datetime import datetime
from pytz import timezone
from threading import Lock

from mongoengine import *

from log import logger

preset_lock = Lock()


class DisconDay(EmbeddedDocument):
    timetable = ListField(StringField())


class DisconWeek(EmbeddedDocument):
    days = ListField(EmbeddedDocumentField(DisconDay))


class DisconSchedule(Document):
    groups = ListField(EmbeddedDocumentField(DisconWeek), required=True, unique=True)
    last_update = DateTimeField(required=True)


def get_preset(browser) -> DisconSchedule | None:
    with preset_lock:
        if len(DisconSchedule.objects) >= 1:
            if len(DisconSchedule.objects) > 1:
                logger.warning('Multiple records for DisconSchedule')
            if expiration_check(DisconSchedule.objects[0]):
                browser.update_preset()
            return DisconSchedule.objects[0]

        preset = browser.update_preset()
        if preset is None:
            logger.error('Data base doesn`t have disconnect schedule and also cannot get it from browser')
        return preset


def expiration_check(preset: DisconSchedule) -> bool:
    now = datetime.now(timezone('Europe/Kiev'))
    last_update = preset.last_update.replace(tzinfo=timezone('Europe/Kiev'))
    calculation = now - last_update
    expired = calculation.days >= 1
    if expired:
        expired_log = 'The preset has already expired\n'
        expired_log += f'{now=}, {last_update=},' \
                       f'{calculation=}'
        logger.info(expired_log)

    return expired
