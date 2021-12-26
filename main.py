# -*- coding: utf-8 -*-

import re
from botrequests.request_api import hotel_query, get_city_id, \
    user, bot, logging
from telebot import util
from datetime import datetime
from botrequests.keyboards import types, Keyboard
from telegram_bot_calendar import WYearTelegramCalendar, DAY
from botrequests.user_class import Users
from botrequests.locales import loctxt, info_help, welcome


class MyStyleCalendar(WYearTelegramCalendar):
    """ Класс календаря с выбором дня месяца
    """
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"


def add_user(message) -> None:
    """Функция для добавления пользователя
    """
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
        logging.info(f"Добавление пользователя {message.from_user.id}")
    user[message.chat.id].clearCache()


@bot.message_handler(commands=["help", "start"])
def help_start_message(message: types.Message) -> None:
    """Функция для обработки команд "help", "start"
    """
    add_user(message)
    user[message.chat.id].command = message.text.lower()
    bot.send_message(chat_id=message.chat.id,
                     text='Выберите язык (Choose language)',
                     reply_markup=Keyboard().set_lang())
    logging.info(f"Пользователь {message.from_user.id} выбрал команду {message.text}")


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"])
def command_message(message: types.Message) -> None:
    """Функция для обработки команд "lowprice", "highprice", "bestdeal"
    """
    add_user(message)
    user[message.chat.id].command = message.text.lower()
    user[message.chat.id].language = (
        message.from_user.language_code + "_RU" if message.from_user.language_code == 'ru' else 'en_US')
    logging.info(f"Пользователь {message.from_user.id} выбрал команду {message.text}")
    m = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][2])
    bot.register_next_step_handler(m, ask_search_city)


@bot.message_handler(commands=["history"])
def history_message(message: types.Message) -> None:
    """Функция для обработки команды вывода истории
    """
    add_user(message)
    user[message.chat.id].language = (
        message.from_user.language_code + "_RU" if message.from_user.language_code == 'ru' else 'en_US')
    logging.info(f"Пользователь {message.from_user.id} запросил историю запросов")
    m = bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][11],
                         reply_markup=Keyboard().requests_numb(user[message.chat.id].language))
    user[message.chat.id].message_id = m.message_id


@bot.message_handler(content_types=['text'])
def get_text_messages(message: types.Message) -> None:
    """Функция слушает все входящие сообщения и если
    не знакомы выдает сообщения и строку помощи
    """
    add_user(message)
    logging.info(
        f"Неизвестная команда или текст {message.text} от пользователя {message.from_user.id}")
    user[message.chat.id].language = (
        "ru_RU" if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', message.text.lower())) else "en_US")
    bot.set_my_commands(commands=Keyboard().my_commands(user[message.chat.id].language),
                        scope=types.BotCommandScopeChat(message.chat.id))
    bot.send_message(text=loctxt[user[message.chat.id].language][25] + info_help[user[message.chat.id].language],
                     chat_id=message.from_user.id)


def ask_search_city(message: types.Message) -> None:
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
    bot.set_my_commands(commands=Keyboard().my_commands(user[message.chat.id].language),
                        scope=types.BotCommandScopeChat(message.chat.id))
    logging.info(f"Пользователю {message.from_user.id} изменен язык меню на {user[message.chat.id].language}")
    msg = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][0])
    user[message.chat.id].message_id = msg.message_id

    query_str = user[message.from_user.id].query_string('city')
    city = get_city_id(query_str)
    if city.get('city'):
        markup = types.InlineKeyboardMarkup()
        for id_city, i_city in city['city'].items():
            markup.add(types.InlineKeyboardButton(i_city, callback_data='cbid_' + str(id_city)))
        markup.add(
            types.InlineKeyboardButton(loctxt[user[message.chat.id].language][26], callback_data='Cancel_process'))
        logging.info(f"Пользователь {message.from_user.id} получил данные городов в чат")
        bot.edit_message_text(text=loctxt[user[message.chat.id].language][3], chat_id=message.chat.id,
                              message_id=user[message.chat.id].message_id,
                              parse_mode='HTML', reply_markup=markup)
    elif city.get('empty'):
        command = user[message.from_user.id].command
        user[message.chat.id].clearCache()
        user[message.chat.id].command = command
        bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][1])
        m = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][2])
        logging.info(
            f"Для пользователя {message.from_user.id} город {message.text} не найден. "
            f"Повторение ввода другого города")
        bot.register_next_step_handler(m, ask_search_city)
    else:
        logging.info(f"Пользователь {message.chat.id} получил сообщение {city['error']} от сервера")
        bot.send_message(message.chat.id, city['error'])


