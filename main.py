## -*- coding: utf-8 -*-

from decouple import config
import re
import json
from telebot import TeleBot, util
from keyboards import types, Keyboard
import requests
from telegram_bot_calendar import WYearTelegramCalendar, DAY
from datetime import datetime
import logging
from typing import Any
from botrequests.parse_text import city_parse, price_parse
from botrequests.user_class import Users
from botrequests.locales import l_text, loctxt, info_help, loc_txt, \
    server_error, loc

bot = TeleBot(config('TELEGRAM_API_TOKEN'))

logging.basicConfig(filename="logger.log", level=logging.INFO)

user: dict = {}


class MyStyleCalendar(WYearTelegramCalendar):
    """ Класс календаря с выбором дня месяца
    """
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"


@bot.message_handler(commands=["help", "start"])
def help_start_message(message: types.Message) -> None:
    """Функция для обработки команд "help", "start"
    """
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    user[message.chat.id].command = message.text.lower()
    bot.send_message(chat_id=message.chat.id,
                     text='Выберите язык (Choose language)',
                     reply_markup=Keyboard().set_lang())


@bot.message_handler(commands=["lowprice", "highprice", "bestdeal"])
def command_message(message: types.Message) -> None:
    """Функция для обработки команд "lowprice", "highprice", "bestdeal"
    """
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


@bot.message_handler(commands=["history"])
def history_message(message: types.Message) -> None:
    """Функция для обработки команды вывода истории
    """
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
def get_text_messages(message: types.Message) -> None:
    """Функция слушает все входящие сообщения и если
    не знакомы выдает сообщения и строку помощи
    """
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].language = (
        "ru_RU" if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', message.text.lower())) else "en_US")
    bot.send_message(text=l_text[user[message.chat.id].language][2] + info_help[user[message.chat.id].language],
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
    msg = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][0])
    user[message.from_user.id].message_id = msg.message_id

    query_str = user[message.from_user.id].query_string('city')
    if not get_city_id(query_str, message):
        command = user[message.from_user.id].command
        user[message.chat.id].clearCache()
        user[message.chat.id].command = command
        bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][1])
        m = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][2])
        bot.register_next_step_handler(m, ask_search_city)


def ask_date(message: types.Message, txt: str) -> None:
    """Функция предлагает ввести дату
    """
    lng = user[message.chat.id].language
    bot.edit_message_text(text=txt, chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          parse_mode='MARKDOWN',
                          reply_markup=MyStyleCalendar(calendar_id=1,
                                                       locale=lng[:2]).build()[0])


def ask_count_hotels(message: types.Message) -> None:
    """Функция предлагает указать количество отелей, которые необходимо вывести
    :param message: входящее сообщение от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][5],
                          chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,

                          reply_markup=Keyboard().hotel_numb(user[message.chat.id].language))


def price_min_max(message: types.Message) -> None:
    """Функция предлагает ввести через пробел диапазон диапазон цен, если все введено корректно
    вызывает функцию distance_min_max
    :param message: входящее сообщение от пользователя
    """
    try:
        price_max, price_min = int(message.text.split()[1]), int(message.text.split()[0])
        if price_min > price_max:
            bot.send_message(text=loctxt[user[message.chat.id].language][21],
                             chat_id=message.chat.id)
            price_min, price_max = price_max, price_min
        user[message.chat.id].price_min = price_min
        user[message.chat.id].price_max = price_max
        m = bot.send_message(text=loctxt[user[message.chat.id].language][20],
                             chat_id=message.chat.id)
        bot.register_next_step_handler(m, distance_min_max)
    except Exception as er:
        logging.error(f"{datetime.now()} - {er} - Функция price_min_max - Ошибка ввода мин- макс. цены")
        msg = bot.send_message(text=loctxt[user[message.chat.id].language][18],
                               chat_id=message.chat.id)
        bot.register_next_step_handler(msg, price_min_max)


def distance_min_max(message: types.Message) -> None:
    """Функция предлагает ввести через пробел диапазон расстояния до центра, если все введено корректно
    вызывает функцию hotel_query вывода гостиниц в чат
    :param message: входящее сообщение от пользователя
    """

    try:

        user[message.chat.id].distance_max, user[message.chat.id].distance_min = float(message.text.split()[1]), \
                                                                                 float(message.text.split()[0])
        if user[message.chat.id].distance_min > user[message.chat.id].distance_max:
            bot.send_message(text=loctxt[user[message.chat.id].language][19],
                             chat_id=message.chat.id)
            user[message.chat.id].distance_max, user[message.chat.id].distance_min = user[message.chat.id].distance_min, \
                                                                                     user[message.chat.id].distance_max
        # bot.delete_message(chat_id=message.chat.id, message_id=user[message.chat.id].message_id)

    except Exception as er:
        logging.error(f"{datetime.now()} - {er} - Функция distance_min_max - Ошибка ввода мин- макс. расстояния")
        msg = bot.send_message(text=loctxt[user[message.chat.id].language][18],
                               chat_id=message.chat.id)
        bot.register_next_step_handler(msg, distance_min_max)
    bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][0])
    query_str = user[message.chat.id].query_string()
    hotel_query(query_str, message)


def ask_show_photo(message: types.Message):
    """Функция предлагает показ фотографии отелей
    :param message: входящее сообщение от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][6], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=Keyboard().photo_yes_no(user[message.chat.id].language))


