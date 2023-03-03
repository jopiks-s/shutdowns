from mongoengine import Document, IntField, BooleanField, connect

from log import logger

connect('tg')


class User(Document):
    user_id = IntField(required=True, unique=True)
    group = IntField(default=-1)
    notification = BooleanField(default=False)


def get_user(user_id: int) -> User:
    users = User.objects(user_id=user_id)
    if len(users) > 1:
        logger.error(f'Multiple records for user_id: {user_id}')
    if len(users):
        return users[0]
    return User(user_id=user_id).save()
