# -*- coding: utf-8 -*-

from requests import get
import re
from locales import loctxt
from telebot import TeleBot, types
from requests_api import get_city_id, query_string, hotel_query
from telegram_bot_calendar import WYearTelegramCalendar, DAY
from decouple import config
import logging


bot = TeleBot(config('TELEGRAM_API_TOKEN'))

logging.basicConfig(filename="logger.log", level=logging.INFO)

user = {}

class MyStyleCalendar(WYearTelegramCalendar):
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"

def next_step_city(mess):
    """
    Функция проверки на корректность ввода названия города.
    В случае корректного ввода города предлагает ввести дату заезда в гостиницу.
    :param mess: объект входящего сообщения от пользователя
    """

    if len(re.findall(r'[А-Яа-яЁёa-zA-Z0-9 -]+', mess.text)) > 1:
        err_city = bot.send_message(mess.chat.id,
                                    'Город должен содержать только буквы, повторите ввод.')
        bot.register_next_step_handler(err_city, next_step_city)
    else:
        user[mess.chat.id].search_city = mess.text
        user[mess.chat.id].language = ("ru_RU" if re.findall(r'[А-Яа-яЁё -]',
                                                             re.sub(r'[- ]', '', mess.text)) else "en_US")
        user[mess.chat.id].currency = ('RUB' if user[mess.chat.id].language == 'ru_RU' else 'USD')
        user[mess.chat.id].id_city = get_city_id(user[mess.chat.id].search_city,
                                                 user[mess.chat.id].language)

        if user[mess.chat.id].id_city is not None:
            loc = user[mess.chat.id].language[:2]
            msg = bot.send_message(chat_id=mess.chat.id, text="Выберите дату *ЗАЕЗДА*",
                                   parse_mode='MARKDOWN',
                                   reply_markup=MyStyleCalendar(calendar_id=1, locale=loc).build()[0])
            user[mess.chat.id].message_id_photo = msg.message_id

        else:
            bot.send_message(mess.chat.id, "Такой город не найден. Повторите поиск.")
            msg = bot.send_message(mess.chat.id, 'В каком городе будем искать?')
            bot.register_next_step_handler(msg, next_step_city)


def next_step_date(message):
    """Функция предлагает календарь для ввода даты выезда
    :param m: входящее сообщение от пользователя
    """
    loc = user[message.chat.id].language[:2]
    bot.edit_message_text(text="Выберите дату *ВЫЕЗДА*", chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id_photo,
                          parse_mode='MARKDOWN',
                          disable_web_page_preview=True,
                          reply_markup=MyStyleCalendar(calendar_id=1, locale=loc).build()[0])


def next_step_count_hotels(message):
    """Функция предлагает указать количество отелей, которые необходимо вывести
    :param message: входящее сообщение от пользователя
    """
    #time.sleep(1)
    bot.edit_message_text(text="Укажите количество отелей, которые необходимо вывести (не более 25)",
                          chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id_photo,
                          reply_markup=user[message.chat.id].hotel_class.getHotel_kbd())


def next_step_show_photo(message):
    """Функция предлагает показ фотографии отелей
    :param message: входящее сообщение от пользователя
    """

    bot.edit_message_text(text="Показать фотографии отелей?", chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id_photo,
                          reply_markup=user[message.chat.id].hotel_class.getPhoto_yes_no())


def next_step_count_photo(mess):
    """
    Функция прелагает выбрать количество фото для загрузки
    :param mess: объект входящего сообщения от пользователя
    """
    bot.edit_message_text(text="Выберите количество фото для загрузки", chat_id=mess.chat.id,
                          message_id=user[mess.chat.id].message_id_photo,
                          reply_markup=user[mess.chat.id].hotel_class.getKbd_photo_numb())


def next_step_show_info(mess):
    """
    Функция для вывода информации в чат
    :param mess: объект входящего сообщения от пользователя
    """
    print(user[mess.chat.id])
    bot.delete_message(chat_id=mess.chat.id, message_id=user[mess.chat.id].message_id_photo)
    querystring = query_string(user[mess.chat.id].command, user[mess.chat.id].getQuerystring())
    user[mess.chat.id].hotels_act.all_hotels = hotel_query(querystring)
    get_hotel = user[mess.chat.id].hotels_act.hotel_forward()
    if user[mess.chat.id].status_show_photo:
        get_photo = user[mess.chat.id].hotels_act.photo_forward()
        mes_id_photo = bot.send_photo(mess.chat.id, get(get_photo).content)
        user[mess.chat.id].message_id_photo = mes_id_photo.message_id
        keyboard_bot = user[mess.chat.id].hotels_act.getShow_kbd()
    else:
        keyboard_bot = user[mess.chat.id].hotels_act.getShowNoPhoto_kbd()

    meshotel = bot.send_message(chat_id=mess.chat.id, text="*" + get_hotel + "*",
                                parse_mode='MARKDOWN',
                                disable_web_page_preview=True,
                                reply_markup=keyboard_bot)
    user[mess.chat.id].message_id_hotel = meshotel.message_id


