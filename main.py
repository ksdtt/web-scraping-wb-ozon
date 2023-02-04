import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import csv

def get_jsonfile(name, url):
    headers = {
                    "Accept": "*/*",
                    "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
                }

    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding

    data = r.json()
    with open(name, 'w', encoding='UTF-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f'Данные сохранены в {name}')


def get_data(file):
    pref_url = "https://www.wildberries.ru"

    with open(file, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)

    category_id = {}
    for x in data:
        category = x['name']
        id = x['id']
        url = x['url']

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

file = 'wb_catalogs_data.json'
name = 'wb_catalogs_data.json'
url = "https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json"
# get_jsonfile(name, url)
get_data(file)
