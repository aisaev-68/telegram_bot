# -*- coding: utf-8 -*-

from handlers import types
from locales import hotel_kbd


class HotelKbd:
    """ Класс инлайн кнопок для выводы количества гостиниц
    """

    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup(row_width=5)
        self.__markup.add(types.InlineKeyboardButton(text='5', callback_data='five'),
                          types.InlineKeyboardButton(text='10', callback_data='ten'),
                          types.InlineKeyboardButton(text='15', callback_data='fifteen'),
                          types.InlineKeyboardButton(text='20', callback_data='twenty'),
                          types.InlineKeyboardButton(text='25', callback_data='twenty_five'))

    def get_hotel_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__markup

class Lang:
    """ Класс инлайн кнопок с вопросом будем ли искать фото?
    """

    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.add(types.InlineKeyboardButton(text='✅Russian', callback_data='ru_RU'),
                          types.InlineKeyboardButton(text='✅English', callback_data='en_US'))

    def get_langkb(self) -> types.InlineKeyboardMarkup:
        return self.__markup

class PhotoYesNo:
    """ Класс инлайн кнопок с вопросом будем ли искать фото?
    """

    def __init__(self, loc='ru_RU') -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.add(types.InlineKeyboardButton(text='✅' + hotel_kbd[loc][5], callback_data='yes_photo'),
                          types.InlineKeyboardButton(text='❌' + hotel_kbd[loc][6], callback_data='no_photo'))

    def get_photo_yes_no(self) -> types.InlineKeyboardMarkup:
        return self.__markup


class PhotoNumbKbd:
    """ Класс инлайн кнопок для выбора количества выводимых фото
    """

    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup(row_width=5)
        self.__markup.add(types.InlineKeyboardButton(text='1', callback_data='one_photo'),
                          types.InlineKeyboardButton(text='2', callback_data='two_photo'),
                          types.InlineKeyboardButton(text='3', callback_data='three_photo'),
                          types.InlineKeyboardButton(text='4', callback_data='four_photo'),
                          types.InlineKeyboardButton(text='5', callback_data='five_photo'))

    def get_kbd_photo_numb(self) -> types.InlineKeyboardMarkup:
        return self.__markup


