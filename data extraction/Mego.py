# -*- coding: utf-8 -*-
import json
import requests
import re
import time
from bs4 import BeautifulSoup

url = "https://mego.lv/kontakti"


def scrap_mego(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)
    pattern = r"\[.*]"
    chunk = re.findall(pattern, str(all_scripts[4]))
    raw_json = json.loads(chunk[0])
    for i in raw_json:
        i['address'] = BeautifulSoup(i['info'], 'html.parser').text.rstrip()
        each_div = soup.find('div', attrs={'data-shop-id': i['shop_id']})
        working_hours = each_div.select('p')[0].text.strip()
        i['working_hours'] = working_hours

    with open("Mego.json", "w", encoding='utf8') as f:
        f.write(json.dumps(raw_json, ensure_ascii=False, indent=4))


scrap_mego(url)
