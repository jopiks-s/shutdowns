from mongoengine import Document, IntField, BooleanField


class User(Document):
    tg_id = IntField(required=True, unique=True)
    group = IntField(default=-1)
    notification = BooleanField(default=False)
