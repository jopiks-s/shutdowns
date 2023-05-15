import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Thread, current_thread

import schedule
from mongoengine import ValidationError
from pytz import timezone

from bot import db
from log import logger

update_rate = None
fresh = False


# todo this is crap :(, why it even exists?
def expired(preset: db.DisconSchedule) -> bool | None:
    if update_rate is None:
        logger.warning('Uninitialized Updater class, update_rate not set')
        return

    now = datetime.now(timezone('Europe/Kiev')).replace(tzinfo=None)
    last_update = preset.last_update
    calculation = now - last_update
    is_expired = calculation.days >= update_rate
    if is_expired:
        expired_log = 'The preset has already expired\n'
        expired_log += f'{now=}, {last_update=},\n' \
                       f'{calculation=}'
        logger.info(expired_log)

    return is_expired


class Updater:
    def __init__(self, upd_rate: int, browser, notification):
        global update_rate
        update_rate = upd_rate
        self.browser = browser
        self.notification = notification

        schedule.every(update_rate).days.do(self._update_data)
        self._update_data(boot_up=True)

    def _loop(self):
        # todo replace schedule with simple sleep
        logger.info(f'Updater looping: {current_thread().name}')
        with True:
            schedule.run_pending()
            time.sleep(300)

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="updater0", target=self._loop).start)

    def _update_data(self, boot_up=False):
        global fresh
        new_preset = self._update_preset()
        if new_preset is None:
            logger.warning('Failed to update data')
            fresh = False
            if boot_up:
                raise RuntimeError('Unable to initialize data because preset could not be retrieved')
            return

        fresh = True
        self.browser.update_photos(new_preset)
        self.notification.update_all_notification(new_preset)
        logger.info('Successfully updated data')

    def _update_preset(self) -> db.DisconSchedule | None:
        new_preset = self.browser.retrieve_preset()
        try:
            new_preset.validate()
            db.DisconSchedule.objects().delete()
            new_preset.save()
            logger.info('Preset successfully updated')
            return new_preset
        except ValidationError as e:
            logger.warning('Failed to update preset\n'
                           'Can`t validate "preset" to create "DisconSchedule" object\n'
                           f'Object to validate: {new_preset.to_json(indent=4)}\n'
                           f'Exception: {e}')
            return
