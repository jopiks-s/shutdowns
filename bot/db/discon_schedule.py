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


def get_preset() -> DisconSchedule | None:
    with preset_lock:
        if len(DisconSchedule.objects) >= 1:
            if len(DisconSchedule.objects) > 1:
                logger.warning('Multiple records for DisconSchedule')
            return DisconSchedule.objects[0]
        logger.warning('Failed to get preset')
        return
