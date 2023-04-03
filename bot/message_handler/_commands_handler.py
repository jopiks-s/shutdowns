from bot import db
from bot.botAPI import response
from log import logger


def not_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Your message: {message.text}")


def start_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")


def setgroup_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")

    user = db.get_user(message.from_.id)
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

        case ():
            message = '/setgroup [1-3]\n' \
                      'Where [1-3] is your group number\n'
            self.client.send_message(user.user_id, message)


def notification_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")
    user = db.get_user(message.from_.id)
    user.notification = not user.notification
    user.save()
    message = 'Your notification is now enabled' if user.notification else 'Your notification is now disabled'
    self.client.send_message(user.user_id, message)
    logger.warning('Missing logic to disable scheduled notifications for user')


def info_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"[DEBUG] Got command: {message.command}, params: {message.parameters}")
    user = db.get_user(message.from_.id)
    message = ''
    if user.group == -1:
        if user.notification:
            logger.warning('Enabled notifications while group isn`t set')
        message = 'Your group isn`t set and notification disabled'
    else:
        message = f'Your group is {user.group}\n'
        message += f'Notification enabled' if user.notification else 'Notification disabled'

    self.client.send_message(user.user_id, message)


def about_command(self, message: response.Message):
    ...
