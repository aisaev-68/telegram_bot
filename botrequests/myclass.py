from telegram_bot_calendar import WMonthTelegramCalendar, DAY
import datetime




class Users:
    """
    Класс пользователя, с параметрами необходимые для формирования запроса.
        Args: user: объект вх. сообщения от пользователя
    """
    commands = ["/lowprice", "/highprice", "/bestdeal", "/history"]

    def __init__(self, user) -> None:
        self.__username: str = user.from_user.username
        self.__id_user: int = user.from_user.id
        self.__search_city: str = user.text
        self.__id_city: str = ''
        self.__checkIn: str = ''
        self.__checkOut: str = ''
        self.__cache_data = None
        self.__count_show_hotels: int = 0
        self.__all_hotels: dict = dict()
        self.__count_show_photo: int = 0
        self.__status_show_foto: bool = False
        self.__price_min_max: dict = dict()
        self.__distance_min_max: dict = dict()
        self.__history: dict = dict()
        self.__language: str = ''
        self.__currency: str = ''
        self.__diff_date: int = 0
        self.__command: str = ''

    def setUsername(self, nameuser: str) -> None:
        self.__username = nameuser

    def getUsername(self) -> str:
        return self.__username

    username = property(getUsername, setUsername)

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

    checkOut = property(getCheckIn, setCheckOut)

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

    def setHistory(self, hist):
        self.__history["history"] = hist

    def getHistory(self) -> dict:
        return self.__history

    history = property(getHistory, setHistory)

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

    # def setPhotos_hotel(self, photos: list) -> None:
    #     self.__photos_hotel = photos
    #
    # def getPhotos_hotel(self) -> list:
    #     return self.__photos_hotel
    #
    # photos_hotel = property(getPhotos_hotel, setPhotos_hotel)

    def setAll_hotels(self, hotels: dict) -> None:
        self.__all_hotels = hotels

    def getAll_hotels(self) -> dict:
        return self.__all_hotels

    all_hotels = property(getAll_hotels, setAll_hotels)

    def setStatus_show_photo(self, stat: bool) -> None:
        self.__status_show_foto = stat

    def getStatus_show_photo(self) -> bool:
        """
        Функция определения состояния вывода фото
        :return: возвращает булево (True, False) значение состояния вывода фото
        """
        return self.__status_show_foto

    status_show_foto = property(getStatus_show_photo, setStatus_show_photo)

    def diff_date(self) -> None:
        """
        Функция определения количества суток проживания
        :return: возвращает количество суток
        """
        a = self.__checkIn
        b = self.__checkOut
        d = str(datetime.date(int(b[0]), int(b[1]), int(b[2])) - datetime.date(int(a[0]), int(a[1]), int(a[2])))
        self.__diff_date = int(d)

    def getDiff_date(self) -> int:
        """Функция возвращает количество суток проживания (целое число)

        """
        return self.__diff_date

    def create_idcity_query(self) -> dict:
        """Функция возвращает строку запроса к API для получения ID города
        в формате словаря {"query": "Москва","locale": "ru_RU"}

        """
        return {"query": self.__search_city, "locale": self.__language}

    def queryAPI(self, command) -> dict:
        """Функция формирует строку запроса в виде словаря
        :param command: команды от пользователя /lowprice, /highprice, /bestdeal
        возвращает строку запроса к API в виде словаря
        querystring= {
                "destinationId": self.__id_city,
                "pageNumber": "1",
                "pageSize": self.__count_show_hotels",
                "checkIn": self.__checkIn,
                "checkOut": self.__checkOut,
                "adults1": "1",
                "sortOrder": "PRICE",
                "locale": self.__language,
                "currency": self.__currency
            }

        """
        querystring = None
        if self.commands[0] == command:
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
        if self.commands[1] == command:
            pass
        if self.commands[2] == command:
            pass

        return querystring


class MyStyleCalendar(WMonthTelegramCalendar):
    """ Класс календаря
    """
    prev_button = "⬅️"
    next_button = "➡️"
    first_step = DAY



class Hotel:

    def __init__(self, name_hotel: str = None, countryName: str = None,
                 locality: str = None, streetAddress: str = None,
                 distance: str = None, current: str = None, max_price: str = None, min_price: str = None):

        self.__name_hotel = name_hotel
        self.__countryName = countryName
        self.__locality = locality
        self.__streetAddress = streetAddress
        self.__distance = distance
        self.__current = current
        self.__priceMax = max_price
        self.__priceMin = min_price
        self.__photo = []

    def setPhoto(self, photo_hotel):
        self.__photo.append(photo_hotel)

    def getPhoto(self):
        return self.__photo

    photo = property(getPhoto, setPhoto)

    def setName(self, name_hotel):
        self.__name_notel = name_hotel

    def getName(self):
        return self.__name_notel

    name_hotel = property(getName, setName)

    def setCountry(self, countryName):
        self.__countryName = countryName

    def getCountry(self):
        return self.__countryName

    country_Name = property(getCountry, setCountry)


    def setLocality(self, locality):
        self.__locality = locality

    def getLocality(self):
        return self.__locality

    locality = property(getLocality, setLocality)


    def setstreetAddress(self, streetAddress):
        self.__streetAddress = streetAddress

    def getstreetAddress(self):
        return self.__streetAddress

    streetAddress = property(getstreetAddress, setstreetAddress)

    def setdistance(self, distance):
        self.__distance = distance

    def getdistance(self):
        return self.__distance

    distance = property(getdistance, setdistance)

    def setcurrent(self, current):
        self.__current = current

    def getcurrent(self):
        return self.__current

    current = property(getcurrent, setcurrent)