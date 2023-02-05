import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json
import csv
from time import sleep
import random

def get_json_file_menu(name, url, headers):
    r = requests.get(url, headers=headers)
    r.encoding = r.apparent_encoding

    data = r.json()
    with open(name, 'a', encoding='UTF-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)
        print(f'Данные сохранены в {name}')

def get_json_file_category(category, subcategory, shard, query, headers):
    page = 1
    flag = True
    name = f'data_json/{category}_{subcategory}.json'
    while flag:
        url = get_url(shard, query, page)
        r = requests.get(url, headers=headers)

        if len(r.text) > 0:
            data = r.json()
            with open(name, 'a', encoding='utf-8') as json_file:
                json.dump(data, json_file, indent=4, ensure_ascii=False)
                page += 1
            
            sleep(random.randrange(1,3))
        else:
            flag = False
            print(f'Данные сохранены в {name}')

def get_url(shard, query, page):
    url = f"https://catalog.wb.ru/catalog/{shard}/catalog?appType=1&{query}&couponsGeo=2,12,7,3,6,18,22,21&curr=rub&dest=-1075831,-72193,-2725551,-3927439&emp=0&lang=ru&locale=ru&page={page}&pricemarginCoeff=1.0&reg=1&regions=80,64,83,4,38,33,70,69,86,30,40,48,1,22,66,31&sort=popular&spp=26&sppFixGeo=4"
    return url

def get_data(file, headers):
    with open(file, 'r', encoding='UTF-8') as json_file:
        data = json.load(json_file)

    category_id = {}
    datas = {} # названия категорий и их подкатегорий, у которых нет параметров shard, query
    for x in data:
        category = x['name']
        id = x['id']
        url = x['url']

        if 'childs' in x:
            with open(f'data/{category}.csv', 'w', encoding="utf-8-sig", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(("id", "sub_id", "subcategory", "url"))

            for y in x['childs']:
                subcategory = y['name']
                subid = y['id']
                suburl = y['url']
                if 'shard' in y and 'query' in y:
                    subshard = y['shard']
                    subquery = y['query']

                    get_json_file_category(category, subcategory, subshard, subquery, headers)

                else:
                    if category in datas:
                        datas[category].append(subcategory)
                    else:
                        datas[category] = [subcategory]

                with open(f'data/{category}.csv', 'a', encoding="utf-8-sig", newline='') as file:
                    writer = csv.writer(file, delimiter=';')
                    writer.writerow((id, subid, subcategory, suburl))
        else:  
            if 'shard' in x and 'query' in x:
                shard = x['shard']
                query = x['query']

                get_json_file_category(category, '', shard, query, headers)
            else:
                datas[category] = []          
            with open(f'data/{category}.csv', 'w', encoding="utf-8-sig", newline='') as file:
                writer = csv.writer(file, delimiter=';')
                writer.writerow(("id", "url"))
                writer.writerow((id, url))

        category_id[category] = id


if __name__ == '__main__':
    file = 'wb_catalogs_data.json'
    name = 'wb_catalogs_data.json'
    url_wb = "https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json"
    headers = {
                        "Accept": "*/*",
                        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
                    }
    # get_json_file(name, url_wb, headers)
    get_data(file, headers)