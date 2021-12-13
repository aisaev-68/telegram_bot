# -*- coding: utf-8 -*-

from requests_api import req_api, get_photos, config, logging, datetime
from handlers import types
import json

loc_txt = {'ru_RU':
               ['Рейтинг: ', 'Отель: ', 'Адрес: ', 'От центра города:', 'Дата заезда-выезда: ',
                'Цена за сутки (в руб): ', 'Цена за {} сутки (в руб): ', 'Ссылка на страницу: ',
                'Найдено {} отелей'],
           'en_US':
               ['Rating: ', 'Hotel: ', 'Address: ', 'From the city center: ', 'Check-in (check-out) date: ',
                'Price per day (USD): ', 'Price for {} day (USD): ', 'link to the page: ',
                'Found {} hotels']
           }

def hotel_query(querystring: dict, source_dict: dict, bot, mes: types.Message, user: dict):
    """
    Формирует словарь отелей на основе запроса пользователя и сортировкой по цене.
    Если отелей не найдено возвращает пустой словарь.
    :param querystring: строка запроса
    :param source_dict: исходные данные для формирования строки запроса
    :return result_low: возвращает словарь (название отеля, адрес,
    фотографии отеля (если пользователь счёл необходимым их вывод)
    """

    url_low = config('URL_LOW')
    loc = source_dict['language']
    low_data = req_api(url_low, querystring, loc)

    links_htmls = ("https://ru.hotels.com/ho{}" if loc[:2] == "ru"
                   else "https://hotels.com/ho{}?pos=HCOM_US&locale=en_US")
    # TypeError: 'NoneType' object is not subscriptable
    if low_data:
        for hotel_count, results in enumerate(low_data['data']['body']['searchResults']['results']):
            photo_lst = []
            txt = ''
            summa = float(source_dict['diff_date']) * results["ratePlan"]["price"]["exactCurrent"]
            if source_dict['count_show_hotels'] != hotel_count:
                txt = f"<strong>⭐⭐⭐{loc_txt[loc][0]} {(results.get('starRating')) if results.get('starRating') else '--'}⭐⭐⭐</strong>\n" \
                      f"🏨 {loc_txt[loc][1]} {results['name']}\n" \
                      f"       {loc_txt[loc][2]} {results['address'].get('countryName')}, {results['address'].get('locality')}, " \
                      f"{(results['address'].get('streetAddress') if results['address'].get('streetAddress') else 'Нет данных об адресе...')}\n" \
                      f"🚗 {loc_txt[loc][3]} {results['landmarks'][0]['distance']}\n" \
                      f"📅 {loc_txt[loc][4]} {source_dict['checkIn']} - {source_dict['checkOut']}\n" \
                      f"💵 {loc_txt[loc][5]} <b>{(results['ratePlan']['price']['exactCurrent']) if results['ratePlan']['price']['exactCurrent'] else 'Нет данных о расценках...'}</b>\n" \
                      f"💵 {loc_txt[loc][6].format(source_dict['diff_date'])} <b>{summa if results['ratePlan']['price']['exactCurrent'] else 'Нет данных о расценках...'}</b>\n" \
                      f"🌍 {loc_txt[loc][7]}" + f"{links_htmls.format(results['id'])}\n\n"

                if source_dict['status_show_photo']:
                    data_photo = get_photos(results['id'])

                    photo_lst = [types.InputMediaPhoto(media=link) for index, link in enumerate(data_photo) if
                                 source_dict['count_show_photo'] > index]
                    try:
                        bot.send_media_group(chat_id=mes.chat.id, media=photo_lst)
                    except Exception as er:
                        logging.error(f"{datetime.now()} - {er} - Отправка фото")

                    user[mes.chat.id].all_hotels[txt] = photo_lst
                else:
                    user[mes.chat.id].all_hotels[txt] = []
                try:
                    bot.send_message(chat_id=mes.chat.id, text=txt,
                                     disable_web_page_preview=True,
                                     parse_mode="HTML")
                except Exception as e:
                    logging.error(f"{datetime.now()} - {e} - Отправка гостиниц")
        user[mes.chat.id].insert_db()
        bot.send_message(chat_id=mes.chat.id, text=loc_txt[loc][8].format(len(user[mes.chat.id].all_hotels)))

        with open('hotel.json', 'w') as f:
            json.dump(user[mes.chat.id].all_hotels, f, indent=4)
    else:
        bot.send_message(chat_id=mes.chat.id, text=low_data,
                         disable_web_page_preview=True,
                         parse_mode="HTML")

