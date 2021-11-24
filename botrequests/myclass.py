from telegram_bot_calendar import WMonthTelegramCalendar, DAY
import datetime
import requests
from decouple import config
import json


class Users:
    """
    Класс пользователя, с параметрами необходимые для формирования запроса.
        Args: user: объект вх. сообщения от пользователя
    """
    commands = ["/lowprice", "/highprice", "/bestdeal", "/history"]

    loc_txt = {'ru_RU': ['Рейтинг:', 'Название отеля:', 'Адрес:', 'Удаленность от центра города:', 'Дата въезда:',
                         'Дата выезда', 'Стоимость за сутки (в руб):', 'Стоимость за {} сутки (в руб):'],
               'en_US': [
                   'Rating:', 'The name of the hotel:', 'Address:', 'Distance from the city center:', 'Arrival date:',
                   'Date of departure:', 'Cost per day (USD):', 'Price for {} day (USD):'
               ]}

    def __init__(self, user) -> None:
        self.__username: str = user.from_user.username
        self.__id_user: int = user.from_user.id
        self.__search_city: str = user.text
        self.__search_hotels: int = 0
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
        self.__index_hotel: list = [0]
        self.__index_photo: list = [0]
        self.__mes_id_hotel: int = 0
        self.__mes_id_photo: int = 0

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

    def setSearch_hotels(self, numb: int) -> None:
        self.__search_hotels = numb

    def getSearch_hotels(self) -> int:
        return self.__search_hotels

    search_hotels = property(getSearch_hotels, setSearch_hotels)

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

    def setCurrency(self, curr: str) -> None:
        self.__currency = curr

    def getCurrency(self) -> str:
        return self.__currency

    currency = property(getCurrency, setCurrency)

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

    def setIndex_hotel(self, ind: int) -> None:
        self.__index_hotel[0] += ind

    def getIndex_hotel(self) -> int:
        if self.__index_hotel[0] >= self.__search_hotels:
            self.__index_hotel[0] = self.__search_hotels - 1
        elif self.__index_hotel[0] < 0:
            self.__index_hotel[0] = 0

        return self.__index_hotel[0]

    index_hotel = property(getIndex_hotel, setIndex_hotel)

    def setIndex_photo(self, ind: int) -> None:

        self.__index_photo[0] += ind

    def getIndex_photo(self) -> int:
        return self.__index_photo[0]

    index_photo = property(getIndex_photo, setIndex_photo)

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

    def h_forward_backward(self):
        """
        Функция возвращает отель по индексу

        """
        hotels_lst = list(self.__all_hotels.keys())
        self.getIndex_hotel()
        print(self.__index_hotel[0])
        return hotels_lst[self.__index_hotel[0]]

    def p_forward_backward(self):
        """
        Функция возвращает список фото отеля по индексу

        """
        hotel = self.h_forward_backward()
        photos_lst = self.__all_hotels[hotel]
        if 0 <= self.__index_photo[0] <= self.__count_show_photo:
            return photos_lst[self.__index_photo[0]]

    def diff_date(self) -> None:
        """
        Функция определения количества суток проживания
        :return: возвращает количество суток
        """
        a = self.__checkIn.split('-')
        b = self.__checkOut.split('-')
        d = str(datetime.date(int(b[0]), int(b[1]), int(b[2])) - datetime.date(int(a[0]), int(a[1]), int(a[2])))
        self.__diff_date = int(d.split()[0])

    def getDiff_date(self) -> int:
        """Функция возвращает количество суток проживания (целое число)

        """
        return self.__diff_date

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

    def req_api(self, url, querystring):

        """
        Функция возвращает данные запроса к API гостиниц.
        :param url: страница поиска
        :param querystring: срока запроса
        :return data: возвращаемые данные
        """

        headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': config('RAPID_API_KEY')
        }
        response = requests.request("GET", url, headers=headers, params=querystring)
        if response.status_code == 200:
            data = json.loads(response.text)
            return data
        else:
            return None

    def low_price(self, querystring: dict):
        """
            Формирует словарь отелей на основе запроса пользователя и сортировкой по цене.
            Если отелей не найдено возвращает пустой словарь.
            :param querystring: строка запроса
            :return result_low: возвращает словарь (название отеля, адрес,
            фотографии отеля (если пользователь счёл необходимым их вывод)
            """

        url_low = config('URL_LOW')
        hotels_dict = {}
        low_data = self.req_api(url_low, querystring)
        loc = self.language
        # TypeError: 'NoneType' object is not subscriptable
        count = 0
        print(low_data)
        for hotel_count, results in enumerate(low_data['data']['body']['searchResults']['results']):
            summa = float(self.getDiff_date()) * results["ratePlan"]["price"]["exactCurrent"]
            count += 1
            if self.count_show_hotels != hotel_count:
                txt = f'⭐⭐⭐{self.loc_txt[loc][0]} {(results.get("starRating")) if results.get("starRating") else "--"}⭐⭐⭐\n' \
                      f'🏨 {self.loc_txt[loc][1]} {results["name"]}\n' \
                      f'      {self.loc_txt[loc][2]} {results["address"].get("countryName")}, {results["address"].get("locality")}\n' \
                      f'      {(results["address"].get("streetAddress") if results["address"].get("streetAddress") else "Нет данных об адресе...")}\n' \
                      f'🚗 {self.loc_txt[loc][3]} {results["landmarks"][0]["distance"]}\n' \
                      f'📅 {self.loc_txt[loc][4]} {self.checkIn}\n' \
                      f'📅 {self.loc_txt[loc][5]} {self.checkOut}\n' \
                      f'💵 {self.loc_txt[loc][6]} {(results["ratePlan"]["price"]["exactCurrent"]) if results["ratePlan"]["price"]["exactCurrent"] else "Нет данных о расценках..."}\n' \
                      f'💵 {self.loc_txt[loc][7].format(self.getDiff_date())} {summa if results["ratePlan"]["price"]["exactCurrent"] else "Нет данных о расценках..."}\n' \
                      f'🌍 Ссылка https://ru.hotels.com/ho{results["id"]}'
                data_photo = self.get_photos(results['id'])
                photo_lst = []
                for index, photo in enumerate(data_photo):
                    if self.count_show_photo != index:
                        photo_lst.append(photo)
                    else:
                        break
                hotels_dict[txt] = photo_lst

        self.__search_hotels = count
        self.__all_hotels = hotels_dict

        with open('hotel.json', 'w') as f:
            json.dump(self.all_hotels, f, indent=4)

    def get_city_id(self) -> str:
        """
        Функция возвращает ID города. Если город не найден, возвращает пустую строку.
        querystring: строка запроса в виде словаря
        {"query": 'Москва', "locale": 'ru_RU'}
        """
        querystring = {"query": self.__search_city, "locale": self.__language}
        url = config('URL')

        result_locations_search = self.req_api(url, querystring)
        destination_id = None
        # TypeError: 'NoneType' object is not subscriptable
        for group in result_locations_search['suggestions']:
            if group['group'] == 'CITY_GROUP':
                if group['entities']:
                    destination_id = group['entities'][0]['destinationId']
                    break
        return destination_id

    def get_photos(self, id_photo):
        """
        Функция возвращает список ссылок на фотографии отеля. Если не найдены, возвращает пустой список.
        :param id_photo: ID отеля
        :return photo_list: список ссылок на фотографии отеля
        """

        url = config('URL_PHOTOS')
        querystring = {"id": f"{id_photo}"}
        response = self.req_api(url, querystring)
        print(response["roomImages"])
        photo_list = []
        for photo in response["roomImages"]:
            for img in photo['images']:
                photo_list.append(img['baseUrl'].replace('{size}', 'z'))
        print(photo_list)
        return photo_list

    def __str__(self):

        txt = f"username: {self.__username}\nid_user: {self.__id_user:}\n" \
              f"search_city: {self.__search_city}\nid_city: {self.__id_city}\n" \
              f"checkIn: {self.__checkIn}\ncheckOut: {self.__checkOut:}\n" \
              f"count_show_hotels: {self.__count_show_hotels}\n" \
              f"count_show_photo: {self.__count_show_photo}\nlanguage: {self.__language}\n" \
              f"currency: {self.__currency}\ndiff_date: {self.__diff_date}\ncommand: {self.__command}" \
              f"search_hotels: {self.__search_hotels}"
        return txt


class MyStyleCalendar(WMonthTelegramCalendar):
    """ Класс календаря
    """
    prev_button = "⬅️"
    next_button = "➡️"
    first_step = DAY
