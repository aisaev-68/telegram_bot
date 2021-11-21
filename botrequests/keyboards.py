from telebot import types

class PhotoYesNo:
    """ Класс кнопок с вопросом будем ли искать фото?
    """
    def __init__(self) -> None:
        self.__markup = types.InlineKeyboardMarkup()
        self.__yes_photo_hotels = types.InlineKeyboardButton(text='✅Да', callback_data='yes_photo')
        self.__no_photo_hotels = types.InlineKeyboardButton(text='❌Нет', callback_data='no_photo')
        self.__markup.add(self.__yes_photo_hotels, self.__no_photo_hotels)

    def get_photo_yes_no(self):
        return self.__markup


class InlKbPhoto:
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

    def getkbd(self):
        return self.__markup

