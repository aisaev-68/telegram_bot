import logging
from datetime import date, datetime
import os
from dotenv import load_dotenv
import telebot
from telebot import types
from telegram_bot_calendar import WMonthTelegramCalendar, LSTEP, DAY
from telebot.types import ReplyKeyboardRemove, CallbackQuery


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

usertable = dict()
usertable['USERNAME'] = True
TOKEN = os.environ.get('TELEGRAM_API_TOKEN')

bot = telebot.TeleBot(TOKEN, parse_mode=None)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

data = {}
LSTEP = {
    'ru':
        {'y': 'год', 'm': 'месяц', 'd': 'день'},
    'en':
        {'y': 'year', 'm': 'month', 'd': 'day'}
}
locale = 'ru'

class MyStyleCalendar(WMonthTelegramCalendar):
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"

calendar = MyStyleCalendar(locale=locale).build()

@bot.message_handler(commands=['start', 'help'])
def send_welcom(message):
    bot.reply_to(message, f'Хей, {message.from_user.first_name}')


@bot.message_handler(commands=['menu'])
def start(m):
    mg = bot.send_message(m.chat.id, "Имя")
    bot.register_next_step_handler(mg, next_date)

def next_date(mess):



    if not data.get('in'):
        markup1 = types.InlineKeyboardMarkup()
        in_data = types.InlineKeyboardButton(text='✅Дата въезда', callback_data='data_in')
        markup1.add(in_data)
        bot.send_message(mess.chat.id, "Выберите дату", reply_markup=markup1)

    if data.get('in') and not data.get('out'):
        markup2 = types.InlineKeyboardMarkup()
        out_data = types.InlineKeyboardButton(text='✅Дата выезда', callback_data='data_out')
        markup2.add(out_data)
        bot.send_message(mess.chat.id, "Выберите дату", reply_markup=markup2)


@bot.callback_query_handler(func=lambda c: c.data in ['data_in', 'data_out'])
def inline(c):
    if c.data == 'data_in':

        bot.send_message(c.message.chat.id,
                         "Выберите дату въезда",
                         reply_markup=calendar)
    elif c.data == 'data_out':

        bot.send_message(c.message.chat.id,
                         "Выберите дату выезда",
                         reply_markup=calendar)

@bot.callback_query_handler(func=MyStyleCalendar(locale=locale).func())
def cal(c):
    result, key, step = MyStyleCalendar().process(c.data)

    if not result and key:
        bot.edit_message_text(f"Select {LSTEP[locale][step]}",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        bot.edit_message_text(c.message.chat.id,
                              c.message.message_id,
                              reply_markup=ReplyKeyboardRemove())
        if not data.get('in'):
            data['in'] = result
            next_date(c.message)
        else:
            data['out'] = result
            print(data)



bot.polling(none_stop=True)