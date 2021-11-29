# -*- coding: utf-8 -*-

from requests import get
import re
from myclass import MyStyleCalendar

from decouple import config
from telebot import TeleBot, types
import logging

logging.basicConfig(filename="logger.log", level=logging.INFO)


bot = TeleBot(config('TELEGRAM_API_TOKEN'))

user = {}

loc_dict1 = {'ru_RU': ['Выберите дату заезда:', 'Выберите дату выезда:', 'Будут выведены 25 отелей:',
                       'Показать фотографии отелей?',
                       'Укажите количество отелей, которые необходимо вывести (не более 25):',
                       'Количество фотографий, которые необходимо вывести в результате (не более 5)?',
                       'Дата выезда должна быть больше даты въезда.Повторите ввод.',
                       'Город должен содержать только буквы, повторите ввод.',
                       'Такой город не найден. Повторите поиск.', 'В каком городе будем искать?',
                       'Количество должно состоять из цифр, повторите ввод'
                       ],
             'en_US': ['Select check-in date:', 'Select check-out date:', '25 hotels will be displayed:',
                       'Show photos of hotels?', 'Specify the number of hotels to be displayed (no more than 25):',
                       'The number of photos to be displayed as a result (no more than 5)?',
                       'The check-out date must be greater than the check-in date. Please re-enter.',
                       'The city must only contain letters, please re-enter.',
                       'No such city has been found. Repeat the search.', ' In which city are we looking? ',
                       'The number must consist of numbers, please re-enter'
                       ]
             }


