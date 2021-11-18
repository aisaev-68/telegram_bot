import json
from . import functions
#import req, get_photos
import os


def low_price(data: dict):
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
    results_low = {}
    i_text = ''
    url_low = "https://hotels4.p.rapidapi.com/properties/list"
    # f"{data['pSize']}",
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': os.environ.get('RAPID_API_KEY')
    }
    querystring_low = {
        "destinationId": f"{data['destinationId']}",
        "pageNumber": "1",
        "pageSize": f"{data['pageSize']}",
        "checkIn": f"{data['checkIn']}",
        "checkOut": f"{data['checkOut']}",
        "adults1": "1",
        "sortOrder": "PRICE",
        "locale": f"{data['locale']}",
        "currency": f"{data['currency']}"
    }

    low_data = functions.req(url_low, headers, querystring_low)

    for results in low_data['data']['body']['searchResults']['results']:
        results_low[results['id']] = dict()
        data_photo = functions.get_photos(results['id'])
        results_low[results['id']]['photo'] = []
        for photo in data_photo["roomImages"]:

            for img in photo['images']:
                results_low[results['id']]['photo'].append(img['baseUrl'].replace('{size}', 'z'))

        i_text = f'*Имя: {results["name"]}*\n' \
                 f'Адрес: {results["address"].get("countryName")}, {results["address"].get("locality")}' \
                 f'{(", " + results["address"].get("streetAddress") if results["address"].get("streetAddress") else "")}\n' \
                 f'От центра города: {results["landmarks"][0]["distance"]}\nЦена {results["ratePlan"]["price"]["current"]}\n\n'

        # results_low[results['id']]['name'] = results['name']
        # if results['address'].get('streetAddress'):
        #     results_low[results['id']]['address'] = results['address']['streetAddress']
        # results_low[results['id']][
        #     'price'] = f"{results['ratePlan']['price']['current']} - {results['ratePlan']['price']['info']}"
        # results_low[results['id']]['exactCurrent'] = results['ratePlan']['price']['exactCurrent']
        # landmarks_list = ''
        # for landmarks in results['landmarks']:
        #     landmarks_list += f"{landmarks['label']} - {landmarks['distance']}\n"
        # results_low[results['id']]['landmarks'] = landmarks_list
        # txt_rating = ''
        # if results.get('guestReviews'):
        #     if results['guestReviews'].get('rating'):
        #         txt_rating = f"{results['guestReviews']['rating']}"
        #     elif results['guestReviews'].get('badgeText'):
        #         txt_rating += f"{results['guestReviews']['badgeText']}"
        # results_low[results['id']]['guestReviews'] = txt_rating

    return i_text
