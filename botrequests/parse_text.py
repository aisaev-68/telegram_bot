# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup


def price_parse(line_text: dict, lang: str, logging, datetime) -> dict:
    """Функция возвращает из полученной строки кол-во дней, общаую сумму и цену за сутки в виде словаря
    {'day': day, 'price_total': price_total, 'price_day': price_day}
    :param line_text: строка для парсинга
    :param lang: язык пользователя
    :param logging: модуль logging
    :param datetime: модуль datetime"""
    if lang == 'ru_RU':
        try:
            day = line_text['price']['info'].split()[4]
            price_total = line_text['price']['exactCurrent']
            price_day = round(price_total / float(day), 2)
            return {'day': day, 'price_total': price_total, 'price_day': price_day}
        except Exception as er:
            logging.error(f"{datetime.now()} - {er} - Функция price_parse (русский язык)")
    else:
        try:
            day = BeautifulSoup(line_text['price']['fullyBundledPricePerStay'], 'html.parser').get_text().split()[3]
            price_total = \
            BeautifulSoup(line_text['price']['fullyBundledPricePerStay'], 'html.parser').get_text().split()[1][
            1:].replace(',', '')
            print(BeautifulSoup(line_text['price']['fullyBundledPricePerStay'], 'html.parser'))
            price_day = round(float(price_total) / float(day), 2)
            return {'day': day, 'price_total': price_total, 'price_day': price_day}
        except Exception as er:
            logging.error(f"{datetime.now()} - {er} - Функция price_parse (английски язык)")


def city_parse(line_text: str) -> str:
    """Функци возвращает из полученной строки названия города и региона
    :param line_text: срока для парсинга
    """

    return BeautifulSoup(line_text, 'html.parser').get_text().lower()
