from bot import response
from bot import db


def not_command(self, message: response.Message):
    # time.sleep(random.random()*5)
    self.client.send_message(message.chat.id,
                             f"Your message: {message.text}")


def start_command(self, message: response.Message):
    self.client.send_message(message.chat.id,
                             f"Got command: {message.command}, params: {message.parameters}")

    user_id = message.from_.id
    if len(db.User.objects(tg_id=user_id)):
        return

    db.User(tg_id=user_id).save()