def next_hotel_show(call):
    get_hotel = user[call.message.chat.id].hotels_act.hotel_forward()
    if user[call.message.chat.id].status_show_photo:
        keyboard_bot = user[call.message.chat.id].hotels_act.getShow_kbd()
        photo = user[call.message.chat.id].hotels_act.photo_forward()
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=user[call.message.chat.id].message_id_photo,
                               media=types.InputMediaPhoto(get(photo).content))
    else:
        keyboard_bot = user[call.message.chat.id].hotels_act.getShowNoPhoto_kbd()

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=user[call.message.chat.id].message_id_hotel,
                          text="*" + get_hotel + "*", parse_mode='MARKDOWN',
                          disable_web_page_preview=True,
                          reply_markup=keyboard_bot)
    #bot.answer_callback_query(callback_query_id=call.id)


def photo_show(call, photo):

    bot.edit_message_media(chat_id=call.message.chat.id,
                           message_id=user[call.message.chat.id].message_id_photo,
                           media=types.InputMediaPhoto(get(photo).content))
    #bot.answer_callback_query(callback_query_id=call.id)


@bot.callback_query_handler(func=lambda call: True)
def inline(call):

    if call.data in ['yes_photo', 'no_photo']:
        user[call.message.chat.id].status_show_photo = (True if call.data == 'yes_photo' else False)
        if user[call.message.chat.id].status_show_photo:
            next_step_count_photo(call.message)
        else:
            next_step_show_info(call.message)

    elif call.data.startswith('cbcal_1'):
        result, key, step = MyStyleCalendar(calendar_id=1).process(call.data)
        if not result:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=user[call.message.chat.id].message_id_photo,
                                          reply_markup=key)
        elif result:
            if not user[call.message.chat.id].checkIn:
                user[call.message.chat.id].checkIn = result.strftime('%Y-%m-%d')
                next_step_date(call.message)

            else:
                user[call.message.chat.id].checkOut = result.strftime('%Y-%m-%d')
                if user[call.message.chat.id].checkOut > user[call.message.chat.id].checkIn:
                    user[call.message.chat.id].diff_date()
                    next_step_count_hotels(call.message)
                else:
                    bot.edit_message_text(text="Дата выезда должна быть больше даты заезда.Повторите ввод.",
                                          chat_id=call.message.chat.id,
                                          message_id=user[call.message.chat.id].message_id_photo,
                                          reply_markup=MyStyleCalendar(calendar_id=1,
                                                                       locale=user[call.message.chat.id].language).build()[0])

    elif call.data == "hotel_forward":

        if user[call.message.chat.id].hotels_act.getHotel_forward_triger():
            next_hotel_show(call)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Последняя гостиница')

    elif call.data == "hotel_backward":

        if user[call.message.chat.id].hotels_act.getHotel_backward_triger():
            next_hotel_show(call)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Первая гостиница')

    elif call.data == "photo_backward":  # фото назад
        if user[call.message.chat.id].hotels_act.photo_backward_triger:
            photo = user[call.message.chat.id].hotels_act.photo_backward()
            photo_show(call, photo)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Первое фото')

    elif call.data == "photo_forward":  # фото вперед
        if user[call.message.chat.id].hotels_act.photo_forward_triger:
            photo = user[call.message.chat.id].hotels_act.photo_forward()
            photo_show(call, photo)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Последнее фото')

    elif call.data in ["five", "ten", "fifteen", "twenty", "twenty_five"]:
        numbers_hotel = {"five": 5, "ten": 10, "fifteen": 15, "twenty": 20, "twenty_five": 25}
        user[call.message.chat.id].count_show_hotels = numbers_hotel[call.data]
        next_step_show_photo(call.message)

    elif call.data in ["one_photo", "two_photo", "three_photo", "four_photo", "five_photo"]:
        numbers_photo = {"one_photo": 1, "two_photo": 2, "three_photo": 3, "four_photo": 4, "five_photo": 5}
        user[call.message.chat.id].count_show_photo = numbers_photo[call.data]
        next_step_show_info(call.message)

    else:
        logging.info(call.message.chat.id, f'Команда {call.data} не обработана')