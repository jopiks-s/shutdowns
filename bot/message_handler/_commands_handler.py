from bot import db
from bot.botAPI import response
from log import logger


def not_command(self, message: response.Message):
    return


def start_command(self, message: response.Message):
    return


def view_command(self, message: response.Message):
    user = db.get_user(message.from_.id)

    # TODO render 'no group' image when user.grop is None
    def handle_user_group():
        if user.group is None:
            self.client.send_message(user.user_id, 'You have not yet set the group index\n'
                                                   'You can do this with the command - /setgroup 1-3\n'
                                                   'If you want to look at any group, write the command - /view 1-3')
        else:
            self.client.send_photo(user.user_id, self.browser.get_photo(user.group), f'Group {group_index}')

    if len(message.parameters):
        group_index = message.parameters[0]
        if isinstance(group_index, int) and 1 <= group_index <= 3:
            self.client.send_photo(user.user_id, self.browser.get_photo(group_index), f'Group {group_index}')
        else:
            handle_user_group()
    else:
        handle_user_group()


def setgroup_command(self, message: response.Message):
    user = db.get_user(message.from_.id)
    match message.parameters:
        case (1 | 2 | 3 as group, *_):
            user.group = group
            user = user.save()
            message = 'Your group has been successfully updated!'

            self.notification.subscribe_user(user)
            self.client.send_message(user.user_id, message)

        case (group, *_) if isinstance(group, int):
            message = f'You send group number of "{group}", but possible only in range 1-3'
            self.client.send_message(user.user_id, message)

        case (group, *_):
            message = 'Wrong command :<\n' \
                      'Maybe you meant this: "/setgroup 1-3"\n' \
                      'Where 1-3 is your group number\n'
            self.client.send_message(user.user_id, message)

        case _:
            message = 'Example: /setgroup 1-3\n' \
                      'Where 1-3 is your group index\n'
            self.client.send_message(user.user_id, message)


def notification_advance_command(self, message: response.Message):
    user = db.get_user(message.from_.id)
    max_advance = db.User.notification_advance.max_value
    match message.parameters:
        case (advance, *_) if 0 <= advance <= max_advance:
            user.notification_advance = advance
            user = user.save()

            logger.warning('Missing logic to update notifications according to new offset')

            message = 'Your notification advance has been successfully updated!'
            self.client.send_message(user.user_id, message)

        case (advance, *_) if isinstance(advance, int):
            message = f'You send notification advance of "{advance}", but possible only in range 0-{max_advance}'
            self.client.send_message(user.user_id, message)

        case (advance, *_):
            message = 'Wrong command :<\n' \
                      f'Maybe you meant this: "/notification_advance 0-{max_advance}"\n' \
                      f'Where 0-{max_advance} is notification advance in minutes'
            self.client.send_message(user.user_id, message)

        case _:
            message = f'Example "/notification_advance 0-{max_advance}"\n' \
                      f'Where 0-{max_advance} is notification advance in minutes'
            self.client.send_message(user.user_id, message)


def info_command(self, message: response.Message):
    user = db.get_user(message.from_.id)
    if user.group is None:
        message = 'Your group isn`t set yet\n' \
                  'Notification disabled'
    else:
        message = f'Your group is {user.group}\n' \
                  f'Notification advance is {user.notification_advance}min'

    self.client.send_message(user.user_id, message)


def help_command(self, message: response.Message):
    return
