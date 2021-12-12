import http.client
import time
import requests
import http.client
import json
from bs4 import BeautifulSoup
import lxml

def rectsd():
    conn = http.client.HTTPSConnection("hotels4.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "550e348515mshf137fa7221ce1bbp100461jsn2890da073a15"
    }

    conn.request("GET",
                 "/properties/list?destinationId=243351&pageNumber=1&pageSize=5&checkIn=2021-12-08&checkOut=2021-12-10&adults1=1&sortOrder=PRICE&locale=ru_RU&currency=RUB",
                 headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))


def time_func(func):
    start_time = time.time()
    func()
    print("--- %s seconds ---" % (time.time() - start_time))

def qhttp():
    conn = http.client.HTTPSConnection("hotels4.p.rapidapi.com")

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "71c2dde9b4mshcb25d2a24ecc0a8p1028a9jsn28e630ca48da"
        }

    conn.request("GET", "/properties/list?destinationId=243351&pageNumber=1&pageSize=5&checkIn=2021-12-08&checkOut=2021-12-10&adults1=1&sortOrder=PRICE&locale=ru_RU&currency=RUB", headers=headers)

    res = conn.getresponse()
    data = res.read()

    print(data.decode("utf-8"))

def id_city():
    url = "https://hotels4.p.rapidapi.com/locations/search"

    querystring = {"query": "London", "locale": "en_US"}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "70d6c25f42msh251ac7432fef32bp1f4502jsn416b189200bc"
    }

    response = requests.request("GET", url, headers=headers, params=querystring)

    with open('id_city.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)


def req():
    url = "https://hotels4.p.rapidapi.com/properties/list"

    querystring = {"destinationId": "1506246", "pageNumber": "1", "pageSize": "25", "checkIn": "2021-12-08",
                   "checkOut": "2021-12-15", "adults1": "1", "priceMin": "5000", "priceMax": "10000",
                   "sortOrder": "PRICE", "locale": "en_US", "currency": "USD", "themeIds": "City center"}

    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': "550e348515mshf137fa7221ce1bbp100461jsn2890da073a15",
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)
    with open('id_city1.json', 'w', encoding='utf-8') as f:
        json.dump(response.json(), f, ensure_ascii=False, indent=4)

def yan():
    r = requests.get('https://yandex.ru/yaca/geo.c2n')
    r.raise_for_status()
    lines = r.content.decode(r.apparent_encoding).splitlines()
    #regions = dict(line.split('\t') for line in lines)

    print(lines)
req()
