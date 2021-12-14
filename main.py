# -*- coding: utf-8 -*-
from decouple import config
import re
import json
from telebot import TeleBot, types
import requests
from bs4 import BeautifulSoup
from telegram_bot_calendar import WYearTelegramCalendar, DAY
import datetime
import logging
from typing import Any
from botrequests.user_class import Users
from botrequests.locales import l_text, loctxt, info_help, loc_txt, commands, \
    server_error, loc, hotel_kbd, commands_bot

bot = TeleBot(config('TELEGRAM_API_TOKEN'))

logging.basicConfig(filename="logger.log", level=logging.INFO)

user = {}


class Keyboard:
    """ Класс инлайн кнопок
    """

    def __init__(self):
        self.__markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

    def set_lang(self):
        """ Функция инлайн кнопок с выбора языка?
        """
        self.__markup.add(types.InlineKeyboardButton(text='✅Russian', callback_data='ru_RU'),
                          types.InlineKeyboardButton(text='✅English', callback_data='en_US'))
        return self.__markup

    def hotel_numb(self) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок для выводы количества гостиниц
        """
        self.__markup.row_width = 5
        self.__markup.add(types.InlineKeyboardButton(text='5', callback_data='five'),
                          types.InlineKeyboardButton(text='10', callback_data='ten'),
                          types.InlineKeyboardButton(text='15', callback_data='fifteen'),
                          types.InlineKeyboardButton(text='20', callback_data='twenty'),
                          types.InlineKeyboardButton(text='25', callback_data='twenty_five'))
        return self.__markup

    def photo_yes_no(self, loc) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок с вопросом будем ли искать фото?
        """
        self.__markup.add(types.InlineKeyboardButton(text='✅' + hotel_kbd[loc][0], callback_data='yes_photo'),
                          types.InlineKeyboardButton(text='❌' + hotel_kbd[loc][1], callback_data='no_photo'))
        return self.__markup

    def photo_numb(self) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок для выбора количества выводимых фото
        """
        self.__markup.row_width = 5
        self.__markup.add(types.InlineKeyboardButton(text='1', callback_data='one_photo'),
                          types.InlineKeyboardButton(text='2', callback_data='two_photo'),
                          types.InlineKeyboardButton(text='3', callback_data='three_photo'),
                          types.InlineKeyboardButton(text='4', callback_data='four_photo'),
                          types.InlineKeyboardButton(text='5', callback_data='five_photo'))
        return self.__markup

    @classmethod
    def my_commands(cls, lng) -> [types.BotCommand]:
        """ Функция возвращает каманды на языке пользователя
        """

        return [types.BotCommand("lowprice", commands_bot[lng]["lowprice"]),
                types.BotCommand("highprice", commands_bot[lng]["highprice"]),
                types.BotCommand("bestdeal", commands_bot[lng]["bestdeal"]),
                types.BotCommand("history", commands_bot[lng]["history"]),
                types.BotCommand("help", commands_bot[lng]["help"])]


class MyStyleCalendar(WYearTelegramCalendar):
    """ Класс календаря с выбором дня месяца
    """
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"


def diff_date(checkIn: str, checkOut: str) -> int:
    """
    Функция определения количества суток проживания
    :return: возвращает количество суток
    """
    a, b = checkIn.split('-'), checkOut.split('-')
    d = str(datetime.date(int(b[0]), int(b[1]), int(b[2])) - datetime.date(int(a[0]), int(a[1]), int(a[2])))

    return int(d.split()[0])


@bot.message_handler(commands=["help", "start"])
def help_start_message(message: types.Message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    user[message.chat.id].command = message.text.lower()
    bot.send_message(chat_id=message.chat.id,
                     text='Выберите язык (Choose language)',
                     reply_markup=Keyboard().set_lang())


@bot.message_handler(commands=["lowprice", "highprice"])
def lowprice_message(message: types.Message):
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
def bestdeal_message(message: types.Message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].clearCache()
    user[message.chat.id].command = message.text.lower()
    if user[message.chat.id].language == '':
        user[message.chat.id].language = (
            message.from_user.language_code + "_RU" if not user[message.chat.id].language else user[
                message.chat.id].language)
    pass


@bot.message_handler(commands=["history"])
def history_message(message: types.Message):
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
def get_text_messages(message: types.Message):
    if not user.get(message.from_user.id):
        user[message.from_user.id] = Users(message)
    user[message.chat.id].language = (
        "ru_RU" if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', message.text.lower())) else "en_US")
    bot.send_message(text=l_text[user[message.chat.id].language][2] + info_help[user[message.chat.id].language],
                     chat_id=message.from_user.id)


def ask_search_city(message: types.Message):
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
    bot.set_my_commands(Keyboard().my_commands(user[message.chat.id].language))
    msg = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][0])
    user[message.from_user.id].message_id = msg.message_id
    command = user[message.from_user.id].command
    query_str = user[message.from_user.id].query_string('0')
    if not get_city_id(query_str, message):
        user[message.chat.id].clearCache()
        user[message.chat.id].command = command
        bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][1])
        m = bot.send_message(message.chat.id, loctxt[user[message.chat.id].language][2])
        bot.register_next_step_handler(m, ask_search_city)


def ask_date(message: types.Message, txt):
    lng = user[message.chat.id].language
    bot.edit_message_text(text=txt, chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          parse_mode='MARKDOWN',
                          reply_markup=MyStyleCalendar(calendar_id=1,
                                                       locale=lng[:2]).build()[0])


def ask_count_hotels(message: types.Message):
    """Функция предлагает указать количество отелей, которые необходимо вывести
    :param message: входящее сообщение от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][5],
                          chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=Keyboard().hotel_numb())


