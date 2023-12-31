from decouple import config
import json
from requests import request, ConnectionError, Timeout
import logging
from logging.handlers import RotatingFileHandler
from bs4 import BeautifulSoup

logging.basicConfig(handlers=[RotatingFileHandler('logger.log', maxBytes=100000, backupCount=10)], level=logging.INFO,
                    format="%(asctime)s - %(module)s - %(levelname)s - %(funcName)s: %(lineno)d - %(message)s",
                    datefmt='%d-%b-%y %H:%M:%S')

server_error = {"ru_RU": {"ertime": "Время ожидания запроса истекло. Попробуйте позже.",
                          "erjson": "Получен некорректный ответ от сервиса. Попробуйте позже.",
                          "ercon": "Нет, соединения с сервисом. Попробуйте позже.",
                          "erhttp": "Что-то пошло не так. Повторите позже.",
                          "quota": 'Превышена ежемесячная квота для запросов по плану BASIC.'},
                "en_US": {"ertime": "The request timed out. Please try again later.",
                          "erjson": "Received an invalid response from the service. Please try again later.",
                          "ercon": "No, connecting to the service. Please try again later.",
                          "erhttp": "Something went wrong. Please try again later.",
                          "quota": 'Monthly quota exceeded for BASIC plan requests.'}}

loc_txt = {'ru_RU':
               ['Отмена', 'Ваша история пуста.', 'Команда выполнена.',
                'Рейтинг: ', 'Отель: ', 'Адрес: ', 'От центра города:', 'Дата заезда-выезда: ',
                'Цена за сутки (в руб): ', 'Цена за {} сутки (в руб): ', 'Ссылка на страницу: ',
                'Нет данных об адресе.', 'Нет данных о расценках.'],
           'en_US':
               ['Cancel', 'Your history is empty.', 'Command completed.',
                'Rating: ', 'Hotel: ', 'Address: ', 'From the city center: ', 'Check-in (check-out) date: ',
                'Price per day (USD): ', 'Price for {} day (USD): ', 'link to the page: ',
                'No address data.', 'No price data.']
           }


def diff_date(check_in: str, check_out: str) -> int:
    """
    Функция определения количества суток проживания по датам заезда и выезда
    :param check_in: дата заезда
    :param check_out: дата выезда
    :return: возвращает количество суток
    """
    import datetime
    a = check_in.split('-')
    b = check_out.split('-')
    d = str(datetime.date(int(b[0]), int(b[1]), int(b[2])) - datetime.date(int(a[0]), int(a[1]), int(a[2])))
    return int(d.split()[0])


def price_parse(line_text: dict, language: str, check_in: str, check_out: str) -> dict:
    """Функция возвращает из полученной строки кол-во дней, обшую сумму и цену за сутки в виде словаря
    {'day': day, 'price_total': price_total, 'price_day': price_day}
    :param line_text: строка для парсинга
    :param language: язык пользователя
    :param check_in: дата заезда
    :param check_out: дата выезда"""

    if language == 'ru_RU':
        try:
            if line_text['price'].get('info'):
                day = line_text['price']['info'].split()[4]
                price_total = line_text['price']['exactCurrent']
                price_day = round(price_total / float(day), 2)
                return {'day': day, 'price_total': price_total, 'price_day': price_day}
            else:
                day = diff_date(check_in, check_out)
                price_day = line_text['price']['exactCurrent']
                price_total = round(price_day * float(day), 2)
                return {'day': day, 'price_total': price_total, 'price_day': price_day}
        except Exception as er:
            logging.error(f"{er} - Функция price_parse (русский язык)")
    else:
        try:

            if line_text['price'].get('fullyBundledPricePerStay'):
                pr = BeautifulSoup(line_text['price']['fullyBundledPricePerStay'], 'html.parser').get_text().split()
                if len(pr) > 2:
                    day = BeautifulSoup(line_text['price']['fullyBundledPricePerStay'],
                                        'html.parser').get_text().split()[3]
                else:
                    day = diff_date(check_in, check_out)
                price_total = BeautifulSoup(line_text['price']['fullyBundledPricePerStay'],
                                            'html.parser').get_text().split()[1][1:].replace(',', '')
                price_day = round(float(price_total) / float(day), 2)
                return {'day': day, 'price_total': price_total, 'price_day': price_day}
            else:
                day = diff_date(check_in, check_out)
                price_day = line_text['price']['exactCurrent']
                price_total = round(price_day * float(day), 2)
                return {'day': day, 'price_total': price_total, 'price_day': price_day}
        except Exception as er:
            logging.error(f"{er} - Функция price_parse (английски язык)")


def city_parse(line_text: str) -> str:
    """Функци возвращает из полученной строки названия города и региона
    :param line_text: срока для парсинга
    """

    return BeautifulSoup(line_text, 'html.parser').get_text().lower()


