import urllib3
import json
import re
import Geo
import os

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
        for entry in raw_json:
            props = re.findall(r'>(.*?)<', entry['info'])
            entry['address'] = props[1][2:]
            entry['phone'] = props[3][2:]
            if 'fax' in props:
                entry['fax'] = props[5][2:]

        json_data = json.dumps(raw_json, ensure_ascii=False, indent=4)

        file_handler.write(json_data)
        return True


scrap_maxima(url)


def get_maxima_class(shop):
    if shop['tag'] == 'abcf790c307391b4214df700051470d2.png':
        return 'Maxima X'
    elif shop['tag'] == 'xexpress-4257-2237.png':
        return 'Maxima Express'
    elif shop['tag'] == '10b5a0785ed38b910e5677dce6ea894f.png':
        return 'Maxima XXX'
    elif shop['tag'] == '63d9d709e7dd5772856dbc8da1b6da62.png':
        return 'Maxima XX'
    else:
        return 'Maxima'


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Maxima extracting......")
    # iterate over dictionary
    for each in data:
        lat = float(each['lat'].strip()[:17])
        lon = float(each['lng'].strip()[:17])
        coordinates = [lon, lat]
        dms_lat = Geo.fraction_to_min_sec(coordinates[1]) + " N"
        dms_lon = Geo.fraction_to_min_sec(coordinates[0]) + " E"
        X = coordinates[0]
        Y = coordinates[1]
        X1 = dms_lon
        Y1 = dms_lat
        props = dict()
        additional_props = Geo.get_info(lat, lon)
        props.update(each)
        props.update(additional_props)
        final = dict()
        props['NOSAUKUMS'] = get_maxima_class(each)
        props['SUBCATEGORY'] = 'Rimi'
        props['GRUPA'] = 'Pārtikas/mājsaimniecības preču tīklu veikali'
        props['X'] = X
        props['Y'] = Y
        props['X1'] = X1
        props['Y1'] = Y1
        final['type'] = "Feature"
        final['geometry'] = {"type": "Point", "coordinates": coordinates}
        final['properties'] = props
        most_final['features'].append(final)

    return most_final


with open('Maxima.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open(os.path.join(Geo.SAVE_PATH, "Maxima_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Maxima extracted successfully!")
