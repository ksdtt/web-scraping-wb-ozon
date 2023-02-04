import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import json

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

with open('wb_catalogs_data.json', 'r', encoding='UTF-8') as json_file:
    data = json.load(json_file)

category_id = {}
sub1category_id_parent = {}
sub2category_id_parent = {}
sub3category_id_parent = {}
url_id = {}
count = 0
for element in data:
    category = element['name']
    id = element['id']

    if 'childs' in element:

        for child in element['childs']:
            sub1category = child['name']
            sub1id = child['id']
            sub1parent = child['parent']

            sub1category_id_parent[f"{sub1category}"] = (sub1id, sub1parent) 

            if 'childs' in child:

                for sub_child in child['childs']:
                    sub2category = sub_child['name']
                    sub2id = sub_child['id']
                    sub2parent = sub_child['parent']

                    sub2category_id_parent[f"{sub2category}"] = (sub2id, sub2parent)

                    if 'childs' in sub_child:

                        for sub__child in sub_child['childs']:
                            ''''''
                            if 'childs' in sub__child:
                                for sub___child in sub__child['childs']:
                                    count += 1
                                    # где-то ещё 27 ссылок теряется
                            ''''''
                            sub3category = sub__child['name']
                            sub3id = sub__child['id']
                            sub3parent = sub__child['parent']

                            sub3category_id_parent[f"{sub3category}"] = (sub3id, sub3parent)

                            if "https://" in sub__child['url']:
                                url_id[sub3id] = sub__child['url']
                            else:
                                url_id[sub3id] = pref_url + sub__child['url']
                    
                    if "https://" in sub_child['url']:
                        url_id[sub2id] = sub_child['url']
                    else:
                        url_id[sub2id] = pref_url + sub_child['url']
           
            if "https://" in child['url']:
                url_id[sub1id] = child['url']
            else:
                url_id[sub1id] = pref_url + child['url']

    if "https://" in element['url']:
        url_id[id] = element['url']
    else:
        url_id[id] = pref_url + element['url']

    category_id[category] = id

# словари в dataframe

table1 = pd.DataFrame.from_dict(category_id, orient='index').rename(columns={0:'id'})
table2 = pd.DataFrame.from_dict(sub1category_id_parent, orient='index').rename(columns={0: 'id_sub', 1: 'parent'})
table3 = pd.DataFrame.from_dict(sub2category_id_parent, orient='index').rename(columns={0: 'id_subsub', 1: 'parent'})
table4 = pd.DataFrame.from_dict(sub3category_id_parent, orient='index').rename(columns={0: 'id_subsub', 1: 'parent'})

url_id_pd = pd.DataFrame.from_dict(url_id, orient='index').rename(columns={0:'url'})

print(5, len(url_id))

print(6, count)
#print(table2.join(table3, lsuffix='_caller', rsuffix='_other'))
