from threading import Lock

from mongoengine import Document, IntField, StringField

from log import logger

user_lock = Lock()


class User(Document):
    user_id = IntField(required=True, unique=True)
    group = IntField(default=None)
    notification_advance = IntField(min_value=0, max_value=1440, default=15)
    language_code = StringField(default='uk')


def get_user(user_id: int, language_code: str) -> User:
    with user_lock:
        users = User.objects(user_id=user_id)
        if len(users) >= 1:
            if len(users) > 1:
                logger.warning(f'Multiple records for user_id: {user_id}')

            # user = User.objects(user_id=user_id)[0]
            user = users[0]
            user.language_code = language_code
            return user.save()
        else:
            return User(user_id=user_id, language_code=language_code).save()
