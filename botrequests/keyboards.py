# -*- coding: utf-8 -*-

from telebot import types

class HotelKbd:
    """ Класс для выводы количества гостиниц
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


class PhotoYesNo:
    """ Класс кнопок с вопросом будем ли искать фото?
    """
    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.add(types.InlineKeyboardButton(text='✅Да', callback_data='yes_photo'),
                          types.InlineKeyboardButton(text='❌Нет', callback_data='no_photo'))

    def get_photo_yes_no(self) -> types.InlineKeyboardMarkup:
        return self.__markup


class PhotoNumbKbd:
    """ Класс для выбора количества выводимых фото
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


class InlKbShow:
    """ Класс кнопок с навигацией по гостиницам и соответствущим ему фотографиям
       """
    def __init__(self):
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.row_width = 3
        self.__markup.add(types.InlineKeyboardButton(text="⬅️", callback_data='hotel_backward'),
                          types.InlineKeyboardButton(text="Гостиница", callback_data='hotel'),
                          types.InlineKeyboardButton(text="➡️", callback_data='hotel_forward'))
        self.__markup.row_width = 3
        self.__markup.add(types.InlineKeyboardButton(text="⬅️", callback_data='photo_backward'),
                          types.InlineKeyboardButton(text="Фото", callback_data='photo'),
                          types.InlineKeyboardButton(text="➡️", callback_data='photo_forward'))

    def get_show_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__markup

class InlKbShowNoPhoto:
    """ Класс кнопок с навигацией по гостиницам и соответствущим ему фотографиям
       """
    def __init__(self):
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.row_width = 3
        self.__markup.add(types.InlineKeyboardButton(text="⬅️", callback_data='hotel_backward'),
                          types.InlineKeyboardButton(text="Гостиница", callback_data='hotel'),
                          types.InlineKeyboardButton(text="➡️", callback_data='hotel_forward'))

    def get_show_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__markup

class StartKbd:

    def __init__(self):
        self.__markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True)
        self.__markup_start.row(types.KeyboardButton('/help'), types.KeyboardButton('/start'),
                                types.KeyboardButton('/lowprice'), types.KeyboardButton('/history'))

    def get_start_kbd(self) -> types.ReplyKeyboardMarkup:
        return self.__markup_start