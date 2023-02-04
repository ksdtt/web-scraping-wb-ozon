import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import csv

headers = {
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
            }

url = "https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json"
pref_url = "https://www.wildberries.ru"

'''
r = requests.get(url, headers=headers)
r.encoding = r.apparent_encoding

data = r.json()
with open('wb_catalogs_data.json', 'w', encoding='UTF-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)
    print('Данные сохранены в wb_catalogs_data.json')
'''

def check_childs(category):
    return True if 'childs' in category else False

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

#print(table2.join(table3, lsuffix='_caller', rsuffix='_other'))


file = 'wb_catalogs_data.json'
get_data(file)