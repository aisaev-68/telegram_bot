# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from requests_api import req_api, config
from handlers import types


def get_city_id(user: dict, message: types.Message, bot) -> bool:
    """
    Функция выводит в чат города.
    :param user: словарь с данными пользователя
    :param message: сообщение
    :param bot: bot
    """
    lang = user[message.chat.id].language
    loc = {'ru_RU':
               ['Отмена', 'Пожалуйста, уточните город', 'Превышена ежемесячная квота для запросов по плану BASIC.'],
           'en_US':
               ['Cancel', 'Please specify city', 'Monthly quota exceeded for BASIC plan requests.']
           }

    l_txt = loc[lang]
    search_city = user[message.chat.id].search_city
    querystring = {"query": search_city, "locale": lang}
    result_id_city = req_api(config('URL'), querystring, lang)

    if isinstance(result_id_city, dict) and not result_id_city.get("message"):
        if len(result_id_city) > 0:
            markup = types.InlineKeyboardMarkup()
            for city in result_id_city['suggestions']:
                for name in city['entities']:
                    parse_city = (BeautifulSoup(name['caption'], 'html.parser').get_text()).lower()
                    if parse_city.startswith(search_city) and name['type'] == 'CITY':
                        # Добавить для точного совпадения and name['name'].lower() == search_city
                        markup.add(types.InlineKeyboardButton(parse_city.title(),
                                                              callback_data='cbid_' + str(name['destinationId'])))
            markup.add(types.InlineKeyboardButton(l_txt[0],
                                                  callback_data='Cancel_process'))
            bot.edit_message_text(text=l_txt[1], chat_id=message.chat.id,
                                  message_id=user[message.chat.id].message_id,
                                  parse_mode='HTML', reply_markup=markup)
            return True
        else:
            return False
    elif result_id_city.get("message"):
        bot.edit_message_text(text=l_txt[2],
                              chat_id=message.chat.id, message_id=user[message.chat.id].message_id)
        return True

    else:
        bot.send_message(message.chat.id, result_id_city)
        return True
