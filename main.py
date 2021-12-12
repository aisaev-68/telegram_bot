# -*- coding: utf-8 -*-

from user import Users
import logging
from datetime import datetime
from telebot import asyncio_filters
from botrequests.handlers import user, bot, MyStates, history


@bot.message_handler(commands=["help"])
async def help_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    await bot.send_message(chat_id=message.chat.id,
                           text='Выберите язык (Choose language)',
                           reply_markup=user[message.chat.id].getInl_lang())


@bot.message_handler(commands=["start"])
async def start_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    await bot.send_message(chat_id=message.chat.id,
                           text='Выберите язык (Choose language)',
                           reply_markup=user[message.chat.id].getInl_lang())



@bot.message_handler(commands=["lowprice"])
async def lowprice_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    user[message.chat.id].command = message.text.lower()
    await bot.set_state(message.from_user.id, MyStates.ask_search_city)
    await bot.send_message(message.chat.id, 'В каком городе будем искать?')




@bot.message_handler(commands=["highprice"])
async def highprice_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    pass


@bot.message_handler(commands=["bestdeal"])
async def bestdeal_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    pass


@bot.message_handler(commands=["history"])
async def history_message(message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    await bot.send_message(message.chat.id, 'Будет выведена информация о двух последних запросах')
    await history(message)



if __name__ == '__main__':
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))
    while True:
        try:
            logging.error(f"{datetime.now()} - Бот запущен")
            import asyncio
            asyncio.run(bot.polling(none_stop=True, interval=0))
        except Exception as ex:
            logging.error(f"{datetime.now()} - {ex}")
