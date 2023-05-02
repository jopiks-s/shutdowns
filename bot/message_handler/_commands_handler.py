import random

from bot import db
from bot.botAPI import response
from log import logger


def not_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Your message: {message.text}")


def start_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")


def viewschedule_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")

    user = db.user.get_user(message.from_.id)
    preset = db.get_preset(self.browser)
    debug_msg = ''

    if preset is None:
        debug_msg = 'Unfortunately, we are now unable to access the shutdown schedule :('
    else:
        for group in preset.groups:
            for day in group.days:
                debug_msg += str(day.timetable) + '\n'
            debug_msg += '-' * 100 + '\n'
        debug_msg += str(preset.last_update)
    # todo return group of user if parameters is empty
    if not len(message.parameters):
        group_index = random.randint(1, 3)
    else:
        group_index = message.parameters[0]

    self.client.send_message(user.user_id, debug_msg)
    self.client.send_photo(user.user_id, self.browser.get_preset_photo(group_index), f'Group {group_index}')


def setgroup_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")

    user = db.user.get_user(message.from_.id)
    match message.parameters:
        case (1 | 2 | 3 as group, *_):
            user.group = group
            user.save()
            message = 'Your group has been successfully updated!'
            logger.warning('Missing logic to update notification schedule according with new group index')
            self.client.send_message(user.user_id, message)

        case (group, *_) if isinstance(group, int):
            message = f'You send group number {group}, but possible only in range 1-3'
            self.client.send_message(user.user_id, message)

        case (group, *_):
            message = 'Wrong command :<\n' \
                      'The correct way "/setgroup [1-3]"\n' \
                      'Where [1-3] is your group number\n'
            self.client.send_message(user.user_id, message)

        case _:
            message = 'Syntax: /setgroup [1-3]\n' \
                      'Where [1-3] is your group number\n'
            self.client.send_message(user.user_id, message)


def notification_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")

    user = db.user.get_user(message.from_.id)
    user.notification = not user.notification
    user.save()
    message = 'Your notification is now enabled' if user.notification else 'Your notification is now disabled'
    self.client.send_message(user.user_id, message)
    logger.warning('Missing logic to disable scheduled notifications for user')


def info_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")

    user = db.user.get_user(message.from_.id)
    if user.group == -1:
        if user.notification:
            logger.warning('Enabled notifications while group isn`t set')
            logger.warning(f'User id: {user.id}')
        message = 'Your group isn`t set and notification disabled'
    else:
        message = f'Your group is {user.group} \nNotification {"Enabled" if user.notification else "Disabled"}'

    self.client.send_message(user.user_id, message)


def about_command(self, message: response.Message):
    ...
