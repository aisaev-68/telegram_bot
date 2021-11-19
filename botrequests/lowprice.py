from functions import get_photos, req
from myclass import Hotel


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

    url_low = "https://hotels4.p.rapidapi.com/properties/list"

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

    low_data = req(url_low, querystring_low)
    for results in low_data['data']['body']['searchResults']['results']:
        low_hotel = Hotel()
        low_hotel.name_hotel = f'*Имя: {results["name"]}*'
        low_hotel.country_Name = f'Адрес: {results["address"].get("countryName")}'
        low_hotel.locality = results["address"].get("locality")
        low_hotel.streetAddress = f'{(results["address"].get("streetAddress") if results["address"].get("streetAddress") else "Нет данных об адресе...")}'
        low_hotel.distance = f'От центра города: {results["landmarks"][0]["distance"]}'
        low_hotel.current = f'Цена {(results["ratePlan"]["price"]["current"]) if results["ratePlan"]["price"]["current"] else "Нет данных о расценках..."}'
        data_photo = get_photos(results['id'])
        for photo in data_photo["roomImages"]:
            for img in photo['images']:
                low_hotel.photo = img['baseUrl'].replace('{size}', 'z')