def next_step_city(mess):
    """
    Функция проверки на корректность ввода названия города.
    В случае корректного ввода города прелагает ввести дату въезда в гостиницу.
    :param mess: объект входящего сообщения от пользователя
    """

    if len(re.findall(r'[А-Яа-яЁёa-zA-Z0-9 -]+', mess.text)) > 1:
        err_city = bot.send_message(mess.chat.id,
                                    'Город должен содержать только буквы, повторите ввод.')
        bot.register_next_step_handler(err_city, next_step_city)
    else:
        user[mess.chat.id].search_city = mess.text
        user[mess.chat.id].language = (
            "ru_RU" if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', mess.text)) else "en_US")
        user[mess.chat.id].currency = ('RUB' if user[mess.chat.id].language == 'ru_RU' else 'USD')
        idcity = user[mess.chat.id].get_city_id()

        if idcity is not None:
            user[mess.chat.id].id_city = idcity
            loc = user[mess.chat.id].language[:2]
            msg = bot.send_message(chat_id=mess.chat.id, text="Выберите дату *заезда*",
                                   parse_mode='MARKDOWN',
                                   reply_markup=MyStyleCalendar(calendar_id=1, locale=loc).build()[0])
            user[mess.chat.id].message_id_photo = msg.message_id

        else:
            bot.send_message(mess.chat.id, "Такой город не найден. Повторите поиск.")
            msg = bot.send_message(mess.chat.id, 'В каком городе будем искать?')
            bot.register_next_step_handler(msg, next_step_city)


def next_step_date(m):
    loc = user[m.chat.id].language[:2]
    bot.edit_message_text(text="Выберите дату *выезда*", chat_id=m.chat.id,
                          message_id=user[m.chat.id].message_id_photo,
                          parse_mode='MARKDOWN',
                          disable_web_page_preview=True,
                          reply_markup=MyStyleCalendar(calendar_id=1, locale=loc).build()[0])

def next_step_count_hotels(message):
    #time.sleep(1)
    bot.edit_message_text(text="Укажите количество отелей, которые необходимо вывести (не более 25)",
                          chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id_photo,
                          reply_markup=user[message.chat.id].getHotel_kbd())


def next_step_show_photo(message):

    bot.edit_message_text(text="Показать фотографии отелей?", chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id_photo,
                          reply_markup=user[message.chat.id].getPhoto_yes_no())


def next_step_count_photo(mess):
    """
    Функция проверки на корректность ввода количества отелей в городе.
    В случае положительного ответа, вызываем функцию 'range_request_price'.
    :param mess: объект входящего сообщения от пользователя
    """
    bot.edit_message_text(text="Выберите количество фото для загрузки", chat_id=mess.chat.id,
                          message_id=user[mess.chat.id].message_id_photo,
                          reply_markup=user[mess.chat.id].getKbd_photo_numb())


def next_step_show_info(mess):
    """
    Функция проверки на корректность ввода количества отображаемых изображений с отелями.
    :param mess: объект входящего сообщения от пользователя
    """
    print(user[mess.chat.id])
    bot.delete_message(chat_id=mess.chat.id, message_id=user[mess.chat.id].message_id_photo)
    querystring = user[mess.chat.id].queryAPI(user[mess.chat.id].command)
    user[mess.chat.id].low_price(querystring)
    get_hotel = user[mess.chat.id].hotel_forward()
    if user[mess.chat.id].status_show_photo:
        get_photo = user[mess.chat.id].photo_forward()
        mes_id_photo = bot.send_photo(mess.chat.id, get(get_photo).content)
        user[mess.chat.id].message_id_photo = mes_id_photo.message_id
        keyword_bot = user[mess.chat.id].getShow_kbd()
    else:
        keyword_bot = user[mess.chat.id].getShowNoPhoto_kbd()

    meshotel = bot.send_message(chat_id=mess.chat.id, text="*" + get_hotel + "*",
                                parse_mode='MARKDOWN',
                                disable_web_page_preview=True,
                                reply_markup=keyword_bot)
    user[mess.chat.id].message_id_hotel = meshotel.message_id


def next_hotel_show(call):
    get_hotel = user[call.message.chat.id].hotel_forward()
    if user[call.message.chat.id].status_show_photo:
        keyword_bot = user[call.message.chat.id].getShow_kbd()
        photo = user[call.message.chat.id].photo_forward()
        bot.edit_message_media(chat_id=call.message.chat.id,
                               message_id=user[call.message.chat.id].message_id_photo,
                               media=types.InputMediaPhoto(get(photo).content))
    else:
        keyword_bot = user[call.message.chat.id].getShowNoPhoto_kbd()

    bot.edit_message_text(chat_id=call.message.chat.id,
                          message_id=user[call.message.chat.id].message_id_hotel,
                          text="*" + get_hotel + "*", parse_mode='MARKDOWN',
                          disable_web_page_preview=True,
                          reply_markup=keyword_bot)
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
        if result:
            if not user[call.message.chat.id].checkIn:
                user[call.message.chat.id].checkIn = result.strftime('%Y-%m-%d')
                next_step_date(call.message)

            else:
                user[call.message.chat.id].checkOut = result.strftime('%Y-%m-%d')
                if user[call.message.chat.id].checkOut > user[call.message.chat.id].checkIn:
                    user[call.message.chat.id].diff_date()
                    next_step_count_hotels(call.message)
                else:
                    bot.send_message(call.message.chat.id,
                                     "Дата выезда должна быть больше даты въезда.Повторите ввод.",
                                     reply_markup=MyStyleCalendar(calendar_id=1).build()[0])

    elif call.data == "hotel_forward":

        if user[call.message.chat.id].getHotel_forward_triger():
            next_hotel_show(call)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Последняя гостиница')

    elif call.data == "hotel_backward":

        if user[call.message.chat.id].getHotel_backward_triger():
            next_hotel_show(call)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Первая гостиница')

    elif call.data == "photo_backward":  # фото назад
        if user[call.message.chat.id].photo_backward_triger:
            photo = user[call.message.chat.id].photo_backward()
            photo_show(call, photo)
            bot.answer_callback_query(callback_query_id=call.id)
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Первое фото')

    elif call.data == "photo_forward":  # фото вперед
        if user[call.message.chat.id].photo_forward_triger:
            photo = user[call.message.chat.id].photo_forward()
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
