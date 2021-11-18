import datetime
import os
import telebot
from dotenv import load_dotenv
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from telegram_bot_calendar import WMonthTelegramCalendar, LSTEP, DAY



dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

bot = telebot.TeleBot(TOKEN, parse_mode=None)

data = {}
class MyStyleCalendar(WMonthTelegramCalendar):
    prev_button = "⬅️"
    next_button = "➡️"
    first_step = DAY

def gen_markup():
    calendar, step = MyStyleCalendar(calendar_id=1).build()
    return calendar

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id,
                     "Выберите дату въезда",
                     reply_markup=gen_markup())



def start1(m):

    calendar, step = MyStyleCalendar(calendar_id=1).build()
    bot.send_message(m.chat.id,
                     "Выберите дату выезда",
                     reply_markup=calendar)





@bot.callback_query_handler(func=MyStyleCalendar.func(calendar_id=1))
def cal1(c):
    # calendar_id is used here too, since the new keyboard is made
    result, key, step = MyStyleCalendar(calendar_id=1).process(c.data)
    print(type(result))
    if result:
        bot.edit_message_text(f"Выбрана дата {result}",
                              c.message.chat.id,
                              c.message.message_id)
        if not data.get('in_date'):
            data['in_date'] = result.isoformat()
            bot.callback_query_handler(start1(c.message), reply_markup=gen_markup())
        else:
            data['out_date'] = result.isoformat()
            print(data)





if __name__ == '__main__':
    bot.polling(none_stop=True)