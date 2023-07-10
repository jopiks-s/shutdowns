from datetime import timedelta

from bot import db
from bot.botAPI import response, Messages
from log import logger


def not_command(self, message: response.Message):
    user = db.get_user(message.from_.id, message.from_.language_code)
    self.client.send_message(user, Messages.start)


def start_command(self, message: response.Message):
    user = db.get_user(message.from_.id, message.from_.language_code)
    self.client.send_message(user, Messages.start)


def view_command(self, message: response.Message):
    user = db.get_user(message.from_.id, message.from_.language_code)

    # TODO render 'no group' image when user.grop is None
    def handle_user_group(was_params: bool):
        if user.group is None:
            if was_params:
                self.client.send_message(user, Messages.view_failure_param)
            else:
                self.client.send_message(user, (Messages.view_failure_group, Messages.setgroup))
        else:
            self.client.send_photo(user, self.browser.get_photo(user.group), Messages.view_success, group=user.group)

    if len(message.parameters):
        group_index = message.parameters[0]
        if isinstance(group_index, int) and 1 <= group_index <= 3:
            self.client.send_photo(user, self.browser.get_photo(group_index), Messages.view_success, group=group_index)
        else:
            handle_user_group(True)
    else:
        handle_user_group(False)


def setgroup_command(self, message: response.Message):
    user = db.get_user(message.from_.id, message.from_.language_code)
    match message.parameters:
        case (1 | 2 | 3 as group, *_):
            user.group = group
            user = user.save()

            self.notification.subscribe_user(user)
            self.client.send_message(user, Messages.setgroup_success)

        case (group, *_) if isinstance(group, int):
            self.client.send_message(user, (Messages.setgroup_failure, Messages.setgroup))

        case (group, *_):
            self.client.send_message(user, (Messages.setgroup_failure, Messages.setgroup))

        case _:
            self.client.send_message(user, Messages.setgroup)


def notification_advance_command(self, message: response.Message):
    user = db.get_user(message.from_.id, message.from_.language_code)
    max_advance = db.User.notification_advance.max_value
    match message.parameters:
        case (advance, *_) if isinstance(advance, int) and 0 <= advance <= max_advance:
            user.notification_advance = advance
            user = user.save()
            self.notification.subscribe_user(user)
            self.client.send_message(user, Messages.notification_advance_success)

        case (advance, *_) if isinstance(advance, int):
            self.client.send_message(user, (Messages.notification_advance_failure, Messages.notification_advance))

        case (_, *_):
            self.client.send_message(user, (Messages.notification_advance_failure, Messages.notification_advance))

        case _:
            self.client.send_message(user, Messages.notification_advance)


def info_command(self, message: response.Message):
    user = db.get_user(message.from_.id, message.from_.language_code)
    if user.group is None:
        self.client.send_message(user, (Messages.info_unset, Messages.setgroup))
    else:
        # date_to_str = timedelta(minutes=user.notification_advance)
        # d = date_to_str.days
        # if d:
        #     time = str(date_to_str).split(',')[-1].strip()  # 0:00:00
        #     h, m = list(map(int, time.split(':')[0:-1]))  # [0, 0]
        # else:
        #     h, m = list(map(int, str(date_to_str).split(':')[0:-1]))  # [0, 0]
        #
        # advance = f'{d}d ' if d else ''
        # advance += f'{h:02d}h ' if h else ''
        # advance += f'{m:02d}min' if m else ''
        # advance = '0min' if not advance else advance
        # message = f'Your group is {user.group}\n' \
        #           f'Notification advance is {advance}'
        self.client.send_message(user, Messages.info_set, group=user.group,
                                 notification_advance=user.notification_advance)


def help_command(self, message: response.Message):
    return