def req_api(url: str, querystring: dict, lang: str) -> dict:
    """
    Функция возвращает данные запроса к API гостиниц.
    :param url: страница поиска
    :param querystring: срока запроса
    :param lang: язык пользователя
    :return data: возвращаемые API данные  в виде словаря
    """

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': config('RAPID_API_KEY')
    }
    try:

        response = request("GET", url, headers=headers, params=querystring, timeout=15)
        if response.status_code == 200:
            data = json.loads(response.text)
            return {"ok": data}
        else:
            if json.loads(response.text).get("message"):
                logging.error(
                    "Функция req_api - Превышена ежемесячная квота для запросов по плану BASIC.")
                return {"error": server_error[lang]["quota"]}
            else:
                logging.error("Функция req_api - Что-то пошло не так. Повторите позже.")
                return {"error": server_error[lang]["erhttp"]}
    except ConnectionError as ercon:
        logging.error(f"{ercon} - Функция req_api - Нет, соединения с сервисом.")
        return {"error": server_error[lang]["ercon"]}
    except Timeout as ertime:
        logging.error(f"{ertime} - Функция req_api - Время ожидания запроса истекло")
        return {"error": server_error[lang]["ertime"]}
    except json.decoder.JSONDecodeError as erjson:
        logging.error(
            f"{erjson} - Функция req_api - Получены некорректные данные от сервиса.")
        return {"error": server_error[lang]["erjson"]}


def get_photos(id_photo: str, count: int, lang: str) -> list:
    """
    Функция возвращает список ссылок на фотографии отеля. Если не найдены, возвращает пустой список.
    :param id_photo: ID отеля
    :param count: количество фото для загрузки
    :param lang: язык пользователя
    :return photo_list: список ссылок на фотографии отеля в виде списка
    """

    url = config('URL_PHOTOS')
    querystring = {"id": f"{id_photo}"}
    response = req_api(url, querystring, lang)
    photo_list = []
    if response.get("ok"):
        for photo in response["ok"]["roomImages"]:
            for img in photo['images']:
                if len(photo_list) != count:
                    photo_list.append(img['baseUrl'].replace('{size}', 'z'))
            if len(photo_list) != count:
                break
    return photo_list


def get_city_id(querystring: dict) -> dict:
    """
    Функция запрашивает информацию для вывода в чат городов.Возвращает ID городов.
    :param querystring: строка запроса в виде словаря {'query': 'минск', 'locale': 'ru_RU'}
    """
    lang = querystring['locale']
    result_id_city = req_api(config('URL'), querystring, lang)

    if result_id_city.get("ok"):
        parse_city = {}
        for city in result_id_city["ok"]['suggestions']:
            if city['group'] in ['CITY_GROUP', 'CITY']:
                for name in city['entities']:
                    parse_city[name['destinationId']] = city_parse(name['caption']).title()
                return {"city": parse_city}
        return {'empty': 1}
    else:
        return result_id_city


def hotel_query(querystring: dict, par_dict: dict) -> dict:
    """
    Формирует словарь отелей на основе запроса пользователя и сортировкой по цене.
    Если отелей не найдено возвращает пустой словарь.
    :param querystring: строка запроса в виде словаря
    :param par_dict: словарь с дистанцией и ценой, командой
    :return : возвращает словарь (название отеля, адрес,
    фотографии отеля (если пользователь счёл необходимым их вывод) либо сообщение сервера
    """

    url_low = config('URL_LOW')
    lang = querystring["locale"]
    data = req_api(url_low, querystring, lang)
    links_html = ("https://ru.hotels.com/ho{}" if lang == "ru_RU"
                   else "https://hotels.com/ho{}?pos=HCOM_US&locale=en_US")

    if data.get("ok"):
        if par_dict['command'] == '/bestdeal':
            if lang == 'ru_RU':
                low_data = [d for d in data["ok"]['data']['body']['searchResults']['results']
                            if par_dict['dist_min'] <= float(
                        d['landmarks'][0]['distance'].split()[0].replace(',', '.')) <= par_dict['dist_max']]
            else:
                low_data = [d for d in data["ok"]['data']['body']['searchResults']['results']
                            if par_dict['dist_min'] <= float(
                        d['landmarks'][0]['distance'].split()[0]) <= par_dict['dist_max']]
        else:
            low_data = [d for d in data["ok"]['data']['body']['searchResults']['results']]
        all_hotels = {}
        for hotel_count, results in enumerate(low_data):
            txt = ''
            price = {'day': diff_date(querystring['checkIn'], querystring['checkOut']),
                     'price_total': loc_txt[lang][12], 'price_day': loc_txt[lang][12]}
            if results.get('ratePlan'):
                price = price_parse(results["ratePlan"], lang, querystring['checkIn'], querystring['checkOut'])
            if querystring["pageSize"] != hotel_count:
                photos = []
                if par_dict['stat_photo']:
                    data_photo = get_photos(results['id'], par_dict['count_photo'], lang)
                    if len(data_photo) > 0:
                        photos = [link for link in data_photo]

                txt = f"<strong>⭐{loc_txt[lang][3]} {(results.get('starRating')) if results.get('starRating') else '--'}⭐</strong>\n" \
                      f"🏨 {loc_txt[lang][4]} {results['name']}\n" \
                      f"       {loc_txt[lang][5]} {results['address'].get('countryName')}, {results['address'].get('locality')}, " \
                      f"{(results['address'].get('streetAddress') if results['address'].get('streetAddress') else loc_txt[lang][11])}\n" \
                      f"🚗 {loc_txt[lang][6]} {results['landmarks'][0]['distance']}\n" \
                      f"📅 {loc_txt[lang][7]} {querystring['checkIn']} - {querystring['checkOut']}\n" \
                      f"💵 {loc_txt[lang][8]} <b>{price['price_day']}</b>\n" \
                      f"💵 {loc_txt[lang][9].format(price['day'])} <b>{price['price_total']}</b>\n" \
                      f"🌍 {loc_txt[lang][10]} {links_html.format(results['id'])}\n\n"

                all_hotels[txt] = photos

        return all_hotels
    else:
        return data
