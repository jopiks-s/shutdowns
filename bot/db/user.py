from threading import Lock

from mongoengine import Document, IntField

from log import logger

user_lock = Lock()

# TODO set max value for notify offset
class User(Document):
    user_id = IntField(required=True, unique=True)
    group = IntField(default=None)
    notification_advance = IntField(min_value=0, max_value=999, default=15)


def get_user(user_id: int) -> User:
    with user_lock:
        users = User.objects(user_id=user_id)
        if len(users) >= 1:
            if len(users) > 1:
                logger.warning(f'Multiple records for user_id: {user_id}')
            return users[0]
        else:
            return User(user_id=user_id).save()
