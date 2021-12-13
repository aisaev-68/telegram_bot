# -*- coding: utf-8 -*-

from decouple import config
import logging
import re
from telebot import TeleBot, types
from requests_api import query_string
from search_city_id import get_city_id
from hotels_search import hotel_query
from telegram_bot_calendar import WYearTelegramCalendar, DAY

bot = TeleBot(config('TELEGRAM_API_TOKEN'))

logging.basicConfig(filename="logger.log", level=logging.INFO)

user = {}

info_help = {'ru_RU':
                 'Привет , я БОТ по поиску отелей. Подобрать для Вас отель? 🏨✅\n'
                 '● /help — помощь по командам бота\n● /lowprice — вывод самых дешёвых отелей в городе\n'
                 '● /highprice — вывод самых дорогих отелей в городе\n'
                 '● /bestdeal — вывод отелей, наиболее подходящих по цене и расположению от центра\n'
                 '● /history - вывод истории поиска отелей',
             'en_US':
                 "Hi, I'm a hotel search BOT. Find a hotel for you? 🏨✅\n"
                 '● /help — help with bot commands\n● /lowprice — listing of the cheapest hotels in the city\n'
                 '● /highprice — conclusion of the most expensive hotels in the city\n'
                 '● /bestdeal — conclusion of hotels that are most suitable in terms of price and location '
                 'from the center\n'
                 '● /history - hotel search history display'
             }


loctxt = {'ru_RU':
              ['Ищем...', 'Такой город не найден. Повторите поиск.', 'В каком городе будем искать?',
               'Выберите дату *заезда*:', 'Выберите дату *выезда*:',
               'Укажите количество отелей, которые необходимо вывести (не более 25).',
               'Показать фотографии отелей?', 'Выберите количество фото для загрузки:',
               'Дата заезда выбрана.', 'Дата выезда выбрана.',
               'Дата выезда должна быть больше даты въезда.Повторите ввод.', 'История запросов:\n',
               'Ваша история пуста.',
               'Команда:', 'Дата запросов:', 'Команда выполнена.', 'Вы отменили данную операцию'
               ],
          'en_US':
              ['Are looking for...', 'No such city has been found. Repeat the search.',
               ' In which city are we looking?',
               'Select *check-in date*:', 'Select *check-out date*:',
               'Specify the number of hotels to be displayed (no more than 25).',
               'Show photos of hotels?', 'Select the number of photos to upload:',
               ' Check-in date selected. ', ' Check-out date selected.',
               'The check-out date must be greater than the check-in date. Please re-enter.',
               'Request history:\n', 'Your story is empty.', 'Command:', 'Date of requests:',
               'Command completed.', 'You canceled this operation'
               ]
          }


class MyStyleCalendar(WYearTelegramCalendar):
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"


def check_city(mess):
    """
        Функция проверки на корректность ввода названия города. re.findall(r'^[а-яА-ЯёЁa-zA-Z-\s]+$', txt)
    """
    if len(re.findall(r'^[a-zA-Z]+(?:[\s-][a-zA-Z]+)*$', mess.text)) == 0:
        # err_city = bot.send_message(mess.chat.id,
        #                             'Город должен содержать только буквы, пробел и дефис, вводи еще раз город.')
        # user[mess.chat.id].message_id = err_city.message_id
        m = bot.send_message(chat_id=mess.from_user.id,
                             text=loctxt[user[mess.chat.id].language][3])
        user[mess.chat.id].message_id = m.message_id
        # bot.register_next_step_handler(m, next_step_city)
        # await next_step_city(m)
    else:
        return True


def ask_search_city(message):
    """
    Функция готовит данные для запроса городов и вызывает функцию get_city_id()
    для вывода в чат городов
    :param message: сообщение
    """

    user[message.from_user.id].message_id = message.message_id
    user[message.chat.id].search_city = message.text.lower()
    user[message.chat.id].language = (
        "ru_RU" if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', message.text.lower())) else "en_US")
    user[message.chat.id].currency = ('RUB' if user[message.chat.id].language == 'ru_RU' else 'USD')
    bot.set_my_commands(user[message.chat.id].my_commands)
    msg = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][0])
    user[message.chat.id].message_id = msg.message_id
    if not get_city_id(user, message, bot):
        command = user[message.chat.id].command
        user[message.chat.id].clearCache()
        user[message.chat.id].command = command
        bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][1])
        m = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][2])
        bot.register_next_step_handler(m, ask_search_city)


def ask_date(message, txt):
    lng = user[message.chat.id].language
    bot.edit_message_text(text=txt, chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          parse_mode='MARKDOWN',
                          reply_markup=MyStyleCalendar(calendar_id=1,
                                                       locale=lng[:2]).build()[0])


def ask_count_hotels(message):
    """Функция предлагает указать количество отелей, которые необходимо вывести
    :param message: входящее сообщение от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][5],
                          chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=user[message.chat.id].getHotel_kbd())


def ask_show_photo(message):
    """Функция предлагает показ фотографии отелей
    :param message: входящее сообщение от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][6], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=user[message.chat.id].getPhoto_yes_no())


