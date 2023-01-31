from config import bot_token
from bot_lib.bot import Bot

bot = Bot(bot_token)
bot.loop()