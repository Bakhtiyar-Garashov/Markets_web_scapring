import json
import requests
import urllib3

url = "https://www.drogas.lv/lv/mahazyny/all"


def scrap_drogas(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    raw_json = response.data.decode('utf-8')

    with open("Drogas.json", "w+", encoding='utf8') as f:
        f.write(json.loads(json.dumps(raw_json, ensure_ascii=False, indent=5)))


scrap_drogas(url)
