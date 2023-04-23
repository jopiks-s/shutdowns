from threading import Lock
from datetime import datetime

from mongoengine import *
from log import logger

preset_lock = Lock()


class DisconDay(EmbeddedDocument):
    timetable = ListField(StringField())


class DisconWeek(EmbeddedDocument):
    days = ListField(EmbeddedDocumentField(DisconDay))


class DisconSchedule(Document):
    groups = ListField(EmbeddedDocumentField(DisconWeek), required=True, unique=True)
    last_update = DateTimeField(default=datetime.utcnow())


def get_preset(browser) -> DisconSchedule | None:
    with preset_lock:
        if len(DisconSchedule.objects) >= 1:
            if len(DisconSchedule.objects) > 1:
                logger.warning('Multiple records for DisconSchedule')
            if _expiration_check(DisconSchedule.objects[0]):
                browser.update_preset()
            return DisconSchedule.objects[0]
        else:
            preset = browser.update_preset()
            if preset is None:
                logger.error('Data base doesn`t have disconnect schedule and also cannot get it from browser')
            return preset


def _expiration_check(preset: DisconSchedule) -> bool:
    return (datetime.utcnow() - preset.last_update).days >= 1
    # return True