def ask_show_photo(message: types.Message):
    """Функция предлагает показ фотографии отелей
    :param message: входящее сообщение от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][6], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=Keyboard().photo_yes_no(user[message.chat.id].language))


def ask_count_photo(message: types.Message):
    """
    Функция прелагает выбрать количество фото для загрузки
    :param mess: объект входящего сообщения от пользователя
    """
    bot.edit_message_text(text=loctxt[user[message.chat.id].language][7], chat_id=message.chat.id,
                          message_id=user[message.chat.id].message_id,
                          reply_markup=Keyboard().photo_numb())


def step_show_info(message: types.Message):
    """
    Функция для вывода информации в чат
    :param mess: объект входящего сообщения от пользователя
    """
    bot.delete_message(chat_id=message.chat.id, message_id=user[message.chat.id].message_id)
    command = user[message.chat.id].command
    query_str = user[message.chat.id].query_string(command)
    hotel_query(query_str, message)


def history(message: types.Message):
    if user[message.chat.id].language == '':
        user[message.chat.id].language = (
            message.from_user.language_code + "_RU" if not user[message.chat.id].language else user[
                message.chat.id].language)
    bot.set_my_commands(Keyboard().my_commands(user[message.chat.id].language))
    history = user[message.chat.id].history(logging, datetime)
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
                    f"{datetime.datetime.now()} - Функция req_api - Превышена ежемесячная квота для запросов по плану BASIC.")
                return json.loads(response.text)
            else:
                logging.error(f"{datetime.datetime.now()} - Функция req_api - Что-то пошло не так. Повторите позже.")
                return server_error[lng]["erhttp"]
    except ConnectionError as ercon:
        logging.error(f"{datetime.datetime.now()} - {ercon} - Функция req_api - Нет, соединения с сервисом.")
        return server_error[lng]["ercon"]
    except TimeoutError as ertime:
        logging.error(f"{datetime.datetime.now()} - {ertime} - Функция req_api - Время ожидания запроса истекло")
        return server_error[lng]["ertime"]
    except json.decoder.JSONDecodeError as erjson:
        logging.error(f"{datetime.datetime.now()} - {erjson} - Функция req_api - Получен некорректный ответ от сервиса.")
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
    :param message: сообщение
    """
    lang = user[message.chat.id].language
    l_txt = loc[lang]
    search_city = querystring["query"]
    result_id_city = req_api(config('URL'), querystring, lang)

    if isinstance(result_id_city, dict) and not result_id_city.get("message"):
        if len(result_id_city) > 0:
            markup = types.InlineKeyboardMarkup()
            for city in result_id_city['suggestions']:
                for name in city['entities']:
                    parse_city = (BeautifulSoup(name['caption'], 'html.parser').get_text()).lower()
                    if parse_city.startswith(search_city) and name['type'] == 'CITY':
                        # Добавить для точного совпадения города: and name['name'].lower() == search_city
                        markup.add(types.InlineKeyboardButton(parse_city.title(),
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
    :param querystring: строка запроса
    :return result_low: возвращает словарь (название отеля, адрес,
    фотографии отеля (если пользователь счёл необходимым их вывод)
    """

    url_low = config('URL_LOW')
    loc = querystring["locale"]
    low_data = req_api(url_low, querystring, loc)

    links_htmls = ("https://ru.hotels.com/ho{}" if loc[:2] == "ru"
                   else "https://hotels.com/ho{}?pos=HCOM_US&locale=en_US")

    if low_data:
        for hotel_count, results in enumerate(low_data['data']['body']['searchResults']['results']):
            difdate = diff_date(user[message.chat.id].checkIn, user[message.chat.id].checkOut)
            summa = round(float(difdate) * results["ratePlan"]["price"]["exactCurrent"], 2)
            if querystring["pageSize"] != hotel_count:
                txt = f"<strong>⭐⭐⭐{loc_txt[loc][0]} {(results.get('starRating')) if results.get('starRating') else '--'}⭐⭐⭐</strong>\n" \
                      f"🏨 {loc_txt[loc][1]} {results['name']}\n" \
                      f"       {loc_txt[loc][2]} {results['address'].get('countryName')}, {results['address'].get('locality')}, " \
                      f"{(results['address'].get('streetAddress') if results['address'].get('streetAddress') else loc_txt[loc][10])}\n" \
                      f"🚗 {loc_txt[loc][3]} {results['landmarks'][0]['distance']}\n" \
                      f"📅 {loc_txt[loc][4]} {querystring['checkIn']} - {querystring['checkOut']}\n" \
                      f"💵 {loc_txt[loc][5]} <b>{(results['ratePlan']['price']['exactCurrent']) if results['ratePlan']['price']['exactCurrent'] else loc_txt[loc][11]}</b>\n" \
                      f"💵 {loc_txt[loc][6].format(difdate)} <b>{summa if results['ratePlan']['price']['exactCurrent'] else loc_txt[loc][11]}</b>\n" \
                      f"🌍 {loc_txt[loc][7]}" + f"{links_htmls.format(results['id'])}\n\n"

                if user[message.chat.id].status_show_photo:
                    data_photo = get_photos(results['id'])

                    photo_lst = [types.InputMediaPhoto(media=link) for index, link in enumerate(data_photo) if
                                 user[message.chat.id].count_show_photo > index]
                    try:
                        bot.send_media_group(chat_id=message.chat.id, media=photo_lst)
                    except Exception as er:
                        logging.error(f"{datetime.datetime.now()} - {er} - Функция hotel_query - Отправка фото")

                    user[message.chat.id].all_hotels[txt] = photo_lst
                    photo_lst.clear()
                else:
                    user[message.chat.id].all_hotels[txt] = []
                try:
                    bot.send_message(chat_id=message.chat.id, text=txt,
                                     disable_web_page_preview=True,
                                     parse_mode="HTML")

                except Exception as e:
                    logging.error(f"{datetime.datetime.now()} - {e} - Функция hotel_query - Отправка гостиниц")
                txt = ''
        user[message.chat.id].insert_db(logging, datetime)
        bot.send_message(chat_id=message.chat.id, text=loc_txt[loc][8].format(len(user[message.chat.id].all_hotels)))

        with open('hotel.json', 'w') as f:
            json.dump(user[message.chat.id].all_hotels, f, indent=4)
    else:
        bot.send_message(chat_id=message.chat.id, text=low_data,
                         disable_web_page_preview=True,
                         parse_mode="HTML")


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
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
        bot.answer_callback_query(callback_query_id=call.id)
        ask_show_photo(call.message)

    elif call.data in ["one_photo", "two_photo", "three_photo", "four_photo", "five_photo"]:
        numbers_photo = {"one_photo": 1, "two_photo": 2, "three_photo": 3, "four_photo": 4, "five_photo": 5}
        user[call.message.chat.id].count_show_photo = numbers_photo[call.data]
        bot.answer_callback_query(callback_query_id=call.id)
        step_show_info(call.message)

    elif call.data in ['ru_RU', 'en_US']:
        user[call.message.chat.id].language = call.data
        bot.set_my_commands(Keyboard().my_commands(user[call.message.chat.id].language))
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

    else:
        bot.answer_callback_query(callback_query_id=call.id)


if __name__ == '__main__':
    while True:
        try:
            logging.error(f"{datetime.datetime.now()} - Бот запущен")
            bot.polling(none_stop=True, interval=0)
        except Exception as ex:
            logging.error(f"{datetime.datetime.now()} - {ex} - Модуль main")
