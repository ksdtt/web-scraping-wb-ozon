import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

def correct_id(x):
    return int(x[0])

def correct_parent(x): return int(x[1])

headers = {
                "Accept": "*/*",
                "User-Agent": "Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1"
            }

url = "https://static-basket-01.wb.ru/vol0/data/main-menu-ru-ru-v2.json"

'''
r = requests.get(url, headers=headers)
r.encoding = r.apparent_encoding

data = r.json()
with open('wb_catalogs_data.json', 'w', encoding='UTF-8') as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)
    print('Данные сохранены в wb_catalogs_data.json')
'''

with open('wb_catalogs_data.json', 'r', encoding='UTF-8') as json_file:
    data = json.load(json_file)

category_id = {}
subcategory_id_parent = {}
subsubcategory_id_parent = {}
url_id = {}

for element in data:
    category = element['name']
    id = element['id']

    if 'childs' in element:
        for child in element['childs']:
            subcategory = child['name']
            subid = child['id']
            subparent = child['parent']

            subcategory_id_parent[f"{subcategory}"] = (subid, subparent) 

            if 'childs' in child:
                for sub_child in child['childs']:
                    subsubcategory = sub_child['name']
                    subsubid = child['id']
                    subsubparent = child['parent']

                    subsubcategory_id_parent[f"{subsubcategory}"] = (subsubid, subsubparent)

                    url_id[subsubid] = "https://www.wildberries.ru" + sub_child['url']
            else:
                url_id[subid] = "https://www.wildberries.ru" + child['url']
    else:
        url_id[id] = "https://www.wildberries.ru" + element['url']
    category_id[category] = id

'''словари в dataframe'''
'''1 способ'''
table1 = pd.DataFrame(list(category_id.items()), columns=['category', 'id'])

table2 = pd.DataFrame(list(subcategory_id_parent.items()), columns=['category', 'id_parent'])
table2 = table2.assign(parent=table2['id_parent'].apply(correct_parent))
table2['id_parent'] = table2['id_parent'].apply(correct_id)
table2.rename(columns={'id_parent': 'id'}, inplace=True)

table3 = pd.DataFrame(list(subsubcategory_id_parent.items()), columns=['category', 'id_parent'])
table3 = table3.assign(parent=table3['id_parent'].apply(correct_parent))
table3['id_parent'] = table3['id_parent'].apply(correct_id)
table3.rename(columns={'id_parent': 'id'}, inplace=True)

"""2 способ"""
table1 = pd.DataFrame.from_dict(category_id, orient='index').rename(columns={0:'id'})
table2 = pd.DataFrame.from_dict(subcategory_id_parent, orient='index').rename(columns={0: 'id', 1: 'parent'})
table3 = pd.DataFrame.from_dict(subsubcategory_id_parent, orient='index').rename(columns={0: 'id', 1: 'parent'})