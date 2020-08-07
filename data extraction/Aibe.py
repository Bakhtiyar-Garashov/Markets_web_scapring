import json
import requests

url = "http://www.aibe.lv/shops.json"


def scrap_aibe(url):
    response = requests.get(url)
    raw_json = response.json()

    with open("Aibe.json", "w+", encoding='utf8') as f:
        f.write(json.dumps(raw_json, ensure_ascii=False, indent=5))


scrap_aibe(url)
