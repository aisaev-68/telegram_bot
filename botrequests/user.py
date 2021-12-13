# -*- coding: utf-8 -*-

import datetime
import database
from keyboards import PhotoYesNo, HotelKbd, PhotoNumbKbd, Lang, types

commands_bot = {
    "ru_RU": {
        "lowprice": "Поиск дешевых отелей",
        "highprice": "Поиск отелей класса люкс", "bestdeal": "Поиск лучших отелей",
        "history": "Показать историю запросов", "help": "Помощь"},
    "en_US": {
        "lowprice": "Search for cheap hotels",
        "highprice": "Search for luxury hotels", "bestdeal": "Search for the best hotels",
        "history": "Show request history", "help": "Help", }}


class Users:
    """
    Класс пользователя, с параметрами необходимыми для формирования запроса.
        Args: user: объект вх. сообщения от пользователя
    """

    def __init__(self, mess) -> None:
        self.__username: str = mess.from_user.username
        self.__id_user: int = mess.from_user.id
        self.__search_city: str = ''
        self.__command: str = ''
        self.__id_city: str = ''
        self.__checkIn: str = ''
        self.__checkOut: str = ''
        self.__count_show_hotels: int = 0
        self.__count_show_photo: int = 0
        self.__status_show_photo: bool = False
        self.__price_min_max: dict = dict()
        self.__distance_max: float = 0.0
        self.__language: str = ''
        self.__currency: str = ''
        self._get_hotel_kbd: types.InlineKeyboardMarkup = HotelKbd().get_hotel_kbd()
        self.__get_kbd_photo_numb: types.InlineKeyboardMarkup = PhotoNumbKbd().get_kbd_photo_numb()
        self._inl_lang = Lang().get_langkb()
        self.__get_photo_yes_no: types.InlineKeyboardMarkup = PhotoYesNo().get_photo_yes_no()
        self.__all_hotels: dict = dict()
        self.__message_id: str = ''
        self.__my_commands: list = []

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
    def distance_max(self, distance: float) -> None:
        self.__distance_max = distance

    @property
    def price_min_max(self) -> dict:
        return self.__price_min_max

    @price_min_max.setter
    def price_min_max(self, pr_min_max: str) -> None:
        self.__price_min_max["price_min"] = pr_min_max.split()[0]
        self.__price_min_max["price_max"] = pr_min_max.split()[1]

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
        print(11, self.__message_id)
        self.__message_id = mesid

    @property
    def language(self) -> str:
        return self.__language

    @language.setter
    def language(self, lng: str) -> None:
        self.__language = lng
        self.__my_commands = [types.BotCommand("lowprice", commands_bot[lng]["lowprice"]),
                              types.BotCommand("highprice", commands_bot[lng]["highprice"]),
                              types.BotCommand("bestdeal", commands_bot[lng]["bestdeal"]),
                              types.BotCommand("history", commands_bot[lng]["history"]),
                              types.BotCommand("help", commands_bot[lng]["help"])]
        self.__get_photo_yes_no: types.InlineKeyboardMarkup = PhotoYesNo(lng).get_photo_yes_no()
        self.__get_kbd_photo_numb: types.InlineKeyboardMarkup = PhotoNumbKbd().get_kbd_photo_numb()

    @property
    def currency(self) -> str:
        return self.__currency

    @currency.setter
    def currency(self, curr: str) -> None:
        self.__currency = curr

    @property
    def all_hotels(self) -> dict:
        return self.__all_hotels

    @all_hotels.setter
    def all_hotels(self, hotel_dict: dict) -> None:
        self.__all_hotels = hotel_dict

    @property
    def status_show_photo(self) -> bool:
        return self.__status_show_photo

    @status_show_photo.setter
    def status_show_photo(self, status: bool):
        self.__status_show_photo = status

    @property
    def my_commands(self) -> list:
        return self.__my_commands

    def getInl_lang(self):
        return self._inl_lang

    def getHotel_kbd(self) -> types.InlineKeyboardMarkup:
        return self._get_hotel_kbd

    def getPhoto_yes_no(self) -> types.InlineKeyboardMarkup:
        return self.__get_photo_yes_no

    def getKbd_photo_numb(self) -> types.InlineKeyboardMarkup:
        return self.__get_kbd_photo_numb

    def diff_date(self) -> int:
        """
        Функция определения количества суток проживания
        :return: возвращает количество суток
        """
        diff_date = 0
        if self.__checkIn and self.__checkOut:
            a = self.__checkIn.split('-')
            b = self.__checkOut.split('-')
            d = str(datetime.date(int(b[0]), int(b[1]), int(b[2])) - datetime.date(int(a[0]), int(a[1]), int(a[2])))
            diff_date = int(d.split()[0])

        return diff_date

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
                'language': self.__language, 'currency': self.__currency,
                'diff_date': self.diff_date()}

    def clearCache(self):
        """Функция для очистки не нужных данных при формировании нового запроса"""

        self.__search_city: str = ''
        self.__command: str = ''
        self.__id_city: str = ''
        self.__checkIn: str = ''
        self.__checkOut: str = ''
        self.__count_show_hotels: int = 0
        self.__count_show_photo: int = 0
        self.__status_show_photo: bool = False
        self.__price_min_max: dict = dict()
        self.__distance_max: float = 0.0
        self.__currency: str = ''
        self.__all_hotels: dict = dict()
        self.__message_id: str = ''

    def insert_db(self):
        """Функция вставки данных (ID пользователя, имени, команды,
        даты запроса, списка найденных гостиниц без фото) в базу данных
        """
        con = database.sql_connection()
        database.sql_table(con)
        txt = ''
        for item in list(self.__all_hotels.keys()):
            txt += item
        database.sql_insert(con, (self.__id_user, self.__username, self.__command,
                                  str(datetime.datetime.now()), txt))
        con.close()

    def history(self) -> list:
        """Функция возвращет историю запросов пользователя (команда,
        дата запроса, список найденных гостиниц без фото (две последние запросы с ответами)
        """
        con = database.sql_connection()
        database.sql_table(con)
        rows = database.sql_fetch(con, self.__id_user)
        con.close()
        return rows
