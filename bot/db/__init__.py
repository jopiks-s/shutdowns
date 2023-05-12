from threading import Lock
from typing import Tuple

from mongoengine import connect

from bot.browser import Browser
from log import logger
from .discon_schedule import DisconSchedule, expiration_check
from .user import User, get_user

connect('tg')


class DB:
    def __init__(self, browser: Browser, notification):
        self.browser = browser
        self.notification = notification
        self.preset_lock = Lock()

    def get_preset(self, boot_up=False) -> Tuple[DisconSchedule, bool] | None:
        with self.preset_lock:
            if len(DisconSchedule.objects) >= 1:
                updated = False
                if len(DisconSchedule.objects) > 1:
                    logger.warning('Multiple records for DisconSchedule')
                if expiration_check(DisconSchedule.objects[0]):
                    updated = self._update_storage(boot_up)
                return DisconSchedule.objects[0], updated

            if not self._update_storage(boot_up):
                logger.error('Data base doesn`t have disconnect schedule and also cannot get it from browser')
                return None

            return DisconSchedule.objects[0], True

    def _update_storage(self, boot_up) -> bool:
        new_preset = self.browser.update_preset()
        if new_preset is None:
            logger.warning('Failed to update storage')
            return False
        if boot_up:
            return True
        self.browser.update_photos(new_preset)
        self.notification.update_all_notification(new_preset)  # !!! deadlock
        return True
