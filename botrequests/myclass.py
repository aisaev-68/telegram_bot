from telebot import types
from telegram_bot_calendar import WMonthTelegramCalendar, DAY


class MyStyleCalendar(WMonthTelegramCalendar):
    """ Класс календаря
    """
    prev_button = "⬅️"
    next_button = "➡️"
    first_step = DAY


class PhotoYesNo:
    """ Класс кнопок с вопросом будем ли искать фото?
    """
    def __init__(self):
        self.__markup = types.InlineKeyboardMarkup()
        self.__yes_photo_hotels = types.InlineKeyboardButton(text='✅Да', callback_data='yes_photo')
        self.__no_photo_hotels = types.InlineKeyboardButton(text='❌Нет', callback_data='no_photo')
        self.__markup.add(self.__yes_photo_hotels, self.__no_photo_hotels)

    def get_photo_yes_no(self):
        return self.__markup


class InlKbPhoto:
    def __init__(self):
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.row_width = 6
        self.__hotel_backward = types.InlineKeyboardButton(text="⬅️", callback_data='hotel_backward')
        self.__hotel = types.InlineKeyboardButton(text="Гостиница", callback_data='hotel')
        self.__hotel_forward = types.InlineKeyboardButton(text="➡️", callback_data='hotel_forward')

        self.__photo_backward = types.InlineKeyboardButton(text="⬅️", callback_data='photo_backward')
        self.__photo = types.InlineKeyboardButton(text="Фото", callback_data='photo')
        self.__photo_forward = types.InlineKeyboardButton(text="➡️", callback_data='photo_forward')
        self.__markup.add(self.__hotel_backward, self.__hotel, self.__hotel_forward,
                          self.__photo_backward, self.__photo, self.__photo_forward)

    def getkbd(self):
        return self.__markup


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