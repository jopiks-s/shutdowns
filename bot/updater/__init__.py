import time
import traceback
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from threading import Thread, current_thread

from mongoengine import ValidationError
from pytz import timezone

from bot import db
from log import logger

update_rate = None
fresh = False


def expired(preset: db.DisconSchedule) -> bool:
    if update_rate is None:
        logger.warning('Uninitialized Updater class, update_rate not set')
        return True
    if preset is None:
        logger.warning('Preset is None')
        return True

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
    def __init__(self, upd_rate: int, browser, notification, check_rate: int = 15):
        global update_rate
        update_rate = upd_rate
        self.check_rate = check_rate
        self.browser = browser
        self.notification = notification

        self._update_data(boot_up=True, debug=True)

    def _loop(self):
        logger.info(f'Updater looping: {current_thread().name}')
        with True:
            time.sleep(self.check_rate * 60)  # min to sec

            preset = db.get_preset()
            if expired(preset):
                self.fresh = False
                self._update_data()
                logger.info('Preset updated in a given interval')
            else:
                logger.info('Preset still fresh')

    def start_thread(self, executor: ThreadPoolExecutor):
        executor.submit(Thread(name="updater0", target=self._loop).start)

    def _update_data(self, boot_up=False, debug=False):
        global fresh
        if not debug:
            new_preset = self._update_preset()
            if new_preset is None:
                logger.warning('Failed to update data')
                if boot_up:
                    raise RuntimeError('Unable to initialize data because preset could not be retrieved')
                return
        else:
            new_preset = db.get_preset()
        fresh = True
        self.browser.update_photos(new_preset)
        self.notification.update_all_notification(new_preset)
        logger.info('Successfully updated data')

    def _update_preset(self) -> db.DisconSchedule | None:
        new_preset = self.browser.retrieve_preset()
        if new_preset is None:
            logger.warning('Failed to update preset')
            return

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
                           f'Exception:\n'
                           f'{traceback.print_exc()}')
            return
