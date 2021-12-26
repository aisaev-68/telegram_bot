# -*- coding: utf-8 -*-


import sqlite3
from sqlite3 import Error
from telegram_bot_calendar import WYearTelegramCalendar, DAY


class MyStyleCalendar(WYearTelegramCalendar):
    """ Класс календаря с выбором дня месяца
    """
    first_step = DAY
    prev_button = "⬅️"
    next_button = "➡️"


class Users:
    """
    Класс пользователя, для хранения промежуточной информации.
        Args: user: объект вх. сообщения от пользователя
    """

    def __init__(self, message) -> None:
        self.__username: str = message.from_user.username
        self.__id_user: int = message.from_user.id
        self.__search_city: str = ''
        self.__command: str = ''
        self.__id_city: str = ''
        self.__checkIn: str = ''
        self.__checkOut: str = ''
        self.__count_show_hotels: int = 0
        self.__count_show_photo: int = 0
        self.__status_show_photo: bool = False
        self.__price_min: int = 0
        self.__price_max: int = 0
        self.__distance_max: float = 0.0
        self.__distance_min: float = 0.0
        self.__language: str = ''
        self.__currency: str = ''
        self.__message_id: str = ''

    @property
    def search_city(self) -> str:
        return self.__search_city

    @search_city.setter
    def search_city(self, city: str) -> None:
        self.__search_city = city

    @property
    def id_city(self) -> str:
        return self.__id_city

    @id_city.setter
    def id_city(self, idcity: str) -> None:
        self.__id_city = idcity

    @property
    def checkIn(self) -> str:
        return self.__checkIn

    @checkIn.setter
    def checkIn(self, in_date: str) -> None:
        self.__checkIn = in_date

    @property
    def checkOut(self) -> str:
        return self.__checkOut

    @checkOut.setter
    def checkOut(self, out_date: str) -> None:
        self.__checkOut = out_date

    @property
    def count_show_hotels(self) -> int:
        return self.__count_show_hotels

    @count_show_hotels.setter
    def count_show_hotels(self, count: int) -> None:
        self.__count_show_hotels = count

    @property
    def count_show_photo(self) -> int:
        return self.__count_show_photo

    @count_show_photo.setter
    def count_show_photo(self, count: int) -> None:
        self.__count_show_photo = count

    @property
    def distance_max(self) -> float:
        return self.__distance_max

    @distance_max.setter
    def distance_max(self, dist_max: float) -> None:
        self.__distance_max = dist_max

    @property
    def distance_min(self) -> float:
        return self.__distance_min

    @distance_min.setter
    def distance_min(self, dist_min: float) -> None:
        self.__distance_min = dist_min

    @property
    def price_min(self) -> int:
        return self.__price_min

    @price_min.setter
    def price_min(self, pr_min: int) -> None:
        self.__price_min = pr_min

    @property
    def price_max(self) -> int:
        return self.__price_max

    @price_max.setter
    def price_max(self, pr_max: int) -> None:
        self.__price_max = pr_max

    @property
    def command(self) -> str:
        return self.__command

    @command.setter
    def command(self, cmnd: str) -> None:
        self.__command = cmnd

    @property
    def message_id(self) -> str:
        return self.__message_id

    @message_id.setter
    def message_id(self, mesid: str) -> None:
        self.__message_id = mesid

    @property
    def language(self) -> str:
        return self.__language

    @language.setter
    def language(self, lng: str) -> None:
        self.__language = lng

    @property
    def currency(self) -> str:
        return self.__currency

    @currency.setter
    def currency(self, curr: str) -> None:
        self.__currency = curr

    @property
    def status_show_photo(self) -> bool:
        return self.__status_show_photo

    @status_show_photo.setter
    def status_show_photo(self, status: bool) -> None:
        self.__status_show_photo = status

    def query_string(self, idcity: str = None) -> dict:
        """Функция формирует строку запроса в виде словаря
        :param idcity: команды для формирования строки запроса по поиску ID города
        возвращает строку запроса к API в виде словаря

        """
        querystring = {}
        if idcity == 'city':
            querystring = {"query": self.__search_city, "locale": self.__language}

        elif self.__command == '/lowprice':
            querystring = {
                "destinationId": self.__id_city,
                "pageNumber": "1",
                "pageSize": str(self.__count_show_hotels),
                "checkIn": self.__checkIn,
                "checkOut": self.__checkOut,
                "adults1": "1",
                "sortOrder": "PRICE",
                "locale": self.__language,
                "currency": self.__currency
            }
        elif self.__command == '/highprice':
            querystring = {
                "destinationId": self.__id_city,
                "pageNumber": "1",
                "pageSize": str(self.__count_show_hotels),
                "checkIn": self.__checkIn,
                "checkOut": self.__checkOut,
                "adults1": "1",
                "sortOrder": "PRICE_HIGHEST_FIRST",
                "locale": self.__language,
                "currency": self.__currency
            }

        elif self.__command == '/bestdeal':
            querystring = {
                "destinationId": self.__id_city,
                "pageNumber": "1",
                "pageSize": str(self.__count_show_hotels),
                "checkIn": self.__checkIn,
                "checkOut": self.__checkOut,
                "adults1": "1",
                "sortOrder": "PRICE",
                "locale": self.__language,
                "currency": self.__currency,
                "priceMin": str(self.__price_min),
                "priceMax": str(self.__price_max),
                "landmarkIds": ("City center" if self.__language == "en_US" else "Центр города")
            }
        return querystring

    def get_param(self) -> dict:
        param = {'command': self.__command, 'stat_photo': self.__status_show_photo,
                 'count_photo': self.__count_show_photo}
        if self.__command == '/bestdeal':
            param = {'command': self.__command, 'dist_min': self.__distance_min,
                     'dist_max': self.__distance_max, 'stat_photo': self.__status_show_photo,
                     'count_photo': self.__count_show_photo}
        return param

    def clearCache(self) -> None:
        """Функция для очистки не нужных данных при формировании нового запроса"""

        self.__search_city: str = ''
        self.__command: str = ''
        self.__id_city: str = ''
        self.__checkIn: str = ''
        self.__checkOut: str = ''
        self.__count_show_hotels: int = 0
        self.__count_show_photo: int = 0
        self.__status_show_photo: bool = False
        self.__price_min: int = 0
        self.__price_max: int = 0
        self.__distance_min: float = 0.0
        self.__distance_max: float = 0.0
        self.__currency: str = ''
        self.__message_id: str = ''

    def insert_db(self, all_hotels, logging, datetime) -> None:
        """Функция вставки данных (ID пользователя, имени, команды,
        даты запроса, списка найденных гостиниц без фото) в базу данных
        """
        lng = self.__language
        d_loc: dict = {"ru_RU": ["Команда:", "Дата и время запроса:"],
                       "en_US": ["Command:", "Request date and time:"]}
        try:
            con = sqlite3.connect('data.db')
            with con:
                con.execute(
                    "CREATE TABLE IF NOT EXISTS users(user_id INTEGER, name TEXT, "
                    "command TEXT, date TEXT, hotels TEXT);")

            txt = ''
            for item in list(all_hotels.keys()):
                txt += item
            with con:
                con.execute("INSERT INTO users(user_id, name, command, date, hotels) "
                            "VALUES(?, ?, ?, ?, ?);",
                            (self.__id_user, self.__username, self.__command, str(datetime.now()),
                             f"<strong>{d_loc[lng][0]} {self.__command}\n{d_loc[lng][1]} "
                             f"{str(datetime.now())}</strong>\n{txt}"))
        except Error:
            logging.error(f"Функция insert_db - {Error}")

    def history(self, logging, numb: int) -> list:
        """Функция возвращет историю запросов пользователя (команда,
        дата запроса, список найденных гостиниц без фото (три последние запросы с ответами)
        """
        try:
            con = sqlite3.connect('data.db')
            with con:
                con.execute(
                    "CREATE TABLE IF NOT EXISTS users(user_id INTEGER, name TEXT, "
                    "command TEXT, date TEXT, hotels TEXT);")
            with con:
                cur = con.cursor()
                cur.execute(
                    "SELECT hotels FROM users WHERE user_id ={} "
                    "ORDER BY rowid DESC LIMIT {};".format(self.__id_user, numb))
                rows = cur.fetchall()
                return rows
        except Error:
            logging.error(f"Функция history - {Error}")
