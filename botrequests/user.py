# -*- coding: utf-8 -*-

import datetime
import database
from keyboards import PhotoYesNo, InlKbShow, HotelKbd, PhotoNumbKbd, InlKbShowNoPhoto, InlMenu, types


class Users:
    """
    Класс пользователя, с параметрами необходимыми для формирования запроса.
        Args: user: объект вх. сообщения от пользователя
    """

    def __init__(self, mess) -> None:
        self.__username = (mess.from_user.username if mess.from_user.username else mess.from_user.first_name)
        self.__id_user: int = mess.from_user.id
        self.__search_city: str = mess.text
        self.__command: str = ''
        self.__id_city: str = ''
        self.__checkIn: str = ''
        self.__checkOut: str = ''
        self.__count_show_hotels: int = 0
        self.__count_show_photo: int = 0
        self.__status_show_photo: bool = False
        self.__price_min_max: dict = dict()
        self.__distance_min_max: dict = dict()
        self.__language: str = ''
        self.__currency: str = ''
        self.__mes_id_hotel: int = 0
        self.__mes_id_photo: int = 0
        self._get_hotel_kbd: types.InlineKeyboardMarkup = HotelKbd().get_hotel_kbd()
        self.__get_photo_yes_no: types.InlineKeyboardMarkup = PhotoYesNo().get_photo_yes_no()
        self.__get_kbd_photo_numb: types.InlineKeyboardMarkup = PhotoNumbKbd().get_kbd_photo_numb()
        self.__get_show_kbd: types.InlineKeyboardMarkup = InlKbShow().get_show_kbd()
        self.__get_show_no_photo_kbd: types.InlineKeyboardMarkup = InlKbShowNoPhoto().get_show_kbd()
        self._inln_menu = InlMenu().get_inl_menu()
        self.__all_hotels: dict = dict()
        self.__start_index_hotel: int = -1
        self.__start_index_photo: int = -1
        self.__hotel_forward_triger: bool = True
        self.__hotel_backward_triger: bool = False
        self.__photo_backward_triger: bool = False
        self.__photo_forward_triger: bool = True
        self.__photo_list: list = []

    def getUsername(self) -> str:
        return self.__username

    def setId_user(self, iduser: int) -> None:
        self.__id_user = iduser

    def getId_user(self) -> int:
        return self.__id_user

    id_user = property(getId_user, setId_user)

    def setSearch_city(self, city: str) -> None:
        self.__search_city = city

    def getSearch_city(self) -> str:
        return self.__search_city

    search_city = property(getSearch_city, setSearch_city)

    def setId_city(self, id_city: str) -> None:
        self.__id_city = id_city

    def getId_city(self) -> str:
        return self.__id_city

    id_city = property(getId_city, setId_city)

    def setCheckIn(self, in_date: str) -> None:
        self.__checkIn = in_date

    def getCheckIn(self) -> str:
        return self.__checkIn

    checkIn = property(getCheckIn, setCheckIn)

    def setCheckOut(self, out_date: str) -> None:
        self.__checkOut = out_date

    def getCheckOut(self) -> str:
        return self.__checkOut

    checkOut = property(getCheckOut, setCheckOut)

    def setCount_show_hotels(self, count: int) -> None:
        self.__count_show_hotels = count

    def getCount_show_hotels(self) -> int:
        return self.__count_show_hotels

    count_show_hotels = property(getCount_show_hotels, setCount_show_hotels)

    def setCount_show_photo(self, count: int) -> None:
        self.__count_show_photo = count

    def getCount_show_photo(self) -> int:
        return self.__count_show_photo

    count_show_photo = property(getCount_show_photo, setCount_show_photo)

    def setDistance_min_max(self, distance: str) -> None:
        self.__distance_min_max["min_dist"] = distance.split()[0]
        self.__distance_min_max["max_dist"] = distance.split()[1]

    def getDistance_min_max(self) -> dict:
        return self.__distance_min_max

    distance_min_max = property(getDistance_min_max, setDistance_min_max)

    def setPrice_min_max(self, pr_min_max: str) -> None:
        self.__price_min_max["price_min"] = pr_min_max.split()[0]
        self.__price_min_max["price_max"] = pr_min_max.split()[1]

    def getPrice_min_max(self) -> dict:
        return self.__price_min_max

    price_min_max = property(getPrice_min_max, setPrice_min_max)

    def setCommand(self, cmnd: str) -> None:
        self.__command = cmnd

    def getCommand(self) -> str:
        return self.__command

    command = property(getCommand, setCommand)

    def setLanguage(self, hist: str) -> None:
        self.__language = hist

    def getLanguage(self) -> str:
        return self.__language

    language = property(getLanguage, setLanguage)

    def setCurrency(self, curr: str) -> None:
        self.__currency = curr

    def getCurrency(self) -> str:
        return self.__currency

    currency = property(getCurrency, setCurrency)

    def setMes_id_hotel(self, mid: int) -> None:
        self.__mes_id_hotel = mid

    def getMes_id_hotel(self) -> int:
        return self.__mes_id_hotel

    message_id_hotel = property(getMes_id_hotel, setMes_id_hotel)

    def setMes_id_photo(self, pid: int) -> None:
        self.__mes_id_photo = pid

    def getMes_id_photo(self) -> int:
        return self.__mes_id_photo

    message_id_photo = property(getMes_id_photo, setMes_id_photo)

    def getInln_menu(self) -> types.InlineKeyboardMarkup:
        return self._inln_menu

    def setInln_menu(self, markup) -> None:
        self._inln_menu = markup

    inln_menu = property(getInln_menu, setInln_menu)

    def getAllhotels(self) -> dict:
        return self.__all_hotels

    def setAllhotels(self, hotel_dict: dict) -> None:
        self.__all_hotels = hotel_dict

    all_hotels = property(getAllhotels, setAllhotels)

    def getHotel_kbd(self) -> types.InlineKeyboardMarkup:
        return self._get_hotel_kbd

    def getPhoto_yes_no(self) -> types.InlineKeyboardMarkup:
        return self.__get_photo_yes_no

    def getKbd_photo_numb(self) -> types.InlineKeyboardMarkup:
        return self.__get_kbd_photo_numb

    def getShow_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__get_show_kbd

    def getShowNoPhoto_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__get_show_no_photo_kbd


    def getHotel_forward_triger(self):
        return self.__hotel_forward_triger

    def getHotel_backward_triger(self):
        return self.__hotel_backward_triger

    def getPhoto_forward_triger(self):
        return self.__photo_forward_triger

    def setPhoto_forward_triger(self, trig):
        self.__photo_forward_triger = trig

    photo_forward_triger = property(getPhoto_forward_triger, setPhoto_forward_triger)

    def getPhoto_backward_triger(self):
        return self.__photo_backward_triger

    def setPhoto_backward_triger(self, trig):
        self.__photo_backward_triger = trig

    photo_backward_triger = property(getPhoto_backward_triger, setPhoto_backward_triger)


    def hotel_forward(self) -> str:
        """
        Функция возвращает отель по индексу

        """
        lst_hotels = list(self.__all_hotels)
        self.__start_index_photo = -1
        self.__photo_backward_triger = False
        self.__photo_forward_triger = True
        if self.__start_index_hotel < len(lst_hotels):
            self.__start_index_hotel += 1
            if self.__start_index_hotel > 0:
                self.__hotel_backward_triger = True
        else:
            self.__start_index_hotel = len(lst_hotels) - 1
            self.__hotel_forward_triger = False
        if self.__start_index_hotel == len(lst_hotels) - 1:
            self.__hotel_forward_triger = False
        hotel = lst_hotels[self.__start_index_hotel]
        self.__photo_list = self.__all_hotels[hotel]

        return hotel


    def hotel_backward(self) -> str:
        """
        Функция возвращает отель по индексу

        """
        self.__start_index_photo = -1
        self.__photo_backward_triger = False
        self.__photo_forward_triger = True
        if self.__start_index_hotel > 0:
            self.__start_index_hotel -= 1
            self.__hotel_forward_triger = True
        else:
            self.__start_index_hotel = 0
            self.__hotel_backward_triger = False
        if self.__start_index_hotel == 0:
            self.__hotel_backward_triger = False

        hotel = list(self.__all_hotels)[self.__start_index_hotel]
        self.__photo_list = self.__all_hotels[hotel]

        return hotel

    def photo_forward(self) -> str:
        """
        Функция возвращает следующее фото отеля по индексу

        """
        if self.__start_index_photo < len(self.__photo_list):
            self.__start_index_photo += 1
            if self.__start_index_photo > 0:
                self.__photo_backward_triger = True
        else:
            self.__start_index_photo = len(self.__photo_list) - 1
            self.__photo_forward_triger = False
        if self.__start_index_photo == len(self.__photo_list) - 1:
            self.__photo_forward_triger = False

        return self.__photo_list[self.__start_index_photo]

    def photo_backward(self) -> str:
        """
        Функция возвращает предыдущее фото отеля по индексу

        """
        if self.__start_index_photo > 0:
            self.__start_index_photo -= 1
            self.__photo_forward_triger = True
        else:
            self.__start_index_photo = 0
            self.__photo_backward_triger = False
        if self.__start_index_photo == 0:
            self.__photo_backward_triger = False

        return self.__photo_list[self.__start_index_photo]

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

    def getStatus_show_photo(self) -> bool:
        return self.__status_show_photo

    def setStatus_show_photo(self, status:bool):
        self.__status_show_photo = status

    status_show_photo = property(getStatus_show_photo, setStatus_show_photo)

    def getSource_dict(self):
        """Функция возвращает исходные данные для формирования запроса к API"""

        return {'id_user': self.__id_user, 'search_city':self.__search_city, 'id_city': self.__id_city,
                'checkIn': self.__checkIn, 'checkOut': self.__checkOut,
                'command': self.__command, 'count_show_hotels': self.__count_show_hotels,
                'count_show_photo': self.__count_show_photo,
                'status_show_photo': self.__status_show_photo,
                'price_min': self.__price_min_max.get('min'),
                'price_max': self.__price_min_max.get('max'),
                'distance_min': self.__distance_min_max.get('min'),
                'distance_max': self.__distance_min_max.get('max'),
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
        self.__distance_min_max: dict = dict()
        self.__language: str = ''
        self.__currency: str = ''
        self.__mes_id_hotel: int = 0
        self.__mes_id_photo: int = 0
        self.__all_hotels: dict = dict()
        self.__start_index_hotel: int = -1
        self.__start_index_photo: int = -1
        self.__hotel_forward_triger: bool = True
        self.__hotel_backward_triger: bool = False
        self.__photo_backward_triger: bool = False
        self.__photo_forward_triger: bool = True
        self.__photo_list: list = []

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



