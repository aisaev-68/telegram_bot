from decouple import config
import json
from telebot import TeleBot, util
from keyboards import types, Keyboard
import requests
from datetime import datetime
import logging
from typing import Any
from bs4 import BeautifulSoup

bot = TeleBot(config('TELEGRAM_API_TOKEN'))

logging.basicConfig(filename="logger.log", level=logging.INFO)

user: dict = {}

server_error = {"ru_RU": {"ertime": "Время ожидания запроса истекло. Попробуйте позже.",
                          "erjson": "Получен некорректный ответ от сервиса. Попробуйте позже.",
                          "ercon": "Нет, соединения с сервисом. Попробуйте позже.",
                          "erhttp": "Что-то пошло не так. Повторите позже."},
                "en_US": {"ertime": "The request timed out. Please try again later.",
                          "erjson": "Received an invalid response from the service. Please try again later.",
                          "ercon": "No, connecting to the service. Please try again later.",
                          "erhttp": "Something went wrong. Please try again later."}}

loc = {'ru_RU':
           ['Отмена', 'Пожалуйста, уточните город', 'Превышена ежемесячная квота для запросов по плану BASIC.',
            'Ваша история пуста.', 'Команда выполнена.'],
       'en_US':
           ['Cancel', 'Please specify city', 'Monthly quota exceeded for BASIC plan requests.',
            'Your history is empty.', 'Command completed.']
       }

loc_txt = {'ru_RU':
               ['Рейтинг: ', 'Отель: ', 'Адрес: ', 'От центра города:', 'Дата заезда-выезда: ',
                'Цена за сутки (в руб): ', 'Цена за {} сутки (в руб): ', 'Ссылка на страницу: ',
                'Найдено {} отелей', 'Нет данных об адресе.', 'Нет данных о расценках.'],
           'en_US':
               ['Rating: ', 'Hotel: ', 'Address: ', 'From the city center: ', 'Check-in (check-out) date: ',
                'Price per day (USD): ', 'Price for {} day (USD): ', 'link to the page: ',
                'Found {} hotels', 'No address data.', 'No price data.']
           }


def price_parse(line_text: dict, lang: str, logging, datetime) -> dict:
    """Функция возвращает из полученной строки кол-во дней, общаую сумму и цену за сутки в виде словаря
    {'day': day, 'price_total': price_total, 'price_day': price_day}
    :param line_text: строка для парсинга
    :param lang: язык пользователя
    :param logging: модуль logging
    :param datetime: модуль datetime"""
    if lang == 'ru_RU':
        try:
            day = line_text['price']['info'].split()[4]
            price_total = line_text['price']['exactCurrent']
            price_day = round(price_total / float(day), 2)
            return {'day': day, 'price_total': price_total, 'price_day': price_day}
        except Exception as er:
            logging.error(f"{datetime.now()} - {er} - Функция price_parse (русский язык)")
    else:
        try:
            day = BeautifulSoup(line_text['price']['fullyBundledPricePerStay'], 'html.parser').get_text().split()[3]
            price_total = BeautifulSoup(line_text['price']['fullyBundledPricePerStay'], 'html.parser').get_text().split()[1][
            1:].replace(',', '')
            print(BeautifulSoup(line_text['price']['fullyBundledPricePerStay'], 'html.parser'))
            price_day = round(float(price_total) / float(day), 2)
            return {'day': day, 'price_total': price_total, 'price_day': price_day}
        except Exception as er:
            logging.error(f"{datetime.now()} - {er} - Функция price_parse (английски язык)")


def city_parse(line_text: str) -> str:
    """Функци возвращает из полученной строки названия города и региона
    :param line_text: срока для парсинга
    """

    return BeautifulSoup(line_text, 'html.parser').get_text().lower()


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
    lang = querystring["locale"]
    data = req_api(url_low, querystring, lang)
    links_htmls = ("https://ru.hotels.com/ho{}" if lang == "ru_RU"
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
                txt = f"<strong>⭐⭐⭐{loc_txt[lang][0]} {(results.get('starRating')) if results.get('starRating') else '--'}⭐⭐⭐</strong>\n" \
                      f"🏨 {loc_txt[lang][1]} {results['name']}\n" \
                      f"       {loc_txt[lang][2]} {results['address'].get('countryName')}, {results['address'].get('locality')}, " \
                      f"{(results['address'].get('streetAddress') if results['address'].get('streetAddress') else loc_txt[lang][10])}\n" \
                      f"🚗 {loc_txt[lang][3]} {results['landmarks'][0]['distance']}\n" \
                      f"📅 {loc_txt[lang][4]} {querystring['checkIn']} - {querystring['checkOut']}\n" \
                      f"💵 {loc_txt[lang][5]} <b>{price['price_day']}</b>\n" \
                      f"💵 {loc_txt[lang][6].format(price['day'])} <b>{price['price_total']}</b>\n" \
                      f"🌍 {loc_txt[lang][7]} {links_htmls.format(results['id'])}\n\n"

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
        bot.send_message(chat_id=message.chat.id, text=loc_txt[lang][8].format(len(user[message.chat.id].all_hotels)))
        with open('hotel.json', 'w') as f:
            json.dump(user[message.chat.id].all_hotels, f, indent=4)
    else:
        bot.send_message(chat_id=message.chat.id, text=data,
                         disable_web_page_preview=True,
                         parse_mode="HTML")


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
        txt = loc[user[message.chat.id].language][3]
        bot.send_message(chat_id=message.chat.id, text=txt)
    else:
        for elem in history:
            splitted_text = util.split_string(elem, 3000)
            for txt in splitted_text:
                bot.send_message(chat_id=message.chat.id, text=txt, disable_web_page_preview=True, parse_mode="HTML")

    bot.send_message(chat_id=message.chat.id, text=loc[user[message.chat.id].language][4])