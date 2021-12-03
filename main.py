# -*- coding: utf-8 -*-

from botrequests.handlers import bot, next_step_city, user, logging
from botrequests.myclass import Users
from botrequests.requests_api import datetime
from botrequests.locales import info_help


@bot.message_handler(commands=["help", "lowprice", "highprice", "bestdeal", "history"])
def comands_message(message):
    print(message)
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    if message.text.lower() == "/help":
        bot.send_message(message.from_user.id, info_help,
                         reply_markup=user[message.from_user.id].getStart_kbd())

    elif message.text.lower() == '/start':
        start_help_text = f"Привет {user[message.from_user.id].username}, я БОТ по поиску отелей✅,\n" \
                              "И я готов подобрать для Вас отель 🏨"
        bot.send_message(message.from_user.id, start_help_text,
                         reply_markup=user[message.from_user.id].getStart_kbd())

    elif message.text.lower() == '/lowprice':
        user[message.chat.id].command = message.text
        msg = bot.send_message(message.from_user.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, next_step_city)

    elif message.text.lower() == '/history':
        history = user[message.from_user.id].history()
        if not history:
            history = 'Ваша история пуста'
        bot.send_message(message.from_user.id, (",").join(history), parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    user[call.message.chat.id].clearCache()
    if call.data == '/lowprice':
        user[call.message.chat.id].command = call.message.text
        msg = bot.send_message(call.message.from_user.id, 'В каком городе будем искать?')
        bot.register_next_step_handler(msg, next_step_city)

    elif call.data == '/history':
        history = user[call.message.from_user.id].history()[0]
        if not history:
            history = 'Ваша история пуста'
        bot.send_message(call.message.from_user.id, (",").join(history), parse_mode="Markdown")


if __name__ == '__main__':
    while True:
        try:
            logging.error(f"{datetime.now()} - Бот запущен")
            bot.polling(none_stop=True, interval=0)
        except Exception as ex:
            logging.error(f"{datetime.now()} - {ex}")