def ask_date(message: types.Message, txt: str) -> None:
    """Функция предлагает ввести дату
    :param message: сообщение от пользователя
    :patam txt: текст с предложением ввода даты
    """

    lng = user[message.chat.id].language
    logging.info(
        f"Бот {message.from_user.id} предлагает пользователю {message.chat.id} ввести {txt}")
    m = bot.edit_message_text(text=txt, chat_id=message.chat.id,
                              message_id=user[message.chat.id].message_id,
                              parse_mode='MARKDOWN',
                              reply_markup=MyStyleCalendar(calendar_id=1, locale=lng[:2]).build()[0])
    user[message.chat.id].message_id = m.message_id


def ask_count_hotels(message: types.Message) -> None:
    """Функция предлагает указать количество отелей, которые необходимо вывести
    :param message: входящее сообщение от пользователя
    """
    logging.info(f"Бот {message.from_user.id} предлагает пользователю  {message.chat.id} "
                 f"выбрать количество отелей")
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][6],
                          chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,

                          reply_markup=Keyboard().hotel_numb(user[message.chat.id].language))


def price_min_max(message: types.Message) -> None:
    """Функция предлагает ввести через пробел диапазон цен, если все введено корректно
    вызывает функцию distance_min_max
    :param message: входящее сообщение от пользователя
    """
    try:
        if len(message.text.split()) == 2 and message.text.split()[1].isdigit() and message.text.split()[0].isdigit():
            price_max, price_min = int(message.text.split()[1]), int(message.text.split()[0])
            logging.info(f"Пользователь {message.chat.id} ввел "
                         f"{message.text.split()[0]}-{message.text.split()[1]}")
        else:
            raise Exception

        if price_min > price_max:
            bot.send_message(text=loctxt[user[message.chat.id].language][24],
                             chat_id=message.chat.id)
            price_min, price_max = price_max, price_min
        user[message.chat.id].price_min = price_min
        user[message.chat.id].price_max = price_max

        m = bot.send_message(text=loctxt[user[message.chat.id].language][23],
                             chat_id=message.chat.id)
        logging.info(f"Бот {m.from_user.id} предлагает пользователю {m.chat.id} "
                     f"ввести через пробел диапазон расстояния до центра")
        bot.register_next_step_handler(m, distance_min_max)
    except Exception as er:
        logging.error(f"{er} - Функция price_min_max - Ошибка ввода мин- макс. цены")
        msg = bot.send_message(text=loctxt[user[message.chat.id].language][21],
                               chat_id=message.chat.id)
        bot.register_next_step_handler(msg, price_min_max)


def distance_min_max(message: types.Message) -> None:
    """Функция предлагает ввести через пробел диапазон расстояния до центра, если все введено корректно
    вызывает функцию send_hotels_chat вывода гостиниц в чат
    :param message: входящее сообщение от пользователя
    """

    try:
        if len(message.text.split()) == 2 and message.text.split()[1].isdigit() and message.text.split()[0].isdigit():
            user[message.chat.id].distance_max, user[message.chat.id].distance_min = float(message.text.split()[1]), \
                                                                                     float(message.text.split()[0])
            logging.info(f"Пользователь {message.chat.id} ввел "
                         f"{message.text.split()[0]}-{message.text.split()[1]}")
        else:
            raise Exception
        if user[message.chat.id].distance_min > user[message.chat.id].distance_max:
            bot.send_message(text=loctxt[user[message.chat.id].language][22],
                             chat_id=message.chat.id)
            user[message.chat.id].distance_max, user[message.chat.id].distance_min = user[message.chat.id].distance_min, \
                                                                                     user[message.chat.id].distance_max
        send_hotels_chat(message)

    except Exception as er:
        logging.error(f"{er} - Функция distance_min_max - Ошибка ввода мин- макс. расстояния")
        msg = bot.send_message(text=loctxt[user[message.chat.id].language][21],
                               chat_id=message.chat.id)
        bot.register_next_step_handler(msg, distance_min_max)


def ask_show_photo(message: types.Message):
    """Функция предлагает показ фотографии отелей
    :param message: входящее сообщение от пользователя
    """
    logging.info(
        f"Бот {message.from_user.id} предлагает пользователю  "
        f"{message.chat.id} показ фотографии отелей")
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][7], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=Keyboard().photo_yes_no(user[message.chat.id].language))


