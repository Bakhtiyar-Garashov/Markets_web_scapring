import json
import requests
import re
import time
from bs4 import BeautifulSoup

url = "https://www.latts.lv/lv/veikali"


def scrap_lats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)
    final = []
    data = repr(all_scripts[12])
    pattern = r"\{.*}"
    result = re.findall(pattern, data)

    address_patter = r"<h3>(.*?)\."
    # r"<h3>(.*?)\/h3>"
    lat = r'\"latitude\":[-+]?(\d+\.\d+)'
    lon = r'\"longitude\":[-+]?(\d+\.\d+)'
    for i in result:
        dicts = dict()
        prop = re.findall(address_patter, i)
        address = prop[0].replace('"', "'")
        full_address = address.split('</a>')
        if full_address:
            for each in full_address:
                each_text = BeautifulSoup(each, 'html.parser')
                dicts['address'] = each_text.text[:len(each_text.text) - 15]

        dicts['feature'] = "Point"
        dicts['lat'] = re.findall(lat, i)[0] if re.findall(lat, i) else ""
        dicts['lon'] = re.findall(lon, i)[0] if re.findall(lon, i) else ""
        final.append(dicts)

    with open("Lats.json", "w", encoding='utf8') as f:
        f.write(json.dumps(final, ensure_ascii=False, indent=4))


scrap_lats(url)
