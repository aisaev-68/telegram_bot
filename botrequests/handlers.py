# -*- coding: utf-8 -*-
import time

from decouple import config
import logging
from requests import get
import re
from locales import loctxt, info_help
from telebot import types
from telebot.async_telebot import AsyncTeleBot
from requests_api import get_city_id, query_string, hotel_query
from telegram_bot_calendar import WYearTelegramCalendar, DAY

bot = AsyncTeleBot(config('TELEGRAM_API_TOKEN'))

logging.basicConfig(filename="logger.log", level=logging.INFO)

user = {}


class MyStates:
    ask_search_city = 1
    ask_specify_city = 2
    ask_history = 3



class MyStyleCalendar(WYearTelegramCalendar):
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"


async def check_city(mess):
    """
        Функция проверки на корректность ввода названия города. re.findall(r'^[а-яА-ЯёЁa-zA-Z-\s]+$', txt)
    """
    if len(re.findall(r'^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', mess.text)) == 0:
        # err_city = bot.send_message(mess.chat.id,
        #                             'Город должен содержать только буквы, пробел и дефис, вводи еще раз город.')
        # user[mess.chat.id].message_id = err_city.message_id
        m = await bot.send_message(chat_id=mess.from_user.id,
                                   text=loctxt[user[mess.chat.id].language][3])
        user[mess.chat.id].message_id = m.message_id
        # bot.register_next_step_handler(m, next_step_city)
        # await next_step_city(m)
    else:
        return True

@bot.message_handler(state="*", commands='cancel')
async def any_state(message):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, "Команда отменена")
    await bot.delete_state(message.from_user.id)

@bot.message_handler(state=MyStates.ask_search_city)
async def ask_search_city(message):
    """
    State 2. Will process when user's state is 2.
    """

    user[message.from_user.id].message_id = message.message_id
    # await bot.set_state(message.from_user.id, MyStates.ask_specify_city)
    async with bot.retrieve_data(message.from_user.id) as user[message.chat.id].search_city:
        user[message.chat.id].search_city = message.text.lower()
    user[message.chat.id].language = (
        "ru_RU" if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', message.text.lower())) else "en_US")
    user[message.chat.id].currency = ('RUB' if user[message.chat.id].language == 'ru_RU' else 'USD')
    await bot.set_my_commands(user[message.chat.id].my_commands)
    msg = await bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][0])
    user[message.chat.id].message_id = msg.message_id
    await bot.delete_state(message.chat.id)
    await ask_specify_city(message)


async def ask_specify_city(message):
    lng = user[message.from_user.id].language
    city_list = get_city_id(user[message.chat.id].search_city, lng)
    print(city_list)
    print(type(city_list))
    if isinstance(city_list, list):
        if len(city_list) > 1:
            markup = types.InlineKeyboardMarkup(row_width=2)
            for i in city_list:
                button = types.InlineKeyboardButton(i['city_name'], callback_data='cbid_' + str(i["destinationID"]))
                markup.add(button)
            await bot.edit_message_text(text=loctxt[lng][21], chat_id=message.chat.id,
                                        message_id=user[message.chat.id].message_id,
                                        parse_mode='html', reply_markup=markup)


        elif len(city_list) == 1:
            user[message.from_user.id].id_city = city_list[0]['destinationID']
            await ask_date(message, 'Введите дату заезда')
        else:
            command = user[message.chat.id].command
            user[message.chat.id].clearCache()
            user[message.chat.id].command = command
            await bot.send_message(message.chat.id, loctxt[lng][2])
            await bot.set_state(message.from_user.id, MyStates.ask_search_city)
            await bot.send_message(message.chat.id, loctxt[lng][3])
    else:
        await bot.send_message(message.chat.id, city_list)


async def ask_date(message, txt):
    lng = user[message.chat.id].language
    await bot.edit_message_text(text=txt, chat_id=message.chat.id,
                                message_id=user[message.chat.id].message_id,
                                parse_mode='MARKDOWN',
                                reply_markup=MyStyleCalendar(calendar_id=1,
                                                             locale=lng[:2]).build()[0])


