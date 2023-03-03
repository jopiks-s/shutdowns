from bot import response
from bot import db
from log import logger


def not_command(self, message: response.Message):
    # time.sleep(random.random()*5)
    self.client.send_message(message.chat.id,
                             f"Your message: {message.text}")


def start_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"Got command: {message.command}, params: {message.parameters}")


def setgroup_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"Got command: {message.command}, params: {message.parameters}")

    user = db.get_user(message.from_.id)
    match message.parameters:
        case (1 | 2 | 3 as group, *_):
            logger.debug('correct group')
        case (group, *_) if isinstance(group, int):
            logger.debug('int out of range')
        case (group, *_):
            logger.debug('first argument must be int')
        case ():
            logger.debug('no args')