def ask_count_photo(message: types.Message) -> None:
    """
    Функция прелагает выбрать количество фото для загрузки
    :param message: объект входящего сообщения от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][7], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=Keyboard().photo_numb(user[message.chat.id].language))


def step_show_info(message: types.Message) -> None:
    """
    Функция для вызова функции hotel_query вывода информации в чат. В случае если выбрана команда /bestdeal
    вызывается функция price_min_max
    :param message: объект входящего сообщения от пользователя
    """
    command = user[message.chat.id].command
    bot.delete_message(chat_id=message.chat.id, message_id=user[message.chat.id].message_id)
    if command == '/bestdeal':
        bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][17])

        bot.register_next_step_handler(message, price_min_max)
    else:
        query_str = user[message.chat.id].query_string()
        hotel_query(query_str, message)


def history(message: types.Message) -> None:
    """
    Функция вывода трех последних запросов в чат.
    :param message: объект входящего сообщения от пользователя
    """
    if user[message.chat.id].language == '':
        user[message.chat.id].language = (
            message.from_user.language_code + "_RU" if not user[message.chat.id].language else user[
                message.chat.id].language)
    bot.set_my_commands(commands=Keyboard().my_commands(user[message.chat.id].language),
                        scope=types.BotCommandScopeChat(message.chat.id))
    history = user[message.chat.id].history(logging, datetime)
    if len(history) == 0:
        txt = loctxt[user[message.chat.id].language][12]
        bot.send_message(chat_id=message.chat.id, text=txt)
    else:
        for elem in history:
            splitted_text = util.split_string(elem, 3000)
            for txt in splitted_text:
                bot.send_message(chat_id=message.chat.id, text=txt, disable_web_page_preview=True, parse_mode="HTML")

    bot.send_message(chat_id=message.chat.id, text=loctxt[user[message.chat.id].language][15])


def req_api(url: str, querystring: dict, lng="en_US") -> Any:
    """
    Функция возвращает данные запроса к API гостиниц.
    :param url: страница поиска
    :param querystring: срока запроса
    :param lng: язык пользователя
    :return data: возвращаемые API данные
    """

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': config('RAPID_API_KEY')
    }
    try:
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            if json.loads(response.text).get("message"):
                logging.error(
                    f"{datetime.now()} - Функция req_api - Превышена ежемесячная квота для запросов по плану BASIC.")
                return json.loads(response.text)
            else:
                logging.error(f"{datetime.now()} - Функция req_api - Что-то пошло не так. Повторите позже.")
                return server_error[lng]["erhttp"]
    except ConnectionError as ercon:
        logging.error(f"{datetime.now()} - {ercon} - Функция req_api - Нет, соединения с сервисом.")
        return server_error[lng]["ercon"]
    except TimeoutError as ertime:
        logging.error(f"{datetime.now()} - {ertime} - Функция req_api - Время ожидания запроса истекло")
        return server_error[lng]["ertime"]
    except json.decoder.JSONDecodeError as erjson:
        logging.error(
            f"{datetime.now()} - {erjson} - Функция req_api - Получен некорректный ответ от сервиса.")
        return server_error[lng]["erjson"]


def get_photos(id_photo: str) -> list:
    """
    Функция возвращает список ссылок на фотографии отеля. Если не найдены, возвращает пустой список.
    :param id_photo: ID отеля
    :return photo_list: список ссылок на фотографии отеля
    """

    url = config('URL_PHOTOS')
    querystring = {"id": f"{id_photo}"}
    response = req_api(url, querystring)
    photo_list = []
    for photo in response["roomImages"]:
        for img in photo['images']:
            photo_list.append(img['baseUrl'].replace('{size}', 'z'))
    return photo_list


def get_city_id(querystring: dict, message: types.Message) -> bool:
    """
    Функция выводит в чат города.
    :param querystring: строка запроса в виде словаря {'query': 'минск', 'locale': 'ru_RU'}
    :param message: сообщение
    """
    lang = user[message.chat.id].language
    l_txt = loc[lang]
    # search_city = querystring["query"]
    result_id_city = req_api(config('URL'), querystring, lang)

    if isinstance(result_id_city, dict) and not result_id_city.get("message"):
        if len(result_id_city) > 0:
            markup = types.InlineKeyboardMarkup()
            for city in result_id_city['suggestions']:
                if city['group'] == 'CITY_GROUP':
                    for name in city['entities']:
                        parse_city = city_parse(name['caption']).title()
                        markup.add(types.InlineKeyboardButton(parse_city,
                                                              callback_data='cbid_' + str(name['destinationId'])))
            markup.add(types.InlineKeyboardButton(l_txt[0],
                                                  callback_data='Cancel_process'))
            bot.edit_message_text(text=l_txt[1], chat_id=message.chat.id,
                                  message_id=user[message.chat.id].message_id,
                                  parse_mode='HTML', reply_markup=markup)
            return True
        else:
            return False
    elif result_id_city.get("message"):
        bot.edit_message_text(text=l_txt[2],
                              chat_id=message.chat.id, message_id=user[message.chat.id].message_id)
        return True

    else:
        bot.send_message(message.chat.id, result_id_city)
        return True


def hotel_query(querystring: dict, message: types.Message):
    """
    Формирует словарь отелей на основе запроса пользователя и сортировкой по цене.
    Если отелей не найдено возвращает пустой словарь.
    :param querystring: строка запроса в виде словаря
    :param message: сообщение
    :return result_low: возвращает словарь (название отеля, адрес,
    фотографии отеля (если пользователь счёл необходимым их вывод)
    """

    url_low = config('URL_LOW')
    loc = querystring["locale"]
    data = req_api(url_low, querystring, loc)
    links_htmls = ("https://ru.hotels.com/ho{}" if loc[:2] == "ru"
                   else "https://hotels.com/ho{}?pos=HCOM_US&locale=en_US")

    if data:
        if user[message.chat.id].command == '/bestdeal':
            if user[message.chat.id].language == 'ru_RU':
                low_data = [d for d in data['data']['body']['searchResults']['results']
                            if user[message.chat.id].distance_min <= float(
                        d['landmarks'][0]['distance'].split()[0].replace(',', '.')) <= user[
                                message.chat.id].distance_max]
            else:
                low_data = [d for d in data['data']['body']['searchResults']['results']
                            if user[message.chat.id].distance_min <= float(
                        d['landmarks'][0]['distance'].split()[0]) <= user[message.chat.id].distance_max]
        else:
            low_data = [d for d in data['data']['body']['searchResults']['results']]
        for hotel_count, results in enumerate(low_data):
            price = price_parse(results["ratePlan"], user[message.chat.id].language, logging, datetime)
            if querystring["pageSize"] != hotel_count:
                txt = f"<strong>⭐⭐⭐{loc_txt[loc][0]} {(results.get('starRating')) if results.get('starRating') else '--'}⭐⭐⭐</strong>\n" \
                      f"🏨 {loc_txt[loc][1]} {results['name']}\n" \
                      f"       {loc_txt[loc][2]} {results['address'].get('countryName')}, {results['address'].get('locality')}, " \
                      f"{(results['address'].get('streetAddress') if results['address'].get('streetAddress') else loc_txt[loc][10])}\n" \
                      f"🚗 {loc_txt[loc][3]} {results['landmarks'][0]['distance']}\n" \
                      f"📅 {loc_txt[loc][4]} {querystring['checkIn']} - {querystring['checkOut']}\n" \
                      f"💵 {loc_txt[loc][5]} <b>{price['price_day']}</b>\n" \
                      f"💵 {loc_txt[loc][6].format(price['day'])} <b>{price['price_total']}</b>\n" \
                      f"🌍 {loc_txt[loc][7]} {links_htmls.format(results['id'])}\n\n"

                if user[message.chat.id].status_show_photo:
                    data_photo = get_photos(results['id'])

                    photo_lst = [types.InputMediaPhoto(media=link) for index, link in enumerate(data_photo) if
                                 user[message.chat.id].count_show_photo > index]
                    try:
                        bot.send_media_group(chat_id=message.chat.id, media=photo_lst)
                    except Exception as er:
                        logging.error(f"{datetime.now()} - {er} - Функция hotel_query - Отправка фото")

                    user[message.chat.id].all_hotels[txt] = photo_lst
                    photo_lst.clear()
                else:
                    user[message.chat.id].all_hotels[txt] = []
                try:
                    bot.send_message(chat_id=message.chat.id, text=txt,
                                     disable_web_page_preview=True,
                                     parse_mode="HTML")

                except Exception as e:
                    logging.error(f"{datetime.now()} - {e} - Функция hotel_query - Отправка гостиниц")
                txt = ''
        user[message.chat.id].insert_db(logging, datetime)
        bot.send_message(chat_id=message.chat.id, text=loc_txt[loc][8].format(len(user[message.chat.id].all_hotels)))
        with open('hotel.json', 'w') as f:
            json.dump(user[message.chat.id].all_hotels, f, indent=4)
    else:
        bot.send_message(chat_id=message.chat.id, text=data,
                         disable_web_page_preview=True,
                         parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    """Обработчик call инлайн клавиатуры
    """
    if call.data in ['yes_photo', 'no_photo']:
        user[call.message.chat.id].status_show_photo = (True if call.data == 'yes_photo' else False)

        if user[call.message.chat.id].status_show_photo:
            bot.answer_callback_query(callback_query_id=call.id)
            ask_count_photo(call.message)

        else:
            bot.send_message(call.message.chat.id, loctxt[user[call.message.chat.id].language][0])
            bot.answer_callback_query(callback_query_id=call.id)
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
        ask_show_photo(call.message)
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data in ["one_photo", "two_photo", "three_photo", "four_photo", "five_photo"]:
        numbers_photo = {"one_photo": 1, "two_photo": 2, "three_photo": 3, "four_photo": 4, "five_photo": 5}
        user[call.message.chat.id].count_show_photo = numbers_photo[call.data]
        bot.answer_callback_query(callback_query_id=call.id)
        step_show_info(call.message)

    elif call.data in ['ru_RU', 'en_US']:
        user[call.message.chat.id].language = call.data
        bot.set_my_commands(commands=Keyboard().my_commands(user[call.message.chat.id].language),
                            scope=types.BotCommandScopeChat(call.message.chat.id))
        user[call.message.chat.id].message_id = call.message.message_id
        bot.delete_message(chat_id=call.message.chat.id, message_id=user[call.message.chat.id].message_id)
        if user[call.message.chat.id].command in ['/start', '/help']:
            bot.send_message(text=info_help[user[call.message.chat.id].language], chat_id=call.message.chat.id)
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data.startswith('cbid_'):
        user[call.message.chat.id].id_city = call.data[5:]
        user[call.message.chat.id].message_id = call.message.message_id
        ask_date(call.message, loctxt[user[call.message.chat.id].language][3])
        bot.answer_callback_query(callback_query_id=call.id)

    elif call.data == 'Cancel_process':
        bot.edit_message_text(text=loctxt[user[call.message.chat.id].language][16], chat_id=call.message.chat.id,
                              message_id=user[call.message.chat.id].message_id)
        bot.answer_callback_query(callback_query_id=call.id)


if __name__ == '__main__':
    while True:
        try:
            logging.error(f"{datetime.now()} - Бот запущен")
            bot.polling(none_stop=True, interval=0)
        except Exception as ex:
            logging.error(f"{datetime.now()} - {ex} - Модуль main")
