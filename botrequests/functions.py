from . import lowprice
import requests
import json
import re
from telegram_bot_calendar import WMonthTelegramCalendar, DAY
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


class MyStyleCalendar(WMonthTelegramCalendar):
    prev_button = "⬅️"
    next_button = "➡️"
    first_step = DAY


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


def req(url, headers, querystring):
    response = requests.request("GET", url, headers=headers, params=querystring)
    if response.status_code == 200:
        data = json.loads(response.text)
        return data
    else:
        return None


def get_city_id(querystring: dict) -> str:
    """
    Функция возвращает ID города.Если город не найден,  возвращает пустую строку.
    :param txt: название города, введённое пользователем бота
    :param local: язык поиска
    :return destination_id: id города
    """

    url = "https://hotels4.p.rapidapi.com/locations/search"
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': config['RAPID_API_KEY']
    }

    result_locations_search = req(url, headers, querystring)
    destination_id = None
    for group in result_locations_search['suggestions']:
        if group['group'] == 'CITY_GROUP':
            if group['entities']:
                destination_id = group['entities'][0]['destinationId']
                break
    return destination_id


def get_photos(id):
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"

    querystring = {"id": f"{id}"}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': config['RAPID_API_KEY']
    }

    response = requests.request("GET", url, headers=headers, params=querystring)
    data_photo = json.loads(response.text)

    with open('get_hotel_photos.json', 'w', encoding='utf-8') as file:
        json.dump(data_photo, file, ensure_ascii=False, indent=4)

    return data_photo


def next_step_city(mess, chat_id):
    """
    Ф-ция проверки на корректность ввода названия города.
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
                             reply_markup=gen_markup())
        else:
            data.clear()
            bot.send_message(mess.chat.id, "Такой город не найден. Повторите поиск.")
            msg = bot.send_message(mess.from_user.id, 'В каком городе будем искать?')
            bot.register_next_step_handler(msg, next_step_city)
        print('я тут')


def gen_markup():
    calendar, step = MyStyleCalendar(calendar_id=1).build()
    return calendar


def next_step_date(m):
    calendar, step = MyStyleCalendar(calendar_id=1).build()
    bot.send_message(m.chat.id,
                     "Выберите дату выезда",
                     reply_markup=calendar)


def next_step_count_hotels(mess):
    """
    Ф-ция проверки на корректность ввода кол-ва искомых отелей в городе.
    В случае положительного ответа, вызываем ф-цию range_request_price.
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
        request_photo(mess)


def request_photo(mess):
    """
    Ф-ция отправляющая кнопки с вопросом будем ли искать фото?
    :param mess: объект входящего сообщения от пользователя
    """

    markup = types.InlineKeyboardMarkup()
    yes_photo_hotels = types.InlineKeyboardButton(text='✅Да', callback_data='yes_photo')
    no_photo_hotels = types.InlineKeyboardButton(text='❌Нет', callback_data='no_photo')
    markup.add(yes_photo_hotels, no_photo_hotels)
    bot.send_message(mess.chat.id, "Показать фотографии отелей?", reply_markup=markup)


def next_step_count_photo(mess):
    """
    Ф-ция проверки на корректность ввода пользователем кол-ва отображаемых изображений с отелями.
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


@bot.callback_query_handler(func=MyStyleCalendar.func(calendar_id=1))
def cal(c):
    result, key, step = MyStyleCalendar(calendar_id=1).process(c.data)
    if result:
        bot.edit_message_text(f"Выбрана дата {result}",
                              c.message.chat.id,
                              c.message.message_id)
        if not data.get('checkIn'):
            data['checkIn'] = result.strftime('%d-%m-%Y')
            bot.callback_query_handler(next_step_date(c.message), reply_markup=gen_markup())
        else:
            data['checkOut'] = result.strftime('%d-%m-%Y')
            if data['checkOut'] > data['checkIn']:
                mmes = bot.send_message(c.message,
                                        'Укажите количество отелей, которые необходимо вывести (не более 25)')
                bot.register_next_step_handler(mmes, next_step_count_hotels)
            else:
                bot.send_message(c.message, 'Дата выезда должна быть больше даты въезда.\nПовторите ввод.')
                bot.callback_query_handler(next_step_date(c.message), reply_markup=gen_markup())


@bot.callback_query_handler(func=lambda c: c.data in ['yes_photo', 'no_photo'])
def inline(c):
    bot.delete_message(c.message.chat.id, message_id=c.message.id)
    data['photo'] = (True if c.data == 'yes_photo' else False)
    if data['photo']:
        msg2 = bot.send_message(c.message.chat.id,
                                'Количество фотографий, которые необходимо вывести в результате? (не более 5)')
        bot.register_next_step_handler(msg2, next_step_count_photo)
    else:
        txt = lowprice.low_price(data)
        bot.send_message(chat_id=data['chat_id'], text=txt)
