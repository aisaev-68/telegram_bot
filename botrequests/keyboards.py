# -*- coding: utf-8 -*-

from telebot import types

hotel_kbd = {'ru_RU': ['Да', 'Нет', 'Отмена'], 'en_US': ['Yes', 'No', 'Cancel']}

commands_bot = {
    "ru_RU": {
        "lowprice": "Поиск дешевых отелей",
        "highprice": "Поиск отелей класса люкс", "bestdeal": "Поиск лучших отелей",
        "history": "Показать историю запросов", "help": "Помощь"},
    "en_US": {
        "lowprice": "Search for cheap hotels",
        "highprice": "Search for luxury hotels", "bestdeal": "Search for the best hotels",
        "history": "Show request history", "help": "Help"}}


class Keyboard:
    """ Класс инлайн кнопок и метод my_commands
    """

    def __init__(self) -> None:
        self.__markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

    def set_lang(self) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок с выбора языка?
        """
        self.__markup.add(types.InlineKeyboardButton(text='✅Russian', callback_data='ru_RU'),
                          types.InlineKeyboardButton(text='✅English', callback_data='en_US'))
        return self.__markup

    def hotel_numb(self, lang: str) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок для выводы количества гостиниц
        """
        self.__markup.row_width = 5
        self.__markup.add(types.InlineKeyboardButton(text='5', callback_data='five'),
                          types.InlineKeyboardButton(text='10', callback_data='ten'),
                          types.InlineKeyboardButton(text='15', callback_data='fifteen'),
                          types.InlineKeyboardButton(text='20', callback_data='twenty'),
                          types.InlineKeyboardButton(text='25', callback_data='twenty_five'))
        self.__markup.row_width = 1
        self.__markup.add(types.InlineKeyboardButton(text=hotel_kbd[lang][2], callback_data='Cancel_process'))
        return self.__markup

    def photo_yes_no(self, lang: str) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок с вопросом будем ли искать фото?
        """
        self.__markup.add(types.InlineKeyboardButton(text='✅' + hotel_kbd[lang][0], callback_data='yes_photo'),
                          types.InlineKeyboardButton(text='❌' + hotel_kbd[lang][1], callback_data='no_photo'),
                          types.InlineKeyboardButton(text=hotel_kbd[lang][2], callback_data='Cancel_process'))
        return self.__markup

    def photo_numb(self, lang: str) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок для выбора количества выводимых фото
        """
        self.__markup.row_width = 5
        self.__markup.add(types.InlineKeyboardButton(text='1', callback_data='one_photo'),
                          types.InlineKeyboardButton(text='2', callback_data='two_photo'),
                          types.InlineKeyboardButton(text='3', callback_data='three_photo'),
                          types.InlineKeyboardButton(text='4', callback_data='four_photo'),
                          types.InlineKeyboardButton(text='5', callback_data='five_photo'))
        self.__markup.row_width = 1
        self.__markup.add(types.InlineKeyboardButton(text=hotel_kbd[lang][2], callback_data='Cancel_process'))
        return self.__markup

    def requests_numb(self, lang: str) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок для выбора количества выводимых фото
        """
        self.__markup.row_width = 5
        self.__markup.add(types.InlineKeyboardButton(text='1', callback_data='one_req'),
                          types.InlineKeyboardButton(text='2', callback_data='two_req'),
                          types.InlineKeyboardButton(text='3', callback_data='three_req'),
                          types.InlineKeyboardButton(text='4', callback_data='four_req'),
                          types.InlineKeyboardButton(text='5', callback_data='five_req'))
        self.__markup.row_width = 1
        self.__markup.add(types.InlineKeyboardButton(text=hotel_kbd[lang][2], callback_data='Cancel_process'))
        return self.__markup

    @classmethod
    def my_commands(cls, lng: str) -> [types.BotCommand]:
        """ Функция возвращает каманды на языке пользователя
        """

        return [types.BotCommand("lowprice", commands_bot[lng]["lowprice"]),
                types.BotCommand("highprice", commands_bot[lng]["highprice"]),
                types.BotCommand("bestdeal", commands_bot[lng]["bestdeal"]),
                types.BotCommand("history", commands_bot[lng]["history"]),
                types.BotCommand("help", commands_bot[lng]["help"])]