def ask_count_photo(message: types.Message) -> None:
    """
    Функция прелагает выбрать количество фото для загрузки
    :param message: объект входящего сообщения от пользователя
    """
    logging.info(f"Бот {message.from_user.id} предлагает пользователю {message.chat.id} выбрать "
                 f"количество фото для загрузки")
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][8], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=Keyboard().photo_numb(user[message.chat.id].language))


def step_show_info(message: types.Message) -> None:
    """
    Функция для вызова функции send_hotels_chat вывода информации в чат. В случае если выбрана команда /bestdeal
    вызывается функция price_min_max
    :param message: объект входящего сообщения от пользователя
    """
    command = user[message.chat.id].command
    bot.delete_message(chat_id=message.chat.id, message_id=user[message.chat.id].message_id)
    if command == '/bestdeal':
        logging.info(f"Бот {message.from_user.id} предлагает пользователю  {message.chat.id}"
                     f" ввести через пробел диапазон цен")
        bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][20])
        logging.info(f"Бот {message.from_user.id} вызвал функцию price_min_max")

        bot.register_next_step_handler(message, price_min_max)
    else:
        logging.info(f"Бот {message.from_user.id} вызвал функцию send_hotels_chat")
        send_hotels_chat(message)


def send_hotels_chat(message: types.Message):
    """Функция вывода в чат информации о отелях
    :param message: объект входящего сообщения от пользователя
    """
    logging.info(f"Вывод в чат информации о отелях - функция send_hotels_chat")
    bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][0])
    query_str = user[message.chat.id].query_string()
    data = hotel_query(query_str, user[message.chat.id].get_param())

    if not data.get("error"):
        for hotel, photo in data.items():
            if len(photo) > 0:
                links_photo = [types.InputMediaPhoto(media=link) for link in photo]
                try:
                    bot.send_media_group(chat_id=message.chat.id, media=links_photo)
                except Exception as er:
                    logging.error(f"{er} - Функция send_hotels_chat - Отправка фото")
            try:
                bot.send_message(chat_id=message.chat.id, text=hotel,
                                 disable_web_page_preview=True,
                                 parse_mode="HTML")
            except Exception as e:
                logging.error(f"{e} - Функция send_hotels_chat - Отправка гостиниц")
        logging.info(f"Пользователю {message.chat.id} отправлены в чат фото и отели")
        user[message.chat.id].insert_db(data, logging, datetime)
        logging.info(f"Сформированные для {message.chat.id} данные отправлены в базу")
        bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][13].format(len(data)))
    else:
        logging.error(f"Пользователь {message.chat.id} получил сообщение от сервера {data['error']}")
        bot.send_message(chat_id=message.chat.id, text=data["error"],
                         disable_web_page_preview=True,
                         parse_mode="HTML")


