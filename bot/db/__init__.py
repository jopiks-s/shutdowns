from mongoengine import connect

from .discon_schedule import DisconSchedule, get_preset
from .user import User, get_user

connect('tg')
