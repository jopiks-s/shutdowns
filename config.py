import os
from dotenv import load_dotenv

load_dotenv()

bot_token = os.getenv('bot_token')
root_path = os.path.dirname(__file__)
