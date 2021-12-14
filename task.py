def getSource_dict(self):
    """Функция возвращает исходные данные для формирования запроса к API"""

    return {'id_user': self.__id_user, 'search_city': self.__search_city, 'id_city': self.__id_city,
            'checkIn': self.__checkIn, 'checkOut': self.__checkOut,
            'command': self.__command, 'count_show_hotels': self.__count_show_hotels,
            'count_show_photo': self.__count_show_photo,
            'status_show_photo': self.__status_show_photo,
            'price_min': self.__price_min_max.get('min'),
            'price_max': self.__price_min_max.get('max'),
            'distance_max': self.__distance_max,
            'language': self.__language, 'currency': self.__currency}

def query_string(command: str, qstring: dict) -> dict:
    """Функция формирует строку запроса в виде словаря
    :param command: команды от пользователя /lowprice, /highprice, /bestdeal
    :param qstring: исходные данные в виде словаря для формирования строки запроса
    возвращает строку запроса к API в виде словаря

    """
    if command[0] == self.__command:
        querystring = {"query": self.__search_city, "locale": self.__language}

    elif commands[1] == command:
        querystring = {
            "destinationId": self.__id_city,
            "pageNumber": "1",
            "pageSize": self.__count_show_hotels,
            "checkIn": self.__checkIn,
            "checkOut": self.__checkOut,
            "adults1": "1",
            "sortOrder": "PRICE",
            "locale": self.__language,
            "currency": self.__currency
        }
    if commands[1] == command:
        querystring = {
            "destinationId": self.__id_city,
            "pageNumber": "1",
            "pageSize": self.__count_show_hotels,
            "checkIn": self.__checkIn,
            "checkOut": self.__checkOut,
            "adults1": "1",
            "sortOrder": "PRICE_HIGHEST_FIRST",
            "locale": self.__language,
            "currency": self.__currency
        }

    elif commands[2] == command:
        querystring = {
            "destinationId": self.__id_city,
            "pageNumber": "1",
            "pageSize": "25",
            "checkIn": self.__checkIn,
            "checkOut": self.__checkOut,
            "adults1": "1",
            "sortOrder": "PRICE",
            "locale": self.__language,
            "currency": self.__currency,
            "priceMin": self.__price_min_max.get('min'),
            "priceMax": self.__price_min_max.get('max'),
            "landmarkIds": ("City center" if self.__language == "en_US" else "Центр города")
        }

    return querystring