from datetime import datetime

from mongoengine import *
from log import logger


class DisconDay(EmbeddedDocument):
    timetable = ListField(StringField())


class DisconWeek(EmbeddedDocument):
    days = ListField(EmbeddedDocumentField(DisconDay))


class DisconSchedule(Document):
    groups = ListField(EmbeddedDocumentField(DisconWeek), required=True, unique=True)
    last_update = DateTimeField(default=datetime.utcnow())


def get_preset(browser) -> DisconSchedule | None:
    if len(DisconSchedule.objects) >= 1:
        if len(DisconSchedule.objects) > 1:
            logger.warning('Multiple records for DisconSchedule')
        preset = DisconSchedule.objects[0]
        if _expiration_check(preset):
            preset = browser.update_preset()
        return DisconSchedule.objects[0] if preset is None else preset

    preset = browser.update_preset()
    if preset is None:
        logger.error('Data base doesn`t have disconnect schedule and also cannot get it from browser')
        return
    return preset


def _expiration_check(preset: DisconSchedule) -> bool:
    # return (datetime.utcnow() - preset.last_update).days > 1
    # todo debug version
    return (datetime.utcnow() - preset.last_update).days >= 0
