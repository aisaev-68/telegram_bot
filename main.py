# -*- coding: utf-8 -*-

from user import Users
import logging
from datetime import datetime
from botrequests.handlers import user, bot, ask_search_city, history, info_help, re

l_text = {'ru_RU': ['В каком городе будем искать?', 'Будет выведена информация о двух последних запросах',
                    'Извините, данная команда мне неизвестна.\n'],
          'en_US': ['What city are we looking for?', 'Information about the last two requests will be displayed',
                    'Sorry, this command is unknown to me.\n']}


@bot.message_handler(commands=["help", "start"])
def help_start_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    user[message.chat.id].command = message.text.lower()
    bot.send_message(chat_id=message.chat.id,
                     text='Выберите язык (Choose language)',
                     reply_markup=user[message.chat.id].getInl_lang())


@bot.message_handler(commands=["lowprice", "highprice"])
def lowprice_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    user[message.chat.id].command = message.text.lower()
    if user[message.chat.id].language == '':
        user[message.chat.id].language = (
            message.from_user.language_code + "_RU" if not user[message.chat.id].language else user[
                message.chat.id].language)
    m = bot.send_message(message.chat.id, l_text[user[message.chat.id].language][0])
    bot.register_next_step_handler(m, ask_search_city)


@bot.message_handler(commands=["bestdeal"])
def bestdeal_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    pass


@bot.message_handler(commands=["history"])
def history_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    if user[message.chat.id].language == '':
        user[message.chat.id].language = (
            message.from_user.language_code + "_RU" if not user[message.chat.id].language else user[
                message.chat.id].language)
    bot.send_message(message.chat.id, l_text[user[message.chat.id].language][1])
    history(message)

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].language = (
        "ru_RU" if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', message.text.lower())) else "en_US")
    bot.send_message(text=l_text[user[message.chat.id].language][2] + info_help[user[message.chat.id].language],
                     chat_id=message.from_user.id)

if __name__ == '__main__':
    while True:
        try:
            logging.error(f"{datetime.now()} - Бот запущен")
            bot.polling(none_stop=True, interval=0)
        except Exception as ex:
            logging.error(f"{datetime.now()} - {ex} - Модуль main")
