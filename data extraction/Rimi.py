import json
import requests
from bs4 import BeautifulSoup
import Geo
import os

url = "https://www.rimi.lv/veikali"


def scrap_rimi_data(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    all_scripts = soup.find_all('script')
    all_scripts = list(all_scripts)

    for text in str(all_scripts[8]).split(';'):
        if 'list' in text:
            text = text.split('=')
            raw_json_result = json.loads(text[1])
            with open('Rimi.json', 'w', encoding='utf8') as file_handler:
                json_data = json.dumps(raw_json_result, ensure_ascii=False, indent=4)
                json_data = json.loads(json_data)

                for i in json_data:
                    shop_items = soup.find('a', {'data-shop-id': i['id']})
                    if shop_items:
                        list_item = shop_items.parent.parent
                        i['full_address'] = str(list_item.select('.shop__address--desktop')[0].text).strip()
                        i['phone'] = str(list_item.select('.shop__info-value')[0].text).split(':')[1].strip()
                        i['email'] = str(list_item.select('.shop__info-value')[1].text).split(':')[1].strip()
                        days = list_item.select('.shop-hours__day')
                        times = list_item.select('.shop-hours__time')
                        opening_hours = dict()
                        for day, time in zip(days, times):
                            opening_hours[str(day.text).strip()] = str(time.text).strip()

                        i['opening_hours'] = opening_hours
                        i["google_map_url"] = list_item.find('a', {'class': 'gtm'}, href=True)['href']
                file_handler.write(json.dumps(json_data, ensure_ascii=False, indent=4))


scrap_rimi_data(url)


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Rimi extracting......")
    # iterate over dictionary
    for each in data:
        lat = float(each['latitude'].strip()[:17])
        lon = float(each['longitude'].strip()[:17])
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
        props['NOSAUKUMS'] = each['full_name']
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


with open('Rimi.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open(os.path.join(Geo.SAVE_PATH, "Rimi_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Rimi extracted successfully!")
