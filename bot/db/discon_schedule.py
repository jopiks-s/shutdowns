from datetime import datetime

from mongoengine import *
from pytz import timezone

from log import logger


class DisconDay(EmbeddedDocument):
    timetable = ListField(StringField())


class DisconWeek(EmbeddedDocument):
    days = ListField(EmbeddedDocumentField(DisconDay))


class DisconSchedule(Document):
    groups = ListField(EmbeddedDocumentField(DisconWeek), required=True, unique=True)
    last_update = DateTimeField(required=True)


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
