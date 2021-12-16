# -*- coding: utf-8 -*-

from botrequests.locales import loc, hotel_kbd, commands_bot
from telebot import types


class Keyboard:
    """ Класс инлайн кнопок и метод my_commands
    """

    def __init__(self):
        self.__markup: types.InlineKeyboardMarkup = types.InlineKeyboardMarkup()

    def set_lang(self):
        """ Функция инлайн кнопок с выбора языка?
        """
        self.__markup.add(types.InlineKeyboardButton(text='✅Russian', callback_data='ru_RU'),
                          types.InlineKeyboardButton(text='✅English', callback_data='en_US'))
        return self.__markup

    def hotel_numb(self, lang) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок для выводы количества гостиниц
        """
        self.__markup.row_width = 5
        self.__markup.add(types.InlineKeyboardButton(text='5', callback_data='five'),
                          types.InlineKeyboardButton(text='10', callback_data='ten'),
                          types.InlineKeyboardButton(text='15', callback_data='fifteen'),
                          types.InlineKeyboardButton(text='20', callback_data='twenty'),
                          types.InlineKeyboardButton(text='25', callback_data='twenty_five'))
        self.__markup.row_width = 1
        self.__markup.add(types.InlineKeyboardButton(text=loc[lang][0], callback_data='Cancel_process'))
        return self.__markup

    def photo_yes_no(self, lang) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок с вопросом будем ли искать фото?
        """
        self.__markup.add(types.InlineKeyboardButton(text='✅' + hotel_kbd[lang][0], callback_data='yes_photo'),
                          types.InlineKeyboardButton(text='❌' + hotel_kbd[lang][1], callback_data='no_photo'),
                          types.InlineKeyboardButton(text=loc[lang][0], callback_data='Cancel_process'))
        return self.__markup

    def photo_numb(self, lang) -> types.InlineKeyboardMarkup:
        """ Функция инлайн кнопок для выбора количества выводимых фото
        """
        self.__markup.row_width = 5
        self.__markup.add(types.InlineKeyboardButton(text='1', callback_data='one_photo'),
                          types.InlineKeyboardButton(text='2', callback_data='two_photo'),
                          types.InlineKeyboardButton(text='3', callback_data='three_photo'),
                          types.InlineKeyboardButton(text='4', callback_data='four_photo'),
                          types.InlineKeyboardButton(text='5', callback_data='five_photo'))
        self.__markup.row_width = 1
        self.__markup.add(types.InlineKeyboardButton(text=loc[lang][0], callback_data='Cancel_process'))
        return self.__markup

    @classmethod
    def my_commands(cls, lng) -> [types.BotCommand]:
        """ Функция возвращает каманды на языке пользователя
        """

        return [types.BotCommand("lowprice", commands_bot[lng]["lowprice"]),
                types.BotCommand("highprice", commands_bot[lng]["highprice"]),
                types.BotCommand("bestdeal", commands_bot[lng]["bestdeal"]),
                types.BotCommand("history", commands_bot[lng]["history"]),
                types.BotCommand("help", commands_bot[lng]["help"])]