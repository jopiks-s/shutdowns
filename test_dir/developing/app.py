from config import bot_token
import telebot
import parser

bot = telebot.TeleBot(bot_token)
start_c = telebot.types.BotCommand("start", "start bot")
setaddress_c = telebot.types.BotCommand("setaddress", "set your address")
bot.set_my_commands(commands=[start_c, setaddress_c])


@bot.message_handler(commands=["start"])
def start(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"hi, supported command = 'start'!, message text = {message.text}")
    bot.send_message(message.chat.id, parser.get_schedule(parser.address, parser.house_number))


@bot.message_handler(commands=["setaddress"])
def set_address(message: telebot.types.Message):
    bot.send_message(message.chat.id, f"supported command = 'setaddress'!, message text = {message.text}")
    address = message.text.replace("/setaddress", "").lstrip()
    bot.send_message(message.chat.id, f"Your new address: {address}")

    to_pin = bot.send_message(message.chat.id, address)
    bot.pin_chat_message(message.chat.id, to_pin.id)

@bot.message_handler(commands=["info"])
def info(message: telebot.types.Message):
    pass
    # print(message.chat.se)

def main():
    print("bot started")
    bot.infinity_polling()

if __name__ == "__main__":
    main()