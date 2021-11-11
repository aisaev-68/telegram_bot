import os
from dotenv import load_dotenv
import telebot
from telebot import types

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

bot = telebot.TeleBot(TOKEN, parse_mode=None)

@bot.message_handler(commands=["help", "start", "lowprice"])
def comands_message(message):
    print(message)
    if message.text == "/help":
        bot.send_message(message.from_user.id, "/lowprice: поиск дешевых отелей.")
    elif message.text == "/start":
        low_command = types.KeyboardButton('/lowprice')
        kbd = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kbd.row(low_command)
        bot.send_message(message.from_user.id, "Поиск отелей.", reply_markup=kbd)
    elif message.text == "/lowprice":
        #users[message.chat.id].hotel.sort_order = 'PRICE'
        bot.send_message(message.from_user.id, "Поиск дешевых отелей.\nКакой город искать?")

@bot.message_handler(content_types=["text"])
def text_message(message):
    print(message.text)




if __name__ == '__main__':
    bot.polling(none_stop=True)
