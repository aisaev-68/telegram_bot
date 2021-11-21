import requests
from requests import get
import json
import re
from myclass import MyStyleCalendar
from keyboards import PhotoYesNo, InlKbPhoto
from decouple import config
from telebot import TeleBot
from lowprice import low_price



bot = TeleBot(config('TELEGRAM_API_TOKEN'))

data_user = {}

loc_dict1 = {'ru_RU': ['Выберите дату въезда:', 'Выберите дату выезда:', 'Будут выведены 25 отелей:',
                       'Показать фотографии отелей?', 'Укажите количество отелей, которые необходимо вывести (не более 25):',
                       'Количество фотографий, которые необходимо вывести в результате (не более 5)?',
                       'Дата выезда должна быть больше даты въезда.Повторите ввод.', 'Город должен содержать только буквы, повторите ввод.',
                       'Такой город не найден. Повторите поиск.', 'В каком городе будем искать?', 'Количество должно состоять из цифр, повторите ввод'
                       ],
            'en_US': ['Select check-in date:', 'Select check-out date:', '25 hotels will be displayed:',
                       'Show photos of hotels?', 'Specify the number of hotels to be displayed (no more than 25):',
                       'The number of photos to be displayed as a result (no more than 5)?',
                       'The check-out date must be greater than the check-in date. Please re-enter.', 'The city must only contain letters, please re-enter.',
                       'No such city has been found. Repeat the search.', ' In which city are we looking? ', 'The number must consist of numbers, please re-enter'
                      ]
             }








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
        'x-rapidapi-key': config('RAPID_API_KEY')
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

    url = config('URL')

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
    Функция возвращает ссылки на фотографии отеля. Если не найдены, возвращает пустую строку.
    :param id_photo: название города, введённое пользователем бота
    :return photo_list: ссылки на фотографии отеля
    """

    url = config('URL_PHOTOS')
    querystring = {"id": f"{id_photo}"}
    response = req(url, querystring)
    print(response["roomImages"])
    photo_list = []
    for photo in response["roomImages"]:
        for img in photo['images']:
            photo_list.append(img['baseUrl'].replace('{size}', 'z'))


    return photo_list


def next_step_city(mess):
    """
    Функция проверки на корректность ввода названия города.
    В случае корректного ввода города прелагает ввести дату въезда в гостиницу.
    :param mess: объект входящего сообщения от пользователя
    """


    if len(re.findall(r'[А-Яа-яЁёa-zA-Z0-9 -]+', mess.text)) > 1:
        err_city = bot.send_message(mess.chat.id,
                                    'Город должен содержать только буквы, повторите ввод.')
        bot.register_next_step_handler(err_city, next_step_city)
    else:
        idcity = get_city_id(data_user[mess.chat.id].create_idcity_query())

        if idcity is not None:
            data_user[mess.chat.id].id_city = idcity
            bot.send_message(mess.chat.id,
                             "Выберите дату въезда",
                             reply_markup=MyStyleCalendar(calendar_id=1).build()[0])
        else:
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
    chat_id = mess.chat.id
    if not isinstance(mess.text, str) or not mess.text.isdigit():
        err_num = bot.send_message(chat_id,
                                   'Количество должно состоять из цифр! Повторите ввод')
        bot.register_next_step_handler(err_num, next_step_count_hotels)
    else:
        if int(mess.text) > 25:
            data_user[chat_id].count_show_hotels = 25
            bot.send_message(chat_id, 'Будут выведены 25 отелей')
        else:
            data_user[chat_id].count_show_hotels = int(mess.text)
        bot.send_message(chat_id, "Показать фотографии отелей?", reply_markup=PhotoYesNo().get_photo_yes_no())


def next_step_count_photo(mess):
    """
    Функция проверки на корректность ввода количества отображаемых изображений с отелями.
    :param mess: объект входящего сообщения от пользователя
    """
    chat_id = mess.chat.id
    if not isinstance(mess.text, str) or not mess.text.isdigit():
        err_num = bot.send_message(chat_id,
                                   'Количество должно состоять из цифр! Повторите ввод.')
        bot.register_next_step_handler(err_num, next_step_count_photo)
    else:
        if data_user.get(chat_id):
            if int(mess.text) >= 5:
                data_user[chat_id].count_show_photo = 5
                bot.send_message(chat_id, 'Будут выведены 5 фото.')

            else:
                data_user[chat_id].count_show_photo = int(mess.text)
            comand = data_user[chat_id].command
            data_user[chat_id].all_hotels = low_price(data_user[chat_id].queryAPI(comand), chat_id)
            hotels_all = data_user[chat_id].all_hotels
            bot.send_photo(chat_id, get(hotels_all[0][0]).content)
            bot.send_message(chat_id, hotels_all[0], reply_markup=InlKbPhoto().getkbd())


@bot.callback_query_handler(func=lambda call: True)
def inline(call):
    print(call)
    chat_id = call.message.chat.id

    if call.data in ['yes_photo', 'no_photo']:
        data_user[chat_id].status_show_photo = (True if call.data == 'yes_photo' else False)
        if data_user[chat_id].status_show_photo:
            msg2 = bot.send_message(chat_id,
                                    'Количество фотографий, которые необходимо вывести в результате (не более 5)? ')
            bot.register_next_step_handler(msg2, next_step_count_photo)
        else:
            comand = data_user[chat_id].command
            data_user[chat_id].all_hotels = low_price(data_user[chat_id].queryAPI(comand), chat_id)
            bot.send_photo(chat_id, data_user[chat_id].all_hotels.values()[0])
            bot.send_message(chat_id, data_user[chat_id].all_hotels.keys()[0],
                             reply_markup=InlKbPhoto().getkbd())

    elif call.data.startswith('cbcal_1'):
        result, key, step = MyStyleCalendar(calendar_id=1).process(call.data)
        if result:
            bot.edit_message_text(f"Выбрана дата {result}",
                                  chat_id,
                                  call.message.message_id)
            if not data_user[chat_id].checkIn:
                data_user[chat_id].checkIn = result.strftime('%Y-%m-%d')
                bot.send_message(chat_id,
                                 "Выберите дату выезда",
                                 reply_markup=MyStyleCalendar(calendar_id=1).build()[0])
            else:
                data_user[chat_id].checkOut = result.strftime('%Y-%m-%d')
                data_user[chat_id].diff_date()
                if data_user[chat_id].checkOut > data_user[chat_id].checkIn:
                    mmes = bot.send_message(chat_id,
                                            'Укажите количество отелей, которые необходимо вывести (не более 25)')
                    bot.register_next_step_handler(mmes, next_step_count_hotels)
                else:
                    bot.send_message(chat_id,
                                     "Дата выезда должна быть больше даты въезда.Повторите ввод.",
                                     reply_markup=MyStyleCalendar(calendar_id=1).build()[0])
    elif call.data is ["hotel_backward", "hotel_forward", "photo_backward", "photo_forward"]:
        hotels_all = iter(data_user[chat_id].all_hotels)
        if call.data == "hotel_backward": # гостиница назад
            print(1)

        elif call.data == "hotel_forward": # гостиница вперед
            next_hotel = next(hotels_all)
            next_photo = iter(hotels_all[next_hotel])
            bot.send_photo(chat_id, get(next_photo).content)
            bot.send_message(chat_id, next_hotel, reply_markup=InlKbPhoto().getkbd())

        elif call.data == "photo_backward": # фото назад
            print(3)

        elif call.data == "photo_forward": # фото вперед
            print(4)


