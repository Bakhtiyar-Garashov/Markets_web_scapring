# -*- coding: utf-8 -*-
import json
import requests
import re
import os
import Geo
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


def make_geojson(data):
    most_final = {"type": "FeatureCollection", "features": []}
    print("Mego extracting......")
    # iterate over dictionary
    for each in data:
        lat = float(each["x"].strip()[:17])
        lon = float(each["y"].strip()[:17])
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
        props['NOSAUKUMS'] = "Mego"
        props['SUBCATEGORY'] = "Mego"
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


with open('Mego.json', 'r', encoding='utf8') as f:
    data = json.loads(f.read())
    geo_out = make_geojson(data)

    with open(os.path.join(Geo.SAVE_PATH, "Mego_out.json"), "w+", encoding='utf8') as fayl:
        fayl.write(json.dumps(geo_out, ensure_ascii=False, indent=6))
        print("Mego extracted successfully!")
