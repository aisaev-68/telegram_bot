import json
from main import data_user


loc_dict = {'ru_RU': ['Рейтинг:', 'Название отеля:', 'Адрес:', 'Удаленность от центра города:', 'Дата въезда:',
                      'Дата выезда', 'Стоимость за сутки (в руб):', 'Стоимость за {} сутки (в руб):'],
            'en_US': ['Rating:', 'The name of the hotel:', 'Address:', 'Distance from the city center:', 'Arrival date:',
                      'Date of departure:', 'Cost per day (USD):', 'Price for {} day (USD):']}


def low_price(querystring_low: dict, chat_id):
    """
        Формирует словарь отелей на основе запроса пользователя и сортировкой по цене.
        Если отелей не найдено возвращает пустой словарь.
        :param destination_id: ID города
        :param pageSize: количество страниц для вывода
        :param checkIn: дата въезда в гостиницу
        :param checkOut: дата выезда из гостиницы
        :param sortOrder: сортировка по умолчанию для данного режима "PRICE"
        :param loc: локализация (русский, английский)
        :param currency: цена за сутки
        :return result_low: возвращает словарь (название отеля, адрес,
        фотографии отеля (если пользователь счёл необходимым их вывод)
        """

    url_low = "https://hotels4.p.rapidapi.com/properties/list"
    hotels_dict = {}
    low_data = req(url_low, querystring_low)
    locale = data_user[chat_id].language
    for hotel_count, results in enumerate(low_data['data']['body']['searchResults']['results']):
        summa = float(data_user[chat_id].getDiff_date()) * results["ratePlan"]["price"]["exactCurrent"]
        if data_user[chat_id].count_show_hotels != hotel_count:
            txt = f'{loc_dict[locale][0]} {(results.get("starRating")) if results.get("starRating") else "--"}\n' \
                  f'{loc_dict[locale][1]} {results["name"]}\n{loc_dict[locale][2]} {results["address"].get("countryName")}, ' \
                  f'{results["address"].get("locality")}\n' \
                  f'{(results["address"].get("streetAddress") if results["address"].get("streetAddress") else "Нет данных об адресе...")}\n' \
                  f'{loc_dict[locale][3]} {results["landmarks"][0]["distance"]}\n' \
                  f'{loc_dict[locale][4]} {data_user[chat_id].checkIn}\n' \
                  f'{loc_dict[locale][5]} {data_user[chat_id].checkOut}\n' \
                  f'{loc_dict[locale][6]} {(results["ratePlan"]["price"]["exactCurrent"]) if results["ratePlan"]["price"]["exactCurrent"] else "Нет данных о расценках..."}\n' \
                  f'{loc_dict[locale][7].format(data_user[chat_id].getDiff_date())} {(summa) if results["ratePlan"]["price"]["exactCurrent"] else "Нет данных о расценках..."}'
            data_photo = get_photos(results['id'])
            photo_lst = []
            for index, photo in enumerate(data_photo):
                if data_user[chat_id].count_show_photo != index:
                    photo_lst.append(photo)
                else:
                    break
            hotels_dict[txt] = photo_lst

    data_user[chat_id].all_hotels = hotels_dict

    with open('hotel.json', 'w') as f:
        json.dump(data_user, f, ensure_ascii=False, indent=4)

