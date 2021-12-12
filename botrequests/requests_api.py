# -*- coding: utf-8 -*-
import re
import requests
import json
from handlers import logging, config
from datetime import datetime
from locales import loc_txt
from typing import Any
from bs4 import BeautifulSoup

commands = ["/lowprice", "/highprice", "/bestdeal", "/history"]


def req_api(url: str, querystring: dict, lng="en_US") -> Any:
    """
    Функция возвращает данные запроса к API гостиниц.
    :param url: страница поиска
    :param querystring: срока запроса
    :return data: возвращаемые API данные
    """
    server_error = {"ru_RU": {"ertime": "Время ожидания запроса истекло. Попробуйте позже.",
                              "erjson": "Получен некорректный ответ от сервиса. Попробуйте позже.",
                              "ercon": "Нет, соединения с сервисом. Попробуйте позже.",
                              "erhttp": "Что-то пошло не так. Повторите позже."},
                    "en_US": {"ertime": "The request timed out. Please try again later.",
                               "erjson": "Received an invalid response from the service. Please try again later.",
                               "ercon": "No, connecting to the service. Please try again later.",
                               "erhttp": "Something went wrong. Please try again later."}}
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
            logging.error(f"{datetime.now()} - Что-то пошло не так. Повторите позже.")
            return server_error[lng]["erhttp"]
    except ConnectionError as ercon:
        logging.error(f"{datetime.now()} - {ercon} - Нет, соединения с сервисом.")
        return server_error[lng]["ercon"]
    except TimeoutError as ertime:
        logging.error(f"{datetime.now()} - {ertime} -Время ожидания запроса истекло")
        return server_error[lng]["ertime"]
    except json.decoder.JSONDecodeError as erjson:
        logging.error(f"{datetime.now()} - {erjson} - Получен некорректный ответ от сервиса.")
        return server_error[lng]["erjson"]


def query_string(command: str, qstring: dict) -> dict:
    """Функция формирует строку запроса в виде словаря
    :param command: команды от пользователя /lowprice, /highprice, /bestdeal
    :param qstring: исходные данные в виде словаря для формирования строки запроса
    возвращает строку запроса к API в виде словаря

    """
    querystring = {
        "destinationId": qstring['id_city'],
        "pageNumber": "1",
        "pageSize": qstring['count_show_hotels'],
        "checkIn": qstring['checkIn'],
        "checkOut": qstring['checkOut'],
        "adults1": "1",
        "sortOrder": "PRICE",
        "locale": qstring['language'],
        "currency": qstring['currency']
    }
    if commands[1] == command:
        querystring.update({"sortOrder": "PRICE_HIGHEST_FIRST"})
    if commands[2] == command:
        querystring.update({"pageSize": "25", "priceMin": qstring['min'],
                            "priceMax": qstring['max'],
                            "sortOrder": "PRICE",
                            "landmarkIds": ("City center" if qstring['language'] == "en_US" else "Центр города")}
                           )
    return querystring


def get_city_id(search_city: str, lang: str) -> Any:
    """
    Функция возвращает ID города. Если город не найден, возвращает пустую строку.
    :param search_city: строка запроса
    :param lang: язык запроса
    """
    querystring = {"query": search_city, "locale": lang}
    result_id_city = req_api(config('URL'), querystring, lang)
    search_city_list = []
    print(type(result_id_city))
    # TypeError: 'NoneType' object is not subscriptable
    if isinstance(result_id_city, dict):
        for city in result_id_city['suggestions']:
            for name in city['entities']:
                parse_city = (BeautifulSoup(name['caption'], 'html.parser').get_text()).lower()
                if parse_city.startswith(search_city) and name['type'] == 'CITY':
                    # Добавить для точного совпадения and name['name'].lower() == search_city
                    search_city_list.append({
                        'destinationID': name['destinationId'],
                        'city_name': parse_city.title()})
        return search_city_list
    else:
        return result_id_city


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


def hotel_query(querystring: dict, source_dict: dict) -> Any:
    """
    Формирует словарь отелей на основе запроса пользователя и сортировкой по цене.
    Если отелей не найдено возвращает пустой словарь.
    :param querystring: строка запроса
    :param source_dict: исходные данные для формирования строки запроса
    :return result_low: возвращает словарь (название отеля, адрес,
    фотографии отеля (если пользователь счёл необходимым их вывод)
    """

    url_low = config('URL_LOW')
    hotels_dict = {}
    loc = source_dict['language']
    low_data = req_api(url_low, querystring, loc)

    links_htmls = ("https://ru.hotels.com/ho{}" if loc[:2] == "ru"
                   else "https://hotels.com/ho{}?pos=HCOM_US&locale=en_US")
    # TypeError: 'NoneType' object is not subscriptable
    if low_data:
        for hotel_count, results in enumerate(low_data['data']['body']['searchResults']['results']):
            summa = float(source_dict['diff_date']) * results["ratePlan"]["price"]["exactCurrent"]
            if source_dict['count_show_hotels'] != hotel_count:
                txt = f"⭐⭐⭐*{loc_txt[loc][0]} {(results.get('starRating')) if results.get('starRating') else '--'}*⭐⭐⭐\n" \
                      f"🏨 {loc_txt[loc][1]} {results['name']}\n" \
                      f"       {loc_txt[loc][2]} {results['address'].get('countryName')}, {results['address'].get('locality')}, " \
                      f"{(results['address'].get('streetAddress') if results['address'].get('streetAddress') else 'Нет данных об адресе...')}\n" \
                      f"🚗 {loc_txt[loc][3]} {results['landmarks'][0]['distance']}\n" \
                      f"📅 {loc_txt[loc][4]} {source_dict['checkIn']} - {source_dict['checkOut']}\n" \
                      f"💵 {loc_txt[loc][5]} *{(results['ratePlan']['price']['exactCurrent']) if results['ratePlan']['price']['exactCurrent'] else 'Нет данных о расценках...'}*\n" \
                      f"💵 {loc_txt[loc][6].format(source_dict['diff_date'])} *{summa if results['ratePlan']['price']['exactCurrent'] else 'Нет данных о расценках...'}*\n" \
                      f"🌍 {loc_txt[loc][7]}" + f"{links_htmls.format(results['id'])}\n"
                if source_dict['status_show_photo']:
                    data_photo = get_photos(results['id'])
                    photo_lst = []
                    for index, photo in enumerate(data_photo):
                        if source_dict['count_show_photo'] != index:
                            photo_lst.append(photo)
                        else:
                            break
                    hotels_dict[txt] = photo_lst
                else:
                    hotels_dict[txt] = []
        with open('hotel.json', 'w') as f:
            json.dump(hotels_dict, f, indent=4)
        return hotels_dict
    else:
        return low_data
