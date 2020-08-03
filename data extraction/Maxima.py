import urllib3
import json

url = "https://www.maxima.lv/ajax/shopsnetwork/map/getCities"


def scrap_maxima(url):
    http = urllib3.PoolManager()
    r = http.request('POST', url, fields={"body": "cityId=0&shopType=&mapId=1&shopId=&language=lv_lv"}, headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36",
        "Accept": "application/json, text/javascript, */*; q=0.01",
        "Accept-Language": "lv,en-US;q=0.7,en;q=0.3",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "X-Requested-With": "XMLHttpRequest",
        "Cache-Control": "max-age=0",
        "referer": "https://www.maxima.lv/veikalu-kedes",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "x-requested-with": "XMLHttpRequest",
    })

    with open('Maxima.json', 'w', encoding='utf8') as file_handler:
        raw_json = json.loads(r.data.decode('utf-8'))
        json_data = json.dumps(raw_json, ensure_ascii=False, indent=4)
        file_handler.write(json_data)
        return True


scrap_maxima(url)