def ask_count_photo(message):
    """
    Функция прелагает выбрать количество фото для загрузки
    :param mess: объект входящего сообщения от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][7], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=user[message.chat.id].getKbd_photo_numb())


def step_show_info(message):
    """
    Функция для вывода информации в чат
    :param mess: объект входящего сообщения от пользователя
    """
    bot.delete_message(chat_id=message.chat.id, message_id=user[message.chat.id].message_id)
    querystring = query_string(user[message.chat.id].command, user[message.chat.id].getSource_dict())
    user[message.chat.id].all_hotels = hotel_query(querystring, user[message.chat.id].getSource_dict(),
                                                   bot, message, user)


def history(message):
    if user[message.chat.id].language == '':
        user[message.chat.id].language = (
            message.from_user.language_code + "_RU" if not user[message.chat.id].language else user[
                message.chat.id].language)
    bot.set_my_commands(user[message.chat.id].my_commands)
    history = user[message.chat.id].history()
    txt = loctxt[user[message.chat.id].language][11]
    if len(history) == 0:
        txt += loctxt[user[message.chat.id].language][12]
        bot.send_message(chat_id=message.chat.id, text=txt)
    else:
        for elem in history:
            txt += f'{loctxt[user[message.chat.id].language][13]} {elem[0]}\n' \
                   f'{loctxt[user[message.chat.id].language][14]} {elem[1]}\n{elem[2]}\n'
            bot.send_message(chat_id=message.chat.id, text=txt, disable_web_page_preview=True, parse_mode="HTML")
            txt = ''

    bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][15])


@bot.callback_query_handler(func=lambda call: True)
def inline(call):

    if call.data in ['yes_photo', 'no_photo']:
        user[call.message.chat.id].status_show_photo = (True if call.data == 'yes_photo' else False)
        if user[call.message.chat.id].status_show_photo:
            ask_count_photo(call.message)
        else:
            step_show_info(call.message)

    elif call.data.startswith('cbcal_1'):
        result, key, step = MyStyleCalendar(calendar_id=1).process(call.data)
        if not result:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=user[call.message.chat.id].message_id,
                                          reply_markup=key)
        elif result:
            if not user[call.message.chat.id].checkIn:
                user[call.message.chat.id].checkIn = result.strftime('%Y-%m-%d')
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=loctxt[user[call.message.chat.id].language][8])
                ask_date(call.message, loctxt[user[call.message.chat.id].language][4])

            else:
                user[call.message.chat.id].checkOut = result.strftime('%Y-%m-%d')
                if user[call.message.chat.id].checkOut > user[call.message.chat.id].checkIn:
                    ask_count_hotels(call.message)
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text=loctxt[user[call.message.chat.id].language][9])
                else:
                    ask_date(call.message, loctxt[user[call.message.chat.id].language][10])

    elif call.data in ["five", "ten", "fifteen", "twenty", "twenty_five"]:
        numbers_hotel = {"five": 5, "ten": 10, "fifteen": 15, "twenty": 20, "twenty_five": 25}
        user[call.message.chat.id].count_show_hotels = numbers_hotel[call.data]
        bot.answer_callback_query(callback_query_id=call.id)
        ask_show_photo(call.message)

    elif call.data in ["one_photo", "two_photo", "three_photo", "four_photo", "five_photo"]:
        numbers_photo = {"one_photo": 1, "two_photo": 2, "three_photo": 3, "four_photo": 4, "five_photo": 5}
        user[call.message.chat.id].count_show_photo = numbers_photo[call.data]
        bot.answer_callback_query(callback_query_id=call.id)
        step_show_info(call.message)

    elif call.data in ['ru_RU', 'en_US']:
        user[call.message.chat.id].language = call.data
        bot.set_my_commands(user[call.message.chat.id].my_commands)
        user[call.message.chat.id].message_id = call.message.message_id
        bot.delete_message(chat_id=call.message.chat.id, message_id=user[call.message.chat.id].message_id)
        bot.answer_callback_query(callback_query_id=call.id)
        if user[call.message.chat.id].command in ['start', 'help']:
            bot.send_message(text=info_help[user[call.message.chat.id].language], chat_id=call.message.from_user.id)

    elif call.data.startswith('cbid_'):
        user[call.message.chat.id].id_city = call.data[5:]
        user[call.message.chat.id].message_id = call.message.message_id
        ask_date(call.message, loctxt[user[call.message.chat.id].language][3])
    elif call.data == 'Cancel_process':
        bot.edit_message_text(text=loctxt[user[call.message.chat.id].language][16], chat_id=call.message.chat.id,
                              message_id=user[call.message.chat.id].message_id)
        bot.answer_callback_query(callback_query_id=call.id)

    else:
        bot.answer_callback_query(callback_query_id=call.id)
