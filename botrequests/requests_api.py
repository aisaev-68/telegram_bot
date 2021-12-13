# -*- coding: utf-8 -*-
import re
import requests
import json
from handlers import logging, config
from datetime import datetime
from typing import Any

commands = ["/lowprice", "/highprice", "/bestdeal", "/history"]


def req_api(url: str, querystring: dict, lng="en_US") -> Any:
    """
    Функция возвращает данные запроса к API гостиниц.
    :param url: страница поиска
    :param querystring: срока запроса
    :param lng: язык пользователя
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
            if json.loads(response.text).get("message"):
                logging.error(f"{datetime.now()} - Превышена ежемесячная квота для запросов по плану BASIC.")
                return json.loads(response.text)
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