def history_req(message: types.Message, numb: int) -> None:
    """Функция выводит в чат историю запросов
    :param message: сообщение от пользователя
    :param numb: количество запросов, которые необходимо вывести в чат
    """
    history = user[message.chat.id].history(logging, numb)
    if len(history) == 0:
        txt = loctxt[user[message.chat.id].language][15]
        bot.edit_message_text(chat_id=message.chat.id, text=txt, message_id=user[message.chat.id].message_id)
    else:
        for elem in history:
            splitted_text = util.smart_split(elem[0], 3000)
            for txt in splitted_text:
                bot.send_message(chat_id=message.chat.id, text=txt,
                                 disable_web_page_preview=True, parse_mode="HTML")
        bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][18])


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    """Обработчик call инлайн клавиатуры
    """
    if call.data in ['yes_photo', 'no_photo']:
        user[call.message.chat.id].status_show_photo = (True if call.data == 'yes_photo' else False)

        if user[call.message.chat.id].status_show_photo:
            logging.info(f"Пользователь {call.message.chat.id} выбрал показ фото")
            bot.answer_callback_query(callback_query_id=call.id)
            ask_count_photo(call.message)

        else:
            logging.info(f"Пользователь {call.message.chat.id} отказался от показа фото")
            bot.answer_callback_query(callback_query_id=call.id)
            step_show_info(call.message)

    elif call.data.startswith('cbcal_1'):
        result, key, step = MyStyleCalendar(calendar_id=1, locale=user[call.message.chat.id].language[:2]).process(
            call.data)
        if not result:
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,
                                          message_id=user[call.message.chat.id].message_id,
                                          reply_markup=key)

        elif result:
            if not user[call.message.chat.id].checkIn:
                user[call.message.chat.id].checkIn = result.strftime('%Y-%m-%d')
                logging.info(f"Пользователь {call.message.chat.id} выбрал дату заезда "
                             f"{user[call.message.chat.id].checkIn}")
                bot.answer_callback_query(callback_query_id=call.id,
                                          text=loctxt[user[call.message.chat.id].language][9])
                ask_date(call.message, loctxt[user[call.message.chat.id].language][5])

            else:

                user[call.message.chat.id].checkOut = result.strftime('%Y-%m-%d')
                if user[call.message.chat.id].checkOut > user[call.message.chat.id].checkIn:
                    logging.info(f"Пользователь {call.message.chat.id} выбрал дату выезда "
                                 f"{user[call.message.chat.id].checkOut}")
                    ask_count_hotels(call.message)
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text=loctxt[user[call.message.chat.id].language][10])
                else:
                    logging.info(f"Пользователь {call.message.chat.id} ошибся при выборе даты")
                    bot.answer_callback_query(callback_query_id=call.id,
                                              text=loctxt[user[call.message.chat.id].language][12])

    elif call.data in ["five", "ten", "fifteen", "twenty", "twenty_five"]:
        numbers_hotel = {"five": 5, "ten": 10, "fifteen": 15, "twenty": 20, "twenty_five": 25}
        user[call.message.chat.id].count_show_hotels = numbers_hotel[call.data]
        logging.info(f"Пользователь {call.message.chat.id} выбрал "
                     f"{user[call.message.chat.id].count_show_hotels} отелей для загрузки")
        ask_show_photo(call.message)
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data in ["one_photo", "two_photo", "three_photo", "four_photo", "five_photo"]:
        numbers_photo = {"one_photo": 1, "two_photo": 2, "three_photo": 3, "four_photo": 4, "five_photo": 5}
        user[call.message.chat.id].count_show_photo = numbers_photo[call.data]
        logging.info(f"Пользователь {call.message.chat.id} выбрал "
                     f"{user[call.message.chat.id].count_show_photo} фото для загрузки")
        bot.answer_callback_query(callback_query_id=call.id)
        step_show_info(call.message)

    elif call.data in ["one_req", "two_req", "three_req", "four_req", "five_req"]:
        numbers_req = {"one_req": 1, "two_req": 2, "three_req": 3, "four_req": 4, "five_req": 5}
        bot.delete_message(chat_id=call.message.chat.id, message_id=user[call.message.chat.id].message_id)
        logging.info(f"Пользователь {call.message.chat.id} выбрал "
                     f"{numbers_req[call.data]} запросов для показа")

        bot.answer_callback_query(callback_query_id=call.id)
        history_req(call.message, numbers_req[call.data])

    elif call.data in ['ru_RU', 'en_US']:
        user[call.message.chat.id].language = call.data
        bot.set_my_commands(commands=Keyboard().my_commands(user[call.message.chat.id].language),
                            scope=types.BotCommandScopeChat(call.message.chat.id))
        logging.info(f"Пользователь {call.message.chat.id} сменил меню на {call.data}")
        user[call.message.chat.id].message_id = call.message.message_id
        bot.delete_message(chat_id=call.message.chat.id, message_id=user[call.message.chat.id].message_id)
        if user[call.message.chat.id].command in ['/start', '/help']:
            logging.info(f"Пользователь {call.message.chat.id} получил помощь")
            bot.send_message(
                text=welcome[user[call.message.chat.id].language] + info_help[user[call.message.chat.id].language],
                chat_id=call.message.chat.id)
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data.startswith('cbid_'):
        user[call.message.chat.id].id_city = call.data[5:]
        logging.info(f"Пользователь {call.message.chat.id} выбрал город c ID - {call.data[5:]}")
        user[call.message.chat.id].message_id = call.message.message_id
        ask_date(call.message, loctxt[user[call.message.chat.id].language][4])
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data == 'Cancel_process':
        logging.info(f"Пользователь {call.message.chat.id} отменил операцию")
        bot.edit_message_text(text=loctxt[user[call.message.chat.id].language][19], chat_id=call.message.chat.id,
                              message_id=user[call.message.chat.id].message_id)
        bot.answer_callback_query(callback_query_id=call.id)


if __name__ == '__main__':
    while True:
        try:
            logging.info("Бот запущен")
            bot.polling(none_stop=True, interval=0)
        except Exception as ex:
            logging.error(f"{ex} - Модуль main")