async def ask_count_hotels(message):
    """Функция предлагает указать количество отелей, которые необходимо вывести
    :param message: входящее сообщение от пользователя
    """
    lng = user[message.chat.id].language
    await bot.edit_message_text(text=loctxt[lng][5],
                                chat_id=message.chat.id,
                                message_id=user[message.chat.id].message_id,
                                reply_markup=user[message.chat.id].getHotel_kbd())


async def ask_show_photo(message):
    """Функция предлагает показ фотографии отелей
    :param message: входящее сообщение от пользователя
    """
    lng = user[message.chat.id].language
    await bot.edit_message_text(text=loctxt[lng][6], chat_id=message.chat.id,
                                message_id=user[message.chat.id].message_id,
                                reply_markup=user[message.chat.id].getPhoto_yes_no())


async def ask_count_photo(message):
    """
    Функция прелагает выбрать количество фото для загрузки
    :param mess: объект входящего сообщения от пользователя
    """
    lng = user[message.chat.id].language
    await bot.edit_message_text(text=loctxt[lng][7], chat_id=message.chat.id,
                                message_id=user[message.chat.id].message_id,
                                reply_markup=user[message.chat.id].getKbd_photo_numb())


async def step_show_info(message):
    """
    Функция для вывода информации в чат
    :param mess: объект входящего сообщения от пользователя
    """
    await bot.delete_message(chat_id=message.chat.id, message_id=user[message.chat.id].message_id)
    querystring = query_string(user[message.chat.id].command, user[message.chat.id].getSource_dict())
    user[message.chat.id].all_hotels = hotel_query(querystring, user[message.chat.id].getSource_dict())
    count_hotel = len(user[message.chat.id].all_hotels)
    if isinstance(user[message.chat.id].all_hotels, dict):
        user[message.chat.id].insert_db()
        if count_hotel > 0:
            for hotel, photo_list in user[message.chat.id].all_hotels.items():
                media_list = []
                if len(photo_list) > 1:
                    first_photo = photo_list[0]
                    media_list = [types.InputMediaPhoto(media=first_photo, caption=hotel, parse_mode="Markdown")]
                    for ind in range(1, len(photo_list)):
                        time.sleep(1)
                        media_list.append(types.InputMediaPhoto(photo_list[ind]))
                    await bot.send_media_group(chat_id=message.chat.id,
                                               media=media_list)
                elif len(photo_list) == 1:
                    await bot.send_media_group(chat_id=message.chat.id,
                                               media=[types.InputMediaPhoto(photo_list[0], caption=hotel,
                                                                            parse_mode="Markdown")])
                else:
                    if user[message.chat.id].status_show_photo:
                        img = open('botrequests/images/f5ed7098_z.jpg', 'rb')
                        await bot.send_media_group(chat_id=message.chat.id,
                                                   media=[types.InputMediaPhoto(media=img,
                                                                                caption=hotel, parse_mode="Markdown")])
                        img.close()
                    else:
                        img = open('botrequests/images/1e007e4f_z', 'rb')
                        await bot.send_media_group(chat_id=message.chat.id,
                                                   media=[types.InputMediaPhoto(media=img,
                                                                                caption=hotel, parse_mode="Markdown")])
                        img.close()

        else:
            lng = user[message.chat.id].language
            command = user[message.chat.id].command
            user[message.chat.id].clearCache()
            user[message.chat.id].command = command
            await bot.send_message(message.chat.id, user[message.chat.id].all_hotels)
            await bot.send_message(message.chat.id, loctxt[lng][3])
            await bot.set_state(message.from_user.id, MyStates.ask_search_city)

        await bot.send_message(chat_id=message.chat.id,
                               text=loctxt[user[message.chat.id].language][22].format(count_hotel))
        user[message.from_user.id].clearCache()

    else:
        await bot.send_message(chat_id=message.chat.id, text=user[message.from_user.id].all_hotels)
        user[message.from_user.id].message_id = message.message_id


