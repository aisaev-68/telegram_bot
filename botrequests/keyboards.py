from telebot import types

class HotelKbd:
    """ Класс для выводы количества гостиниц
    """
    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup(row_width=5)
        self.__five_hotels = types.InlineKeyboardButton(text='5', callback_data='five')
        self.__ten_hotels = types.InlineKeyboardButton(text='10', callback_data='ten')
        self.__fifteen_hotels = types.InlineKeyboardButton(text='15', callback_data='fifteen')
        self.__twenty_hotels = types.InlineKeyboardButton(text='20', callback_data='twenty')
        self.__twenty_five_hotels = types.InlineKeyboardButton(text='25', callback_data='twenty_five')
        self.__markup.add(self.__five_hotels, self.__ten_hotels, self.__fifteen_hotels,
                          self.__twenty_hotels, self.__twenty_five_hotels)

    def get_hotel_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__markup


class PhotoYesNo:
    """ Класс кнопок с вопросом будем ли искать фото?
    """
    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__yes_photo_hotels = types.InlineKeyboardButton(text='✅Да', callback_data='yes_photo')
        self.__no_photo_hotels = types.InlineKeyboardButton(text='❌Нет', callback_data='no_photo')
        self.__markup.add(self.__yes_photo_hotels, self.__no_photo_hotels)

    def get_photo_yes_no(self) -> types.InlineKeyboardMarkup:
        return self.__markup


class PhotoNumbKbd:
    """ Класс для выбора количества выводимых фото
    """
    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup(row_width=5)
        self.__one_photo = types.InlineKeyboardButton(text='1', callback_data='one_photo')
        self.__two_photo = types.InlineKeyboardButton(text='2', callback_data='two_photo')
        self.__three_photo = types.InlineKeyboardButton(text='3', callback_data='three_photo')
        self.__four_photo = types.InlineKeyboardButton(text='4', callback_data='four_photo')
        self.__five_photo = types.InlineKeyboardButton(text='5', callback_data='five_photo')
        self.__markup.add(self.__one_photo, self.__two_photo, self.__three_photo,
                          self.__four_photo, self.__five_photo)

    def get_kbd_photo_numb(self) -> types.InlineKeyboardMarkup:
        return self.__markup


class InlKbShow:
    """ Класс кнопок с навигацией по гостиницам и соответствущим ему фотографиям
       """
    def __init__(self):
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.row_width = 3
        self.__hotel_backward = types.InlineKeyboardButton(text="⬅️", callback_data='hotel_backward')
        self.__hotel = types.InlineKeyboardButton(text="Гостиница", callback_data='hotel')
        self.__hotel_forward = types.InlineKeyboardButton(text="➡️", callback_data='hotel_forward')
        self.__markup.add(self.__hotel_backward, self.__hotel, self.__hotel_forward)
        self.__markup.row_width = 3
        self.__photo_backward = types.InlineKeyboardButton(text="⬅️", callback_data='photo_backward')
        self.__photo = types.InlineKeyboardButton(text="Фото", callback_data='photo')
        self.__photo_forward = types.InlineKeyboardButton(text="➡️", callback_data='photo_forward')
        self.__markup.add(self.__photo_backward, self.__photo, self.__photo_forward)

    def get_show_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__markup

