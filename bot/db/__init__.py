from threading import Lock

from mongoengine import connect

from bot.browser import Browser
from bot.notification import Notification
from log import logger
from .discon_schedule import DisconSchedule, expiration_check
from .user import User, get_user

connect('tg')


class DB:
    def __init__(self, browser: Browser, notification: Notification):
        self.browser = browser
        self.notification = notification
        self.preset_lock = Lock()

    def get_preset(self) -> DisconSchedule | None:
        with self.preset_lock:
            if len(DisconSchedule.objects) >= 1:
                if len(DisconSchedule.objects) > 1:
                    logger.warning('Multiple records for DisconSchedule')
                if expiration_check(DisconSchedule.objects[0]):
                    self._update_storage()
                return DisconSchedule.objects[0]

            if not self._update_storage():
                logger.error('Data base doesn`t have disconnect schedule and also cannot get it from browser')
                return None

            return DisconSchedule.objects[0]

    def _update_storage(self) -> bool:
        new_preset = self.browser.update_preset()
        if new_preset is None:
            logger.warning('Failed to update storage')
            return False
        self.browser.update_photos(new_preset)
        self.notification.update_all_notification(new_preset)
        return True
