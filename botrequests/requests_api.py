# -*- coding: utf-8 -*-

import requests
import json
from handlers import logging, config
from datetime import datetime
from locales import loc_txt


commands = ["/lowprice", "/highprice", "/bestdeal", "/history"]

def req_api(url: str, querystring: dict):
    """
    Функция возвращает данные запроса к API гостиниц.
    :param url: страница поиска
    :param querystring: срока запроса
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
            return None
    except ConnectionError as ercon:
        logging.error(f"{datetime.now()} - {ercon} - Нет, соединения с сервисом.")
        return None
    except TimeoutError as ertime:
        logging.error('Время ожидания запроса истекло {}'.format(ertime) )
        return None
    except json.decoder.JSONDecodeError as erjson:
        logging.error(f'JSON decode error {erjson} - Получен некорректный ответ от сервиса.')
        return None

def query_string(command: str, qstring: dict) -> dict:

    """Функция формирует строку запроса в виде словаря
    :param command: команды от пользователя /lowprice, /highprice, /bestdeal
    :param qstring: исходные данные в виде словаря для формирования строки запроса
    возвращает строку запроса к API в виде словаря

    """
    querystring = None
    if commands[0] == command:
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
        pass
    if commands[2] == command:
        pass

    return querystring


def get_city_id(search_city: str, lang: str) -> str:
    """
    Функция возвращает ID города. Если город не найден, возвращает пустую строку.
    :param search_city: строка запроса
    :param lang: язык запроса
    """
    querystring = {"query": search_city, "locale": lang}
    url = config('URL')

    result_id_city = req_api(url, querystring)
    destination_id = None
    # TypeError: 'NoneType' object is not subscriptable
    for group in result_id_city['suggestions']:
        if group['group'] == 'CITY_GROUP':
            if group['entities']:
                destination_id = group['entities'][0]['destinationId']
                break
    return destination_id


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


def hotel_query(querystring: dict, source_dict: dict) -> dict:
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
    low_data = req_api(url_low, querystring)

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
                      f"🌍 {loc_txt[loc][7]}" + f"{links_htmls.format(results['id'])}"
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
                    hotels_dict[txt] = ['']
        return hotels_dict




