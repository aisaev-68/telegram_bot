# -*- coding: utf-8 -*-

from handlers import types


class InlMenu:
    """ Класс инлайн кнопок для выбора количества выводимых фото
    """

    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup(row_width=1)
        self.__markup.add(types.InlineKeyboardButton(text='≡ МЕНЮ ВЫБОРА', callback_data='menu'),
                          types.InlineKeyboardButton(text='💵 Дешёвые', callback_data='/lowprice'),
                          types.InlineKeyboardButton(text='💰 Дорогие', callback_data='/highprice'),
                          types.InlineKeyboardButton(text='⭐ Лучшие', callback_data='/bestdeal'),
                          types.InlineKeyboardButton(text='🗃 История', callback_data='/history'))

    def get_inl_menu(self) -> types.InlineKeyboardMarkup:
        return self.__markup


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


class PhotoYesNo:
    """ Класс инлайн кнопок с вопросом будем ли искать фото?
    """

    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.add(types.InlineKeyboardButton(text='✅Да', callback_data='yes_photo'),
                          types.InlineKeyboardButton(text='❌Нет', callback_data='no_photo'))

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


class InlKbShow:
    """ Класс инлайн кнопок с навигацией по гостиницам и соответствущим ему фотографиям
    """

    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.row_width = 3
        self.__markup.add(types.InlineKeyboardButton(text="⬅️", callback_data='hotel_backward'),
                          types.InlineKeyboardButton(text="Гостиница", callback_data='hotel'),
                          types.InlineKeyboardButton(text="➡️", callback_data='hotel_forward'))
        self.__markup.row_width = 3
        self.__markup.add(types.InlineKeyboardButton(text="⬅️", callback_data='photo_backward'),
                          types.InlineKeyboardButton(text="Фото", callback_data='photo'),
                          types.InlineKeyboardButton(text="➡️", callback_data='photo_forward'))
        self.__markup.row_width = 1
        self.__markup.add(types.InlineKeyboardButton(text="≡ Меню", callback_data='kb_menu'))

    def get_show_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__markup


class InlKbShowNoPhoto:
    """ Класс инлайн кнопок с навигацией по гостиницам
    """

    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__markup.row_width = 3
        self.__markup.add(types.InlineKeyboardButton(text="⬅️", callback_data='hotel_backward'),
                          types.InlineKeyboardButton(text="Гостиница", callback_data='hotel'),
                          types.InlineKeyboardButton(text="➡️", callback_data='hotel_forward'))
        self.__markup.row_width = 1
        self.__markup.add(types.InlineKeyboardButton(text="Меню", callback_data='kb_menu'))

    def get_show_kbd(self) -> types.InlineKeyboardMarkup:
        return self.__markup
