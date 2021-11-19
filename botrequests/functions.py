from . import lowprice
import requests
import json
import re
from .myclass import MyStyleCalendar, PhotoYesNo, InlKbPhoto
from dotenv import dotenv_values
from telebot import TeleBot, types


config = dotenv_values(".env")
bot = TeleBot(config['TELEGRAM_API_TOKEN'])

data = {}

LSTEP = {
    'ru':
        {'y': 'год', 'm': 'месяц', 'd': 'день'},
    'en':
        {'y': 'year', 'm': 'month', 'd': 'day'}
}





def local_leng(txt: str) -> str:
    """
    Функция определения языка (локали), для GET запроса
    :param txt: текст, с названием города из бота
    :return: возвращает 'en_US' или 'ru_RU'
    """
    if re.findall(r'[А-Яа-яЁё -]', re.sub(r'[- ]', '', txt)):
        return "ru_RU"
    else:
        return "en_US"


def req(url, querystring):
    """
    Функция возвращает данные запроса к API гостиниц.
    :param url: страница поиска
    :param querystring: срока запроса
    :param headers: Словарь заголовков HTTP для отправки с помощью `Request`.
    :return data: возвращаемы данные
    """

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': config['RAPID_API_KEY']
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return None


def get_city_id(querystring: dict) -> str:
    """
    Функция возвращает ID города. Если город не найден, возвращает пустую строку.
    :param txt: название города, введённое пользователем бота
    :param local: язык поиска
    :return destination_id: id города
    """

    url = config['URL']

    result_locations_search = req(url, querystring)
    destination_id = None
    for group in result_locations_search['suggestions']:
        if group['group'] == 'CITY_GROUP':
            if group['entities']:
                destination_id = group['entities'][0]['destinationId']
                break
    return destination_id


def get_photos(id_photo):
    """
    Функция возвращает ID города. Если город не найден, возвращает пустую строку.
    :param id_photo: название города, введённое пользователем бота
    :param local: язык поиска
    :return destination_id: id города
    """

    url = config['URL_PHOTOS']
    querystring = {"id": f"{id_photo}"}
    response = req(url, querystring)
    data_photo = json.loads(response.text)

    with open('get_hotel_photos.json', 'w', encoding='utf-8') as file:
        json.dump(data_photo, file, ensure_ascii=False, indent=4)

    return data_photo


def next_step_city(mess, chat_id):
    """
    Функция проверки на корректность ввода названия города.
    В случае корректного ввода города прелагает ввести дату въезда в гостиницу.
    :param mess: объект входящего сообщения от пользователя
    """
    data['chat_id'] = chat_id
    if len(re.findall(r'[А-Яа-яЁёa-zA-Z0-9 -]+', mess.text)) > 1:
        err_city = bot.send_message(mess.chat.id,
                                    'Город должен содержать только буквы, вводи еще раз город.')
        bot.register_next_step_handler(err_city, next_step_city)
    else:
        data['query'] = mess.text
        data['locale'] = local_leng(mess.text)

        if data['locale'] == 'ru_RU':
            data['currency'] = 'RUB'
        else:
            data['currency'] = 'USD'

        idcity = get_city_id(data)
        print(data)
        if idcity is not None:
            data['destinationId'] = idcity
            bot.send_message(mess.chat.id,
                             "Выберите дату въезда",
                             reply_markup=MyStyleCalendar(calendar_id=1).build()[0])
        else:
            data.clear()
            bot.send_message(mess.chat.id, "Такой город не найден. Повторите поиск.")
            msg = bot.send_message(mess.from_user.id, 'В каком городе будем искать?')
            bot.register_next_step_handler(msg, next_step_city)


def next_step_date(m):
    bot.send_message(m.chat.id,
                     "Выберите дату выезда",
                     reply_markup=MyStyleCalendar(calendar_id=1).build()[0])


def next_step_count_hotels(mess):
    """
    Функция проверки на корректность ввода количества отелей в городе.
    В случае положительного ответа, вызываем функцию 'range_request_price'.
    :param mess: объект входящего сообщения от пользователя
    """

    if not isinstance(mess.text, str) or not mess.text.isdigit():
        err_num = bot.send_message(mess.chat.id,
                                   'Количество должно состоять из цифр! Повторите ввод')
        bot.register_next_step_handler(err_num, next_step_count_hotels)
    else:
        if int(mess.text) > 25:
            data['pageSize'] = 25
            bot.send_message(mess.chat.id, 'Будут выведены 25 отелей')

        else:
            data['pageSize'] = int(mess.text)
        bot.send_message(mess.chat.id, "Показать фотографии отелей?", reply_markup=PhotoYesNo().get_photo_yes_no())


def next_step_count_photo(mess):
    """
    Функция проверки на корректность ввода количества отображаемых изображений с отелями.
    :param mess: объект входящего сообщения от пользователя
    """

    if not isinstance(mess.text, str) or not mess.text.isdigit():
        err_num = bot.send_message(mess.chat.id,
                                   'Количество должно состоять из цифр! Повторите ввод.')
        bot.register_next_step_handler(err_num, next_step_count_photo)
    else:
        if int(mess.text) >= 5:
            data['count_show_photo'] = 5
            bot.send_message(chat_id=data['chat_id'], text='Будут выведены 5 фото.')

        else:
            data['count_show_photo'] = int(mess.text)
        txt = lowprice.low_price(data)
        bot.send_message(chat_id=data['chat_id'], text=txt)


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    if call.data in ['yes_photo', 'no_photo']:
        data['photo'] = (True if call.data == 'yes_photo' else False)
        if data['photo']:
            msg2 = bot.send_message(call.message.chat.id,
                                    'Количество фотографий, которые необходимо вывести в результате? (не более 5)')
            bot.register_next_step_handler(msg2, next_step_count_photo)
        else:
            txt = lowprice.low_price(data)
            bot.send_message(chat_id=data['chat_id'], text=txt)

    elif call.data == MyStyleCalendar.func(calendar_id=1):
        result, key, step = MyStyleCalendar(calendar_id=1).process(call.data)
        if result:
            bot.edit_message_text(f"Выбрана дата {result}",
                                  call.message.chat.id,
                                  call.message.message_id)
            if not data.get('checkIn'):
                data['checkIn'] = result.strftime('%d-%m-%Y')
                bot.send_message(call.chat.id,
                                 "Выберите дату выезда",
                                 reply_markup=MyStyleCalendar(calendar_id=1).build()[0])
            else:
                data['checkOut'] = result.strftime('%d-%m-%Y')
                if data['checkOut'] > data['checkIn']:
                    mmes = bot.send_message(call.message,
                                            'Укажите количество отелей, которые необходимо вывести (не более 25)')
                    bot.register_next_step_handler(mmes, next_step_count_hotels)
                else:
                    bot.send_message(call.chat.id,
                                     "Дата выезда должна быть больше даты въезда.\nПовторите ввод.",
                                     reply_markup=MyStyleCalendar(calendar_id=1).build()[0])
    elif call.data == "hotel_backward": # гостиница назад
        pass

    elif call.data == "hotel_forward": # гостиница вперед
        pass

    elif call.data == "photo_backward": # фото назад
        pass

    elif call.data == "photo_forward": # фото вперед
        pass