async def history(message):
    lng = (message.from_user.language_code + "_RU" if not user[message.chat.id].language else user[
        message.chat.id].language)
    await bot.set_my_commands(user[message.chat.id].my_commands)
    history = user[message.chat.id].history()
    txt = loctxt[lng][16]
    if len(history) == 0:
        txt += loctxt[lng][17]
        await bot.send_message(chat_id=message.chat.id, text=txt)
    else:
        for item in history:
            txt += f'{loctxt[lng][18]} {item[0]}\n{loctxt[lng][19]} {item[1]}\n{item[2]}\n'
            await bot.send_message(chat_id=message.chat.id, text=txt, disable_web_page_preview=True)
            txt = ''
    await bot.send_message(chat_id=message.chat.id, text='Команда выполнена')


@bot.callback_query_handler(func=lambda call: True)
async def inline(call):
    lng = user[call.message.chat.id].language
    if call.data in ['/help']:
        m = await bot.send_message(text=info_help[lng], chat_id=call.message.from_user.id)
        user[call.message.chat.id].message_id = m.message_id

    elif call.data in ['yes_photo', 'no_photo']:
        user[call.message.chat.id].status_show_photo = (True if call.data == 'yes_photo' else False)
        if user[call.message.chat.id].status_show_photo:
            await ask_count_photo(call.message)
        else:
            await step_show_info(call.message)

    elif call.data.startswith('cbcal_1'):
        result, key, step = MyStyleCalendar(calendar_id=1).process(call.data)
        if not result:
            await bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                                message_id=user[call.message.chat.id].message_id,
                                                reply_markup=key)
        elif result:
            if not user[call.message.chat.id].checkIn:
                user[call.message.chat.id].checkIn = result.strftime('%Y-%m-%d')
                await bot.answer_callback_query(callback_query_id=call.id,
                                                text=loctxt[lng][9])
                await ask_date(call.message, 'Введите дату выезда')

            else:
                user[call.message.chat.id].checkOut = result.strftime('%Y-%m-%d')
                if user[call.message.chat.id].checkOut > user[call.message.chat.id].checkIn:
                    await ask_count_hotels(call.message)
                    await bot.answer_callback_query(callback_query_id=call.id,
                                                    text=loctxt[lng][10])
                else:
                    await ask_date(call.message, 'Введите дату выезда')

    elif call.data in ["five", "ten", "fifteen", "twenty", "twenty_five"]:
        numbers_hotel = {"five": 5, "ten": 10, "fifteen": 15, "twenty": 20, "twenty_five": 25}
        user[call.message.chat.id].count_show_hotels = numbers_hotel[call.data]
        await bot.answer_callback_query(callback_query_id=call.id)
        await ask_show_photo(call.message)

    elif call.data in ["one_photo", "two_photo", "three_photo", "four_photo", "five_photo"]:
        numbers_photo = {"one_photo": 1, "two_photo": 2, "three_photo": 3, "four_photo": 4, "five_photo": 5}
        user[call.message.chat.id].count_show_photo = numbers_photo[call.data]
        await bot.answer_callback_query(callback_query_id=call.id)
        await step_show_info(call.message)

    elif call.data in ['ru_RU', 'en_US']:
        user[call.message.chat.id].language = call.data
        await bot.set_my_commands(user[call.message.chat.id].my_commands)
        user[call.message.chat.id].message_id = call.message.message_id
        await bot.delete_message(chat_id=call.message.chat.id, message_id=user[call.message.chat.id].message_id)
        await bot.answer_callback_query(callback_query_id=call.id)

    elif call.data.startswith('cbid_'):
        user[call.message.chat.id].id_city = call.data[5:]
        user[call.message.chat.id].message_id = call.message.message_id
        await ask_date(call.message, 'Введите дату заезда')

    else:
        await bot.answer_callback_query(callback_query_id=call.id)
