from mongoengine import connect

from .discon_schedule import DisconSchedule, get_preset, expiration_check
from .user import User, get_user

connect('tg')
