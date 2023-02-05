import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import csv
import os

def get_json_file(name, url, headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding

    data = r.json()
    with open(name, 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f'Данные сохранены в {name}')

def get_htmp_page(url, category, headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding
    with open(f'data/{category}.html', 'w', encoding="utf-8") as file:
        file.write(r.text)
        print(f'Данные сохранены в {category}')

def get_content(shard, query, low_price=None, top_price=None):
    headers = {'Accept': "*/*", 'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    data_list = []
    for page in range(1, 101):
        print(f'Сбор позиций со страницы {page} из 100')
        url = f'https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&curr=rub&dest=-1075831,-77677,-398551,12358499' \
              f'&locale=ru&page={page}&priceU={low_price * 100};{top_price * 100}' \
              f'®=0®ions=64,83,4,38,80,33,70,82,86,30,69,1,48,22,66,31,40&sort=popular&spp=0&{query}'
        r = requests.get(url, headers=headers)
        data = r.json()
        print(f'Добавлено позиций: {len(get_data_from_json(data))}')
        if len(get_data_from_json(data)) > 0:
            data_list.extend(get_data_from_json(data))
        else:
            print(f'Сбор данных завершен.')
            break
    return data_list

def get_url(shard, query):
    url = f"https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&{query}&couponsGeo=2,12,7,3,6,18,22,21&curr=rub&dest=-1075831,-72193,-2725551,-3927439&emp=0&lang=ru&locale=ru&page=1&pricemarginCoeff=1.0&reg=1&regions=80,64,83,4,38,33,70,69,86,30,40,48,1,22,66,31&sort=popular&spp=26&sppFixGeo=4"
    return url


def get_data(file, headers):
    pref_url = "https://www.wildberries.ru"

    with open(file, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)

    category_id = {}
    for x in data:
        category = x['name']
        id = x['id']
        url = x['url']
        if 'shard' in x and 'query' in x:
            shard = x['shard']
            query = x['query']

        if "https://" not in url:
            url = pref_url + url

        if 'childs' in x:
            with open(f'data/{category}.csv', 'w', encoding="utf-8-sig", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(("id", "sub_id", "subcategory", "url"))

            for y in x['childs']:
                subcategory = y['name']
                subid = y['id']
                suburl = y['url']

                if "https://" not in suburl:
                    suburl = pref_url + suburl

                with open(f'data/{category}.csv', 'a', encoding="utf-8-sig", newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow((id, subid, subcategory, suburl))
        else:            
            with open(f'data/{category}.csv', 'w', encoding="utf-8-sig", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(("id", "url"))
                writer.writerow((id, url))

        category_id[category] = id

        if category == 'Сделано в Москве':
            url = get_url(shard,query)
            print(url)
            get_htmp_page(url, category, headers)

file = 'wb_catalogs_data.json'
name = 'wb_catalogs_data.json'
url_wb = "https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json"
headers = {
                    "Accept": "*/*",
                    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
                }
# get_json_file(name, url_wb, headers)
get_data(file, headers)
